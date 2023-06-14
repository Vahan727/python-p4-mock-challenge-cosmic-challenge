import pytest

from app import app
from models import db, Planet, Scientist, Mission
from sqlalchemy.exc import IntegrityError


class TestModels:
    """SQLAlchemy models in models.py"""

    def test_validates_scientist_name(self):
        """require scientist to have names."""
        with app.app_context():
            Scientist.query.delete()
            db.session.commit()

            scientist = Scientist()
            with pytest.raises(IntegrityError):
                db.session.add(scientist)
                db.session.commit()

            # with pytest.raises(ValueError):
            #     db.session.add(scientist)
            #     db.session.commit()

    def test_validates_scientist_field_of_study(self):
        """require scientist to have fields of study."""
        with app.app_context():
            Scientist.query.delete()
            db.session.commit()

            scientist = Scientist(name="tony stark")
            with pytest.raises(IntegrityError):
                db.session.add(scientist)
                db.session.commit()

            # with pytest.raises(ValueError):
            #     db.session.add(scientist)
            #     db.session.commit()

    def test_validates_scientist_unique(self):
        """requires scientist to have unique names"""
        with app.app_context():
            Scientist.query.delete()
            db.session.commit()
            scientist1 = Scientist(
                name="John Smith", field_of_study="robotics"
            )
            scientist2 = Scientist(
                name="John Smith", field_of_study="robotics"
            )
            with pytest.raises(IntegrityError):
                db.session.add_all([scientist1, scientist2])
                db.session.commit()

    def test_validates_mission_name(self):
        """require missions to have name"""
        with app.app_context():
            Mission.query.delete()
            db.session.commit()
            mission1 = Mission(scientist_id=2, planet_id=1)
            with pytest.raises(IntegrityError):
                db.session.add(mission1)
                db.session.commit()

    def test_validates_mission_scientist(self):
        """require missions to have scientist"""
        with app.app_context():
            Mission.query.delete()
            db.session.commit()
            mission1 = Mission(name="mars trip", planet_id=1)
            with pytest.raises(IntegrityError):
                db.session.add(mission1)
                db.session.commit()

    def test_validates_mission_planet(self):
        """require missions to have name"""
        with app.app_context():
            Mission.query.delete()
            db.session.commit()
            mission1 = Mission(scientist_id=2, name="john smith")
            with pytest.raises(IntegrityError):
                db.session.add(mission1)
                db.session.commit()

    # this can be commented out if you want to test using Api
    def test_validates_mission_scientist_only_once(self):
        """requires scientists only be added to a mission once."""
        with app.app_context():
            Mission.query.delete()
            db.session.commit()
            scientist1 = Scientist(
                name="Tony Stark",
                field_of_study="robotics",
                avatar="https://placekitten.com/250/250",
            )
            mars = Planet(
                name="Mars",
                distance_from_earth="400",
                nearest_star="the sun",
                image="image.jpg",
            )
            db.session.add_all([scientist1, mars])
            db.session.commit()
            mission1 = Mission(
                name="Mars", scientist_id=scientist1.id, planet_id=mars.id
            )
            mission2 = Mission(
                name="Mars", scientist_id=scientist1.id, planet_id=mars.id
            )
            with pytest.raises(IntegrityError):
                db.session.add_all([mission1, mission2])
                db.session.commit()
