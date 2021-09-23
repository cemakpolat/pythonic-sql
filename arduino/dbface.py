"""
@author: Cem Akpolat
@created by cemakpolat at 2021-09-13
"""
import mysql.connector


DB_NAME = "university"
TABLE_NAME = "doorscards"
COLUMN_DOORID = "doorid"
COLUMN_CARDID = "cardid"

myconn = None

def get_connection(database=None):
    return mysql.connector.connect(user='arduino', password='arduino',
                                            host='127.0.0.1',
                                            database = database,
                                            auth_plugin='mysql_native_password')

def initial_setup():

    """
    1. create database
    2. create table
    3. add doors and cards id
    4. get doors id from table

    :return:
    """
    create_database()
    db_connection = get_connection(DB_NAME)
    create_table(db_connection)
    insert_doorcard_data(db_connection)
    select(db_connection)


def list_dbs(conn):

    mycursor = conn.cursor()
    mycursor.execute("SHOW DATABASES")
    dbs = []
    for x in mycursor:
        dbs.append(x[0])
    return dbs


def select(conn):
    mycursor = conn.cursor()

    mycursor.execute("SELECT * FROM " + TABLE_NAME)

    myresult = mycursor.fetchall()

    for x in myresult:
        print(x)


def get_authorized_doors(cardid, conn):
    door_list = []
    mycursor = conn.cursor()

    sql = "SELECT "+COLUMN_DOORID+" FROM "+TABLE_NAME+" WHERE "+COLUMN_CARDID+"='"+cardid+"'"
    mycursor.execute(sql)

    myresult = mycursor.fetchall()

    for x in myresult:
        door_list.append(x[0])
    return door_list


def create_database():
    db_connection = get_connection()
    existing_dbs = list_dbs(db_connection)

    if DB_NAME in existing_dbs:
        delete_db(db_connection)

    mycursor = db_connection.cursor()
    mycursor.execute("CREATE DATABASE "+DB_NAME)


def create_table(conn):
    """
    We use the statement "INT AUTO_INCREMENT PRIMARY KEY" which will insert a unique number for each record. Starting at 1, and increased by one for each record.
    :return:
    """
    mycursor = conn.cursor()

    mycursor.execute(
        "CREATE TABLE "+TABLE_NAME+" (id INT AUTO_INCREMENT PRIMARY KEY,"+COLUMN_DOORID+" VARCHAR(100), "+COLUMN_CARDID+" VARCHAR(255))")


def insert_doorcard_data(conn):
    mycursor = conn.cursor()

    sql = "INSERT INTO "+TABLE_NAME+" ("+COLUMN_DOORID+", "+COLUMN_CARDID+") VALUES (%s, %s)"
    val = [
        ('01', 'AABBCC'),
        ('02', 'AABBCC'),
        ('03', 'AABBCC'),
        ('01', 'AABBDD'),
        ('02', 'AABBDD'),
        ('01', 'AABBXX'),
    ]

    mycursor.executemany(sql, val)

    conn.commit()


def delete_table(conn):
    mycursor = conn.cursor()

    sql = "DROP TABLE IF EXISTS "+TABLE_NAME

    mycursor.execute(sql)


def delete_db(conn):
    mycursor = conn.cursor()
    mycursor.execute("DROP DATABASE IF EXISTS "+DB_NAME)

def delete_all():
    delete_table()
    delete_db()

initial_setup()

