pyRemoteControl
===============

pyRemoteControl is a remote control server for interacting with your X11 session. It was developed to support the [Remote Control for Linux](https://play.google.com/store/apps/details?id=net.rbaron.remotecontrol) android app, but it can be used by any application that can communicate via TCP sockets.

Installation and usage
----------------------

Download the zip file, extract it and run the `pyRemoteControl.py` python script. It should be waiting for a connection.

If you would like to automate this process, copy and paste the following lines on a terminal:

```bash
$  wget https://github.com/raaapha/pyRemoteControl/archive/master.zip && \
   unzip master.zip && \
   cd pyRemoteControl-master && \
   chmod +x pyRemoteControl.py
```

You can now run the python script with:

```bash
$  ./pyRemoteControl.py
```

If everything went fine, you should see something like this:

```bash
$ ./pyRemoteControl.py
   Xlib.protocol.request.QueryExtension
   pyRemoteControl version v1.0
   Waiting for connection...
```

Make sure you have python2 installed and available under `python2`.

Contribute
----------

Please feel free to send in suggestions and pull requests!

License
-------

GPLv2. The python [Xlib](http://python-xlib.sourceforge.net/) is also distributed under GPLv2.
