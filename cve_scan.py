# CVE Vulnerability Scanner (Basic)
import requests

def get_vulnerabilities(query, results=5):
    url = f"https://services.nvd.nist.gov/rest/json/cves/1.0?keyword={query}&resultsPerPage={results}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        vulnerabilities = data.get("result", {}).get("CVE_Items", [])

        if not vulnerabilities:
            print(f"No vulnerabilities found for '{query}'.")
            return

        print(f"Top {results} vulnerabilities for '{query}':\n")
        for vuln in vulnerabilities:
            cve_id = vuln.get("cve", {}).get("CVE_data_meta", {}).get("ID", "Unknown")
            description = vuln.get("cve", {}).get("description", {}).get("description_data", [{}])[0].get("value", "No description")
            print(f"[{cve_id}] {description}\n")

    else:
        print("Failed to retrieve data from NVD.")

# Example usage
service = input("Enter software/service name (e.g., Apache, OpenSSH): ")
get_vulnerabilities(service)
