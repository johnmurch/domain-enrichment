import os

def generate_blocked_txt():
    blocked_directory = 'blocked'
    blocked_file_path = 'blocked.txt'

    blocked_domains = []

    for domain_dir in os.listdir(blocked_directory):
        domain_path = os.path.join(blocked_directory, domain_dir)
        page_file = os.path.join(domain_path, 'page.html')
        if os.path.isdir(domain_path) and os.path.exists(page_file):
            blocked_domains.append(domain_dir)

    with open(blocked_file_path, 'w') as blocked_file:
        for domain in blocked_domains:
            blocked_file.write(f"{domain}\n")

    print(f'Generated {blocked_file_path} with the following domains:')
    for domain in blocked_domains:
        print(domain)

if __name__ == "__main__":
    generate_blocked_txt()

