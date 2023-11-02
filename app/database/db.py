import psycopg2

class Database:

    def __init__(self, dbname, user, password, host, port):

        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        self.connection = None
        self.cursor = None


    def connect(self):

        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )

            self.cursor = self.connection.cursor()

        except psycopg2.Error as e:
            print(f"Error : {e}")


    def close_connection(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
    def save_doctor(obj):
        pass
    def save_admin():
            pass
    def save_patient(obj):
            pass
    
    def save_visit_time(obj):
            pass
    def remove_database_visit_time(obj):
            pass
    def get_database_visit_time(obj):
            pass
    def cancel_database_visit_time(obj):
            # set null in patient id clumn of visit time table
            pass
    def catched_visit_time():
            # show all visit time for id_patient

            pass
    def save_patient_bill():
            pass
    def show_bill():
            pass
    def show_patient_information(obj):
            pass

    def show_doctor_information(obj):
            pass
    def show_income_visit(obj):
            # search for information of object income
            pass
    def show_number_visits():
            # get information for find visits and show them from database
            pass
    def show_income_hospital():
            
            pass
    def show_visit_form(obj):
            pass
    def save_medical_record(obj):
           pass
    def save_visit_form(obj):
           pass
    # ......
    
    def add_visit_time():
            pass

    def edit_visit_time():
            # first catch the exist time then edit it and delete old time so create edited time by call save_visit_time function
            pass

    def remove_visit_time():
            pass
    def save_medical_record(obj):
           pass
    
    # ......
    
    def show_log_info():
            pass

    def show_log_error():
            pass