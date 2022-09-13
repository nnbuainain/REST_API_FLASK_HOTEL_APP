from models.site import SiteModel
from flask_restful import Resource

class Sites(Resource):
    def get(self):
        return {'sites' : [site.to_json() for site in SiteModel.query.all()]}

class Site(Resource):
    def get(self, url):
        site = SiteModel.find_site(url)
        
        if site:
            return site.to_json()
        
        return {'message' : 'site not found'}, 404
    
    def post(self, url):
        if SiteModel.find_site(url):
            return {'message' : 'Site already exists'}
        
        try:
            site = SiteModel(url)
            site.save_site()
        except:
            return {'message': 'an internal error has occurred while saving site'}
        return site.to_json()
    
    def delete(self, url):
        site = SiteModel.find_site(url)
        
        if site:
            site.delete_site()
            return {'message' : 'site successfully deleted'}

        return {'message' : 'site not found'}, 404