import pyodbc

class SqlController():

    def __init__(self, driver, server, database, username, password, pair, timeframe, file_name, log):
        self.driver = driver
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.pair = pair
        self.timeframe = timeframe
        self.file_name = file_name
        self.log = log

        self.conn_string = 'DRIVER={'+self.driver+'};SERVER='+self.server+';DATABASE='+self.database+';UID='+self.username+';PWD='+self.password
        self.conn = pyodbc.connect(self.conn_string)

        print(f"Creating cursor for {self.database}")
        self.cursor = self.conn.cursor()

    def form_insert_statement(self, table, attributes, values):
        statement = f"INSERT INTO {table} ({attributes}) VALUES ({values})"

        return statement

    def form_update_statement(self, table, attributes, id):
        statement = f"UPDATE {table} SET {attributes} WHERE id = '{id}'"

        return statement

    def execute_statement(self, statement):
        print(f"Executing statement {statement}")
        self.cursor.execute(statement)

        print(f"Committing change to insert {self.cursor.rowcount} row(s)")
        self.cursor.commit()

    def close_cursor(self):
        print(f"Closing cursor")
        self.cursor.close()

    def db_write_start_stream(self, stream_id):
        try:
            self.execute_statement(self.form_insert_statement("stream", "id,start_time,log_filename,pair,timeframe", f"'{stream_id}', CURRENT_TIMESTAMP, '{self.file_name}', '{self.pair}', '{self.timeframe}'"))

        except Exception as e:
            print(f"Failed to write start stream to database and caught exception {repr(e)}")

    def db_write_end_stream(self, stream_id):
        try:
            self.execute_statement(self.form_update_statement("stream", "end_time=CURRENT_TIMESTAMP", f"{stream_id}"))
        
        except Exception as e:
            print(f"Failed to write end stream to database and caught exception {repr(e)}")