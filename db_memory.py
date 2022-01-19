import sqlite3
import random

conn = sqlite3.connect(':memory:')

c = conn.cursor()

c.execute("""CREATE TABLE encouragements (
  id INTEGER PRIMARY KEY,
  encouring_message TEXT
)""")

c.execute("INSERT INTO encouragements (encouring_message) VALUES ('Cheer up!')")
c.execute("INSERT INTO encouragements (encouring_message) VALUES ('Hang in there.')")
c.execute("INSERT INTO encouragements (encouring_message) VALUES ('You are a great person!')")

conn.commit()

# check if messeage already exist
def return_true_if_encouring_message_exists(new_encouring_message):
  with conn:
    c.execute("SELECT * FROM encouragements WHERE encouring_message=?", (new_encouring_message,))
    if (len(c.fetchall()) != 0):
      return True
    else:
      return False


def add_encouring_message(new_encouring_message):
  if (return_true_if_encouring_message_exists == True):
    print("Encouring_message already exist")
    return
  with conn:
    c.execute("INSERT INTO encouragements (encouring_message) VALUES (?)", (new_encouring_message,))

def get_random_encouring_message():
  with conn:
    c.execute("SELECT COUNT(*) FROM encouragements")
    number_of_encouring_messages = c.fetchall()[0][0]
    random_encouring_message_id = random.randint(1, number_of_encouring_messages)
    c.execute("SELECT * FROM encouragements WHERE id=?", (random_encouring_message_id,))
    random_encouring_message = c.fetchall()[0][1]
    return random_encouring_message

def get_all_from_encouragements_table():
  with conn:
     c.execute("SELECT * FROM encouragements LIMIT 50")
     return c.fetchall()

def delete_encouragement(index):
    with conn:
      c.execute("SELECT COUNT(*) FROM encouragements")
      number_of_encouring_messages = c.fetchall()[0][0]
      if (index > number_of_encouring_messages or index < 1):
        return "index out of range!"
      c.execute("DELETE from encouragements WHERE id=?", (index,))
      return "encouring message deleted!"
      
      


new_encouring_message = "Clap yourself on the shoulder."
print(return_true_if_encouring_message_exists(new_encouring_message))
new_encouring_message = "You are a great person!"
print(return_true_if_encouring_message_exists(new_encouring_message))
new_encouring_message = "Hang in there."
print(return_true_if_encouring_message_exists(new_encouring_message))

new_encouring_message = "Clap yourself on the shoulder."
add_encouring_message(new_encouring_message)

c.execute("SELECT * FROM encouragements")
print(c.fetchall())

print(get_random_encouring_message())
print(get_all_from_encouragements_table())

conn.close()
