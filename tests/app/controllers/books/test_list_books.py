from src.app.controllers.books import ListBookController
from src.app.models.books import Book
from src.app.models.novelists import Novelist
from src.app.schemas.requests.books import BookQueryParams


def test_list_books_success(session):
    first_novelist = Novelist(name="Isaac Asimov")
    second_novelist = Novelist(name="Arthur C. Clarke")
    third_novelist = Novelist(name="J.D. Salinger")
    fourth_novelist = Novelist(name="John Wyndham")
    fifth_novelist = Novelist(name="Ray Bradbury")

    session.add_all([
        first_novelist,
        second_novelist,
        third_novelist,
        fourth_novelist,
        fifth_novelist,
    ])
    session.commit()
    session.refresh(first_novelist)
    session.refresh(second_novelist)
    session.refresh(third_novelist)
    session.refresh(fourth_novelist)
    session.refresh(fifth_novelist)

    book1 = Book(
        title="Foundation",
        year=1951,
        novelist_id=first_novelist.id,
    )
    book2 = Book(
        title="The Martian Chronicles",
        year=1951,
        novelist_id=fifth_novelist.id,
    )
    book3 = Book(
        title="The Catcher in the Rye",
        year=1951,
        novelist_id=third_novelist.id,
    )
    book4 = Book(
        title="The Day of the Triffids",
        year=1951,
        novelist_id=fourth_novelist.id,
    )
    book5 = Book(
        title="The Sands of Mars",
        year=1951,
        novelist_id=second_novelist.id,
    )

    session.add_all([book1, book2, book3, book4, book5])
    session.commit()

    query_params = BookQueryParams(title="a", year=1951)
    response = ListBookController.handle(session, query_params)

    expected_result = 5
    assert len(response["books"]) == expected_result


def test_list_books_no_results(session):
    query_params = BookQueryParams(title="Nonexistent Book", year=9999)
    response = ListBookController.handle(session, query_params)

    assert len(response["books"]) == 0
