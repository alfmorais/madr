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
    ("payload", "parameter_name"),
    [
        (
            {
                "username": "abcde123",
                "password": "7i2$&xT@#1",
                "email": "fghij46@gmail.com",
            },
            "username",
        ),
        (
            {
                "username": "abcde12",
                "password": "7i2$&xT@#1",
                "email": "fghij456@gmail.com",
            },
            "email",
        ),
    ],
)
def test_user_create_error_already_exists(
    session,
    payload,
    parameter_name,
):
    user = User(**payload)
    session.add(user)

    with pytest.raises(IntegrityError) as database_error:
        session.commit()

    session.rollback()

    assert database_error.typename == "IntegrityError"
    assert parameter_name in database_error.value.args[0]
    assert issubclass(database_error.type, IntegrityError)
