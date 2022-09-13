from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from models.site import SiteModel
from resources.filtros import normalize_path_params, consulta_sem_cidade, consulta_com_cidade
from flask_jwt_extended import jwt_required
import sqlite3


path_params = reqparse.RequestParser()
path_params.add_argument("cidade", type = str)
path_params.add_argument("estrelas_min", type = float)
path_params.add_argument("estrelas_max", type = float)
path_params.add_argument("diaria_min", type = float)
path_params.add_argument("diaria_max", type = float)
path_params.add_argument("limit", type = int)
path_params.add_argument("offset", type = int)

class Hoteis(Resource):
    def get(self):
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()

        dados = path_params.parse_args()

        dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}

        parametros = normalize_path_params(**dados_validos)

        if not parametros.get('cidade'):
            valores_parametros = tuple([parametros[chave] for chave in parametros]) 

            resultado = cursor.execute(consulta_sem_cidade, valores_parametros)
            
        else:
            valores_parametros = tuple([parametros[chave] for chave in parametros]) 

            resultado = cursor.execute(consulta_com_cidade, valores_parametros)

        hoteis = []

        for linha in resultado:
            hoteis.append({
                'hotel_id' : linha[0],
                'nome' : linha[1],
                'estrelas' : linha[2],
                'diaria' : linha[3],
                'cidade' : linha[4],
                'site_id' : linha[5]
            })

        return {'hoteis': hoteis}


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type = str, required = True, help = "the field nome cannot be blank")
    argumentos.add_argument('estrelas', type = float, required = True, help = "the field estrela cannot be blank")
    argumentos.add_argument('diaria', type = float)
    argumentos.add_argument('cidade', type = str)
    argumentos.add_argument('site_id', type = int, required = True, help = 'Hotel needs a source website')

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
        
        if not SiteModel.find_site_by_id(dados.get('site_id')):
            return {'message' : 'The hotel must have a valid site id'}
        
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