import datetime

import app.src.csv_management as csv_management
import app.src.user_class as user_class
import app.src.login_check as login_check
import app.src.health_center as health_center
import app.src.rating_record as rating_record
import app.src.appointment_record as appointment_record
import os 

REMOVE_FILE = False
csv_management.prefix = ""
csv_management.prefix = "test"
open(csv_management.prefix + "record.csv","w+").close()
open(csv_management.prefix + "rating.csv","w+").close()
open(csv_management.prefix + "provider_health_centre.csv","w+").close()
open(csv_management.prefix + "provider.csv","w+").close()
open(csv_management.prefix + "patient.csv","w+").close()
open(csv_management.prefix + "health_centres.csv","w+").close()

if (True):
    record = csv_management.csv_manage("record.csv")
    rating = csv_management.csv_manage("rating.csv")
    provider_health_centre = csv_management.csv_manage("provider_health_centre.csv")
    provider = csv_management.csv_manage("provider.csv")
    patient = csv_management.csv_manage("patient.csv")
    health_centres = csv_management.csv_manage("health_centres.csv")

    new_patient0 = user_class.Patient("patient_0@gmail.com", "123456", "Mark", "0456789", "1234567")
    flag = new_patient0.update(add = True)
    new_provider0 = user_class.Provider("provider_0@gmail.com", "123456", "Mark", "0456789", "1234567", "GP")
    new_provider0.update(add = True)

    print(type(new_patient0))

    new_patient1 = user_class.Patient("patient_A@gmail.com", "123456", "Mark", "0456789", "1234567")
    new_patient1.update(add = True)
    new_provider1 = user_class.Provider("provider_A@gmail.com", "123456", "Mark", "0456789", "1234567", "GP")
    new_provider1.update(add = True)

    new_patient2 = user_class.Patient("patient_B@gmail.com", "123456", "Mark", "0456789", "1234567")
    new_patient2.update(add = True)
    new_provider2 = user_class.Provider("provider_B@gmail.com", "123456", "Mark", "0456789", "1234567", "GP")
    new_provider2.update(add = True)

    new_center1 = health_center.Center("Hospital", "1111", "Sydney Children Hospital", "93821111", "Randwick")
    new_center1.save()
    new_center2 = health_center.Center("Hospital", "1112", "Hospital1", "93821112", "Randwick")
    new_center2.save()
    new_center3 = health_center.Center("Hospital", "1113", "Hospital2", "93821113", "Randwick")
    new_center3.save()

cm = health_center.Center_management()
cm.save("provider_0@gmail.com", "Hospital1", 
 datetime.datetime.strptime("05:00:00", "%H:%M:%S"),
 datetime.datetime.strptime("07:00:00", "%H:%M:%S"))
cm.save("provider_A@gmail.com", "Hospital1", 
 datetime.datetime.strptime("06:00:00", "%H:%M:%S"),
 datetime.datetime.strptime("8:30:00", "%H:%M:%S"))
cm.save("provider_B@gmail.com", "Hospital1", 
 datetime.datetime.strptime("11:00:00", "%H:%M:%S"),
 datetime.datetime.strptime("18:30:00", "%H:%M:%S"))

cm.save("provider_0@gmail.com", "Hospital2", 
 datetime.datetime.strptime("09:00:00", "%H:%M:%S"),
 datetime.datetime.strptime("12:00:00", "%H:%M:%S"))
 
def test_login_check():
    uc = login_check.user_check()
    #test1: not exist
    assert(uc.get_user("120@xx.com") == None)
    #test2: exist patient
    test_patient1 = uc.get_user("patient_A@gmail.com")
    assert(test_patient1.email == "patient_A@gmail.com")
    assert(test_patient1.password == "123456")
    assert(test_patient1.name == "Mark")
    assert(test_patient1.phone == "0456789")
    assert(test_patient1.authority == "patient")
    assert(test_patient1.cardNumber == "1234567")
    #test3: exist provider
    test_provider1 = uc.get_user("provider_A@gmail.com")
    assert(test_provider1.email == "provider_A@gmail.com")
    assert(test_provider1.password == "123456")
    assert(test_provider1.name == "Mark")
    assert(test_provider1.phone == "0456789")
    assert(test_provider1.authority == "provider")
    assert(test_provider1.providerNumber == "1234567")
    assert(test_provider1.type == "GP")
    #test3: check password for not exist user
    assert(uc.check_password("abcd", "123") == False)
    #test4: check exist user with not exist password
    assert(uc.check_password("patient_A@gmail.com", "") == False)
    #test5: check exist user with wrong password
    assert(uc.check_password("patient_A@gmail.com", "6432") == False)
    #test6: check exist user with right password
    test_patient1 = uc.check_password("patient_A@gmail.com", "123456")
    assert(test_patient1.email == "patient_A@gmail.com")
    assert(test_patient1.password == "123456")
    assert(test_patient1.name == "Mark")
    assert(test_patient1.phone == "0456789")
    assert(test_patient1.authority == "patient")
    assert(test_patient1.cardNumber == "1234567")

