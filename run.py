import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="labana123*"
)
cursor = db.cursor()

# Open and run schema.sql
with open("shema.sql", "r") as f:
    sql_commands = f.read().split(";")

for command in sql_commands:
    if command.strip():
        cursor.execute(command)

print("✅ Shema imported successfully!")
