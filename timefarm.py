import requests
import time
from colorama import Fore, Style, init
import json
from datetime import datetime, timedelta, timezone
import argparse
import urllib.parse

def parse_arguments():
    parser = argparse.ArgumentParser(description='TimeFarm BOT')
    parser.add_argument('--task', type=str, choices=['y', 'n'], help='Claim Task (y/n)')
    parser.add_argument('--upgrade', type=str, choices=['y', 'n'], help='Auto Upgrade (y/n)')
    args = parser.parse_args()

    if args.task is None:
        task_input = input("Do you want to auto claim task? (y/n, default n): ").strip().lower()
        args.task = task_input if task_input in ['y', 'n'] else 'n'
    
    if args.upgrade is None:
        upgrade_input = input("Do you want to auto upgrade clock? (y/n, default n): ").strip().lower()
        args.upgrade = upgrade_input if upgrade_input in ['y', 'n'] else 'n'

    return args

args = parse_arguments()
cek_task_enable = args.task
cek_upgrade_enable = args.upgrade

# Set headers once at the beginning
headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'text/plain;charset=UTF-8',
    'origin': 'https://tg-tap-miniapp.laborx.io',
    'priority': 'u=1, i',
    'referer': 'https://tg-tap-miniapp.laborx.io/',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}

def get_access_token_and_info(query_data):
    url = 'https://tg-bot-tap.laborx.io/api/v1/auth/validate-init'
    try:
        response = requests.post(url, headers=headers, data=query_data)
        response.raise_for_status()  # Raises an error if status is not 200
        return response.json()
    except json.JSONDecodeError:
        print(f"JSON Decode Error: Your query is incorrect")
        return None
    except requests.RequestException as e:
        print(f"Request Error: {e}")
        return None

def cek_farming(token):
    url = 'https://tg-bot-tap.laborx.io/api/v1/farming/info'
    headers['authorization'] = f'Bearer {token}'
    response = requests.get(url, headers=headers)
    return response.json()

def start_farming(token):
    url = 'https://tg-bot-tap.laborx.io/api/v1/farming/start'
    headers['authorization'] = f'Bearer {token}'
    response = requests.post(url, headers=headers, json={})
    return response.json()

def finish_farming(token):
    url = 'https://tg-bot-tap.laborx.io/api/v1/farming/finish'
    headers['authorization'] = f'Bearer {token}'
    response = requests.post(url, headers=headers, json={})
    return response.json()

def cek_task(token):
    url = 'https://tg-bot-tap.laborx.io/api/v1/tasks'
    headers_task = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers_task)
    return response.json()

def submit_task(token, task_id):
    url = f'https://tg-bot-tap.laborx.io/api/v1/tasks/{task_id}/submissions'
    headers_submit = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers_submit, json={})
    return response.json()

def claim_task(token, task_id):
    url = f'https://tg-bot-tap.laborx.io/api/v1/tasks/{task_id}/claims'
    headers_claim = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers_claim, json={})
    return response.json()

start_time = datetime.now()

def upgrade_level(token):
    url = 'https://tg-bot-tap.laborx.io/api/v1/me/level/upgrade'
    headers_upgrade = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://tg-tap-miniapp.laborx.io',
        'referer': 'https://tg-tap-miniapp.laborx.io/',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    response = requests.post(url, headers=headers_upgrade)
    return response.json()

def auto_upgrade(token):
    while True:
        response = upgrade_level(token)
        if 'error' in response:
            if response['error']['message'] == "Not enough balance":
                print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade ] : Not enough balance to upgrade.", flush=True)
                break
            elif response['error']['message'] == "Forbidden":
                print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade ] : Error upgrading.", flush=True)
            elif response['error']['message'] == "Max level reached":
                print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade ] : Already reached maximum level.", flush=True)
                break
            else:
                print(Fore.RED + Style.BRIGHT + f"\r[ Upgrade ] : Error upgrading. {response['error']['message']}", flush=True)
                break
        else:
            print(Fore.GREEN + Style.BRIGHT + f"\r[ Upgrade ] : Upgrade successful, next..", flush=True)

# Add a call to this function in the main loop if the user chooses to auto upgrade


def animated_loading(duration):
    frames = ["|", "/", "-", "\\"]
    end_time = time.time() + duration
    while time.time() < end_time:
        remaining_time = int(end_time - time.time())
        for frame in frames:
            print(f"\rWaiting for the next claim time {frame} - Remaining {remaining_time} seconds         ", end="", flush=True)
            time.sleep(0.25)
    print("\rWaiting for the next claim time finished.                            ", flush=True)