def test_user_class_check():
    uc = login_check.user_check()
    #test1: edit patient information
    new_patient1 = user_class.Patient("patient_A@gmail.com", "654321", "MarkGay", "0498765", "7654321")
    new_patient1.update()
    test_patient1 = uc.get_user("patient_A@gmail.com")
    assert(test_patient1.email == "patient_A@gmail.com")
    assert(test_patient1.password == "654321")
    assert(test_patient1.name == "MarkGay")
    assert(test_patient1.phone == "0498765")
    assert(test_patient1.authority == "patient")
    assert(test_patient1.cardNumber == "7654321")
    #test2: edit provider information
    new_provider1 = user_class.Provider("provider_A@gmail.com", "654321", "MarkGay", "0498765", "7654321", "PG")
    new_provider1.update()
    test_provider1 = uc.get_user("provider_A@gmail.com")
    assert(test_provider1.email == "provider_A@gmail.com")
    assert(test_provider1.password == "654321")
    assert(test_provider1.name == "MarkGay")
    assert(test_provider1.phone == "0498765")
    assert(test_provider1.authority == "provider")
    assert(test_provider1.providerNumber == "7654321")
    assert(test_provider1.type == "PG")

def test_health_center():
    #test: Center
    #test1: not exist center name
    test_center1 = health_center.Center("Hospital", "1111", "pital", "93821111", "Randwick")
    assert(test_center1.check() == False)
    #test2: right center name
    test_center2 = health_center.Center("Hospital", "1111", "Sydney Children Hospital", "93821111", "Randwick")
    assert(test_center2.check() == True)
    
    #test: Center_management
    #test1: get not exist center
    assert(cm.get_center("ABCDE") == None)
    #test2: exist center
    test_center1 = cm.get_center("Sydney Children Hospital")
    
    assert(test_center1.type == "Hospital")
    assert(test_center1.Abn == "1111")
    assert(test_center1.name ==  "Sydney Children Hospital")
    assert(test_center1.phone == "93821111")
    assert(test_center1.location == "Randwick")
    
    #test: get_workingTime
    #test1: not exist name
    assert(cm.get_workingTime("ABCDE", "abc") == False)
    assert(cm.get_workingTime("provider_0@gmail.com", "abc") == False)
    assert(cm.get_workingTime("ABCDE", "Hospital1") == False)
    #test2: exist time
    test_time1 = cm.get_workingTime("provider_0@gmail.com", "Hospital1")
    assert(test_time1[0].strftime('%H:%M:%S') == "05:00:00")
    assert(test_time1[1].strftime('%H:%M:%S') == "07:00:00")
    #test: providerlist
    #test1:not exist
    assert(cm.get_provider_list("ase") == [])
    #test2: exist
    test_provider_list1 = cm.get_provider_list("Hospital1")
    assert(len(test_provider_list1) == 3)
    assert(test_provider_list1[0].email == "provider_0@gmail.com")
    assert(test_provider_list1[1].email == "provider_A@gmail.com")
    assert(test_provider_list1[2].email == "provider_B@gmail.com")
    #test: get_center_list
    #test1:not exist
    assert(cm.get_center_list("ase") == [])
    #test2: exist
    test_center_list1 = cm.get_center_list("provider_0@gmail.com")
    assert(len(test_center_list1) == 2)
    assert(test_center_list1[0].name == "Hospital1")
    assert(test_center_list1[1].name == "Hospital2")
    
