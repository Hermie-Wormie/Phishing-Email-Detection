import requests
import re
from email.parser import Parser

API_KEY = 'c177ebfe27c37c0aec97609d333dcf803645c65fc855f44d5ffebfd8993ff700'
VT_URL = 'https://www.virustotal.com/vtapi/v2/url/report'


def extract_urls(email_content):
    url_pattern = r'(https?://[^\s]+)'
    urls = re.findall(url_pattern, email_content)
    return urls


def check_url_virustotal(url):
    params = {'apikey': API_KEY, 'resource': url}
    response = requests.get(VT_URL, params=params)
    return response.json()


def scan_email(email_content):
    urls = extract_urls(email_content)
    results = {}

    for url in urls:
        result = check_url_virustotal(url)
        results[url] = result
    
    return results

def print_scan_results(results):
    for url, result in results.items():
        print(f"Scanning URL: {url}")
        if result['response_code'] == 1:
            if result['positives'] > 0:
                print(f"Malicious! Positives: {result['positives']}")
                print(f"Vendors that flagged this site as malicious:")
                for vendor, report in result['scans'].items():
                    if report['detected']:
                        print(f"     - {vendor}: {report['result']}")

            else:
                print("Clean URL")
        else:
            print("URL not found in VirusTotal database")
        print("\n")


if __name__ == "__main__":
    email_content = """
    Hello, check out this link: http://google.com/
    Also visit: http://myetherevvalliet.com/
    """

    results = scan_email(email_content)

    print_scan_results(results)