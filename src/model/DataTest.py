from src.model.connection import connection


class DataTest:

    def __init__(self):
        self.cursor = connection.cursor
        self.table = 'data_test'

    def store(self, data: dict):
        keys = ', '.join(data.keys())
        values = list(data.values())
        quest_mark = ['?' for k in range(len(values))]
        mark = ','.join(quest_mark)
        self.cursor.execute('INSERT INTO '+self.table +
                            '('+keys+') VALUES ('+mark+')', values)
        connection.cnn.commit()

