from src.app.controllers.novelists import (
    CreateNovelistController,
    ListNovelistController,
)
from src.app.schemas.requests.novelists import (
    NovelistListQueryParams,
    NovelistRequest,
)


def test_list_novelist_success(session):
    first_novelist = NovelistRequest(name="Isaac Asimov")
    second_novelist = NovelistRequest(name="Isaac Newton")

    CreateNovelistController.handle(first_novelist, session)
    CreateNovelistController.handle(second_novelist, session)

    query_params = NovelistListQueryParams(name="aa")
    response = ListNovelistController.handle(session, query_params)

    expected_result = 2

    assert isinstance(response, dict)
    assert "novelists" in response
    assert len(response["novelists"]) == expected_result
    assert response["novelists"][0]["name"] == "isaac asimov"
    assert response["novelists"][1]["name"] == "isaac newton"


def test_list_novelist_not_found(session):
    query_params = NovelistListQueryParams(name="y")
    response = ListNovelistController.handle(session, query_params)

    assert isinstance(response, dict)
    assert "novelists" in response
    assert len(response["novelists"]) == 0
