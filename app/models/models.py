import datetime
import logging
# from venv import logger
import os
import sys
from pathlib import Path
project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_folder)
from database.db import DbPostgresManager


hospital_db =DbPostgresManager()
hospital_db.create_table()
class User:
    def __init__(self, user_name, user_pass, user_email, user_mobile):
        self.user_name = user_name
        self.user_pass = user_pass
        self.user_email = user_email
        self.user_mobile = user_mobile
        


class Admin(User):
    def __init__(self,user_name, user_pass, user_email, user_mobile):
        User.__init__(self,user_name, user_pass, user_email, user_mobile)

    @classmethod
    def add_new_admin(cls):
        try:
            user_name = input("Please enter a username: ")
            user_pass = input("Please enter a password: ")
            user_email = input("Please enter your email: ")
            user_mobile = input("Please enter your phone: ")
            admin_obj = cls(user_name, user_pass, user_email, user_mobile)
            hospital_db.insert_table("users", [ "user_name","user_pass", "user_email", "user_mobile"],
                      [admin_obj.user_name,admin_obj.user_pass,admin_obj.user_email,admin_obj.user_mobile])
            user_id=hospital_db.select(table_name=["users"], select_options=["user_id"])
            hospital_db.insert_table("admin",["users_user_id"],[user_id])

            print("New admin added successfully!")

        except Exception as e:
            print(f"Error adding a new admin: {str(e)}")


    def list_patients(self):
        hospital_db.select(self, table_name=["users","patients"],
                           on_conditions=[("users.user_id","patients.users_user_id")],
                             join_type = "INNER", printed = True)

    def list_doctors(self):
        hospital_db.select(self, table_name=["users","doctors"],
                           on_conditions=[("users.user_id","doctors.users_user_id")],
                             join_type = "INNER", printed = True)

    

# this class add search ability to doctor and patient class
class Mixinsearch:
    def get_information(self,role)->dict:
        try: 
            name=input("please  name : ")
            role_list=[role]
            role_list.append
            return hospital_db.select(role.role_list.append("users"),
                                      on_conditions=[("users.user_id",f"{role}.users_user_id")],
                                      join_type= "INNER", printed= False)

        except Exception as e:
            print(f"Error retrieving {role} information: {str(e)}")
            return {}
    
class Doctor(User,Mixinsearch):
    def __init__(self,user_name, user_pass_1, user_email, user_mobile,doctor_name , experties, work_experienceit, salary, address, visit_price):
        User.__init__(self,user_name, user_pass_1, user_email, user_mobile)
        self.doctor_name = doctor_name
        self.experties = experties
        self.work_experienceit = work_experienceit
        self.salary = salary
        self.address = address
        self.visit_price = visit_price
        
    @classmethod
    def search_doctor_information(cls):
        dict_information=cls.get_information("doctor")
        if dict_information:
            print(dict_information)
        else:
            print("No doctor information found for the entered name.")
        
           
    def search_income_visit():
        # calculate all income of a doctor
        try :  
            user_name=input("please enter a user name: ")
            user_pass=input("please enter a password: ")
            str_information=hospital_db.select(table_name=["users","doctors","visit_dates"], select_options=["visit_price","count(visit_id)"],
               filter_options= [("users_name","=",f'{user_name}'),("patients_patient_id","IS NOT","NULL")],group_options= ["visit_dates.doctors_doctor_id"],
               on_conditions= [("users.suer_id","doctors.users_user_id"),("doctors.doctor_id","visit_dates.doctors_doctor_id")], join_type= "INNER")
            list_information=str_information.split(", ")
            income=list_information[0]*list_information[1]
            print(income)

        except Exception as e:
            print(f"An error occurred: {e}")


        



