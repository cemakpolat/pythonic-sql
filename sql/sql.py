"""
@author: Cem Akpolat
@created by cemakpolat at 2021-09-18
"""
import mysql.connector


class DataTypes:
    # numeric
    bit = "BIT"
    tinyint = "TINYINT"
    smallint = "SMALLINT"
    int = "INT"
    bigint = "BIGINT"
    decimal = "DECIMAL"
    numeric = "NUMERIC"
    float = "FLOAT"
    real = "REAL"

    # date/time
    date = "DATE"  # YYYY-MM-DD
    time = "TIME"  # HH:MI:SS
    datetime = "DATETIME"  # YYYY-MM-DD HH:MI:SS
    timestamp = "TIMESTAMP"  # Unix epoch (‘1970-01-01 00:00:00’ UTC)
    year = "YEAR"  # in 2 dgits or 4 digits

    # character/String
    char = "CHAR"
    varchar = "VARCHAR"
    text = "TEXT"

    # unicode /string
    nchar = "NCHAR"
    nvarchar = "NVARCHAR"
    ntext = "NTEXT"

    # binary
    binary = "BINARY"
    varbinary = "VARBINARY"
    image = "IMAGE"

    # misc
    clob = "CLOB"
    blob = "BLOB"
    xml = "XML"
    json = "JSON"


class DBConfig:
    def __init__(self,user, password, host, database):
        self.user = user
        self.password = password
        self.database = database
        self.host = host

    @staticmethod
    def get_connection(self):
        print(self.user, self.password, self.host)
        connection = mysql.connector.connect(user=self.user, password=self.password,
                                             host=self.host,
                                             database=self.database,
                                             auth_plugin='mysql_native_password')
        return connection


class Create(DBConfig):

    def __init__(self,user, password, host, database):
        super().__init__(user, password, host, database)
        self.table_name = None
        self.columns = []
        self.fkeys = []
        self.pkeys = []
        self.sql = None

    def table(self, name):
        self.table_name = name
        return self

    def column(self, name, vtype, vlength=None):
        if name and vtype:
            self.columns.append({"name": name, "type": vtype, "length": vlength})
        else:
            print("name or type is not properly defined")
        return self

    def set_pkey(self, c_name, auto_increment=True):
        exist = False
        for col in self.columns:
            if "pkey" in col:
                exist = True
                break

        if exist:
            print("there is already a primary key")
        else:
            for col in self.columns:
                if col["name"] == c_name:
                    col["pkey"] = True
                    if auto_increment:
                        col["auto_increase"] = True
                        break
        return self

    def set_pkeys(self, c_names):
        if len(c_names) > 0:
            self.pkeys = c_names
        return self

    def add_fkey(self, table_id, foreign_table_name, foreign_column_id):
        if table_id and foreign_column_id and foreign_table_name:
            self.fkeys.append(
                {"host_column_id": table_id, "fkey_table": foreign_table_name, "fkey_id": foreign_column_id})
        return self

    def apply(self):

        self.sql = "CREATE TABLE " + self.table_name + " ("

        column_types = ""

        for item in self.columns:

            if "pkey" in item and len(self.pkeys) == 0:
                column_types += item["name"] + " " + item["type"] + " AUTO_INCREMENT PRIMARY KEY,"

            elif item["type"] is DataTypes.int:
                column_types += item["name"] + " " + item["type"] + ","
            else:
                column_types += item["name"] + " " + item["type"] + "(" + str(item["length"]) + "),"

        for item in self.fkeys:
            column_types += "FOREIGN KEY(" + item["host_column_id"] + ") REFERENCES " + item["fkey_table"] + \
                            "(" + item["fkey_id"] + "),"

        if len(self.pkeys) > 0:
            column_types += " PRIMARY KEY("
            for item in self.pkeys:
                column_types += item + ","

            column_types = column_types[:-1]
            column_types += ")"
        else:
            column_types = column_types[:-1]

        self.sql += column_types  # remove last comma character
        self.sql += ");"
        print(self.sql)
        self.execute()

    def execute(self):
        connection = self.get_connection(self)
        try:

            connection.cursor().execute(self.sql)
            connection.commit()

        except mysql.connector.Error as error:
            print("Failed to create table in MySQL: {}".format(error))
        finally:
            if connection.is_connected():
                connection.close()
                #  cursor.close()
                print("MySQL connection is closed")

        self.clean()

    def clean(self):
        self.table_name = None
        self.columns = []
        self.fkeys = []
        self.pkeys = []
        self.sql = None


