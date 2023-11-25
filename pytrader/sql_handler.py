import pyodbc
import uuid

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

        self.log.info(f"Creating cursor for {self.database}")
        self.cursor = self.conn.cursor()

    def form_insert_statement(self, table, attributes, values):
        statement = f"INSERT INTO {table} ({attributes}) VALUES ({values})"

        return statement

    def form_update_statement(self, table, attributes, id):
        statement = f"UPDATE {table} SET {attributes} WHERE id = '{id}'"

        return statement

    def execute_statement(self, statement):
        self.log.info(f"Executing statement {statement}")
        self.cursor.execute(statement)

        self.log.info(f"Committing change to {self.cursor.rowcount} row(s)")
        self.cursor.commit()

    def close_cursor(self):
        self.log.info(f"Closing cursor")
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

    def db_write_closed_candle(self, candle):
        try:
            self.execute_statement(self.form_insert_statement("candle", "id,stream_id,open_time,open_price,high_price,low_price,close_price,close_time", f"'{candle.id}', '{candle.stream_id}', '{candle.open_time}', '{candle.open}', '{candle.high}', '{candle.low}', '{candle.close}', '{candle.close_time}'"))

        except Exception as e:
            print(f"Failed to write close candle to database and caught exception {repr(e)}")

    def db_write_open_trade(self, candle, trade_id):
        try:
            self.execute_statement(self.form_insert_statement("trade", "id,open_candle_id,amount1,amount2,status", f"'{trade_id}', '{candle.id}', 1.0, 1.0, 'Open'"))

        except Exception as e:
            print(f"Failed to write open trade to database and caught exception {repr(e)}")

    def db_write_close_trade(self, candle, trade_id):
        try:
            statement = f"""
            DECLARE @trade_id AS VARCHAR(100)
                SET @trade_id = '{trade_id}'

                UPDATE trade
                    SET 
                    	close_candle_id = '{candle.id}',
                        close_price = '{candle.close}',
                        close_timestamp = '{candle.close_time}',
                        status = 'Closed',
                        profit = (
                            SELECT candle_open.close_price - '{candle.close}' as profit
                                FROM trade
                                    LEFT JOIN candle candle_open ON trade.open_candle_id = candle_open.id
                                    LEFT JOIN candle candle_close ON trade.close_candle_id = candle_close.id
                                
                                WHERE trade.id = @trade_id
                        )

                    WHERE id = @trade_id
            """

            self.execute_statement(statement)

        except Exception as e:
            print(f"Failed to write close trade to database and caught exception {repr(e)}")