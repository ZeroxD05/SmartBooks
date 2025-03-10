import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-for-smartbooks'
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False