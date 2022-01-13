from app.models import User, Role


def test_new_user():
    """
    Given a User model
    When a new User is created
    Then check the email, hashed_password, and role fields are defined correctly
    """

    user = User(username='testuser',
                email='user1@test.com',
                password='TestPassword1',
                location='Toronto, ON',
                role_id=Role.MUSICIAN)
    assert user.username == 'testuser'
    assert user.email == 'user1@test.com'
    assert user.password_hash != 'TestPassword1'
    assert user.role_id == Role.MUSICIAN
    assert user.location == 'Toronto, ON'

    