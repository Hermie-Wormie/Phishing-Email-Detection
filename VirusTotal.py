import hashlib
import requests
import re
from email.parser import Parser

API_KEY = 'c177ebfe27c37c0aec97609d333dcf803645c65fc855f44d5ffebfd8993ff700'
VT_URL = 'https://www.virustotal.com/vtapi/v2/url/report'


def file_to_hash(file_path):
    sha256_hash = hashlib.sha256()

    with open(file_path, "rb") as file:
        # Read the file in chunks to avoid memory overload with large files
        for byte_block in iter(lambda: file.read(4096), b""):
            sha256_hash.update(byte_block)

    return sha256_hash.hexdigest()


def check_hash(file_hash):
    url = f"https://www.virustotal.com/vtapi/v2/file/report"
    params = {
        'apikey': API_KEY,
        'resource': file_hash
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}"


def check_url(url):
    params = {'apikey': API_KEY, 'resource': url}
    response = requests.get(VT_URL, params=params)

    # Check if response is successful
    if response.status_code == 200:
        result = response.json()
        if result:
            url_scan_results(result)
        else:
            return "Empty response from VirusTotal."
    else:
        return f"Error: {response.status_code} from VirusTotal"


def url_scan_results(result):
    if result is None:
        return "No result returned from VirusTotal."

    if result['response_code'] == 1:
        if result['positives'] > 0:
            numPositive = result['positives']
            return numPositive
        #     print(f"Vendors that flagged this site as malicious:")
        #     for vendor, report in result['scans'].items():
        #         if report['detected']:
        #             print(f"     - {vendor}: {report['result']}")
        # else:
        #     print("Clean URL")
        else:
            return "Clean URL"
    else:
        return "URL not found in VirusTotal database"


def print_hash_scan_results(result):
    if result['response_code'] == 1:
        print(f"Hash: {result['resource']}")

        if result['positives'] > 0:
            print(f"Malicious! Positives: {result['positives']}")
            print(f"Vendors that flagged this file as malicious:")

            for vendor, report in result['scans'].items():
                if report['detected']:
                    print(f"     - {vendor}: {report['result']}")
        else:
            print("The file is clean.")
    else:
        print("Hash not found in VirusTotal database.\n")


if __name__ == "__main__":

    # URL and Filepath of attachment
    url = "http://myetherevvalliet.com/"
    file_path = r"C:\Users\herma\OneDrive\Desktop\hi.jpg"

    # Check URL on VirusTotal
    # check_url(url)

    # Test malicious hash: b1b74ff5c67cfdc16f1cb30db9b885046c4c5d71af575a2d3de4a79918c1ce89
    # hash_result = check_hash("b1b74ff5c67cfdc16f1cb30db9b885046c4c5d71af575a2d3de4a79918c1ce89")

    # Hash file then check VirusTotal 
    # hash_of_file = file_to_hash(file_path)
    # hash_result = check_hash(hash_of_file)
    # print_hash_scan_results(hash_result)
