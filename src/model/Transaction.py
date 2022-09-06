from src.model.connection import connection


class Transaction:

    def __init__(self):
        self.cursor = connection.cursor
        self.table = 'tr_identification'

    def store(self, data: dict):
        keys = ', '.join(data.keys())
        values = list(data.values())
        quest_mark = ['?' for k in range(len(values))]
        mark = ','.join(quest_mark)
        self.cursor.execute('INSERT INTO '+self.table +
                            '('+keys+') VALUES ('+mark+')', values)
        connection.cnn.commit()

    def get(self, select_clause, by=""):

        if by == "":
            where_clause = by
        else:
            where_clause = " WHERE "+by

        self.cursor.execute("SELECT "+select_clause +
                            " FROM "+self.table+where_clause)
        return self.cursor.fetchall()
