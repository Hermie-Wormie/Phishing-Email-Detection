import hashlib
import requests
import re
from email.parser import Parser

API_KEY = 'c177ebfe27c37c0aec97609d333dcf803645c65fc855f44d5ffebfd8993ff700'
VT_URL = 'https://www.virustotal.com/vtapi/v2/url/report'
VT_FILE = 'https://www.virustotal.com/vtapi/v2/file/report'


def file_to_hash(file_path):
    sha256_hash = hashlib.sha256()

    with open(file_path, "rb") as file:
        # Read the file in chunks to avoid memory overload with large files
        for byte_block in iter(lambda: file.read(4096), b""):
            sha256_hash.update(byte_block)

    return sha256_hash.hexdigest()


def check_hash(file_hash):
    params = {'apikey': API_KEY, 'resource': file_hash}
    response = requests.get(VT_FILE, params=params)

    # Check if response is successful
    if response.status_code == 200:
        result = response.json()
        if result:
            return hash_scan_results(result)

        else:
            return "Empty response from VirusTotal."
    else:
        return f"Error: {response.status_code} from VirusTotal"


def hash_scan_results(result):
    if result['response_code'] == 1:

        if result['positives'] > 0:
            num_positives = result['positives']
            vt_link = result['permalink']
            return num_positives, vt_link

        else:
            return "The file is clean."
    else:
        return "Hash of file not found in VirusTotal database."


def check_url(url):
    params = {'apikey': API_KEY, 'resource': url}
    response = requests.get(VT_URL, params=params)

    # Check if response is successful
    if response.status_code == 200:
        result = response.json()
        if result:
            return url_scan_results(result)

        else:
            return "Empty response from VirusTotal."
    else:
        return f"Error: {response.status_code} from VirusTotal"


def url_scan_results(result):
    if result is None:
        return "No result returned from VirusTotal."

    if result['response_code'] == 1:
        if result['positives'] > 0:
            num_positive = result['positives']
            vt_link = result['permalink']
            return num_positive, vt_link

        else:
            return "Clean URL"

    else:
        return "URL not found in VirusTotal database"


if __name__ == "__main__":
    
    # Test malicious url: 
    url = "http://www.myetherevvalliet.com/"
    # print(check_url(url))

    # Test malicious hash: 
    hash = "b1b74ff5c67cfdc16f1cb30db9b885046c4c5d71af575a2d3de4a79918c1ce89"
    # print(check_hash(hash))

    # Hash file then check VirusTotal
    # hash_of_file = file_to_hash(file_path)
    # print(check_hash(hash_of_file))
