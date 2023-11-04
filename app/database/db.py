from configparser import ConfigParser
import psycopg2
from psycopg2 import Error
import logging
import importlib


class DbPostgresManager:
    def __init__(self, dbps_defult="database.ini", dbname='db_hospital', password='1234'):
        self.dbps_defult = dbps_defult
        self.dbname = dbname
        self.password = password
        self.table_name = None
        self.columns = None
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
        conn.autocommit = True
        with conn:
            with conn.cursor() as cursor:
                query_exist_database = '''(select 1 from pg_database where  datname=%s)'''
                cursor.execute(query_exist_database, (self.dbname,))
                print(":D----")
                params['dbname'], params['password'] = self.dbname, self.password
                if cursor.fetchone():
                    print(":D----")
                    return params
                else:
                    cursor.execute(f'CREATE DATABASE {self.dbname}')
                    params['dbname'], params['password'] = self.dbname, self.password
                    conn.commit()
                    print(":D")
                return params

    def _db_connect(self):
        """Establish a connection to the PostgreSQL database."""

        try:
            params = self.connection_database()
            self.__conn = psycopg2.connect(**params)
            self.__cur = self.__conn.cursor()
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

    def creat_table(self, tables_name):

        for table in tables_name:
            self._db_connect()
            self.__cur.execute(F"CREATE TABLE *{tables_name}*();")

    def create_columns(self, table_name, columns: dict):
        for column_name, value in self.columns.items():
            self.__cur.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {value[0]};")
            # self.__cur.execute(f"ALTER TABLE {table_name} ADD COLUMN {new_column_name} data_type constraint;")
            if len(value) >= 2:
                self.intro_key(table_name, column_name)
        self._close()

    def intro_key(self, table_name, new_column_name):
        if new_column_name[1] == "primary":
            self.__cur.execute(f"alter table {table_name} add primary key {new_column_name[0]};")
        else:
            self.__cur.execute(
                f"alter table {table_name} add foreign key (employee_number) EFERENCES {new_column_name[2]} {new_column_name[0]}")
        self._close()

    connection_database()


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