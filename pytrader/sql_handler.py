import pyodbc

class SqlController():

    def __init__(self, driver, server, database, username, password):
        self.driver = driver
        self.server = server
        self.database = database
        self.username = username
        self.password = password

        self.conn_string = 'DRIVER={'+self.driver+'};SERVER='+self.server+';DATABASE='+self.database+';UID='+self.username+';PWD='+self.password
        self.conn = pyodbc.connect(self.conn_string)

        self.cursor = self.conn.cursor()

        print("connected")

    def insert(self, table, attributes, values):
        statement = f"""
            INSERT INTO {table} 
                    ({attributes})
                VALUES 
                    ({values})
        """

        result = self.cursor.execute(statement)

        cursor = self.cursor.commit()

        print("inserted")

    def update(self, table, attributes, id):
        statement = f"""
            UPDATE {table}
                SET {attributes}
            WHERE id = '{id}'
        """

        result = self.cursor.execute(statement)

        cursor = self.cursor.commit()

        print("updated")
    
    def close_cursor(self):
        cursor = self.cursor.close()

        print("closed")