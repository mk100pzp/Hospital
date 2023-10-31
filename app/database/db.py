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
