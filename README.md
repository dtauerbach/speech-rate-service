# speech-rate-service
A web service that wraps speech identification and measurement tools

## Getting Started

This is a web app and api written in flask that wraps some academic software, notably Praat.

## Setting up Dev Environment

The first step is to install pip, virtualenv at the system level. (Note: instructions below were tested with Ubuntu 14.10, but the set up may be different on different platforms).

    $ sudo apt-get install python-pip 
    $ sudo pip install virtualenv

This may be helpful but not necessary:

    $ sudo pip install virtualenvwrapper

You also need to install some esoteric academic software called Praat, which underlies a lot of the computational analysis of the audio:

    # sudo apt-get install praat

And some audio processing packages...

    # sudo apt-get install libav-tools

Next, start a virtualenv instance to install the project specific dependencies.

    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt