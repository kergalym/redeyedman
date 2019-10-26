#! /usr/bin/python2.7

import sys

activate_this = '/var/www/redeyedman-flask.ru/htdocs/redeyedman-flask.ru/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

sys.path.insert(0, '/var/www/redeyedman-flask.ru/htdocs/redeyedman-flask.ru/')

from application import app as application
