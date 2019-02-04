from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    # filtra o json
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field can't be left blank")

    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store ID")


    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "The item '{}' already exists".format(name)}, 400

        post_data = self.parser.parse_args()

        # item = ItemModel(name, post_data['price'], post_data['store_id'])
        item = ItemModel(name, **post_data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item"}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

        return {"message": "Have no more itens witch '{}' name.".format(name)}, 200

    def put(self, name):
        data = self.parser.parse_args()

        item = ItemModel.find_by_name(name)  # ItemModel(name, data['price'])

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):

        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}  # [item.json() for item in ItemModel.query.all()]
