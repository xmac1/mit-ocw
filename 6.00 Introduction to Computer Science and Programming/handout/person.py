import datetime

class Person(object):
    def __init__(self, name):
        """create a person with name name"""
        self.name = name
        try:
            lastBlank = name.rindex(' ')
            self.lastName = name[lastBlank+1:]
        except:
            self.lastName = name
            self.bitheday = None
    def getLastName(self):
        """return self's last name"""
        return self.lastName
    def setBirthday(self, birthDate):
        """Assumes birthDate is of type datetime.date
           sets self's birthday to birthDate"""
        self.birhthday = birthDate
    def getAge(self):
        """returns self's current age in days"""
        if self.birthday == None:
            raise ValueError
        return (datetime.date.today() - self.birthday)
    def __lt__(self, other):
        """return True if self's name is lexicographically
           less than other's name, and False otherwise"""
        if slef.lastName == other.lastName:
            return self.name < other.name
        return self.lastName < other.lastName
    def __str__(self):
        """return self's name"""
        return self.name

me = Person('Michael Cuttag')
him = Person('Barack Hussein Obama')
her = Person('Madonna')
print him.getLastName()
him.setBirthday(datetime.date(1961, 8, 4))
her.setBirthday(datetime.date(1958, 8, 16))
