from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

def scrape_indeed_pk():
    driver = None
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        options.add_argument(f"--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(80,120)}.0.0.0 Safari/537.36")
        
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        
        # Force PK domain
        driver.get("https://pk.indeed.com")
    
        #driver.get("https://m.pk.indeed.com/jobs?q=python&l=karachi")
        time.sleep(2)
        

        # Use PK-specific selectors
        search_bar = driver.find_element(By.ID, "text-input-what")  # Different ID in PK
        location_bar = driver.find_element(By.ID, "text-input-where")
        
        # Human-like typing
        for char in "Python Developer":
            search_bar.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))
        
        location_bar.clear()
        for char in "Karachi":  # Example PK city
            location_bar.send_keys(char)
            time.sleep(random.uniform(0.1, 0.2))
        
        # PK search button selector
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(3)
        input("Solve CAPTCHA manually in the browser, then press Enter...")
        
        # PK job card selector
        jobs = []
        for card in driver.find_elements(By.CSS_SELECTOR, "div.job_seen_beacon"):
            title = card.find_element(By.CSS_SELECTOR, "h2.jobTitle").text
            company = card.find_element(By.CSS_SELECTOR, "span.companyName").text
            jobs.append({"title": title, "company": company})
        
        return jobs
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
            # Close the browser
        time.sleep(random.uniform(1, 2))
            # Add this before the finally/driver.quit() to debug:
        print("Final URL:", driver.current_url)  # Check if you're on a CAPTCHA page
        driver.save_screenshot("debug.png")  # Save a screenshot to see what happened
        time.sleep(10)  # Pause to manually observe the browser before it closes
        driver.quit()

if __name__ == "__main__":
    jobs = scrape_indeed_pk()
    print(jobs[:3])  # Print first 3 jobs