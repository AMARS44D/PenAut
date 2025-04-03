# File: shodan_scan.py
from shodan import Shodan, APIError
import json
import logging

# Configuration
OUTPUT_FILE = 'shodan_results.json'
SEARCH_QUERY = 'appache'  # Your query
RESULT_LIMIT = 10
API_KEY = '4r0qsTvjuSvnYubE1v0iow4Z2hbWEfg2'

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def save_to_file(data, filename):
    """Save data to a JSON file with pretty formatting."""
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4, separators=(',', ': '))
        logging.info(f"Results saved to {filename}")
    except Exception as e:
        logging.error(f"Failed to save results to {filename}: {e}")

def search_shodan(api, query, limit):
    """Search Shodan for the given query and return results."""
    results = []
    try:
        for banner in api.search_cursor(query):
            results.append(banner)
            if len(results) >= limit:
                break
        logging.info(f"Found {len(results)} results for query: {query}")
        return results
    except APIError as e:
        logging.error(f"Shodan search error: {e}")
        return []

def get_ics_count(api):
    """Get the count of industrial control systems services."""
    try:
        ics_services = api.count('tag:ics')
        total = ics_services.get("total", "Unknown")
        logging.info(f"Industrial Control Systems: {total}")
        return total
    except APIError as e:
        logging.error(f"Shodan count error: {e}")
        return "Unknown"

def main():
    # Initialize Shodan API
    api = Shodan(API_KEY)

    # Lookup an IP address
    try:
        ipinfo = api.host('8.8.8.8')
        logging.info("IP Info retrieved successfully.")
    except APIError as e:
        logging.error(f"Shodan API error while retrieving IP info: {e}")
        ipinfo = {}

    # Search for websites that match the query
    search_results = search_shodan(api, SEARCH_QUERY, RESULT_LIMIT)

    # Get the count of industrial control systems services
    ics_count = get_ics_count(api)

    # Combine all results into a single dictionary
    results = {
        "ip_info": ipinfo,
        "search_results": search_results,
        "ics_count": ics_count
    }

    # Save results to a file
    save_to_file(results, OUTPUT_FILE)

if __name__ == "__main__":
    main()