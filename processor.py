import os
import shutil
from fetch_about_us import fetch_about_us_link
from fetch_social_links import fetch_social_links
from fetch_contact_info import fetch_contact_info
from download_logo import download_logo
from fetcher import load_or_fetch_html

def read_domains_from_file(file_path):
    with open(file_path, 'r') as file:
        domains = file.read().splitlines()
    return domains

def save_to_file(directory, filename, content):
    if content.strip():
        file_path = os.path.join(directory, filename)
        with open(file_path, 'w') as file:
            file.write(content)
        return file_path
    return None

def log_failed_domain(domain):
    with open('failed.txt', 'a') as file:
        file.write(f"{domain}\n")

def copy_blocked_pages(domain):
    blocked_file = 'blocked.txt'
    with open(blocked_file, 'r') as file:
        blocked_domains = file.read().splitlines()
    
    if domain in blocked_domains:
        src_file = f'blocked/{domain}/page.html'
        dst_dir = f'domains/{domain}'
        dst_file = f'{dst_dir}/page.html'
        if os.path.exists(src_file):
            os.makedirs(dst_dir, exist_ok=True)
            shutil.copy2(src_file, dst_file)
            print(f'Copied {src_file} to {dst_file}')
        else:
            print(f'No blocked page found for {domain} in {src_file}')

def process_domain(domain, report):
    print(f'Processing domain: {domain}')
    domain_directory = os.path.join('domains', domain)
    os.makedirs(domain_directory, exist_ok=True)

    # Copy blocked pages before fetching content
    copy_blocked_pages(domain)
    
    # Check if blocked page exists and use it if available
    blocked_page_path = os.path.join(domain_directory, 'page.html')
    if os.path.exists(blocked_page_path):
        with open(blocked_page_path, 'r') as file:
            html_content = file.read()
        used_url = None
    else:
        html_content, used_url = load_or_fetch_html(domain)
        if used_url:
            save_to_file(domain_directory, 'domain.txt', used_url)

    if not html_content:
        print(f"Failed to fetch content for {domain}")
        log_failed_domain(domain)
        report['missing_about'].append(domain)
        report['missing_social'].append(domain)
        report['missing_contact'].append(domain)
        report['missing_logo'].append(domain)
        return

    about_us_link = fetch_about_us_link(domain)
    if about_us_link:
        save_to_file(domain_directory, 'about.txt', about_us_link)
        print(f'About Us Link saved to {os.path.join(domain_directory, "about.txt")}')
    else:
        print('No About Us link found.')
        report['missing_about'].append(domain)

    social_links_map = fetch_social_links(domain)
    if social_links_map:
        social_links_content = '\n'.join([f"{platform}: {link}" for platform, link in social_links_map.items()])
        save_to_file(domain_directory, 'social.txt', social_links_content)
        print(f'Social Links saved to {os.path.join(domain_directory, "social.txt")}')
    else:
        print("No social links found.")
        report['missing_social'].append(domain)

    contact_info = fetch_contact_info(domain)
    contact_info_content = ''
    if contact_info:
        if contact_info['phone_numbers']:
            contact_info_content += 'Phone Numbers:\n' + '\n'.join(contact_info['phone_numbers']) + '\n'
        if contact_info['emails']:
            contact_info_content += 'Emails:\n' + '\n'.join(contact_info['emails'])
        
    contact_file_path = save_to_file(domain_directory, 'contact.txt', contact_info_content.strip())
    if contact_file_path:
        print(f'Contact Info saved to {contact_file_path}')
    else:
        print("No contact info found.")
        report['missing_contact'].append(domain)

    logo_path = download_logo(domain, domain_directory)
    if logo_path:
        print(f'Logo downloaded and saved to {logo_path}')
    else:
        print(f'Failed to download logo for {domain}')
        report['missing_logo'].append(domain)

def generate_report(report):
    print("\n--- Report ---")
    print(f"Domains missing 'About Us' link: {len(report['missing_about'])}")
    for domain in report['missing_about']:
        print(f" - {domain}")
    
    print(f"\nDomains missing social links: {len(report['missing_social'])}")
    for domain in report['missing_social']:
        print(f" - {domain}")

    print(f"\nDomains missing contact info: {len(report['missing_contact'])}")
    for domain in report['missing_contact']:
        print(f" - {domain}")

    print(f"\nDomains missing logo: {len(report['missing_logo'])}")
    for domain in report['missing_logo']:
        print(f" - {domain}")
    print("\n--------------")
