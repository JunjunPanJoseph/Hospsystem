from app.src.login_check import user_check
from app.src.csv_management import csv_manage
import datetime
class Center():
    def __init__(self, type, Abn, name, phone, location):
        self.type = type
        self.Abn = Abn
        self.name = name
        self.phone = phone
        self.location = location
    def check(self):
        cv = csv_manage("health_centres.csv")
        data = cv.search_data([[2, self.name]])
        if data == []:
            return False
        return True
    def save(self):
        cv = csv_manage("health_centres.csv")
        line = [self.type, self.Abn, self.name, self.phone, self.location]
        cv.write_data(line)
class Center_management():
    def get_center(self, centerName):
        cv = csv_manage("health_centres.csv")
        provide_list = cv.search_data([[2, centerName]])
        if provide_list == []:
            return None
        provide_list = provide_list[0]
        return Center(provide_list[0], provide_list[1], provide_list[2], provide_list[3], provide_list[4])
    def get_all_list(self):
        cv = csv_manage("health_centres.csv")
        center_list = cv.get_all_data()
        result = []
        for line in center_list:
            result.append(self.get_center(line[2]))
        return result
    def get_workingTime(self, provider_, center_):
        if (provider_ == None):
            return False
        if (center_ == None):
            return False
        cv = csv_manage("provider_health_centre.csv")
        if (type(provider_) == str or type(provider_) == unicode):
            provider = str(provider_)
        else:
            provider = provider_.email
        if (type(center_) == str or type(center_) == unicode):
            center = str(center)
        else:
            center = center_.name
        time = cv.search_data([[0, provider], [1, center]])
        if (time == []):
            return False
        time = time[0]
        return datetime.datetime.strptime(time[2], '%H:%M:%S'), datetime.datetime.strptime(time[3], '%H:%M:%S')
    def get_provider_list(self, center):
        cv = csv_manage("provider_health_centre.csv")
        provide_list = cv.search_data([[1, center]])
        result = []
        uc = user_check()
        for line in provide_list:
            result.append(uc.get_user(line[0]))
        return result
    def get_center_list(self, provider):
        cv = csv_manage("provider_health_centre.csv")
        center_list = cv.search_data([[0, provider]])
        result = []
        for line in center_list:
            result.append(self.get_center(line[1]))
        return result
    def save(self, provider_email, center_name, start_time, end_time):
        cv = csv_manage("provider_health_centre.csv")
        line = [provider_email, center_name, start_time.strftime('%H:%M:%S'), end_time.strftime('%H:%M:%S')]
        cv.write_data(line)