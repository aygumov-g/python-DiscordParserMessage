import discord, os, colorama, io
from discord.ext import commands

me = commands.Bot(command_prefix=discord, intents=discord.Intents.all(), self_bot=True)

messageParsingLen = 50 # number of messages that will be parsed

def log(params):
	if params['LogParam'] == 0:
		color = colorama.Fore.GREEN
		print(color, f"\n\nData: {os.getcwd()}\servers", colorama.Fore.WHITE, sep="")
	elif params['LogParam'] == 1:
		color = colorama.Fore.RED
		print(color, f"Failed to create a folder for the server: {params['Guild'].id} ({params['Guild'].name}) [{params['Exception']}]:", colorama.Fore.WHITE, sep="")
	elif params['LogParam'] == 2:
		color = colorama.Fore.YELLOW
		print(color, f"[{params['CheckComplited']}]: Channel added successfully: ", colorama.Fore.WHITE, f"\"{params['Channel']}\"", sep="")
	elif params['LogParam'] == 3:
		color = colorama.Fore.RED
		print(color, f"[{params['CheckComplited']}]: [{params['Exception']}]: Couldn't add a channel: ", colorama.Fore.WHITE, f"\"{params['Channel']}\"", sep="")
	elif params['LogParam'] == 4:
		color = colorama.Fore.GREEN
		print(color, f"Folder \"channels\" server {params['Guild'].id} ({params['Guild'].name}) completed successfully", colorama.Fore.WHITE, sep="")
	elif params['LogParam'] == 5:
		color = colorama.Fore.RED
		print(color, f"[{params['CheckComplited']}]: [{params['Exception']}]: The message could not be recorded", colorama.Fore.WHITE, sep="")

def main_create_folder():
	for guild in me.guilds:
		if not os.path.isdir("servers"):
			os.mkdir("servers")

		if not os.path.isdir(f"servers\{guild.id} ({guild.name})"):
			try:
				os.mkdir(f"servers\{guild.id} ({guild.name})")
			except Exception as e:
				log({
					"LogParam": 1,
					"Guild": guild,
					"Exception": e
				})

def get_message_time(message_created_at):
	hour = ("0" * 1) + str(message_created_at.hour) if len(str(message_created_at.hour)) == 1 else str(message_created_at.hour)
	minute = ("0" * 1) + str(message_created_at.minute) if len(str(message_created_at.minute)) == 1 else str(message_created_at.minute)
	second = ("0" * 1) + str(message_created_at.second) if len(str(message_created_at.second)) == 1 else str(message_created_at.second)

	year = ("0" * 1) + str(message_created_at.year) if len(str(message_created_at.year)) == 1 else str(message_created_at.year)
	month = ("0" * 1) + str(message_created_at.month) if len(str(message_created_at.month)) == 1 else str(message_created_at.month)
	day = ("0" * 1) + str(message_created_at.day) if len(str(message_created_at.day)) == 1 else str(message_created_at.day)
	
	return "{}.{}.{} {}:{}:{}".format(year, month, day, hour, minute, second)

def edit_message(message, guild):

	def append_message_CMR(message, guild):

		def check(sim):
			return True if sim == "@" or sim == "#" else False

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


			return append_message_CMR(returnMessage, guild) if "<" in returnMessage or ">" in returnMessage else returnMessage


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

		return check_message_CMR(messageBracketsContent, message, guild) if not messageBracketsContent == "" else message

	def get_message_attachments(message, guild):

		messageAttachments = ""

		for attach in message.attachments:
			messageAttachments += f"<{attach.filename}|{attach.url}>"
		
		if not messageAttachments == "":
			if not message.content == "":
				returns = f"{messageAttachments}\n{message.content}".replace("  ", " ")
			else:
				returns = f"{messageAttachments}{message.content}".replace("  ", " ")
		else:
			returns = f"{message.content}"

		return append_message_CMR(returns, guild)

	

	def CONTROLLER(message, guild):

		message = get_message_attachments(message, guild)

		message = append_message_CMR(message, guild)

		return message
	
	return get_message_attachments(message, guild)



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
								probel = "=" * 200
								msg = f"Message at {get_message_time(message.created_at)} from {message.author}: {edit_message(message, guild)}\n" + f"{probel}\n"
								fileChannel.write(f"{msg}")
							except Exception as e:
								log({
									"LogParam": 5,
									"CheckComplited": checkComplited
								})

						fileChannel.close()

						log({
							"LogParam": 2,
							"Channel": channel,
							"CheckComplited": checkComplited
						})
				except Exception as e:
					log({
						"LogParam": 3,
						"Channel": channel,
						"CheckComplited": checkComplited,
						"Exception": e
					})

				checkComplited += 1

		log({
			"LogParam": 4,
			"Guild": guild
		})

	log({
		"LogParam": 0
	})

me.run("DISCORD ACCOUNT TOKEN", bot=False)
