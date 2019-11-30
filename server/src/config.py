"""
    config.py
    - settings for the flask application object
"""

class BaseConfig(object):
    DEBUG = True
    SECRET_KEY = r'_5#y2L"F4Q8z\n\xec]/'
    CORS_HEADERS = 'Content-Type'
    DATABASE = 'server/data/data.db'
