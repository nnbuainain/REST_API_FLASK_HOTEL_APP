from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required
class Hoteis(Resource):
    def get(self):
        return {'hoteis': [hotel.to_json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type = str, required = True, help = "the field nome cannot be blank")
    argumentos.add_argument('estrelas', type = float, required = True, help = "the field estrela cannot be blank")
    argumentos.add_argument('diaria', type = float)
    argumentos.add_argument('cidade', type = str)

    def find_hotel(hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel

        return None
    
    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)        
        
        if hotel:
            return hotel.to_json()
        
        return {'message': 'Hotel not found.'}, 404 #not found

    @jwt_required()
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' already exists.".format(hotel_id)}, 400 # BAD REQUEST

        dados = Hotel.argumentos.parse_args()
        
        hotel = HotelModel(hotel_id, **dados)
        
        try:
            hotel.save_hotel()
        except:
            return {"message" : "an internal error occurred while saving hotel"}, 500

        return hotel.to_json(), 200

    @jwt_required()
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.to_json(), 200 #OK

        hotel = HotelModel(hotel_id, **dados)
        
        try:
            hotel.save_hotel()
        except:
            return {"message" : "an internal error occurred while saving hotel"}, 500

        return hotel.to_json(), 201 #CREATED

    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        
        if hotel:
            try:
                hotel.delete_hotel()
            
            except:
                return {"message" : "an internal error occurred while saving hotel"}, 500

            return {"message":"Hotel '{}' deleted".format(hotel_id)}
        
        return {'message':'Hotel not found'}