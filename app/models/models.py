from database.db import Database
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
        user_name=input("please enter a user name: ")
        user_pass=input("please enter a password: ")
        user_email=input("please enter your email: ")
        user_mobile=input("please enter your phone: ")
        admin_obj=cls(user_name,user_pass,user_email,user_mobile)
        Database.save_admin(admin_obj)

# this class add search ability to doctor and patient class
class Mixinsearch:
    def get_information()->dict:
        name=input("please  name : ")
        dict_information=Database.serch_database_information("doctor",name)
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
        dict_information=cls.get_information()
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
        incom=Database.calculate_visit_incom_doctor(user_name,user_pass)
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
        dict_information=Database.search_visit_form(username, password)
        print(dict_information)
    @classmethod
    def get_visit_time(cls):
        try:
            dict_time=Database.search_empty_time()
            for num, time in dict_time.items():
                print(num, ":", time)
            choise_num=input("Please enter a number to get :  ")
        
            dict_choise_time=dict_time[choise_num]
            visit_id=dict_choise_time["visit_id"]
            user_name=input("Please enter your user name: ")
            password=input("Please enter your password: ")
            if Database.save_visit_time(visit_id,user_name,password):
                print("your visit time is saved")
            else:
                ("sorry please try again later")
        except KeyError:
            print("please enter right number! ")
            cls.get_information()


    def cancel_visit_time():
        id_visit=input("Please enter id of your visit time")
        if Database.cancel_visit_time(id_visit):
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
    def __init__(self,doctor_id, visit_date_time,patient_id="Null"):
        self.doctor_id = doctor_id
        self.visit_date_time = visit_date_time
        self.patient_id = patient_id

    @staticmethod
    def create_visit_date():
        doctor_id=input("please enter yor id: ")
        visit_date=input("please enter visit date like '07/01/2019 07:00:00': ")
        obj=Visit_Date(doctor_id, visit_date)
        if Database.add_visit_time(obj):
            print("Adding visit time successfully")
        else:
            print("please try again!")
    
    @staticmethod
    def remove_visit_time():
        id_visit_time=input("please enter id_visit_time: ")
        if Database.remove_visit_time(id_visit_time):
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

    
    
    

class Medical_Record:
    def __init__(self):
        pass

    