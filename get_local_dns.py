import subprocess
import re
import json

hostname_pattern = re.compile(r"Ping (.*) \[")
ip_pattern = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+")
filename = "dns.json"


def get_ips():
    output = subprocess.check_output(f"arp -a", shell=True).decode("cp1252")
    return re.findall(ip_pattern, output)


def get_dns():
    print("Getting dns...")
    dns = {}
    for ip in get_ips():
        try:
            output = subprocess.check_output(f"ping -a {ip}", shell=True).decode("cp1252")
            dns[ip] = re.search(hostname_pattern, output).group(1)
        except:
            pass
    return dns


def dump_dns(dns):
    with open(filename, "w") as f:
        json.dump(dns, f, indent=4)
    print(f"Dns dumped in '{filename}'")


if __name__ == '__main__':
    dns = get_dns()
    if dns:
        dump_dns(dns)
    else:
        print("Some error has occurred")
    input("\nClick any button to exit...")
