import sqlite3
import threading
from datetime import datetime
import json
# current_datetime = datetime.now()

# data_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

# codigo = '00100580000115620006565611212'
# data = (codigo,str(data_time))
# data2 = (12,17,17,12,2,1,data_time)

class SqliteManager(threading.Thread):
    def __init__(self,rs232, stop_event):
        super().__init__()
        self.rs232 = rs232
        self.stop_event = stop_event
        self.create_tables()

    def run(self):
        while not self.stop_event.is_set():
            with self.rs232.lock:
                if self.rs232.validation:
                    aux_data = self.rs232.getData()
                    current_datetime = datetime.now()
                    data_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                    self.insert_transaction((aux_data,data_time))

    def add_transaction(self,conn, transaction):
        sql = ''' INSERT INTO transactions(VALUE,DATE)
                VALUES(?,?) '''
        cur = conn.cursor()
        cur.execute(sql, transaction)
        conn.commit()
        return cur.lastrowid

    def add_parameter(self,conn, parameter):
        sql = ''' INSERT INTO parameters(time_turnstile,time_open_actuator,time_close_actuator,time_special_door,time_delay_turnstile,time_delay_special,date)
                VALUES(?,?,?,?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, parameter)
        conn.commit()
        return cur.lastrowid
    def get_transactions(self,conn):
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM transactions")
        filas = cursor.fetchall()
        nombres_columnas = [descripcion[0] for descripcion in cursor.description]
        resultado = [dict(zip(nombres_columnas, fila)) for fila in filas]
        json_resultado = json.dumps(resultado, indent=4)
        conn.close()
        return json_resultado

    def create_tables(self):
        sql_statements = [ 
            """CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY, 
                    value text    NOT NULL, 
                    date timestamp NOT NULL 
            );"""
            ,
            """CREATE TABLE IF NOT EXISTS parameters (
                    id INTEGER PRIMARY KEY, 
                    time_turnstile INTEGER  NOT NULL,
                    time_open_actuator INTEGER NOT NULL,
                    time_close_actuator INTEGER NOT NULL,
                    time_special_door INTEGER NOT NULL,
                    time_delay_turnstile INTEGER NOT NULL,
                    time_delay_special INTEGER NOT NULL,
                    date timestamp INTEGER NOT NULL
            );"""
            ]

        try:
            with sqlite3.connect('app.db') as conn:
                cursor = conn.cursor()
                for statement in sql_statements:
                    cursor.execute(statement)
                
                conn.commit()
        except sqlite3.Error as e:
            print("OCURRIO ALGO")
            print(e)

    def insert_transaction(self,_data):
        try:
            with sqlite3.connect('app.db') as conn:
                transaction_id = self.add_transaction(conn, _data)
                print(f'Created a TRANSACTION with the id {transaction_id}')
        except sqlite3.Error as e:
            print(e)

    def insert_parameter(self,_data):
        try:
            with sqlite3.connect('app.db') as conn:
                parameter_id = self.add_parameter(conn, _data)
                print(f'Created a PARAMETERS with the id {parameter_id}')
        except sqlite3.Error as e:
            print(e)

