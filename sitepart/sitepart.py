from http import HTTPStatus

from flask import Blueprint,jsonify
from flasgger import swag_from

# Создаем Blueprint для отдельной части веб API
sitepart = Blueprint("sitepart", __name__, template_folder='templates',static_folder='static')

# Создаем хранилище
DATA = [
    {'country': 'Russia',
     'language': 'russia',
     'speakers': 150000000,
     'letters': 32,
     'words': 200000},
    {'country': 'Russia',
     'language': 'tatar',
     'speakers': 4000000,
     'letters': 39,
     'words': 100000},
    {'country': 'France',
     'language': 'french',
     'speakers': 67000000,
     'letters': 26,
     'words': 135000},
    {'country': 'England',
     'language': 'english',
     'speakers': 70000000,
     'letters': 26,
     'words': 600000},
    {'country': 'China',
     'language': 'chinese',
     'speakers': 1400000000,
     'letters': 100000,
     'words': 370000},
    {'country': 'Papua New Guinea',
     'language': 'rotokas',
     'speakers': 4320,
     'letters': 12,
     'words': 5000}
]

# Возвращает полный список данных
@sitepart.route('/get', methods=['GET'])
@swag_from('get.yml')
def get():
    return jsonify(DATA), HTTPStatus.OK

# # Возвращает запись по id
# @sitepart.route('/get/<int:id>/', methods=['GET'])
# @swag_from('getid.yml')
# def getid(id: int):
#     return jsonify([rect for rect in DATA if rect['id'] == id])

# Среднее значение по полю
@sitepart.route('/average/<field>/', methods=['GET'])
@swag_from('average.yml')
def average(field: str):
    arr = list(map(lambda r: r[field], DATA))
    return jsonify(sum(arr) / len(arr)), HTTPStatus.OK

# Запись с минимальным значением по полю
@sitepart.route('/min/<field>/', methods=['GET'])
@swag_from('minmax.yml')
def minimum(field: str):
    arr = list(map(lambda r: r[field], DATA))
    idMin = arr.index(min(arr))
    return jsonify(DATA[idMin]), HTTPStatus.OK

# Запись с максимальным значением по полю
@sitepart.route('/max/<field>/', methods=['GET'])
@swag_from('minmax.yml')
def maximum(field: str):
    arr = list(map(lambda r: r[field], DATA))
    idMin = arr.index(max(arr))
    return jsonify(DATA[idMin]), HTTPStatus.OK

# Добавляем запись
@sitepart.route('/add?<record>', methods=['POST'])
@swag_from('add.yml')
@swag_from('add.yml')
def add(country: str, language: str, speakers: int, letters: int, words: int):
    rect = {'country': country,
            'language': language,
            'speakers': speakers,
            'letters': letters,
            'words': words}

    DATA.append(rect)

    return jsonify(DATA[len(DATA)])
