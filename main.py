# Подключение библиотек для работы с Flask и Blueprint
from flask import Flask, jsonify, Blueprint

# Подключение библиотеки для создания автоматической документации API
from flasgger import Swagger, swag_from

from config import DevelopmentConfig
# Подключение части нашего веб-сервиса с использованием Blueprint
from sitepart.sitepart import sitepart

# Приложение Flask
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Инициализация для нашего API сервиса документации Swagger
swagger = Swagger(app)

# Создаем основной Blueprint сайта
main = Blueprint("/", __name__, template_folder='templates',static_folder='static')

# объявляем декоратор для метода http get
# Информация, которая будет выдаваться по URL/info/something
# Параметр в <> при вводе URL будет передан в переменную about функции info
@main.route('/info/<about>/')
@swag_from('about.yml')
def info(about):
    all_info = {
        'all': 'ЛяшенкоА.Н. 1.0 2025',
        'version': '1.0',
        'author': 'ЛяшенкоА.Н.',
        'year': '2025'
    }
    result = {about:all_info[about]}
    return jsonify(result)

# Регистрируем основной Blueprint и Blueprint другой части сайта
app.register_blueprint(main,url_prefix='/')

# url_prefix указывает URL в контексте которого будет доступна часть данного Blueprint
app.register_blueprint(sitepart,url_prefix='/sitepart')
