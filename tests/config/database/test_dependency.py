from unittest.mock import MagicMock, patch

from src.config.database.dependency import get_db


def test_get_db():
    mock_session = MagicMock()

    with patch(
        "src.config.database.dependency.SessionLocal",
        return_value=mock_session,
    ):
        gen = get_db()
        db = next(gen)

        assert db == mock_session
        mock_session.close.assert_not_called()

        try:
            next(gen)
        except StopIteration:
            pass

        mock_session.close.assert_called_once()


def test_get_db_exception():
    mock_session = MagicMock()

    with patch(
        "src.config.database.dependency.SessionLocal",
        return_value=mock_session,
    ):
        gen = get_db()
        db = next(gen)

        assert db == mock_session
        mock_session.close.assert_not_called()

        try:
            raise RuntimeError("Some error")
        except Exception:
            try:
                next(gen)
            except StopIteration:
                pass

        mock_session.close.assert_called_once()
