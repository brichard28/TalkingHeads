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
ONLY USE THIS FOR PERFORMANCE TESTING DURING DEVELOPMENT.
OTHERWISE, USE `PsychToolboxInterface` INSTEAD.

This is a playback back-end, mostly identical to the
`PsychToolboxInterface` back-end, but with a `Player` class
that wraps `psychtoolbox` functionality *indirectly* via
`psychopy.sound.Sound` (in PTB mode) instead of directly. The
`Player` here is very much less flexible, containing only the
minimal functionality required by the `PlayerLatency.py`
performance tests, and since it relies on `psychopy` it brings
with it an enormous number of extra dependencies.  In theory,
the more fully-featured, less-dependency-heavy
`PsychToolboxInterface` back-end *should* perform identically
to this one in terms of latency. The only reason to use this
one is to verify that our `PsychToolboxInterface` wrapping
isn't missing some extra tuning trick that Peirce and co
might have figured out in their `psychopy.sound` wrapping.
(The performance I've seen so far, as at 2020-02-20, is
identical, so we probably aren't missing anything.)
"""

import os
import tempfile

from psychopy import prefs
prefs.hardware[ 'audioLib' ] = [ 'PTB' ]
from psychopy.sound import Sound as PSS

from . import PsychToolboxInterface; from .PsychToolboxInterface import *
__all__ = list( PsychToolboxInterface.__all__ )

class Player( PSS ):
	def __init__( self, sound, device=None, stream=None, latencyClass='DEFAULT', bufferLengthMsec=None, minLatencyMsec='auto', fs=None, resample=True, verbose=None, **kwargs ):
		tmp = None
		if isinstance( latencyClass, str ): latencyClass = getattr( LATENCY_CLASS, latencyClass.upper() )
		if abs( latencyClass ) != 3: raise NotImplementedError( 'need latencyClass=3 until we figure out how to pass that setting into psychopy.sound.Sound' )
		self.latencyClass = latencyClass
		self.minLatencyMsec = None  # corresponding constructor argument is unused
		self.bufferLengthMsec = None  # corresponding constructor argument is unused
		# constructor argument fs is also ignored
		if hasattr( sound, 'Write' ):
			with tempfile.NamedTemporaryFile( suffix='.wav', delete=False ) as tmp: pass
			sound.Write( tmp.name )
			sound = sound.filename
		PSS.__init__( self, sound )
		self.loop = False
		if tmp:
			try: os.remove( tmp.name )
			except: pass
		self.stream.outputDevice = GetDeviceInfo()[ int( self.track.status[ 'OutDeviceIndex' ] ) ]
	def Play( self, loop=None ):
		if loop is not None: self.loop = loop
		status = self.track.status
		alreadyPlaying = status.get( 'Active', 0 ) or status.get( 'State', 0 )
		if not alreadyPlaying: self.play( loops=0 if self.loop else 1 )
	def Pause( self, loop=None ):
		if loop is not None: self.loop = loop
		self.pause()
	Stop = Pause
	
	@property
	def fs( self ):
		return self.__stream.fs
		
