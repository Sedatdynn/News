from dbconnection import connect
import matplotlib as plt

class Visualization:
    def __init__(self):
        self.db = connect()
        self.category = []

    def read_db(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM all_news")
        row = cursor.fetchall()

        for i in row:
            self.category.append(i[7])

        self.db.close()
        self.visualite(self.category)
    def visualite(self,category):
        for i in category:
            pass


a = Visualization()
a.read_db()