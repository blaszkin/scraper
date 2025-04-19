from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import os

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

def search(category):
    list_of_links = []
    try:
        link_to_site = "https://cybernews.com/" + category
        driver.get(link_to_site)

        time.sleep(random.uniform(10, 15))

        try:
            cookie_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept')]"))
            )
            cookie_button.click()
            print("Clicked 'Accept Cookies'")
        except:
            print("No cookies window")

        previous_count = 0
        max_scrolls = 10
        scroll_pause_time = random.uniform(2, 4)

        for _ in range(max_scrolls):
            driver.execute_script("window.scrollBy(0, 800);")
            time.sleep(scroll_pause_time)

            articles = driver.find_elements(By.XPATH, "//h2/ancestor::a | //h3/ancestor::a | //h4/ancestor::a")

            if len(articles) == previous_count:
                break

            previous_count = len(articles)

        articles = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, "//h2/ancestor::a | //h3/ancestor::a | //h4/ancestor::a"))
        )

        print("\n Article titles from " + category)
        for article in articles:
            title = article.text.strip()
            link = article.get_attribute("href")
            if title and link:
                list_of_links.append(f"- {title} → {link}" + "\n")

        time.sleep(5)

    finally:
        return list_of_links

directory_name = "categories"
try:
    os.mkdir(directory_name)
    print(f"Directory created successfully.")
except FileExistsError:
    print(f"Directory already exists.")
except PermissionError:
    print(f"Permission Error")
except Exception as e:
    print(f"An error occurred: {e}")

os.chdir("categories")

topics = ["security", "privacy", "crypto", "tech", "gaming", "gadgets", "entertainment", "science", "cybercrime"]
for i in topics:
    x = search(i)
    file = open(i, 'w', encoding="utf-8")
    file.writelines(x)
    file.close()
