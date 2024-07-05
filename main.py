from processor import process_domain, generate_report, read_domains_from_file

if __name__ == "__main__":
    domains_file = 'input-domains.txt'
    domains = read_domains_from_file(domains_file)

    report = {
        'missing_about': [],
        'missing_social': [],
        'missing_contact': [],
        'missing_logo': []
    }

    for domain in domains:
        process_domain(domain, report)
    
    generate_report(report)
