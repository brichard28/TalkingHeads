audiomath's default back-end for recording and playing sounds is the third-party
library PortAudio, by Ross Bencina and Phil Burk. The Python files in this directory
were created specifically for audiomath and are released under the same license
(GPL) as the rest of audiomath, but the binaries (dynamic libraries) in this
directory are builds from unaltered third-party code, released under the PortAudio
license (see below). Builds for various platforms are included here in this directory,
so that you probably will not need to install PortAudio separately.

The libraries here were built from sources available at
http://www.portaudio.com/archives/pa_stable_v190600_20161030.tgz
via http://www.portaudio.com/download.html

On Linux (Ubuntu 18.04 LTS), ALSA was installed first::
	
	sudo apt install libasound-dev

Then the standard combo worked::
	
	./configure
	make

producing the dynamic library inside `lib/.libs/`

On macOS (10.13, High Sierra, 2017) the `--disable-mac-universal` was necessary::

	./configure --disable-mac-universal
	make

...in order to work around two errors from `./configure`::

	xcode-select: error: tool 'xcodebuild' requires Xcode, but active developer directory '/Library/Developer/CommandLineTools' is a command line tools instance
	configure: error: Could not find 10.5 to 10.12 SDK.

(The first one *could* presumably have been worked-around by biting the bullet and
installing full-blown XCode, and the second has other suggested workarounds at
https://github.com/VCVRack/Rack/issues/144 .)  As with Linux, the library appeared
inside `lib/.libs/`

For Windows, the procedure is documented at:

- http://portaudio.com/docs/v19-doxydocs/compile_windows.html
- http://portaudio.com/docs/v19-doxydocs/compile_windows_asio_msvc.html

(TODO: don't remember whether or not that worked out-of-the-box for me).


PortAudio Credits and License
=============================

Here is the PortAudio license V19 as retrieved on 20190801 from 
http://www.portaudio.com/license.html

PortAudio Portable Real-Time Audio Library
Copyright (c) 1999-2011 Ross Bencina and Phil Burk

Permission is hereby granted, free of charge, to any person obtaining a copy of this 
software and associated documentation files (the "Software"), to deal in the 
Software without restriction, including without limitation the rights to use, copy, 
modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
and to permit persons to whom the Software is furnished to do so, subject to the 
following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
PARTICULAR PURPOSE AND NONINFRINGEMENT.

IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES 
OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.
