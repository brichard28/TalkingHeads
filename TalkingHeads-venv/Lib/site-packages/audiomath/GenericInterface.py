# $BEGIN_AUDIOMATH_LICENSE$
# 
# This file is part of the audiomath project, a Python package for
# recording, manipulating and playing sound files.
# 
# Copyright (c) 2008-2022 Jeremy Hill
# 
# audiomath is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/ .
# 
# The audiomath distribution includes binaries from the third-party
# AVbin and PortAudio projects, released under their own licenses.
# See the respective copyright, licensing and disclaimer information
# for these projects in the subdirectories `audiomath/_wrap_avbin`
# and `audiomath/_wrap_portaudio` . It also includes a fork of the
# third-party Python package `pycaw`, released under its original
# license (see `audiomath/pycaw_fork.py`).
# 
# $END_AUDIOMATH_LICENSE$

"""
The GenericInterface submodule provides `GenericPlayer`. and
`GenericRecorder` classes. Specific interface implementations
can subclass these (for example, `PortAudioInterface`).
"""
__all__ = [
	# from here:
	'Delay', 'Fader', 'Seconds',
	'Prompt', 'WaitFor',
	# from Queueing:
	'Queue', 'QueueTest',
]

import sys
import time
import ctypes
import inspect
import weakref
import collections

from . import Dependencies;   from .Dependencies import numpy

from . import Base;           from .Base import Sound, ACROSS_SAMPLES
from . import IO;             from .IO import ffmpeg
from . import Queueing;       from .Queueing import Queue, QueueError, QueueTest

try:
	from . import accel;      from .accel import TransferAudioChunk
except Exception as error:
	TransferAudioChunk = None
	print( 'failed to import accelerator: %s' % error )

try:
	from builtins import raw_input as _input # Python 2 (for some reason just referencing `raw_input` directly gave a NameError on Python 2.7.15 on linux...)
except ImportError:
	try: from __builtin__ import raw_input as _input # Python 2 (because the line above failed on Python 2.7.10 for macOS)
	except ImportError: _input = input # Python 3
class Prompt( object ):
	def __init__( self, prompt='', catch=( KeyboardInterrupt, EOFError ) ):
		self.prompt = prompt
		self.catch = tuple( catch ) if isinstance( catch, ( tuple, list ) ) else ( catch, ) if catch else ()
	def __call__( self ):
		try: return _input( self.prompt )
		except BaseException as err:
			print( '' )
			if not isinstance( err, self.catch ): raise
			return ''

def extend_doc(*pargs):
	def doit( fn ): fn.__doc__ = fn.__doc__ % pargs; return fn
	return doit

def WaitFor( condition ):
		"""
		Sleep until `condition` is fulfilled. The `condition`
		argument may be:
			
			a `Recorder` instance:
				in which case the method waits until the
				recorder is no longer recording;
			
			a `Player` instance:
				in which case the method waits until the
				player is no longer playing;
			
			a string:
				in which case the method will print the
				string as a prompt and wait for the user
				to enter press ctrl-C on the console;
			
			any callable:
				in which case the method will repeatedly
				call `condition()` between 1-ms sleeps
				until it returns anything other than `None`.
		"""
		handle_ctrl_c = False
		def wait():
			while True:
				result = condition()
				if result is not None: break
				time.sleep( 0.001 )
			return result
		if isinstance( condition, GenericRecorder ):
			obj = condition
			condition = lambda: None if obj.recording else '%s finished recording' % obj._short_repr()
		if isinstance( condition, GenericPlayer ):
			obj = condition
			condition = lambda: None if obj.playing else '%s finished playing' % obj._short_repr()
		if isinstance( condition, str ):
			print( condition )
			condition = lambda: None
			handle_ctrl_c = True
		if handle_ctrl_c:
			try: result = wait()
			except KeyboardInterrupt: result = None
		else:
			result = wait()
		return result

class thing( object ):
	_classNamePrefix = ''
	def __str__( self ):  return self._report( with_repr='short', indent='' )
	def __repr__( self ): return self._report( with_repr='short', indent='' )
	def _short_repr( self, *p ): return '<%s%s 0x%0*X>' % ( self._classNamePrefix, self.__class__.__name__, ( 16 if sys.maxsize > 2 ** 32 else 8 ), id( self ) )
	def _super_repr( self, *p ): return object.__repr__( self )
	def _report( self, with_repr='short', indent='' ):
		s = ''
		if with_repr:
			if   with_repr in [ True, 'short' ]:   f = self._short_repr
			elif with_repr in [ 'super', 'long' ]: f = self._super_repr
			elif callable( with_repr ): f = with_repr
			else: f = object.__repr__
			s = indent + f( self ) + '\n'
			indent += '    '
		indent = ''.join( c if c.isspace() else ' ' for c in indent )
		if getattr( self, 'queue',  None ): s += self.queue._report(  with_repr=with_repr, indent=indent + 'queue  = ', short=True ) + '\n' 
		if getattr( self, 'sound',  None ): s += self.sound._report(  with_repr=with_repr, indent=indent + 'sound  = ' ) + '\n'
		if getattr( self, 'stream', None ): s += self.stream._report( with_repr=with_repr, indent=indent + 'stream = ' ) + '\n'
		rpr = lambda x: ( '%g' if isinstance( x, float ) else '%r' ) % x
		fields = 'volume muted levels pan norm'
		conditions = ', '.join( '%s=%s' % ( k, rpr( v ) ) for k in fields.split() for v in [ getattr( self, k, None ) ] if v not in [ None, '' ] )
		if conditions: s += '%s%s\n' % ( indent, conditions )
		return s.rstrip( '\n' )