class Insert(DBConfig):
    def __init__(self,user, password, host, database):
        super().__init__(user, password, host, database)
        self.table_name = None
        self.columns_values = []
        self.column_values = []
        self.values = None
        self.sql = None

    def table(self, name):
        self.table_name = name
        return self

    def columns(self, columns, values):

        column_str = "("
        pattern = "("
        for col in columns:
            column_str += col + ","
            pattern += "%s,"
        column_str = column_str[:-1] + ")"
        pattern = pattern[:-1] + ")"
        self.columns_values.append({"columns": column_str, "pattern": pattern, "values": values})
        return self

    def column(self, cname, value):
        self.column_values.append({"column": cname, "value": value})
        return self

    def apply(self):

        self.sql = "INSERT INTO " + self.table_name

        if len(self.column_values) > 0:
            column_str = ""
            pattern = ""
            val = []
            for col in self.column_values:
                column_str += col["column"] + ","
                pattern += "%s,"
                val.append(col["value"])

            column_str = "(" + column_str[:-1] + ")"
            pattern = "(" + pattern[:-1] + ")"
            self.sql += column_str + " VALUES " + pattern

            values = (val)
            self.values = [values]
        elif len(self.columns_values) > 0:
            item = self.columns_values[0]
            self.sql += item["columns"] + " VALUES " + item["pattern"]
            self.values = item["values"]
            print(self.values)
        else:
            print("there is neither columns nor values")

        print(self.sql)
        self.execute()

    def execute(self):
        connection = self.get_connection(self)
        try:
            print(self.values)
            connection.cursor().executemany(self.sql, self.values)
            connection.commit()

        except mysql.connector.Error as error:
            print("Failed to create table in MySQL: {}".format(error))
        finally:
            if connection.is_connected():
                connection.close()
                #  cursor.close()
                print("MySQL connection is closed")

        self.clean()

    def clean(self):
        self.table_name = None
        self.columns_values = []
        self.column_values = []
        self.values = None
        self.sql = None


