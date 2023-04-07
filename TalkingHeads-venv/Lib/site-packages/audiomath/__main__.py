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
If no options are supplied, `-s` is assumed---i.e., an IPython
shell will be opened on the console, with `audiomath` and `numpy`
already imported (both under their full names and under their
respective abbreviated names, `am` and `np`).

If options are supplied, the shell will not be opened unless the
`-s` option is explicitly present among them.
"""
import ast
import time
import argparse

import audiomath, audiomath as am
		
parser = argparse.ArgumentParser( prog='python -m audiomath', description=__doc__ )
parser.add_argument( "-v", "--version", action='store_true', default=False, help='print the version number' )
parser.add_argument( "-V", "--versions", action='store_true', default=False, help='print package and dependency version information' )
parser.add_argument( "-p", "--package-path", metavar='RELATIVE_PATH',  action='store', default=None, help='take a filesystem path that is expressed relative to the audiomath package location, resolve it, and print it as an absolute path' )
parser.add_argument( "-a", "--apis", "--host-apis", action='store_true', default=False, help='print a list of host APIs' )
parser.add_argument( "-l", "--list-devices", "--devices", action='store_true', default=False, help='print a list of devices' )
parser.add_argument( "-2", "--twoChannelTest", action='store_true', default=False, help='same as -t2, i.e. play a 2-channel test stimulus on an endless loop' )
parser.add_argument( "-8", "--eightChannelTest", action='store_true', default=False, help='same as -t8, i.e. play an 8-channel test stimulus on an endless loop' )
parser.add_argument( "-t", "--test",  metavar='NUMBER_OF_CHANNELS', action='store', default=0, type=int, help='play a test stimulus with the specified number of channels (up to 8) on an endless loop' )
parser.add_argument( "-g", "--glitch-test",  "--tone-test", action='store_true', default=False, help='generate and play a seamlessly looped tone.' )
parser.add_argument( "-s", "--shell", action='store_true', default=False, help='open an IPython shell, even if other flags are supplied' )
parser.add_argument( "-d", "--device",  metavar='DEVICE_INDEX',  action='store', default=None, help='specify which device should be used for playback in the --test and/or --glitch-test' )
parser.add_argument(       "--install-ffmpeg",  metavar='PATH_TO_FFMPEG_BINARY',  action='store', default=None, type=str, help='call `ffmpeg.Install()` on the specified path' )
parser.add_argument(       "--install-sox",  metavar='PATH_TO_SOX_BINARY', action='store', default=None, type=str, help='call `sox.Install()` on the specified path' )
parser.add_argument(       "--ptb", "--psychtoolbox", metavar='DEFAULT_LATENCY_CLASS',  action='store', default=None, help='if omitted, use the default back-end. If supplied, use the "PsychToolboxInterface" back-end, and set its default latency class to the specified value (3 is recommended).' )
parser.add_argument( "-m", "--master-volume", "--system-volume", metavar='LEVEL[:MUTE_STATUS]',  action='store', default=None, help='lastingly set the master volume to LEVEL (0.0 to 1.0) and the mute status to MUTE_STATUS (0=unmuted, 1=muted)' )
parser.add_argument( "-c", "--config", metavar='SAMPLE_RATE[:MIN_LATENCY_MSEC[:BUFFER_LENGTH_MSEC]]',  action='store', default='', help='set sampling frequency, minimum latency (msec) and/or buffer size (msec) for the test stimuli. (You can also specify buffer length in samples instead of milliseconds, by putting the value in brackets.)' )

opts = parser.parse_args( args=None ) # args=sys.argv[ 1: ]
#opts, argv = parser.parse_known_args( args=None )

openShell = True
player = None
playerName = 'p'
tone = None
toneName = 't'
fs = None
minLatencyMsec = None
bufferLengthMsec = None

if opts.config:
	parameters = opts.config.replace( ':', '+' ).split( '+' )
	if parameters: fs = parameters.pop( 0 )
	if parameters: minLatencyMsec = parameters.pop( 0 )
	if parameters: bufferLengthMsec = parameters.pop( 0 )
	fs = None if fs.lower() == 'none' or not fs else float( fs )

if opts.ptb:
	latencyClass = opts.ptb
	if latencyClass.lower() in [ 'psychopy', '-3' ]:
		am.BackEnd.Load( 'PsychoPyInterface' )
		am.LATENCY_CLASS.DEFAULT = -3
	else:
		am.BackEnd.Load( 'PsychToolboxInterface' )
		if latencyClass == '': latencyClass = 'DEFAULT'
		try: latencyClass = int( latencyClass )
		except: latencyClass = getattr( am.LATENCY_CLASS, latencyClass.upper() )
		am.LATENCY_CLASS.DEFAULT = latencyClass

if opts.version:
	openShell = opts.shell
	print( am.__version__ )

if opts.versions:
	openShell = opts.shell
	print( '' )
	am.ReportVersions()

if opts.package_path:
	openShell = opts.shell
	print( am.PackagePath( opts.package_path ) )
	
if opts.apis:
	openShell = opts.shell
	print( '' )
	print( am.GetHostApiInfo() )

if opts.list_devices:
	openShell = opts.shell
	print( '' )
	print( am.GetDeviceInfo() )

if opts.eightChannelTest and not opts.test: opts.test = 8
if opts.twoChannelTest   and not opts.test: opts.test = 2

if opts.master_volume:
	openShell = opts.shell
	parameters = opts.master_volume.replace( ':', '+' ).split( '+' )
	vargs = {}
	if len( parameters ) >= 1 and parameters[ 0 ]: vargs[ 'level' ] = float( parameters[ 0 ] )
	if len( parameters ) >= 2 and parameters[ 1 ]: vargs[ 'mute'  ] = bool( ast.literal_eval( parameters[ 1 ] ) )
	from audiomath.SystemVolume import SetVolume
	vargs = SetVolume( **vargs )
	print( '{%s}' % ', '.join( repr( k ) + ':' + fmt % vargs[ k ] for term in 'level:%g mute:%s previousLevel:%g previousMute:%s'.split() for k, fmt in [ term.split( ':' ) ] if k in vargs ) )
	
if opts.glitch_test:
	openShell = opts.shell
	tone = am.ToneTest( fs=fs, device=opts.device, bufferLengthMsec=bufferLengthMsec, minLatencyMsec=minLatencyMsec, verbose=False, playing=True )
	print( tone._report( with_repr='short', indent=toneName + ' = ' ) )
	if not openShell and not opts.test:
		tone.WaitFor( am.Prompt( 'press return to stop/exit: ' ), False )
		del tone; time.sleep( 0.25 )
	
if opts.test:
	openShell = opts.shell
	player = am.Player( am.TestSound( list( range( opts.test ) ) ), fs=fs, device=opts.device, bufferLengthMsec=bufferLengthMsec, minLatencyMsec=minLatencyMsec, loop=True, playing=True )
	print( player._report( with_repr='short', indent=playerName + ' = ' ) )
	if not openShell:
		player.WaitFor( am.Prompt( 'press return to stop/exit: ' ), False )
		if tone: del tone
		del player; time.sleep( 0.25 )

if opts.install_ffmpeg:
	openShell = opts.shell
	try: am.ffmpeg.Install( opts.install_ffmpeg )
	except Exception as err: sys.sterr.write( '%s\n' % err )

if opts.install_sox:
	openShell = opts.shell
	try: am.sox.Install( opts.install_sox )
	except Exception as err: sys.sterr.write( '%s\n' % err )

if openShell:
	def Shell():
		if player: locals()[ playerName ] = player
		if tone: locals()[ toneName ] = tone
		import os, sys, time, IPython, numpy, numpy as np, audiomath, audiomath as am
		del sys.argv[ 1: ]
		print( '' )
		IPython.start_ipython( user_ns=locals() )	
	Shell()