class GenericPlayer( thing ):
	"""
	A `Player` provides a persistent connection to the chosen
	playback hardware, allowing a `Sound` instance to be played.
	
	A `Player` instance can only play one `Sound` at a time,
	but it can optionally maintain a list of `Sound` instances
	in a `Queue` and switch between them.  For overlapping
	sounds, use multiple `Player` instances.
	
	A `Player` instance can be created directly from a filename,
	list of filenames or filename glob pattern. The current
	`Sound` instance is available in the `.sound` property and
	the complete `Queue` is available in the `.queue` property.
	
	It is better to create a `Player` instance than to rely on
	the quick-and-dirty `.Play()` methods of the `Sound` and
	`Queue` classes---these methods just create a `Player`
	(entailing some computational overhead), wait synchronously
	for it to finish, and then destroy it again. Creating your
	own `Player` instance provides much greater flexibility
	and performance.
	"""
	
	__t0_global = [ None ]

	def __init__( self, sound=None, **kwargs ):
		self._loop = False
		self._playing = False
		self._speed = 1.0
		self._volume = 1.0
		self._levels = []
		self._pan = 0.0
		self._norm = 'inf'
		self.__synchronizeDynamics = True
		self.__autoAdvance = False

		self._nextSample = 0
		self._outputData = None
		self._outputDataParams = None
		self._outputDataPointer = None
		self._channelSub = None
		self._channelSubParams = None
		self._sampleSub = None
		self._sampleSubParams = None
		self._sampleRateEqualizationFactor = 1.0
		
		self._previousSource = None

		self._dynamics = {}		
		self._panLevels = [ 1.0, 1.0 ]
		self._muted = False
		self.__t0_synch = None
		self.__t0_unsynch = None

		self._accel = TransferAudioChunk
		self._accel_args = []
		
		self.queue = Queue( sound ) # sets .__queue and .__sound
		if kwargs: self.Set( **kwargs )

	@property
	def sound( self ):
		"""
		A reference to the `Sound` instance that the `Player`
		is currently playing, or `None`.   You can change it
		on-the-fly. It may also change automatically when
		the current sound finishes playing, if you have
		appended additional `Sound` instances the `.queue`
		and have set the `.autoAdvance` property.
		"""
		return self.__sound
	@sound.setter
	def sound( self, value ):
		self.__sound = value
		stream = getattr( self, 'stream', None )
		if value and stream:
			self._sampleRateEqualizationFactor = float( value.fs ) / stream.fs
			
	def _OutputCallback( self, t, outputData, outputSampleCount, outputChannelCount, sampleFormat ):
		if self.__t0_global[ 0 ] is None: self.__t0_global[ 0 ] = t # all players will share this t0
		if self.__t0_synch is None: self.__t0_synch = t
		if self.__t0_unsynch is None: self.__t0_unsynch = t
		if self.__synchronizeDynamics:
			runDynamics = self._playing
			if self.__synchronizeDynamics == 'playing' and not self._playing:
				self.__synchronizeDynamics = ( 'paused', t )
			elif isinstance( self.__synchronizeDynamics, tuple ) and self._playing:
				self.__t0_synch += t - self.__synchronizeDynamics[ 1 ]
				self.__synchronizeDynamics = 'playing'
			t -= self.__t0_synch
		else:
			runDynamics = True
			t -= self.__t0_unsynch
		if runDynamics and self._dynamics: self._RunDynamics( t )
		
		
		while True:
			source = self.sound
			if source is None and self.__queue:
				source = self.sound = self.__queue.currentSound
			if not source:
				self._playing = False
			if not self._playing or not self._speed:
				return outputData
				
			source = source.y
			nSamplesAvailable, nChannelsAvailable = source.shape
			
			if self._nextSample < nSamplesAvailable:
				break
			if self._loop:
				if not nSamplesAvailable: return outputData
				self._nextSample %= nSamplesAvailable
				break
				
			self._nextSample = 0
			if not self.__autoAdvance or not self.NextTrack( raiseException=False ) or self.__autoAdvance == 'pause':
				self._playing = False
		
		firstInChain = not isinstance( outputData, numpy.ndarray )
		if firstInChain:
			outputDataParams = ( outputData, outputSampleCount, outputChannelCount, sampleFormat )
			if outputDataParams == self._outputDataParams: 
				outputData = self._outputData
			else:
				obj = Exception() # just because it's the easiest-to-access built-in object that has a __dict__ and can therefore receive:
				obj.__array_interface__ = dict(
					version = 3,
					data = ( outputData, False ),
					shape = ( outputSampleCount, outputChannelCount ),
					typestr = numpy.dtype( sampleFormat ).str,
				)
				outputData = numpy.asarray( obj )
				self._outputDataParams = outputDataParams
		if self._outputData is not outputData:
			self._outputData = outputData
			self._outputDataPointer = ctypes.cast( outputData.__array_interface__[ 'data' ][ 0 ], ctypes.c_char_p )
			self._accel_args[ 0:6 ] = self._outputDataPointer, outputData.dtype.itemsize, outputData.shape[ 0 ], outputData.shape[ 1 ], outputData.strides[ 0 ], outputData.strides[ 1 ],
			self._levelsArray = ( ctypes.c_double * outputChannelCount )()
		speed = self._speed * self._sampleRateEqualizationFactor
		if self._muted: 
			left = right = 0.0
		else:
			left, right = self._panLevels
			left *= self._volume
			right *= self._volume
		levels = self._levels

		
		if self._accel and isinstance( source, numpy.ndarray ):
			### accelerated implementation
			if not self._previousSource or source is not self._previousSource():
				self._inputDataPointer = ctypes.cast( source.__array_interface__[ 'data' ][ 0 ], ctypes.c_char_p )
				self._previousSource = weakref.ref( source )
				self._accel_args[ 6:12 ] = self._inputDataPointer, source.dtype.itemsize, source.shape[ 0 ], source.shape[ 1 ], source.strides[ 0 ], source.strides[ 1 ],
			nLevels = min( len( levels ), outputChannelCount ) 
			self._levelsArray[ :nLevels ] = levels[ :nLevels ]
			self._accel_args[ 12:20 ] = self._loop, speed, self._nextSample, left, right, nLevels, self._levelsArray, firstInChain
			result = self._accel ( *self._accel_args )
			if result < 0: print( 'accelerator failed with error %g' % result )
			#if t - getattr( self, 'lastPrint', 0 ) > 1: self.lastPrint = t; print( self._accel_args )
			self._nextSample = result
			return outputData
			
		#### non-accelerated implementation from here on down
		if speed == 1.0:
			start = int( self._nextSample )
			stop = self._nextSample = start + outputSampleCount
			sampleSub = numpy.arange( start, stop )  # NB: not a slice - so it will create a copy later on
		else:
			sampleSubParams = ( outputSampleCount, speed )
			if self._sampleSubParams != sampleSubParams:
				self._sampleSubParams = sampleSubParams
				self._sampleSubBase = numpy.linspace( 0, outputSampleCount * speed, int( outputSampleCount ), endpoint=False )
			sampleSub = ( self._sampleSubBase + self._nextSample ).astype( int )
			self._nextSample += outputSampleCount * speed

		if sampleSub[ -1 ] >= nSamplesAvailable:
			if self._loop:
				sampleSub %= nSamplesAvailable
			else:
				sampleSub = sampleSub[ sampleSub < nSamplesAvailable ]
				
		chunk = source[ sampleSub, : ] # this creates a copy, because sampleSub is a sequence not a slice
		
		channelSubParams = ( outputChannelCount, nChannelsAvailable )
		if self._channelSubParams != channelSubParams:
			self._channelSubParams = channelSubParams
			if   outputChannelCount == nChannelsAvailable: self._channelSub = None
			elif outputChannelCount <  nChannelsAvailable: self._channelSub = slice( None, outputChannelCount )
			else: self._channelSub = numpy.arange( outputChannelCount ) % nChannelsAvailable
		channelSub = self._channelSub
		if channelSub is not None: chunk = chunk[ :, channelSub ]
		
		if left  != 1.0: chunk[ :, 0::2 ] *= left
		if right != 1.0: chunk[ :, 1::2 ] *= right
		if levels:
			nch = chunk.shape[ 1 ]
			if len( levels ) != nch: levels[ : ] = ( levels * nch )[ :nch ]
			chunk *= [ levels ]
			
		# TODO: should apply the appropriate scaling factor when changing formats between float and int.
		# The logic is already implemented in `snd.dat2str( data=chunk, dtype=sampleFormat )` 
		# but it really needs to happen outside this callback,  in `_wrap_portaudio._objectinterface` after data
		# from multiple players have been mixed. Also its impacts on accuracy and efficiency are untested as yet.
		if firstInChain: outputData[ :chunk.shape[ 0 ], :chunk.shape[ 1 ] ] = chunk # TODO: optimize packing of frame when created?
		else:            outputData[ :chunk.shape[ 0 ], :chunk.shape[ 1 ] ] += chunk
		return outputData
		
	
	def ResetDynamics( self, synchronized=None ):
		"""
		To restart the clock from which the dynamic properties of
		a `Player` instance `p` are computed, resetting its "time
		zero" to the current time::
		
			p.ResetDynamics()
		
		To set the `.synchronizeDynamics` policy at the same time,
		pass `True` or `False` as the input argument.
			
		To synchronize `p` to a global "time zero" that multiple
		`Player` instances can share (hence, necessarily,
		unsynchronized with respect to the playing/pausing of
		`p` itself)::
		
			p.ResetDynamics('global')
		
		See also:  `.dynamics`, `.synchronizeDynamics`
		"""
		if synchronized == 'global':
			self.synchronizeDynamics = False
			self.__t0_unsynch = self.__t0_global[ 0 ]
		else:
			if synchronized is not None: self.synchronizeDynamics = synchronized
			if self.__synchronizeDynamics: self.__t0_synch = None
			else: self.__t0_unsynch = None
	
	@classmethod
	def ResetGlobalClock( cls ):
		cls.__t0_global[ 0 ] = None

	@property
	def synchronizeDynamics( self ):
		"""
		Many `Player` properties, such as `.volume`, `.speed`,
		`.pan`, `.levels` and even `.playing`, can be dynamic,
		i.e. they can be set to functions of time `t` in seconds.
		
		If `p.synchronizeDynamics` is true, then the dynamic
		clock pauses whenever playback pauses and resumes only
		when `.playing` becomes true again. Hence, if `.playing`
		itself is dynamic and becomes false, it will not be
		able to become true again on its own. So this example
		will only play once::
		
			import audiomath as am
			p = am.Player( am.TestSound( '12' ) )
			p.Play(
				0,
				loop = True,
				synchronizeDynamics = True,
				playing = lambda t: (t / p.sound.duration) % 2 < 1,
			)
		
		If `p.synchronizeDynamics` is false, then the dynamic
		clock continues even when playback is paused. Hence,
		if `.playing` is dynamic, the `Player` can stop *and*
		resume on a schedule. So the same example, with only
		a change to the `.synchronizeDynamics` setting, will
		play repeatedly, with pauses::
		
			import audiomath as am
			p = am.Player( am.TestSound( '12' ) )
			p.Play(
				0,
				loop = True,
				synchronizeDynamics = False,
				playing = lambda t: (t / p.sound.duration) % 2 < 1,
			)
		
		A separate but related issue is that of the "time zero"
		from which dynamic time `t` is measured.  By default,
		time zero for a given `Player` instance `p` is the time
		at which `p` was created. The clock can be reset by
		using the `.ResetDynamics()` method.  You can also
		synchronize `p` with a global clock, available to all
		`Player` instances, by saying `p.ResetDynamics('global')`
		
		See also:  `.dynamics`, `.ResetDynamics()`
		"""
		return True if self.__synchronizeDynamics else False
	@synchronizeDynamics.setter
	def synchronizeDynamics( self, value ):
		if value:
			if self.__synchronizeDynamics: return
			self.__synchronizeDynamics = 'playing'
			self.__t0_synch = None
		else:
			if not self.__synchronizeDynamics: return
			self.__synchronizeDynamics = False
			self.__t0_unsynch = None
				
	@property
	def dynamics( self ):
		"""
		Many `Player` properties, such as `.volume`, `.speed`,
		`.pan`, `.levels` and even `.playing`, support "dynamic
		value assignment".  This means you can do something
		like the following::
		
			import audiomath as am
			p = am.Player(am.TestSound('12'), loop=True)
			
			p.volume = lambda t: min( 1.0, t / 5.0 )
			
			p.Play()
		
		When queried, `p.volume` still appears to be a
		floating-point number, but this value changes as a
		function of time `t` in seconds---in this example,
		the volume fades up from 0.0 to 1.0 over the course
		of five seconds.
		
		Dynamic functions are called automatically in the
		streaming callback. You should take care to make
		them as computationally lightweight and efficient
		as possible. Your functions may accept 0, 1 or 2
		arguments.  If they accept 1 argument, it is always
		time in seconds. If they accept 2 arguments, these
		will be the `Player` instance first, followed by
		time in seconds.
		
		Time `t` may be synchronized with, or independent
		of, the playing/pausing status of the `Player`
		itself, according to the `.synchronizeDynamics`
		property. "Time zero" may be reset, or synchronized
		with other players, using `.ResetDynamics()`.
		
		Dynamic functions may choose to terminate and remove
		themselves, by saying `raise StopIteration()` or
		even `raise StopIteration(final_property_value)`
		
		See also:
			`.synchronizeDynamics`,
			`.ResetDynamics()`,
			`.GetDynamic()`,
			`.SetDynamic()`
		"""
		return collections.OrderedDict( ( name, func ) for order, name, func, nArgs in sorted( self._dynamics.values() ) )
	
	@property
	def playing( self ):
		"""
		This boolean property reflects, and determines, whether
		the `Player` is currently playing or paused.
		
		`.playing` is a dynamic property (see `.dynamics`).
		"""
		return self._playing
	@playing.setter
	def playing( self, value ):
		if self.SetDynamic( 'playing', value if callable( value ) else None ): return
		self._playing = value
	
	@property
	def loop( self ):
		"""
		This boolean-valued property determines whether the
		current sound should wrap around to the beginning when
		it finishes playing (NB: if you are looping, you will
		stay on the current `.sound` and never advance through
		the `.queue`).
		
		`.loop` is a dynamic property (see `.dynamics`).
		"""
		return self._loop
	@loop.setter
	def loop( self, value ):
		if self.SetDynamic( 'loop', value if callable( value ) else None ): return
		self._loop = value
	
	@property
	def speed( self ):
		"""
		This floating-point property determines the speed at
		which the sound should be played. Normal speed is 1.0
		
		`.speed` is a dynamic property (see `.dynamics`).
		"""
		return self._speed
	@speed.setter
	def speed( self, value ):
		if self.SetDynamic( 'speed', value if callable( value ) else None ): return
		self._speed = float( value )
		
	@property
	def volume( self ):
		"""
		This floating-point property is a multiplier for the
		amplitude of the sound waveforms.  It is independent
		of (i.e. its effect simply gets multiplied by the
		effects of) other properties that affect channel-to-
		channel level differences, such as `.levels` and `.pan`
		
		`.volume` is a dynamic property (see `.dynamics`).
		"""
		return self._volume
	@volume.setter
	def volume( self, value ):
		if self.SetDynamic( 'volume', value if callable( value ) else None ): return
		self._volume = float( value )
	vol = volume
	
	@property
	def muted( self ):
		"""
		This is a boolean property that, if true, causes the
		`Player` to be silent, independent of the current
		`.volume` and/or `.levels`.
		
		`.muted` is a dynamic property (see `.dynamics`).
		"""
		return self._muted
	@muted.setter
	def muted( self, value ):
		if self.SetDynamic( 'muted', value if callable( value ) else None ): return
		self._muted = bool( value )
	
	@property
	def levels( self ):
		"""
		This is an optional sequence of multipliers applied
		to each channel in turn. It is independent of (i.e. its
		effects simply get multiplied by the effects of) other
		properties that affect intensity, such as `.volume`
		and `.pan`
		
		`.levels` is a dynamic property (see `.dynamics`).
		"""
		return self._levels
	@levels.setter
	def levels( self, value ):
		if self.SetDynamic( 'levels', value if callable( value ) else None ): return
		try: len( value )
		except: value = [ float( value ) ]
		else: value = [ float( each ) for each in value ]
		self._levels[ : ] = value

	@property
	def pan( self ):
		"""
		A value of -1 means left channels only, right channels silent.
		A value of 0 means left and right channels at equal volume.
		A value of +1 means right channels only, left channels silent.
		
		The way levels are computed from scalar values between -1 and
		+1 depends on `.norm`. Alternatively, you can supply a two-
		element sequence that explicitly specifies `[left, right]`
		levels.
		
		Note that these levels are independent from (i.e. they are
		simply multiplied by) the overall `.volume` and channel-by-
		channel `.levels` settings.
		
		`.pan` is a dynamic property (see `.dynamics`).
		"""
		return self._pan
	@pan.setter
	def pan( self, value ):
		if self.SetDynamic( 'pan', value if callable( value ) else None ): return
		try: len( value )
		except: pass
		else: self._panLevels[ : ] = float( value[ 0 ] ), float( value[ 1 ] ); return
		self._pan = float( value )
		self._UpdatePanLevels( pan=value )

	@property
	def norm( self ):
		"""
		For a `Player` instance `p`, if you set `p.pan` to a scalar
		value between -1 and +1, the relative levels of left and right
		channels are computed such that::
		
			left ** p.norm + right ** p.norm = 1
		
		The value `p.norm=2` produces a natural-sounding pan but it
		means that stereo sounds are reduced to 70.71% of their
		maximum amplitude by default.  So instead, the default is
		to use the infinity-norm, `p.norm='inf'`, which ensures that
		the larger of the two sides is always 1.0
		"""
		return self._norm
	@norm.setter
	def norm( self, value ):
		if self.SetDynamic( 'norm', value if callable( value ) else None ): return
		self._norm = value
		self._UpdatePanLevels( norm=value )
		
	def _UpdatePanLevels( self, pan=None, norm=None ):
		if pan  is None: pan  = self._pan
		if norm is None: norm = self._norm
		if norm is None or pan is None: return
		v = [ 0.5 + 0.5 * min( 1.0, max( -1.0, vi ) ) for vi in [ -pan, pan ] ]
		if 'inf' in str( norm ).lower():  denom = abs( max( v, key=abs ) )
		else: denom = sum( vi ** norm for vi in v ) ** ( 1.0 / norm if norm else 1.0 )
		if denom: v = [ vi / float( denom ) for vi in v ]
		self._panLevels[ : ] = v
	
	def GetDynamic( self, name ):
		"""
		For dynamic properties, return the actual callable object
		that generates property values, rather than the current
		static value.

		Args:
			name (str): Name of the property

		Returns:
			Callable object responsible for generating values for
			the named property (or `None` if there is no such
			dynamic).
			
		Example::
			
			import audiomath as am, numpy as np
			p = am.Player(am.TestSound('12'), loop=True, playing=True)
			p.volume = lambda t: 0.5+0.5*np.sin(2.0*np.pi*t*0.25)
			v = p.volume                # this retrieves a float
			f = p.GetDynamic('volume')  # this retrieves the lambda 
		"""
		dynamics = getattr( self, '_dynamics', None )
		return dynamics.get( name, None ) if dynamics else None
		
	def SetDynamic( self, name, func, order=1 ):
		"""
		Associate a "dynamic" (i.e. a function that can be called
		repeatedly to set an attribute) with the name of an
		attribute.

		For example::

				foo.Set( 'bar',  lambda t: t ** 2 )

		This will set `foo.bar` to `t ** 2`  every time the method
		`foo._RunDynamics( t )` is called (this call will happen
		automatically from the API user's point of view, in the
		object's infrastructure implementation).

		If the `.bar` attribute happens to have been already
		configured as a "dynamic property" this means it supports
		"dynamic value assignment", i.e. you can do::

				foo.bar = lambda t: t ** 2
		
		as a syntactic shorthand for `.SetDynamic()`---the setter
		will detect the fact that the value is callable, and divert
		it to the register of 	dynamics rather than assigning it
		directly (so the actual static value you get from querying
		`foo.bar` will not immediately change).

		Args:
			name (str)
				name of the attribute
			func
				callable object, or `None` to remove any dynamic that may
				already be associated with `name`
			order (int, float)
				optional numeric ordering key that allows you to control the
				serial order in which dynamics are evaluated

		Returns:
				`self`
		
		See also:  `.GetDynamic()`, `.GetDynamics()`, `.ClearDynamics()`
		"""
		dynamics = getattr( self, '_dynamics', None )
		if not hasattr( self, name ): setattr( self, name, None )
		if func is None:
			if dynamics: dynamics.pop( name, None )
		else:
			if dynamics is None: dynamics = self._dynamics = {}
			try: getargspec = inspect.getfullargspec
			except: getargspec = inspect.getargspec
			try: spec = getargspec( func )
			except: spec = getargspec( func.__call__ )
			nArgs = len( spec.args )
			if hasattr( func, '__self__' ): nArgs -= 1
			elif not inspect.isfunction( func ) and not inspect.ismethod( func ): nArgs -= 1  # callable custom instance: won't have a __self__ itself but its __call__ method will
			if nArgs == 0 and spec.varargs: nArgs = 1
			dynamics[ name ] = ( order, name, func, nArgs )
			return func
	
	def _RunDynamics( self, t ):
		#dynamics = getattr( self, '_dynamics', None )
		#if dynamics is None: dynamics = self._dynamics = {}
		dynamics = self._dynamics
		updates = {}
		for entry in sorted( dynamics.values() ):
			order, name, func, nArgs = entry
			try:
				if nArgs == 0: value = func()
				elif nArgs == 1: value = func( t )
				elif nArgs == 2: value = func( self, t )
				else: raise TypeError( 'dynamic property values should take 0, 1 or 2 arguments' )
			except StopIteration as exc:
				value = None
				for arg in exc.args:
					if isinstance( arg, dict ):
						if value is None: value = arg.pop( '_', None )
						updates.update( arg )
					else: value = arg
				if value is None: dynamics.pop( name )
				else: setattr( self, name, value )
			except:
				einfo = sys.exc_info()
				sys.stderr.write( 'Exception while evaluating dynamic .%s property of %s:\n' % ( name, self ) )
				getattr( self, '_excepthook', sys.excepthook )( *einfo )
				dynamics.pop( name )
			else:
				setattr( self, name, value )
				dynamics[ name ] = entry
		if updates:
			for name, value in updates.items():
				setattr( self, name, value )

	def Set( self, **kwargs ):
		"""
		Set the values of multiple attributes or properties in
		one call. An error will be raised if you try to set the
		value of a non-existent attribute.

		Note that the `.Play()` and `.Pause()` methods also
		allow you to set arbitrary properties prior to their
		manipulation of `.playing` status.

		Returns:
			`self`

		Example::

			p.Set( head=0, loop=True, volume=0.5 )
		"""
		for k, v in kwargs.items():
			if not hasattr( self, k ): raise AttributeError( '%s instance has no attribute %r' % ( self.__class__.__name__, k ) )
			setattr( self, k, v )
		return self
	
	def Resample( self, newFs, wholeQueue=True ):
		"""
		Replace `self.sound` with a copy resampled at the
		new sampling rate `newFs`.  Also adjust the Player's
		internal speed compensation factor, to ensure things
		sound the same on the existing stream. The most
		common usage will be to match the sound sample rate
		to the sample rate of the hardware (so the Player's
		compensation factor becomes 1.0) to ensure more
		efficient playback.
		"""
		# TODO: does not handle multiple sounds in the self.queue... what to do - create a whole deep copy of the Queue?
		if hasattr( newFs, 'fs' ): newFs = newFs.fs
		originalLoadedSound = self.sound
		if wholeQueue:
			for i, sound in enumerate( self.queue ):
				wasLoaded = sound is originalLoadedSound
				sound = self.queue[ i ] = sound.Copy().Resample( newFs )
				if wasLoaded: self.sound = sound
		if self.sound is originalLoadedSound: # still, for whatever reason
			self.sound = self.sound.Copy().Resample( newFs )
		
	def Play( self, position=None, wait=False, **kwargs ):
		"""
		Start playing. Optionally use `position` to specify
		the exact `.head` position from which to start playing
		(in seconds from the beginning of the current `.sound`).
		Otherwise playack starts from wherever it last ended up
		(or at the beginning, if the sound previously ran to the
		end).
		
		If you call `p.Play()` without an explicit `position`
		on an instance `p` that is *already* playing, nothing
		changes---playback simply continues. In this sense it
		is equivalent to manipulating the `.playing` property
		by saying `p.playing = True`.
		 
		If `wait` is true, immediately call `.Wait()` so that
		playback is synchronous.
		
		Optionally, use further keyword arguments to set
		additional properties (e.g. `volume`, `pan`, `levels`,
		`speed`, `loop`, `.track`, etc) at the same time.
		"""
		if position is not None: self.Seek( position )
		if kwargs: self.Set( **kwargs )
		self._playing = True
		if wait: self.Wait()
		#return self
		
	def Pause( self, position=None, **kwargs ):
		"""
		Stop playing. Optionally change the `.head` position
		to the specified absolute `position` in seconds, ready
		for subsequent playback. Optionally, use keyword
		arguments to set additional properties (e.g. `volume`,
		`pan`, `levels`, `speed`, `loop`, etc) at the same time.
		"""
		if position is not None: self.Seek( position )
		if kwargs: self.Set( **kwargs )
		self._playing = False
		#return self
	Stop = Pause
	
	def Wait( self ):
		"""
		Sleep until `self` stops playing, or until the user
		presses ctrl-C to interrupt.
		"""
		try: self.WaitFor( self )  # ownself wait for ownself lah!
		except KeyboardInterrupt: self.playing = False

	@extend_doc( WaitFor.__doc__ )
	def WaitFor( self, condition, finalPlayingStatus=None ):
		"""%s
		
		If `finalPlayingStatus` is not `None`, then
		`self.playing` is set to its value when the wait
		is over.  So for example, you can prompt a user
		to end ongoing playback as follows::
		
			p.WaitFor('Press ctrl-C to stop playing: ', finalPlayingStatus=False)
			
		"""
		result = WaitFor( condition )
		if finalPlayingStatus is not None:
			self.playing = finalPlayingStatus
		return result

	def Seek( self, position, relative=False ):
		"""
		Move the playback `.head` to the specified `position`
		in seconds. Negative values count back from the end of
		`self.sound`. If `relative` is true, `position` is
		interpreted as an offset relative to the current head
		position. The following are equivalent::
		
			p.Seek( 5.0, relative=False )  # more efficient
			p.head = 5.0
		
		And the following are also equivalent::
		
			p.Seek( -2.0,  relative=True ) # more efficient
			p.head -= 2.0
		"""
		samples = int( round( self.sound.fs * position ) )
		if relative: self._nextSample = max( 0, self._nextSample + samples )
		else: self._nextSample = ( self.sound.NumberOfSamples() + samples ) if samples < 0 else samples
		return self
	
	@property
	def head( self ):
		"""
		Current playback position, in seconds relative to the
		beginning.
		
		You can change the playback position by assigning to
		`.head`, but note that it is fractionally faster/more
		efficient to do this by calling the `.Seek()` method. 
		"""
		if not self.sound: return 0.0
		return self._nextSample / self.sound.fs
	@head.setter
	def head( self, value ):
		self.Seek( value, relative=False )

	@property
	def queue( self ):
		"""
		This special sequence of class `Queue` provides a list of
		`Sound` instances between which the `Player` may switch.
		
		The `Player` instance's `.repeatQueue` and `.autoAdvance`
		properties allow you to specify how the queue is used when
		a given `Sound` finishes playing.  The `.track` property
		allows you to jump immediately to a given place in the queue.
		
		NB: direct manipulation of the queue, for example using
		its own methods `self.queue.Forward()` or `self.queue.Back()`,
		will *not* affect whichever `self.sound` is currently loaded
		into the `Player`, but they will affect what happens when
		that sound has finished playing.  If you want to change tracks
		with immediate effect, you should instead use corresponding
		`Player` methods `self.NextTrack()` or `self.PreviousTrack()`,
		or manipulate the property `self.track`.
		
		See also:
			`.autoAdvance`, `.repeatQueue`, `.track`,
			`.NextTrack()`, `.PreviousTrack()`
		"""
		return self.__queue
	@queue.setter
	def queue( self, value ):
		self.__queue = Queue( value )
		self.sound = self.__queue.currentSound

	@property
	def track( self ):
		"""
		If there are multiple items in the `.queue`, this
		property allows you to switch between them.  You
		may use an integer zero-based index,  a `Sound`
		instance, or the string `.label` of that instance
		(provided the instance is already in the `.queue`)
		
		`.track` is a dynamic property (see `.dynamics`).
		
		See also:
			`.autoAdvance`, `.queue`, `.repeatQueue`,
			`.NextTrack()`, `.PreviousTrack()`
		"""
		return self.__queue.position
	@track.setter
	def track( self, value ):
		if self.SetDynamic( 'track', value if callable( value ) else None ): return
		self.SwitchToTrack( value, raiseException=True )
	
	@property
	def autoAdvance( self ):
		"""
		This property may take the following values:
		
		`False`:
			when the current `.sound` finishes playing,
			rewind the `.head` to the start of the current 
			sound but do not advance through the `.queue`.
		
		`True` or `'play'`:
			when the current `.sound` finishes playing,
			continue to the next `Sound` instance in the
			`.queue`, if any.
		
		`'pause'`:
			when the current `.sound` finishes playing, advance
			to the next `Sound` instance in the `.queue`, if
			any, but pause playback.
		
		`.autoAdvance` is a dynamic property (see `.dynamics`).
		
		See also:
			`.queue`, `.repeatQueue`, `.track`,
			`.NextTrack()`, `.PreviousTrack()`
		"""
		return self.__autoAdvance
	@autoAdvance.setter
	def autoAdvance( self, value ):
		if self.SetDynamic( 'autoAdvance', value if callable( value ) else None ): return
		if isinstance( value, str ): value = value.lower()
		acceptable = [ False, True, 'play', 'pause' ]
		if value not in acceptable:
			raise ValueError( 'invalid value %r for .autoAdvance---acceptable values are %s' % ( value, '/'.join( repr( x ) for x in acceptable ) ) )
		self.__autoAdvance = value
	
	@property
	def repeatQueue( self ):
		"""
		This boolean property is a shortcut to the sub-property
		`self.queue.loop`. If true, then moving beyond either end
		of the `.queue` causes a wrap-around to the other end.
		
		`.repeatQueue` is a dynamic property (see `.dynamics`).
		
		See also:
			`.autoAdvance`, `.queue`, `.track`,
			`.NextTrack()`, `.PreviousTrack()`
		"""
		return self.__queue.loop
	@repeatQueue.setter
	def repeatQueue( self, value ):
		if self.SetDynamic( 'repeatQueue', value if callable( value ) else None ): return
		self.__queue.loop = bool( value )

	def SwitchToTrack( self, position, raiseException=True, allowNegative=True ):
		"""
		Immediately jump to the sound at the given position
		in the `.queue` (equivalent to setting the `.track`
		property).
		"""
		previousPosition = self.__queue.position
		try:
			nextSound = self.__queue.SetPosition( position, allowNegative=allowNegative ).currentSound
			if self.__queue.position == previousPosition: return self.__sound
		except QueueError:
			if raiseException: raise
			nextSound = None
		self._nextSample = 0
		if nextSound: self.sound = nextSound
		else: self._playing = False
		return nextSound

	def NextTrack( self, count=1, raiseException=True ):
		"""
		Jump to the beginning of the next track in the `.queue`
		and return the corresponding `Sound` instance.
		
		If this entails going beyond the last track, raise an
		exception unless `raiseException=False` (in which case
		go to the beginning of the last track, stop playing, 
		and return `None`).
		"""
		return self.SwitchToTrack( self.__queue.position + count, raiseException=raiseException, allowNegative='loop' )

	def PreviousTrack( self, count=1, raiseException=True ):
		"""
		Jump to the beginning of the track prior to the current one
		in the `.queue` and return the corresponding `Sound`
		instance.
		
		If this entails going back beyond the beginning, raise an
		exception unless `raiseException=False` (in which case go
		to the beginning of the first track, stop playing, and
		return `None`).

		Unlike the "back" button on your music player, this
		does *not* go to the beginning of the current track before
		skipping to the previous track.  To restart the current
		track, use `p.Play(0)` or `p.Seek(0)` or `p.head = 0`
		"""
		return self.SwitchToTrack( self.__queue.position - count, raiseException=raiseException, allowNegative='loop' )


