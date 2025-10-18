import pytest

from .backend import database

def test_initial_activities_loaded():
    """Verify initial activities are seeded into the in-memory database"""
    database.init_database()
    activities = {a['_id'] for a in database.activities_collection.find()}
    # Basic expectations
    assert 'Chess Club' in activities
    assert 'Manga Club' in activities


def test_activity_fields():
    """Ensure activity documents include required fields"""
    database.init_database()
    for a in database.activities_collection.find():
        assert 'description' in a
        assert 'schedule_details' in a
        assert 'max_participants' in a
        assert 'participants' in a
