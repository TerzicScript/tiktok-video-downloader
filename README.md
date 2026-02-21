# TikTok Profile Scraper & Downloader (No Watermark)

A robust Python automation tool designed to crawl a TikTok user's profile, extract all video links, and download them in high definition without watermarks.

## ✨ Features
* **Anti-Bot Bypass:** Utilizes `undetected-chromedriver` to avoid being flagged as a bot.
* **Infinite Scroll:** Automatically calculates page height and scrolls until every video is indexed.
* **Smart Selection:** Uses `data-e2e` attributes to find video containers, making it resistant to TikTok's dynamic class name updates.
* **Automatic Downloading:** Interfaces with `ssstik.io` to fetch the "Without Watermark" version of each video.
* **Folder Organization:** Automatically creates a directory named after the user to store the `.mp4` files.

---

## 🛠️ Prerequisites

Before running the script, ensure you have the following installed:

1.  **Python 3.8+**
2.  **Google Chrome** (Ensure your Chrome version matches the `version_main` in the script).

---

## 📦 Requirements

To install all necessary libraries, run the following command:
```
pip install undetected-chromedriver beautifulsoup4 requests selenium
```
---

## 🚀 Setup & Usage

### 1. Configure Chrome Path
Open the script and update the `binary_location` to match your computer's Chrome installation:
```
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
```

### 2. Run the Script
Execute the script from your terminal:
```
python tiktok_downloader.py
```

### 3. Workflow
1.  **Input Username:** Type the TikTok handle (e.g., `officialsixflags`).
2.  **Scrolling:** The script will open a browser, head to the profile, and scroll to the bottom.
3.  **Verification:** It will report how many videos were found and ask for a `y` to proceed.
4.  **Download:** It will open a new instance to process each link through the downloader service.

---

## ⚙️ Technical Logic


The script operates in two distinct phases to maximize efficiency:

1.  **Phase A (Extraction):** Uses Selenium to simulate a real user scrolling. Once the `scrollHeight` stops changing, `BeautifulSoup` parses the static HTML to grab all `<a>` tags within the post items.
2.  **Phase B (Downloading):** A separate function handles the interaction with the download provider. It includes a **Retry Logic** that waits 10 seconds if a popup or overlay blocks the download button.

---

## ⚠️ Disclaimer
This project is for **educational purposes only**. Scraping TikTok may violate their Terms of Service. Please ensure you have permission to download content and respect the copyright of creators.
