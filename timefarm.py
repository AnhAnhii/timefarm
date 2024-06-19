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
        # Jika parameter --upgrade tidak diberikan, minta input dari pengguna
        task_input = input("Bạn có muốn tự động nhận nhiệm vụ không? (y/n, mặc định n): ").strip().lower()
        # Jika pengguna hanya menekan enter, gunakan 'n' sebagai default
        args.task = task_input if task_input in ['y', 'n'] else 'n'
    
    if args.upgrade is None:
        upgrade_input = input("Bạn có muốn tự động nâng cấp đồng hồ không? (y/n, mặc định n): ").strip().lower()
        args.upgrade = upgrade_input if upgrade_input in ['y', 'n'] else 'n'

    return args

args = parse_arguments()
cek_task_enable = args.task
cek_upgrade_enable = args.upgrade
# Set headers sekali saja di awal
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
        response.raise_for_status()  # Akan memicu error jika status bukan 200
        return response.json()
    except json.JSONDecodeError:
        print(f"Lỗi giải mã JSON: Query của bạn sai")
        return None
    except requests.RequestException as e:
        print(f"Lỗi yêu cầu: {e}")
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
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    return response.json()
def submit_task(token, task_id):
    url = f'https://tg-bot-tap.laborx.io/api/v1/tasks/{task_id}/submissions'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json={})
    return response.json()

def claim_task(token, task_id):
    url = f'https://tg-bot-tap.laborx.io/api/v1/tasks/{task_id}/claims'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, json={})
    return response.json()
start_time = datetime.now()
def upgrade_level(token):
    url = 'https://tg-bot-tap.laborx.io/api/v1/me/level/upgrade'
    headers = {
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
    response = requests.post(url, headers=headers)
    # print(response.json())
    return response.json()

def auto_upgrade(token):
    while True:
        response = upgrade_level(token)
        if 'error' in response:
            if response['error']['message'] == "Not enough balance":
                print(Fore.RED + Style.BRIGHT + f"\r[ Nâng cấp ] : Không đủ số dư để nâng cấp.", flush=True)
                break
            elif response['error']['message'] == "Forbidden":
                print(Fore.RED + Style.BRIGHT + f"\r[ Nâng cấp ] : Lỗi nâng cấp.", flush=True)
            elif response['error']['message'] == "Max level reached":
                print(Fore.RED + Style.BRIGHT + f"\r[ Nâng cấp ] : Đã đạt cấp độ tối đa.", flush=True)
                break
            else:
                print(Fore.RED + Style.BRIGHT + f"\r[ Nâng cấp ] : Lỗi nâng cấp. {response['error']['message']}", flush=True)
                break
        else:
            print(Fore.GREEN + Style.BRIGHT + f"\r[ Nâng cấp ] : Nâng cấp thành công, tiếp theo..", flush=True)

# Tambahkan pemanggilan fungsi ini di dalam loop utama jika pengguna memilih untuk auto upgrade


def animated_loading(duration):
    frames = ["|", "/", "-", "\\"]
    end_time = time.time() + duration
    while time.time() < end_time:
        remaining_time = int(end_time - time.time())
        for frame in frames:
            print(f"\rĐang chờ thời gian nhận tiếp theo {frame} - Còn lại {remaining_time} giây         ", end="", flush=True)
            time.sleep(0.25)
    print("\rĐang chờ thời gian nhận tiếp theo hoàn thành.                            ", flush=True)     
def print_welcome_message():
    print(r"""
          
█▀▀ █░█ ▄▀█ █░░ █ █▄▄ █ █▀▀
█▄█ █▀█ █▀█ █▄▄ █ █▄█ █ ██▄
          """)
    print(Fore.GREEN + Style.BRIGHT + "TimeFarm BOT")
    print(Fore.CYAN + Style.BRIGHT + "Liên kết cập nhật: https://github.com/adearman/timefarm")
    print(Fore.YELLOW + Style.BRIGHT + "Credit: https://t.me/ghalibie")
    current_time = datetime.now()
    up_time = current_time - start_time
    days, remainder = divmod(up_time.total_seconds(), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(Fore.CYAN + Style.BRIGHT + f"Thời gian bot chạy: {int(days)} ngày, {int(hours)} giờ, {int(minutes)} phút, {int(seconds)} giây")

def extract_user_details(query_line):
    parts = query_line.split(' ')
    token = parts[0]
    user_id = parts[1]
    username = parts[2]
    return token, user_id, username

def read_query_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

def run_bot(file_path):
    query_lines = read_query_file(file_path)
    for query_line in query_lines:
        token, user_id, username = extract_user_details(query_line)
        print_welcome_message()
        response = get_access_token_and_info(query_line)
        if response is None:
            continue
        access_token = response['access_token']
        user_info = response['user']
        username = user_info['username']
        user_id = user_info['id']
        print(f"Xin chào, {username}! ID của bạn là {user_id}.")
        while True:
            farming_info = cek_farming(access_token)
            if 'error' in farming_info:
                if farming_info['error']['message'] == 'Farming is not running':
                    start_response = start_farming(access_token)
                    if 'error' in start_response:
                        print(Fore.RED + Style.BRIGHT + f"\r[ Khởi động Farming ] : Lỗi khi khởi động farming. {start_response['error']['message']}", flush=True)
                    else:
                        print(Fore.GREEN + Style.BRIGHT + "\r[ Khởi động Farming ] : Khởi động farming thành công.", flush=True)
                else:
                    print(Fore.RED + Style.BRIGHT + f"\r[ Kiểm tra Farming ] : Lỗi khi kiểm tra farming. {farming_info['error']['message']}", flush=True)
            else:
                finish_response = finish_farming(access_token)
                if 'error' in finish_response:
                    print(Fore.RED + Style.BRIGHT + f"\r[ Kết thúc Farming ] : Lỗi khi kết thúc farming. {finish_response['error']['message']}", flush=True)
                else:
                    print(Fore.GREEN + Style.BRIGHT + "\r[ Kết thúc Farming ] : Kết thúc farming thành công.", flush=True)

            if cek_task_enable == 'y':
                tasks = cek_task(access_token)
                for task in tasks:
                    task_id = task['id']
                    task_status = task['status']
                    if task_status == 'pending':
                        claim_response = claim_task(access_token, task_id)
                        if 'error' in claim_response:
                            print(Fore.RED + Style.BRIGHT + f"\r[ Nhận Nhiệm vụ ] : Lỗi khi nhận nhiệm vụ. {claim_response['error']['message']}", flush=True)
                        else:
                            print(Fore.GREEN + Style.BRIGHT + f"\r[ Nhận Nhiệm vụ ] : Nhận nhiệm vụ thành công. ID Nhiệm vụ: {task_id}", flush=True)
                    elif task_status == 'completed':
                        submit_response = submit_task(access_token, task_id)
                        if 'error' in submit_response:
                            print(Fore.RED + Style.BRIGHT + f"\r[ Nộp Nhiệm vụ ] : Lỗi khi nộp nhiệm vụ. {submit_response['error']['message']}", flush=True)
                        else:
                            print(Fore.GREEN + Style.BRIGHT + f"\r[ Nộp Nhiệm vụ ] : Nộp nhiệm vụ thành công. ID Nhiệm vụ: {task_id}", flush=True)
            if cek_upgrade_enable == 'y':
                auto_upgrade(access_token)
            animated_loading(300)  # Delay antara setiap farming 5 phút

if __name__ == "__main__":
    init(autoreset=True)
    file_path = 'query.txt'  # Ganti dengan path file query Anda
    run_bot(file_path)
