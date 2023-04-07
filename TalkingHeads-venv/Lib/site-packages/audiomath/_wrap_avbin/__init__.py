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
# 
# This file was adapted from pyglet.media.sources.avbin (any redistribution
# of this file must therefore also reproduce the pyglet credits and license
# information below). It is designed to be packaged with the AVBin binaries
# right here, right now so that you do not have to install anything system-wide,
# and so that compatibility between this Python wrapper and the binaries can
# be maintained: "batteries included" philosophy.
# 
# The difficulties with extracting things from pyglet are (a) that every
# tiniest part of pyglet imports the whole of pyglet, and (b) that importing
# pyglet has side effects (e.g. the Shadow Window) which must be explicitly
# avoided.
# 
# Here's the pyglet info:
# 
# ----------------------------------------------------------------------------
# pyglet
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions 
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright 
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

"""
Use avbin to decode audio and video media.

Adapted from `pyglet.media.sources.avbin` by removing dependence on
the rest of the `pyglet` package.
"""
from __future__ import print_function
from __future__ import division

import os
import sys
import time
import struct
import atexit
import ctypes
import inspect
import platform
import threading

_debug = False

#from pyglet.media.exceptions import MediaFormatException # let's duck-type this instead
class MediaException(Exception): pass
class MediaFormatException(MediaException): pass

#from pyglet.media.sources.base import StreamingSource, SourceInfo, AudioData, AudioFormat, VideoFormat # let's duck-type these instead
class StreamingSource(object):
    audio_format = None
    video_format = None
    info = None
    _duration = None
    @property
    def duration(self):
        return self._duration
class SourceInfo( object ):
    pass
class AudioData(object):
    def __init__(self, data, length, timestamp, duration, events):
        self.data = data
        self.length = length
        self.timestamp = timestamp
        self.duration = duration
        self.events = events
class AudioFormat(object):
    def __init__(self, channels, sample_size, sample_rate):
        self.channels = channels
        self.sample_size = sample_size
        self.sample_rate = sample_rate
        # Convenience
        self.bytes_per_sample = (sample_size >> 3) * channels
        self.bytes_per_second = self.bytes_per_sample * sample_rate
    def __eq__(self, other):
        return ( self.channels == other.channels and self.sample_size == other.sample_size and self.sample_rate == other.sample_rate )
    def __ne__(self, other):
        return not self.__eq__(other)
    def __repr__(self):
        return '%s(channels=%d, sample_size=%d, sample_rate=%d)' % ( self.__class__.__name__, self.channels, self.sample_size, self.sample_rate )
class VideoFormat(object):
    def __init__(self, width, height, sample_aspect=1.0):
        self.width = width
        self.height = height
        self.sample_aspect = sample_aspect
        self.frame_rate = None
#from pyglet image import ImageData # let's replace this with something much simpler
class ImageData(object):
	def __init__(self, width, height, format, data, pitch=None):
		if pitch is None: pitch = width * len( format )
		self.width, self.height, self.format, self.data, self.pitch = width, height, data, format, pitch
		self.__array_interface__ = dict( version=3, typestr='uint8', data=( ctypes.cast( data, ctypes.c_void_p ).value, True ), shape=( height, width, len( format ) ) )
# from pyglet.media.threads import WorkerThread # here's the complete source of that class pasted (but with whitespace compressed and docstrings removed) from pyglet 1.3.2
class MediaThread(object):
    """A thread that cleanly exits on interpreter shutdown, and provides
    a sleep method that can be interrupted and a termination method"""
    _threads = set()
    _threads_lock = threading.Lock()
    def __init__(self, target=None):
        self._thread = threading.Thread(target=self._thread_run)
        self._thread.setDaemon(True)
        if target is not None: self.run = target
        self.condition = threading.Condition()
        self.stopped = False
    @classmethod
    def _atexit(cls):
        with cls._threads_lock: threads = list(cls._threads)
        for thread in threads: thread.stop()
    def run(self): pass
    def _thread_run(self):
        with self._threads_lock: self._threads.add(self)
        self.run()
        with self._threads_lock: self._threads.remove(self)
    def start(self):
        self._thread.start()
    def stop(self):
        #assert _debug('MediaThread.stop()')
        with self.condition:
            self.stopped = True
            self.condition.notify()
        self._thread.join()
    def sleep(self, timeout):
        #assert _debug('MediaThread.sleep(%r)' % timeout)
        with self.condition:
            if not self.stopped: self.condition.wait(timeout)
    def notify(self):
        #assert _debug('MediaThread.notify()')
        with self.condition:
            self.condition.notify()
