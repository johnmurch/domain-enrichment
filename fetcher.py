import asyncio
import os
from pyppeteer import launch

minimal_args = [
    '--autoplay-policy=user-gesture-required',
    '--disable-background-networking',
    '--disable-background-timer-throttling',
    '--disable-backgrounding-occluded-windows',
    '--disable-breakpad',
    '--disable-client-side-phishing-detection',
    '--disable-component-update',
    '--disable-default-apps',
    '--disable-dev-shm-usage',
    '--disable-domain-reliability',
    '--disable-extensions',
    '--disable-features=AudioServiceOutOfProcess',
    '--disable-hang-monitor',
    '--disable-ipc-flooding-protection',
    '--disable-notifications',
    '--disable-offer-store-unmasked-wallet-cards',
    '--disable-popup-blocking',
    '--disable-print-preview',
    '--disable-prompt-on-repost',
    '--disable-renderer-backgrounding',
    '--disable-setuid-sandbox',
    '--disable-speech-api',
    '--disable-sync',
    '--hide-scrollbars',
    '--ignore-gpu-blacklist',
    '--metrics-recording-only',
    '--mute-audio',
    '--no-default-browser-check',
    '--no-first-run',
    '--no-pings',
    '--no-sandbox',
    '--no-zygote',
    '--password-store=basic',
    '--use-gl=swiftshader',
    '--use-mock-keychain',
    '--single-process',
    '--disable-accelerated-2d-canvas',
    '--disable-gpu',
    "--proxy-server='direct://",
    '--proxy-bypass-list=*',
]

user_agent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/91.0.4472.124 Safari/537.36"
)

async def fetch_html(url, timeout=10):
    try:
        browser = await launch(headless=True, args=minimal_args)
        page = await browser.newPage()
        await page.setUserAgent(user_agent)
        await page.setViewport({'width': 1280, 'height': 800})
        await page.goto(url, {'timeout': timeout * 1000})
        content = await page.content()
        await browser.close()
        return content, url
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None, None

def fetch_html_sync(url, timeout=10):
    return asyncio.get_event_loop().run_until_complete(fetch_html(url, timeout))

def load_or_fetch_html(domain, timeout=10):
    domain_directory = os.path.join('domains', domain)
    html_path = os.path.join(domain_directory, 'page.html')
    url_path = os.path.join(domain_directory, 'domain.txt')

    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8') as file:
            return file.read(), None

    # Try fetching with https://www first, then fallback to https://
    url = f'https://www.{domain}'
    html_content, used_url = fetch_html_sync(url, timeout)
    if not html_content:
        url = f'https://{domain}'
        html_content, used_url = fetch_html_sync(url, timeout)

    if html_content:
        os.makedirs(domain_directory, exist_ok=True)
        with open(html_path, 'w', encoding='utf-8') as file:
            file.write(html_content)
        with open(url_path, 'w', encoding='utf-8') as file:
            file.write(used_url)

    return html_content, used_url
