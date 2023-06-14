import pytest

from app import app
from models import db, Planet, Scientist, Mission


class TestModels:
    """SQLAlchemy models in models.py"""

    def test_validates_scientist_name(self):
        """require scientist to have names."""

        with app.app_context():
            with pytest.raises(ValueError):
                Scientist(name=None)

            with pytest.raises(ValueError):
                Scientist(name="")

    def test_validates_scientist_unique(self):
        """requires scientist to have unique names"""
        with app.app_context():
            Scientist(name="John Smith")
            with pytest.raises(ValueError):
                Scientist(name="John Smith")

    def test_validates_mission_crew(self):
        """require missions to have scientist,name, and planet"""
        with app.app_context():
            with pytest.raises(ValueError):
                Mission(name="", scientist_id=2, planet_id=1)

            with pytest.raises(ValueError):
                Mission(name="Venus", scientist_id=None, planet_id=1)

            with pytest.raises(ValueError):
                Mission(name="Mars", scientist_id=2, planet_id=None)

    def test_validates_mission_scientist(self):
        """requires scientists only be added to a mission once."""
        with app.app_context():
            Mission(name="Mars", scientist_id=2, planet_id=3)
            with pytest.raises(ValueError):
                Mission(name="Mars", scientist_id=2, planet_id=3)
