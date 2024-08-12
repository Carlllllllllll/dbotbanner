import requests
import base64
import os

# Read the bot token from environment variables
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Define URLs for profile picture and/or banner. Leave one blank "" if you only want to do the other one
PROFILE_IMAGE_URL = "https://media.discordapp.net/attachments/1208810080426795061/1271602484061671424/Gido-PFP-Carl.gif?ex=66b9e9d9&is=66b89859&hm=435b9550427e5f05bbff780e509e83170057b9f576f2380b672826c6b346c801&="
BANNER_IMAGE_URL = "https://media.discordapp.net/attachments/1208810080426795061/1271602484519112724/Gido-Banner-Carl.gif?ex=66b9e9d9&is=66b89859&hm=36cef24fa243affd09339b811aff865f0169dd29cd64b453724963d13e4941e8&="

# Initialize payload dictionary
payload = {}

# Check and download profile image if URL is provided
if PROFILE_IMAGE_URL:
    profile_image_response = requests.get(PROFILE_IMAGE_URL)
    if profile_image_response.status_code == 200:
        profile_image_base64 = base64.b64encode(profile_image_response.content).decode('utf-8')
        payload["avatar"] = f"data:image/gif;base64,{profile_image_base64}"
    else:
        print('Failed to download profile picture.')

# Check and download banner image if URL is provided
if BANNER_IMAGE_URL:
    banner_image_response = requests.get(BANNER_IMAGE_URL)
    if banner_image_response.status_code == 200:
        banner_image_base64 = base64.b64encode(banner_image_response.content).decode('utf-8')
        payload["banner"] = f"data:image/gif;base64,{banner_image_base64}"
    else:
        print('Failed to download banner.')

# Proceed only if there's something to update
if payload:
    # Prepare headers with bot token
    headers = {
        'Authorization': f'Bot {DISCORD_BOT_TOKEN}',
        'Content-Type': 'application/json'
    }

    # Send HTTP PATCH request to update profile picture and/or banner
    response = requests.patch('https://discord.com/api/v10/users/@me', headers=headers, json=payload)

    # Check if the response indicates success
    if response.status_code == 200:
        print('Profile and/or banner updated successfully!')
    else:
        print('Failed to update profile and/or banner:', response.text)
else:
    print('No updates to make. Both profile and banner URLs were blank.')
