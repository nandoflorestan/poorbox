poorbox
=======

*Poor man's dropbox -- Recursively downloads a dropbox directory
using the REST API.*

This is especially useful for the Raspberry Pi or any other
ARM-based system, since Dropbox does not provide an ARM version
of their official client. This might also be a simple alternative
to the complicated Dropbox setup on a server without X installed.

Good news: this downloads only the files that have been modified.

Bad news: this is considerably slower than the "real" Dropbox software,
due to 2 reasons:

1. No optimization has been done: files are downloaded sequentially.

2. The Dropbox REST API only deals with entire files, not file-deltas.

We don't upload changes yet, so sync is one-way only.
Maybe in the future!

When you run the app for the first time and authorize in your browser,
Dropbox will create an "Apps/poorbox" directory which poorbox can see.
You can put files and folders there and poorbox will be able to
download them. This is because this app currently has
"app_folder" access, not entire dropbox access.

Requirements
------------

- Python 2.7 or 3.x
- An ability to install Python packages

Installation
------------

With one command you can install poorbox and its (few) dependencies.
This is achieved through the famous *pypi (Python Package Index)*,
which hosts poorbox downloads here:

http://pypi.python.org/pypi/poorbox

The command is:

    easy_install -UZ poorbox

If you don't like *distribute* you can use *pip* and the result is the same:

    pip install poorbox

You also need an app key
------------------------

This software is in the process of getting approved by Dropbox. Meanwhile,
to use it, you need your own *app key* and *app secret*. Please register
with Dropbox to obtain a key:

https://www.dropbox.com/developers/apps

Usage
-----

The installation procedure above puts in your path the ``poorbox`` command.
There is no other difference between invoking ``poorbox`` or ``poorbox.py``.

poorbox has a few command-line arguments. Use the ``--help`` switch to view them:

    poorbox -h

On the first run, poorbox will print a URL and pause. Click the URL to
open your web browser. There you will authenticate against Dropbox and
authorize poorbox to download your files for you. When done, go back to
your console and press Enter. poorbox will proceed to download your files.

On subsequent runs you don't need to authenticate anymore -- poorbox
downloads immediately. This is because poorbox stores its credentials
in a cache -- a simple text file. There is a switch for you to control the
location of this cache.

Configuration files aren't supported yet; in the meantime, I suggest you
just create a little script to run poorbox with the necessary switches.

Bugs? Feature requests? Pull requests?
--------------------------------------

This project is hosted at https://github.com/nandoflorestan/poorbox

You are welcome to our issue tracker:

https://github.com/nandoflorestan/poorbox/issues