def print_welcome_message():
    print(r"""
          
█▀▀ █░█ ▄▀█ █░░ █ █▄▄ █ █▀▀
█▄█ █▀█ █▀█ █▄▄ █ █▄█ █ ██▄
          """)
    print(Fore.GREEN + Style.BRIGHT + "TimeFarm BOT")
    print(Fore.CYAN + Style.BRIGHT + "Update Link: https://github.com/adearman/timefarm")
    print(Fore.YELLOW + Style.BRIGHT + "Free Consultation Join Telegram Channel: https://t.me/ghalibie")
    print(Fore.BLUE + Style.BRIGHT + "Buy me a coffee :) 0823 2367 3487 GOPAY / DANA")
    print(Fore.RED + Style.BRIGHT + "NOT FOR SALE! Use your brain a bit, bro. Coding isn't easy, just rename :)")
    current_time = datetime.now()
    up_time = current_time - start_time
    days, remainder = divmod(up_time.total_seconds(), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(Fore.CYAN + Style.BRIGHT + f"Bot uptime: {int(days)} days, {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds")

def extract_user_details(query_line):
    parts = query_line.split('&')
    user_info_encoded = [part for part in parts if part.startswith('user=')][0]
    user_info_encoded = user_info_encoded.split('=')[1]
    user_info_json = urllib.parse.unquote(user_info_encoded)
    user_info = json.loads(user_info_json)
    return user_info.get('username', "No Username"), user_info.get('first_name', "No Firstname"), user_info.get('last_name', "No Lastname")

def main():
    while True:
        print_welcome_message()
        try:
            with open('query.txt', 'r') as file:
                queries = file.readlines()
            
            for query_data in queries:
                username, first_name, last_name = extract_user_details(query_data.strip())

                query_data = query_data.strip()
                auth_response = get_access_token_and_info(query_data)
                # user_info = extract_user_info(query_data)
                # print(user_info)
                token = auth_response['token']

                balance_info = auth_response['balanceInfo']

                # username = balance_info.get('user', {}).get('userInfo', {}).get('userName', "No Username")
                # first_name = balance_info.get('user', {}).get('userInfo', {}).get('firstName', "No Firstname")
                # last_name = balance_info.get('user', {}).get('userInfo', {}).get('lastName', "No Lastname")
                print(Fore.CYAN + Style.BRIGHT + f"\n===== [ {first_name} {last_name} | {username} ] =====")
                print(Fore.YELLOW + Style.BRIGHT + f"[ Balance ] : {int(balance_info['balance']):,}".replace(',', '.'))
                if cek_upgrade_enable == 'y':
                    print(Fore.YELLOW + Style.BRIGHT + f"\r[ Upgrade ] : Upgrading Clock..", end="", flush=True)
                    auto_upgrade(token)
                if cek_task_enable == 'y':
                    print(Fore.YELLOW + Style.BRIGHT + f"\r[ Task ] : Checking ...", end="", flush=True)
                    tasks = cek_task(token)

                if tasks:
    for task in tasks:
        # if "TimeFarm" in task['title']:
        #     continue  
        if task.get('submission', {}).get('status') == 'CLAIMED':
            print(Fore.GREEN + Style.BRIGHT + f"\r[ Task ] : {task['title']} | Claimed                                               ", flush=True)
        elif task.get('submission', {}).get('status') == 'COMPLETED':
            print(Fore.GREEN + Style.BRIGHT + f"\r[ Task ] : Claiming {task['title']}", flush=True)
            response = claim_task(token, task['id'])
            # print(response)
            if response is not None:
                if 'error' in response:
                    if response['error']['message'] == "Failed to claim reward":
                        print(Fore.RED + Style.BRIGHT + f"\r[ Task ] : Claim task: {task['title']} | Already claimed", end="", flush=True)
                else:
                    print(Fore.GREEN + Style.BRIGHT + f"\r[ Task ] : Claim task: {task['title']} | Claimed", flush=True)    
        
        else:
            print(f"\r[ Task ] : Submit task: {task['title']}", end="", flush=True)
            if task.get('submission', {}).get('status') == 'SUBMITTED':
                print(Fore.YELLOW + Style.BRIGHT + f"\r[ Task ] : Submit task: {task['title']} | Already Submitted", flush=True)
            else:
                response = submit_task(token, task['id'])
                # print(response)
                if response is not None:
                    if 'error' in response:
                        print(Fore.RED + Style.BRIGHT + f"\r[ Task ] : Submit task: {task['title']} | {response['error']['message']}", end="", flush=True)
                    else:
                        print(Fore.GREEN + Style.BRIGHT + f"\r[ Task ] : Submit task: {task['title']} | Submitted", flush=True)
                time.sleep(3)  # Wait for 3 seconds before claiming
            print(f"\r[ Task ] : Claim task: {task['title']}", end="", flush=True)
            response = claim_task(token, task['id'])
            # print(response)
            if response is not None:
                if 'error' in response:
                    if response['error']['message'] == "Failed to claim reward":
                        print(Fore.RED + Style.BRIGHT + f"\r[ Task ] : Claim task: {task['title']} | Failed to claim reward / already claimed", end="", flush=True)
                else:
                    print(Fore.GREEN + Style.BRIGHT + f"\r[ Task ] : Claim task: {task['title']} | Claimed", flush=True)
print(Fore.YELLOW + Style.BRIGHT + f"\r[ Farming ] : Checking ...", end="", flush=True)
time.sleep(2)
farming_response = finish_farming(token)
if farming_response is not None:
    if 'error' in farming_response:
        if farming_response['error']['message'] == "Too early to finish farming":

            cek_farming_response = cek_farming(token)
            if cek_farming_response:
                started_at = datetime.fromisoformat(cek_farming_response['activeFarmingStartedAt'].replace('Z', '+00:00')).astimezone(timezone.utc)
                duration_sec = cek_farming_response['farmingDurationInSec']
                end_time = started_at + timedelta(seconds=duration_sec)
                time_now = datetime.now(timezone.utc)

                remaining_time = end_time - time_now
                if remaining_time.total_seconds() > 0:
                    hours, remainder = divmod(remaining_time.total_seconds(), 3600)
                    minutes, _ = divmod(remainder, 60)
                    print(Fore.RED + Style.BRIGHT + f"\r[ Farming ] : Claim farming in {int(hours)} hours {int(minutes)} minutes", flush=True)
                else:
                    print(Fore.GREEN + Style.BRIGHT + f"\r[ Farming ] : Farming can be claimed now", flush=True)
        elif farming_response['error']['message'] == "Farming didn't start":
            print(Fore.YELLOW + Style.BRIGHT + f"\r[ Farming ] : Starting Farming..", end="", flush=True)
            time.sleep(2)
            start_farming_response = start_farming(token)
            if start_farming_response is not None:
                print(Fore.GREEN + Style.BRIGHT + f"\r[ Farming ] : Started | Reward : {int(start_farming_response['farmingReward']):,}".replace(',', '.'), flush=True)
            else:
                if 'error' in start_farming_response:
                    if start_farming_response['error']['message'] == "Farming already started":
                        print(Fore.RED + Style.BRIGHT + f"\r[ Farming ] : Farming Already Started", flush=True)
                else:
                    print(Fore.RED + Style.BRIGHT + f"\r[ Farming ] : Failed to Start Farming", flush=True)
        else:
            print(f"\r[ Farming ] : {farming_response['error']['message']}", flush=True)
    else:
        print(Fore.GREEN + Style.BRIGHT + f"\r[ Farming ] : Claimed | Balance: {int(farming_response['balance']):,}".replace(',', '.'), flush=True)
        print(Fore.YELLOW + Style.BRIGHT + f"\r[ Farming ] : Checking Farming..", end="", flush=True)
        time.sleep(2)
        cek_farming_response = cek_farming(token)
        if cek_farming_response is not None:
                if cek_farming_response['activeFarmingStartedAt'] is None:
                    print(Fore.RED + Style.BRIGHT + f"\r[ Farming ] : Farming not started", flush=True)
                    print(Fore.YELLOW + Style.BRIGHT + f"\r[ Farming ] : Starting Farming..", end="", flush=True)
                    time.sleep(2)
                    start_farming_response = start_farming(token)
                    if start_farming_response is not None:
                        print(Fore.GREEN + Style.BRIGHT + f"\r[ Farming ] : Started | Reward : {int(start_farming_response['farmingReward']):,}".replace(',', '.'), flush=True)
                    else:
                        if 'error' in start_farming_response:
                            if start_farming_response['error']['message'] == "Farming already started":
                                print(Fore.RED + Style.BRIGHT + f"\r[ Farming ] : Farming Already Started", flush=True)
                        else:
                            print(Fore.RED + Style.BRIGHT + f"\r[ Farming ] : Failed to Start Farming", flush=True)
                else:
                    print(Fore.YELLOW + Style.BRIGHT + f"\r[ Farming ] : Farming Already Started", flush=True)                              
else:
    print(Fore.RED + Style.BRIGHT + f"\r[ Farming ] : Failed to Check Farming", flush=True)
    continue

print(Fore.BLUE + Style.BRIGHT + f"\n==========ALL ACCOUNTS PROCESSED==========\n",  flush=True)    
animated_loading(300)
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
