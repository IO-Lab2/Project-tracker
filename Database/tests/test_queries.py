import pytest
from db_connection import execute_query
from queries import (
    get_scientists_by_last_name, 
    get_organizations_by_type, 
    get_publications_by_citation_count
)

@pytest.fixture
def setup_database():
    """Fixture przygotowujący dane testowe przed każdym testem."""
    # Dodanie danych testowych do bazy danych
    execute_query("INSERT INTO scientists (id, first_name, last_name) VALUES ('00000000-0000-0000-0000-000000000001', 'Jan', 'Kowalski')")
    execute_query("INSERT INTO organizations (id, name, type) VALUES ('00000000-0000-0000-0000-000000000002', 'Politechnika', 'university')")
    execute_query("INSERT INTO scientist_organization (scientist_id, organization_id) VALUES ('00000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000002')")
    execute_query("INSERT INTO publications (id, title, citations_count) VALUES ('00000000-0000-0000-0000-000000000003', 'Example Publication', 50)")
    execute_query("INSERT INTO scientists_publications (scientist_id, publication_id) VALUES ('00000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000003')")
    execute_query("INSERT INTO bibliometrics (scientist_id, h_index, citation_count, publication_count, ministerial_score) VALUES ('00000000-0000-0000-0000-000000000001', 10, 100, 5, 15.0)")
    yield
    # Usunięcie danych testowych po zakończeniu testów
    execute_query("DELETE FROM scientists_publications WHERE scientist_id = '00000000-0000-0000-0000-000000000001'")
    execute_query("DELETE FROM publications WHERE id = '00000000-0000-0000-0000-000000000003'")
    execute_query("DELETE FROM scientist_organization WHERE scientist_id = '00000000-0000-0000-0000-000000000001'")
    execute_query("DELETE FROM organizations WHERE id = '00000000-0000-0000-0000-000000000002'")
    execute_query("DELETE FROM bibliometrics WHERE scientist_id = '00000000-0000-0000-0000-000000000001'")
    execute_query("DELETE FROM scientists WHERE id = '00000000-0000-0000-0000-000000000001'")

def test_get_scientists_by_last_name(setup_database):
    """Test sprawdza, czy możemy pobrać naukowców o określonym nazwisku."""
    query = get_scientists_by_last_name('Kowalski')
    result = execute_query(query)
    assert len(result) == 1
    assert result[0]['first_name'] == 'Jan'

def test_get_organizations_by_type(setup_database):
    """Test sprawdza, czy możemy pobrać organizacje o określonym typie."""
    query = get_organizations_by_type('university')
    result = execute_query(query)
    assert len(result) == 1
    assert result[0]['name'] == 'Politechnika'

def test_get_publications_by_citation_count(setup_database):
    """Test sprawdza, czy możemy pobrać publikacje o liczbie cytowań powyżej określonej wartości."""
    query = get_publications_by_citation_count(10)
    result = execute_query(query)
    assert len(result) >= 1
    assert result[0]['citations_count'] >= 10

def test_scientist_organization_relationship(setup_database):
    """Test sprawdza, czy naukowiec jest przypisany do organizacji."""
    query = "SELECT * FROM scientist_organization WHERE scientist_id = '00000000-0000-0000-0000-000000000001'"
    result = execute_query(query)
    assert len(result) == 1
    assert result[0]['organization_id'] == '00000000-0000-0000-0000-000000000002'

def test_scientist_publication_relationship(setup_database):
    """Test sprawdza, czy naukowiec jest przypisany do publikacji."""
    query = "SELECT * FROM scientists_publications WHERE scientist_id = '00000000-0000-0000-0000-000000000001'"
    result = execute_query(query)
    assert len(result) == 1
    assert result[0]['publication_id'] == '00000000-0000-0000-0000-000000000003'

def test_bibliometric_data(setup_database):
    """Test sprawdza, czy dane bibliometryczne są prawidłowo zapisane dla naukowca."""
    query = "SELECT * FROM bibliometrics WHERE scientist_id = '00000000-0000-0000-0000-000000000001'"
    result = execute_query(query)
    assert len(result) == 1
    assert result[0]['h_index'] == 10
    assert result[0]['citation_count'] == 100
    assert result[0]['publication_count'] == 5
    assert result[0]['ministerial_score'] == 15.0
