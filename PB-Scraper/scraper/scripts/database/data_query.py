from logging import getLogger

from psycopg2 import sql

logger = getLogger(__name__)

def does_row_exist(table, identifier, conn):
    '''
    returns bool
    raises psycopg2.Error or psycopg2.Warning if sth goes wrong

    table (str) : table name
    identifier (uuid.UUID | str) : id of the row you're trying to reach
    conn (psycopg2.connection) : connection that will be used
    '''
    identifier = str(identifier)

    query = sql.SQL("SELECT 1 FROM {} WHERE id = %s;").format( sql.Identifier(table) )

    with conn.cursor() as cur:
        cur.execute( query, [identifier])
        return bool( cur.fetchone() )
#end of does_row_exist


def select_match(table, search_param, conn, col_to_return=None):
    '''
    uses col_name = col_value condition to fetch the first matching row or just col_to_return

    returns row as tuple 
        or if col_to_return is specified - specific value

    raises psycopg2.Error or psycopg2.Warning if sth goes wrong
    raises ValueError if values is empty

    table (str) : table name
    search_param (dict) : dictionary of column name : column value - specifying exact values that a searched row must have
    conn (psycopg2.connection) : connection that will be used
    col_to_return (optional str) : name of a single column you want to fetch
    '''
    if len(search_param) == 0:
        raise ValueError("select_match: search_param is empty, cannot construct a query")

    search_columns = search_param.keys()
    search_values = list( search_param.values() ) #converting to sequence

    #formating SELECT {}
    if col_to_return is None:
        col_to_return = sql.SQL("*")
    else:
        col_to_return = sql.Identifier(col_to_return)

    #formating FROM {}
    table = sql.Identifier(table)

    #formatting WHERE {}
    search_conditions = sql.SQL(' AND ').join(  [ sql.Identifier(col) + sql.SQL(' = ') + sql.Placeholder() for col in search_columns ] )
    

    query = sql.SQL("SELECT {} FROM {} WHERE {};").format(
        col_to_return, table, search_conditions) 
    

    with conn.cursor() as cur:
        cur.execute( query, search_values )
        result = cur.fetchone()

    if result and len(result) == 1:
        return result[0]
    return result
#end of select_match


def select_by_id(table, identifier, conn, col=None):
    '''
    alias for select_match(table, {"id" : identifier} conn, col)

    identifier (uuid.UUID | str) : id of the row you're trying to reach
    '''
    identifier = str(identifier)
    return select_match(table, {"id" : identifier}, conn, col)
#end of select_by_id
