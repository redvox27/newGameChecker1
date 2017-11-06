class Game():
    name = ""
    releaseDate = ""

    def __init__(self, name, releaseDate):
        self.name = name
        self.releaseDate = releaseDate

    def getName(self):
        return self.name

    def getReleasedate(self):
        return self.releaseDate