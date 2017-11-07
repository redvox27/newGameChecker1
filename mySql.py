import pymysql
class MySql():

    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='#enterPassword', db='#enterDatanase')
    cursor = db.cursor()

    def insertGame(self, title, releaseDate):
        query = "insert into games.game (title, releaseDate)\
                 values (%s, %s)"

        self.cursor.execute(query,(title, releaseDate))
        self.db.commit()


    def getGameFromDatabase(self, title):
        query = "select title from game where title like %s "
        result = self.cursor.execute(query, "%" + title + "%")
        entryFound = False

        if result > 0:
            entryFound = True

        return entryFound

sql = MySql()
sql.getGameFromDatabase("Call Of Duty3")
