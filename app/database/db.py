from configparser import ConfigParser
import os
import psycopg2
from psycopg2 import Error
import logging
import importlib
import csv

database_file = os.path.dirname(os.path.realpath(__file__))

class DbPostgresManager:
    def __init__(self, dbps_defult=os.path.join(database_file, 'database.ini'), dbname='db_hospital_v1', password=None, tables=os.path.join(database_file, 'hospital.ini')):
        self.table_name = None
        self.select_columns = None
        self.data = None
        self.dbps_defult = dbps_defult
        self.dbname = dbname
        self.password = password
        self.tables = tables
        self.conn = None
        self.cur = None

    @staticmethod
    def reade_file(filename):
        """Read  file content about database's details"""
        parser = ConfigParser()
        parser.read(filename)
        return parser

    @staticmethod
    def config(filename=os.path.join(database_file, 'hospital.ini'), section=None):
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
            self.conn = psycopg2.connect(**params)
            self.cur = self.conn.cursor()
            return self.conn, self.cur
        
        except Exception as error:

            print(
                f"Error: Could not connect to the {self.dbname} database. \n{error}"
            )
            return None

    def close(self):
        """
            Simple method that closes the connection.
        """

        try:
            self.conn.commit()
            self.cur.close()
            self.conn.close()

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
            self.conn.set_isolation_level(iso_lvl)
            self.cur = self.conn.cursor()
            self.cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = dbname")
            exists_db = self.cur.fetchone()[0]
            if not exists_db:
                print(f"Db {dbname} Not Exists")
            else:
                self.cur.execute("DROP DATABASE IF EXISTS %s;" % dbname)
            self.close()
        except Error as err:
            print(err)

    def insert_old_datafile(self, file_name: str='exported_'):
        # self._db_connect() 
        try:
            all_tables = self.reade_file(self.tables).sections()
            
            for table_name in all_tables:
                file_name += f"{table_name}.csv"
                print(file_name)
                file_path = os.path.join(database_file,file_name)
                if os.path.exists(file_path):
                    with open(file_path, "r" ,newline='') as csvfile:
                        readers = csv.reader(csvfile)
                        header_row=next(readers)    
                        column_titles = header_row
                        column_titles_list = column_titles[0].split('\x1b') 
                        for row in readers:
                            row_list = row[0].split('\x1b')
                            self.insert_table(table_name , column_titles_list, row_list)
                        file_name='exported_'
                        print(f"export {table_name} table datas successfully")
                else:
                    print(f"The file {table_name} does not exist.")

        except Exception as e:
            return f"Error importing data: {str(e)}"
        finally:
            pass
            return f"imported tables to database successfully"
    

    def export_tables_to_csv(self, output_file: str='exported_'):
        self._db_connect() 
        try:
            all_tables = self.reade_file(self.tables).sections()
            for table_name in all_tables:
                output_file += f"{table_name}.csv"
                self.cur.execute(f"SELECT * FROM {table_name}")
                results = self.cur.fetchall()
                rows_table = [list(item) for item in results]
                print(rows_table)
                with open(output_file, "w", newline="") as csvfile:
                    csvwriter = csv.writer(csvfile,delimiter=',') 
                    headers = [desc[0] for desc in self.cur.description]
                    csvwriter.writerow(headers)  
                    csvwriter.writerows(rows_table)
                    print(f"export {table_name} table datas successfully")
                    output_file='exported_'
        except Exception as e:
            return f"Error exporting data: {str(e)}"
        finally:
            self.close()
        return f"Exported tables to {output_file} successfully"
    

    def export_tables_to_csv(self, output_file: str='exported_'):
        self._db_connect() 
        try:
            all_tables = self.reade_file(self.tables).sections()
            for table_name in all_tables:
                output_file += f"{table_name}.csv"
                self.cur.execute(f"SELECT * FROM {table_name}")
                results = self.cur.fetchall()
                rows_table = [list(item) for item in results]
                print(rows_table)
                with open(output_file, "w", newline="") as csvfile:
                    csvwriter = csv.writer(csvfile,delimiter=',') 
                    headers = [desc[0] for desc in self.cur.description]
                    csvwriter.writerow(headers)  
                    csvwriter.writerows(rows_table)
                    print(f"export {table_name} table datas successfully")
                    output_file='exported_'
        except Exception as e:
            return f"Error exporting data: {str(e)}"
        finally:
            self.close()
        return f"Exported tables to {output_file} successfully"

    def create_table(self):
        self._db_connect()
        all_tables = DbPostgresManager.reade_file(self.tables).sections()
        
        for table in all_tables:
            columns = DbPostgresManager.config(self.tables, section=table)
            
            query = "CREATE TABLE IF NOT EXISTS {0} ({1});".format(table, ", ".join(
                (str(value[0]) + " " + str(value[1])) for value in columns.items()))
            print(query)
            self.cur.execute(query)
        self.close()
        

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
        self.cur.execute(query)
        print("table drop..")
        self.close()

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
            self.cur.execute(query)
            print("data update in tables")
            self.close()
        except Error as err:
            print(err)

    def delete_from_table(self, table_name: str, condition: dict):
        self._db_connect()
        query = f"DELETE FROM {table_name} "
        if condition:
            query += f"WHERE {condition};"
        else:
            query += ";"
        self.cur.execute(query)
        self.close()

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
            query = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({','.join(new_col_value)}) RETURNING {table_name[:-1]}_id"

            self.cur.execute(query)
            print("data insert to table")
            id = self.cur.fetchone()
            print("id = ", id[0])
            self.close()
        except Error as err:
            print(err)

    def join_table(self, join_type: str, table_name: list, on_conditions: list):
        """
        Create a JOIN clause for the SQL query.

        Parameters:
        - join_type (str): The type of JOIN (e.g., INNER, LEFT, RIGHT).
        - table_name (list): The name of the tables to join.
        - on_conditions (list of tuples): List of ON tuples the tuple contain of columns name for the JOIN.
        """

        join_clause = ''
        for table in range(len(table_name) - 1):
            join_clause += (f" {join_type} JOIN {table_name[table + 1]} ON "
                            f"{on_conditions[table][0]} = {on_conditions[table][1]} ")
        return join_clause

    def select(self, table_name: list, limit=None, select_options: list = None,
               filter_options: list = None, order_options: list = None, group_options: list = None,
               on_conditions: list = None, join_type: str = None, printed: str = False):
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

                printed:        The defulted value is None, for show the result of select change it to True

                join_type: The type of join clouse

                on_conditions: The name of column for join
       """
        try:
            self._db_connect()
            query = "SELECT "
            if len(select_options)>1:
                query = query + ",".join(select_options)
            elif len(select_options)==1:
                query = query + select_options[0]
            else:
                query = query + "*"

            if len(table_name) > 1:
                query = query + " FROM " + table_name[0] + self.join_table(join_type, table_name, on_conditions)
            else:
                query = query + " FROM " + table_name[0] + " "

            if filter_options:
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

            self.cur.execute(query)
            self.data = self.cur.fetchall()
            self.select_columns = [desc[0] for desc in self.cur.description]
            if printed== True:self.show_table(table_name)
            self.close()
            return self.data
        except Error as err:
            print(err)

    def show_table(self, table_name):
        """
        Display the contents of a table.

        Parameters
        ----------
        table_name : str
            The name of the table to display.
        """
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

    def alter_table(self, table_name: str, alterations: dict):
        """
        Alter the table structure by adding, dropping, or modifying columns.

        Parameters:
        table_name (str): The name of the table to alter.
        alterations (list): A list of alteration statements, each represented as a dictionary.
        """
        try:
            self._db_connect()
            query = f"ALTER TABLE {table_name} "
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
            self.cur.execute(query)
            print(f"Table '{table_name}' altered successfully.")
            self.close()
        except Error as err:
            print(err)


# Test Case
fdb = DbPostgresManager()
# # first_db.export_tables_to_csv()

fdb.create_table()
fdb.insert_old_datafile()
fdb.export_tables_to_csv()


# first_db.drop_table("users")
# insert---------------------------------
# first_db.insert_table("users", ["user_name", "user_pass", "user_email", "user_mobil"],
#                       ["kaveh", "789", "sara@gmail.com", 9124568675])
# first_db.insert_table("users", ["user_name", "user_pass", "user_email", "user_mobil"],
#                       ["shima", "1234", "shima@gmail.com", 9338693536])
# first_db.insert_table("patients", ["patient_name", "patient_adress", "users_user_id"],
#                       ["fariba", "saveh", 4])
# first_db.insert_table("users", ["user_name", "user_pass", "user_email", "user_mobil"],
#                       ["shima", "1234", "shima@gmail.com", 9338693536])
# first_db.insert_table("doctors", ["expertis", "work_experience", "adress", "visit_price"],
#                       ["brain", "12", "karaj", "3000"])
# first_db.insert_table("visit_dates", ["visit_time","patients_patient_id"],
#                       ["08/02/2023",7])
# first_db.insert_table("visit_dates", ["visit_time"],
#                       ["02/06/2021"])

# select ---------------------------------
# first_db.select(table_name=["users"], select_options=["user_name", "user_email", "user_pass"],
#                 filter_options=[("user_pass", "=", "'1234'")], group_options=["user_id"], logical_operator="AND")
# first_db.select(table_name=["users","patients"], select_options=["user_name", "user_email", "user_pass"],
#                on_conditions=[("users.user_id", "patients.users_user_id")],printed=True)
# first_db.select(table_name=["users", "patients",], select_options=["user_name", "user_email", "user_pass", "patient_name"],
#                 on_conditions=[("users.user_id", "patients.users_user_id")], join_type="INNER",)
# first_db.select(table_name=["users", "patients", "visit_dates"],
#                 select_options=["user_name", "user_email", "user_pass", "patient_name", "visit_time"],
#                 on_conditions=[("users.user_id", "patients.users_user_id"),
#                                ("patients.patient_id", "visit_dates.patients_patient_id")], join_type="INNER", )
# show -----------------------------------
# first_db.show_table("users")
# delete -----------------------------------
# first_db.delete_from_table("users", "user_name='shima'")
# update -----------------------------------
# first_db.update_table("users", {"user_name": "'ali'"}, [("user_name", "=", "'shima'")])
# alter -----------------------------------
# first_db.alter_table("users", {"action": "add_column", "column_name": "user_mobil", "column_definition": "bigint"})


# filter_options=[("patient_id", "=", "5")]

