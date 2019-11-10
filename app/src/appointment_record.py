from app.src.csv_management import csv_manage
from app.src.login_check import user_check
from app.src.health_center import Center_management
import datetime
def strToTime(timestr):
    return datetime.datetime.strptime(timestr, '%d-%m-%Y %H:%M:%S')

class Record():
    def __init__(self, patient, provider, center, reason, start_time, end_time, note = "", med =""):
        self.patient = patient
        self.provider = provider
        self.center = center
        self.reason = reason
        if (type(start_time) == str):
            self.start_time = datetime.datetime.strptime(start_time, '%d-%m-%Y %H:%M:%S')
        else:
            self.start_time = start_time
        if (type(end_time) == str):
            self.end_time = datetime.datetime.strptime(end_time, '%d-%m-%Y %H:%M:%S')
        else:
            self.end_time = end_time
        self.note = note
        self.med = med
    def get_list(self):
        return [self.patient.email, self.provider.email, self.center.name,
         self.reason, self.start_time.strftime('%d-%m-%Y %H:%M:%S'), 
         self.end_time.strftime('%d-%m-%Y %H:%M:%S'),
         self.note, self.med]
    def check(self):
        if (self.patient == None or self.provider == None or self.center == None):
            print("None error")
            return False
        if (self.end_time <= self.start_time):
            print("end time <start time")
            return False
        
        if self.start_time.date() != self.end_time.date():
            print("start %s end %s not same date"%( self.start_time.date(),  self.end_time.date()))
            return False
        cm = Center_management()
        record = cm.get_workingTime(self.provider, self.center)
        if record == False:
            print("working time false")
            return False
        if record[0].time() > self.start_time.time() or record[1].time() < self.end_time.time():
            
            print("time false")
            print(self.get_list())
            print("record %s-%s"%(record[0].time(), record[1].time()))
            print("self %s-%s"%(self.start_time.time(), self.end_time.time()))
            return False
        return self.patient.check() and self.provider.check() and self.center.check()
    def write_check(self):
        if (self.check() == False):
            return False
        cv = csv_manage("record.csv")
        search_list = [[1, self.provider.email]]
        result = cv.search_data(search_list)
        overlap_time = 0
        for line in result:

            line_start_time = datetime.datetime.strptime(line[4], '%d-%m-%Y %H:%M:%S')
            line_end_time = datetime.datetime.strptime(line[5], '%d-%m-%Y %H:%M:%S')
            if (self.start_time <= line_start_time and self.end_time >= line_start_time):
                overlap_time = 1
            if  (self.start_time <= line_end_time and self.end_time >= line_end_time):
                overlap_time = 1
            if  (self.start_time >= line_start_time and self.end_time <= line_end_time):
                overlap_time = 1
            if overlap_time == 1:
                print("overlap_time fail")
                print(self.get_list())
                print("line_start: %s line_end: %s"%(datetime.datetime.strptime(line[4], '%d-%m-%Y %H:%M:%S'), datetime.datetime.strptime(line[5], '%d-%m-%Y %H:%M:%S')))
                print("self start: %s, self end : %s"%(self.start_time, self.end_time))
                print("---")
                return False
            

        if datetime.datetime.now() > self.start_time:
            return False
        return True
    
class record_management():
    def exist_record(self, patient, provider):
        if (patient == None):
            return False
        if (provider == None):
            return False
        cv = csv_manage("record.csv")
        search_list = []
        if (type(patient) == str):
            search_list.append([0, patient])
        else:
            search_list.append([0, patient.email])
            
        if (type(provider) == str):
            search_list.append([1, provider])
        else:
            search_list.append([1, provider.email])
        result = cv.search_data(search_list)
        if result == []:
            return False
        else:
            return True
    def update_record(self, record, provider = None):
        if record.check() == False:
            return False
        if provider != None:
            if provider.email != record.provider.email:
                return False
        cv = csv_manage("record.csv")
        search_list = [[0, record.patient.email],[1, record.provider.email], 
         [2, record.center.name], [4, record.start_time.strftime('%d-%m-%Y %H:%M:%S')], 
         [5, record.end_time.strftime('%d-%m-%Y %H:%M:%S')]]
        result = cv.search_data(search_list)
        if result == []:
            if record.write_check() == False:
                return False
            cv.write_data(record.get_list())
        else:
            cv.edit_data(search_list, record.get_list())
        return True

    def search_edit(self, search_list):
        cv = csv_manage("record.csv")
        uc = user_check()
        cm = Center_management()
        result = cv.search_data(search_list)
        return_list = []
        for line in result:
            return_list.append(Record(uc.get_user(line[0]), uc.get_user(line[1]), cm.get_center(line[2]),line[3], 
             datetime.datetime.strptime(line[4], '%d-%m-%Y %H:%M:%S'),
             datetime.datetime.strptime(line[5], '%d-%m-%Y %H:%M:%S'), 
             line[6], line[7]))
        return return_list
    def get_record_by_patient(self, patient):
        if patient == None:
            return False
        if type(patient) == str:
            search_list = [[0, patient]]
        else:
            search_list = [[0, patient.email]]
        return self.search_edit(search_list)
    def get_record_by_provider(self, provider):
        if provider == None:
            return False
        if type(provider) == str:
            search_list = [[1, provider]]
        else:
            search_list = [[1,  provider.email]]
        
        return self.search_edit(search_list)
    def get_record_by_center(self, center):
        if center == None:
            return False
        if type(center) == str or type(center) == unicode:
            search_list = [[2, str(center)]]
        else:
            search_list = [[2,  center.name]]
        return self.search_edit(search_list)
        