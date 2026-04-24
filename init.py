import mysql.connector

try:
    db = mysql.connector.connect(
        host="database-1.cfonvzfkm37u.us-east-1.rds.amazonaws.com",
        user="admin",
        port="3306",
        password="xxxxxx"  
    )
    cursor = db.cursor()
    sql_commands = [
        "DROP DATABASE IF EXISTS lab4;",
        "CREATE DATABASE IF NOT EXISTS lab4;",
        "USE lab4;",
        """
        CREATE TABLE IF NOT EXISTS Students (
            Name varchar(40) NOT NULL,
            ID varchar(40) NOT NULL,
            Department varchar(40) NOT NULL,
            Email varchar(40) DEFAULT NULL,
            PRIMARY KEY (ID)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        """
    ]

    for command in sql_commands:
        cursor.execute(command)
        print(f"success: {command.split()[0]}...")
    print("lab4 database and Students table established")

    print("--- database ---")
    cursor.execute("SHOW DATABASES")
    for (db_name,) in cursor:
        print(f"{db_name}")
 

except mysql.connector.Error as err:
    print(f"error: {err}")

finally:
    if 'db' in locals() and db.is_connected():
        cursor.close()
        db.close()
