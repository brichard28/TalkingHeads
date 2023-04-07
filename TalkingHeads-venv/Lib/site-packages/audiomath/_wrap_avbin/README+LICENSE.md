audiomath's default solution for reading compressed sound formats is the third-party
library AVbin, created by Alex Holkner and others, based on Libav. The Python code
in this directory was adapted from `pyglet.media.sources.avbin` in the pyglet project
(see the extended license and credits information in the file).

AVbin binaries (dynamic libraries) are included in this directory so that you do not
have to perform a separate system-wide installation.  They come straight from the AVbin
version 10 installers downloaded on 20190801 via https://avbin.github.io/AVbin/Download.html
They are released under the Lesser GNU Public License (LGPL).  The source code, full
credits and licensing details are available at https://github.com/AVbin/AVbin and
https://github.com/AVbin/libav