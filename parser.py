import discord, os, colorama, io
from discord.ext import commands

me = commands.Bot(command_prefix=discord, intents=discord.Intents.all(), self_bot=True)

messageParsingLen = 50 # number of messages that will be parsed

def log(logParam, guild=None, channel=None, checkComplited=None):
	if logParam == 1:
		color = colorama.Fore.RED
		print(color, f"Failed to create a folder for the server: {guild.id} ({guild.name})", colorama.Fore.WHITE, sep="")
	elif logParam == 2:
		color = colorama.Fore.YELLOW
		print(color, f"[{checkComplited}]: Channel added successfully: ", colorama.Fore.WHITE, f"\"{channel}\"", sep="")
	elif logParam == 3:
		color = colorama.Fore.RED
		print(color, f"[{checkComplited}]: Couldn't add a channel: ", colorama.Fore.WHITE, f"\"{channel}\"", sep="")
	elif logParam == 4:
		color = colorama.Fore.GREEN
		print(color, f"Folder \"channels\" server {guild.id} ({guild.name}) completed successfully", colorama.Fore.WHITE, sep="")
	elif logParam == 5:
		color = colorama.Fore.RED
		print(color, f"[{checkComplited}]: The message could not be recorded", colorama.Fore.WHITE, sep="")
	elif logParam == 6:
		color = colorama.Fore.GREEN
		print(color, f"\n\nData: {os.getcwd()}\servers", colorama.Fore.WHITE, sep="")

def main_create_folder():
	for guild in me.guilds:
		if not os.path.isdir("servers"):
			os.mkdir("servers")

		if not os.path.isdir(f"servers\{guild.id} ({guild.name})"):
			try:
				os.mkdir(f"servers\{guild.id} ({guild.name})")
			except:
				log(1, guild)

def get_message_time(message_created_at):
	hour = ("0" * 1) + str(message_created_at.hour) if len(str(message_created_at.hour)) == 1 else str(message_created_at.hour)
	minute = ("0" * 1) + str(message_created_at.minute) if len(str(message_created_at.minute)) == 1 else str(message_created_at.minute)
	second = ("0" * 1) + str(message_created_at.second) if len(str(message_created_at.second)) == 1 else str(message_created_at.second)

	year = ("0" * 1) + str(message_created_at.year) if len(str(message_created_at.year)) == 1 else str(message_created_at.year)
	month = ("0" * 1) + str(message_created_at.month) if len(str(message_created_at.month)) == 1 else str(message_created_at.month)
	day = ("0" * 1) + str(message_created_at.day) if len(str(message_created_at.day)) == 1 else str(message_created_at.day)
	
	return "{}.{}.{} {}:{}:{}".format(year, month, day, hour, minute, second)

def append_message_CMR(message, guild):

	def check(sim):
#		if sim == 1 or sim == 2 or sim == 3 or sim == 4 or sim == 5 or sim == 6 or sim == 7 or sim == 8 or sim == 9 or sim == 0:
		if sim == "@" or sim == "#":
			return True
		else:
			return False 

	def check_message_CMR(messageBracketsContent, message, guild):

		returnMessage = "<сообщение не распознано>"

		if "#" in messageBracketsContent:
			returnMessageBracketsContent = messageBracketsContent.replace("#", "")
			try:
				returnMessage = message.replace(f"<{messageBracketsContent}>", f"#{str(me.get_channel(int(returnMessageBracketsContent)))}")
			except:
				pass
		elif "@!" in messageBracketsContent:
			returnMessageBracketsContent = messageBracketsContent.replace("@!", "")
			try:
				returnMessage = message.replace(f"<{messageBracketsContent}>", f"@{str(me.get_user(int(returnMessageBracketsContent)))}")
			except:
				pass
		elif "@&" in messageBracketsContent:
			returnMessageBracketsContent = messageBracketsContent.replace("@&", "")
			try:
				returnMessage = message.replace(f"<{messageBracketsContent}>", f"@{str(discord.utils.get(guild.roles, int(returnMessageBracketsContent)))}")
			except:
				pass			

		if "<" in returnMessage or ">" in returnMessage:
			return append_message_CMR(returnMessage, guild)
		else:
			return returnMessage

	messageBracketsContent = ""
	messageSimInt = 0

	while messageSimInt < len(message):
		if message[messageSimInt] == ">":

			bracketsCloseIndex = messageSimInt
			messageSimIntBracketsCloseIndex = messageSimInt - 1

			while(messageSimIntBracketsCloseIndex >= 0):
				if message[messageSimIntBracketsCloseIndex] == "<":
					if not message[messageSimIntBracketsCloseIndex+1] == ":" and check(message[messageSimIntBracketsCloseIndex+1]):

						bracketsOpenIndex = messageSimIntBracketsCloseIndex
						bracketsCloseIndexBracketsOpenIndex = messageSimIntBracketsCloseIndex + 1

						while(bracketsCloseIndexBracketsOpenIndex < messageSimInt):
							messageBracketsContent += message[bracketsCloseIndexBracketsOpenIndex]

							bracketsCloseIndexBracketsOpenIndex += 1

						break

				messageSimIntBracketsCloseIndex -= 1

			break

		messageSimInt += 1

	if not messageBracketsContent == "":
		return check_message_CMR(messageBracketsContent, message, guild)
	else:
		return message

@me.event
async def on_ready():
	main_create_folder()

	checkComplited = 1

	for guild in me.guilds:
		for channel in me.get_guild(guild.id).channels:

			messages = ""

			if isinstance(channel, discord.channel.TextChannel):
				try:
					with io.open(f"servers\{guild.id} ({guild.name})\{channel}.txt", "w", encoding="utf-8") as fileChannel:

						async for message in channel.history(limit=messageParsingLen):
							try:
								msg = f"Message at {get_message_time(message.created_at)} from {message.author}: {append_message_CMR(message.content, guild)}\n\n"
								fileChannel.write(f"{msg}")
							except Exception as e:
								log(5, None, None, checkComplited)

						fileChannel.close()

						log(2, None, channel, checkComplited)
				except:
					log(3, None, channel, checkComplited)

					checkComplited += 1

		log(4, guild)

	log(6)

me.run("DISCORD ACCOUNT TOKEN", bot=False)
