import openai
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_company_name_and_description_from_domain(domain):
    messages = [
        {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
        {"role": "user", "content": f"Extract the company name, a company description such a 140-character description from the domain: {domain} as well as the domain {domain} and output to json. If the domain is not recognized, respond with empty strings."}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    raw_response = response.choices[0].message['content'].strip()
    try:
        parsed_response = json.loads(raw_response)
        company_name = parsed_response.get("company_name", "")
        company_description = parsed_response.get("company_description", "")
    except json.JSONDecodeError:
        company_name = ""
        company_description = ""
    return company_name, company_description, response.to_dict()

def read_domains_from_file(file_path):
    with open(file_path, 'r') as file:
        domains = file.read().splitlines()
    return domains

def save_company_info(domain, company_info):
    domain_directory = os.path.join('domains', domain)
    os.makedirs(domain_directory, exist_ok=True)
    file_path = os.path.join(domain_directory, 'company.json')
    with open(file_path, 'w') as file:
        json.dump(company_info, file, indent=4)

def save_raw_response(domain, response):
    domain_directory = os.path.join('domains', domain)
    os.makedirs(domain_directory, exist_ok=True)
    file_path = os.path.join(domain_directory, 'openai_raw.json')
    with open(file_path, 'w') as file:
        json.dump(response, file, indent=4)

def main():
    domains_file = 'input-domains.txt'
    domains = read_domains_from_file(domains_file)

    for domain in domains:
        company_name, company_description, raw_response = get_company_name_and_description_from_domain(domain)

        if not company_name:
            company_name = ""
            company_description = ""

        company_info = {
            "domain": domain,
            "company_name": company_name,
            "company_description": company_description
        }

        save_company_info(domain, company_info)
        save_raw_response(domain, raw_response)
        print(f'Saved company info and raw response for {domain} to domains/{domain}/company.json and domains/{domain}/openai_raw.json')

if __name__ == "__main__":
    main()
