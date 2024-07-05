import os
import requests

def download_logo(domain, save_path, timeout=10):
    logo_url = f'https://logo.clearbit.com/{domain}?size=512'
    logo_path = os.path.join(save_path, 'logo.png')

    try:
        response = requests.get(logo_url, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException:
        return None

    with open(logo_path, 'wb') as file:
        file.write(response.content)
    return logo_path
