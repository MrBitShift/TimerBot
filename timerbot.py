import discord
import datetime
import time
from math import floor as fl

client = discord.Client()

def format_time(time, name):
	return name + ": " + str(fl(time.seconds / 3600)).rjust(2, '0') + ":" + str(fl(time.seconds / 60)).rjust(2, '0') + ":" + str(fl(time.seconds % 60)).rjust(2, '0')

@client.event
async def on_ready():
	print("logged on as {0.user}".format(client))

@client.event
async def on_message(message):
	if message.content.startswith(".timerbot"):
		command = message.content.split(' ')
		if (len(command) >= 4 and command[1] == "start"):
			timer = None
			timer_name = " ".join(command[3:len(command)])
			try:
				timer = float(command[2])
			except ValueError:
				await client.send_message(message.channel, "Invalid time. Time is measured in minutes and should be a number" + 
					" greater than 0.")
				return
			now = datetime.datetime.now()
			delta = datetime.timedelta(minutes = timer)
			end = now + delta
			diff = end - now
			timer_message = await client.send_message(message.channel, format_time(diff, timer_name))
			while (now < end):
				now = datetime.datetime.now()
				diff = end - now
				await client.edit_message(timer_message, format_time(diff, timer_name))
				time.sleep(1)
			await client.edit_message(timer_message, format_time(datetime.timedelta(minutes=0), timer_name))
			await client.send_message(message.channel, "Beep Beep! The timer \"" + timer_name + "\" is done!")
		else:
			await client.send_message(message.channel, "Improper command syntax. Try \".timerbot start <minutes> <timername>\"")
			return
client.run(open("./token.txt", 'r').read().strip())
