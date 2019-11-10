from flask import Flask, render_template,session, redirect, url_for, flash,request
from flask_login import LoginManager,login_user, current_user, login_required, logout_user
import datetime
from app import app, login_manager

from flask_login import UserMixin
from app.src.csv_management import csv_manage

import app.src.csv_management as csv_management
import app.src.user_class as user_class
import app.src.login_check as login_check
import app.src.health_center as health_center
import app.src.rating_record as rating_record
import app.src.appointment_record as appointment_record

@login_manager.user_loader
def load_user(user_id):
    uc = login_check.user_check()
    user = uc.get_user(user_id)
    return user
    

    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html', get=True, success = None)
    else:
        username = request.form["username"]
        password_input = request.form["password"]
        uc = login_check.user_check()
        user = uc.check_password(username, password_input)
        if (user != False):
            login_user(user)
            #return render_template("login.html", success = True)
            if (user.authority == "patient"):
                return redirect(url_for("patient"))
            else:
                return redirect(url_for("provider"))
    return render_template("login.html", success = False)
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
def welcome():
    return render_template('welcome.html')
    
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    same_password = None
    success_update = None
    if (request.method == "POST"):
        current_user.password = request.form["new_password"]
        current_user.name = request.form["name"]
        current_user.phone = request.form["phone"]
        success_update = current_user.update()
        
    return render_template('profile.html', current_user = current_user,
     same_password = same_password, success_update = success_update)
@app.route('/provider', methods=['GET', 'POST'])
@login_required
def provider():
    if current_user.authority == "patient":
        return redirect(url_for("patient"))
    rm = appointment_record.record_management()
    data = rm.get_record_by_provider(current_user)
    return render_template("provider.html", data = data,  current_user = current_user)
@app.route('/patient/<name>', methods=['GET', 'POST'])
@login_required
def patient_name(name):
    rm = appointment_record.record_management()
    if (rm.exist_record(name, current_user)):
        data = rm.get_record_by_patient(name)
        return render_template("patient_data.html", data = data)
    else:
        return render_template("patient_data.html", data = [])
@app.route('/edit/<patient>/<provider>/<center>/<start_time>/<end_time>', methods=['GET', 'POST'])
@login_required
def edit_record(patient, provider, center, start_time, end_time):
    if current_user.authority == "patient":
        return redirect(url_for("patient"))
    search_list = [[0, patient], [1,provider], [2,center], [4, start_time], [5,end_time]]
    success = None
    rm = appointment_record.record_management()
    data = rm.search_edit(search_list)
    if request.method == "POST":
        if (data != []):
            if rm.exist_record( data[0].patient, data[0].provider):
                data[0].note = request.form["note"]
                data[0].med = request.form["med"]
                success = rm.update_record(data[0], current_user)
    #return render_template("welcome.html")
    return render_template("edit_appointment.html", data = data, current_user = current_user, success = success)


@app.route('/patient', methods=['GET', 'POST'])
def patient():
    if current_user.authority == "provider":
        return redirect(url_for("provider"))
    cm = health_center.Center_management()
    
    list = cm.get_all_list()
    if request.method == "POST":
        name = request.form["name"]
        type = request.form["type"]
        if type == "name":
            return redirect(url_for("search_name", name = name))
        if type == "suburb":
            return redirect(url_for("search_suburb", name = name))
        if type == "service":
            return redirect(url_for("search_service", name = name))
        if type == "provider":
            return redirect(url_for("search_provider", name = name))
          #  return render_template("patient_welcome.html",name=username)
    else :
        return render_template("patient.html", current_user = current_user, LIST = list, name = current_user.id,  
         authority = current_user.authority, rating = rating_record.Rating_Management())

@app.route('/centres/<name>', methods=['GET', 'POST'])
def centres_list(name):
    cm = health_center.Center_management()
    center_data = cm.get_center(name)
    if (center_data != None):
        provider_data = cm.get_provider_list(center_data.name)
    else:
        provider_data = []
    return render_template("center.html", current_user = current_user, 
     center_data = center_data, provider_data = provider_data, 
     rating = rating_record.Rating_Management(), get_workingTime = cm.get_workingTime)
     

@app.route('/providers/<name>', methods=['GET', 'POST'])
def providers_list(name):

    cm = health_center.Center_management()
    uc = login_check.user_check()
    provider_data = uc.get_user(name)
    if (provider_data != None):
        center_data = cm.get_center_list(provider_data.email)
    else:
        center_data = []
    
    return render_template("providers.html", current_user = current_user, 
     c = center_data, p = provider_data, 
     rating = rating_record.Rating_Management(), get_workingTime = cm.get_workingTime)