def test_rating_record():
    #test: Rating_Management
    #test1: default
    rm = rating_record.Rating_Management()
    assert(rm.get_rating(provider = "provider_0@gmail.com") == 5)
    assert(rm.get_rating(centre = "Hospital1") == 5)
    #test2: adding rating to same center / provider
    test_rating1 = rating_record.Rating("patient_0@gmail.com", 4, provider = "provider_0@gmail.com")
    rm.update_rating(test_rating1)
    assert(rm.get_rating(patient = "patient_0@gmail.com", provider = "provider_0@gmail.com") == 4)
    test_rating2 = rating_record.Rating("patient_0@gmail.com", 2, provider = "provider_0@gmail.com")
    rm.update_rating(test_rating2)
    assert(rm.get_rating(patient = "patient_0@gmail.com", provider = "provider_0@gmail.com") == 2)
    
    test_rating3 = rating_record.Rating("patient_0@gmail.com", 4, centre = "Hospital1")
    rm.update_rating(test_rating3)
    assert(rm.get_rating(patient = "patient_0@gmail.com",  centre = "Hospital1") == 4)
    test_rating4 = rating_record.Rating("patient_0@gmail.com", 2, centre = "Hospital1")
    rm.update_rating(test_rating4)
    assert(rm.get_rating(patient = "patient_0@gmail.com", centre = "Hospital1") == 2)
    
    #test 3:average rating
    test_rating5 = rating_record.Rating("patient_A@gmail.com", 5, centre = "Hospital1")
    rm.update_rating(test_rating5)
    assert(rm.get_rating(centre = "Hospital1") == 3.5)
    
    test_rating6 = rating_record.Rating("patient_A@gmail.com", 4, provider = "provider_0@gmail.com")
    rm.update_rating(test_rating6)
    assert(rm.get_rating(provider = "provider_0@gmail.com") == 3)
 
