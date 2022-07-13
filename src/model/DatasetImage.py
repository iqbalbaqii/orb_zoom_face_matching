from src.model.connection import connection

cursor = connection.cursor
table = 'dataset_image'


def store(data):
    keys = ', '.join(data.keys())
    values = list(data.values())
    cursor.execute('INSERT INTO '+table +
                   '('+keys+') VALUES (?,?,?,?,?,?)', values)
    connection.cnn.commit()


def get(select_clause, by=""):

    if by == "":
        where_clause = by
    else:
        where_clause = " WHERE "+by

    cursor.execute("SELECT "+select_clause+" FROM "+table+where_clause)
    return cursor.fetchall()
