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
Package introspection tools.
"""
__all__ = [
	'__meta__',
	'__version__',
	'__homepage__',
	
	'WhereAmI',
	'PackagePath',
	'ComputerName',
	'GetRevision',
	'Manifest',
	
	'FindFile',
]

import os
import re
import sys
import ast
import glob
import shlex
import socket
import inspect
import textwrap
import subprocess

if sys.version < '3': bytes = str
else: unicode = str; basestring = ( unicode, bytes )
def IfStringThenRawString( x ):
	return x.encode( 'utf-8' ) if isinstance( x, unicode ) else x
def IfStringThenNormalString( x ):
	if str is bytes or not isinstance( x, bytes ): return x
	try: return x.decode( 'utf-8' )
	except: pass
	try: return x.decode( sys.getfilesystemencoding() )
	except: pass
	return x.decode( 'latin1' ) # bytes \x00 to \xff map to characters \x00 to \xff (so, in theory, cannot fail)

def WhereAmI( nFileSystemLevelsUp=1, nStackLevelsBack=0 ):
	"""
	`WhereAmI( 0 )` is equivalent to `__file__`
	
	`WhereAmI()` or `WhereAmI(1)` gives you the current source file's
	parent directory.
	"""
	my_getfile = inspect.getfile
	if getattr( sys, 'frozen', False ) and hasattr( sys, '_MEIPASS' ):
		# sys._MEIPASS indicates that we're in PyInstaller which, in a surprise reversal
		# of the old py2exe situation, supports `__file__` but NOT `inspect.getfile()`.
		# The following workaround is adapted from
		# http://lists.swapbytes.de/archives/obspy-users/2017-April/002395.html
		def my_getfile( object ):
			if inspect.isframe( object ):
				try: return object.f_globals[ '__file__' ]
				except: pass
			return inspect.getfile( object )
			
	try:
		frame = inspect.currentframe()
		for i in range( abs( nStackLevelsBack ) + 1 ):
			frame = frame.f_back
		file = my_getfile( frame )
	finally:
		del frame  # https://docs.python.org/3/library/inspect.html#the-interpreter-stack
	return os.path.realpath( os.path.join( file, *[ '..' ] * abs( nFileSystemLevelsUp ) ) )


def Bang( cmd, shell=False, stdin=None, cwd=None, raiseException=False ):
	windows = sys.platform.lower().startswith('win')
	# If shell is False, we have to split cmd into a list---otherwise the entirety of the string
	# will be assumed to be the name of the binary. By contrast, if shell is True, we HAVE to pass it
	# as all one string---in a massive violation of the principle of least surprise, subsequent list
	# items would be passed as flags to the shell executable, not to the targeted executable.
	# Note: Windows seems to need shell=True otherwise it doesn't find even basic things like ``dir``
	# On other platforms it might be best to pass shell=False due to security issues, but note that
	# you lose things like ~ and * expansion
	if isinstance( cmd, str ) and not shell:
		if windows: cmd = cmd.replace( '\\', '\\\\' ) # otherwise shlex.split will decode/eat backslashes that might be important as file separators
		cmd = shlex.split( cmd ) # shlex.split copes with quoted substrings that may contain whitespace
	elif isinstance( cmd, ( tuple, list ) ) and shell:
		quote = '"' if windows else "'"
		cmd = ' '.join( ( quote + item + quote if ' ' in item else item ) for item in cmd )
	try: sp = subprocess.Popen( cmd, shell=shell, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
	except OSError as exc: returnCode, output, error = 'command failed to launch', '', str( exc )
	else: output, error = [ IfStringThenNormalString( x ).strip() for x in sp.communicate( stdin ) ]; returnCode = sp.returncode
	if raiseException and returnCode:
		if isinstance( returnCode, int ): returnCode = 'command failed with return code %s' % returnCode
		raise OSError( '%s:\n    %s\n    %s' % ( returnCode, cmd, error ) )
	return returnCode, output, error
	

	
PACKAGE_LOCATION = WhereAmI()

def PackagePath( *pieces ):
	"""
	Return a resolved absolute filesystem path based on the
	`pieces` that are expressed relative to the location
	of this package. Useful for finding resources within a
	package.
	
	The returned path will contain forward or backward
	slashes (whichever is native to the filesystem) and
	will not have a trailing slash.
	"""
	return os.path.realpath( os.path.join( PACKAGE_LOCATION, *pieces ) )

def StripPackagePath( path ):
	"""
	The inverse of `PackagePath()`: given a path that may
	or may not be absolute, return the path relative to the
	package location if it is inside the package. If the
	path is not inside the package, return an absolute path.
	
	The returned path always has forward slashes and no
	trailing slash.
	"""
	path = os.path.realpath( path ).replace( '\\', '/' ).rstrip( '/' )
	prefix = PACKAGE_LOCATION.replace( '\\', '/' ).rstrip( '/' )
	if sys.platform.lower().startswith( ( 'win', 'darwin' ) ): f = lambda x: x.lower()
	else: f = lambda x: x
	if f( path ) == f( prefix ): return ''
	prefix += '/'
	if f( path ).startswith( f( prefix ) ): return path[ len( prefix ) : ]
	return path

def ComputerName():
	"""
	Return the name of the computer.
	"""
	return os.path.splitext( socket.gethostname() )[ 0 ].lower()

def GetRevision():
	"""
	If this package is installed as an "editable" copy, running
	out of a location that is under version control by Mercurial
	or git (which is the way it is developed), then return
	information about the current revision.
	"""
	rev = '@REVISION@'
	if rev.startswith( '@' ):
		rev = 'unknown revision'
		possibleRepo = PackagePath( '..', '..' )
		repoSubdirectories = [ entry for entry in os.listdir( possibleRepo ) if os.path.isdir( os.path.join( possibleRepo, entry ) ) ]
		if all( x in repoSubdirectories for x in [ '.git', 'python' ] ): # then we're probably in the right place
			out = ' '.join(
				stdout.strip()
				for cmd in [
					'git log -1 "--format=%h %ci"',
					'git describe --always --all --long --dirty=+ --broken=!',
				] for errorCode, stdout, stderr in [ Bang( cmd, cwd=possibleRepo ) ] if not errorCode
			)
			if out: rev = 'git ' + out 
		elif all( x in repoSubdirectories for x in [ '.hg', 'python' ] ): # then we're probably in the right place
			errorCode, stdout, stderr = Bang( 'hg id -intb -R "%s"' % possibleRepo )
			if not errorCode: rev = 'hg ' + stdout
	return rev
	

__meta__ = ast.literal_eval( open( PackagePath( 'MASTER_META' ), 'rt' ).read() )
__version__ = __meta__[ 'version' ]
__homepage__ = __meta__[ 'homepage' ]

def SearchForFiles( top, relstart='', patterns=() ):
	class wd( object ):
		def __init__( self, target ): self.target = target
		def __enter__( self ): self.olddir = os.getcwd(); os.chdir( self.target ); return self
		def __exit__( self, *blx ): os.chdir( self.olddir )
	if isinstance( top, ( tuple, list ) ): top = os.path.join( *top )
	if isinstance( relstart, ( tuple, list ) ): relstart = os.path.join( *relstart )
	if not relstart: relstart = '.'
	with wd( top ): files = [ os.path.join( d, f ) for d, subdirs, files in os.walk( relstart ) for f in files ]
	files = [ f.replace( '\\', '/' ) for f in files ]
	files = [ ( f[ 2: ] if f.startswith( './' ) else f ) for f in files ]
	if patterns: files = [ f for f in files if any( re.findall( pattern, f, re.I ) for pattern in patterns ) ]
	return files

def AddPackageData( mode, container, paths=(), regex=(), subpackage=None, include_modes=None, exclude_modes=None ):
	if include_modes is not None and mode not in include_modes: return container
	if exclude_modes is not None and mode     in exclude_modes: return container
	if not isinstance( paths, ( tuple, list ) ): paths = [ paths ]
	if not isinstance( regex, ( tuple, list ) ): regex = [ regex ]
	if subpackage:
		searchRoot = PackagePath( *subpackage.split( '.' ) )
		fullPackageName = __package__ + '.' + subpackage
	else:
		searchRoot = PackagePath()
		fullPackageName = __package__
	searchRoot = searchRoot.replace( '\\', '/' ).rstrip( '/' )
	matches = list( paths )
	if regex: matches += SearchForFiles( searchRoot, patterns=regex )
	if mode == 'setup':
		# `container` should be a dict of arguments to be passed to `setup()`
		if container is None: container = {} 
		packages = container.setdefault( 'packages', [] )
		if fullPackageName not in packages: packages.append( fullPackageName )
		package_data = container.setdefault( 'package_data', {} )
		package_data = package_data.setdefault( fullPackageName, [] )
		package_data += matches
	elif mode == 'pyinstaller':
		# `container` should be a dict of arguments to be passed to Analysis()
		# or possibly just `list` that will be passed as the `datas` argument
		if container is None: container = {}
		if isinstance( container, list ): datas = container
		else: datas = container.setdefault( 'datas', [] )
		datas += [
			( searchRoot + '/' + match, fullPackageName.replace( '.', '/' ) + '/' +  os.path.dirname( match ) )
			for match in matches
		]
	else:
		raise ValueError( 'unknown mode %r' % mode )
	return container

def Manifest( mode='setup', container=None ):
	"""
	`container` may be a `dict` of keyword arguments that
	are going to be passed to `setuptools.setup()` (assuming
	`mode='setup'`).   Or it may be the `dict` of keyword
	arguments that are going to be passed to
	`pyinstaller.Analysis()` (assuming `mode='pyinstaller'`).
	"""	
	for item in __meta__[ 'manifest' ]:
		container = AddPackageData( mode, container, **item )
	return container

class Indenter( object ):
	def __init__( self, *pargs, **kwargs ):
		self.things = dict( *pargs, **kwargs )
	def __getitem__( self, arg ):
		key = arg.lstrip()
		prefix = arg[ :-len( key )  ]
		txt = str( self.things[ key ] )
		return ''.join( prefix + line for line in textwrap.dedent( txt.replace( '\t', '    ' ) ).splitlines( True ) ).strip()
# __meta__[ 'indent' ] = Indenter( __meta__ ) # allows things like long_description='...\n* {indent[  citation]}\n...'.format( **__meta__ )


### AUDIOMATH-SPECIFIC
def FindFile( filename ):
	"""
	Look for a file based on `filename`.  Return the full path
	to it if it can be found, or `None` if not.
	
	If the `filename` does not include a file extension, try a
	number of different common extensions. 
	
	If the `filename` does not specify a parent directory, look
	in the current working directory *and* in the `example_media`
	directory that is bundled with this package.
	"""
	if not isinstance( filename, str ): return
	filename = os.path.expanduser( filename )
	variants = []
	parent, basename = os.path.split( filename )
	stem, extension = os.path.splitext( basename )
	basenames = [ basename ]
	if not extension: basenames.extend( basename + extensionVariant for extension in '.wav .mp3 .ogg .aac .m4a'.split() for extensionVariant in [ extension, extension.upper() ] )
	if parent: parents = [ os.path.realpath( parent ) ]
	else: parents = [ os.getcwd(), PackagePath( 'example_media' ) ]
	for parent in parents:
		for basename in basenames:
			variant = os.path.join( parent, basename )
			if os.path.isfile( variant ): return variant
		
