import requests
import base64
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DISCORD_BOT_TOKEN = os.getenv('TOKEN')

# Check if the bot token is set
if not DISCORD_BOT_TOKEN:
    print("Error: TOKEN environment variable not set.")
    exit()

# Define URLs for profile picture and/or banner
PROFILE_IMAGE_URL = "https://media.discordapp.net/attachments/1208810080426795061/1271602484061671424/Gido-PFP-Carl.gif?ex=66b9e9d9&is=66b89859&hm=435b9550427e5f05bbff780e509e83170057b9f576f2380b672826c6b346c801&="
BANNER_IMAGE_URL = "https://media.discordapp.net/attachments/1208810080426795061/1271602484519112724/Gido-Banner-Carl.gif?ex=66b9e9d9&is=66b89859&hm=36cef24fa243affd09339b811aff865f0169dd29cd64b453724963d13e4941e8&="

payload = {}

# Create a file to track if the code has run
FLAG_FILE = 'profile_update_flag.txt'

# Check if the script has already run
if os.path.exists(FLAG_FILE):
    print("The profile has already been updated. Exiting.")
    exit()

# Download and encode the profile picture
if PROFILE_IMAGE_URL:
    profile_image_response = requests.get(PROFILE_IMAGE_URL)
    if profile_image_response.status_code == 200:
        profile_image_base64 = base64.b64encode(profile_image_response.content).decode('utf-8')
        payload["avatar"] = f"data:image/gif;base64,{profile_image_base64}"
    else:
        print('Failed to download profile picture.')

# Download and encode the banner image
if BANNER_IMAGE_URL:
    banner_image_response = requests.get(BANNER_IMAGE_URL)
    if banner_image_response.status_code == 200:
        banner_image_base64 = base64.b64encode(banner_image_response.content).decode('utf-8')
        payload["banner"] = f"data:image/gif;base64,{banner_image_base64}"
    else:
        print('Failed to download banner.')

# Update profile and/or banner if there is something to update
if payload:
    headers = {
        'Authorization': f'Bot {DISCORD_BOT_TOKEN}',
        'Content-Type': 'application/json'
    }

    while True:
        response = requests.patch('https://discord.com/api/v10/users/@me', headers=headers, json=payload)

        if response.status_code == 200:
            print('Profile and/or banner updated successfully!')
            break
        elif response.status_code == 429:
            retry_after = response.json().get('retry_after', 60)
            print(f'Rate limit exceeded. Retrying after {retry_after} seconds...')
            time.sleep(retry_after)
        elif response.status_code == 401:
            print('Invalid token. Please check your token and try again.')
            break
        elif response.status_code == 50035:
            print('Avatar rate limit exceeded. Try again later.')
            break
        else:
            print(f'Failed to update profile and/or banner: {response.text}')
            break
else:
    print('No updates to make. Both profile and banner URLs were blank.')

# Create a flag file to indicate that the script has run
with open(FLAG_FILE, 'w') as f:
    f.write('Profile update script has run.')

# Print the port and other details
print("\n------------------------------------------")
print("Running on port 3000")
print("Powered by Carl, GlaceYT")
print("------------------------------------------")