class Paient(User,Mixinsearch):
    def __init__(self, user_name, user_pass_1, user_email, user_mobile,patient_name, patient_address):
        User.__init__(self,user_name, user_pass_1, user_email, user_mobile)
        self.patient_name = patient_name
        self.patient_address = patient_address

    @staticmethod
    def show_visit_form():
        try:
            username = input("Please enter your username: ")
            password = input("Please enter your password: ")
            hospital_db.select(table_name=["users","patients","visit_dates","doctors","visit_forms"], 
                               select_options=["visit_forms.visit_form_id","visit_forms.from_name","visit_forms.visit_desc","visit_forms.hospitalization","visit_forms.duration_of_hospitalization","visit_forms.visit_dates_id",'doctors.doctor_name'],
               order_options= ["visit_dates.visit_time"],filter_options=[("users.user_name","=",f"'{username}'")],on_conditions= [("users.user_id","patients.users_user_id"),("patients.patient_id","visit_dates.patients_patient_id"),("visit_dates.doctors_doctor_id","doctors.doctor_id"),("visit_dates.patients_patient_id","patients.patient_id")], join_type= "INNER",printed=True )

        except Exception as e:
            print(f"An error occurred: {e}")

# ==================================================================================================================
    @classmethod
    def get_visit_time(cls):
        try:
            str_empty_time=hospital_db.select(table_name=["visit_dates"], 
            select_options=["visit_time"],
            filter_options=[("patients_patient_id","IS","NULL")],printed=False )
            list_empty_time=str_empty_time.split(", ")
            print(list_empty_time)
            for i in range(len(list_empty_time)):
                print(f"{int(i)+1}-{list_empty_time[i]}")
            time_index=int(input("please enter the number of time that you want to visit"))
            choised_time=list_empty_time[time_index-1]
            user_name=input("Please enter your user name: ")
            id_patient=hospital_db.select(table_name=["patients","users"], 
            select_options=["patients.patient_id"],
            filter_options=[("users.user_name","=",f"{user_name}")],on_conditions=[("users.user_id","patients.users_user_id")], join_type="INNER",printed=False )
            print(id_patient)
            hospital_db.update_table("visit_dates", {"visit_time": f"{choised_time}"}, [("patients_patient_id", "=", id_patient)])
        except Exception as e:
            print(e)


# ==================================================================================================================



    # def cancel_visit_time():
    #     hospital_db.select(table_name=["patients","visit_dates","visit_forms"], 
    #                         on_conditions= [("patients.patient_id","visit_dates.patients_patient_id"),("visit_dates.visit_date_id","Visit_forms.visit_dates.visit_date_id")], join_type= "INNER")
        
    #     input_time = input("Please enter time for canceling visit time : ")
    #     paient_name = input("Please enter your name")   
        
    #     hospital_db.delete_from_table(table_name="visit_form", condition=visit_forms.visit_form_id=)

        

    @classmethod
    def search_patient_information(cls):
        dict_information=cls.get_information("patients")
        if dict_information:
            print(dict_information)
        else:
            print("No patient information found for the entered name.")


    @staticmethod
    def show_visit_time():
        try:
            hospital_db.select(table_name=["visit_dates","doctors"],
                                select_options=["visit_dates.visit_date_id","visit_dates.visit_time","doctors.doctor_name"],
                                filter_options=[("visit_dates.visit_date_id","IS","NULL")],
                                on_conditions=[("visit_dates.doctors_doctor_id","doctors.doctor_id")],
                                join_type= "INNER",printed=True)
        except Exception as e:
            print(e)

        


class Visit_Form:
    def __init__(self, form_name, visit_desc,hospitalization=False, duration_of_hospitalization=0):
        self.form_name = form_name
        self.visit_desc = visit_desc
        self.hospitalization = hospitalization
        self.duration_of_hospitalization = duration_of_hospitalization

    @staticmethod
    def show_number_visit():
            patient_id = input("Please Enter patient_id  : ")
            doctor_id = input("Please Enter doctor_id  : ")
            hospital_db.select(table_name=["visit_dates"], 
                               select_options=["COUNT(visit_id)"],
               filter_options=[("visit_dates.patients_patient_id","=",f"{patient_id}"),("visit_dates.doctors_doctor_id","=",doctor_id)],printed=True )
        


        


    
