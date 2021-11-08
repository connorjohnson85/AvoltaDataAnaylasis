class Obituary:
    def __init__(self):
        self.name = ""
        self.dateOfDeath = ""
        self.condolences = []
        self.images = []
        self.obituary = ""

    def __iter__(self):
        return iter([self.name, self.dateOfDeath, self.obituary, " ".join(self.condolences), " ".join(self.images)])
