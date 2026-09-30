import os
import shutil
import subprocess
from pathlib import Path


class PentestAgent:
    def __init__(self, domain):
        self.domain = domain.strip()
        self.base_dir = Path("outputs") / self.domain

        self.subdomains_dir = self.base_dir / "subdomains"
        self.urls_dir = self.base_dir / "extracted_urls"
        self.gf_dir = self.base_dir / "gf_parameters"
        self.ports_dir = self.base_dir / "port_scans"
        self.directory_dir = self.base_dir / "directory_bruteforce"
        self.results_dir = self.base_dir / "result"
        self.xss_dir = self.base_dir / "xss"
        self.cve_dir = self.base_dir / "cve"

        self.setup_folders()

    def setup_folders(self):
        print("[*] Setting up directories...")

        directories = [
            self.subdomains_dir,
            self.urls_dir,
            self.gf_dir,
            self.ports_dir,
            self.directory_dir,
            self.results_dir,
            self.xss_dir,
            self.cve_dir,
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def tool_exists(self, tool):
        return shutil.which(tool) is not None

    def run_command(self, command, output_file=None):
        tool = command[0]

        if not self.tool_exists(tool):
            print(f"[!] {tool} is not installed. Skipping.")
            return False

        print(f"[*] Running: {' '.join(command)}")

        try:
            if output_file:
                with open(output_file, "w") as output:
                    result = subprocess.run(
                        command,
                        stdout=output,
                        stderr=subprocess.STDOUT,
                        text=True
                    )
            else:
                result = subprocess.run(command)

            if result.returncode != 0:
                print(f"[!] {tool} returned exit code {result.returncode}")
                return False

            return True

        except Exception as error:
            print(f"[!] Error running {tool}: {error}")
            return False

    def enumerate_subdomains(self):
        print(f"\n[*] Enumerating subdomains for {self.domain}...")

        tools = [
            (
                "subfinder",
                ["subfinder", "-d", self.domain, "-silent"],
                self.subdomains_dir / "subfinder.txt",
            ),
            (
                "assetfinder",
                ["assetfinder", "--subs-only", self.domain],
                self.subdomains_dir / "assetfinder.txt",
            ),
            (
                "amass",
                ["amass", "enum", "-passive", "-d", self.domain],
                self.subdomains_dir / "amass.txt",
            ),
            (
                "findomain",
                ["findomain", "-t", self.domain, "--quiet"],
                self.subdomains_dir / "findomain.txt",
            ),
        ]

        for tool, command, output in tools:
            self.run_command(command, output)

        all_subdomains = self.subdomains_dir / "all_subdomains.txt"

        discovered = set()

        for file in self.subdomains_dir.glob("*.txt"):
            if file.name == "all_subdomains.txt":
                continue

            try:
                with open(file, "r", errors="ignore") as source:
                    for line in source:
                        value = line.strip()
                        if value:
                            discovered.add(value)
            except OSError:
                pass

        with open(all_subdomains, "w") as output:
            for subdomain in sorted(discovered):
                output.write(subdomain + "\n")

        print(
            f"[*] Subdomain enumeration completed. "
            f"Found {len(discovered)} unique entries."
        )

    def discover_live_hosts(self):
        print("\n[*] Discovering live hosts...")

        input_file = self.subdomains_dir / "all_subdomains.txt"
        output_file = self.urls_dir / "live_hosts.txt"

        if not input_file.exists():
            print("[!] Subdomain list not found.")
            return

        if self.tool_exists("httpx"):
            self.run_command(
                [
                    "httpx",
                    "-l",
                    str(input_file),
                    "-silent",
                ],
                output_file,
            )
        else:
            print("[!] httpx is not installed. Skipping live host discovery.")

    def collect_urls(self):
        print("\n[*] Collecting URLs...")

        live_hosts = self.urls_dir / "live_hosts.txt"

        if not live_hosts.exists():
            print("[!] Live host list not found. Skipping URL collection.")
            return

        collected = self.urls_dir / "collected_urls.txt"

        if self.tool_exists("gau"):
            self.run_command(
                [
                    "gau",
                    "--subs",
                    self.domain,
                ],
                collected,
            )

        elif self.tool_exists("waybackurls"):
            self.run_command(
                [
                    "waybackurls",
                    self.domain,
                ],
                collected,
            )

        else:
            print("[!] Neither gau nor waybackurls is installed.")

    def analyze_parameters(self):
        print("\n[*] Running GF parameter analysis...")

        urls_file = self.urls_dir / "collected_urls.txt"

        if not urls_file.exists():
            print("[!] URL collection file not found.")
            return

        patterns = [
            "xss",
            "sqli",
            "ssrf",
            "lfi",
            "rce",
            "redirect",
            "idor",
        ]

        if not self.tool_exists("gf"):
            print("[!] gf is not installed. Skipping GF analysis.")
            return

        for pattern in patterns:
            pattern_dir = self.gf_dir / pattern
            pattern_dir.mkdir(parents=True, exist_ok=True)

            output = pattern_dir / f"{pattern}.txt"

            self.run_command(
                [
                    "gf",
                    pattern,
                ],
                output_file=output,
            )

    def perform_port_scan(self):
        print("\n[*] Performing port scan...")

        output = self.ports_dir / "ports.txt"

        self.run_command(
            [
                "nmap",
                self.domain,
                "-p",
                "1-1000",
                "-sV",
                "-oN",
                str(output),
            ]
        )

    def directory_bruteforce(self):
        print("\n[*] Performing directory enumeration...")

        output = self.directory_dir / "dirsearch.txt"

        if not self.tool_exists("dirsearch"):
            print("[!] dirsearch is not installed. Skipping.")
            return

        self.run_command(
            [
                "dirsearch",
                "-u",
                f"https://{self.domain}",
                "-o",
                str(output),
            ]
        )

    def vulnerability_assessment(self):
        print("\n[*] Running vulnerability assessment...")

        urls_file = self.urls_dir / "collected_urls.txt"
        output = self.results_dir / "nuclei_results.txt"

        if not urls_file.exists():
            print("[!] No URL file available for vulnerability assessment.")
            return

        if not self.tool_exists("nuclei"):
            print("[!] nuclei is not installed. Skipping.")
            return

        self.run_command(
            [
                "nuclei",
                "-l",
                str(urls_file),
                "-o",
                str(output),
            ]
        )

    def xss_assessment(self):
        print("\n[*] Running XSS assessment...")

        urls_file = self.urls_dir / "collected_urls.txt"

        if not urls_file.exists():
            print("[!] URL collection file not found.")
            return

        output = self.xss_dir / "dalfox_results.txt"

        if self.tool_exists("dalfox"):
            self.run_command(
                [
                    "dalfox",
                    "file",
                    str(urls_file),
                ],
                output,
            )
        else:
            print("[!] dalfox is not installed. Skipping XSS assessment.")

    def generate_summary(self):
        print("\n[*] Generating scan summary...")

        summary = self.results_dir / "scan_summary.txt"

        with open(summary, "w") as report:
            report.write("APTF - Automated Penetration Testing Framework\n")
            report.write("=" * 55 + "\n\n")
            report.write(f"Target: {self.domain}\n\n")

            report.write("Generated Directories:\n")
            report.write("-" * 25 + "\n")

            for directory in [
                self.subdomains_dir,
                self.urls_dir,
                self.gf_dir,
                self.ports_dir,
                self.directory_dir,
                self.results_dir,
                self.xss_dir,
                self.cve_dir,
            ]:
                report.write(f"- {directory}\n")

        print(f"[*] Summary generated: {summary}")

    def run(self):
        print("\n" + "=" * 60)
        print("APTF - Automated Penetration Testing Framework")
        print("=" * 60)
        print(f"Target: {self.domain}")
        print("=" * 60)

        self.enumerate_subdomains()
        self.discover_live_hosts()
        self.collect_urls()
        self.analyze_parameters()
        self.perform_port_scan()
        self.directory_bruteforce()
        self.vulnerability_assessment()
        self.xss_assessment()
        self.generate_summary()

        print("\n" + "=" * 60)
        print("[+] APTF scan workflow completed.")
        print(f"[+] Results saved in: {self.base_dir}")
        print("=" * 60)


if __name__ == "__main__":
    domain = input("Enter the authorized target domain: ").strip()

    if not domain:
        print("[!] No domain provided.")
        raise SystemExit(1)

    agent = PentestAgent(domain)
    agent.run()