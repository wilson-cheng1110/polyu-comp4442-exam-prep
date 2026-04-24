import mysql.connector

try:
    db = mysql.connector.connect(
        host="database-1.cfonvzfkm37u.us-east-1.rds.amazonaws.com",
        user="admin",
        port="3306",
        password="12345678"  
    )
    cursor = db.cursor()
    sql_commands = [
        "DROP DATABASE IF EXISTS lab6;",
        "CREATE DATABASE IF NOT EXISTS lab6;",
        "USE lab6;",
        """
            CREATE TABLE IF NOT EXISTS Monitor
            (
            id int(11) unsigned NOT NULL AUTO_INCREMENT,
            num int(11) DEFAULT NULL,
            ctime bigint(11) DEFAULT NULL,
            PRIMARY KEY (id) 
            ) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8;
        """
    ]

    for command in sql_commands:
        cursor.execute(command)
        print(f"success: {command.split()[0]}...")
    print("lab6 database and Monitor table established")

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
