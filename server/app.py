#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]

    response = make_response(bakeries, 200)
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    
    bakery = bakery.to_dict() if bakery else {"error": "Bakery not found"}
    response = make_response(bakery, 200)
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    # in descending order
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()

    response = make_response([bg.to_dict() for bg in baked_goods], 200)
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()

    if baked_good:
        response = make_response(baked_good.to_dict(), 200)
        return response
    return make_response({"error": "Baked good not found"}, 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
