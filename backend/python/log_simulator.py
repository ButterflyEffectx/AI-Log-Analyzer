# log_simulator.py
import time, random, datetime, argparse, os

MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

def now_ts():
    return datetime.datetime.now().strftime("%b %d %H:%M:%S")

def generate_line(victim_hostname, pid=None, ip=None, user="admin", success=False):
    pid = pid or random.randint(1000,9999)
    port = random.randint(20000,60000)
    ts = now_ts()
    if success:
        return f"{ts} {victim_hostname} sshd[{pid}]: Accepted password for {user} from {ip} port {port} ssh2\n"
    else:
        return f"{ts} {victim_hostname} sshd[{pid}]: Failed password for invalid user {user} from {ip} port {port} ssh2\n"

def main():
    parser = argparse.ArgumentParser(description="Simulate SSH brute-force style logs")
    parser.add_argument("--out", default="bruteforce.log", help="Output log file path")
    parser.add_argument("--count", type=int, default=200, help="Total log lines to generate")
    parser.add_argument("--delay", type=float, default=0.3, help="Seconds between lines")
    parser.add_argument("--ips", default="192.168.56.20,192.168.56.21", help="Comma-separated attacker IPs")
    parser.add_argument("--hostname", default="victim", help="Hostname to write in each log line")
    args = parser.parse_args()

    ips = [ip.strip() for ip in args.ips.split(",")]
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)

    with open(args.out, "a") as f:
        for i in range(args.count):
            ip = random.choice(ips)
            # Insert some successes occasionally
            success = (random.random() < 0.02)
            line = generate_line(args.hostname, ip=ip, success=success)
            f.write(line)
            f.flush()
            time.sleep(args.delay)

if __name__ == "__main__":
    main()
