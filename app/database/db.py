from configparser import ConfigParser
import psycopg2
from psycopg2 import Error
import logging
import importlib


class DbPostgresManager:
    def __init__(self, dbps_defult="database.ini", dbname='db_hospital', password=None):
        self.dbps_defult = dbps_defult
        self.dbname = dbname
        self.password = password
        self.__conn = None
        self.__cur = None

    @staticmethod
    def config(filename="database.ini", section=None):
        parser = ConfigParser()
        parser.read(filename)
        if parser.has_section(section):
            db_config = dict(parser.items(section))
        else:
            raise Exception(f'section {section} not found')
        return db_config

    def connection_database(self):
        params = DbPostgresManager.config(self.dbps_defult, section="default_inf_connect")
        conn = psycopg2.connect(**params)
        cur=conn.cursor()
        conn.autocommit = True
        query_exist_database = '''(select 1 from pg_database where  datname=%s)'''
        cur.execute(query_exist_database, (self.dbname,))
        if cur.fetchone():
            params['dbname']= self.dbname
            return params
        else:
            cur.execute(f'CREATE DATABASE {self.dbname}')
            params['dbname']=self.dbname
        return params
        
    def _db_connect(self):
        """Establish a connection to the PostgreSQL database."""

        try:
            params = self.connection_database()
            self.__conn = psycopg2.connect(**params)
            self.__cur = self.__conn.cursor()
            
            return self.__conn,self.__cur
        except Exception as error:
            logging.error(
                f"Error: Could not connect to the {self.dbname} database. \n{error}"
            )
            return None

    def _close(self):
        """
            Simple method that closes the connection.
        """

        try:
            self.__conn.commit()
            self.__cur.close()
            self.__conn.close()

        except Exception:
            print("---- Error closing database")

        return

    def drop_database(self, dbname: str):
        """
        Deletes a Database.

        Paramaters
        ----------
        dbname : str
            The name of the Database to drop.
        """
        try:
            self._db_connect()
            iso_lvl = importlib.import_module("psycopg2.extensions").ISOLATION_LEVEL_AUTOCOMMIT
            self.__conn.set_isolation_level(iso_lvl)
            self.__cur = self.__conn.cursor()
            self.__cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = dbname")
            exists_db = self.__cur.fetchone()[0]
            if not exists_db:
                print(f"Db {dbname} Not Exists")
            else:
                self.__cur.execute("DROP DATABASE IF EXISTS %s;" % dbname)
            self._close()
        except Error as err:
            print(err)

    def creat_table(self, tables: dict):
        self._db_connect()
        for table, coloumn in tables.items():
            query = "CREATE TABLE IF NOT EXISTS {0} ({1});".format(table, ", ".join(
                (str(value[0]) + " " + str(value[1])) for value in coloumn.items()))
            self.__cur.execute(query)
        self.__conn.commit()
        self._close()
        print("table create successfully")


        

    # def update_table(self,table_name, name_column,value :str, taget_cell:str, target_value):
    #     self.__cur.execute(f" UPDATE {table_name} SET {taget_cell} = {target_value} WHERE {name_column}={value});")

    # def insert_row(self,table_name : str ,columns_name:tuple,values : tuple):
    #     self.__cur.execute(f"INSERT INTO {table_name} {columns_name} VALUES({values};")
    #     #RETURNING output_expression AS output_name;

    # def delete_row(self,table_name : str,column_name : str,value: None):
    #     self.__cur.execute(f"DELETE FROM {table_name} WHERE {column_name}={value} RETURNING (select_list | *)")

    # def select_row(self,table_name: str,column_name: str, values : None ,order_base_row: str,columns_show = "*"):
    #     self.__cur.execute(f"SELECT {columns_show} FROM {table_name} WHERE {column_name}={values} ORDER BY {order_base_row};")
    
    # @staticmethod
    # def check_password(hashed_password, input_password):
    #         return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password)
    
#     #=================================================================================================

    # اسم کاربری و پسورد رو با ورودی مقایسه کند و اگر چنین دکتری وجود داشت ترو را برگداند
    #برای مقایسه از تابع چک پسورد استفاده کند
    def check_exist(table_name, username, password):
           pass
    
    #=================================================================================================
#     def save_doctor(obj):
#             pass
#     def save_admin():
#             pass
#     def save_patient(obj):
#             pass
    
#     def save_visit_time(obj):
#             pass
#     def remove_database_visit_time(obj):
#             pass
#     def get_database_visit_time(obj):
#             pass
    # def cancel_database_visit_time(obj):
    #         # set null in patient id clumn of visit time table
    #         pass
#     def catched_visit_time():
#             # show all visit time for id_patient

#             pass
#     def save_patient_bill():
#             pass
#     def show_bill():
#             pass
#     def show_patient_information(obj):
#             pass

#     def show_doctor_information(obj):
#             pass
#     def show_income_visit(obj):
#             # search for information of object income
#             pass
#     def show_number_visits():
#             # get information for find visits and show them from database
#             pass
#     def show_income_hospital():
            
#             pass
#     def show_visit_form(obj):
#             pass
#     def save_medical_record(obj):
#            pass
#     def save_visit_form(obj):
#            pass
#     # ......
    
#     def add_visit_time():
#             pass

#     def edit_visit_time():
#             # first catch the exist time then edit it and delete old time so create edited time by call save_visit_time function
#             pass

#     def remove_visit_time():
#             pass
#     def save_medical_record(obj):
#            pass
    
#     # ......
    
#     def show_log_info():
#             pass

#     def show_log_error():
#             pass
    
#     def serch_database_information(table_name,name)->dict:
#         pass
# #     it should search in tablename for a specific name in database the return dictionary if his information that their key is name of clumn and value is information
# # if there is not any record with that name return empty dictionary

first_db=DbPostgresManager()
 
table={
      "users": {"user_id":"serial primary key",
                "user_name":"varchar(100)",
                "user_pass":"varchar(255)",
                "user_email":"varchar(255)",
                "user_mobil":"int"       
      },
      "patients":{"patient_id":"serial primary key",
                "patient_name":"varchar (100)",
                "patient_adress":"text",
                "users_user_id":"int references users(user_id)"
      },
      "doctors":{"doctor_id":"serial primary key",
                "expertis":"varchar (50)",
                "work_experience":"int",
                "adress": "text",
                "visit_price":"decimal(10,3)",
                "users_user_id":"int references users(user_id)"      
      },
     "admin":{"admin_id": "serial primary key",
             "users_user_id": "int references users(user_id)" 
      },
      "visit_dates":{"visit_id":"serial primary key",
                   "visit_time": "timestamp",
                   "doctors_doctor_id": "int references doctors (doctor_id)",
                   "patients_patient_id": "int references patients (patient_id)"    
      },
            "medical_records":{"record_id":"serial primary key",
                         "record_date":"timestamp"
      },
      "visit_forms":{"from_id": "serial primary key",
                     "from_name": "varchar (50)",
                     "visit_desc": "text",
                     "hospitalization": "bool",
                     "duration_of_hospitalization": "int",
                     "medical_records_record_id":"int references medical_records (record_id)",
                     "visit_dates_visit_id": "int references visit_dates (visit_id)"   
      },
      "patient_bills":{"bill_id":"serial primary key",
                       "date" : "timestamp",
                       "patient_share": "decimal(10,3)",
                       "mount_paid": "decimal(10,3)",
                       "the_remaining_amount": "decimal(10,3)",
                       "insurance_contribution": "decimal(10,3)" 

      }
}

first_db.creat_table(table)