atexit.register(MediaThread._atexit)
class WorkerThread(MediaThread):
    def __init__(self, target=None):
        super(WorkerThread, self).__init__(target)
        self._jobs = []
    def run(self):
        while True:
            job = self.get_job()
            if not job: break
            job()
    def get_job(self):
        with self.condition:
            while self._empty() and not self.stopped: self.condition.wait()
            if self.stopped: result = None
            else: result = self._get()
        return result
    def put_job(self, job):
        with self.condition:
            self._put(job)
            self.condition.notify()
    def clear_jobs(self):
        with self.condition:
            self._clear()
            self.condition.notify()
    def _empty(self): return not self._jobs
    def _get(self): return self._jobs.pop(0)
    def _put(self, job): self._jobs.append(job)
    def _clear(self): del self._jobs[:]
#from pyglet.compat import asbytes, asbytes_filename  # let's duck-type these instead
asbytes = asbytes_filename = str
if sys.version_info[ 0 ] >= 3:
    def asbytes(s):
        if isinstance(s, bytes): return s
        elif isinstance(s, str): return s.encode( 'utf-8' )
        else: return bytes(s)
    def asbytes_filename(s):
        if isinstance(s, bytes): return s
        elif isinstance(s, str): return s.encode(encoding=sys.getfilesystemencoding())
### end duck-typing.  Watch out for remaining pyglet imports in specific situations below
### Here's a helper for those remaining instances:
def AvoidPygletImportSideEffects( msg=None ):
	if _debug and msg: print( 'importing pyglet (%s)' % msg )
	if 'pyglet' not in sys.modules:
		os.environ[ 'PYGLET_SHADOW_WINDOW' ] = '0'

###########
def LoadLib( dllNameStem, usePlatformInflection=True, searchIfNotFoundHere=True ):
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
	uninflectedStem = dllNameStem
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
	if not os.path.isfile( dllPath ) and searchIfNotFoundHere:
		found = ctypes.util.find_library( uninflectedStem )
		if not found and uninflectedStem.startswith( 'lib' ): found = ctypes.util.find_library( uninflectedStem[ 3: ] )
		if found: dllPath = found
	try: dll = ctypes.CDLL( dllPath )
	except Exception as err:
		msg = "file exists, but may be corrupt" if os.path.isfile( dllPath ) else "file is missing---perhaps it has not been compiled for your platform?"
		raise OSError( "%s\nfailed to load shared library %s\n%s" % ( err, os.path.basename( dllPath ), msg ) )
	return dll

av = dll = LoadLib( 'libavbin' )
###########

AVBIN_RESULT_ERROR = -1
AVBIN_RESULT_OK = 0
AVbinResult = ctypes.c_int

AVBIN_STREAM_TYPE_UNKNOWN = 0
AVBIN_STREAM_TYPE_VIDEO = 1
AVBIN_STREAM_TYPE_AUDIO = 2
AVbinStreamType = ctypes.c_int

AVBIN_SAMPLE_FORMAT_U8 = 0
AVBIN_SAMPLE_FORMAT_S16 = 1
AVBIN_SAMPLE_FORMAT_S24 = 2
AVBIN_SAMPLE_FORMAT_S32 = 3
AVBIN_SAMPLE_FORMAT_FLOAT = 4
AVbinSampleFormat = ctypes.c_int

AVBIN_LOG_QUIET = -8
AVBIN_LOG_PANIC = 0
AVBIN_LOG_FATAL = 8
AVBIN_LOG_ERROR = 16
AVBIN_LOG_WARNING = 24
AVBIN_LOG_INFO = 32
AVBIN_LOG_VERBOSE = 40
AVBIN_LOG_DEBUG = 48
AVbinLogLevel = ctypes.c_int

