from app.src.csv_management import csv_manage

class Rating():
    def __init__(self, patient, level, provider = None, centre = None):
        self.patient = patient
        self.level = level
        self.provider = provider
        self.centre = centre
    def get_list(self):
        tmp = []
        if self.patient != None:
            tmp.append(self.patient)
        if self.provider != None:
            tmp.append(self.provider)
        if self.centre != None:
            tmp.append(self.centre)
        tmp.append(self.level)
        return tmp
class Rating_Management():
    def update_rating(self, rating):
        cs = csv_manage("rating.csv")
        add_list = [[0, rating.patient]]
        if rating.provider != None:
            add_list.append([1, rating.provider])
        if rating.centre != None:
            add_list.append([1, rating.centre])
            
        if (cs.search_data(add_list) != []):
            return cs.edit_data(add_list, rating.get_list())
        else:
            return cs.write_data(rating.get_list())
        
    def get_rating(self, patient = None, provider = None, centre = None):
        cs = csv_manage("rating.csv")
        add_list = []
        if patient != None:
            add_list.append([0, patient])
        if provider != None:
            add_list.append([1, provider])
        if centre != None:
            add_list.append([1, centre])
        search_result = cs.search_data(add_list)
        average = 0
        if (search_result == []):
            return 5
            
        for line in search_result:
            average = average + int(line[2])
        average = average / len(search_result)
        return average
        