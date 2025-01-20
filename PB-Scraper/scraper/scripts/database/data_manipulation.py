from psycopg2 import sql

from logging import getLogger

from scripts.database.data_query import does_row_exist, select_match

logger = getLogger(__name__)


def insert_or_update_with_id(table, identifier, conn, values, append_id=True):
    '''
    insert_or_update_matched where search_param = {"id" : identifier}

    append_id (bool) : whether to append assigning identifier to "id" column
       if "id" is specified in values, does nothing
    '''
    if append_id and "id" not in values:
        values["id"] = identifier

    return insert_or_update_matched(table, {"id" : identifier}, conn, values)
 

def insert_or_update_matched(table, search_param, conn, values):
    '''
    searches in table for first match that has exact values from search_param (see select_match)
    fetches id of that row
    depending on whether that id exists inserts or updates using values dict

    table (str) : name of a table
    search_param (dict) : columan name, column value pairs that will be used to find a match in table
    conn (psycopg2 connnection) : connection to use
    values (dict) : values to insert/update - keys are column names, values are values to put into these columns

    returns str id of the inserted/updated row

    raises psycopg2.Error or psycopg2.Warning if sth goes wrong
    '''
    matched_id = select_match(table, search_param, conn, col_to_return="id")
    if not matched_id:
        return insert_row(table, conn, values)
    else:
        update_row_with_id(table, matched_id, conn, values)
        return matched_id
    #end of insert_or_update_matched



def insert_row(table, conn, values):
    '''
    inserts rows into table with values dict providing column names and respective values
    e.g. 
    insert_row(table, conn,  
        values = {"id" : 123, "name" : "Jan"} )

    table (str) : name of a table
    conn (psycopg2.connection) : connection to use
    values (dict) : values to be inserted

    returns str id of the inserted row

    raises psycopg2.Error or psycopg2.Warning if sth goes wrong
    raises ValueError if values is empty
    '''
    if len(values) == 0:
        raise ValueError("insert_row: values is empty. Cannot construct a query")

    col_names = values.keys()
    col_values = list( values.values() ) #turning into a sequence

    query = sql.SQL("INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING id;").format(
        table=sql.Identifier(table),
        columns = sql.SQL(', ').join( [ sql.Identifier(s) for s in col_names ] ),
        placeholders = sql.SQL(', ').join( sql.Placeholder() *len(col_names) )
    )

    with conn.cursor() as cur:
        cur.execute( query, col_values)
        id = cur.fetchone()[0]

    conn.commit()
    return id

    #end of insert_row


def update_row_with_id(table, identifier, conn, values, add_updated_at=True):
    '''
    updates a row found using identifier - see insert_row

    identifier (str | uuid.UUID) : id of the row to update
    add_updated_at (bool) : whether to include 'updated_at=NOW()' in query

    raises psycopg2.Error or psycopg2.Warning if sth goes wrong
    raises ValueError if values is empty
    '''
    if len(values) == 0:
        raise ValueError("update_row_with_id: values is empty. Cannot construct a query")

    col_names = values.keys()
    col_values = list( values.values() ) #turning into a sequence
    col_values.append( str(identifier) )

    if add_updated_at:
        query = sql.SQL("UPDATE {table} SET {pairs}, updated_at=NOW() WHERE id = %s;").format(
            table=sql.Identifier(table),
            pairs = sql.SQL(', ').join( [ sql.Identifier(s) +  sql.SQL("=") + sql.Placeholder() for s in col_names ] ),
        )
    else:
        query = sql.SQL("UPDATE {table} SET {pairs} WHERE id = %s;").format(
            table=sql.Identifier(table),
            pairs = sql.SQL(', ').join( [ sql.Identifier(s) +  sql.SQL("=") + sql.Placeholder() for s in col_names ] ),
        )

    with conn.cursor() as cur:
        cur.execute( query, col_values)

    conn.commit()
    #end of update_row_with_id


