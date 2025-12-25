from http import HTTPStatus

from flask import Blueprint, jsonify, request
from flasgger import swag_from

# Создаем Blueprint для отдельной части веб API
sitepart = Blueprint("sitepart", __name__, template_folder='templates',static_folder='static')

# Создаем хранилище
DATA = [
    {'id': 1,
     'country': 'Russia',
     'language': 'russia',
     'speakers': 150000000,
     'letters': 32,
     'words': 200000},
    {'id': 2,
     'country': 'Russia',
     'language': 'tatar',
     'speakers': 4000000,
     'letters': 39,
     'words': 100000},
    {'id': 3,
     'country': 'France',
     'language': 'french',
     'speakers': 67000000,
     'letters': 26,
     'words': 135000},
    {'id': 4,
     'country': 'England',
     'language': 'english',
     'speakers': 70000000,
     'letters': 26,
     'words': 600000},
    {'id': 5,
     'country': 'China',
     'language': 'chinese',
     'speakers': 1400000000,
     'letters': 100000,
     'words': 370000},
    {'id': 6,
     'country': 'Papua New Guinea',
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

# Возвращает запись по id
@sitepart.route('/get/<int:id>/', methods=['GET'])
@swag_from('getid.yml')
def getid(id: int):
    return jsonify([rect for rect in DATA if rect['id'] == id])

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
@sitepart.route('/add', methods=['POST'])
@swag_from('add.yml')
def add():
    args = request.args

    country = args.get('country')
    if not country: return jsonify({'error': 'country not found.'}), HTTPStatus.NOT_FOUND

    language = args.get('language')
    if not language: return jsonify({'error': 'language not found.'}), HTTPStatus.NOT_FOUND

    speakers = args.get('speakers')
    if not speakers: return jsonify({'error': 'speakers not found.'}), HTTPStatus.NOT_FOUND
    if int(speakers) < 0: return jsonify({'error': 'speakers is negative.'}), HTTPStatus.NOT_FOUND

    letters = args.get('letters')
    if not letters: return jsonify({'error': 'letters not found.'}), HTTPStatus.NOT_FOUND
    if int(letters) <= 0: return jsonify({'error': 'letters is negative.'}), HTTPStatus.NOT_FOUND

    words = args.get('words')
    if not words: return jsonify({'error': 'words not found.'}), HTTPStatus.NOT_FOUND
    if int(words) <= 0: return jsonify({'error': 'words is negative.'}), HTTPStatus.NOT_FOUND

    rect = {'id': int(DATA[len(DATA) - 1].get('id'))+1,
            'country': country,
            'language': language,
            'speakers': int(speakers),
            'letters': int(letters),
            'words': int(words)}

    DATA.append(rect)

    return jsonify(DATA[len(DATA)-1]), HTTPStatus.OK

# # Обновляем запись
# @sitepart.route('/change/<int:id>/', methods=['PUT'])
# @swag_from('change.yml')
# def change(id: int):
#
#     rec = [rect for rect in DATA if rect['id'] == id]
#     if len(rec) < 1:
#         return jsonify({'error': 'no such record.'}), HTTPStatus.NOT_FOUND
#
#     args = request.args
#
#     country = args.get('country')
#     if country is not None:
#         rec[0]['country'] = country
#
#     language = args.get('language')
#     if language is not None:
#         rec[0]['language'] = language
#
#     speakers = args.get('speakers')
#     if speakers is not None:
#         if 0 <= int(speakers):
#             rec[0]['speakers'] = int(speakers)
#
#     letters = args.get('letters')
#     if letters is not None:
#         if 0 < int(letters):
#             rec[0]['letters'] = int(letters)
#
#     words = args.get('words')
#     if words is not None:
#         if 0 < int(words):
#             rec[0]['words'] = int(words)
#
#     return jsonify(rec), HTTPStatus.OK

# # Удаляем записи
# @sitepart.route('/delete/<int:id>', methods=['DELETE'])
# @swag_from('delete.yml')
# def delete(id: int):
#
#     rec = [rect for rect in DATA if rect['id'] == id]
#     if len(rec) < 1:
#         return jsonify({'error': 'no such record.'}), HTTPStatus.NOT_FOUND
#
#     DATA.remove(rec[0])
#
#     return jsonify(DATA), HTTPStatus.OK

# Сортировка записей по полю в сторону увеличения значений
@sitepart.route('/sortIncrease/<field>/', methods=['GET'])
@swag_from('sort.yml')
def sortInc(field: str):
    DATA.sort(key=lambda x: x[field])
    return jsonify(DATA), HTTPStatus.OK

# Сортировка записей по полю в сторону уменьшения значений
@sitepart.route('/sortDecrease/<field>/', methods=['GET'])
@swag_from('sort.yml')
def sortDec(field: str):
    DATA.sort(key=lambda x: x[field], reverse=True)
    return jsonify(DATA), HTTPStatus.OK
