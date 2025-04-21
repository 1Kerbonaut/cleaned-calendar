import requests
import re
import os

SOURCE_URL = "https://elearning.uni-bremen.de/dispatch.php/ical/index/HWGXt9vk"
OUTPUT_PATH = "docs/cleaned_calendar.ics"

ics = requests.get(SOURCE_URL).text
cleaned = []

# Flexible pattern to extract the course name after the codes
pattern = re.compile(r"^[^:]+:\s+(?:[A-Z0-9]+-)+[A-Z0-9]+\s+(.*)$")

Changed_Entry = 0

for line in ics.splitlines():
    if line.startswith("SUMMARY:"):
        original = line[8:].strip()
        match = pattern.match(original)
        if match:
            title = match.group(1)  # Access the first capturing group for course name            
            cleaned.append("SUMMARY:" + title)
        else:
            cleaned.append("SUMMARY:" + original)
    else:
        cleaned.append(line)
# Ensure output directory exists
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# Compare with previous version from OUTPUT_PATH, ignoring lines starting with "DTSTAMP"
with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
    previous = [line for line in f.read().splitlines() if not line.startswith("DTSTAMP")]
    cleaned_filtered = [line for line in cleaned if not line.startswith("DTSTAMP")]
    Changed_Entry = len([line for line in cleaned_filtered if line not in previous])

# Output number of changed entries
print("Changed Entries: " + str(Changed_Entry))

if Changed_Entry > 0:
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(cleaned))

