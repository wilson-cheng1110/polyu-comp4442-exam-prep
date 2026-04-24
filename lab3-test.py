import mysql.connector

mydb = mysql.connector.connect( host =
							    '',
	user = '',
	port = '',
	database = '',
	passwd = '')

mycursor = mydb.cursor()
mycursor.execute("select * from Persons")

myresult = mycursor.fetchall()

for x in myresult:
	print(x)