class Select(DBConfig):
    def __init__(self,user, password, host, database):
        super().__init__(user, password, host, database)
        self.table_name = None
        self.column_names = []
        self.wheres = []
        self.tables = []
        self.order_bys = []
        self.group_bys = []
        self.joins = []
        self.sql = None
        self.likes = []
        self.betweens = []
        self.result = None


    def table(self, name):
        self.table_name = name
        return self

    def column(self, col_name):
        self.column_names.append(col_name)
        return self

    def columns(self, col_array):
        for col in col_array:
            if col in self.column_names:
                continue
            else:
                self.column_names.append(col)

        return self

    def group_by(self, column):
        self.group_bys.append(column)
        return self

    def orderby(self, column, operator):
        if operator == "DESC" or operator == "ASC":
            self.order_bys.append({"column": column, "operator": operator})
        else:
            print("invalid operator")
        return self

    def where(self, conditions):

        for cond in conditions:
            if ("<=" and "=<") in cond or ("<=!" and "!=<") in cond:  # BETWEEN and NOT BETWEN

                if ("<=!" and "!=<") in cond:  # NOT BETWEEN
                    first = cond.split("<=!")
                    second = first[1].split("!=<")
                    self.wheres.append(second[0] + " NOT BETWEEN " + first[0] + " AND " + second[1])

                elif ("<=" and "=<") in cond:  # BETWEEN
                    first = cond.split("<=")
                    second = first[1].split("=<")
                    self.wheres.append(second[0]+" BETWEEN " + first[0] + " AND " + second[1])

            elif "!=" in cond:  # NOT and NOT IN

                arr = cond.split("!=")
                arr_list = arr[1].strip("[]").split(",")
                if len(arr_list) > 1:
                    self.wheres.append(arr[0] + " NOT IN ("+arr[1].strip("[]") +")")
                else:
                    self.wheres.append("NOT " + arr[0] + "=" + arr[1])

            elif "|" in cond:  # OR
                arr = cond.replace("|", "OR")
                self.wheres.append(arr)

            elif "~" in cond or "!~" in cond:  # LIKE und NOT LIKE
                if "!~" in cond:
                    arr = cond.split("!~")
                    self.wheres.append(arr[0] + " NOT LIKE " + arr[1])
                else:
                    arr = cond.split("~")
                    self.wheres.append(arr[0] + " LIKE " + arr[1])

            elif "=" in cond or ">" in cond or "<" in cond or ">=" in cond or "<=" in cond or "<>" in cond:  # WHERE
                arr = cond.split("=")
                if isinstance(arr[0], list):  # IN
                    # operation is here IN
                    self.wheres.append({"operator": "IN", "values": arr[1], "column": arr[0]})
                else:
                    print(cond)
                    self.wheres.append(cond)

        return self

    def innerjoin(self, table, condition):
        self.joins.append({"type":"innerjoin", "table":table, "condition":condition})
        return self

    def leftjoin(self,table, condition):
        self.joins.append({"type":"leftjoin", "table":table, "condition":condition})
        return self

    def rightjoin(self, table, condition):
        self.joins.append({"type":"rightjoin", "table":table, "condition":condition})
        return self

    def fulljoin(self, table, condition):
        self.joins.append({"type":"fulljoin", "table":table, "condition":condition})
        return self

    def apply(self):

        self.sql = "SELECT "

        cols = ""
        for col in self.column_names:
            cols += col + ","

        self.sql += cols[:-1] + " FROM " + self.table_name

        joins = ""

        for item in self.joins:
            if item["type"] == "innerjoin":
                joins += " INNER JOIN " + item["table"] + " ON " + item["condition"]
            elif item["type"] == "leftjoin":
                joins += " LEFT JOIN " + item["table"] + " ON " + item["condition"]
            elif item["type"] == "rightjoin":
                joins += " RIGHT JOIN " + item["table"] + " ON " + item["condition"]
            elif item["type"] == "fulljoin":
                joins += " FULL JOIN " + item["table"] + " ON " + item["condition"]

        self.sql += joins

        where = ""
        if len(self.wheres) > 0:
            where = " WHERE "
        for item in self.wheres:
            where += "(" + item + ")" + " AND "
        self.sql += where[:-5]

        orderby = ""
        for item in self.order_bys:
            orderby += " ORDER BY " + item["column"] + " " + item["operator"]

        self.sql += orderby

        groupby = ""
        for item in self.group_bys:
            groupby += " GROUP BY " + item
        self.sql += groupby

        self.execute()

    def execute(self):
        connection = self.get_connection(self)
        cursor = connection.cursor(buffered=True)
        try:
            print(self.sql)
            cursor.execute(self.sql)
            connection.commit()
            result = cursor.fetchall()
            self.result = result
            print(self.result[0])

        except mysql.connector.Error as error:
            print("Failed to create table in MySQL: {}".format(error))
        finally:
            if connection.is_connected():
                connection.close()
                print("MySQL connection is closed")

        self.clean()

    def clean(self):
        self.table_name = None
        self.column_names = []
        self.wheres = []
        self.tables = []
        self.order_bys = []
        self.group_bys = []
        self.joins = []
        self.sql = None
        self.likes = []
        self.betweens = []


