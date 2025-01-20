
import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    """Funkcja zwraca połączenie do bazy danych PostgreSQL."""
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="&r6:a}$ryXVAh!n",
        host="ioprojectdatabase.postgres.database.azure.com",
        port="5432"
    )

def execute_query(query, params=None):
    """Funkcja do wykonywania zapytań SQL. Zwraca wyniki dla SELECT lub None dla pozostałych."""
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            if query.strip().lower().startswith("select"):
                return cursor.fetchall()
            conn.commit()
    except Exception as e:
        print(f"Błąd podczas wykonywania zapytania: {e}")
    finally:
        conn.close()
