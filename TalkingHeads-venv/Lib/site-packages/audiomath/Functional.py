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
Provides a `Synth` class allowing `Sound` content to be
functionally generated on-the-fly.
"""
__all__ = [
	'Synth',
	'TWO_PI',
]

import inspect

from . import Base;         from .Base import ACROSS_SAMPLES, ACROSS_CHANNELS, _SubscriptHelper
from . import Dependencies; from .Dependencies import numpy
TWO_PI = 6.28318530717958623200

class Synth( object ):
	"""
	This class is a duck-typed substitute for the numpy
	array `s.y` at the heart of a `Sound` instance `s`,
	but instead of containing static data it allows
	on-the-fly functional computation of the sound signal.
	
	Example::

	    import numpy as np, audiomath as am
	    TWO_PI = 2.0 * np.pi
	    carrierFreq = 440
	    modFreq = 0.5
	    @am.Synth
	    def wobble(fs, samples, channels):
	        t = samples / fs
	        return np.sin(TWO_PI * carrierFreq * t) * (0.5 - 0.5 * np.cos(TWO_PI * modFreq * t))
	    p = am.Player(wobble)     # could also say am.Sound(wobble)
	    print(p.sound)
	    p.Play()
	
	You can also use a pre-configured *instance* of `Synth`
	as the decorator, with the same effect::
	
	    @am.Synth(fs=22050)
	    def y(fs, samples, channels):
	        t = samples / fs
	        return np.sin(2 * np.pi * 440 * t)
	    p = am.Player(y)     # could also say am.Sound(y)
	
	...or the `.Use()` method of an instance::
	
	    y = am.Synth()
	    @y.Use
	    def func(fs, samples, channels):   # this way, `func` will be unchanged
	        t = samples / fs
	        return np.sin(2 * np.pi * 440 * t)
	    p = am.Player(y)     # could also say am.Sound(y)
	
	...or you can subclass `am.Synth` with `func` as an
	overshadowed method::
	
	    class Tone(am.Synth):
	        def func(self, fs, samples, channels):
	            return np.sin(2 * np.pi * self.freq * samples / fs )
	    t = Tone()
	    t.freq = 440
	    p = am.Player(t)
	    
	"""
	def __init__( self, func=None, fs=44100, duration='inf', nChannels=1, dtype='float32' ):
		"""
		Args:
		    func:
		        A function that takes three arguments: a scalar
		        sampling frequency,  an `m x 1` array of sample
		        indices, and a `1 x n` array of channel indices.
		        `func` should return an `m x 1` or `m x n` array
		        of sample values.
		        
		        Alternatively, `func` may be defined like a
		        method (four arguments, the first being `self`).
		    
		    fs (float):
		        Scalar numeric value specifying the sampling rate.
		    
		    duration (float):
		        The nominal duration of the sound in seconds. May
		        be infinite.
		    
		    nChannels (int):
		        Nominal number of channels.
		    
		    dtype (str):
		        numpy data type for the generated sample data.
		"""
		if func: self.Use( func )
		self.fs = fs
		self.duration = float( duration )
		self.nChannels = nChannels
		self.dtype = numpy.dtype( dtype )
	
	def __call__( self, func ):   # so a synth instance (pre-initialized with custom fs or nChannels) can be used as a decorator on the definition of func
		self.Use( func )
		return self
	
	def Use( self, func ):        # alternative decorator on the definition of func
		try: getargspec = inspect.getfullargspec
		except: getargspec = inspect.getargspec
		try: spec = getargspec( func )
		except: spec = getargspec( func.__call__ )
		nArgs = len( spec.args )
		self.func = func if nArgs <= 3 else func.__get__( self )
		return func

	@property
	def fs( self ):
		return self.__fs
	@fs.setter
	def fs( self, value ):
		if hasattr( value, 'fs' ): value = value.fs
		self.__fs = float( value )
		
	@property
	def nSamples( self ):
		ns = self.duration * self.fs
		try: ns = int( round( ns ) )
		except: pass
		return ns	
	@nSamples.setter
	def nSamples( self, value ):
		self.duration = value / self.fs

	@property
	def nChannels( self ):
		return self.__nChannels
	@nChannels.setter
	def nChannels( self, value ):
		self.__nChannels = int( value )
		
	@property
	def shape( self ):
		return _SubscriptHelper( self.nSamples, self.__nChannels )
	
	@property
	def ndim( self ):
		return 2
	
	@property
	def size( self ):
		return self.nSamples * self.__nChannels
	
	def __getitem__( self, subs ):
		subs = list( subs ) if isinstance( subs, ( tuple, list ) ) else [ subs ]
		if len( subs ) == 1: subs.append( slice( None ) )
		if len( subs ) > 2: raise IndexError( 'too many subscripts' )
		
		samples = subs[ ACROSS_SAMPLES ]
		nSamples = self.nSamples
		if isinstance( samples,  slice ):
			if numpy.isinf( nSamples ): nSamples = samples.stop
			samples  = range( *samples.indices(  nSamples  ) )
		samples  = numpy.asarray( samples ).ravel()
		if any( samples > nSamples ): samples = samples[ samples < nSamples ]
		samples = numpy.expand_dims( samples, ACROSS_CHANNELS )
		
		channels = subs[ ACROSS_CHANNELS ]
		nChannels = self.__nChannels
		if isinstance( channels, slice ): channels = range( *channels.indices( nChannels ) )
		channels = numpy.asarray( channels ).ravel()
		if any( channels > nChannels ): channels = channels[ channels < nChannels ]
		channels = numpy.expand_dims( channels, ACROSS_SAMPLES )
		
		y = self.func( self.__fs, samples, channels )
		if y.dtype != self.dtype: y = y.astype( self.dtype )
		return y

	def __array__( self ):
		limit = 44100 * 10
		ns = int( min( self.nSamples, limit ) )
		if ns < self.nSamples:
			duration = 'infinite duration' if numpy.isinf( self.nSamples ) else 'nominal duration %g sec' % self.duration
			print( 'returning only the first %d samples (%g sec) of a Synth of %s' % ( ns, ns / self.__fs, duration ) )
		return self[ :ns, : ]
	
	@staticmethod
	def func( fs, samples, channels ):
		"""
		Demo function.  Replace this, e.g. by saying `y.func = something_else`,
		where `y` is your `Synth` instance. Or use the `@y.Use` decorator
		when defining a new function.  Or use `@Synth` as the decorator
		in the first place.
		"""
		t = samples / fs
		return numpy.sin( TWO_PI * 440 * t )
		