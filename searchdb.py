import requests
import json

def search_cve(base_url, **kwargs):
    """
    Searches the NVD CVE API with given parameters.
    :param base_url: Base URL of the API.
    :param kwargs: Query parameters for the API.
    :return: JSON response from the API.
    """
    response = requests.get(base_url, params=kwargs)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Request failed with status code {response.status_code}"}

def main():
    base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    
    print("Choose search criteria:")
    print("1. Search by CVE ID")
    print("2. Search by CPE Name")
    print("3. Search by Severity (CVSSv3)")
    print("4. Search by Keywords")
    print("5. Search by CWE ID")
    
    choice = input("Enter your choice (1-5): ")
    params = {}
    
    if choice == "1":
        cve_id = input("Enter CVE ID (e.g., CVE-2023-12345): ")
        params["cveId"] = cve_id
    elif choice == "2":
        cpe_name = input("Enter CPE Name (e.g., cpe:2.3:o:microsoft:windows_10:1607): ")
        params["cpeName"] = cpe_name
    elif choice == "3":
        severity = input("Enter severity level (LOW, MEDIUM, HIGH, CRITICAL): ")
        params["cvssV3Severity"] = severity.upper()
    elif choice == "4":
        keyword = input("Enter keyword for search (e.g., Windows): ")
        params["keywordSearch"] = keyword
    elif choice == "5":
        cwe_id = input("Enter CWE ID (e.g., CWE-287): ")
        params["cweId"] = cwe_id
    else:
        print("Invalid choice!")
        return
    
    print("Fetching results...")
    result = search_cve(base_url, **params)
    
    # Save results to a JSON file
    with open("cve_results.json", "w") as file:
        json.dump(result, file, indent=4)
    
    print("Results saved to cve_results.json")
    
if __name__ == "__main__":
    main()
