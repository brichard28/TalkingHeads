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
Defines a symbol `CURRENT_BACK_END` and function `Load()` for
dynamically switching between different "back ends", i.e. different
implementations of `Player` and `Recorder` code.  The default
back-end, loaded when the `audiomath` package is first imported,
is the `PortAudioInterface`. This can be changed as and when other
back-ends are written.
"""
__all__ = [
	'CURRENT_BACK_END',
]

DEFAULT = 'PortAudioInterface'

import re as _re
import sys as _sys
class _NotLoaded( object ):
	__bool__ = __nonzero__ = lambda self: False
	__getattr__ = lambda self, attrName: getattr( Load(), attrName )
CURRENT_BACK_END = _NotLoaded()

def Load( name=None ):
	"""
	`Load('PortAudioInterface')` is performed automatically when
	the `audiomath` package is imported.  It does not yet load
	any PortAudio-specific binaries, but it does establish that
	the `PortAudioInterface.Player` and `PortAudioInterface.Recorder`
	should be the default player and recorder implementations, by
	importing these classes into the top-level `audiomath.*`
	namespace. It also imports PortAudio-specific global functions
	like `GetHostApiInfo()` and other items such as `PORTAUDIO`,
	which represents the library itself.
	
	If you write another back-end (creating subclasses of 
	`GenericInterface.Player` and `GenericInterface.Recorder` just
	as `PortAudioInterface` does) then you can `Load()` that instead,
	similarly by passing the name of the submodule. The symbols from
	the previously-loaded back-end will be removed from the top-level
	namespace and replaced by whatever your submodule exports in its
	`__all__` attribute.
	
	The currently-loaded back-end is also available as
	`CURRENT_BACK_END`.
	"""
	global CURRENT_BACK_END
	if not name and not CURRENT_BACK_END:
		name = DEFAULT
	
	target = _sys.modules[ __package__ ]

	oldBackEnd = CURRENT_BACK_END
	
	if name:
		exec( 'from . import {name}'.format( name=_re.sub(r'[^a-zA-Z0-9_].*', '', name ) ) )
		CURRENT_BACK_END = locals()[ name ]
		setattr( target, name, CURRENT_BACK_END )
		
	if oldBackEnd:
		for symbol in oldBackEnd.__all__:
			if hasattr( target, symbol ):
				delattr( target, symbol )
				
	setattr( target, 'CURRENT_BACK_END', CURRENT_BACK_END )
	for symbol in CURRENT_BACK_END.__all__:
		setattr( target, symbol, getattr( CURRENT_BACK_END, symbol ) )
	return CURRENT_BACK_END
