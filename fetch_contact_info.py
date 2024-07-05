import re
from bs4 import BeautifulSoup
from fetcher import load_or_fetch_html

def fetch_contact_info(domain):
    html_content, _ = load_or_fetch_html(domain)
    if not html_content:
        return None

    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove all svg, img, and other non-text tags
    for tag in soup(['svg', 'img', 'script', 'style', 'noscript']):
        tag.decompose()
    
    # Get the cleaned text content
    cleaned_text_content = soup.get_text(separator=' ', strip=True)

    # Regular expression to find phone numbers
    phone_pattern = re.compile(r'(?<!\d)(?:\+?\d{1,3})?[\s\-\.]?\(?\d{3}\)?[\s\-\.]?\d{3}[\s\-\.]?\d{4}(?!\d)')
    
    # Regular expression to find email addresses
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

    phone_numbers = set(phone_pattern.findall(cleaned_text_content))
    emails = set(email_pattern.findall(cleaned_text_content))

    contact_info = {
        'phone_numbers': list(phone_numbers),
        'emails': list(emails)
    }

    return contact_info
