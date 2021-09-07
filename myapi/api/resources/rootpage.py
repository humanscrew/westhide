from flask_restful import Resource


class RootPage(Resource):
    
    def get(self):
        return "westhideAPI success!"
