from flask_restful import Resource


class RootPage(Resource):
    @staticmethod
    def get():
        return "westhideAPI success!"
