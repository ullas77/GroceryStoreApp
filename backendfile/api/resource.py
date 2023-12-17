from flask_restful import Api, Resource, abort, fields, marshal
from application.models import db ,user as users_model
from flask import jsonify
api=Api(prefix="/")

user_resourse_fields={
    "username":fields.String,
    "email": fields.String
}

class user(Resource):
    def get(self, userid=None):
        if userid==5:
            abort(400, message="the user id restricted")
        else:
            use=users_model.query.filter_by(userid=userid).first()
            if use:
                return marshal(user, user_resourse_fields)
                
            else:
                abort(404, messsage="user is not found")




    

api.add_resource(user, '/users/<int:id>')
