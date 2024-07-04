from src.app.models.novelists import Novelist


def test_create_novelist(session):
    novelist = Novelist(name="Isaac Asimov")
    session.add(novelist)
    session.commit()
    session.refresh(novelist)

    assert novelist.id is not None
    assert novelist.name == "Isaac Asimov"
