# Durian Player Summary

A local web application to visualize and aggregate player statistics from the Durian game across different versions.

## Features

*   **Version Control:** View statistics for specific game versions (v0.6.20, v0.6.21, v0.6.22, etc.).
*   **Aggregate Data:** "All Versions (Combined)" view to see lifetime player statistics.
*   **Detailed Metrics:**
    *   Unique Players count.
    *   Total Runs.
    *   Win Rate calculation.
    *   Survival/Death counts.
    *   Breakdown by Difficulty (Normal, Hard, Hell, Duriano).
*   **Dynamic Updates:** Easily add new versions via a Python script without modifying the HTML code.
*   **Responsive Design:** Built with Bootstrap for a clean mobile-friendly interface.

## Quick Start

### Prerequisites
*   Python 3.x (for running the fetch script and local server).
*   A web browser.

### Installation

1.  Clone this repository:
    ```bash
    git clone https://github.com/YOUR_USERNAME/Durian_Player_Summary.git
    cd Durian_Player_Summary
    ```

### How to Use

1.  **Fetch Latest Data:**
    Run the Python script to download the latest stats from the server and generate the metadata.
    ```bash
    python fetch_data.py
    ```

2.  **Start the Viewer:**
    Double-click `start_server.bat` (Windows) or run:
    ```bash
    python -m http.server 8000
    ```

3.  **View Stats:**
    Open your browser to `http://localhost:8000`.

## Adding New Versions

To track a new game version:

1.  Open `fetch_data.py` in a text editor.
2.  Add the new version to the `SOURCES` dictionary:
    ```python
    SOURCES = {
        "summary_counts_0.6.23.json": "https://us-central1-duriano.cloudfunctions.net/getSummaryCountsByNameFunction?version=0.6.23",
        # ... existing versions
    }
    ```
3.  Run `python fetch_data.py`.
4.  Refresh the web page. The new version will automatically appear in the dropdown.

## Project Structure

*   `index.html`: The main dashboard (frontend).
*   `fetch_data.py`: Script to download data and generate `metadata.json`.
*   `metadata.json`: Generated file listing available versions for the frontend.
*   `summary_counts_*.json`: Data files for each version.
*   `start_server.bat`: Helper script to launch the local web server.
