from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, UniqueConstraint
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
    __tablename__ = "planets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.String)
    nearest_star = db.Column(db.String)
    image = db.Column(db.String)
    planet_missions = db.relationship("Mission", back_populates="planet", passive_deletes=True)

    serialize_only = (
        "id",
        "name",
        "distance_from_earth",
        "image",
        "nearest_star",
    )

    def __repr__(self):
        return f"<Planet {self.id}: {self.name}>"


class Scientist(db.Model, SerializerMixin):
    __tablename__ = "scientists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    field_of_study = db.Column(db.String, nullable=False)
    avatar = db.Column(db.String)
    planets = association_proxy("scientist_missions", "planet")
    scientist_missions = db.relationship("Mission", back_populates="scientist", passive_deletes=True)

    serialize_rules = (
        "-missions.scientist",
        "-planets.planet_mission",
        "-scientist_missions.scientist",
    )

    @validates("name")
    def validate_scientist_name(self, key, name):
        if not name or len(name) < 1:
            raise ValueError("Must have a name")
        return name

    @validates("field_of_study")
    def validate_field_of_study(self, key, field_of_study):
        if not field_of_study or len(field_of_study) < 1:
            raise ValueError("Must have field of study")
        return field_of_study

    def __repr__(self):
        return f"<Scientist {self.id}: {self.name}>"


class Mission(db.Model, SerializerMixin):
    __tablename__ = "missions"
    __table_args__ = (UniqueConstraint("name", "scientist_id", "planet_id"),)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    scientist_id = db.Column(
        db.Integer, db.ForeignKey("scientists.id", ondelete="CASCADE"), nullable=False
    )
    scientist = db.relationship(
        "Scientist", back_populates="scientist_missions"
    )
    planet_id = db.Column(
        db.Integer, db.ForeignKey("planets.id", ondelete="CASCADE"), nullable=False
    )
    planet = db.relationship("Planet", back_populates="planet_missions")

    serialize_rules = (
        "-planet.missions",
        "-scientist.missions",
        "-scientists.mission",
        "-planets.mission",
    )

    @validates("name")
    def validate_name(self, key, name):
        if not name or len(name) < 1:
            raise ValueError("Mission must have a name")
        return name


# add any models you may need.