class GenericRecorder( thing ):
	"""
	A `Recorder` provides a persistent connection to the chosen
	recording hardware, allowing sound to be recorded into a
	`Sound` instance.
	
	You may find it more useful to use the global function
	`Record`, which synchronously records and returns a `Sound`
	instance, than to create or interact directly with `Recorder`
	instances. However, `Recorder` instances are the way to
	go if you want to record asynchronously, in the background.
	"""

	def __init__( self, seconds, fs=44100, nChannels=1, filename=None, sampleFormat='float32', start=True, **kwargs ):
		if isinstance( seconds, Sound ): self.sound = seconds
		else: self.sound = Sound( seconds, fs=fs, nChannels=nChannels )
		self._numberOfChannels = self.sound.NumberOfChannels()
		self._nextSample = 0
		self.recording = start
		self.__loop = False
		self.__hasLooped = False
		self.__array_interface__ = dict( version=3, typestr=sampleFormat )
		self.hook = None
		self.auto_dispose_hook = False
		if filename:
			self.hook = ffmpeg( filename, self, nChannels=self._numberOfChannels )
			self.auto_dispose_hook = 'not started yet'
			# NB: we do this because the audio data won't get fully flushed to the file
			# until `self.hook` is garbage-collected. The `MakeRecording` class method
			# (presented as the global `Record()` function) does `.Stop(hook=None)` to
			# ensure this, but now there's a new mechanism in the input callback, below,
			# to make it happen for 

		self.Set( **kwargs )
	
	@property
	def loop( self ):
		"""
		A boolean property. If this is `True`, treat `self.sound`
		as a circular buffer and record into it indefinitely (use
		the `.Cut() method to extract the recorded data in the
		correct order).   If this is `False`, the recorder will
		simply stop recording when the capacity of `self.sound`
		is reached. 
		"""
		return self.__loop
	@loop.setter
	def loop( self, value ):
		if not ( value and self.__loop ): self.__hasLooped = False 
		self.__loop = bool( value )
	
	def _InputCallback( self, t, inputData, frameCount, nInputChannels ):
		if self.recording:
			self.__array_interface__[ 'data' ]  = ( inputData, True )
			self.__array_interface__[ 'shape' ] = ( frameCount, nInputChannels )
			pos = self._nextSample
			samplesAllocated = self.sound.y.shape[ 0 ]
			src = incoming = numpy.array( self ) # TODO: could cache/streamline this like _OutputCallback
			if self.hook:
				if self.auto_dispose_hook == 'not started yet': self.auto_dispose_hook = 'started'
				result = self.hook( src, pos, self.sound.fs )
				if result is not None: src = result
			while True:
				dst = self.sound.y[ pos : pos + frameCount, : ]
				srcSamples, srcChannels = src.shape
				dstSamples, dstChannels = dst.shape
				if   srcChannels < dstChannels: dst = dst[ :, :srcChannels ]
				elif srcChannels > dstChannels: src = src[ :, :dstChannels ]
				if   srcSamples  < dstSamples:  dst = dst[ :srcSamples,  : ]
				elif srcSamples  > dstSamples:  src = src[ :dstSamples,  : ]
				dst.flat = src.flat
				self._nextSample += dst.shape[ 0 ]
				if self._nextSample >= samplesAllocated:
					pos = self._nextSample = 0
					if self.__loop:
						src = incoming[ dstSamples:, : ]
						frameCount -= dstSamples
						self.__hasLooped = True
						if frameCount > 0: continue
					else:
						self.recording = False
				break
		elif self.hook and self.auto_dispose_hook in [ True, 'started' ]:
			if self.auto_dispose_hook == 'started': self.auto_dispose_hook = 'not started yet'
			self.hook = None
			
	def Record( self, position=None, wait=False, **kwargs ):
		"""
		Start recording.  If `position` is specified,
		move the recording `.head` to that position,
		expressed in seconds from the beginning, before
		starting. If `wait` is true, `Wait()` until the
		end, or until the user presses ctrl+C.
		"""
		if position is not None: self.Seek( position )
		self.Set( **kwargs )
		self.recording = True
		if wait: self.Wait()
	Start = Record
		
	def Pause( self, position=None, **kwargs ):
		"""
		Stop recording.  If `position` is specified,
		move the recording `.head` to that position,
		expressed in seconds from the beginning.
		"""
		if position is not None: self.Seek( position )
		self.Set( **kwargs )
		self.recording = False
	Stop = Pause
		
	def Wait( self ):
		"""
		Sleep until `self.recording` is no longer true.
		This will occur when the allocated recording
		time is exhausted, or if the user presses ctrl+C
		in the meantime.
		"""
		try: self.WaitFor( self )  # ownself wait for ownself lah!
		except KeyboardInterrupt: self.recording = False
	
	@extend_doc( WaitFor.__doc__ )
	def WaitFor( self, condition, finalRecordingStatus=None ):
		"""%s
		
		If `finalRecordingStatus` is not `None`, then
		`self.recording` is set to its value when the wait
		is over.  So for example, you can prompt a user
		to end an ongoing recording as follows::
		
			r.WaitFor('Press ctrl-C to stop recording: ', finalRecordingStatus=False)
			
		"""
		result = WaitFor( condition )
		if finalRecordingStatus is not None:
			self.recording = finalRecordingStatus
		return result
		
	def Set( self, **kwargs ):
		"""
		Set the values of multiple attributes or properties in
		one call. An error will be raised if you try to set the
		value of a non-existent attribute.

		Returns:
			`self`

		Example::

			p.Set( head=0, recording=True )
		"""
		for k, v in kwargs.items():
			if not hasattr( self, k ): raise AttributeError( '%s instance has no attribute %r' % ( self.__class__.__name__, k ) )
			setattr( self, k, v )
		return self
	
	def Seek( self, position, relative=False ):
		"""
		Move the recording `.head` to the specified `position`
		in seconds. Negative values count back from the end of
		the available recording space in `self.sound`. If
		`relative` is true, `position` is interpreted as an
		offset relative to the current head position. The
		following are equivalent::
		
			r.Seek( 5.0, relative=False )  # more efficient
			r.head = 5.0
		
		And the following are also equivalent::
		
			r.Seek( -2.0,  relative=True ) # more efficient
			r.head -= 2.0
		"""
		samples = int( round( self.sound.fs * position ) )
		if relative: self._nextSample = max( 0, self._nextSample + samples )
		else: self._nextSample = self.sound.NumberOfSamples() + samples if samples < 0 else samples
		if not relative: self.__hasLooped = False
		return self
	
	@property
	def head( self ):
		"""
		Current recording position, in seconds relative to the
		beginning.
		"""
		return self._nextSample / self.sound.fs
	@head.setter
	def head( self, value ):
		self.Seek( value, relative=False )
		
	def Cut( self, position=None ):
		"""
		Stop recording, and return the portion of `self.sound`
		that has been recorded so far, up to the current `.head`
		position (or the explicitly specified `position` in
		seconds), as a new `Sound` instance.
		"""
		self.recording = False
		if position is None: position = self.head
		position = float( position )
		if position == 0: return self.sound # must have either stopped naturally and automatically rewound, or not started at all
		elif self.__hasLooped: return self.sound[ position: ] % self.sound[ :position ]
		else: return self.sound[ :position ]

	def ReadSamples( self, startPositionInSamples, nSamples ):
		"""
		Read the specified number of samples and return
		them as a `numpy` array. If necessary, wait until
		the requisite number of samples has been recorded.
		If `self.loop==False`, then this method may return
		fewer samples than you ask for if the recording
		reaches, or has already reached, the end of the
		space allocated in `self.sound`. Otherwise, the
		wraparound calculations will be handled
		automatically and the return value will have the
		requested number of samples in chronological order.
		"""
		snd = self.sound
		nAvailable = snd.nSamples
		y = snd.y
		target = startPositionInSamples + nSamples
		if not self.__loop: target = min( target, nAvailable )
		while self._nextSample < target: time.sleep( 0.001 )
		if self.__loop: startPositionInSamples %= nAvailable
		slices = [ slice( None ), slice( None ) ]
		slices[ ACROSS_SAMPLES ] = slice( startPositionInSamples, startPositionInSamples + nSamples )
		segment = y[ tuple( slices ) ]
		looped = nSamples - segment.shape[ ACROSS_SAMPLES ] if self.__loop else 0
		if looped:
			slices[ ACROSS_SAMPLES ] = slice( None, looped )
			segment = numpy.concatenate( [ segment, y[ tuple( slices ) ] ], axis=ACROSS_SAMPLES )
		return segment	

	@classmethod
	def MakeRecording( cls, space=60, prompt=None, verbose=None, cut=True, nChannels=None, filename=None, **kwargs ):
		"""
		Record and return a `Sound` synchronously. Slightly easier
		than creating your own `Recorder` instance and working with
		that (which is what you would have to do if you want to
		record asynchronously).
		
		Args:
			space (Sound, float):
				specifies either a pre-existing `Sound` instance
				into which to record,  or a number of seconds. In
				the latter case a `Sound` instance is created, pre-
				allocated with the specified amount of space in
				seconds.
			
			prompt (None, bool, str, function):
				if this is left as `None`, a default string is
				composed. If `prompt` is a string, it is printed
				to the console and the `Recorder` waits until it
				has finished (or until ctrl-C is pressed).
				Alternatively, supply a callable whose non-`None`
				return value signals that the recording should end.			
				
			verbose (bool):
				Passed through to the constructor of the `Recorder`
				object that is being used.
			
			cut (bool):
				If true, return a `.Cut()` version of the `Sound`
				when recording stops---i.e. ensure that the
				duration of the `Sound` does not exceed the
				duration of the recording.  If false, the entire
				pre-allocated `space` is returned, with the
				recording at the beginning.
				
			nChannels (int):
				Optionally specify the number of channels to record
				(some APIs have crazy defaults, like ALSA's 32
				channels - if you're not using one of those APIs,
				you probably don't need this).

			filename (str):
				Optionally, use the `ffmpeg` class to stream the
				recorded content to the specified file. This
				requires the `ffmpeg` binary to be (separately)
				installed---see the `ffmpeg` class documentation.
			
			**kwargs:
				Additional keyword arguments are passed through to
				the constructor of the `Recorder` object (for example,
				to specify the `device` that should be used).
		
		Examples::
		
		    import audiomath as am
		    
		    s = am.Record()
		    # this records for up to 60 seconds (less if ctrl-C
		    # is pressed) and returns a `Sound` instance containing
		    # the recorded data.

		    s2 = am.Record(10, loop=True, filename='blah.mp3')
		    # this records indefinitely into a 10-second circular
		    # buffer, streaming the recorded data all the while into
		    # the file `blah.mp3`, and when you press ctrl-C it
		    # stops, cleans up, and returns the last 10 seconds as
		    # a `Sound` instance.
		"""
		r = cls( seconds=space, start=True, verbose=verbose, filename=filename, nChannels=nChannels, **kwargs )
		if not prompt and r.verbose:
			prompt = None
		if prompt in ( None, True ):
			if r.loop: prompt = 'Recording - press ctrl + C to end'
			else: prompt = 'Recording for {duration:g} seconds - press ctrl + C to finish early'
		# Don't attempt to replace ctrl+C with an input() - when the recording runs out of
		# space, we want control to return to the console without waiting for the user
		if not prompt or isinstance( prompt, str ):
			if prompt: print( prompt.format( duration=r.sound.Duration() ) )
			r.Wait()
		else:
			r.WaitFor( prompt, finalRecordingStatus=False )
		r.Stop( hook=None )
		return r.Cut() if cut else r.sound

