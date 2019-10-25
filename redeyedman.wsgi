#! /usr/bin/python2.7

import logging
import sys

from cffi.setuptools_ext import execfile

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/redeyedman-flask.ru/htdocs/redeyedman-flask.ru/')

activate_this = '/var/www/redeyedman-flask.ru/htdocs/redeyedman-flask.ru/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