def test_appointment_record():
    #test: Record class
    ar = appointment_record
    rec = ar.Record
    rm = appointment_record.record_management()
    user = login_check.user_check().get_user
    center = health_center.Center_management().get_center
    #test1: right data
    new_record1 = rec( user("patient_0@gmail.com"),user("provider_0@gmail.com"), center("Hospital1"), 
     "test", ar.strToTime("8-11-2018 05:00:00"), ar.strToTime("8-11-2018 07:00:00"))
    assert(new_record1.check() == True)
    assert(new_record1.write_check() == True)
    if (True):
        #test2: wrong patient name
        new_record2 = rec( user("pd"),user("provider_0@gmail.com"), center("Hospital1"), 
         "test", ar.strToTime("8-11-2018 05:00:00"), ar.strToTime("8-11-2018 07:00:00"))
        assert(new_record2.check() == False)
        assert(new_record2.write_check() == False)
        #test3 wrong provider name
        new_record3 = rec( user("patient_0@gmail.com"),user("com"), center("Hospital1"), 
         "test", ar.strToTime("8-11-2018 05:00:00"), ar.strToTime("8-11-2018 07:00:00"))
        assert(new_record3.check() == False)
        assert(new_record3.write_check() == False)
        #test4 wrong center name
        new_record4 = rec( user("patient_0@gmail.com"),user("provider_0@gmail.com"), center("Ho"), 
         "test", ar.strToTime("8-11-2018 05:00:00"), ar.strToTime("8-11-2018 07:00:00"))
        assert(new_record4.check() == False)
        assert(new_record4.write_check() == False)
        #test5 start time > end time
        new_record5 = rec( user("patient_0@gmail.com"),user("provider_0@gmail.com"), center("Hospital1"), 
         "test", ar.strToTime("8-11-2018 07:00:00"), ar.strToTime("8-11-2018 05:00:00"))
        assert(new_record5.check() == False)
        assert(new_record5.write_check() == False)
        #test6 not same year
        new_record6 = rec( user("patient_0@gmail.com"),user("provider_0@gmail.com"), center("Hospital1"), 
         "test", ar.strToTime("8-11-2018 05:00:00"), ar.strToTime("8-11-2019 07:00:00"))
        assert(new_record6.check() == False)
        assert(new_record6.write_check() == False)
        #test7 not in provider valid time
        new_record7 = rec( user("patient_0@gmail.com"),user("provider_0@gmail.com"), center("Hospital1"), 
         "test", ar.strToTime("8-11-2018 02:00:00"), ar.strToTime("8-11-2018 07:00:00"))
        assert(new_record7.check() == False)
        assert(new_record7.write_check() == False)
        #test10: previous record
        new_record10 = rec( user("patient_0@gmail.com"),user("provider_0@gmail.com"), center("Hospital1"), 
         "test", ar.strToTime("8-11-2017 05:00:00"), ar.strToTime("8-11-2017 07:00:00"))
        assert(new_record10.check() == True)
        assert(new_record10.write_check() == False)
        #test: save valid record
        assert(rm.update_record(new_record1) == True)
        assert(rm.search_edit([[0, "patient_0@gmail.com"], [1,"provider_0@gmail.com"], [2, "Hospital1"]]) != [])
        #test9 overlap with saved record
        new_record9 = rec( user("patient_0@gmail.com"),user("provider_0@gmail.com"), center("Hospital1"), 
         "test", ar.strToTime("8-11-2018 06:30:00"), ar.strToTime("8-11-2018 07:00:00"))
        assert(new_record9.check() == True)
        assert(new_record9.write_check() == False)
    #test: record_management
    #test: exist record
    #exist
    assert(rm.exist_record(user("patient_0@gmail.com"),user("provider_0@gmail.com")) == True)
    #not exist
    assert(rm.exist_record(user("patient_A@gmail.com"),user("provider_0@gmail.com")) == False)
    assert(rm.exist_record(user("patient_0@gmail.com"),user("provider_A@gmail.com")) == False)
    #test: update sucess
    new_record1 = rec( user("patient_0@gmail.com"),user("provider_0@gmail.com"), center("Hospital1"), 
     "test", ar.strToTime("8-11-2018 05:00:00"), ar.strToTime("8-11-2018 07:00:00"),"some text", "some text")
    assert(rm.update_record(new_record1) == True)
    test_record1 = rm.get_record_by_provider(user("provider_0@gmail.com"))
    assert(test_record1[0].get_list() == new_record1.get_list())
    
    new_record2 = rec( user("patient_A@gmail.com"),user("provider_0@gmail.com"), center("Hospital1"), 
     "test", ar.strToTime("9-11-2018 05:00:00"), ar.strToTime("9-11-2018 07:00:00"),"some text", "some text")
    assert(rm.update_record(new_record2) == True)
    new_record3 = rec( user("patient_0@gmail.com"),user("provider_A@gmail.com"), center("Hospital1"), 
     "test", ar.strToTime("9-11-2018 06:00:00"), ar.strToTime("9-11-2018 07:00:00"),"some text", "some text")
    assert(rm.update_record(new_record3) == True)
    new_record4 = rec( user("patient_0@gmail.com"),user("provider_0@gmail.com"), center("Hospital2"), 
     "test", ar.strToTime("10-11-2018 09:30:00"), ar.strToTime("10-11-2018 10:00:00"),"some text", "some text")
    print( new_record4.get_list())
    print( new_record4.check())
    print( new_record4.write_check())
    assert(rm.update_record(new_record4) == True)
    new_record1 = rec( user("patient_0@gmail.com"),user("provider_0@gmail.com"), center("Hospital1"), 
     "test", ar.strToTime("8-11-2018 05:00:00"), ar.strToTime("8-11-2018 07:00:00"),"some tsdext", "some adtext")
    assert(rm.update_record(new_record1, user("provider_0@gmail.com")) == True)
    test_record1 = rm.get_record_by_provider(user("provider_0@gmail.com"))
    assert(test_record1[0].get_list() == new_record1.get_list())
    #test: update a record which have different provider (False
    assert(rm.update_record(new_record1, user("provider_A@gmail.com")) == False)
    test_record1 = rm.get_record_by_provider(user("provider_0@gmail.com"))
    assert(test_record1[0].get_list() == new_record1.get_list())
    #test:get_record_by_patient
    #not exist
    assert(rm.get_record_by_patient(user("patient_B@gmail.com")) == [])
    #exist
    test_patient_data = rm.get_record_by_patient(user("patient_0@gmail.com"))
    assert(len(test_patient_data) == 3)
    assert(test_patient_data[0].get_list() == new_record1.get_list())
    assert(test_patient_data[1].get_list() == new_record3.get_list())
    assert(test_patient_data[2].get_list() == new_record4.get_list())
    #test:get_record_by_provider
    #not exist
    assert(rm.get_record_by_provider(user("provider_B@gmail.com")) == [])
    #exist
    test_provider_data = rm.get_record_by_provider(user("provider_0@gmail.com"))
    assert(len(test_provider_data) == 3)
    assert(test_provider_data[0].get_list() == new_record1.get_list())
    assert(test_provider_data[1].get_list() == new_record2.get_list())
    assert(test_provider_data[2].get_list() == new_record4.get_list())
    #test:get_record_by_center
    #not exist
    assert(rm.get_record_by_center(center("Sydney Children Hospital")) == [])
    #exist
    test_center_data = rm.get_record_by_center(center("Hospital1"))
    assert(len(test_center_data) == 3)
    assert(test_center_data[0].get_list() == new_record1.get_list())
    assert(test_center_data[1].get_list() == new_record2.get_list())
    assert(test_center_data[2].get_list() == new_record3.get_list())

if (REMOVE_FILE):
    def test_clearn_test_file():
        os.remove(csv_management.prefix + "record.csv")
        os.remove(csv_management.prefix + "rating.csv")
        os.remove(csv_management.prefix + "provider_health_centre.csv")
        os.remove(csv_management.prefix + "provider.csv")
        os.remove(csv_management.prefix + "patient.csv")
        os.remove(csv_management.prefix + "health_centres.csv")