AVbinFileP = ctypes.c_void_p
AVbinStreamP = ctypes.c_void_p

Timestamp = ctypes.c_int64

class AVbinFileInfo(ctypes.Structure):
    _fields_ = [
        ('structure_size', ctypes.c_size_t),
        ('n_streams', ctypes.c_int),
        ('start_time', Timestamp),
        ('duration', Timestamp),
        ('title', ctypes.c_char * 512),
        ('author', ctypes.c_char * 512),
        ('copyright', ctypes.c_char * 512),
        ('comment', ctypes.c_char * 512),
        ('album', ctypes.c_char * 512),
        ('year', ctypes.c_int),
        ('track', ctypes.c_int),
        ('genre', ctypes.c_char * 32),
    ]

class _AVbinStreamInfoVideo8(ctypes.Structure):
    _fields_ = [
        ('width', ctypes.c_uint),
        ('height', ctypes.c_uint),
        ('sample_aspect_num', ctypes.c_uint),
        ('sample_aspect_den', ctypes.c_uint),
        ('frame_rate_num', ctypes.c_uint),
        ('frame_rate_den', ctypes.c_uint),
    ]

class _AVbinStreamInfoAudio8(ctypes.Structure):
    _fields_ = [
        ('sample_format', ctypes.c_int),
        ('sample_rate', ctypes.c_uint),
        ('sample_bits', ctypes.c_uint),
        ('channels', ctypes.c_uint),
    ]

class _AVbinStreamInfoUnion8(ctypes.Union):
    _fields_ = [
        ('video', _AVbinStreamInfoVideo8),
        ('audio', _AVbinStreamInfoAudio8),
    ]

class AVbinStreamInfo8(ctypes.Structure):
    _fields_ = [
        ('structure_size', ctypes.c_size_t),
        ('type', ctypes.c_int),
        ('u', _AVbinStreamInfoUnion8)
    ]

class AVbinPacket(ctypes.Structure):
    _fields_ = [
        ('structure_size', ctypes.c_size_t),
        ('timestamp', Timestamp),
        ('stream_index', ctypes.c_int),
        ('data', ctypes.POINTER(ctypes.c_uint8)),
        ('size', ctypes.c_size_t),
    ]

AVbinLogCallback = ctypes.CFUNCTYPE(None,
    ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p)

av.avbin_get_version.restype = ctypes.c_int
av.avbin_get_ffmpeg_revision.restype = ctypes.c_int
av.avbin_get_audio_buffer_size.restype = ctypes.c_size_t
av.avbin_have_feature.restype = ctypes.c_int
av.avbin_have_feature.argtypes = [ctypes.c_char_p]

av.avbin_init.restype = AVbinResult
av.avbin_set_log_level.restype = AVbinResult
av.avbin_set_log_level.argtypes = [AVbinLogLevel]
av.avbin_set_log_callback.argtypes = [AVbinLogCallback]

av.avbin_open_filename.restype = AVbinFileP
av.avbin_open_filename.argtypes = [ctypes.c_char_p]
av.avbin_close_file.argtypes = [AVbinFileP]
av.avbin_seek_file.argtypes = [AVbinFileP, Timestamp]
av.avbin_file_info.argtypes = [AVbinFileP, ctypes.POINTER(AVbinFileInfo)]
av.avbin_stream_info.argtypes = [AVbinFileP, ctypes.c_int,
                                 ctypes.POINTER(AVbinStreamInfo8)]

av.avbin_open_stream.restype = ctypes.c_void_p
av.avbin_open_stream.argtypes = [AVbinFileP, ctypes.c_int]
av.avbin_close_stream.argtypes = [AVbinStreamP]

av.avbin_read.argtypes = [AVbinFileP, ctypes.POINTER(AVbinPacket)]
av.avbin_read.restype = AVbinResult
av.avbin_decode_audio.restype = ctypes.c_int
av.avbin_decode_audio.argtypes = [AVbinStreamP, 
    ctypes.c_void_p, ctypes.c_size_t,
    ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)]
av.avbin_decode_video.restype = ctypes.c_int
av.avbin_decode_video.argtypes = [AVbinStreamP, 
    ctypes.c_void_p, ctypes.c_size_t,
    ctypes.c_void_p]


