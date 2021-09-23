# """
# @author: Cem Akpolat
# @created by cemakpolat at 2021-09-14
# """
#
#
# def update():
#
#     mycursor = mydb.cursor()
#
#     sql = "UPDATE customers SET address = 'Canyon 123' WHERE address = 'Valley 345'"
#
#     mycursor.execute(sql)
#
#     mydb.commit()
#
#     print(mycursor.rowcount, "record(s) affected")
#
#     mycursor = mydb.cursor()
#
#     sql = "UPDATE customers SET address = %s WHERE address = %s"
#     val = ("Valley 345", "Canyon 123")
#
#     mycursor.execute(sql, val)
#
#     mydb.commit()
#
# def delete():
#     mycursor = mydb.cursor()
#
#     sql = "DROP TABLE customers"
#     sql = "DROP TABLE IF EXISTS customers"
#
#     mycursor.execute(sql)
#
# def deleteRecord():
#     mycursor = mydb.cursor()
#
#     sql = "DELETE FROM customers WHERE address = 'Mountain 21'"
#
#     mycursor.execute(sql)
#
#     # mycursor = mydb.cursor()
#     #
#     # sql = "DELETE FROM customers WHERE address = %s"
#     # adr = ("Yellow Garden 2",)
#     #
#     # mycursor.execute(sql, adr)
#
#     mydb.commit()
#
#     print(mycursor.rowcount, "record(s) deleted")
#
# def sort():
#     mycursor = mydb.cursor()
#
#     sql = "SELECT * FROM customers ORDER BY name"
#
#     mycursor.execute(sql)
#
#     myresult = mycursor.fetchall()
#
#     for x in myresult:
#         print(x)
#
# def select():
#     mycursor = mydb.cursor()
#
#     sql = "SELECT * FROM customers WHERE address ='Park Lane 38'"
#
#     # sql = "SELECT * FROM customers WHERE address = %s"
#     # adr = ("Yellow Garden 2",)
#     #
#     # mycursor.execute(sql, adr)
#     #
#     mycursor.execute(sql)
#
#     myresult = mycursor.fetchall()
#
#     for x in myresult:
#         print(x)
#
# def select_column():
#     mycursor = mydb.cursor()
#
#     mycursor.execute("SELECT name, address FROM customers")
#
#     myresult = mycursor.fetchall()
#
#     for x in myresult:
#         print(x)
#
# def select_table():
#     mycursor = mydb.cursor()
#
#     mycursor.execute("SELECT * FROM customers")
#
#     myresult = mycursor.fetchall()
#
#     for x in myresult:
#         print(x)
#
# def select_one():
#     mycursor = mydb.cursor()
#
#     mycursor.execute("SELECT * FROM customers")
#
#     myresult = mycursor.fetchone()
#
#     print(myresult)
#
# def insert():
#     mycursor = mydb.cursor()
#
#     sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
#     val = ("John", "Highway 21")
#     mycursor.execute(sql, val)
#
#     mydb.commit()
#
#     print(mycursor.rowcount, "record inserted.")
#
#
# def insert_all():
#     mycursor = mydb.cursor()
#
#     sql = "INSERT INTO doorscards (doorid, cardid) VALUES (%s, %s)"
#     val = [
#         ('Peter', 'Lowstreet 4'),
#         ('Amy', 'Apple st 652'),
#         ('Hannah', 'Mountain 21'),
#         ('Michael', 'Valley 345'),
#         ('Sandy', 'Ocean blvd 2'),
#         ('Betty', 'Green Grass 1'),
#         ('Richard', 'Sky st 331'),
#         ('Susan', 'One way 98'),
#         ('Vicky', 'Yellow Garden 2'),
#         ('Ben', 'Park Lane 38'),
#         ('William', 'Central st 954'),
#         ('Chuck', 'Main Road 989'),
#         ('Viola', 'Sideway 1633')
#     ]
#
#     mycursor.executemany(sql, val)
#
#     mydb.commit()
#
# def get_id_of_inserted():
#     mycursor = mydb.cursor()
#
#     sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
#     val = ("Michelle", "Blue Village")
#     mycursor.execute(sql, val)
#
#     mydb.commit()
#
#     print("1 record inserted, ID:", mycursor.lastrowid)
#
# def create_table():
#     mycursor = mydb.cursor()
#
#     sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
#     val = ("Michelle", "Blue Village")
#     mycursor.execute(sql, val)
#
#     mydb.commit()
#
#     print("1 record inserted, ID:", mycursor.lastrowid)
#
# def list_tablbes():
#     mycursor = mydb.cursor()
#
#     mycursor.execute("SHOW TABLES")
#
#     for x in mycursor:
#         print(x)
#
# def create_pk():
#     """
#     We use the statement "INT AUTO_INCREMENT PRIMARY KEY" which will insert a unique number for each record. Starting at 1, and increased by one for each record.
#     :return:
#     """
#     mycursor = mydb.cursor()
#
#     mycursor.execute(
#         "CREATE TABLE doorscards (id INT AUTO_INCREMENT PRIMARY KEY, door VARCHAR(100), cardid VARCHAR(255))")
#
# def alter_table():
#     """
#     If the table already exists, use the ALTER TABLE keyword:
#
#
#     :return:
#     """
#
#     mycursor = mydb.cursor()
#
#     mycursor.execute("ALTER TABLE customers ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")
#
# def create_db():
#
#     mycursor = mydb.cursor()
#     mycursor.execute("CREATE DATABASE permissions")
#
#
# def delete_db():
#     mycursor = mydb.cursor()
#     mycursor.execute("DROP DATABASE blog;")
#
# def list_db():
#     mycursor = mydb.cursor()
#
#     mycursor.execute("SHOW DATABASES")
#
#     for x in mycursor:
#         print(x)
#
# def get_limit():
#     mycursor = mydb.cursor()
#
#     mycursor.execute("SELECT * FROM customers LIMIT 5")
#
#     myresult = mycursor.fetchall()
#
#     for x in myresult:
#         print(x)
#
# def join():
#     mycursor = mydb.cursor()
#
#     sql = "SELECT \
#       users.name AS user, \
#       products.name AS favorite \
#       FROM users \
#       INNER JOIN products ON users.fav = products.id"
#
#     mycursor.execute(sql)
#
#     myresult = mycursor.fetchall()
#
#     for x in myresult:
#         print(x)
#
# def left_join():
#     """
#     In the example above, Hannah, and Michael were excluded from the result, that is because INNER JOIN only shows the records where there is a match.
#
# If you want to show all users, even if they do not have a favorite product, use the LEFT JOIN statement:
#     :return:
#     """
#     mycursor = mydb.cursor()
#
#     sql = "SELECT \
#       users.name AS user, \
#       products.name AS favorite \
#       FROM users \
#       LEFT JOIN products ON users.fav = products.id"
#
#     mycursor.execute(sql)
#
#     myresult = mycursor.fetchall()
#
#     for x in myresult:
#         print(x)
# def right_join():
#     """
#     If you want to return all products, and the users who have them as their favorite, even if no user have them as their favorite, use the RIGHT JOIN statement:
#
#
#     :return:
#     """
#     mycursor = mydb.cursor()
#
#     sql = "SELECT \
#       users.name AS user, \
#       products.name AS favorite \
#       FROM users \
#       RIGHT JOIN products ON users.fav = products.id"
#
#     mycursor.execute(sql)
#
#     myresult = mycursor.fetchall()
#
#     for x in myresult:
#         print(x)