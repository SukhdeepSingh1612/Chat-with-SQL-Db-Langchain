import sqlite3


## connect to sqlite3
connection = sqlite3.connect("student.db")

## Create a cursor object to insert record, create table
cursor =connection.cursor()


## create the table
table_info =  """
create table STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25),
SECTION VARCHAR(25), MARKS INT)
"""


cursor.execute(table_info)


## Insert some more records
cursor.execute("""Insert Into STUDENT values('Sukhdeep', 'Artificial Intelligence', 'A+', 95)""")
cursor.execute("""Insert Into STUDENT values('John', 'Artificial Intelligence', 'B', 75)""")
cursor.execute("""Insert Into STUDENT values('Mukesh', 'DevOps', 'C', 50)""")
cursor.execute("""Insert Into STUDENT values('Jacob', 'DevOps Intelligence', 'A', 90)""")


## Display all the records
print("The inserted records are")
data = cursor.execute("""
                    SELECT * from STUDENT""")

for row in data:
    print(row)

## Commit your changes in the database
connection.commit()
connection.close()

