class User:
    def __init__(self, user_id, user_name, user_pass, user_email, user_mobile, role):
        self.user_id = user_id
        self.user_name = user_name
        self.user_pass = user_pass
        self.user_email = user_email
        self.user_mobile = user_mobile
        self.role = role


class Admin(User):
    def __init__(self, admin_id, users_user_id):
        self.admin_id = admin_id
        self.users_user_id = users_user_id

    def add_new_admin():
        pass

    

class Doctor(User):
    def __init__(self, doctor_id, experties, work_experienceit, salary, address, visit_price, users_user_id):
        self.doctor_id = doctor_id
        self.experties = experties
        self.work_experienceit = work_experienceit
        self.salary = salary
        self.address = address
        self.visit_price = visit_price
        self.users_user_id = users_user_id

    def serch_doctor_information():
        pass

    def search_income_visit():
        # get information to find visit and create object from that ,call show_visit_information from database module
        pass



class Paient(User):
    def __init__(self, paient_id, paient_name, paient_address, users_user_id):
        self.paient_id = paient_id
        self.paient_name = paient_name
        self.paient_address = paient_address
        self.users_user_id = users_user_id

    def search_patient_information():
        # creat patient object with input information then call show_patient_information from database module
        pass

class Visit_Form:
    def __init__(self, form_id, form_name, visit_desc,medical_record_id, visit_date_visit_id,hospitalization=False, duration_of_hospitalization=0):
        self.form_id = form_id
        self.form_name = form_name
        self.visit_desc = visit_desc
        self.hospitalization = hospitalization
        self.duration_of_hospitalization = duration_of_hospitalization
        self.medical_record_id = medical_record_id
        self.visit_date_visit_id = visit_date_visit_id

    def search_visit_form():
        # get information to find visit and create object from that ,call show_visit_form from database module
        pass

    def create_record(cls):
        # input information
        pass


    
class Visit_Date:
    def __init__(self, visit_id, visit_date_time, doctor_id, paient_id):
        self.visit_id = visit_id
        self.visit_date_time = visit_date_time
        self.doctor_id = doctor_id
        self.paient_id = paient_id

    def get_visit_time():
        pass

    def cancel_visit_time():
        pass


class Paient_Bill:
    def __init__(self, bill_id, paient_paient_id, date, total_amount, paient_share, amount_paid, the_remaining_amount, insurance_contribution):
        self.bill_id = bill_id
        self.paient_paient_id = paient_paient_id
        self.date = date
        self.total_amount = total_amount
        self.paient_share = paient_share
        self.insurance_contribution = insurance_contribution

    def create_patient_bill():
        pass


class Medical_Record:
    def __init__(self, record_id, date_of_visit):
        self.record_id = record_id
        self.date_of_record = date_of_visit
    
    def create_medical_record(cls):
        pass

