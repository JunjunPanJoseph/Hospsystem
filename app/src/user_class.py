from flask_login import UserMixin
from app.src.csv_management import csv_manage
class User(UserMixin):
    def __init__(self, email, password, name, phone):
        self.id = email
        self.email = email
        self.name = name
        self.password = password
        self.phone = phone
        self.authority = None
    def check(self):
        if (self.authority == None):
            return False
        cv = csv_manage(self.authority + ".csv")
        result = cv.search_data([[0, self.email]])
        if (result != []):
            return True
        return False
class Patient(User):
    def __init__(self, email, password, name, phone, cardNumber):
        User.__init__(self, email, password, name, phone)
        self.cardNumber = cardNumber
        self.authority = "patient"
    def get_line(self):
        return [self.email, self.password, self.name, self.phone, self.cardNumber]
    def update(self, add = False):
        cv = csv_manage(self.authority + ".csv")
        if (add == True):
            res = cv.write_data(self.get_line())
            return res
        else:
            return cv.edit_data([[0, self.email]], self.get_line())
class Provider(User):
    def __init__(self, email, password, name, phone, providerNumber, type):
        User.__init__(self, email, password, name, phone)
        self.providerNumber = providerNumber
        self.type = type
        self.authority = "provider"
    def get_line(self):
        return [self.email, self.password, self.name, self.phone, self.providerNumber, self.type]
    def update(self, add = False):
        cv = csv_manage(self.authority + ".csv")
        if (add == True):
            res = cv.write_data(self.get_line())
            return res 
        else:
            return cv.edit_data([[0, self.email]], self.get_line())