@app.route('/book/<name>/<center>', methods=['GET', 'POST'])
@login_required
def book(name, center):
    if current_user.authority == "provider":
        return redirect(url_for("provider"))
    cm = health_center.Center_management()
    uc = login_check.user_check()
    rm = appointment_record.record_management()
    errorMsg = []
    center_data = cm.get_center(center)
    provider_data = uc.get_user(name)
    if (center_data == None):
        errorMsg.append("Center name not exist!")
    if (provider_data == None):
        errorMsg.append("Provider name not exist!")
    if (provider_data.authority == "patient"):
        errorMsg.append("Wrong authority")
    workingTime = cm.get_workingTime(provider_data, center_data)
    if workingTime == False:
        errorMsg.append("The provider are not working for the center")
    bookingMsg = []
    def check_time(timeVal):
        sec = timeVal.strftime('%S')
        min = timeVal.strftime('%M')
        if (sec != "00"):
            return False
        if (min != "00" and min != "30"):
            return False
        return True
    
    if request.method == "POST":
        try:
            r = appointment_record.Record(current_user, provider_data, center_data, request.form["reason"], 
             request.form["start_time"], request.form["end_time"], "", "")
            if (check_time(r.start_time) and check_time(r.end_time)):
                checkValue = rm.update_record(r)
                if (checkValue == False):
                    bookingMsg.append("Can not book appointment - please check your start time and end time")
                else:
                    bookingMsg.append("Booking success!")
            else:
                bookingMsg.append("time are separate to 30min periods!")
        except:
            bookingMsg.append("You need enter time in correct format")
            
    return render_template("booking.html", errorMsg = errorMsg, bookingMsg = bookingMsg, 
     center_data = center_data,
     provider_data = provider_data,
     workingTime = workingTime)

     
@app.route('/rating/center/<center>', methods=['GET', 'POST'])
@login_required
def rating_center(center):
    if current_user.authority == "provider":
        return redirect(url_for("provider"))
    success = None
    cm = health_center.Center_management()
    rm = rating_record.Rating_Management()
    
    if (cm.get_center(center) == None):
        success = False
    else:
        if request.method == "POST":
            val = request.form["rating"]
            
            rating = rating_record.Rating(current_user.email, val, centre = center)
            if (rm.update_rating(rating)):
                success = True
            else:
                success = False
    return render_template("rating.html", current_user = current_user, success = success, 
     currRating = rating_record.Rating_Management().get_rating(current_user.email, centre = center))
     
@app.route('/rating/provider/<center>', methods=['GET', 'POST'])
@login_required
def rating_provider(center):
    if current_user.authority == "provider":
        return redirect(url_for("provider"))
    success = None
    uc = login_check.user_check()
    rm = rating_record.Rating_Management()
    
    if (uc.get_user(center) == None):
        success = False
    else:
        if request.method == "POST":
            val = request.form["rating"]
            
            rating = rating_record.Rating(current_user.email, val, provider = center)
            if (rm.update_rating(rating)):
                success = True
            else:
                success = False
    return render_template("rating.html", current_user = current_user, success = success, 
     currRating = rating_record.Rating_Management().get_rating(current_user.email, centre = center))


@app.route('/search/name/<name>', methods=['GET', 'POST'])
@login_required
def search_name(name):
    provider_data = []
    center_data = []
    f_center = csv_manage("health_centres.csv")
    center_data = f_center.search_data([[2, name]], 0, 1)
    
    cm = health_center.Center_management()
    uc = login_check.user_check()
    class_list_provider = []
    class_list_center = []
    for line in provider_data:
        class_list_provider.append(uc.get_user(line[0]))
    for line in center_data:
        class_list_center.append(cm.get_center(line[2]))
    return render_template("search_result.html", provider_data = class_list_provider, center_data = class_list_center,
     rating = rating_record.Rating_Management(), get_workingTime = cm.get_workingTime)

@app.route('/search/suburb/<name>', methods=['GET', 'POST'])
def search_suburb(name):
    provider_data = []
    center_data = []
    f_center = csv_manage("health_centres.csv")
    center_data = f_center.search_data([[4, name]], 0, 1)
    
    
    cm = health_center.Center_management()
    uc = login_check.user_check()
    class_list_provider = []
    class_list_center = []
    for line in provider_data:
        class_list_provider.append(uc.get_user(line[0]))
    for line in center_data:
        class_list_center.append(cm.get_center(line[2]))
    return render_template("search_result.html", provider_data = class_list_provider, center_data = class_list_center,
     rating = rating_record.Rating_Management(), get_workingTime = cm.get_workingTime)
    
@app.route('/search/service/<name>', methods=['GET', 'POST'])
def search_service(name):
    provider_data = []
    center_data = []
    f_provider = csv_manage("provider.csv")
    provider_data = f_provider.search_data([[2, name]], 0, 1)
    
    cm = health_center.Center_management()
    uc = login_check.user_check()
    class_list_provider = []
    class_list_center = []
    for line in provider_data:
        class_list_provider.append(uc.get_user(line[0]))
    for line in center_data:
        class_list_center.append(cm.get_center(line[2]))
    return render_template("search_result.html", provider_data = class_list_provider, center_data = class_list_center,
     rating = rating_record.Rating_Management(), get_workingTime = cm.get_workingTime)
@app.route('/search/provider/<name>', methods=['GET', 'POST'])
def search_provider(name):
    provider_data = []
    center_data = []
    f_provider = csv_manage("provider.csv")
    provider_data = f_provider.search_data([[0, name]], 0, 1)
    
    cm = health_center.Center_management()
    uc = login_check.user_check()
    class_list_provider = []
    class_list_center = []
    for line in provider_data:
        class_list_provider.append(uc.get_user(line[0]))
    for line in center_data:
        class_list_center.append(cm.get_center(line[2]))
    return render_template("search_result.html", provider_data = class_list_provider, center_data = class_list_center,
     rating = rating_record.Rating_Management(), get_workingTime = cm.get_workingTime)
