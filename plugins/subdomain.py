def enumerate_subdomains(self):
        print(f"[*] Enumerating subdomains for {self.domain}...")
        subprocess.run(["subfinder", "-d", self.domain, "-o", f"recon_results/{self.domain}/subdomains/sub1.txt"])
        subprocess.run(["assetfinder", "--subs-only", self.domain, "-o", f"recon_results/{self.domain}/subdomains/sub2.txt"])
        subprocess.run(["amass", "enum", "-norecursive", "-noalts", "-d", self.domain, "-o", f"recon_results/{self.domain}/subdomains/sub3.txt"])
        subprocess.run(["chaos", "-d", self.domain, "-o", f"recon_results/{self.domain}/subdomains/sub4.txt"])
        subprocess.run(["alterx", "-d", self.domain, "-o", f"recon_results/{self.domain}/subdomains/sub5.txt"])
        subprocess.run(["findomain", "--external-subdomains", "--output", "--target", self.domain, "--unique-output", f"recon_results/{self.domain}/subdomains/sub6.txt"])

        with open(f"recon_results/{self.domain}/subdomains/all_subdomains.txt", "w") as outfile:
            for subfile in ["sub1.txt", "sub2.txt", "sub3.txt", "sub4.txt", "sub5.txt", "sub6.txt"]:
                with open(f"recon_results/{self.domain}/subdomains/{subfile}") as infile:
                    outfile.write(infile.read())

    def check_takeover(self):
        print(f"[*] Checking for subdomain takeovers for {self.domain}...")
        subprocess.run(["subjack", "-w", f"recon_results/{self.domain}/subdomains/all_subdomains.txt", "-t", "100", "-timeout", "30", "-ssl", "-c", "/usr/share/subjack/fingerprints.json", "-v", "-o", f"recon_results/{self.domain}/result/takeover.txt"])
