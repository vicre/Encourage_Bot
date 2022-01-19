import discord
import os
import requests
import json
import random
import sqlite3

client = discord.Client()



sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]


def return_true_if_encouring_message_exists(new_encouring_message):
  conn = sqlite3.connect('bot.db')
  c = conn.cursor()
  with conn:
    c.execute("SELECT * FROM encouragements WHERE encouring_message=?", (new_encouring_message,))
    if (len(c.fetchall()) != 0):
      return True
    else:
      return False

def add_encouring_message(new_encouring_message):
  conn = sqlite3.connect('bot.db')
  c = conn.cursor()
  if (return_true_if_encouring_message_exists == True):
    print("Encouring_message already exist")
    return
  with conn:
    c.execute("INSERT INTO encouragements (encouring_message) VALUES (?)", (new_encouring_message,))

def get_random_encouring_message():
  conn = sqlite3.connect('bot.db')
  c = conn.cursor()
  with conn:
    c.execute("SELECT COUNT(*) FROM encouragements")
    number_of_encouring_messages = c.fetchall()[0][0]
    random_encouring_message_id = random.randint(1, number_of_encouring_messages)
    c.execute("SELECT * FROM encouragements WHERE id=?", (random_encouring_message_id,))
    random_encouring_message = c.fetchall()[0][1]
    return random_encouring_message

def get_all_from_encouragements_table():
  conn = sqlite3.connect('bot.db')
  c = conn.cursor()
  with conn:
     c.execute("SELECT * FROM encouragements LIMIT 50")
     return c.fetchall()

def delete_encouragement(index):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    with conn:
      c.execute("SELECT COUNT(*) FROM encouragements")
      number_of_encouring_messages = c.fetchall()[0][0]
      if (index > number_of_encouring_messages or index < 1):
        return "index out of range!"
      c.execute("DELETE from encouragements WHERE id=?", (index,))
      return "encouring message deleted!"

def get_qoute():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  qoute = json_data[0]['q'] + " -" + json_data[0]['a']
  return qoute

# def update_encouragements(encourageing_message):
#   c.execute("INSERT INTO encouragements (encouring_message) VALUES (?)", (encourageing_message,))
  

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  msg = message.content

  if msg.startswith('$inspire'):
    quote = get_qoute()
    await message.channel.send(quote)
  

  if any(word in msg for word in sad_words):
    await message.channel.send(get_random_encouring_message())

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ", 1)[1]
    add_encouring_message(encouraging_message)
    await message.channel.send("New encouraging message added")

  if msg.startswith("$raw"):
    await message.channel.send(get_all_from_encouragements_table())

  if msg.startswith("$del"):
    index = int(msg.split("$del ", 1)[1])
    await message.channel.send(delete_encouragement(index))

client.run(os.getenv('TOKEN'))

