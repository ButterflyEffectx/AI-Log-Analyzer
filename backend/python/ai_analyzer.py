# ai_analyzer.py (ปรับให้ exact count + load .env)
import os
from openai import OpenAI
import argparse
from collections import defaultdict
import re
from dotenv import load_dotenv

# --------------------
# Load .env
# --------------------
load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY ไม่ถูกตั้งค่าใน .env")

# --------------------
# สร้าง client
# --------------------
client = OpenAI(api_key=OPENAI_API_KEY)

# --------------------
# ฟังก์ชันช่วยอ่าน log
# --------------------
def read_log(path, max_lines=500):
    with open(path, "r") as f:
        lines = f.readlines()[-max_lines:]
    return lines

# --------------------
# นับ failed login ต่อ IP
# --------------------
def count_failed_attempts(lines):
    counts = defaultdict(int)
    pattern = re.compile(r"Failed password.*from (\d+\.\d+\.\d+\.\d+)")
    for line in lines:
        match = pattern.search(line)
        if match:
            ip = match.group(1)
            counts[ip] += 1
    return counts

# --------------------
# ส่ง log + exact counts ให้ AI
# --------------------
def summarize_with_ai(log_text, ip_counts, api_key=None):
    if api_key:
        client.api_key = api_key  

    summary_counts = "\n".join([f"{ip}: {count}" for ip, count in ip_counts.items()])
    prompt = (
        "You are a cybersecurity analyst. Analyze the following SSH auth log and "
        "produce a short human-readable summary with (1) what suspicious patterns were found, "
        "(2) IPs involved, (3) exact counts per IP, and (4) recommended quick actions.\n\n"
        f"LOG:\n{log_text}\n\nExact Counts:\n{summary_counts}\n\nSummary:"
    )

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
        temperature=0.0,
    )
    return resp.choices[0].message.content


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("logfile")
    p.add_argument("--lines", type=int, default=500)
    args = p.parse_args()

    lines = read_log(args.logfile, args.lines)
    ip_counts = count_failed_attempts(lines)

    print("Sending log + exact counts to AI for summary... (using OPENAI_API_KEY from .env)")
    summary = summarize_with_ai("".join(lines), ip_counts)
    print("\n=== AI SUMMARY ===\n")
    print(summary)

