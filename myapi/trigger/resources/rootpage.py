from flask_restful import Resource


class RootPage(Resource):
    @staticmethod
    def get():
        return "<html><body>westhideAPI success!</body></html>"
