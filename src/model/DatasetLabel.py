from src.model.connection import connection


class DatasetLabel:

    def __init__(self):
        self.cursor = connection.cursor
        self.table = 'dataset_label'

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

    def get2(self, select_clause="*", by=""):

        if by == "":
            where_clause = by
        else:
            where_clause = " WHERE "+by

        self.cursor.execute("SELECT "+select_clause +
                            " FROM "+self.table+where_clause)
        desc = self.cursor.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row))
                for row in self.cursor.fetchall()]
        return data
