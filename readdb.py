from dbconnection import connect
import matplotlib.pyplot as plt




class Visualization:
    def __init__(self):
        self.db = connect()
        self.category = []
        self.techno = []
        self.spor = []
        self.eco = []
        self.science = []
        self.game = []
        self.health = []

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
            if i == "Teknoloji":
                self.techno.append(i)
            elif i == "Spor":
                self.spor.append(i)
            elif i == "Oyun":
                self.game.append(i)
            elif i == "Ekonomi":
                self.eco.append(i)
            elif i == "Sağlık":
                self.health.append(i)
            else:
                pass


        Sections =  ["Teknoloji","Spor","Ekonomi","Sağlık","Oyun"]
        SectionsLen = [len(self.techno),len(self.spor),len(self.eco),len(self.health),len(self.game)]



        plt.bar(Sections,SectionsLen)
        plt.title("NEWS CATEGORİES")
        plt.xlabel("Sections")
        plt.ylabel("SectionsLen")
        plt.show()





a = Visualization()
a.read_db()