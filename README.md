# Twitch-Discord-Chat-Bot

This is a Python chat bot that monitors specified Twitch channels for a given search phrase and relays the chat message to a Discord channel.

## Features
- Discord markdown escaping to prevent text formatting errors.
- Non-Twitch link removal.

## Setup

1. Download Bot-Main.py

2. Install the Discord Python module.

```bash
pip install discord
```
3. Set up Twitch and Discord API credentials:

- Create a Twitch account and register a new application to obtain your Twitch API credentials: <br>
https://dev.twitch.tv/docs/authentication/getting-tokens-oauth#oauth-client-id-and-secret
- Create a Discord account and a new application to obtain your Discord API credentials: <br>
https://discord.com/developers/applications

4. Set the following variables:

	- TWITCH_TOKEN: Your Twitch API token.
	- TWITCH_USERNAME: Your Twitch username.
	- DISCORD_TOKEN: Your Discord API token.

5. Modify the following variables according to your preferences:

	- SEARCH_PHRASE: The phrase to search for in Twitch chat.
	- TWITCH_CHANNELS: A list of Twitch channels to monitor.
	- DISCORD_CHANNEL: The Discord channel to post the messages in.

6. Run the bot.




Twitch is a trademark or registered trademark of Twitch Interactive, Inc. in the U.S. and/or other countries. "TwitchIRC-Discord-Bot" is not operated by, sponsored by, or affiliated with Twitch Interactive, Inc. in any way.
