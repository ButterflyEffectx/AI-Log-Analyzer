# heuristic_detector.py
import re
from collections import defaultdict
import argparse

PAT = re.compile(r'Failed password.*from (?P<ip>\d+\.\d+\.\d+\.\d+)')

# ----- เวอร์ชันอ่านจากไฟล์ (เดิม) -----
def analyze_file(path, threshold=10):
    counts = defaultdict(int)
    with open(path, "r") as f:
        for line in f:
            m = PAT.search(line)
            if m:
                ip = m.group("ip")
                counts[ip] += 1
    alerts = {ip:cnt for ip,cnt in counts.items() if cnt >= threshold}
    return counts, alerts

# ----- เวอร์ชันใหม่: รองรับ DataFrame -----
def analyze_dataframe(df_logs, threshold=10):
    """
    df_logs ต้องมี column 'ip_address' และ 'status'
    """
    counts = defaultdict(int)
    for _, row in df_logs.iterrows():
        status = str(row['status']).strip().lower()  # trim & lower
        if status == 'failed' or status == 'fail':   # ครอบคลุมทั้ง 2 กรณี
            counts[row['ip_address']] += 1

    alerts = {ip: cnt for ip, cnt in counts.items() if cnt >= threshold}
    return counts, alerts


# ----- สำหรับ command-line (เดิม) -----
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("logfile")
    p.add_argument("--threshold", type=int, default=10)
    args = p.parse_args()

    counts, alerts = analyze_file(args.logfile, args.threshold)
    print("Counts per IP:")
    for ip, c in counts.items():
        print(f"  {ip}: {c}")
    if alerts:
        print("\nALERT: possible brute-force detected for:")
        for ip,c in alerts.items():
            print(f"  {ip} ({c} attempts)")
    else:
        print("\nNo brute-force detected (threshold {})".format(args.threshold))
