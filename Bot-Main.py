import socket
import discord
import asyncio
import re

# Twitch and Discord API credentials
TWITCH_TOKEN = "TOKEN"
TWITCH_USERNAME = "USERNAME"
DISCORD_TOKEN = "TOKEN"

# Define the phrase to search for in Twitch chat
SEARCH_PHRASE = "WORD"

# Define the Twitch channels to monitor
TWITCH_CHANNELS = ["channel1", "channel2", "channel3", "channel4"]

# Define the Discord channel to post the messages in
DISCORD_CHANNEL = "discord-channel"

# Define the Twitch IRC server and port
IRC_SERVER = "irc.chat.twitch.tv"
IRC_PORT = 6667

# Connect to Twitch IRC server
irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc_socket.connect((IRC_SERVER, IRC_PORT))

# Login to Twitch IRC server with Twitch API credentials
irc_socket.send(f"PASS {TWITCH_TOKEN}\n".encode('utf-8'))
irc_socket.send(f"NICK {TWITCH_USERNAME}\n".encode('utf-8'))

# Join Twitch channels to monitor
async def join_channels():
    for channel in TWITCH_CHANNELS:
        irc_socket.send(f"JOIN #{channel}\n".encode('utf-8'))
        init_resp = irc_socket.recv(2048).decode('utf-8', errors='ignore')
        has_joined = re.search(r'JOIN #\w+', init_resp)
        if has_joined:
            print(has_joined.group())
        await asyncio.sleep(0.5)

# Replace non Twitch links with "[link deleted]"
def filter_links(message):

    pattern = r"https?://[\w.\-~!$&\'()*+;=:@/?]+(?:[/\?_#][^ \n\r\t\f\"\'<>()[\]]*)?"

    def replace_links(input):
        url = input.group(0)
        if "twitch.tv" in url:
            return url
        else:
            print("Link has been deleted: " + url)
            return "`[link deleted]`"

    # Replace links using regular expressions
    return re.sub(pattern, replace_links, message)

# Send message to the Discord channel
async def send_to_discord(message):
    try:
        discord_channel = discord.utils.get(
            bot.get_all_channels(), name=DISCORD_CHANNEL)
        if discord_channel:
            await discord_channel.send(message, silent=True)
        else:
            print(f"Channel {DISCORD_CHANNEL} not found.")
    except AttributeError:
        print(f"Channel {DISCORD_CHANNEL} not found.")

# Respond PONG after receiving PING
def ping_pong(resp):
    if resp.startswith('PING'):
        irc_socket.send(("PONG " + resp.split()[1] + "\r\n").encode())
        print("PING PONG")

# Parse messages
def parse_messages(data):
    for resp in data:

        ping_pong(resp)

        if SEARCH_PHRASE in resp.lower():
            # Parse response to message
            match = re.search(':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', resp)
            if match is None:
                return
            else:
                username, channel, message = match.groups()
                parsed_message = channel + " | " + "**" + username + "**" + ": " + message
                if re.search(r"\b" + SEARCH_PHRASE + r"\b", message, re.IGNORECASE):
                    print("Phrase has been mentioned")
                    parsed_message = filter_links(parsed_message)
                    return parsed_message

# Monitoring
async def monitoring():
    while True:

        # Receive messages
        data = await asyncio.to_thread(irc_socket.recv, 2048)
        data = data.decode('utf-8', errors='ignore').splitlines()

        # Parse, check for phrase and send to Discord
        parsed_message = parse_messages(data)
        if parsed_message:
            await send_to_discord(parsed_message)

# Establish bot
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# Main Bot actions
@bot.event
async def on_ready():

    print(f'{bot.user} has connected to Discord!')
    await join_channels()
    print("MONITORING STARTING")
    await monitoring()

bot.run(DISCORD_TOKEN)
