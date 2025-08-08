from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import warnings
import os

# Suppress TensorFlow and Deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # 0=all, 1=info, 2=warning, 3=error
os.environ['ABSL_LOG_LEVEL'] = 'ERROR'

def get_search_url(driver, job_title, city):
    """
    Performs search on Rozee.pk and returns the final search URL.
    Uses Selenium to interact with the search form and city dropdown.
    """
    actions = ActionChains(driver)
    try:
        print("Loading Rozee.pk homepage...")
        driver.get("https://www.rozee.pk")
        # Wait for search field to appear
        search_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input#search.form-control.input-lg"))
        )
        print(f"Searching for: {job_title}")
        search_field.clear()
        search_field.send_keys(job_title)
        time.sleep(1)  # Small buffer for UI update

        # Locate and click city dropdown
        print("Locating City dropdown...")
        city_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-id='homeSearchCity']"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", city_dropdown)
        driver.execute_script("arguments[0].click();", city_dropdown)
        time.sleep(1)

        print(f"Selecting city: {city}")
        try:
            # Select city from dropdown
            city_option = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, f"//span[contains(@class, 'text') and contains(text(), '{city}')]"))
            )
            city_option.click()
        except Exception:
            print(f"City '{city}' not found in dropdown. Using default (Karachi)")
            # Close dropdown by clicking elsewhere
            actions.move_by_offset(10, 10).click().perform()

        # Submit the search form using JavaScript
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        driver.execute_script("arguments[0].click();", submit_btn)

        # Wait for job results to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.job"))
        )
        time.sleep(2)  # Buffer for page load

        search_url = driver.current_url
        print(f"Search completed. Final URL: {search_url}")
        return search_url

    except Exception as e:
        print(f"Error during search: {str(e)}")
        driver.save_screenshot("search_error.png")
        return None

def scrape_all_rozee_pages(driver, final_url, max_pages=5):
    """
    Scrapes all job listings from Rozee.pk search results pages.
    Returns a pandas DataFrame with job details.
    """
    print("Starting job scraping...")
    print(f"Using URL: {final_url}")

    wait = WebDriverWait(driver, 15)
    all_jobs = []
    base_url = f"{final_url}/stype/title"

    try:
        for page in range(1, max_pages + 1):
            print(f"\nProcessing Page {page}...")
            url = f"{base_url}/fpn/{page*20}" if page > 1 else base_url
            driver.get(url)

            # Wait for jobs to load
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.job")))

            # Extract job cards
            job_cards = driver.find_elements(By.CSS_SELECTOR, "div.job")
            print(f"Found {len(job_cards)} jobs on page {page}")

            for i, card in enumerate(job_cards, 1):
                try:
                    title = card.find_element(By.CSS_SELECTOR, "h3.s-18 a bdi").text.strip()
                    company = card.find_element(By.CSS_SELECTOR, "div.cname a:first-child").text.strip()
                    # Try to get salary, if available
                    try:
                        salary = card.find_element(
                            By.CSS_SELECTOR, "span[data-toggle='tooltip'] span"
                        ).text.strip()
                    except Exception:
                        salary = "Not listed"

                    all_jobs.append({
                        "Title": title,
                        "Company": company,
                        "Salary": salary
                    })
                except Exception as e:
                    print(f"  Error on job {i}: {str(e)}")

            # Stop if fewer jobs than expected (last page)
            if len(job_cards) < 10:  # Adjust if jobs per page changes
                print("Reached last page")
                break

    except Exception as e:
        print(f"Critical error: {str(e)}")
        driver.save_screenshot("pagination_error.png")

    return pd.DataFrame(all_jobs)

if __name__ == "__main__":
    # Set up Chrome options
    options = Options()
    options.add_argument('--headless')  # Uncomment for headless mode
    options.add_argument('--disable-gpu')
    options.add_argument("--window-size=1200,800")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # Create a single driver instance
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        job = input("Enter job title (press Enter for default): ") or "Software Engineer"
        city = input("Enter City (press Enter for default): ") or "Karachi"

        # Get search URL
        final_url = get_search_url(driver, job_title=job, city=city)
        if not final_url:
            print("Failed to get search URL. Exiting.")
        else:
            # Scrape job listings
            df = scrape_all_rozee_pages(driver, final_url, max_pages=10)
            print("\nFinal Results:")
            print(f"Total jobs scraped: {len(df)}")
            filename = f"rozee_{job.lower().replace(' ', '_')}_{city}_jobs.csv"
            df.to_csv(filename, index=False)
            print(f"Data saved to {filename}")
    finally:
        # Always close the driver
        driver.quit()