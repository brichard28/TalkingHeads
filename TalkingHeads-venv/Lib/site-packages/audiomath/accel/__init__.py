import os
import ctypes
import struct
import inspect
import platform

def LoadLib( dllNameStem, usePlatformInflection=True ):
	machine = platform.machine().lower()
	if machine in [ '', 'i386', 'x86_64', 'amd64' ]:
		arch = '%dbit' % ( struct.calcsize( 'P' ) * 8 ) # remember this will depend on the Python executable, not just the machine
	else:
		arch = machine
		if arch.startswith( 'armv' ): arch = arch.rstrip( 'l' )
	uname = platform.system()
	if   uname.lower().startswith( 'win'    ): dllPrefix, dllExtension = '',    '.dll'
	elif uname.lower().startswith( 'darwin' ): dllPrefix, dllExtension = 'lib', '.dylib'
	else:                                      dllPrefix, dllExtension = 'lib', '.so'
	platformInflection = '-' + uname + '-' + arch
	if isinstance( usePlatformInflection, str ) and usePlatformInflection.lower() == 'win64only':
		platformInflection = '64' if platformInflection == '-Windows-64bit' else ''
	if usePlatformInflection: dllNameStem += platformInflection
	dllName = ( '' if dllNameStem.startswith( dllPrefix ) else dllPrefix ) + dllNameStem + dllExtension
	dllNameStem = dllNameStem[ len( dllPrefix ): ]
	try: file = __file__
	except NameError: file = None
	if not file:
		try: frame = inspect.currentframe(); file = inspect.getfile( frame )
		finally: del frame  # https://docs.python.org/3/library/inspect.html#the-interpreter-stack
	HERE = os.path.dirname( os.path.realpath( file ) )
	dllPath = os.path.join( HERE, dllName )
	return ctypes.CDLL( dllPath )

dll = LoadLib( 'libaudiochunk' )

TransferAudioChunk = dll.TransferAudioChunk
TransferAudioChunk.restype = ctypes.c_double
TransferAudioChunk.argtypes = (
	ctypes.c_char_p,                     # outputBaseAddress
	ctypes.c_uint,                       # outputItemSize
	ctypes.c_uint,                       # outputNumberOfSamples
	ctypes.c_uint,                       # outputNumberOfChannels
	ctypes.c_uint,                       # outputSampleStride
	ctypes.c_uint,                       # outputChannelStride
	
	ctypes.c_char_p,                     # inputBaseAddress
	ctypes.c_uint,                       # inputItemSize
	ctypes.c_uint,                       # inputNumberOfSamples
	ctypes.c_uint,                       # inputNumberOfChannels
	ctypes.c_uint,                       # inputSampleStride
	ctypes.c_uint,                       # inputChannelStride
	
	ctypes.c_uint,                       # isLooped
	ctypes.c_double,                     # speed
	ctypes.c_double,                     # inputSampleOffset

	ctypes.c_double,                     # leftVolume
	ctypes.c_double,                     # rightVolume
	ctypes.c_uint,                       # numberOfLevels
	ctypes.POINTER( ctypes.c_double ),   # levels
	
	ctypes.c_uint,                       # isFirstInChain
)	