class Update(DBConfig):
    def __init__(self,user, password, host, database):
        super().__init__(user, password, host, database)
        self.table_name = None
        self.column_values = []
        self.columns_values = []
        self.wheres = []

    def table(self, name):
        self.table_name = name
        return self

    def columns(self, columns, values):

        for index in range(len(columns)):
            if type(values[index]) is str:
                value = "\"" + values[index] + "\""
            self.columns_values.append(columns[index] + " = " +value)
        return self

    def column(self, cname, value):
        if type(value) is str:
            value = "\""+value+"\""
        self.column_values.append(cname + " = " + value)
        return self

    def where(self, condition):
        if "<" in condition or ">" in condition or "=" in condition or ">=" in condition or "<=" in condition or "<>" in condition:
            self.wheres.append(condition)
        else:
            print("invalid operator")
        return self

    def apply(self):

        self.sql = "UPDATE " + self.table_name + " SET "
        if len(self.column_values) > 0:
            cols = ""
            for item in self.column_values:
                cols += item + ","
            self.sql += cols[:-1]
        elif len(self.columns_values) > 0:
            cols = ""
            for item in self.columns_values:
                cols += item + ","
            self.sql += cols[:-1]
        else:
            print(" The operation could not be applied, since neither column nor value are given")
        self.sql += " WHERE "
        if len(self.wheres) > 0:
            where = ""
            for item in self.wheres:
                where += item + ","
            self.sql += where[:-1]
            print(self.sql)
            self.execute()
        else:
            print("At least a single where clause must have!")

    def execute(self):
        connection = self.get_connection(self)
        try:
            connection.cursor().execute(self.sql)
            connection.commit()

        except mysql.connector.Error as error:
            print("Failed to create table in MySQL: {}".format(error))
        finally:
            if connection.is_connected():
                connection.close()
                #  cursor.close()
                print("MySQL connection is closed")

        self.clean()

    def clean(self):
        self.table_name = None
        self.column_values = []
        self.columns_values = []
        self.wheres = []


class Delete(DBConfig):
    def __init__(self,user, password, host, database):
        super().__init__(user, password, host, database)
        self.table_name = None
        self.drop_table = False
        self.sql = None
        self.wheres = []

    def table(self, name):
        self.table_name = name
        return self

    def where(self, condition):
        if "<" in condition or ">" in condition or "=" in condition or ">=" in condition or "<=" in condition or "<>" in condition:
            self.wheres.append(condition)
        else:
            print("invalid operator")
        return self


    def drop(self):
        self.drop_table = True
        return self

    def apply(self):

        self.sql = "DELETE FROM " + self.table_name

        if len(self.wheres) > 0:
            content = " WHERE "
            for item in self.wheres:
                content += item + " AND "
            self.sql += content[:-5]  # -5 removes the " AND " word that corresponds to 5 charachters
            self.sql += ";"
        elif self.drop_table:
            self.sql = "DROP TABLE IF EXISTS " + self.table_name + ";"

        self.execute()

    def execute(self):
        connection = self.get_connection(self)
        try:
            print(self.sql)
            connection.cursor().execute(self.sql)
            connection.commit()

        except mysql.connector.Error as error:
            print("Failed to create table in MySQL: {}".format(error))
        finally:
            if connection.is_connected():
                connection.close()
                #  cursor.close()
                print("MySQL connection is closed")

        self.clean()

    def clean(self):
        self.table_name = None
        self.drop_table = False
        self.sql = None
        self.wheres = []

records = [("cem","akpolat")]
insert = Insert("arduino", "arduino", "127.0.0.1", "university")
#insert.table('reviewers').columns(["name", "surname"], records).apply()
insert.table('reviewers').column("name", "levin").column("surname", "levin").apply()




# select = Select("arduino", "arduino", "127.0.0.1", "university")
# select.table("reviewers").columns(["*"]).where(["id=6"]).apply()
#     where(["10<=!price!=<20","categortyid!=[1,2,3]","a!=b","c>d","d<x | d=y | a=b","w=m","t=m","column ~ a"]).orderby("a.column","ASC").\
#     apply()
