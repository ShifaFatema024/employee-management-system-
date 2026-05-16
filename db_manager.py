import os
import sys
import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILENAME = os.path.join(BASE_DIR, "data.env")


load_dotenv(FILENAME)

class DatabaseManager:
    def __init__(self):
        self.pool = pooling.MySQLConnectionPool(
            pool_name = "emp_pool" ,
            pool_size = 5,
            host = os.getenv("DB_HOST"),
            user = os.getenv("DB_USER"),
            password = os.getenv("DB_PASS"),
            database = os.getenv("DB_NAME")
        )
    print("Connection Pool Created!")

    def get_cursor(self):
        try:
            conn = self.pool.get_connection()
            return conn, conn.cursor(dictionary=True)
        except ValueError:
            print("try again")

    def execute_query(self,query,params = None, fatch = False):
        conn, cursor = self.get_cursor()
        try:
            cursor.execute(query,params or ())
            if fatch == True:
                return cursor.fetchall()
            conn.commit()
            return cursor.rowcount
        finally:
            cursor.close()
            conn.close()
            
class emplyeemanager(DatabaseManager):
    
    def __init__(self):
        super().__init__()

    def create_table(self):
        try:
            query = """
            CREATE TABLE IF NOT EXISTS emp(
            id INT PRIMARY KEY,
            ename VARCHAR(20),
            salary FLOAT
            )
            """
            self.execute_query(query)
            print("Table created!")
        except ValueError:
            return "try again!" 

    def search_records(self,name,):
        try:
                q = "SELECT * FROM emp WHERE ename LIKE %s"
                results = self.execute_query(q,(f"%{name}%",),fatch = True)
                return results if results is not None else [] # Agar kuch na mile toh khali list bhejien
        except Exception as e:
            print(f"Error: {e}")
            return []
                
             

    def add_emplyee(self,id,name,salary,):
        try:
            q = "INSERT INTO emp (id, ename, salary) VALUES (%s, %s, %s)"
            self.execute_query(q, (id, name,salary,))
            return "Record added successfully!"
        except ValueError:
                    return "Invalid input! Please enter numbers for ID and Salary."
        except Exception as e:
            return (f"Error: {e}")


    def show_all(self):
        try:
            records = self.execute_query("SELECT * FROM emp",fatch = True)
            return records
        except Exception as e:
            return []        

    def update_employee(self,eid,new_salary,):
        try:
            q = "UPDATE emp SET salary = %s WHERE id = %s"
            self.execute_query(q,(new_salary,eid))
            return "salary updated!"
        except ValueError:
            return "try again!"

    def delete_employee(self,eid):
        try:
            q = "DELETE FROM emp WHERE id = %s"
            self.execute_query(q,(eid,))
            return "record deleted!"
        except ValueError:
            return "try again!"

