import csv
prefix = "app/src/"
class csv_manage():
    def __init__(self, filename):
        self.filename = prefix +filename
        #print(self.filename)
    def get_all_data(self):
        with open(self.filename, "r") as f:
            reader = csv.reader(f)
            data = []
            for line in reader:
                data.append(line)
            return data
        print("can not open file %s%d", self.filename)
        return False
    def write_data(self, data):
        with open(self.filename, "a", newline='') as f:
            writer = csv.writer(f)
            #print(data)
            writer.writerow(data)
            return True
        print("can not open file %s%d", self.filename)
        return False
    def search_data(self, data, same = 1, case_insensitive = 0):
        #data: [[index1, data1], [index2, data2]]
        lines = self.get_all_data()
        result = []
        for ori_line in lines:
            add = 1
            
            if (case_insensitive):
               line = []
               for x in ori_line:
                    line.append(x.lower())
            else:
               line = ori_line
            for check in data:

               if (case_insensitive):
                   compare = check[1].lower()
               else:
                   compare = check[1]
               if same == 1:
                   if line[check[0]] != compare:
                        add = 0
               else :
                    if compare not in line[check[0]]:
                        add = 0
            if add == 1:
                result.append(ori_line)
        return result
    def edit_data(self,search_data, new_line):
        datalist = self.get_all_data()
        for i in range(len(datalist)):
            find = 1
            for check in search_data:
               if datalist[i][check[0]] != check[1]:
                    find = 0
            if find == 1:
                datalist[i] = new_line
                with open(self.filename, "w", newline='') as f:
                    writer = csv.writer(f)
                    for line in datalist:
                        writer.writerow(line)
                    return True
                print("can not open file %s%d", self.filename)
                return False
        return False