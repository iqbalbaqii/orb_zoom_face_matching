from src.model.connection import connection


class Meeting:

    def __init__(self):
        self.cursor = connection.cursor
        self.table = 'meeting'

    def store(self, data: dict):
        keys = ', '.join(data.keys())
        values = list(data.values())
        quest_mark = ['?' for k in range(len(values))]
        mark = ','.join(quest_mark)
        self.cursor.execute('INSERT INTO '+self.table +
                            '('+keys+') VALUES ('+mark+')', values)
        connection.cnn.commit()

    def get_latest(self):

        self.cursor.execute(
            "SELECT TOP 1 * FROM meeting ORDER BY created_at DESC"
        )
        return self.cursor.fetchall()
