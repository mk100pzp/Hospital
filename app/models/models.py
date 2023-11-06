import datetime
import logging
from venv import logger
import os
import sys
from pathlib import Path
project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_folder)
from database.db import DbPostgresManager


hospital_db =DbPostgresManager()
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
            logger.error(f"Error adding a new admin: {str(e)}")


    def list_patients(self):
        hospital_db.select(self, table_name=["users","patients"],
                           on_conditions=[("users.user_id","patients.users_user_id")],
                             join_type = "INNER JOIN", printed = True)

    def list_doctors(self):
        hospital_db.select(self, table_name=["users","doctors"],
                           on_conditions=[("users.user_id","doctors.users_user_id")],
                             join_type = "INNER JOIN", printed = True)

    

# this class add search ability to doctor and patient class
class Mixinsearch:
    def get_information(self,role)->dict:
        try: 
            name=input("please  name : ")
            dict_information=db.Database.search_database_information(role,name)
            return dict_information

        except Exception as e:
            logger.error(f"Error retrieving {role} information: {str(e)}")
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
            print(f"""
            user id= {dict_information['user_id']}
            user name= {dict_information['user_name']}
            user password= {dict_information['user_pass']}
            user email= {dict_information['user_email']}
            user mobile= {dict_information['user_mobile']}
            doctor id= {dict_information['doctor_id']}
            expertis= {dict_information['expertis']}
            work exprienceit= {dict_information['work_experienceit']}
            salary= {dict_information['salary']}
            address= {dict_information['address']}
            visit price= {dict_information['visit_price']}
            """)

        else:
            print("No doctor information found for the entered name.")
        
           
    def search_income_visit():
        # calculate all income of a doctor
        try :  
            user_name=input("please enter a user name: ")
            user_pass=input("please enter a password: ")
            str_information=hospital_db.select_table(table_name=["users"], select_options=["visit_price","count(visit_id)"],
                filter_options=["users_name","=",user_name,"patients_patient_id","IS NOT"," NULL"],group_options=["visit_dates.doctors_doctor_id"],
               join_query="JOIN doctors ON users.user_id = doctors.users_user_id JOIN visit_date ON visit_dates.doctors_doctor_id = doctors.doctor_id   ;")
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
            visit_form = db.search_visit_form(username, password)
            if visit_form:
                print("Visit Form Information:")
                for key, value in visit_form.items():
                    print(f"{key}: {value}")
            else:
                print("Visit Form not found.")

        except Exception as e:
            print(f"An error occurred: {e}")


    @classmethod
    def get_visit_time(cls):
        try:
            dict_time = db.search_empty_time()
            for num, time in dict_time.items():
                print(num, ":", time)
            choice_num = input("Please enter a number to get: ")
            
            if choice_num in dict_time:
                dict_choice_time = dict_time[choice_num]
                visit_id = dict_choice_time["visit_id"]
                user_name = input("Please enter your username: ")
                password = input("Please enter your password: ")
                
                if db.save_visit_time(visit_id, user_name, password):
                    print("Your visit time is saved.")
                else:
                    print("Sorry, please try again later.")
            else:
                print("Please enter the right number.")
                cls.get_visit_time()

        except Exception as e:
            print(f"An error occurred: {e}")


    def cancel_visit_time():
        id_visit=input("Please enter id of your visit time")
        if db.cancel_visit_time(id_visit):
            print("your visit time cancelled! ")
        else:
            print("please try again later")
        
    @classmethod
    def search_patient_information(cls):
        # creat patient obj with input information then call show_patient_information from database module
        dict_information=cls.get_information()
        try:
            print(f"""
            user id= {dict_information['user_id']}
            user name= {dict_information['user_name']}
            user password= {dict_information['user_pass']}
            user email= {dict_information['user_email']}
            user mobile= {dict_information['user_mobile']}
            patient id= {dict_information['patient_id']}
            patient name= {dict_information['patient_name']}
            patient address= {dict_information['patient_address']}
            """)

        except KeyError:
            print("there isn't any doctor for entered name :")
    @classmethod
    def show_visit_time():
        user_name = input("Please enter your username: ")
        password = input("Please enter your password: ")
        dict_time=db.Database.cached_visit_time(user_name,password)
        print(dict_time)
        


class Visit_Form:
    def __init__(self, form_name, visit_desc,hospitalization=False, duration_of_hospitalization=0):
        self.form_name = form_name
        self.visit_desc = visit_desc
        self.hospitalization = hospitalization
        self.duration_of_hospitalization = duration_of_hospitalization

    @staticmethod
    def show_number_visit():
        doctor_id = input("Please enter doctor id : ")
        patient_id = input("Please enter patient id : ")
        dict_visit=db.Database.search_number_visit(doctor_id,patient_id)
        print(dict_visit)


        

    
    
class Visit_Date:
    def __init__(self,username,password, visit_date_time,patient_id="Null"):
        self.username=username
        self.password=password
        self.visit_date_time = visit_date_time
        self.patient_id = patient_id

    @staticmethod
    def create_visit_date():
        username=input("please enter your username :")
        password=input("please enter your password :")
        visit_date=input("please enter visit date like '07/01/2019 07:00:00': ")
        obj=Visit_Date(username,password, visit_date)
        if db.add_visit_time(obj):
            print("Adding visit time successfully")
        else:
            print("please try again!")
    
    @classmethod
    def remove_visit_time():
        id_visit_time=input("please enter id_visit_time: ")
        if db.remove_visit_time(id_visit_time):
            print("Adding visit time successfully")
        else:
            print("please try again!")




class Paient_Bill:
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
        dict_bill=db.Database.search_bill(user_name, password)
        print(dict_bill)

    def show_income_hospital():
        income=db.Database.search_income()
        print(income)


    
    @classmethod
    def calculate_total_income(cls, time_frame):
        try:
            current_date = datetime.now()
            if time_frame == "daily":
                start_date = current_date - datetime.timedelta(days=1)
            elif time_frame == "weekly":
                start_date = current_date - datetime.timedelta(days=7)
            elif time_frame == "monthly":
                start_date = current_date - datetime.timedelta(days=30)
            else:
                logging.error("Invalid time frame specified.")
                return None

            start_date_str = start_date.strftime("%Y-%m-%d")
            current_date_str = current_date.strftime("%Y-%m-%d")

            total_income = db.calculate_total_income(start_date_str, current_date_str)
            logging.info(f"Total income for the {time_frame} time frame: ${total_income}")
            return total_income

        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None

    
    
    

class Medical_Record(Paient):
    def __init__(self, patient_name,record_id, record_date):
        Paient.__init__(self,patient_name)
        self.record_id = record_id
        self.record_date = record_date

   

    def display_visit_history(self, patient_id):
        try:
            db_connection, db_cursor = db.Database()._db_connect()
            query = "SELECT COUNT(*) FROM doctor_visit WHERE patient_id = %s"
            db_cursor.execute(query, (patient_id,))
            visit_count = db_cursor.fetchone()[0]
            db.Database()._close()
            print(f"Patient with ID {patient_id} has been visited {visit_count} times.")

        except Exception as e:
            logger.error(f"Error displaying visit history for patient ID {patient_id}: {str(e)}")
        return


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

   first_admin=Admin("fariba","123","fariba@gmail.com","9123546845")

   first_admin.list_patients()
   first_admin.list_doctors()