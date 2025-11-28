import requests
import re
import os

SOURCE_URL = "https://elearning.uni-bremen.de/dispatch.php/ical/index/HWGXt9vk"
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "docs", "cleaned_calendar.ics")
MAX_RETRIES = 3
def get_ics_with_retry(SOURCE_URL, MAX_RETRIES):
    TIMEOUT = False
    RETRY_COUNT = 0
    for i in range(MAX_RETRIES):
        try:
            ics = requests.get(SOURCE_URL, timeout=10).text
            break
        except requests.Timeout:
            RETRY_COUNT += 1
            print(f"Timeout, retrying. Attempt {i+1} of {MAX_RETRIES}")
    else:
        TIMEOUT = True
        print(f"Timeout, max retries reached. Giving up.")
        return None
    print("Successful ics request!")
    return ics

ics = get_ics_with_retry(SOURCE_URL, MAX_RETRIES)

if ics is not None:
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
        elif line.startswith("LOCATION:"):        
            # if line contains SFG, IW3, or FZB, add adress
            # adresses:
            # SFG 2030 - Enrique-Schmidt-Straße 7, 28359 Bremen
            # IW3 2020 - Ingenieurwissenschaften 3, Hochschulring 18, 28359 Bremen
            # FZB 0240 - Badgasteiner Straße 3, 28359 Bremen
            if "SFG" in line:
                cleaned.append(line + r"\, Enrique-Schmidt-Straße 7\, 28359 Bremen")
            elif "IW3" in line:
                cleaned.append(line + r"\, Am Biologischen Garten 2\, 28359 Bremen")
            elif "FZB" in line:
                cleaned.append(line + r"\, Badgasteiner Straße 3\, 28359 Bremen")
            else:
                cleaned.append(line)
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