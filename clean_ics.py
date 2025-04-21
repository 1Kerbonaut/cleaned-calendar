import requests
import re
import os

SOURCE_URL = "https://elearning.uni-bremen.de/dispatch.php/ical/index/HWGXt9vk"
OUTPUT_PATH = "docs/cleaned_calendar.ics"

ics = requests.get(SOURCE_URL).text
cleaned = []

# Match example: "Seminar: 04-M30-EM-ITPY Introduction to Python"
pattern = re.compile(r"^[^:]+:\s+(?:[A-Z0-9]+-)+[A-Z0-9]+\s+(.*)$")

for line in ics.splitlines():
    if line.startswith("SUMMARY:"):
        original = line[8:].strip()
        match = pattern.match(original)
        if match:
            title = match.group(2)
            cleaned.append("SUMMARY:" + title)
        else:
            cleaned.append("SUMMARY:" + original)
    else:
        cleaned.append(line)

# Ensure output directory exists
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(cleaned))
