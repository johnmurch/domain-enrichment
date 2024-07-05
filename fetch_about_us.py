import re
from bs4 import BeautifulSoup
from fetcher import load_or_fetch_html

def fetch_about_us_link(domain):
    html_content, _ = load_or_fetch_html(domain)
    if not html_content:
        return None

    soup = BeautifulSoup(html_content, 'html.parser')
    about_us_patterns = [
        re.compile(r'/company/about(-us)?', re.IGNORECASE),
        re.compile(r'/about(-us)?', re.IGNORECASE),
        re.compile(r'about(-us)?', re.IGNORECASE)
    ]

    anchors = soup.find_all('a', href=True)
    matches = []

    for anchor in anchors:
        href = anchor['href']
        normalized_href = href.lower()
        for pattern in about_us_patterns:
            if pattern.search(normalized_href):
                matches.append(href)

    if not matches:
        return None

    matches.sort(key=lambda x: len(x.split('/')))
    return matches[0]
