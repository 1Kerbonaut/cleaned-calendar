import requests
import re

# Your university calendar feed URL
SOURCE_URL = "https://elearning.uni-bremen.de/dispatch.php/ical/index/HWGXt9vk"

def clean_summary(summary):
    # Try to extract course name from known format
    match = re.search(r'(?:CM|EM)-([A-Z]+)\s+(.*)', summary)
    return match.group(2) if match else summary

ics = requests.get(SOURCE_URL).text
cleaned = []

for line in ics.splitlines():
    if line.startswith("SUMMARY:"):
        original = line[8:].strip()
        cleaned_line = clean_summary(original)
        cleaned.append("SUMMARY:" + cleaned_line)
    else:
        cleaned.append(line)

with open("docs/cleaned_calendar.ics", "w", encoding="utf-8") as f:
    f.write("\n".join(cleaned))
