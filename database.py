import sqlite3

conn = sqlite3.connect("farmers.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS farmers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    village TEXT,
    crop TEXT
)
""")

cursor.execute("INSERT INTO farmers (name, village, crop) VALUES ('Ramesh', 'Salem', 'Rice')")
cursor.execute("INSERT INTO farmers (name, village, crop) VALUES ('Suresh', 'Madurai', 'Sugarcane')")
cursor.execute("INSERT INTO farmers (name, village, crop) VALUES ('Priya', 'Coimbatore', 'Tomato')")

conn.commit()
conn.close()

print("Database created successfully!")