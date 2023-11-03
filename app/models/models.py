class User:
    def __init__(self, user_name, user_pass, user_email, user_mobile):
        self.user_name = user_name
        self.user_pass = user_pass
        self.user_email = user_email
        self.user_mobile = user_mobile
        


class Admin(User):
    def __init__(self,user_name, user_pass, user_email, user_mobile):
        User.__init__(self,user_name, user_pass, user_email, user_mobile)

    def add_new_admin():
        pass

    

class Doctor(User):
    def __init__(self,user_name, user_pass_1, user_email, user_mobile,doctor_name , experties, work_experienceit, salary, address, visit_price):
        User.__init__(self,user_name, user_pass_1, user_email, user_mobile)
        self.doctor_name = doctor_name
        self.experties = experties
        self.work_experienceit = work_experienceit
        self.salary = salary
        self.address = address
        self.visit_price = visit_price
        

    def serch_doctor_information():
        pass

    def search_income_visit():
        # get information to find visit and create object from that ,call show_visit_information from database module
        pass



class Paient(User):
    def __init__(self, user_name, user_pass_1, user_email, user_mobile,patient_name, patient_address):
        User.__init__(self,user_name, user_pass_1, user_email, user_mobile)
        self.patient_name = patient_name
        self.patient_address = patient_address
        

    def search_patient_information():
        # creat patient object with input information then call show_patient_information from database module
        pass

class Visit_Form:
    def __init__(self, form_name, visit_desc,hospitalization=False, duration_of_hospitalization=0):
        self.form_name = form_name
        self.visit_desc = visit_desc
        self.hospitalization = hospitalization
        self.duration_of_hospitalization = duration_of_hospitalization
        

    def search_visit_form():
        # get information to find visit and create object from that ,call show_visit_form from database module
        pass

    def create_record(cls):
        # input information
        pass


    
class Visit_Date:
    def __init__(self, visit_date_time):
        self.visit_date_time = visit_date_time
        
    def get_visit_time():
        pass

    def cancel_visit_time():
        pass


class Paient_Bill:
    def __init__(self, date, total_amount, paient_share, amount_paid, the_remaining_amount, insurance_contribution):
        self.amount_paid = amount_paid
        self.the_remaining_amount = the_remaining_amount
        self.date = date
        self.total_amount = total_amount
        self.paient_share = paient_share
        self.insurance_contribution = insurance_contribution

    def create_patient_bill():
        pass


class Medical_Record:
    def __init__(self):
        pass

    def create_medical_record(cls):
        pass

