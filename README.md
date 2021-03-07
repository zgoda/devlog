# Devlog

![Tests](https://github.com/zgoda/devlog/workflows/Tests/badge.svg?branch=master) [![CodeFactor](https://www.codefactor.io/repository/github/zgoda/devlog/badge)](https://www.codefactor.io/repository/github/zgoda/devlog) [![Coverage Status](https://coveralls.io/repos/github/zgoda/devlog/badge.svg?branch=master)](https://coveralls.io/github/zgoda/devlog?branch=master)

My dev log and other logs.

A very simple blogging engine that I often use to test some ideas wrt web programming (and general programming) in Python.

## Microblog client development

This is a bit of crossover but I imagine the only reason to run Devlog is to see how the microblog client application works, so here are basic instructions on how to get Devlog running in dev mode. Devlog is tested on Linux only so I don't know if it works in any other OS.

### Grab the source

```console
git clone https://github.com/zgoda/devlog.git
```

### Set up local Python runtime

Python 3.7 or newer is required. In Ubuntu 20.04 default is Python 3.8 so you should be good to go. It's best to update installation tools upfront.

```console
/usr/bin/python3.8 -m venv venv
source venv/bin/activate
pip install -U pip setuptools
```

With activated virtualenv you now may install Devlog in dev mode.

```console
pip install -U -e .[dev]
```

Once installed Devlog provides CLI for basic management. 1st thing is to initialise database.

```console
devlog db init
```

For testing this program you'd also need to register user account.

```console
devlog user create myusername
```

Now you may launch your local instance. By default it listens on port 5000 and it's bound only to 127.0.0.1. This is fine if you want to access it only from emulator running on the same machine (use 10.0.2.2:5000 as host name), otherwise you may specify host and port using `-h` and `-p` parameters.

```console
devlog run
```

There's a lot of command line options, consult `--help` to learn more.
