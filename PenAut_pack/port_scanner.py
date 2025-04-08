import subprocess
import argparse
import json
import os

def run_nmap_scan(target):
    """Performs Nmap scan for open ports and service enumeration."""
    print("[+] Running Nmap scan...")
    result = subprocess.run(["nmap", "-sV", "-T4", "--unprivileged", "-oN", "../result/nmap_scan.txt", target], capture_output=True, text=True)
    return result.stdout


def run_vuln_scan(target):
    """Runs Nmap using the 'vuln' script category to find known vulnerabilities."""
    print("[+] Running vulnerability scan using Nmap vuln scripts...")
    vuln_output_file = "../result/vuln_scan.txt"
    result = subprocess.run(["nmap", "-sV", "--script=vuln","--unprivileged", "-T4", "-oN", vuln_output_file, target],
                            capture_output=True, text=True)
    return result.stdout



def grab_banner(target, port):
    """Grabs banners using Curl on Windows."""
    print(f"[+] Grabbing banner for {target}:{port}...")
    try:
        result = subprocess.run(["curl", "-I", f"http://{target}:{port}"], capture_output=True, text=True, timeout=5)
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "Timeout"

def brute_force_dirs(target):
    """Runs Gobuster to find hidden directories."""
    print("[+] Running Gobuster...")
    wordlist = "common.txt"  # Adjust path if needed
    if not os.path.exists(wordlist):
        print(f"[!] Wordlist not found at {wordlist}")
        return ""
    target_url = f"http://{target}"
    result = subprocess.run(["gobuster", "dir", "-u", target_url, "-w", wordlist, "-o", "../result/gobuster_results.txt"], 
                            capture_output=True, text=True)
    if result.stderr:
        print(f"[!] Gobuster error: {result.stderr}")
    return result.stdout

def main_port():
    parser = argparse.ArgumentParser(description="Automated Active Recon Script")
    parser.add_argument("target", help="Target IP or domain")
    args = parser.parse_args()

    scan_results = run_nmap_scan(args.target)
    vuln_results = run_vuln_scan(args.target)

    open_ports = [line.split("/")[0] for line in scan_results.split("\n") if "/tcp" in line and "open" in line]
    banners = {port: grab_banner(args.target, port) for port in open_ports}

    dirbusting_results = brute_force_dirs(args.target)

    report = {
        "target": args.target,
        "nmap_results": scan_results,
        "vulnerability_scan": vuln_results,
        "banners": banners,
        "dirbusting_results": dirbusting_results
    }

    os.makedirs("../result", exist_ok=True)
    with open("../result/recon_report.json", "w") as f:
        json.dump(report, f, indent=4)

    print("[+] Recon completed. Results saved to recon_report.json")
