import pytest
from sqlalchemy.exc import IntegrityError

from src.app.models.users import User


def test_user_create_success(session):
    payload = {
        "username": "abcde123",
        "password": "7i2$&xT@#1",
        "email": "fghij456@gmail.com",
    }
    user = User(**payload)

    session.add(user)
    session.commit()
    session.refresh(user)

    assert isinstance(user.id, int)
    assert user.username == payload["username"]
    assert user.password == payload["password"]
    assert user.email == payload["email"]


@pytest.mark.parametrize(
    ("parameter_value", "parameter_name"),
    [("abcde123", "user.username"), ("abcde12", "user.email")],
)
def test_user_create_error_already_exists(
    session,
    parameter_value,
    parameter_name,
):
    error_database_message = "(sqlite3.IntegrityError)"
    expected_response = "{0} UNIQUE constraint failed: {1}".format(
        error_database_message,
        parameter_name,
    )
    payload = {
        "username": parameter_value,
        "password": "7i2$&xT@#1",
        "email": "fghij456@gmail.com",
    }

    user = User(**payload)
    session.add(user)

    with pytest.raises(IntegrityError) as database_error:
        session.commit()

    session.rollback()

    assert database_error.typename == "IntegrityError"
    assert database_error.value.args[0] == expected_response
    assert issubclass(database_error.type, IntegrityError)
