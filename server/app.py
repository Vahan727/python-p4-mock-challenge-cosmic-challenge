#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS
from models import db, Planet, Scientist, Mission

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
CORS(app)
api = Api(app)
db.init_app(app)


@app.route("/")
def home():
    return ""


class Scientists(Resource):
    def get(self):
        scientists = [
            scientist.to_dict() for scientist in Scientist.query.all()
        ]
        return scientists, 200

    def post(self):
        data = request.get_json()
        try:
            new_scientist = Scientist(
                name=data.get("name"),
                field_of_study=data.get("field_of_study"),
                avatar=data.get("avatar"),
            )
            db.session.add(new_scientist)
            db.session.commit()
            return new_scientist.to_dict(), 201
        except Exception:
            return ({"error": "400"}, 400)


api.add_resource(Scientists, "/scientists")


class ScientistByID(Resource):
    def get(self, id):
        try:
            scientist = Scientist.query.filter(Scientist.id == id).first()
            return scientist.to_dict(), 200
        except Exception:
            return ({"error": "404 not found"}, 404)

    def patch(self, id):
        data = request.get_json()
        scientist = Scientist.query.filter(Scientist.id == id).first()
        if not scientist:
            return ({"error": "404 not found"}, 404)
        for attr in data:
            setattr(scientist, attr, data.get(attr))
        db.session.add(scientist)
        db.session.commit()
        return scientist.to_dict(), 200

    def delete(self, id):
        scientist = Scientist.query.filter(Scientist.id == id).first()
        if not scientist:
            return ({"error": "404 not found"}, 404)
        db.session.delete(scientist)
        db.session.commit()
        return ({}, 204)


api.add_resource(ScientistByID, "/scientists/<int:id>")


class Planets(Resource):
    def get(self):
        return [planet.to_dict() for planet in Planet.query.all()], 200


api.add_resource(Planets, "/planets")


class PlanetsByID(Resource):
    def delete(self, id):
        planet = Planet.query.filter(Planet.id == id).first()
        try:
            db.session.delete(planet)
            db.session.commit()
            return ({}, 204)
        except Exception:
            return ({"error": "404"}, 404)


api.add_resource(PlanetsByID, "/planets/<int:id>")


class Missions(Resource):
    def post(self):
        data = request.get_json()
        new_mission = Mission(
            name=data.get("name"),
            scientist_id=data.get("scientist_id"),
            planet_id=data.get("planet_id"),
        )
        db.session.add(new_mission)
        db.session.commit()
        return new_mission.to_dict(), 201


api.add_resource(Missions, "/missions")
if __name__ == "__main__":
    app.run(port=5555, debug=True)
