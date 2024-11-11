import yaml
import requests
import sys
from urllib.parse import urlparse
import json
from collections import defaultdict
import argparse
import schedule
import time
from datetime import datetime

results = {}

def read_config(path: str):
    try:
        with open(path, "r") as f:
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
        headers = endpoint.get("headers", {})
        method = endpoint.get("method", "GET")
        name = endpoint.get("name", "Unnamed endpoint")
        url = endpoint.get("url")
        body = endpoint.get("body")
        domain = urlparse(url).netloc

        if isinstance(body, str):
            try:
                body = json.loads(body)
            except:
                pass

        res = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=body if headers.get("content-type") == "application/json" else None,
            data=body if headers.get("content-type") != "application/json" else None,
            timeout=10,
        )
        return domain, res.status_code in range(200, 300)

    except requests.Timeout:
        print(f"Timeout error checking {name} ({url})")
        return domain, False
    except requests.RequestException as e:
        print(f"Error checking {name}: {str(e)}")
        return domain, False


def check_cycle(endpoints):
    for endpoint in endpoints:
        domain, success = health_check(endpoint)

        if domain not in results.keys():
            results[domain] = defaultdict(int)

        results[domain]["total"] += 1
        if success:
            results[domain]["up"] += 1

    # print result
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\nHealth Check Results (Last Updated: {current_time}):")
    print("-" * 50)

    for domain, result in sorted(results.items()):
        availability = round(result["up"] / result["total"] * 100)
        print(f"{domain} has {availability}% availability percentage")


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Health check endpoints defined in a YAML file"
    )
    parser.add_argument(
        "-c",
        dest="file_path",
        help="Path to the YAML config file containing endpoint definitions",
        required=False,
    )
    parser.add_argument(
        "-s",
        dest="second",
        help="Health check test cycle length (default 15 seconds)",
        required=False,
    )
    args = parser.parse_args()

    file_path = (
        args.file_path if args.file_path else input("Please input config file path:\n")
    )
    endpoints = read_config(file_path)
    if not endpoints:
        print("No endpoint in content...")
        sys.exit(1)

    second = args.second if args.second else 15
    schedule.every(second).seconds.do(check_cycle, endpoints=endpoints)

    print(f"\nStarting health check monitor (checking every {args.second} seconds)")
    print("Press Ctrl+C to exit")
    # Run initial check immediately
    schedule.run_all()

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nexit the program...")
