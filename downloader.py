import os
import csv
import time
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Base configuration
base_folder = "ICLR_2025_Papers"
csv_path = os.path.join(base_folder, "paper_index.csv")

categories = {
    "Oral": "https://openreview.net/group?id=ICLR.cc/2025/Conference#tab-accept-oral",
    "Spotlight": "https://openreview.net/group?id=ICLR.cc/2025/Conference#tab-accept-spotlight",
    "Poster": "https://openreview.net/group?id=ICLR.cc/2025/Conference#tab-accept-poster"
}

os.makedirs(base_folder, exist_ok=True)


def sanitize_filename(name):
    return "".join(c if c.isalnum() or c in "-_()[] " else "_" for c in name)[:100]


def load_full_page(driver):
    while True:
        try:
            load_more = driver.find_element(By.CLASS_NAME, 'load-more-button')
            driver.execute_script("arguments[0].click();", load_more)
            time.sleep(2)
        except Exception:
            break


def download_category(category, url):
    print(f"\nDownloading {category} papers...")
    sub_folder = os.path.join(base_folder, category)
    os.makedirs(sub_folder, exist_ok=True)

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    driver.get(url)
    time.sleep(3)
    load_full_page(driver)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    links = soup.select("a.pdf-link")
    print(f"Found {len(links)} PDF links.")

    entries = []
    failures = 0

    for link in tqdm(links, desc=f"Downloading {category}"):
        href = link.get("href")
        pdf_url = f"https://openreview.net{href}"
        title_tag = link.find_parent("li").find("h4")
        title_text = title_tag.text.strip() if title_tag else href.split("=")[-1]
        safe_name = sanitize_filename(title_text)
        file_path = os.path.join(sub_folder, f"{safe_name}.pdf")

        try:
            res = requests.get(pdf_url)
            res.raise_for_status()
            with open(file_path, "wb") as f:
                f.write(res.content)
            entries.append([category, title_text, file_path])
        except Exception as e:
            failures += 1
            print(f"Failed to download {pdf_url}: {e}")

    print(f"{category} download done. Failures: {failures}")
    return entries


if __name__ == "__main__":
    all_entries = []
    for cat, url in categories.items():
        entries = download_category(cat, url)
        all_entries.extend(entries)

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Category", "Title", "File Path"])
        writer.writerows(all_entries)

    print(f"\nAll done! Paper index saved to {csv_path}.")
