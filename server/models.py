from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, UniqueConstraint, DateTime
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.String)
    nearest_star = db.Column(db.String)
    image = db.Column(db.String)
    # created_at = db.Column(db.DateTime, db.func.now())
    # updated_at = db.Column(db.DateTime, db.func.now())

    planet_missions = db.relationship("Mission", back_populates="planet")
    scientist = association_proxy("planet_missions", "scientist")

    serialize_only = (
        "id",
        "name",
        "distance_from_earth",
        "nearest_star",
        "image",
    )


class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    field_of_study = db.Column(db.String, nullable=False)
    avatar = db.Column(db.String)
    # created_at = db.Column(db.DateTime, db.func.now())
    # updated_at = db.Column(db.DateTime, db.func.now())

    scientist_missions = db.relationship("Mission", back_populates="scientist")
    planets = association_proxy("scientist_missions", "planet")

    serialize_only = (
        "id",
        "name",
        "field_of_study",
        "avatar",
    )

    @validates("name")
    def validates_name(self, key, name):
        if not name or len(name) < 1:
            raise ValueError("Invalid name")
        return name
    
    @validates("field_of_study")
    def validates_field_of_study(self, key, field_of_study):
        if not field_of_study or len(field_of_study) < 1:
            raise ValueError("Invalid field")
        return field_of_study

class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    # created_at = db.Column(db.DateTime, db.func.now())
    # updated_at = db.Column(db.DateTime, db.func.now())
    scientist_id = db.Column(db.Integer, db.ForeignKey("scientists.id"), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"), nullable=False)

    scientist = db.relationship("Scientist", back_populates="scientist_missions")
    planet = db.relationship("Planet", back_populates="planet_missions")

    serialize_only = (
        "id",
        "name",
        "scientist_id",
        "planet_id",
    )

    @validates("name")
    def validates_name(self, key, name):
        if not name or len(name) < 1:
            raise ValueError("Invalid name")
        return name
    
    @validates("scientist_id")
    def validates_scientist_id(self, key, scientist_id):
        if not scientist_id:
            raise ValueError("Invalid scientist_id")
        return scientist_id
    
    @validates("planet_id")
    def validates_planet_id(self, key, planet_id):
        if not planet_id:
            raise ValueError("Invalid planet_id")
        return planet_id
    