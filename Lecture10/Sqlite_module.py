import sqlite3

conn = sqlite3.connect('mydatabase.db')

cur = conn.cursor()

# Create a table
cur.execute('''
	CREATE TABLE IF NOT EXISTS users (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		name TEXT NOT NULL,
		age INTEGER NOT NULL,
		city TEXT NOT NULL
	)
''')

# Insert some data into the table
cur.execute("INSERT INTO users (name, age, city) VALUES ('Alice', 25, 'New York')")
cur.execute("INSERT INTO users (name, age, city) VALUES ('Bob', 30, 'Los Angeles')")
cur.execute("INSERT INTO users (name, age, city) VALUES ('Charlie', 35, 'Chicago')")

# Commit the changes
conn.commit()

# Query the data and display the results
cur.execute("SELECT * FROM users WHERE age > 28")
rows = cur.fetchall()

print("Users older than 28:")
for row in rows:
	print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, City: {row[3]}")

# Close the connection
conn.close()