class Delay( object ):
	"""
	A callable object that can be assigned to one of the
	dynamic properties of a `Player`. It returns its
	`initialValue` until the specified number of `seconds`
	has elapsed, then raises a `StopIteration` exception
	containing its `finalValue`. This will be caught by
	the `Player`, causing it to replace the dynamic with
	the specified final static value.
	
	The following example causes a `Player` object to
	start playing automatically after a delay::
	
	    import audiomath as am
	    p = am.Player(am.TestSound('12'), synchronizeDynamics=False)
	    
	    p.playing = am.Delay(5) # will start playing 5 seconds from now
	    
	
	"""
	def __init__( self, seconds, initialValue=False, finalValue=True ):
		self.t0 = None
		self.seconds = seconds
		self.initialValue = initialValue
		self.finalValue = finalValue
	def __call__( self, t ):
	 	if self.t0 is None:
	 		self.t0 = t
	 	t -= self.t0
	 	if t < self.seconds:
	 		return self.initialValue
	 	raise StopIteration( self.finalValue )

class Fader( object ):
	"""
	A callable object that can be assigned to one of the
	dynamic properties of a `Player` to smoothly transition
	from a `start` to an `end` value. It is a self-
	terminating dynamic: when the transition is finished,
	it will raise a `StopIteration` exception, which will
	be caught by the `Player`, causing it to replace the
	dynamic with a final static value.
	
	Example::
	
		import time, audiomath as am
		p = am.Player(am.TestSound('12'))
		fadeIn = am.Fader(3.0, start=0, end=1)
		p.Play(loop=1, volume=fadeIn) # fade in
		time.sleep(6.0)               # wait for fade-in, then
		                              # stay constant for a few seconds
		p.volume = am.Fader(3.0)      # fade out, then stop.
		
	"""	
	def __init__( self, duration=1.0, start=1, end=0, transform=None, pauseWhenDone='auto' ):
		"""
		Args:
			duration (float):
				duration of the transition, in seconds
			start (float, numpy.ndarray):
				start value
			end (float, numpy.ndarray):
				end value
			transform:
				an optional function through which to transform
				`start`, `end` and any value linearly interpolated
				between them.
			pauseWhenDone:
				if `True`, `.Pause()` the `Sound` when the
				transition is finished.  If `False`, do not.
				A value of `'auto'`, means "pause the sound when
				the transition is finished if the `end` value is
				zero".
			
		"""
		self.t0 = None
		self.start = start
		self.end = end
		self.duration = duration
		self.transform = transform
		if pauseWhenDone == 'auto': pauseWhenDone = ( end == 0 )
		self.pauseWhenDone = pauseWhenDone
		
	def __call__( self, t ):
	 	if self.t0 is None:
	 		self.t0 = t
	 	t -= self.t0
	 	if t <= self.duration:
	 		terminate = False
	 		value = self.start + ( self.end - self.start ) * ( t / self.duration )
	 	elif self.pauseWhenDone:
	 		raise StopIteration( dict( playing=False ) )
	 	else:
	 		terminate = True
	 		value = self.start * 0 + self.end
	 	if self.transform:
	 		value = self.transform( value )
	 	if terminate:
	 		raise StopIteration( value )
	 	return value

# Precision time measurement
# First set some (non-Windows) fallbacks before replacing them with Windows API calls below
# TODO: verify/improve precision on non-Windows platforms?
try:    Seconds = time.monotonic   # only available in Python 3.3+
except: Seconds = time.time        # last resort - vulnerable to system clock updates over network
if sys.platform.lower().startswith( 'win' ):
	LARGE_INTEGER = ctypes.c_int64
	byref = ctypes.byref
	TIMEBASE = LARGE_INTEGER()
	ctypes.windll.kernel32.QueryPerformanceFrequency( byref( TIMEBASE ) )
	TIMEBASE = float( TIMEBASE.value )
	QueryPerformanceCounter = ctypes.windll.kernel32.QueryPerformanceCounter
	def Seconds():
		"""
		A high-precision timer based on `QueryPerformanceCounter`
		in the Windows API.  Origin (time zero) is arbitrary, but
		fixed within a given Python session.
		"""
		counter = LARGE_INTEGER()
		QueryPerformanceCounter( byref( counter ) )
		return 	counter.value / TIMEBASE
