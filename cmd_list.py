import os

def list_files():
    domains_directory = 'domains'
    expected_files = ['page.html', 'domain.txt', 'contact.txt', 'logo.png']

    for domain_dir in os.listdir(domains_directory):
        domain_path = os.path.join(domains_directory, domain_dir)
        if os.path.isdir(domain_path):
            print(f'\nDomain: {domain_dir}')
            found_files = os.listdir(domain_path)
            for file in found_files:
                print(f'  Found: {file}')

            for expected_file in expected_files:
                if expected_file not in found_files:
                    print(f'  Missing: {expected_file}')
                    
if __name__ == "__main__":
    list_files()