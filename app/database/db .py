from configparser import ConfigParser
import psycopg2
from psycopg2 import Error
import logging
import importlib


class DbPostgresManager:
    def __init__(self, dbps_defult="database.ini", dbname='db_hospital', password=None, tables='hospital.ini'):
        self.data = None
        self.dbps_defult = dbps_defult
        self.dbname = dbname
        self.password = password
        self.tables = tables
        self.__conn = None
        self.__cur = None

    @staticmethod
    def reade_file(filename):
        """Read  file content about database's details"""
        parser = ConfigParser()
        parser.read(filename)
        return parser

    @staticmethod
    def config(filename="database.ini", section=None):
        parser = DbPostgresManager.reade_file(filename)
        if parser.has_section(section):
            db_config = dict(parser.items(section))
        else:
            raise Exception(f'section {section} not found')
        return db_config

    def connection_database(self):
        """Establish a connection to the PostgreSQL database to Create database for hospital project """
        params = self.config(self.dbps_defult, section="default_inf_connect")
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        conn.autocommit = True
        query_exist_database = '''(select 1 from pg_database where  datname=%s)'''
        cur.execute(query_exist_database, (self.dbname,))
        if cur.fetchone():
            params['dbname'] = self.dbname
            return params
        else:
            cur.execute(f'CREATE DATABASE {self.dbname}')
            params['dbname'] = self.dbname
        return params

    def _db_connect(self):
        """Establish a connection to hospital database."""

        try:
            params = self.connection_database()
            self.__conn = psycopg2.connect(**params)
            self.__cur = self.__conn.cursor()
            return self.__conn, self.__cur
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

    def create_table(self):
        self._db_connect()
        all_tables = DbPostgresManager.reade_file(self.tables).sections()
        for table in all_tables:
            columns = DbPostgresManager.config(self.tables, section=table)
            query = "CREATE TABLE IF NOT EXISTS {0} ({1});".format(table, ", ".join(
                (str(value[0]) + " " + str(value[1])) for value in columns.items()))
            self.__cur.execute(query)
        self.__conn.commit()
        self._close()
        print("table create successfully")

    def drop_table(self, table_name):
        """
              his method remove a table from a Database.

              parameters
              ---------
              table_name : str
                 The name of the table to remove.
        """
        self._db_connect()
        query = f"DROP TABLE IF EXISTS {table_name} CASCADE;"
        self.__cur.execute(query)
        print("table drop..")
        self._close()

    def update_table(self, table_name, new_value: dict, condition: list):
        """
            This method update rows of table from a Databas
            Parameters
            ----------
            table_name : str
                The name of the table to remove.
            new_value:dict
                The new value for update column table
            condition:
                The conditions for select column of table
        """
        try:
            self._db_connect()
            values = []
            key = 0  # Static value for getting keys in items tuple
            value = 1  # Static value for getting values in items tuple
            for item in new_value.items():
                if isinstance(item[value], float) or isinstance(item[value], int):
                    values.append(f"{item[key]} = {item[value]}")
                else:
                    values.append(f"{item[key]} = {item[value]}")
            query = f"UPDATE {table_name} SET {','.join(values)} "
            if condition:
                if len(condition) > 1:
                    query += f"WHERE {' AND '.join([f'{column} {operator} {value}' for column, operator, value in condition])}"
                else:
                    column, operator, value = condition[0]
                    query += f"WHERE {column} {operator} {value}"
            else:
                query += ";"
            self.__cur.execute(query)
            print("data update in tables")
            self._close()
        except Error as err:
            print(err)

    def delete_from_table(self, table_name: str, condition: dict):
        self._db_connect()
        query = f"DELETE FROM {table_name} "
        # query = f"DELETE FROM {table_name} RETURNING (select_list | *)"
        if condition:
            query += f"WHERE {condition};"
        else:
            query += ";"
        self.__cur.execute(query)
        self._close()

    def insert_table(self, table_name: str, col_name: list, col_value: list):
        """
            This method will insert in the given table by:
            ----------
            table : str
                The table we will insert the values into.
            col_name: list
                list of column table
            col_value : list
                List of values to add.
        """
        try:
            self._db_connect()
            columns = [f'"{x}"' for x in col_name]
            new_col_value = []
            for value in col_value:
                if isinstance(value, float) or isinstance(value, int):
                    new_col_value.append("%s" % value)
                else:
                    new_col_value.append("'%s'" % value)
            query = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({','.join(new_col_value)})"
            self.__cur.execute(query)
            print("data insert to table")
            self._close()
        except Error as err:
            print(err)

    def select(self, table_name: list, limit=None, select_options: list = None,
               filter_options: list = None, order_options: list = None, group_options: list = None,
               join_query:str=None):
        """
            Read data from a table in the database can choose to read only some
            specific fields
            Parameters
            ----------
                table_name   :  Table to read from
                select_options:  list with fields that will be retrieved

                filter_options:  list with filtering options for the SQL query

                order_options:   list with field that will be used for sorting the
                                results of the query
                group_options:   list with field that will be used for group the column of table

                limit:          The maximum number of records to retrieve

       """
        
        try:
            self._db_connect()
            query = "SELECT "
            if select_options:
                query = query + ",".join(select_options)
            else:
                query = query + "*"

            query = query + " FROM " + ",".join(table_name) + " "

            if join_query:
                query = query + join_query

            if filter_options:
                # column, operator, value = zip(*filter_options)
                if len(filter_options) > 1:
                    query += f"WHERE {' AND '.join([f'{column} {operator} {value}' for column, operator, value in filter_options])}"

                else:
                    column, operator, value = filter_options[0]
                    query += f"WHERE {column} {operator} {value}"

            if order_options:
                query = query + "ORDER BY " + ",".join(order_options)
            if group_options:
                query = query + "GROUP BY " + ",".join(group_options)
            if limit:
                query = query + "LIMIT " + limit
            else:
                query += ";"

            self.__cur.execute(query)
            self.data = self.__cur.fetchall()
            
            # self.select_columns = [desc[0] for desc in self.__cur.description]
            # self.show_table(table_name)

            self._close()
            return self.data

        except Error as err:
            print(err)
    
    def show_table(self,table_name: list, limit=None, select_options: list = None,
               filter_options: list = None, order_options: list = None, group_options: list = None,
               logical_operator: str = None,join_query:str=None):
        """
        Display the contents of a table.

        Parameters
        ----------
        table_name : str
            The name of the table to display.
        """
        self.select_table(table_name, limit, select_options,
                          filter_options, order_options,
                            group_options,logical_operator,join_query)
        try:
            if self.data:
                print(f"Table: {table_name}")
                print(', '.join(self.select_columns))
                for row in self.data:
                    print(', '.join(str(value) for value in row))
            else:
                print("The table is empty.")
        except Error as err:
            print(err)

    def alter_table(self, table_name:str, alterations:dict):
        """
        Alter the table structure by adding, dropping, or modifying columns.
    
        Parameters:
        table_name (str): The name of the table to alter.
        alterations (list): A list of alteration statements, each represented as a dictionary.
        """
        try:
            self._db_connect()
            query=f"ALTER TABLE {table_name} "
            action = alterations.get("action")
            column_name = alterations.get("column_name")
            new_column_definition = alterations.get("column_definition")
            if action == "add_column":
                query += f"ADD COLUMN {column_name} {new_column_definition};"
            elif action == "drop_column": 
                query += f"DROP COLUMN {column_name};"
            elif action == "modify_column": 
                query += f"ALTER COLUMN {column_name} SET DATA TYPE {new_column_definition};"
            else:
                print("Invalid action specified in alteration statement.")
            self.__cur.execute(query)
            print(f"Table '{table_name}' altered successfully.") 
            self._close()
        except Error as err:
            print(err)

