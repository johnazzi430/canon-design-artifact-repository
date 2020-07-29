import pytest

import server
import server.modules
import server.modules.models
import server.modules.api

def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, authenticated, and role fields are defined correctly
    """
    user = server.modules.models.User(username = 'patkennedy79@gmail.com')
    user.hash_password('FlaskIsAwesome')
    assert user.username == 'patkennedy79@gmail.com'
    assert user.password_hash != 'FlaskIsAwesome'
    assert user.verify_password('FlaskIsAwesome')

def test_user_in_session(app):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, authenticated, and role fields are defined correctly
    """
    
    res = server.modules.api.user_in_session(app)
    assert res != {"message": "user not in session"}
