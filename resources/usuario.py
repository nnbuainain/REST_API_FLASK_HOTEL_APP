from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from hmac import compare_digest
from blacklist import BLACKLIST

argumentos = reqparse.RequestParser()
argumentos.add_argument('login', type = str, required = True, help = "the field 'login' cannot be blank")
argumentos.add_argument('senha', type = str, required = True, help = "the field 'senha' cannot be blank")


class User(Resource):

    def get(self, user_id):
        user = UserModel.find_user(user_id)        
        
        if user:
            return user.to_json()
        
        return {'message': 'User not found.'}, 404 #not found

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        
        if user:
            try:
                user.delete_user()
            
            except:
                return {"message" : "an internal error occurred while saving user"}, 500

            return {"message":"User '{}' deleted".format(user_id)}
        
        return {'message':'User not found'}


class UserRegister(Resource):
    
    def post(self):  
        dados = argumentos.parse_args()
        
        if UserModel.find_user_by_login(dados['login']):
            return {"message" : "Login '{}' already exists".format(dados['login'])}
        
        user = UserModel(**dados)
        user.save_user()

        return {'message' : 'User registered successfully'}

class UserLogin(Resource):
    
    @classmethod
    def post(cls):
        dados = argumentos.parse_args()
        
        user = UserModel.find_user_by_login(dados['login'])

        if user and compare_digest(user.senha, dados['senha']):
            access_token = create_access_token(identity= user.user_id)
            return {'access_token' : access_token}
        
        return {'message' : 'Incorrect login or password'}

class UserLogout(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti'] # JWT TOKEN IDENTIFIER
        
        BLACKLIST.add(jwt_id)
        
        return {'message' : 'You successfully logged out'}