#     #=================================================================================================

# اسم کاربری و پسورد رو با ورودی مقایسه کند و اگر چنین دکتری وجود داشت ترو را برگداند
# برای مقایسه از تابع چک پسورد استفاده کند
# def check_exist(table_name, username, password):
#        pass
# @staticmethod
# def check_password(hashed_password, input_password):
#         return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password)
# =================================================================================================
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

# def edit_visit_time(): # first catch the exist time then edit it and delete old time so create edited time by call
# save_visit_time function pass

#     def remove_visit_time():
#             pass
#     def save_medical_record(obj):
#            pass

#     # ......

#     def show_log_info():
#             pass

#     def show_log_error():
#             pass

# def serch_database_information(table_name,name)->dict: pass #     it should search in tablename for a specific name
# in database the return dictionary if his information that their key is name of clumn and value is information # if
# there is not any record with that name return empty dictionary


# Test Case
first_db = DbPostgresManager()

first_db.create_table()
# first_db.drop_table("users")
first_db.insert_table("patients", ["patient_name", "patient_adress","users_user_id"],
                      ["sara", "tehran", 1])
# first_db.insert_table("users", ["user_name", "user_pass", "user_email", "user_mobil"],
#                       ["shima", "1234", "shima@gmail.com", "09338693536"])
# first_db.select(table_name=["users"], select_options=["user_name", "user_email", "user_pass"],
#                 filter_options=[("user_pass", "=", "'1234'")], group_options=["user_id"], logical_operator="AND")
first_db.select(table_name=["users"], select_options=["user_name", "user_email", "user_pass"],
               join_query="INNER JOIN patients ON  users.user_id = patients.users_user_id;")
# first_db.show_table("users")
# first_db.delete_from_table("users", "user_name='shima'")
# first_db.update_table("users", {"user_name": "'ali'"}, [("user_name", "=", "'shima'")])
# first_db.alter_table("users", {"action":"add_column","column_name":"user_mobil","column_definition":"bigint"})


