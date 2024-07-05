import os
import sys

def remove_files(file_type):
    if file_type not in ['page.html', 'domain.txt', 'contact.txt', 'logo.png','social.txt']:
        print(f"Invalid file type specified: {file_type}")
        return

    domains_directory = 'domains'
    
    for domain_dir in os.listdir(domains_directory):
        domain_path = os.path.join(domains_directory, domain_dir)
        file_path = os.path.join(domain_path, file_type)
        
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f'Removed {file_path}')
        else:
            print(f'No {file_type} found in {domain_path}')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python remove_files.py <file_type>")
        print("file_type: page.html, domain.txt, contact.txt, logo.png, social.txt")
        sys.exit(1)
    
    file_type = sys.argv[1]
    remove_files(file_type)