class Visit_Date:
    def __init__(self,username,password, visit_date_time,patient_id="Null"):
        self.username=username
        self.password=password
        self.visit_date_time = visit_date_time
        self.patient_id = patient_id

    def show_doctor_time():
        user_name = input("Please enter your username: ")
        
        hospital_db.select(table_name=["users","doctors","visit_dates","patients"],
                            select_options=["visit_dates.visit_date_id","visit_dates.visit_time","patients.patient_name"],
                            filter_options=[("users.user_name","=",f"'{user_name}'")],
                            on_conditions=[("users.user_id","doctors.users_user_id"),("doctors.doctor_id","visit_dates.doctors_doctor_id"),("visit_dates.patients_patient_id","patients.patient_id")],
                            join_type= "INNER",printed=True)

        

    # @staticmethod
    # def create_visit_date():
    #     username=input("please enter your username :")
    #     password=input("please enter your password :")
    #     visit_date=input("please enter visit date like '07/01/2019 07:00:00': ")
    #     obj=Visit_Date(username,password, visit_date)
    #     if db.add_visit_time(obj):
    #         print("Adding visit time successfully")
    #     else:
    #         print("please try again!")
    
# ========================================================================================================

    # @classmethod
    # def remove_visit_time():
    #     id_visit_time=input("please enter id_visit_time: ")
    #     if db.remove_visit_time(id_visit_time):
    #         print("Adding visit time successfully")
    #     else:
    #         print("please try again!")




class Paient_Bill():
    def __init__(self, date, total_amount, paient_share, amount_paid, the_remaining_amount, insurance_contribution):
        self.amount_paid = amount_paid
        self.the_remaining_amount = the_remaining_amount
        self.date = date
        self.total_amount = total_amount
        self.paient_share = paient_share
        self.insurance_contribution = insurance_contribution

    def show_bill():
        user_name = input("Please enter your username: ")
        password = input("Please enter your password: ")
        
        hospital_db.select(table_name=["users","patients","patient_bills"], 
                            select_options=["patients.patient_name","patient_bills.date","patient_bills.patient_share","patient_bills.amount_paid","patient_bills.the_remaining_amount","patient_bills.insurance_contribution"],
                            filter_options=[("users.user_name","=",f"'{user_name}'")],
                            on_conditions= [("users.user_id","patients.users_user_id"),("patients.patient_id","patient_bills.patients_patient_id")], join_type= "INNER",printed=True)
        


    def show_income_hospital():

        hospital_db.select(table_name=["patient_bills"], select_options=["SUM(amount_paid)"], printed=True)



    
    @classmethod
    def calculate_total_income(cls):
        try:
            hospital_db.select(table_name=["patient_bills"], 
            select_options=["sum(amount_paid)"],
            printed=True )

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    
    
    

class Medical_Record():
    def __init__(self,record_id, record_date):
        self.record_id = record_id
        self.record_date = record_date

   

    def display_visit_history(self):
        user_name = input("Please Enter your username : ")
        
        hospital_db.select(table_name=["patients","visit_dates","doctors","visit_forms"], 
                            select_options=["visit_forms.form_id","visit_forms.medical_record_record_id","visit_forms.visit_form_name","visit_forms.visit_desc","visit_forms.hospitalization","visit_forms.duration_of_hospitalization","doctors.doctor_name"],
                            filter_options=[("patients.patient_id","=",f"{user_name}")],
                            on_conditions= [("patients.patient_id","visit_dates.patient_patient_id"),("visit_dates.doctors_doctor_id","doctors.doctor_id"),("visit_dates.visit_id","visit_forms.visit_dates_id")], join_type= "INNER",printed=True)



def show_log_info():
    parent_path = os.getcwd()
    path_windows=os.path.join(parent_path,"app\\logging\\log_error" + ".txt")
    path_vs=path_windows.replace("\\","/")
    os.system(f"notepad.exe {path_vs}")

def show_log_error():
   parent_path = os.getcwd()
   path_windows=os.path.join(parent_path,"app\\logging\\log_info" + ".txt")
   path_vs=path_windows.replace("\\","/")
   os.system(f"notepad.exe {path_vs}")

   first_admin=Admin("fariba","123","fariba@gmail.com",9123546845)
   first_doctor=Doctor("fariba","123","fariba@gmail.com",91263087458,"rezaei","general","20",600,"london",14)
   first_patient=Paient("shayan","564","shayan@gmail.com",9374586578,"shayan","toronto",)
   first_admin.list_patients()
   first_admin.list_doctors()
   first_doctor.search_income_visit()
   first_patient.show_visit_form()