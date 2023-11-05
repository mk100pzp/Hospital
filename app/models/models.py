from venv import logger
from app.database import db

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
            db.Database.save_admin(admin_obj)

            print("New admin added successfully!")

        except Exception as e:
            logger.error(f"Error adding a new admin: {str(e)}")


    def list_patients(self):
        try:
            db_connection, db_cursor = db.Database()._db_connect()
            query = "SELECT * FROM patient"
            db_cursor.execute(query)
            patients = db_cursor.fetchall()
            db.Database()._close()

            print("List of Patients:")
            for patient in patients:
                print(f"Patient ID: {patient[0]}, Name: {patient[1]}, Email: {patient[3]}, Mobile: {patient[4]}")

        except Exception as e:
            logger.error(f"Error listing : {str(e)}")


    def list_doctors(self):
        try:
            db_connection, db_cursor = db.Database()._db_connect()
            query = "SELECT * FROM doctor"
            db_cursor.execute(query)
            doctors = db_cursor.fetchall()
            db.Database()._close()

            print("List of Doctors:")
            for doctor in doctors:
                print(f"Doctor ID: {doctor[0]}, Name: {doctor[1]}, Email: {doctor[3]}, Mobile: {doctor[4]}")

        except Exception as e:
            logger.error(f"Error listing doctors: {str(e)}")

    

# this class add search ability to doctor and patient class
class Mixinsearch:
    def get_information(role)->dict:
        name=input("please  name : ")
        dict_information=db.search_database_information(role,name)
        return dict_information
    
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
    def serch_doctor_information(cls):
        dict_information=cls.get_information("doctor")
        try:
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

        except KeyError:
            print("there isn't any doctor for entered name :")
        
           
    def search_income_visit():
        # calculate all income of a doctor 
        user_name=input("please enter a user name: ")
        user_pass=input("please enter a password: ")
        incom=db.calculate_visit_incom_doctor(user_name,user_pass)
        print(f"the incom of that doctor is {incom}")
        



class Paient(User,Mixinsearch):
    def __init__(self, user_name, user_pass_1, user_email, user_mobile,patient_name, patient_address):
        User.__init__(self,user_name, user_pass_1, user_email, user_mobile)
        self.patient_name = patient_name
        self.patient_address = patient_address

    def show_visit_form():
        # get information to create visit and create object from that ,call show_visit_form from database module
        username=input("please enter your username:  ")
        password=input("please enter your password: ")
        dict_information=db.search_visit_form(username, password)
        print(dict_information)

    @classmethod
    def get_visit_time(cls):
        try:
            dict_time=db.search_empty_time()
            for num, time in dict_time.items():
                print(num, ":", time)
            choise_num=input("Please enter a number to get :  ")
        
            dict_choise_time=dict_time[choise_num]
            visit_id=dict_choise_time["visit_id"]
            user_name=input("Please enter your user name: ")
            password=input("Please enter your password: ")
            if db.save_visit_time(visit_id,user_name,password):
                print("your visit time is saved")
            else:
                ("sorry please try again later")
        except KeyError:
            print("please enter right number! ")
            cls.get_information("patient")


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


class Visit_Form:
    def __init__(self, form_name, visit_desc,hospitalization=False, duration_of_hospitalization=0):
        self.form_name = form_name
        self.visit_desc = visit_desc
        self.hospitalization = hospitalization
        self.duration_of_hospitalization = duration_of_hospitalization
        

    
    
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
    
    @staticmethod
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


    