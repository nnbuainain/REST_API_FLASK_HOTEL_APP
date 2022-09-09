from flask_restful import Resource, reqparse
from models.hotel import HotelModel

hoteis = [
        {
        'hotel_id': 'cayman',
        'nome': 'Hotel Cayman',
        'estrelas': 4.9,
        'diaria': 780,
        'cidade': 'Corumbá'
        },
        {
        'hotel_id': 'toca_onca',
        'nome': 'Hotel Toca da Onca',
        'estrelas': 4.4,
        'diaria': 280,
        'cidade': 'Cáceres'
        },
        {
        'hotel_id': 'bodoquena',
        'nome': 'Hotel Bodoquena',
        'estrelas': 4.3,
        'diaria': 190,
        'cidade': 'Bodoquena'
        },
        ]

class Hoteis(Resource):
    def get(self):
        return {'hoteis': hoteis}

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def find_hotel(hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel

        return None
    
    def get(self, hotel_id):
        hotel = Hotel.find_hotel(hotel_id)        
        
        if hotel:
            return hotel
        
        return {'message': 'Hotel not found.'}, 404 #not found

    def post(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        
        novo_hotel_objeto = HotelModel(hotel_id, **dados)
        novo_hotel = novo_hotel_objeto.convert_to_json()

        hoteis.append(novo_hotel)

        return novo_hotel, 200

    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        
        novo_hotel_objeto = HotelModel(hotel_id, **dados)
        novo_hotel = novo_hotel_objeto.convert_to_json()

        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            hotel.update(novo_hotel)
            return novo_hotel, 200 #OK
        
        hoteis.append(novo_hotel)
        
        return novo_hotel, 201 # CREATED

    def delete(self, hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                hoteis.remove(hotel)
                return {'message':'Hotel delete'}
        return {'message':'Hotel not found'}

    '''SOLUCAO DO PROF
    Achei interessante essa solução. Porém ela percorre todos os itens
    da lista mesmo já tendo achado o id a ser deletado
    para listas muito longas ela pode ser uma solução mais lenta'''
    
    # def delete(self, hotel_id):
    #     global hoteis
    #     hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
    #     return {'message': 'Hotel deleted'}
