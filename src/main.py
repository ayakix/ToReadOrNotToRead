#!-*- coding:utf-8 -*-
from google.appengine.ext.webapp.util import run_wsgi_app

import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api import *
from web import *

application = webapp.WSGIApplication(
    [
    ('/', Top),
    ('/dl', Download),
    ],
    debug=True)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

