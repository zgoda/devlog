# Devlog

![Tests](https://github.com/zgoda/devlog/workflows/Tests/badge.svg?branch=master) [![CodeFactor](https://www.codefactor.io/repository/github/zgoda/devlog/badge)](https://www.codefactor.io/repository/github/zgoda/devlog) [![Coverage Status](https://coveralls.io/repos/github/zgoda/devlog/badge.svg?branch=master)](https://coveralls.io/github/zgoda/devlog?branch=master)

My dev log and other logs.

A very simple blogging engine that I often use to test some ideas wrt web programming (and general programming) in Python.

## Development

### Grab the source

```console
git clone https://github.com/zgoda/devlog.git
```

### Set up local Python runtime

Python 3.8 or newer is required. In Ubuntu 22.04 default is Python 3.10 so you should be good to go. It's best to update installation tools upfront.

```console
/usr/bin/python3 -m venv venv
source venv/bin/activate
pip install -U pip setuptools
```

With activated virtualenv you now may install Devlog in dev mode.

```console
pip install -U -e .[dev]
```

Now copy `.env.example` to `.env` and modify it to suit your environment. Some JS tools are required so run `npm i`. I tested it with Node 18 but it may work with older versions. This will install `cleancss-cli` tool, you will need an implementation of SASS too. Either download `dart-sass` and put it in `PATH` (eg `~/.local/bin` on Ubuntu) or install JS version with `npm i -D sass`.

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
