import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG
from typing import List, Tuple


class Database:    
    @staticmethod
    def get_connection():
        #establish a database connection and return the connection object or none if failed.
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            return connection
        except Error as e:
            print(f"Database connection error: {e}")
            return None
    
    @staticmethod
    def execute_query(query: str, params: tuple = None, fetch: bool = False):

        connection = None
        cursor = None
        try:
            connection = Database.get_connection()
            if connection is None:
                return None
            
            cursor = connection.cursor()
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
                return result
            else:
                connection.commit()
                return cursor.lastrowid
                
        except Error as e:
            print(f"Query execution error: {e}")
            if connection:
                connection.rollback()
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

#m embers
def get_all_members() -> List[Tuple]:
    query = """
        SELECT member_id, first_name, last_name, email, phone,date_of_birth, gender, join_date, status FROM members 
        ORDER BY member_id DESC"""
    return Database.execute_query(query, fetch=True) or []


def add_member(first_name: str, last_name: str, email: str, phone: str, 
               date_of_birth: str, gender: str, status: str) -> bool:
    query = """
        INSERT INTO members (first_name, last_name,email, phone, date_of_birth, gender, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    result = Database.execute_query(query, (first_name, last_name, email, phone, 
                                            date_of_birth, gender, status))
    return result is not None


def update_member(member_id: int, first_name: str, last_name: str, email: str, 
                  phone: str, date_of_birth: str, gender: str, status: str) -> bool:
    query = """
        UPDATE members 
        SET first_name=%s, last_name=%s, email=%s, phone=%s,date_of_birth=%s, gender=%s, status=%s
        WHERE member_id=%s"""
    result = Database.execute_query(query, (first_name, last_name, email, phone, 
                                            date_of_birth, gender, status, member_id))
    return result is not None


def delete_member(member_id: int) -> bool:
    query = "DELETE FROM members WHERE member_id=%s"
    result = Database.execute_query(query, (member_id,))
    return result is not None


def search_members(search_term: str) -> List[Tuple]:
    query = """
        SELECT member_id, first_name, last_name, email, phone,date_of_birth, gender, join_date, status FROM members
        WHERE first_name LIKE %s OR last_name LIKE %s OR email LIKE %s OR phone LIKE %s
        ORDER BY member_id DESC"""
    search_pattern = f"%{search_term}%"
    return Database.execute_query(query, (search_pattern, search_pattern, 
                                         search_pattern, search_pattern), fetch=True) or []
#plans

def get_all_plans() -> List[Tuple]:
    query = """
        SELECT plan_id, plan_name, duration_months, price, description FROM subscription_plans 
        ORDER BY plan_id"""
    return Database.execute_query(query, fetch=True) or []


def add_plan(plan_name: str, duration_months: int, price: float, description: str) -> bool:
    query = """
        INSERT INTO subscription_plans (plan_name, duration_months, price, description)
        VALUES (%s, %s, %s, %s)"""
    result = Database.execute_query(query, (plan_name, duration_months, price, description))
    return result is not None


def update_plan(plan_id: int, plan_name: str, duration_months: int, 
                price: float, description: str) -> bool:
    query = """
        UPDATE subscription_plans 
        SET plan_name=%s, duration_months=%s, price=%s, description=%s
        WHERE plan_id=%s"""
    result = Database.execute_query(query, (plan_name, duration_months, price, 
                                            description, plan_id))
    return result is not None


def delete_plan(plan_id: int) -> bool:
    query = "DELETE FROM subscription_plans WHERE plan_id=%s"
    result = Database.execute_query(query, (plan_id,))
    return result is not None
#subscriptions
def get_all_subscriptions() -> List[Tuple]:
    query = """
        SELECT s.subscription_id, CONCAT(m.first_name, ' ', m.last_name) as member_name,sp.plan_name, s.start_date, s.end_date, s.payment_status
        FROM subscriptions s
        JOIN members m ON s.member_id = m.member_id
        JOIN subscription_plans sp ON s.plan_id = sp.plan_id
        ORDER BY s.subscription_id DESC"""
    return Database.execute_query(query, fetch=True) or []


def add_subscription(member_id: int, plan_id: int, start_date: str, 
                     end_date: str, payment_status: str) -> bool:
    query = """
        INSERT INTO subscriptions (member_id,plan_id, start_date, end_date, payment_status)
        VALUES (%s, %s, %s, %s, %s)"""
    result = Database.execute_query(query, (member_id, plan_id, start_date, 
                                            end_date, payment_status))
    return result is not None


def update_subscription(subscription_id: int, member_id: int, plan_id: int, 
                        start_date: str, end_date: str, payment_status: str) -> bool:
    query = """
        UPDATE subscriptions SET member_id=%s, plan_id=%s, start_date=%s, end_date=%s, payment_status=%s
        WHERE subscription_id=%s"""
    result = Database.execute_query(query, (member_id, plan_id, start_date, 
                                            end_date, payment_status, subscription_id))
    return result is not None


def delete_subscription(subscription_id: int) -> bool:
    query = "DELETE FROM subscriptions WHERE subscription_id=%s"
    result = Database.execute_query(query, (subscription_id,))
    return result is not None
#trainers

def get_all_trainers() -> List[Tuple]:
    query = """
        SELECT trainer_id, first_name, last_name, specialization,email, phone, hire_date, status 
        FROM trainers 
        ORDER BY trainer_id DESC"""
    return Database.execute_query(query, fetch=True) or []


def add_trainer(first_name: str, last_name: str, specialization: str, 
                email: str, phone: str, status: str) -> bool:
    query = """
        INSERT INTO trainers (first_name, last_name, specialization, email, phone, status)
        VALUES (%s, %s, %s, %s, %s, %s)"""
    result = Database.execute_query(query, (first_name, last_name, specialization, 
                                            email, phone, status))
    return result is not None


def update_trainer(trainer_id: int, first_name: str, last_name: str, 
                   specialization: str, email: str, phone: str, status: str) -> bool:
    query = """
        UPDATE trainers 
        SET first_name=%s, last_name=%s, specialization=%s, 
            email=%s, phone=%s, status=%s
        WHERE trainer_id=%s"""
    result = Database.execute_query(query, (first_name, last_name, specialization, 
                                            email, phone, status, trainer_id))
    return result is not None


def delete_trainer(trainer_id: int) -> bool:
    query = "DELETE FROM trainers WHERE trainer_id=%s"
    result = Database.execute_query(query, (trainer_id,))
    return result is not None


def search_trainers(search_term: str) -> List[Tuple]:
    query = """
        SELECT trainer_id, first_name, last_name, specialization,email, phone, hire_date, status 
        FROM trainers 
        WHERE first_name LIKE %s OR last_name LIKE %s OR specialization LIKE %s
        ORDER BY trainer_id DESC"""
    search_pattern = f"%{search_term}%"
    return Database.execute_query(query, (search_pattern, search_pattern, 
                                         search_pattern), fetch=True) or []

# ATTENDANCE Operations
def get_all_attendance() -> List[Tuple]:
    query = """
        SELECT a.attendance_id, CONCAT(m.first_name, ' ', m.last_name) as member_name,a.check_in_time, a.check_out_time
        FROM attendance a
        JOIN members m ON a.member_id = m.member_id
        ORDER BY a.attendance_id DESC"""
    return Database.execute_query(query, fetch=True) or []


def add_attendance(member_id: int, check_in_time: str, check_out_time: str = None) -> bool:
    if check_out_time:
        query = """
            INSERT INTO attendance (member_id, check_in_time, check_out_time)
            VALUES (%s, %s, %s)"""
        result = Database.execute_query(query, (member_id, check_in_time, check_out_time))
    else:
        query = """
            INSERT INTO attendance (member_id, check_in_time)
            VALUES (%s, %s)"""
        result = Database.execute_query(query, (member_id, check_in_time))
    return result is not None


def delete_attendance(attendance_id: int) -> bool:
    query = "DELETE FROM attendance WHERE attendance_id=%s"
    result = Database.execute_query(query, (attendance_id,))
    return result is not None

# stats Operations
def get_statistics() -> dict:
    stats = {}
    
    #total members
    query = "SELECT COUNT(*) FROM members"
    result = Database.execute_query(query, fetch=True)
    stats['total_members'] = result[0][0] if result else 0
    
    #active members
    query = "SELECT COUNT(*) FROM members WHERE status='Active'"
    result = Database.execute_query(query, fetch=True)
    stats['active_members'] = result[0][0] if result else 0
    
    #total trainers
    query = "SELECT COUNT(*) FROM trainers WHERE status='Active'"
    result = Database.execute_query(query, fetch=True)
    stats['active_trainers'] = result[0][0] if result else 0
    
    #total revenue (paid subs)
    query = """
        SELECT COALESCE(SUM(sp.price), 0) FROM subscriptions s
        JOIN subscription_plans sp ON s.plan_id = sp.plan_id
        WHERE s.payment_status = 'Paid' """
    result = Database.execute_query(query, fetch=True)
    stats['total_revenue'] = float(result[0][0]) if result else 0.0
    
    #today's attendance
    query = "SELECT COUNT(*) FROM attendance WHERE DATE(check_in_time) = CURDATE()"
    result = Database.execute_query(query, fetch=True)
    stats['today_attendance'] = result[0][0] if result else 0
    
    return stats

#
def get_members_for_dropdown() -> List[Tuple]:
    query = """
        SELECT member_id, CONCAT(first_name, ' ', last_name) as full_name FROM members 
        WHERE status='Active'
        ORDER BY first_name, last_name"""
    return Database.execute_query(query, fetch=True) or []


def get_plans_for_dropdown() -> List[Tuple]:
    query = "SELECT plan_id, plan_name FROM subscription_plans ORDER BY plan_name"
    return Database.execute_query(query, fetch=True) or []