import subprocess
import json
import os

def run_nmap_scan(target):
    """Performs Nmap scan for open ports and service enumeration."""
    print("[+] Running Nmap scan...")
    result = subprocess.run(["nmap", "-sV", "-T4", "--unprivileged", "-oN", "nmap_scan.txt", target], capture_output=True, text=True)
    return result.stdout


def run_vuln_scan(target):
    """Runs Nmap using the 'vuln' script category to find known vulnerabilities."""
    print("[+] Running vulnerability scan using Nmap vuln scripts...")
    vuln_output_file = os.path.expanduser("~/result_PenAut/vuln_scan.txt")
    result = subprocess.run(["nmap", "-sV", "--script=vuln", "--unprivileged", "-T4", "-oN", vuln_output_file, target],
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


def main_port():
    target = input("Entrez l'adresse IP ou le nom de domaine de la cible : ").strip()

    scan_results = run_nmap_scan(target)
    vuln_results = run_vuln_scan(target)

    open_ports = [line.split("/")[0] for line in scan_results.split("\n") if "/tcp" in line and "open" in line]
    banners = {port: grab_banner(target, port) for port in open_ports}

    report = {
        "target": target,
        "nmap_results": scan_results,
        "vulnerability_scan": vuln_results,
        "banners": banners,
    }

    result_dir = os.path.expanduser("~/result_PenAut")
    os.makedirs(result_dir, exist_ok=True)
    report_path = os.path.join(result_dir, "recon_report.json")

    with open(report_path, "w") as f:
        json.dump(report, f, indent=4)

    print(f"[+] Recon terminée. Résultats enregistrés dans {report_path}")
