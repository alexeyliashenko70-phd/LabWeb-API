import os

class Config:
    # токен для защиты от CSRF-атаки
    SECRET_KEY = os.urandom(32).hex()
    # ключи для работы с капчей
    RECAPTCHA_USE_SSL = False
    RECAPTCHA_PUBLIC_KEY = "6Lec0iQsAAAAAHv2wVmouGDxOysFMZK3MsTzfJwd"
    RECAPTCHA_PRIVATE_KEY = "6Lec0iQsAAAAAONAPzuDygkZ8OUx7kvVHnjWImKn"
    # константы для работы с сесиями и куками
    SESSION_REFRESH_EACH_REQUEST = False
    SESSION_TYPE = "filesystem"

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    DEBUG = False
    TESTING = True
