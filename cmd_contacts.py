import os

def view_contacts():
    domains_directory = 'domains'
    
    for domain_dir in os.listdir(domains_directory):
        domain_path = os.path.join(domains_directory, domain_dir)
        contact_file_path = os.path.join(domain_path, 'contact.txt')
        
        if os.path.isfile(contact_file_path):
            with open(contact_file_path, 'r', encoding='utf-8') as file:
                contact_content = file.read()
                print(f"Domain: {domain_dir}")
                print(contact_content)
                print("-" * 40)

if __name__ == "__main__":
    view_contacts()
