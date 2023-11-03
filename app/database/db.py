import psycopg2
import bcrypt
from configparser import ConfigParser



def config(filename="database.ini", section=None):
    parser = ConfigParser()
    parser.read(filename)
    if parser.has_section(section):
        db_config = dict(parser.items(section))
        params = parser.items(section)
        # for param in params:
        #     db_config[param[0]] = param[1]
    else:
        raise Exception(f'section {section} not found')
    return db_config


def connection_database(db_name):
    try:
        params = config("database.ini", section="default_inf_connect")
        conn = psycopg2.connect(**params)
        conn.autocommit = True
        cursor = conn.cursor()
        query_exist_database = '''(select 1 from pg_database where  datname=%s)'''
        # '''select exists (select 1 from pg_database where  datname=%s)'''
        # '''select exists (SELECT datname from pg_database where datname=%s)'''
        cursor.execute(query_exist_database, (db_name,))
        # (query_exist_database,db_name)
        print(":D----")

        if cursor.fetchone():
            print(":D----")
            pass
        else:

            cursor.execute(f'CREATE DATABASE {db_name}')
            conn.commit()
            print(":D")
    except(Exception, psycopg2.Error) as Error:
        # print('you cant connect to postgres default database, check information of your default database')
        print(Error)
    finally:
        if conn:
            cursor.close()
            conn.close()


def connect(conn, cur, db_name):
    if conn and cur:
        conn, cur, local_connection = conn, cur, False
    else:
        try:
            connection_database(db_name)
            params = config("database.ini", section="inf_connect")
            conn = psycopg2.connect(**params)
            cur = conn.cusor()
            local_connection = True
        except (Exception, psycopg2.DatabaseError) as e:
            conn, cur, local_connection = None, None, None
        return conn, cur, local_connection


def creat_table(conn, cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS request_logs (id SERIAL PRIMARY KEY,role_name VARCHAR(255),role_dec VARCHAR(255)")


connection_database('sample')

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

    @staticmethod
    def check_password(hashed_password, input_password):
            return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password)
    
    #=================================================================================================

    # اسم کاربری و پسورد رو با ورودی مقایسه کند و اگر چنین دکتری وجود داشت ترو را برگداند
    #برای مقایسه از تابع چک پسورد استفاده کند
    def check_exist(table_name, username, password):
           pass
    
    #=================================================================================================
    
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
    
    def serch_database_information(table_name,name)->dict:
        pass
#     it should search in tablename for a specific name in database the return dictionary if his information that their key is name of clumn and value is information
# if there is not any record with that name return empty dictionary