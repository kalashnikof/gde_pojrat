from flask import Flask, jsonify, request, render_template
import random

endpoint_place = '/place'
endpoint_category = 'category'

cat_burgers = 'Бургеры'
cat_pizza = 'Пицца'
cat_ramen = 'Рамен'
cat_asia = 'Азиатская кухня'
cat_pancaces = 'Блины'
cat_shawerma = 'Шаверма'
cat_dumplings = 'Пельмени'
cat_cake = 'Десерты'
cat_sushi = 'Суши'
cat_beer = 'Пиво'

places = [
    {'name': 'Catch-up Burgers', 'address': 'ул. Льва Толстого, 1', 'categories': [cat_burgers, cat_beer], },
    {'name': 'Mashita', 'address': 'Каменноостровский пр., 38/96', 'categories': [cat_asia, cat_ramen], },
    {'name': 'Forno Bravo', 'address': 'ул. Льва Толстого, 1', 'categories': [cat_pizza, cat_beer], },
    {'name': 'Green Box', 'address': 'ул. Льва Толстого, 4', 'categories': [], },
    {'name': 'Теремок', 'address': 'ул. Льва Толстого, 1-3, лит. А', 'categories': [cat_pancaces], },
    {'name': 'Буше', 'address': 'ул. Льва Толстого, 1-3', 'categories': [cat_cake], },
    {'name': 'Burger king', 'address': 'Каменноостровский пр., 40', 'categories': [cat_burgers], },
    {'name': 'MacDonalds', 'address': 'Каменноостровский пр-кт, 39', 'categories': [cat_burgers], },
    {'name': 'KFC', 'address': 'Каменноостровский пр., 37, лит. Д', 'categories': [cat_burgers], },
    {'name': 'Pizza Hut', 'address': 'Каменноостровский пр., 37', 'categories': [cat_pizza], },
    {'name': 'Balkan gourmet', 'address': 'Большая Монетная ул., 14а', 'categories': [], },
    {'name': 'Ленинградская столовая', 'address': 'Петропавловская ул., 4', 'categories': [], },
    {'name': 'Пельменная', 'address': 'набережная Реки Карповки, 7 лит. А', 'categories': [cat_dumplings], },
    {'name': 'Sushi Wok', 'address': 'Большой проспект ПС, 94', 'categories': [cat_sushi], },
    {'name': 'Arij shawarma', 'address': 'Большая Пушкарская ул., 45', 'categories': [cat_beer, cat_shawerma], },
]

app = Flask(__name__)


@app.route('/')
def home():
    pojrat_place = random.choice(places)
    return render_template('index.html', pojrat_place=pojrat_place)


# POST /place data: {name:, address:, categories:}
# create place
@app.route(endpoint_place,
           methods=['POST'])
def create_place():
    request_data = request.get_json()
    new_place = {
        'name': request_data['name'],
        'address': request_data['address'],
        'categories': request_data['categories'],
    }
    places.append(new_place)
    return jsonify(new_place), 201


# GET /place/<string:name>
# get place by name
@app.route(f'{endpoint_place}/<string:name>',
           methods=['GET'])  # 'http://127.0.0.1:5000/place/place_name'
def get_place(name):
    result = jsonify({'message': 'Place not found.'}), 404
    for place in places:
        if place['name'] == name:
            result = jsonify(place), 200
            break
    return result


# GET /place
# get places
@app.route(endpoint_place,
           methods=['GET'])
def get_places():
    return jsonify({'places': places}), 200


# POST /place/<string:name>/category {name:, address:, categories:}
# create place category
@app.route(f'{endpoint_place}/<string:name>/{endpoint_category}',
           methods=['POST'])
def create_category_in_place(name):
    result = jsonify({'message': 'Place not found.'}), 404
    request_data = request.get_json()
    for place in places:
        if place['name'] == name:
            place['categories'].append(request_data['category'])
            place['categories'] = list(set(place['categories']))
            result = jsonify(place['categories']), 201
            break
    return result


# GET /place/<string:name>/category
# get place categories
@app.route(f'{endpoint_place}/<string:name>/{endpoint_category}',
           methods=['GET'])  # 'http://127.0.0.1:5000/place/place_name'
def get_categories_in_place(name):
    result = jsonify({'message': 'Place not found.'}), 404
    for place in places:
        if place['name'] == name:
            result = jsonify({'categories': place['categories']}), 200
            break
    return result


# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
