import subprocess
import argparse
import json
import os

def run_nmap_scan(target):
    """Performs Nmap scan for open ports and service enumeration."""
    print("[+] Running Nmap scan...")
    result = subprocess.run(["nmap", "-sV", "-T4","--unprivileged", "-oN", "nmap_scan.txt", target], capture_output=True, text=True)
    return result.stdout

def grab_banner(target, port):
    """Grabs banners using Curl on Windows."""
    print(f"[+] Grabbing banner for {target}:{port}...")
    try:
        result = subprocess.run(["curl", "-I", f"http://{target}:{port}"], capture_output=True, text=True, timeout=5)
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "Timeout"




def take_screenshot(target):
    """Uses Eyewitness to capture screenshots of websites."""
    print("[+] Capturing screenshot...")
    subprocess.run(["eyewitness", "--web", "-f", target, "-d", "screenshots/", "--no-prompt"], capture_output=True, text=True)
    #subprocess.run(["eyewitness", "--web", "-f", target, "-d", "screenshots/", "--no-prompt"], capture_output=True, text=True)
    subprocess.run(["wsl", "eyewitness", "--web", "-f", target, "-d", "screenshots/", "--no-prompt"], capture_output=True, text=True)

def brute_force_dirs(target):
    """Runs Gobuster to find hidden directories."""
    print("[+] Running Gobuster...")
    wordlist = "common.txt"  # Adjust wordlist path as needed
    result = subprocess.run(["gobuster", "dir", "-u", target, "-w", wordlist, "-o", "gobuster_results.txt"], capture_output=True, text=True)
    return result.stdout
    wordlist = r"C:\Users\SAYF EDDINE\Documents\GitHub\ReconMaster\scan\common.txt"
    if not os.path.exists(wordlist):
        print(f"[!] Wordlist not found at {wordlist}")
        return ""
    target = f"http://{target}"  # Ensure proper URL format
    result = subprocess.run(["gobuster", "dir", "-u", target, "-w", wordlist, "-o", "gobuster_results.txt"], 
                            capture_output=True, text=True)
    if result.stderr:
        print(f"[!] Gobuster error: {result.stderr}")
    with open("gobuster_results.txt", "r") as f:
        output = f.read()
    print(f"[+] Gobuster output: {output}")
    return output


def take_screenshot(target):
    """Uses Eyewitness to capture screenshots of websites."""
    print("[+] Capturing screenshot...")
    subprocess.run(["eyewitness", "--web", "-f", target, "-d", "screenshots/", "--no-prompt"], capture_output=True, text=True)
    #subprocess.run(["eyewitness", "--web", "-f", target, "-d", "screenshots/", "--no-prompt"], capture_output=True, text=True)
    subprocess.run(["wsl", "eyewitness", "--web", "-f", target, "-d", "screenshots/", "--no-prompt"], capture_output=True, text=True)

 
def main():
    parser = argparse.ArgumentParser(description="Automated Active Recon Script")
    parser.add_argument("target", help="Target IP or domain")
    args = parser.parse_args()
    
    scan_results = run_nmap_scan(args.target)
    
    open_ports = [line.split("/")[0] for line in scan_results.split("\n") if "/tcp" in line and "open" in line]
    
    banners = {port: grab_banner(args.target, port) for port in open_ports}
    
    dirbusting_results = brute_force_dirs(args.target)
    
    take_screenshot(args.target)
    
    report = {
        "target": args.target,
        "nmap_results": scan_results,
        "banners": banners,
        "dirbusting_results": dirbusting_results
    }
    
    with open("recon_report.json", "w") as f:
        json.dump(report, f, indent=4)
    
    print("[+] Recon completed. Results saved to recon_report.json")

if __name__ == "__main__":
    main()
