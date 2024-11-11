import yaml
import requests
import sys
from urllib.parse import urlparse
import json
from collections import defaultdict
import argparse
import schedule
import time

results = {}

def read_config(path: str):
    try:
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {path}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
def health_check(endpoint):
    try:
        headers = endpoint.get('headers', {})
        method = endpoint.get('method', 'GET')
        name = endpoint.get('name', 'Unnamed endpoint')
        url = endpoint.get('url')
        body = endpoint.get('body')
        domain = urlparse(url).netloc

        if isinstance(body, str):
            try:
                body = json.loads(body)
            except:
                pass
        
        res = requests.request(method=method, url=url, headers=headers, json=body)
        return domain, res.status_code in range(200, 300)
        
    except requests.RequestException as e:
        print(f"Error checking {name}: {str(e)}")
        return domain, False

def check_cycle(endpoints):
    print('cycle:')
    for endpoint in endpoints:
        domain, success = health_check(endpoint)

        if domain not in results.keys():
            results[domain] = defaultdict(int)

        results[domain]['total'] += 1
        if success:
            results[domain]['up'] += 1
    print(results)
    for domain, result in results.items():
        availability = round(result['up'] / result['total'] * 100)
        print(domain, ' has', availability, '% availability percentage')

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Health check endpoints defined in a YAML file')
    parser.add_argument('-c', dest='file_path', help='Path to the YAML config file containing endpoint definitions', required=False)
    parser.add_argument('-s', dest='second', help='Health check test cycle length (second)', required=False)
    args = parser.parse_args()

    file_path = args.file_path if args.file_path else input('Please input config file path:\n')
    endpoints = read_config(file_path)
    if(not endpoints):
        print('No endpoint in content...')
        sys.exit(1)
    
    schedule.every(15).seconds.do(check_cycle, endpoints=endpoints)
    schedule.run_all()
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()



