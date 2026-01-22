import urllib.request
import json
import ssl

# Configuration: Map filenames to their URLs
SOURCES = {
    "summary_counts_0.6.24.json": "https://us-central1-duriano.cloudfunctions.net/getSummaryCountsByNameFunction?version=0.6.24",
    "summary_counts_0.6.23.json": "https://us-central1-duriano.cloudfunctions.net/getSummaryCountsByNameFunction?version=0.6.23",
    "summary_counts_0.6.22.json": "https://us-central1-duriano.cloudfunctions.net/getSummaryCountsByNameFunction?version=0.6.22",
    "summary_counts_0.6.21.json": "https://us-central1-duriano.cloudfunctions.net/getSummaryCountsByNameFunction?version=0.6.21",
    "summary_counts_0.6.20.json": "https://us-central1-duriano.cloudfunctions.net/getSummaryCountsByNameFunction?version=0.6.20"
}

def fetch_data():
    # Create an SSL context that ignores certificate errors (sometimes needed for simple scripts)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    print("Starting download of player summary data...")
    print("-" * 50)

    for filename, url in SOURCES.items():
        try:
            print(f"Fetching {filename}...")
            with urllib.request.urlopen(url, context=ctx) as response:
                if response.status == 200:
                    data = response.read()
                    # Validate it's JSON before writing
                    json.loads(data)
                    
                    with open(filename, "wb") as f:
                        f.write(data)
                    print(f" [OK] Saved to {filename}")
                else:
                    print(f" [ERR] Failed to fetch {filename}. Status: {response.status}")
        except Exception as e:
            print(f" [ERR] Error fetching {filename}: {e}")

    print("-" * 50)
    
    # Generate metadata.json for the frontend
    metadata = []
    # Sort keys to ensure consistent order (optional, but good for UI)
    # We want newest version first, so we sort reverse
    sorted_versions = sorted(SOURCES.keys(), reverse=True)
    
    for filename in sorted_versions:
        # Extract version number for display (e.g., "summary_counts_0.6.22.json" -> "v0.6.22")
        # Simple string manipulation: remove "summary_counts_" and ".json"
        display_ver = filename.replace("summary_counts_", "v").replace(".json", "")
        metadata.append({
            "file": filename,
            "label": display_ver
        })

    with open("metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    print(" [OK] Generated metadata.json")

    print("Update complete! Refresh your web browser to see the latest stats.")

if __name__ == "__main__":
    fetch_data()