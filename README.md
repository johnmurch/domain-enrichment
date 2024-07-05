# domain-enrichment

Normalizing Domain data and enrichment for future CRM

# Data Enrichment from Domain

Create a series of scripts leveraging a domain (e.g. jproofingandmetalbuildings.com) and process a set of data enrichment from the domain. Current set includes the following:

- Logo - clearbit api
- Page Fetch - assumes homepage fetch using pyppeteer but could swap with Apify. Also using page.html for caching and blocked sites to manually override
- About Page - assume page.html created - try to extract about page
- Social Links - assume page.html created - try to extract all social links
- Contact Info - assume page.html created - try to extract phone and emails
- OpenAI - leverage a basic prompt and list of domains to create a json output

## Install Dependencies

```
python3.9 -m pip install python-dotenv
python3.9 -m pip install requests
python3.9 -m pip install beautifulsoup4
python3.9 -m pip install pyppeteer
python3.9 -m pip install openai
```

## Data

```
.
├── about.txt
├── company.json
├── contact.txt
├── domain.txt
├── logo.png
├── openai_raw.json
├── page.html
└── social.txt
```

- about.txt - about link
- company.json - using openai and domain to get company name as well as a short description (works some of the time)
- contact.txt - contact (phone/email) from webpage
- domain.txt - page fetched for page.html
- logo.png - clearbit logo (512px) downloaded
- openai_raw.json - raw json response from openai API
- page.html - page source (HTML) of domain
- social.txt - social links (facebook, twitter, etc.)

## Setup

```
echo "OPENAI_API_KEY=your_openai_api_key" > .env
```

## Run

```
python main.py
```

Keep in mind it looks at

- input-domains.txt - can add more domains to this file for fetching and updating
- input-blocked.txt - if you need to add a blocked site, create a folder for domain in blocked/ adding both page.html and domain.txt. You can also run `python generate_blocked_txt.py` to generate the input-blocked.txt file
- failed.txt - created on first pass of main.py when new domains are added

## Useful Scripts

```
python cmd_list.py - listing the files and status for each domain in domains/ folder
```

```
python cmd_contacts.py - listing contacts found per domain
```

```
python cmd_clear.py - ability to manually clear all 'page.html', 'domain.txt', 'contact.txt', 'logo.png','social.txt' for all in domains/
```
