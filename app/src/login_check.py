from flask_login import LoginManager,login_user, current_user, login_required, logout_user
from app.src.user_class import Patient, Provider
from app.src.csv_management import csv_manage

class user_check():
    def get_user(self,user_id):
        patient = csv_manage("patient.csv")
        data_patient = patient.search_data([[0, user_id]])
        if data_patient != []:
            data_patient = data_patient[0]
            user = Patient(data_patient[0], data_patient[1], data_patient[2], data_patient[3], data_patient[4])
            return user
        provider = csv_manage("provider.csv")
        data_provider = provider.search_data([[0, user_id]])
        if data_provider != []:
            data_provider = data_provider[0]
            user = Provider(data_provider[0], data_provider[1], data_provider[2], data_provider[3], data_provider[4], data_provider[5])
            return user
        return None
    '''
    def check_user_password(self, user):
        check = csv_manage(user.authority + ".csv")
        search_result = check.search_data([[0, user.email], [1, user.password]])
        if (search_result != []):
            return True
        return False
    '''
    def check_password(self, user_id, password):
        user = self.get_user(user_id)
        if user == None:
            return False
        if (user.password != password):
            return False
        return user
        '''
        patient = csv_manage("patient.csv")
        data_patient = patient.search_data([[0, user_id], [1, password]])
        provider = csv_manage("provider.csv")
        data_provider = provider.search_data([[0, user_id], [1, password]])
        if (data_patient != [] ):
            user = User(user_id)
            login_user(user)
            return True
        '''