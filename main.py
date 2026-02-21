import undetected_chromedriver as uc
uc.Chrome.__del__ = lambda self: None
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import requests
import os

def videoDownload(tiktok_url, index, folder_name):
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options)

    try:
        driver.get("https://ssstik.io/en-1")

        input_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "main_page_text"))
        )
        input_box.clear()
        input_box.send_keys(tiktok_url)

        button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        button.click()

        downloadLink = None
        # Try twice: initial click + retry if popup appears
        for attempt in range(2):
            try:
                no_wm_button = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a.download_link.without_watermark"))
                )
                downloadLink = no_wm_button.get_attribute("href")
                break  # success
            except Exception:
                print("Popup detected, waiting 10s and retrying...")
                time.sleep(10)
                button.click()

        if not downloadLink:
            print(f"Failed to get download link for {tiktok_url}")
            return

    except Exception as e:
        print(f"Error while processing {tiktok_url}: {e}")
        return

    finally:
        driver.quit()

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/141.0.0.0 Safari/537.36 OPR/125.0.0.0"
        ),
        "Accept": "video/mp4,application/octet-stream,*/*"
    }

    resp = requests.get(downloadLink, headers=headers, stream=True, allow_redirects=True)
    resp.raise_for_status()

    ctype = resp.headers.get("Content-Type", "")
    if not any(x in ctype for x in ["video", "octet-stream"]):
        print("Error: Not a video file, got", ctype)
        print(resp.text[:500])  # debug HTML
        return

    os.makedirs(f"videos/{folder_name}", exist_ok=True)
    filename = f"videos/{folder_name}/{index}.mp4"
    with open(filename, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    print(f"Video {index} saved successfully at {filename}")

def main():
    username = input("Enter username:")

    PROFILE_URL = "https://www.tiktok.com/" + username

    options = uc.ChromeOptions()
    options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe" # location to your chrome

    driver = uc.Chrome(version_main=144, options=options)
    driver.get(PROFILE_URL)

    time.sleep(5)

    last_height = driver.execute_script("return document.body.scrollHeight")

    extra_scrolls = 2
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            if extra_scrolls > 0:
                extra_scrolls -= 1
            else:
                break
        last_height = new_height


    soup = BeautifulSoup(driver.page_source, "html.parser")

    videos = soup.find_all("div", {"data-e2e": "user-post-item"})
    driver.close()
    check = input(f"Found {len(videos)} videos, do you want to start download ( type y to continue )?")

    if check == "y":
        for index, video in enumerate(videos):
            href = video.a["href"]

            if "/photo/" in href:
                continue

            videoDownload(href, index, username)
            time.sleep(5)
    else:
        sys.exit()

main()