import re
from bs4 import BeautifulSoup
from fetcher import load_or_fetch_html

def fetch_social_links(domain):
    html_content, _ = load_or_fetch_html(domain)
    if not html_content:
        return None

    soup = BeautifulSoup(html_content, 'html.parser')

    social_platforms = {
        'Facebook': 'facebook.com',
        'Twitter': 'twitter.com',
        'Instagram': 'instagram.com',
        'YouTube': 'youtube.com',
        'LinkedIn': 'linkedin.com',
        'Pinterest': 'pinterest.com',
        'TikTok': 'tiktok.com',
        'Snapchat': 'snapchat.com',
        'Reddit': 'reddit.com',
        'Tumblr': 'tumblr.com',
        'Flickr': 'flickr.com',
        'Medium': 'medium.com',
        'Quora': 'quora.com',
        'Vimeo': 'vimeo.com',
        'WhatsApp': 'whatsapp.com',
        'WeChat': 'wechat.com',
        'Discord': 'discord.com'
    }

    social_links_map = {}

    anchors = soup.find_all('a', href=True)

    for link in anchors:
        href = link['href']
        for platform, domain in social_platforms.items():
            if domain in href:
                social_links_map[platform] = href
                break

    return social_links_map
