import sqlite3


conn = sqlite3.connect('bot.db')
c = conn.cursor()

c.execute("""CREATE TABLE encouragements (
  id INTEGER PRIMARY KEY,
  encouring_message TEXT
)""")

c.execute("INSERT INTO encouragements (encouring_message) VALUES ('Cheer up!')")
c.execute("INSERT INTO encouragements (encouring_message) VALUES ('Hang in there.')")
c.execute("INSERT INTO encouragements (encouring_message) VALUES ('You are a great person!')")

conn.commit()
