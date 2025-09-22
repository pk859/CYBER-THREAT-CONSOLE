import sys
import datetime

def block_ip_address(ip_address):
    """
    Simulates blocking an IP by writing it to a blocklist file.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{ip_address} blocked on {timestamp}\n"

    with open("blocked_ips.txt", "a") as f:
        f.write(log_entry)

    print(f"--- SOAR ACTION TRIGGERED ---")
    print(f"🔥 IP address {ip_address} has been added to the firewall blocklist. 🔥")
    print(f"--------------------------")

if __name__ == "__main__":
    # The IP address is passed as a command-line argument
    if len(sys.argv) > 1:
        ip_to_block = sys.argv[1]
        block_ip_address(ip_to_block)