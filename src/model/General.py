from src.model.connection import connection


class General:
    def __init__(self):
        self.cursor = connection.cursor

    def select(self,select: str):
        
        self.cursor.execute(select)

        desc = self.cursor.description
        column_names = [col[0] for col in desc]
        data = [dict(zip(column_names, row))
                for row in self.cursor.fetchall()]
        return data
