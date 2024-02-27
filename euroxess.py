#!/usr/bin/env python3
import argparse
import requests
from bs4 import BeautifulSoup
import json

def extract_job_info(url):
    response = requests.get(url)
    page_content = BeautifulSoup(response.text, 'html.parser')

    # Extracting job information based on the selectors identified
    job_info = {
        "JobTitle": page_content.select_one('h1').text.strip(),
        "Organization": page_content.select_one("dt:contains('Organisation/Company') + dd").text.strip(),
        "ResearchField": page_content.select_one("dt:contains('Research Field') + dd").text.strip(),
        "Profiles": page_content.select_one("dt:contains('Researcher Profile') + dd").text.strip(),
        "ApplicationDeadline": page_content.select_one("dt:contains('Application Deadline') + dd").text.strip(),
        "JobStatus": page_content.select_one("dt:contains('Job Status') + dd").text.strip(),
        "Location": page_content.select_one("dt:contains('Country') + dd").text.strip(),
        "Requirements": "See document for details",  # Assuming detailed requirements are in the document
        "AdditionalInformation": "See document for details",  # Assuming additional info is in the document
        "ContactDetails": {
            "Email": page_content.select_one("dt:contains('E-mail') + dd").text.strip(),
            "Website": page_content.select_one("dt:contains('Website') + dd a").get('href', '').strip()
        },
        "Funding": "Not specified"  # Placeholder, adjust if more specific info is available
    }

    return job_info

def main():
    parser = argparse.ArgumentParser(description="Extract job offer information from a specified URL.")
    parser.add_argument("url", type=str, help="The URL of the job offer page to scrape.")
    parser.add_argument("--file", type=str, help="Filename to save the extracted data as JSON. If not provided, prints to stdout.", default=None)

    args = parser.parse_args()

    if args.url:
        job_info = extract_job_info(args.url)

        if args.file:
            with open(args.file, 'w', encoding='utf-8') as f:
                json.dump(job_info, f, indent=4)
            print(f"Extracted job information saved to '{args.file}'")
        else:
            print(json.dumps(job_info, indent=4))
    else:
        print("Please provide a URL. Use --help for more information.")

if __name__ == "__main__":
    main()

