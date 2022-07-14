from src.model.connection import connection

cursor = connection.cursor
table = 'dataset_label'


def store(data: dict()):
    keys = ', '.join(data.keys())
    values = list(data.values())
    quest_mark = ['?' for k in range(len(values))]
    mark = ','.join(quest_mark)
    cursor.execute('INSERT INTO '+table +
                   '('+keys+') VALUES ('+mark+')', values)
    connection.cnn.commit()


def get(select_clause, by=""):

    if by == "":
        where_clause = by
    else:
        where_clause = " WHERE "+by

    cursor.execute("SELECT "+select_clause+" FROM "+table+where_clause)
    return cursor.fetchall()
