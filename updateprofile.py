import requests
import base64
import os
import time
from dotenv import load_dotenv
from flask import Flask
from colorama import Fore, Style, init
import logging

# Initialize colorama
init()

# Load environment variables
load_dotenv()

DISCORD_BOT_TOKEN = os.getenv('TOKEN')

if not DISCORD_BOT_TOKEN:
    print(f"{Fore.RED}Error: TOKEN environment variable not set.{Style.RESET_ALL}")
    exit()

PROFILE_IMAGE_URL = "https://media.discordapp.net/attachments/1208810080426795061/1271602484061671424/Gido-PFP-Carl.gif?ex=66b9e9d9&is=66b89859&hm=435b9550427e5f05bbff780e509e83170057b9f576f2380b672826c6b346c801&="
BANNER_IMAGE_URL = "https://media.discordapp.net/attachments/1208810080426795061/1271602484519112724/Gido-Banner-Carl.gif?ex=66b9e9d9&is=66b89859&hm=36cef24fa243affd09339b811aff865f0169dd29cd64b453724963d13e4941e8&="

payload = {}

FLAG_FILE = 'profile_update_flag.txt'

if os.path.exists(FLAG_FILE):
    print(f"{Fore.YELLOW}The profile has already been updated. Exiting.{Style.RESET_ALL}")
    exit()

def download_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return base64.b64encode(response.content).decode('utf-8')
    except requests.RequestException as e:
        return str(e)

if PROFILE_IMAGE_URL:
    profile_image_base64 = download_image(PROFILE_IMAGE_URL)
    if "Error" in profile_image_base64:
        profile_update_status = f"Failed to download profile picture: {profile_image_base64}"
    else:
        payload["avatar"] = f"data:image/gif;base64,{profile_image_base64}"
        profile_update_status = "Success"

if BANNER_IMAGE_URL:
    banner_image_base64 = download_image(BANNER_IMAGE_URL)
    if "Error" in banner_image_base64:
        banner_update_status = f"Failed to download banner: {banner_image_base64}"
    else:
        payload["banner"] = f"data:image/gif;base64,{banner_image_base64}"
        banner_update_status = "Success"

if payload:
    headers = {
        'Authorization': f'Bot {DISCORD_BOT_TOKEN}',
        'Content-Type': 'application/json'
    }

    while True:
        response = requests.patch('https://discord.com/api/v10/users/@me', headers=headers, json=payload)

        if response.status_code == 200:
            break
        elif response.status_code == 429:
            retry_after = response.json().get('retry_after', 60)
            print(f"{Fore.YELLOW}Rate limit exceeded. Retrying after {retry_after} seconds...{Style.RESET_ALL}")
            time.sleep(retry_after)
        elif response.status_code == 401:
            print(f"{Fore.RED}Invalid token. Please check your token and try again.{Style.RESET_ALL}")
            break
        elif response.status_code == 50035:
            print(f"{Fore.RED}Avatar rate limit exceeded. Try again later.{Style.RESET_ALL}")
            break
        else:
            print(f"{Fore.RED}Failed to update profile and/or banner: {response.text}{Style.RESET_ALL}")
            break
else:
    print(f"{Fore.YELLOW}No updates to make. Both profile and banner URLs were blank.{Style.RESET_ALL}")

with open(FLAG_FILE, 'w') as f:
    f.write('Profile update script has run.')

app = Flask(__name__)

@app.route('/')
def index():
    return "Profile update script has run."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))

    # Suppress Flask development server output
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    # Print the formatted console output
    box_width = 70  # Adjusted width for better fit
    profile_update_status = profile_update_status if 'profile_update_status' in locals() else "Not Updated"
    banner_update_status = banner_update_status if 'banner_update_status' in locals() else "Not Updated"

    print(f'\n{Fore.BLUE}╔{"═" * (box_width - 2)}╗{Style.RESET_ALL}')
    print(f'{Fore.BLUE}║{Style.RESET_ALL}{" " * (box_width - 2)}║')
    print(f'{Fore.BLUE}║  🎨 Banner Update: {Fore.GREEN if banner_update_status == "Success" else Fore.RED}{banner_update_status}{Style.RESET_ALL}{" " * (box_width - 2 - len(f"  🎨 Banner Update: {banner_update_status}"))}║')
    print(f'{Fore.BLUE}║  🎨 Avatar Update: {Fore.GREEN if profile_update_status == "Success" else Fore.RED}{profile_update_status}{Style.RESET_ALL}{" " * (box_width - 2 - len(f"  🎨 Avatar Update: {profile_update_status}"))}║')
    print(f'{Fore.BLUE}║  🚀 Running on Port: {Fore.GREEN}{port}{Style.RESET_ALL}{" " * (box_width - 2 - len(f"  🚀 Running on Port: {port}"))}║')
    print(f'{Fore.BLUE}║  ⚙️ Powered by Carl, GlaceYT{Style.RESET_ALL}{" " * (box_width - 2 - len("  ⚙️ Powered by Carl, GlaceYT"))}║')
    print(f'{Fore.BLUE}║{Style.RESET_ALL}{" " * (box_width - 2)}║')
    print(f'{Fore.BLUE}╚{"═" * (box_width - 2)}╝{Style.RESET_ALL}')

    app.run(host='0.0.0.0', port=port, debug=False)
