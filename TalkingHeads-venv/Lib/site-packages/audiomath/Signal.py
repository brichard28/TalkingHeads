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
This semi-independent submodule provides various basic
signal-processing tools that can be used with or without
the `audiomath.Sound` container.
"""

__all__ = [
	'UnwrapDiff',
	'msec2samples', 'samples2msec', 
	'ApplyWindow', 'ModulateAmplitude', 'GenerateWaveform',
	'Click', 'SineWave', 'SquareWave', 'TriangleWave', 'SawtoothWave', 'Noise',
	'fftfreqs', 'fft2ap', 'ap2fft', 'Reconstruct', 'Toy',
	'fft', 'ifft', 'Hann', 'Shoulder', 'Hilbert',
	'Spectrum', 'InverseSpectrum', 'ReweightSpectrum',
	'Timebase', 'PlotSignal', 'PlotSpectrum', 
]

import sys
import inspect
try: getargspec = inspect.getfullargspec
except: getargspec = inspect.getargspec

#### begin compatibility dance
try:
	from . import DependencyManagement  # will succeed if we're part of audiomath
except ImportError:
	# If we're not:
	try: import numpy
	except: numpy = None
	def LoadPyplot( interactive='auto' ):
		import matplotlib
		if interactive == 'auto':
			if 'matplotlib.backends' in sys.modules: interactive = None
			else: interactive = ( 'IPython' in sys.modules )
		if matplotlib and interactive is not None: matplotlib.interactive( interactive )
		if matplotlib: import matplotlib.pyplot as plt
		return plt
else:
	# If we are:
	from . import DependencyManagement; from .DependencyManagement import LoadPyplot
	from . import Dependencies;         from .Dependencies import numpy

if numpy:
	from numpy import pi as PI, sin, cos
	from numpy.fft import fft, ifft
	try: from numpy.lib import hanning as Hann
	except ImportError: Hann = None
else:
	PI = 3.14159265358979311600
	sin = cos = None
	fft = ifft = None
	Hann = None
	
if not Hann:
	def Hann( nSamples ):
		if nSamples < 1: return numpy.array( [] )
		if nSamples == 1: return numpy.ones( 1, dtype=float )
		n = numpy.arange( 0, nSamples )
		return 0.5 - 0.5 * numpy.cos( TWO_PI * n / ( nSamples - 1 ) )
#### end compatibility dance


TWO_PI  = 2.0 * PI
HALF_PI = 0.5 * PI
DEGREES_PER_RADIAN = 180.0 / PI
RADIANS_PER_DEGREE = PI / 180.0


class ArgConflictError(Exception): pass

def IncreaseDimensionality( a, maxdim, left=False ):
	"""
	Return a view of the numpy array `a` that has at least `maxdim + 1`
	dimensions. By default, add new dimensions to the right, but add
	them to the left if `left` is true.
	
	See also `TrimTrailingDims()`
	"""
	if isinstance( a, numpy.matrix ) and maxdim > 1:
		a = numpy.asarray( a )
	else:
		a = a.view()
	extraDims = ( 1, ) * ( maxdim - len( a.shape ) + 1 )
	a.shape = extraDims + a.shape if left else a.shape + extraDims
	return a

def TrimTrailingDims(a):
	"""
	Similar to `numpy.squeeze()` but only removes high dimensions, like
	Matlab's `squeeze`. Returns a view of array `a`.
	
	See also `IncreaseDimensionality()`
	"""
	a = numpy.asarray( a ).view()
	sh = list( a.shape )
	while sh and sh[ -1 ] == 1: sh.pop( -1 )
	a.shape = tuple( sh )
	return a

def AsColumns( a, axis=0 ):
	"""
	Returns a view of the input array `a` suitable for plotting. The
	specified `axis` is swapped with axis 0. The return value has
	exactly 2 dimensions - any other dimensions besides `axis` are
	simply concatenated into the second dimension.
	"""
	a = numpy.asarray( a ).view()
	a = a.swapaxes( 0, axis )
	n = a.shape[ 0 ]
	a = a.reshape( [ n, int( a.size / n ) ] )
	return a

def UnwrapDiff( x, base=TWO_PI, axis=None, startval=None, dtype=None ):
	"""
	Assume `X` is a wrapped version of an underlying value `Y` we're
	interested in. For example, it's a 16-bit value that wraps around
	at 65536, or it's an angle which wraps back to 0 at 2*pi.
	
	`base` is the value (65536 or 2*pi in the above examples) such that
	`X = Y % base`.  The default value of `base` is 2*pi.
	
	Let `dY` be the numeric diff of `Y` in dimension `axis`, computed
	from `X` by unwrapping in order to avoid jumps larger than `base/2`.
	Thus, with `base=65536`, a jump from 65535 to 1 is considered as a
	step of +2. With `base=360`, a jump from 10 to 350 is considered as
	a step of -20.
	
	`Y` is then reconstructed based on `dY` and `startval` (which
	defaults to the actual initial value(s) of `X`).
	
	Return value is `(dY,Y)`.
	"""
	if dtype is not None: x = numpy.asarray( x, dtype=dtype )
	if axis is None:
		axis, = numpy.where( numpy.array( x.shape ) != 1 )
		if len( axis ): axis = axis[ 0 ]
		else: axis = 0
	x = x % base
	d = numpy.diff( x, axis=axis )
	nj = d < -base / 2.0
	d[ nj ] += base
	pj = d > base / 2.0
	d[ pj ] -= base
	d[ numpy.isnan( d ) ] = 0
	sub = [ slice( None ) for i in x.shape ]
	sub[ axis ] = [ 0 ]
	sv = x[ tuple( sub ) ]
	if startval is not None: sv = sv * 0 + startval
	x = numpy.cumsum( numpy.concatenate( ( sv, d ), axis=axis ), axis=axis )
	return d, x

def get_fs(obj, defaultVal=None):
	"""
	Infer the sampling frequency from `obj`. `obj` may simply be the numerical
	sampling-frequency value, or it may be an object in which the sampling
	frequency is stored in `obj.samplingfreq_hz`, `obj.fs` or
	`obj.params['SamplingRate']`.
	"""
	fs = None
	if isinstance(obj, float) or isinstance(obj, int): fs = obj
	elif hasattr(obj, 'samplingfreq_hz'): fs = obj.samplingfreq_hz
	elif hasattr(obj, 'fs'): fs = obj.fs
	elif hasattr(obj, 'params'): fs = obj.params
	elif isinstance( obj, dict ):
		if fs is None: fs = obj.get( 'samplingfreq_hz', None )
		if fs is None: fs = obj.get( 'fs', None )
		if fs is None: fs = obj.get( 'params', None )
			
	if isinstance(fs, dict) and fs.has_key('SamplingRate'): fs = fs['SamplingRate']
	if isinstance(fs, str) and fs.lower().endswith('hz'): fs = fs[:-2]
	if fs is None: return defaultVal
	return float(fs)
	
def msec2samples(msec, samplingfreq_hz):
	"""
	Converts milliseconds to the nearest integer number of samples given
	the specified sampling frequency.
	"""
	fs = get_fs(samplingfreq_hz)
	if msec is None or fs is None: return None
	if isinstance(msec, (tuple,list)): msec = numpy.array(msec)
	if isinstance(msec, numpy.ndarray): msec = msec.astype(numpy.float64)
	else: msec = float(msec)
	return numpy.round(float(fs) * msec / 1000.0)

def samples2msec(samples, samplingfreq_hz):
	"""
	Converts samples to milliseconds given the specified sampling frequency.
	"""
	fs = get_fs(samplingfreq_hz)
	if samples is None or fs is None: return None
	if isinstance(samples, (tuple,list)): samples = numpy.array(samples)
	if isinstance(samples, numpy.ndarray): samples = samples.astype(numpy.float64)
	else: samples = float(samples)
	return 1000.0 * samples / float(fs)

			
def ApplyWindow(s, func=Hann, axis=0, **kwargs):
	"""
	If `s` is a `numpy.ndarray`, return a windowed copy of the array.
	If `s` is an `audiomath.Sound` object (for example, if this is being
	used a method of that class), then its internal array `s.y` will be
	replaced by a windowed copy.
	
	Windowing means multiplication by the specified window function,
	along the specified time `axis`.
	
	`func` should take a single positional argument: length in samples.
	Additional `**kwargs`, if any, are passed through. Suitable examples
	include `numpy.blackman`, `numpy.kaiser`, and friends.
	"""
	if isinstance( s, numpy.ndarray ): y = s
	elif hasattr(s, 'y'): y = s.y
	else: raise TypeError( "don't know how to handle this kind of container object" )
	envelope = func(y.shape[axis], **kwargs)
	envelope.shape = [ ( envelope.size if dim == axis else 1 ) for dim in range( y.ndim ) ]
	y = y * envelope
	if isinstance( s, numpy.ndarray ): s = y
	else: s.y = y
	return s
		
def ModulateAmplitude(s, freq_hz=1.0,phase_rad=None,phase_deg=None,amplitude=0.5,dc=0.5,samplingfreq_hz=None,duration_msec=None,duration_samples=None,axis=None,waveform=sin,**kwargs):
	"""
	If `s` is a `numpy.ndarray`, return a modulated copy of the array.
	If `s` is an `audiomath.Sound` object (for example, if this is being
	used a method of that class), then its internal array `s.y` will be
	replaced by a modulated copy.

	Modulation means multiplication by the specified `waveform`, along the
	specified time `axis`.
	
	Default phase is such that amplitude is 0 at time 0, which corresponds to
	phase_deg=-90 if `waveform` follows sine phase (remember: by default the
	modulator is a raised waveform, because `dc=0.5` by default). To change
	phase, specify either `phase_rad` or `phase_deg`.
	
	Uses `GenerateWaveform()`
	"""
	container = None
	if isinstance( s, numpy.ndarray ): y = s
	elif hasattr(s, 'y'): y = s.y; container = s.copy()
	else: raise TypeError( "don't know how to handle this kind of carrier object" )

	if samplingfreq_hz is None: samplingfreq_hz = get_fs(s)	
	if phase_rad is None and phase_deg is None: phase_deg = -90.0
	if duration_samples is None and duration_msec is None:
		duration_samples = max( IncreaseDimensionality(y,0).shape ) if axis is None else IncreaseDimensionality(y,0).shape[axis]
	envelope = GenerateWaveform(freq_hz=freq_hz,phase_rad=phase_rad,phase_deg=phase_deg,amplitude=amplitude,dc=dc,samplingfreq_hz=samplingfreq_hz,duration_msec=duration_msec,duration_samples=duration_samples,axis=axis,waveform=waveform,container=container,**kwargs)
	if container: y = ( s * envelope ).y
	else: y = y * IncreaseDimensionality(envelope, len(y.shape)-1)
	if isinstance( s, numpy.ndarray ): s = y
	else: s.y = y
	return s

def GenerateWaveform(container=None,freq_hz=1.0,phase_rad=None,phase_deg=None,amplitude=1.0,dc=0.0,samplingfreq_hz=None,duration_msec=None,duration_samples=None,axis=None,waveform=cos,waveform_domain='auto',**kwargs):
	"""
	Create a signal (or multiple signals, if the input arguments are arrays)
	which is a function of time (time being defined along the specified `axis`).
	
	If this is being used as a method of an `audiomath.Sound` instance, then
	the `container` argument is automatically set to that instance. Otherwise
	(if used as a global function), the `container` argument is optional---if
	supplied, it should be a `audiomath.Sound` object. With a `container`, the
	`axis` argument is set to 0, and the container object's sampling frequency
	number of channels and duration (if non-zero) are used as fallback values
	in case these are not specified elsewhere. The resulting signal is put into
	`container.y` and a reference to the `container` is returned.
	
	Default phase is 0, but may be changed by either `phase_deg` or `phase_rad`
	(or both, as long as the values are consistent).
	
	Default duration is 1000 msec, but may be changed by either `duration_samples`
	or `duration_msec` (or both, as long as the values are consistent).
	
	If `duration_samples` is specified and `samplingfreq_hz` is not, then the
	sampling frequency is chosen such that the duration is 1 second---so then
	`freq_hz` can be interpreted as cycles per signal.

	The default `waveform` function is `numpy.cos` which means that amplitude,
	phase and frequency arguments can be taken straight from the kind of
	dictionary returned by `fft2ap()` for an accurate reconstruction. A `waveform`
	function is assumed by default to take an input expressed in radians, unless
	the first argument in its signature is named `cycles`, `samples`, `seconds`
	or `milliseconds`, in which case the input argument is adjusted accordingly
	to achieve the named units. (To specify the units explicitly as one of these
	options, pass one of these words as the `waveform_domain` argument.)
	
	In this module,  `SineWave()`, `SquareWave()`, `TriangleWave()` and
	`SawtoothWave()` are all functions of cycles (i.e. the product of time and
	frequency), whereas `Click()` is a function of milliseconds. Any of these
	can be passed as the `waveform` argument.
	"""
	fs = get_fs(samplingfreq_hz)
	default_duration_msec = 1000.0
	nrep = 1
	across_samples = None
	if container is not None:
		if fs is None: fs = get_fs(container)
		if axis is None:
			across_samples  = getattr( container, 'ACROSS_SAMPLES', None )
			if across_samples is not None: axis = across_samples
		container_duration = getattr( container, 'duration', None )
		container_channels = getattr( container, 'nChannels', None )
		if container_duration: default_duration_msec = container_duration * 1000.0
		if container_channels and container.y.size: nrep = container_channels
		# The purpose of the `and y.size` condition is that the simplest way of
		# creating a Sound object with generated content, `GenerateWaveform(container=Sound())`,
		# should not violate the principle of least surprise by generating more than one,
		# channel---despite the fact that new empty Sound objects have 2 channels by default.
		# There's no perfect solution there, but if you want a stereo generated sound, and
		# have no pre-existing non-zero-length container Sound to base it on, you can
		# always pass a two-element list to freq_hz or any of the other parameters.
	for j in range(0,2):
		for i in range(0,2):
			if duration_msec is None:
				duration_msec = samples2msec(duration_samples, fs)
			if duration_samples is None:
				duration_samples = msec2samples(duration_msec, fs)
				if duration_samples is not None:
					duration_msec = samples2msec(duration_samples, fs)
			if fs is None and duration_samples is not None and duration_msec is not None: fs = 1000.0 * float(duration_samples) / float(duration_msec)
			if fs is None and duration_samples is not None: fs = float(duration_samples)
			if fs is None and duration_msec is not None: fs = float(duration_msec)
		if duration_msec is None: duration_msec = default_duration_msec	
	duration_sec = duration_msec / 1000.0
	duration_samples = float(round(duration_samples))
	if duration_msec != samples2msec(duration_samples,fs) or duration_samples != msec2samples(duration_msec,fs):
		raise ArgConflictError( "conflicting duration_samples and duration_msec arguments" )
	x = numpy.arange( 0.0, duration_samples ) * ( TWO_PI / duration_samples )
	freq_hz = TrimTrailingDims(numpy.array(freq_hz,dtype='float'))
	if phase_rad is None and phase_deg is None: phase_rad = [0.0]
	if phase_rad is not None:
		if not isinstance( phase_rad, numpy.ndarray ) or phase_rad.dtype != 'float': phase_rad = numpy.array(phase_rad,dtype='float')
		phase_rad = TrimTrailingDims(phase_rad)
	if phase_deg is not None:
		if not isinstance( phase_deg, numpy.ndarray ) or phase_deg.dtype != 'float': phase_deg = numpy.array(phase_deg,dtype='float')
		phase_deg = TrimTrailingDims(phase_deg)
	if phase_rad is not None and phase_deg is not None:
		if phase_rad.shape != phase_deg.shape: raise ArgConflictError( "conflicting phase_rad and phase_deg arguments" )
		if numpy.max( numpy.abs( phase_rad * DEGREES_PER_RADIAN - phase_deg ) > 1e-10 ): raise ArgConflictError( "conflicting phase_rad and phase_deg arguments" )
	if phase_rad is None:
		phase_rad = numpy.array( phase_deg * RADIANS_PER_DEGREE )

	amplitude = TrimTrailingDims(numpy.array(amplitude,dtype='float'))
	dc = TrimTrailingDims(numpy.array(dc,dtype='float'))
	if across_samples is None: maxaxis = max(freq_hz.ndim, len(phase_rad.shape), len(amplitude.shape), len(dc.shape)) - 1
	else: maxaxis = 1
	if axis is None:
		if IncreaseDimensionality(freq_hz,0).shape[0]==1 and IncreaseDimensionality(phase_rad,0).shape[0]==1 and IncreaseDimensionality(amplitude,0).shape[0]==1 and IncreaseDimensionality(dc,0).shape[0]==1:
			axis=0
		else:
			axis = maxaxis + 1
	maxaxis = max(axis, maxaxis)
	
	def ShapeUp(a):
		if across_samples is None: return IncreaseDimensionality(a, maxaxis)
		else: return numpy.expand_dims(a.ravel(), across_samples)
	x = IncreaseDimensionality(x,maxaxis).swapaxes(0,axis)
	x = x * (ShapeUp(freq_hz) * duration_sec) # *= won't work for broadcasting here
	# if you get an error here, try setting axis=1 and transposing the return value ;-)
	x = x + ShapeUp(phase_rad)                # += won't work for broadcasting here
	
	if waveform_domain == 'auto':
		waveform_domain = 'radians'
		try:
			spec = getargspec( waveform )
		except:
			pass
		else:
			if spec.args[ 0 ] in [ 'cycles', 'samples', 'seconds', 'sec', 's', 'milliseconds', 'msec', 'ms' ]:
				waveform_domain = spec.args[ 0 ]
		
	if   waveform_domain in [ 'radians' ]: pass
	elif waveform_domain in [ 'cycles'  ]: x /= TWO_PI; x %= 1.0
	elif waveform_domain in [ 'samples' ]: x /= TWO_PI; x %= 1.0; x /= freq_hz / fs
	elif waveform_domain in [ 'seconds', 'sec', 's' ]: x /= TWO_PI; x %= 1.0; x /= freq_hz
	elif waveform_domain in [ 'milliseconds', 'msec', 'ms' ]: x /= TWO_PI; x %= 1.0; x /= freq_hz / 1000.0
	else: raise ValueError( 'unrecognized waveform_domain value %r' % waveform_domain )
	
	x = waveform(x, **kwargs)
	x = x * ShapeUp(amplitude)                # *= won't work for broadcasting here
	if numpy.any(dc.flatten()):
		x = x + ShapeUp(dc)                   # += won't work for broadcasting here
	if container is not None:
		across_channels = getattr(container, 'ACROSS_CHANNELS', 1)
		x = IncreaseDimensionality(x, across_channels)
		if x.shape[across_channels] == 1 and nrep > 1: x = x.repeat(nrep, across_channels)
		container.y = x
		container.fs = int(round(fs))
		x = container
	return x

def fftfreqs(nSamples, samplingfreq_hz=1.0):
	"""
	Return a 1-D numpy.array of length `nSamples` containing the positive and
	negative frequency values corresponding to the elements of an `nSamples`-point
	FFT. If `samplingfreq_hz` is not supplied, 1.0 is assumed, so the result has
	0.5 as its Nyquist frequency.  
	"""
	nSamples = int(nSamples)
	fs = get_fs(samplingfreq_hz)
	biggest_pos_freq = float(numpy.floor(nSamples/2))       # floor(nSamples/2)
	biggest_neg_freq = -float(numpy.floor((nSamples-1)/2))  # -floor((nSamples-1)/2)
	posfreq = numpy.arange(0.0, biggest_pos_freq+1.0) * (float(fs) / float(nSamples))
	negfreq = numpy.arange(biggest_neg_freq, 0.0) * (float(fs) / float(nSamples))
	return numpy.concatenate((posfreq,negfreq))

def fft2ap(X, samplingfreq_hz=2.0, axis=0):
	"""
	Given discrete Fourier transform(s) `X` (with frequency along the
	specified `axis`), return a dict containing a properly scaled
	amplitude spectrum, a phase spectrum in degrees and in radians,
	and a frequency axis (coping with all the fiddly edge conditions).
	
	The inverse of  `d = fft2ap(X)`  is  `X = ap2fft(**d)`
	"""
	fs = get_fs(samplingfreq_hz)	
	nSamples = int(X.shape[axis])
	biggest_pos_freq = float(numpy.floor(nSamples/2))       # floor(nSamples/2)
	biggest_neg_freq = -float(numpy.floor((nSamples-1)/2))  # -floor((nSamples-1)/2)
	posfreq = numpy.arange(0.0, biggest_pos_freq+1.0) * (float(fs) / float(nSamples))
	negfreq = numpy.arange(biggest_neg_freq, 0.0) * (float(fs) / float(nSamples))
	fullfreq = numpy.concatenate((posfreq,negfreq))
	sub = [slice(None)] * max(axis+1, len(X.shape))
	sub[axis] = slice(0,len(posfreq))
	X = IncreaseDimensionality(X, axis)[tuple(sub)]
	ph = numpy.angle(X)
	amp = numpy.abs(X) * (2.0 / float(nSamples))
	if nSamples % 2 == 0:
		sub[axis] = -1
		amp[tuple(sub)] /= 2.0
	return {'amplitude':amp, 'phase_rad':ph, 'phase_deg':ph*DEGREES_PER_RADIAN, 'freq_hz':posfreq, 'fullfreq_hz':fullfreq, 'samplingfreq_hz':fs, 'axis':axis}

def ap2fft(amplitude,phase_rad=None,phase_deg=None,samplingfreq_hz=2.0,axis=0,freq_hz=None,fullfreq_hz=None,nSamples=None):
	"""
	Keyword arguments match the fields of the `dict`
	output by `fft2ap()`.

	The inverse of `d = fft2ap(X)` is `X = ap2fft(**d)`
	"""
	fs = get_fs(samplingfreq_hz)	
	if nSamples is None:
		if fullfreq_hz is not None: nSamples = len(fullfreq_hz)
		elif freq_hz is not None:   nSamples = len(freq_hz) * 2 - 2
		else: nSamples = amplitude.shape[axis] * 2 - 2
	
	amplitude = IncreaseDimensionality(numpy.array(amplitude,dtype='float'), axis)
	if phase_rad is None and phase_deg is None: phase_rad = numpy.zeros(shape=amplitude.shape,dtype='float')
	if phase_rad is not None:
		if not isinstance( phase_rad, numpy.ndarray ) or phase_rad.dtype != 'float': phase_rad = numpy.array(phase_rad,dtype='float')
		phase_rad = IncreaseDimensionality(phase_rad, axis)
	if phase_deg is not None:
		if not isinstance( phase_deg, numpy.ndarray ) or phase_deg.dtype != 'float': phase_deg = numpy.array(phase_deg,dtype='float')
		phase_deg = IncreaseDimensionality(phase_deg, axis)
	if phase_rad is not None and phase_deg is not None:
		if phase_rad.shape != phase_deg.shape: raise ArgConflictError( "conflicting phase_rad and phase_deg arguments" )
		if numpy.max(numpy.abs(phase_rad * DEGREES_PER_RADIAN - phase_deg) > 1e-10): raise ArgConflictError( "conflicting phase_rad and phase_deg arguments" )
	if phase_rad is None:
		phase_rad = phase_deg * RADIANS_PER_DEGREE

	f = phase_rad * 1j
	f = numpy.exp(f)
	f = f * amplitude
	f *= float(nSamples)/2.0
	sub = [slice(None)] * max(axis+1, len(f.shape))
	if nSamples%2 == 0:
		sub[axis] = -1
		f[tuple(sub)] *= 2.0
	sub[axis] = slice((nSamples%2)-2, 0, -1)
	sub = tuple(sub)
	f = numpy.concatenate((f, numpy.conj(f[sub])), axis=axis)
	return f

def Spectrum( x, samplingfreq_hz=None, axis=None ):
	"""
	Runs `fft` on a signal followed by `fft2ap`, to return
	spectral information in "human-readable" format with the
	annoying corner cases handled.
	
	The inverse operation is `InverseSpectrum()`.
	"""
	if hasattr( x, 'fs' ) and hasattr( x, 'y' ): # duck-type audiomath.Sound support
		if samplingfreq_hz is None: samplingfreq_hz = x.fs
		if axis is None: axis = x.ACROSS_SAMPLES
		x = x.y
	if samplingfreq_hz is None: samplingfreq_hz = 2.0
	if axis is None: axis = 0
	return fft2ap( fft( x, axis=axis ), samplingfreq_hz=samplingfreq_hz, axis=axis )

def InverseSpectrum( ap, real=True ):
	"""
	Inverse of `Spectrum()`.  Takes the `dict` output of `Spectrum()`
	(or of the underlying `fft2ap()`) and runs `ap2fft()` followed by
	`ifft()` on it to return a signal. If `real` is true, which it is
	by default, discard the imaginary part of the result.
	"""
	x = ifft( ap2fft( **ap ), axis=ap[ 'axis' ] )
	if real: x = x.real
	return x

def Timebase( x, samplingfreq_hz=None, axis=None ):
	"""
	Return a discrete time axis in seconds, against which signal `x`
	can be plotted. `x` may be an `audiomath.Sound` instance, or
	you may supply `samplingfreq_hz` explicitly.
	"""
	if axis is None and isinstance( samplingfreq_hz, dict ): axis = samplingfreq_hz[ 'axis' ]
	if hasattr( x, 'fs' ) and hasattr( x, 'y' ): # duck-type audiomath.Sound support
		if samplingfreq_hz is None: samplingfreq_hz = x.fs
		if axis is None: axis = x.ACROSS_SAMPLES
		x = x.y
	if axis is None: axis = 0
	samplingfreq_hz = get_fs( samplingfreq_hz )
	if samplingfreq_hz is None: samplingfreq_hz = 2.0
	
	t = samples2msec( numpy.arange( x.shape[ axis ] ), samplingfreq_hz ) / 1000.0
	t = IncreaseDimensionality( t, x.ndim - 1 ).swapaxes( 0, axis )
	return t

def PlotSignal( x, samplingfreq_hz=None, axis=None, **kwargs ):
	"""
	Plot `x` (an array with time running along the specified `axis`,
	or an `audiomath.Sound` instance) against the appropriate
	`Timebase()`.
	"""
	if axis is None and isinstance( samplingfreq_hz, dict ): axis = samplingfreq_hz[ 'axis' ]
	if hasattr( x, 'fs' ) and hasattr( x, 'y' ): # duck-type audiomath.Sound support
		if samplingfreq_hz is None: samplingfreq_hz = x.fs
		if axis is None: axis = x.ACROSS_SAMPLES
		x = x.y
	if axis is None: axis = 0
	samplingfreq_hz = get_fs( samplingfreq_hz )
	if samplingfreq_hz is None: samplingfreq_hz = 2.0
	
	t = Timebase( x, samplingfreq_hz=samplingfreq_hz, axis=axis )
	plt = LoadPyplot()
	axpropnames = 'xlim ylim xlabel ylabel title xticks yticks xticklabels yticklabels'.split()
	aprops = { name : kwargs.pop( name ) for name in list( kwargs.keys() ) if name in axpropnames }
	if not kwargs.pop( 'hold', True ): plt.cla()
	h = plt.plot( AsColumns( t, axis ), AsColumns( x, axis ), **kwargs )
	if aprops: plt.gca().set( **aprops )
	return h
	
def PlotSpectrum( x, samplingfreq_hz=None, axis=None, dB=False, baseValue=None, **kwargs ):
	"""
	Input argument `x` may be a `numpy.array` or `audiomath.Sound`,
	in which case `Spectrum()` will be called on it. Or it may be
	the `dict` output of a previous `Spectrum()` or `fft2ap()` call.
	"""
	if not isinstance( x, dict ):
		if axis is None and isinstance( samplingfreq_hz, dict ): axis = samplingfreq_hz[ 'axis' ]
		if hasattr( x, 'fs' ) and hasattr( x, 'y' ): # duck-type audiomath.Sound support
			if samplingfreq_hz is None: samplingfreq_hz = x.fs
			if axis is None: axis = x.ACROSS_SAMPLES
			x = x.y
		if axis is None: axis = 0
		samplingfreq_hz = get_fs( samplingfreq_hz )
		if samplingfreq_hz is None: samplingfreq_hz = 2.0
		x = Spectrum( x, samplingfreq_hz=samplingfreq_hz, axis=axis )
	y = AsColumns( x[ 'amplitude' ], x[ 'axis' ] )
	if dB: y = 20.0 * numpy.log10( y )
	
	# dammit I effectively had to write my own plt.stem() here because
	# I simply couldn't tame the colour assignments in the original
	plt = LoadPyplot()
	h = []
	f = x[ 'freq_hz' ]
	if baseValue is None: baseValue = ( y.max() - 400 ) if dB else 0.0
	
	axpropnames = 'xlim ylim xlabel ylabel title xticks yticks xticklabels yticklabels'.split()
	aprops = { name : kwargs.pop( name ) for name in list( kwargs.keys() ) if name in axpropnames }
	if not kwargs.pop( 'hold', True ): plt.cla()
	mprops = dict( kwargs )
	mprops.setdefault( 'marker', 'o' )
	mprops[ 'linestyle' ] = 'None'
	for yi in y.T:
		markerline, = plt.plot( f, yi, **mprops ) 
		sprops = dict( kwargs )
		sprops[ 'marker' ] = 'None'		
		sprops.setdefault( 'color', markerline.get_color() )
		ff = [ fjk for fj in f for fjk in [ fj, fj, fj ] ]
		yy = [ yijk for yij in yi for yijk in [ baseValue, yij, numpy.nan ] ]
		stemline = plt.plot( ff, yy, **sprops )
		h.append( [ markerline, stemline ] )
	plt.grid( True )
	if aprops: plt.gca().set( **aprops )
	return h


def _PiecewiseLinear( y, yrange, t, trange ):
	if trange[ 1 ] == trange[ 0 ]:
		y[ t == trange[ 0 ] ] = sum( yrange )/2.0
	else:
		mask = numpy.logical_and( trange[ 0 ] <= t,  t < trange[ 1 ] )
		t = ( t[ mask ] - trange[ 0 ] ) / float( trange[ 1 ] - trange[ 0 ] )
		if len( t ): y[ mask ] = yrange[ 0 ] + ( yrange[ 1 ] - yrange[ 0 ] ) * t
	return trange[1]

def SquareWave( cycles, phase_deg=0, maxharm=None, rescale=False, duty=0.5, ramp=0, tol=1e-8 ):
	"""
	A square wave with its peaks and troughs in sine phase.
	If `maxharm` is an integer, then an anti-aliased approximation
	to the square wave (containing no components of higher frequency
	than `maxharm` times the fundamental) is returned instead. In
	this case, the `rescale` flag can be set to ensure that the
	sampled waveform does not exceed +/- 1.0
	
	This function can be passed as the `waveform` argument to
	`GenerateWaveform`.
	"""
	if ramp + tol > 1.0: raise ValueError( "ramp + tol cannot exceed 1.0" )
	
	cycles = numpy.asarray( cycles, dtype=float ) + numpy.asarray( phase_deg, dtype=float ) / 360.0
	if maxharm is None or maxharm == numpy.inf:
		y = cycles % 1.0		
		t = y * 1.0
		m = ( 1.0 - tol - ramp )
		on, off = duty * m, ( 1.0 - duty ) * m
		x = 0.0
		x = _PiecewiseLinear( y, [  0,  0 ], t, [ x, x + tol/4.0  ] )
		x = _PiecewiseLinear( y, [  0, +1 ], t, [ x, x + ramp/4.0 ] )
		x = _PiecewiseLinear( y, [ +1, +1 ], t, [ x, x + on       ] )
		x = _PiecewiseLinear( y, [ +1,  0 ], t, [ x, x + ramp/4.0 ] )
		x = _PiecewiseLinear( y, [  0,  0 ], t, [ x, x + tol/2.0  ] )
		x = _PiecewiseLinear( y, [  0, -1 ], t, [ x, x + ramp/4.0 ] )
		x = _PiecewiseLinear( y, [ -1, -1 ], t, [ x, x + off      ] )
		x = _PiecewiseLinear( y, [ -1,  0 ], t, [ x, x + ramp/4.0 ] )
		x = _PiecewiseLinear( y, [  0,  0 ], t, [ x, x + tol/4.0  ] )		
		return y
			
	if duty != 0.5 or ramp != 0: raise ValueError( "antialiasing (maxharm!=None) not implemented for duty cycles other than 0.5 or ramps other than 0" )
	theta = cycles * TWO_PI
	y = 0.0
	for h in range( 1, int( maxharm ) + 1, 2 ):
		y += numpy.sin( h * theta ) / h
	y *= 4.0 / PI
	if rescale: y /= 1.01 * numpy.abs( SquareWave( 0.5 / maxharm, maxharm=maxharm, rescale=False ) )
	return y

def TriangleWave( cycles, phase_deg=0, maxharm=None, rescale=False ):
	"""
	A triangle wave with its peaks and troughs in sine phase.
	If `maxharm` is an integer, then an anti-aliased approximation
	to the triangle wave (containing no components of higher frequency
	than `maxharm` times the fundamental) is returned instead. The
	`rescale` flag, included for compatibility with `SawtoothWave()`
	and `SquareWave()`, has no effect.
	
	This function can be passed as the `waveform` argument to
	`GenerateWaveform`.
	"""
	cycles = numpy.asarray( cycles, dtype=float ) + numpy.asarray( phase_deg, dtype=float ) / 360.0
	
	if maxharm is None or maxharm == numpy.inf:
		y = cycles - 0.25
		y %= 1.0
		y -= 0.5
		y = numpy.abs( y )
		y *= 4.0
		y -= 1.0
		return y

	theta = cycles * TWO_PI
	y = 0.0
	for h in range( 1, int( maxharm ) + 1, 2 ):
		y += numpy.sin( h * HALF_PI ) * numpy.sin( h * theta ) / h ** 2
	y *= 8.0 / PI ** 2
	# rescale not necessary -- never overshoots
	return y
	
def SawtoothWave( cycles, phase_deg=0, maxharm=None, rescale=False ):
	"""
	A sawtooth wave with its polarity and zero-crossings in sine phase.
	If `maxharm` is an integer, then an anti-aliased approximation
	to the sawtooth wave (containing no components of higher frequency
	than `maxharm` times the fundamental) is returned instead. In
	this case, the `rescale` flag can be set to ensure that the
	waveform does not exceed +/- 1.0
	
	This function can be passed as the `waveform` argument to
	`GenerateWaveform`.
	"""
	shift = -0.5
	cycles = numpy.asarray( cycles, dtype=float ) + numpy.asarray( phase_deg, dtype=float ) / 360.0
	cycles += shift
	if maxharm is None or maxharm == numpy.inf:
		y = cycles % 1.0
		y *= 2.0
		y -= 1.0
		return y

	theta = cycles * TWO_PI
	y = 0.0
	for h in range( 1, int( maxharm ) + 1 ):
		y += numpy.sin( h * theta ) / h
	y /= -HALF_PI
	if rescale: y /= 1.01 * numpy.abs( SawtoothWave( 0.5 / maxharm - shift, maxharm=maxharm, rescale=False ) )
	return y

def SineWave( cycles, phase_deg=0, maxharm=None, rescale=False ):
	"""
	A sine wave, but with the input expressed in cycles (0 to 1)
	instead of radians (0 to 2*pi).  Otherwise no different from
	`numpy.sin`, except that the function signature has `maxharm`
	and `rescale` arguments (which are ignored) for compatibility
	with `SquareWave()`, `TriangleWave()` and `SawtoothWave()`.
	
	This function can be passed as the `waveform` argument to
	`GenerateWaveform`.
	"""
	cycles = numpy.asarray( cycles, dtype=float ) + numpy.asarray( phase_deg, dtype=float ) / 360.0
	theta = cycles * TWO_PI
	return numpy.sin( theta ) # maxharm and rescale have no effect
	
def Click( milliseconds, positivePulseWidth=0.5, negativePulseWidth='symmetric' ):
	"""
	A signal function that can be passed as the `waveform` argument
	to `GenerateWaveform`, to generate periodic clicks. Each click
	is a positive pulse optionally followed by a negative pulse.
	If `negativePulseWidth` is `None` or the string `'symmetric'`,
	then the width of the negative pulse is made the same as
	`positivePulseWidth`. Otherwise, input arguments are all
	expressed in milliseconds.
	"""
	if negativePulseWidth == 'symmetric':
		negativePulseWidth = None
	if negativePulseWidth is None:
		negativePulseWidth = positivePulseWidth
	a = numpy.zeros_like( milliseconds )
	if negativePulseWidth:
		a[ milliseconds < positivePulseWidth + negativePulseWidth ] = -1
	a[ milliseconds < positivePulseWidth ] = 1
	return a

def Noise( cycles, distribution='uniform', **kwargs ):
	"""
	This function can be passed as the `waveform` argument to
	`GenerateWaveform`. The `distribution` argument should be
	a function, or the name of a function within `numpy.random`,
	that takes a `size` keyword argument dictating the shape
	of its output array. Additional `**kwargs` are passed
	through to the function.
	
	If the function is `numpy.random.uniform`, then the `low`
	argument is set to -1.0 by default instead of the usual 0.0.
	
	If the function is `numpy.random.normal`, then the `scale`
	argument is set to 0.2 by default instead of the usual 1.0.
	"""
	if isinstance( distribution, str ):
		prefix = 'numpy.random.'
		if distribution.startswith( prefix ): distribution = distribution[ len( prefix ): ]
		if distribution.lower() in [ 'gauss', 'gaussian' ]: distribution = 'normal'
		distribution = getattr( numpy.random, distribution )
	if distribution is numpy.random.uniform: kwargs.setdefault( 'low', -1.0 )
	if distribution is numpy.random.normal:  kwargs.setdefault( 'scale', 0.2 )
	kwargs[ 'size' ] = numpy.asarray( cycles ).shape
	return distribution( **kwargs )
	
def Toy( nSamples=11, nCycles=None, amplitude=( 1.0, 0.1 ), phase_deg=0 ):
	"""
	Toy sinusoidal signals for testing `fft2ap()` and `ap2fft()`.
	Check both odd and even `nSamples`.
	"""
	if nCycles is None: nCycles = [ 1.0, int( nSamples / 2 ) ]
	return GenerateWaveform( duration_samples=nSamples, samplingfreq_hz=nSamples, freq_hz=nCycles, phase_deg=phase_deg, amplitude=amplitude, axis=1 ).transpose()
	
def Reconstruct(ap,**kwargs):
	"""
	Check the accuracy of `fft2ap()` and `GenerateWaveform()` by
	reconstructing a signal as the sum of cosine waves with amplitudes
	and phases specified in dict `ap`, which is of the form output by
	`fft2ap()`.
	"""
	ap = dict(ap) # makes a copy, at least of the container dict
	ap['duration_samples'] = len(ap.pop('fullfreq_hz'))
	ap.update(kwargs)
	axis=ap.pop('axis', -1)
	extra_axis = axis+1
	for v in ap.values(): extra_axis = max([extra_axis, len(getattr(v, 'shape', []))])
	ap['freq_hz'] = IncreaseDimensionality(ap['freq_hz'], extra_axis).swapaxes(axis,0)
	ap['axis'] = extra_axis
	r = GenerateWaveform(**ap)
	r = r.swapaxes(extra_axis, axis)
	r = r.sum(axis=extra_axis)
	return r

def _MakeFade(x, start, stop, direction, cosine=True):
	scale = float(stop - start)
	if scale <= 0.0:
		x = x * 0.0 # makes a copy
		x += 1.0
	else:
		x = x - start # makes a copy
		x /= scale
		numpy.fmin(numpy.fmax(x, 0.0, out=x), 1.0, out=x) 
		if cosine:
			x *= PI
			numpy.cos(x, out=x)
			x *= -0.5 * direction
			x += 0.5
		elif direction == -1.0:
			x *= direction
			x += 1.0
	return x

def Shoulder( x, s, complement=False, cosine=True ):
	"""
	Return a (possibly asymmetric) Tukey window function of `x`.
	`s` may have 1, 2, 3 or 4 elements:
	
	1.  raised cosine between `x=s[0]-0.5` and `x=s[0]+0.5`
	2.  raised cosine between `x=s[0]` and `x=s[1]`
	3.  raised cosine rise from `s[0]` to `s[1]`, and fall from `s[1]` to `s[2]`
	4.  raised cosine rise from `s[0]` to `s[1]`, plateau from `s[1]` to `s[2]`,
	    and fall from `s[2]` to `s[3]`
	"""
	if len(s) == 1: s = [s[0]-0.5, s[0]+0.5]
	if len(s) == 2: s = [s[0], 0.5*(s[0]+s[1]), s[1]]
	if len(s) == 3: s = [s[0], s[1], s[1], s[2]]
	if len(s) != 4: raise ValueError( "s must have 1, 2, 3 or 4 elements" )
	xrise = _MakeFade(x, s[0], s[1], +1.0, cosine=cosine)
	xfall = _MakeFade(x, s[2], s[3], -1.0, cosine=cosine)
	w = numpy.fmin(xrise, xfall, out=xrise)
	if complement: w *= -1.0; w += 1.0
	return w
	
def Hilbert(x, N=None, axis=0, band=(), samplingfreq_hz=None, return_dict=False):
	"""
	Compute the analytic signal, just like `scipy.signal.hilbert` but
	with the differences that (a) the computation can be performed
	along any axis and (b) a limited band of the signal may be
	considered.  The `band` argument can be a two-, three- or
	four-element tuple suitable for passing to `Shoulder()`, specifying
	the edges of the passband (expressed in Hz if `samplingfreq_hz` is
	explicitly supplied, or relative to Nyquist if not).
	
	If `return_dict` is True, do not return just the complex analytic signal
	but rather a dict containing its amplitude, phase, and unwrapped phase
	difference.
	"""
	
	fs = get_fs( x )
	if samplingfreq_hz is not None: fs = samplingfreq_hz
	if fs is None: fs = 2.0
	x = getattr( x, 'y', x ) # audiomath.Sound support
	
	if N is None: N = x.shape[ axis ]
	shape = [ 1 for d in x.shape ]
	shape[ axis ] = N
	h = numpy.zeros( shape, dtype=numpy.float64 )
	if N % 2:
		h.flat[ 0 ] = 1
		h.flat[ 1:(N+1) / 2 ] = 2
	else:
		h.flat[ 0 ] = h.flat[ N/2 ] = 1
		h.flat[ 1:N/2 ] = 2
	x = fft( x, n=N, axis=axis )
	x = numpy.multiply( x, h )
	if len( band ):
		f = fftfreqs( N, samplingfreq_hz=fs )
		h.flat = Shoulder( numpy.abs( f ), band )
		x = numpy.multiply( x, h )
	x = ifft( x, n=N, axis=axis )
	if not return_dict: return x
	amplitude = numpy.abs( x )
	phase_rad = numpy.angle( x )
	deltaphase_rad = UnwrapDiff( phase_rad, base=TWO_PI, axis=axis )[ 0 ]
	return {
		'amplitude': amplitude,
		'phase_rad': phase_rad,
		'deltaphase_rad': deltaphase_rad,
	}

def ReweightSpectrum( s, func, *pargs, **kwargs ):
	"""
	Brutally filter the sound `s` by transforming into the
	Fourier domain, weighting the amplitude spectrum, and
	transforming back. The filtering is non-causal and
	(TODO) will have wrap-around artifacts whereby the two
	ends of the signal may bleed into each other, so use
	with caution---it is most suitable for noise or for
	periodic signals. No group delay is introduced.
	
		Args:
			s (numpy.ndarray or audiomath.Sound):
				The input sound data. If `s` is an array,
				a new array will be returned. If it is a
				`Sound` instance, `s` will get changed
				in-place (the array `s.y` will be replaced
				by a new array) and returned. 
			
			func (callable):
				A function that takes a numeric array
				of frequencies, in Hz, as its first
				(and only required) argument, and
				outputs a corresponding array of weights.
	
			samplingfreq_hz (float):
				Sampling frequencym in Hz. Not needed if
				`s` is a `Sound` instance.
	
			axis (int):
				Axis along which time runs. Not needed if
				`s` is a `Sound` instance.
		
	Additional `*pargs` and `**kwargs` are passed straight
	through to `func()`.
	"""
	if isinstance( s, numpy.ndarray ): y, s = s, None
	elif hasattr(s, 'y'): y = s.y
	else: raise TypeError( "don't know how to handle this kind of container object" )
	samplingfreq_hz = kwargs.pop( 'samplingfreq_hz', get_fs( s ) )
	axis = kwargs.pop( 'axis', getattr( s, 'ACROSS_SAMPLES', None ) )
	# TODO: pad to minimize wraparound effects (maybe give an option to append an odd-symmetric
	#       copy of the signal, perhaps superimposed on a linear trend to make it meet both ends?)
	Y = Spectrum( y, axis=axis, samplingfreq_hz=samplingfreq_hz )
	amp = Y[ 'amplitude' ]
	freq = IncreaseDimensionality( Y[ 'freq_hz' ], amp.ndim - 1 ).swapaxes( 0, Y[ 'axis' ] )
	wt = func( freq, *pargs, **kwargs )
	wt[ numpy.isnan( wt ) | numpy.isinf( wt ) ] = 1.0
	amp *= wt
	y = InverseSpectrum( Y )
	if s is None: return y
	s.y = y
	return s