if True:
    # XXX lock all avbin calls.  not clear from ffmpeg documentation if this
    # is necessary.  leaving it on while debugging to rule out the possiblity
    # of a problem.
    def synchronize(func, lock):
        def f(*args):
            lock.acquire()
            result = func(*args)
            lock.release()
            return result
        return f 

    _avbin_lock = threading.Lock()
    for name in dir(av):
        if name.startswith('avbin_'):
            setattr(av, name, synchronize(getattr(av, name), _avbin_lock))

def get_version():
    return av.avbin_get_version()

class AVbinException(MediaFormatException):
    pass

def timestamp_from_avbin(timestamp):
    return float(timestamp) / 1000000

def timestamp_to_avbin(timestamp):
    return int(timestamp * 1000000)

class VideoPacket(object):
    _next_id = 0

    def __init__(self, packet):
        self.timestamp = timestamp_from_avbin(packet.timestamp)
        self.data = (ctypes.c_uint8 * packet.size)()
        self.size = packet.size
        ctypes.memmove(self.data, packet.data, self.size)

        # Decoded image.  0 == not decoded yet; None == Error or discarded
        self.image = 0

        self.id = self._next_id
        self.__class__._next_id += 1

class AVbinSource(StreamingSource):
    def __init__(self, filename, file=None, stream_types='av'): # jez introduced stream_types to allow the caller to avoid corrupt unnecessary streams that can crash avbin 
        if file is not None:
            raise NotImplementedError('Loading from file stream is not supported')

        self._file = av.avbin_open_filename(asbytes_filename(filename))
        if not self._file:
            raise AVbinException('Could not open "%s"' % filename)

        self._video_stream = None
        self._video_stream_index = -1
        self._audio_stream = None
        self._audio_stream_index = -1

        file_info = AVbinFileInfo()
        file_info.structure_size = ctypes.sizeof(file_info)
        av.avbin_file_info(self._file, ctypes.byref(file_info))
        self._duration = timestamp_from_avbin(file_info.duration)

        self.info = SourceInfo()
        self.info.title = file_info.title
        self.info.author = file_info.author
        self.info.copyright = file_info.copyright
        self.info.comment = file_info.comment
        self.info.album = file_info.album
        self.info.year = file_info.year
        self.info.track = file_info.track
        self.info.genre = file_info.genre

        # Pick the first video and audio streams found, ignore others.
        for i in range(file_info.n_streams):
            info = AVbinStreamInfo8()
            info.structure_size = ctypes.sizeof(info)
            av.avbin_stream_info(self._file, i, info)

            if (info.type == AVBIN_STREAM_TYPE_VIDEO and 
                not self._video_stream):

                if 'v' not in stream_types.lower(): continue
                stream = av.avbin_open_stream(self._file, i)
                if not stream:
                    continue

                self.video_format = VideoFormat(
                    width=info.u.video.width,
                    height=info.u.video.height)
                if info.u.video.sample_aspect_num != 0:
                    self.video_format.sample_aspect = (
                        float(info.u.video.sample_aspect_num) /
                            info.u.video.sample_aspect_den)
                if _have_frame_rate:
                    self.video_format.frame_rate = (
                        float(info.u.video.frame_rate_num) / 
                            info.u.video.frame_rate_den)
                self._video_stream = stream
                self._video_stream_index = i
                if 'a' not in stream_types.lower(): break

            elif (info.type == AVBIN_STREAM_TYPE_AUDIO and
                  info.u.audio.sample_bits in (8, 16) and
                  info.u.audio.channels in (1, 2) and 
                  not self._audio_stream):

                if 'a' not in stream_types.lower(): continue
                stream = av.avbin_open_stream(self._file, i)
                if not stream:
                    continue

                self.audio_format = AudioFormat(
                    channels=info.u.audio.channels,
                    sample_size=info.u.audio.sample_bits,
                    sample_rate=info.u.audio.sample_rate)
                self._audio_stream = stream
                self._audio_stream_index = i
                if 'v' not in stream_types.lower(): break

        self._packet = AVbinPacket()
        self._packet.structure_size = ctypes.sizeof(self._packet)
        self._packet.stream_index = -1

        self._events = []

        # Timestamp of last video packet added to decoder queue.
        self._video_timestamp = 0
        self._buffered_audio_data = []
        self._decode_thread = None
        self._video_packets = []

        if self.audio_format:
            self._audio_buffer = \
                (ctypes.c_uint8 * av.avbin_get_audio_buffer_size())()
            
        if self.video_format:
        #    if not hasattr( self, 'WorkerThread' ):
        #    	AvoidPygletImportSideEffects( 'WorkerThread' )
        #    	from pyglet.media.threads import WorkerThread
        #    	self.WorkerThread = WorkerThread
        #    WorkerThread = self.WorkerThread
            self._decode_thread = WorkerThread()
            self._decode_thread.start()
            self._condition = threading.Condition()

    def __del__(self):
        if _debug:
            print('del avbin source')
        try:
            if self._video_stream:
                av.avbin_close_stream(self._video_stream)
            if self._audio_stream:
                av.avbin_close_stream(self._audio_stream)
            av.avbin_close_file(self._file)
        except:
            pass

    def delete(self):
        if self._decode_thread:
            self._decode_thread.stop()

    def seek(self, timestamp):
        if _debug:
            print('AVbin seek', timestamp)
        av.avbin_seek_file(self._file, timestamp_to_avbin(timestamp))

        self._audio_packet_size = 0
        del self._events[:]
        del self._buffered_audio_data[:]

        if self.video_format:
            self._video_timestamp = 0
            if self._decode_thread: self._condition.acquire()
            for packet in self._video_packets:
                packet.image = None
            if self._decode_thread: 
                self._condition.notify()
                self._condition.release()
            del self._video_packets[:]

            if self._decode_thread: self._decode_thread.clear_jobs()

    def _get_packet(self):
        # Read a packet into self._packet.  Returns True if OK, False if no
        # more packets are in stream.
        return av.avbin_read(self._file, self._packet) == AVBIN_RESULT_OK

    def _process_packet(self):
        # Returns (packet_type, packet), where packet_type = 'video' or
        # 'audio'; and packet is VideoPacket or AudioData.  In either case,
        # packet is buffered or queued for decoding; no further action is
        # necessary.  Returns (None, None) if packet was neither type.

        if self._packet.stream_index == self._video_stream_index:
            if self._packet.timestamp < 0:
                # XXX TODO
                # AVbin needs hack to decode timestamp for B frames in
                # some containers (OGG?).  See
                # http://www.dranger.com/ffmpeg/tutorial05.html
                # For now we just drop these frames.
                return None, None

            video_packet = VideoPacket(self._packet)

            if _debug:
                print('Created and queued frame %d (%f)' % \
                    (video_packet.id, video_packet.timestamp))

            self._video_timestamp = max(self._video_timestamp,
                                        video_packet.timestamp)
            self._video_packets.append(video_packet)
            if self._decode_thread: self._decode_thread.put_job( lambda: self._decode_video_packet(video_packet) )
            else: self._decode_video_packet(video_packet)

            return 'video', video_packet

        elif self._packet.stream_index == self._audio_stream_index:
            audio_data = self._decode_audio_packet()
            if audio_data:
                if _debug:
                    print('Got an audio packet at', audio_data.timestamp)
                self._buffered_audio_data.append(audio_data)
                return 'audio', audio_data

        return None, None

    def get_audio_data(self, bytes):
        try:
            audio_data = self._buffered_audio_data.pop(0)
            audio_data_timeend = audio_data.timestamp + audio_data.duration
        except IndexError:
            audio_data = None
            audio_data_timeend = self._video_timestamp + 1

        if _debug:
            print('get_audio_data')

        have_video_work = False

        # Keep reading packets until we have an audio packet and all the
        # associated video packets have been enqueued on the decoder thread.
        while not audio_data or (
            self._video_stream and self._video_timestamp < audio_data_timeend):
            if not self._get_packet():
                break

            packet_type, packet = self._process_packet()

            if packet_type == 'video':
                have_video_work = True
            elif not audio_data and packet_type == 'audio':
                audio_data = self._buffered_audio_data.pop(0)
                if _debug:
                    print('Got requested audio packet at', audio_data.timestamp)
                audio_data_timeend = audio_data.timestamp + audio_data.duration

        if have_video_work:
            # Give decoder thread a chance to run before we return this audio
            # data.
            time.sleep(0)

        if not audio_data:
            if _debug:
                print('get_audio_data returning None')
            return None

        while self._events and self._events[0].timestamp <= audio_data_timeend:
            event = self._events.pop(0)
            if event.timestamp >= audio_data.timestamp:
                event.timestamp -= audio_data.timestamp
                audio_data.events.append(event)

        if _debug:
            print('get_audio_data returning ts %f with events' % \
                audio_data.timestamp, audio_data.events)
            print('remaining events are', self._events)
        return audio_data

    def _decode_audio_packet(self):
        packet = self._packet
        size_out = ctypes.c_int(len(self._audio_buffer))

        while True:
            audio_packet_ptr = ctypes.cast(packet.data, ctypes.c_void_p)
            audio_packet_size = packet.size

            used = av.avbin_decode_audio(self._audio_stream,
                audio_packet_ptr, audio_packet_size,
                self._audio_buffer, size_out)

            if used < 0:
                self._audio_packet_size = 0
                break

            audio_packet_ptr.value += used
            audio_packet_size -= used

            if size_out.value <= 0:
                continue

            # XXX how did this ever work?  replaced with copy below
            # buffer = ctypes.string_at(self._audio_buffer, size_out)

            # XXX to actually copy the data.. but it never used to crash, so
            # maybe I'm  missing something
            buffer = ctypes.create_string_buffer(size_out.value)
            ctypes.memmove(buffer, self._audio_buffer, len(buffer))
            buffer = buffer.raw

            duration = float(len(buffer)) / self.audio_format.bytes_per_second
            self._audio_packet_timestamp = \
                timestamp = timestamp_from_avbin(packet.timestamp)
            return AudioData(buffer, len(buffer), timestamp, duration, []) 

    def _decode_video_packet(self, packet):
        width = self.video_format.width
        height = self.video_format.height
        pitch = width * 3
        buffer = (ctypes.c_uint8 * (pitch * height))()
        result = av.avbin_decode_video(self._video_stream, 
                                       packet.data, packet.size, 
                                       buffer)
        if result < 0:
            image_data = None
        else:
            #if not hasattr( self, 'ImageData' ):
            #    AvoidPygletImportSideEffects( 'ImageData' )
            #    from pyglet.image import ImageData
            #    self.ImageData = ImageData
            #image_data = self.ImageData(width, height, 'RGB', buffer, pitch)
            image_data = ImageData(width, height, 'RGB', buffer, pitch)
            
        packet.image = image_data

        # Notify get_next_video_frame() that another one is ready.
        if self._decode_thread:
            self._condition.acquire()
            self._condition.notify()
            self._condition.release()

    def _ensure_video_packets(self):
        """Process packets until a video packet has been queued (and begun
        decoding).  Return False if EOS.
        """
        if not self._video_packets:
            if _debug:
                print('No video packets...')
            # Read ahead until we have another video packet
            while True:
                if not self._get_packet(): return False
                packet_type, _ = self._process_packet()
                if not packet_type: return False
                if packet_type == 'video': break
            if _debug:
                print('Queued packet', _)
        return True

    def get_next_video_timestamp(self):
        if not self.video_format:
            return

        if self._ensure_video_packets():
            if _debug:
                print('Next video timestamp is', self._video_packets[0].timestamp)
            return self._video_packets[0].timestamp

    def get_next_video_frame(self):
        if not self.video_format:
            return

        if self._ensure_video_packets():
            packet = self._video_packets.pop(0)
            if self._decode_thread:
                if _debug:
                    print('Waiting for', packet)
    
                # Block until decoding is complete
                self._condition.acquire()
                while packet.image == 0:
                    self._condition.wait()
                self._condition.release()
    
                if _debug:
                    print('Returning', packet)
            return packet.image

av.avbin_init()
if _debug: av.avbin_set_log_level(AVBIN_LOG_DEBUG)
else:      av.avbin_set_log_level(AVBIN_LOG_QUIET)
_have_frame_rate = av.avbin_have_feature(asbytes('frame_rate'))
