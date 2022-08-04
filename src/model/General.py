from src.model.connection import connection


class General:
    def __init__(self):
        self.cursor = connection.cursor

    def select(self,select: str):
        
        self.cursor.execute(select)
        return self.cursor.fetchall()
