from configparser import ConfigParser
import psycopg2
from psycopg2 import Error
import logging
import importlib


class DbPostgresManager:
    def __init__(self, dbps_defult="database.ini", dbname='db_hospital', password=None,tables='hospital.ini'):
        self.dbps_defult = dbps_defult
        self.dbname = dbname
        self.password = password
        self.tables=tables
        self.__conn = None
        self.__cur = None
    @staticmethod
    def reade_file(filename):
        parser = ConfigParser()
        parser.read(filename)
        return parser
    @staticmethod
    def config(filename="database.ini", section=None):
        parser=DbPostgresManager.reade_file(filename)
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
            

    def creat_table(self):
        self._db_connect()
        all_tables=DbPostgresManager.reade_file(self.tables).sections()
        for table in all_tables:
            columns= DbPostgresManager.config(self.tables, section=table)
            query = "CREATE TABLE IF NOT EXISTS {0} ({1});".format(table, ", ".join(
                (str(value[0]) + " " + str(value[1])) for value in columns.items()))
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
    
#     def save_visit_time(visit_id,user,password):
# find id_patient with username and password then save it in patient_id clumn in visit_date whith visit_id associated with it
# if it ia successfull return true else return false
#             pass
#     def remove_database_visit_time(obj):
#             pass

    # def cancel_visit_time(visit_id):
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
#     def search_visit_form(username, password):
#  show last visit form for username and password of patient
#             pass
#     def save_medical_record(obj):
#            pass
#     def save_visit_form(obj):
#            pass
#     # ......
    
#     def add_visit_time()->bool:
#             pass



#     def remove_visit_time(id_visit_time)->bool:
#             pass
#     def save_medical_record(obj):
#            pass
    
#     # ......
    
#     def show_log_info():
#             pass

#     def show_log_error():
#             pass
    # def search_empty_time():
        # search all empty time records and return them with all information such as name of doctor ,time and.. in a dictionary like
        # {"1":{"doctor name":...,"visit_id":...,"time":...},"2":{"doctor name":...,"time":...}}

#     def serch_database_information(table_name,name)->dict:
#         pass
# #     it should search in tablename for a specific name in database the return dictionary if his information that their key is name of clumn and value is information
# # if there is not any record with that name return empty dictionary
# def calculate_visit_incom_doctor(user_name,password):
#     # find doctor then find and sum of cost of all visit for that doctor and return amount of that

#     pass
first_db=DbPostgresManager()

first_db.creat_table()





