import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # 0=all, 1=info, 2=warning, 3=error
os.environ['ABSL_LOG_LEVEL'] = 'ERROR'

import warnings
#suppress TensorFlow warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore")

from absl import logging
#suppress absl logging warnings
logging.set_verbosity(logging.ERROR)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd



def get_search_url(driver, job_title, city):
    """Performs search on Rozee.pk and returns the final search URL"""
    actions = ActionChains(driver)
    
    try:
        print("Loading Rozee.pk homepage...")
        driver.get("https://www.rozee.pk")
        time.sleep(2)
        
        print("Locating search field...")
        search_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input#search.form-control.input-lg"))
        )
        
        print(f"Searching for: {job_title}")
        search_field.clear()
        search_field.send_keys(job_title)
        time.sleep(1)
        
        # Click directly on city dropdown (no TAB needed)
        print("Locating City dropdown...")
        city_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-id='homeSearchCity']"))
        )
        
        # Scroll into view and click using JavaScript
        driver.execute_script("arguments[0].scrollIntoView();", city_dropdown)
        driver.execute_script("arguments[0].click();", city_dropdown)
        time.sleep(1)
        
        print(f"Selecting city: {city}")
        try:
            # Find the city in dropdown list
            city_option = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, f"//span[contains(@class, 'text') and contains(text(), '{city}')]"))
            )
            city_option.click()
        except:
            print(f"City '{city}' not found in dropdown. Using default (Karachi)")
            # Close dropdown by clicking elsewhere
            actions.move_by_offset(10, 10).click().perform()
        
        # Submit using JavaScript to avoid interception
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        driver.execute_script("arguments[0].click();", submit_btn)
        
        # Wait for results to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.job"))
        )
        time.sleep(2)
        
        search_url = driver.current_url
        print(f"Search completed. Final URL: {search_url}")
        return search_url
        
    except Exception as e:
        print(f"Error during search: {str(e)}")
        driver.save_screenshot("search_error.png")
        return None
    finally:
        driver.quit()

def scrape_all_rozee_pages(driver, final_url, max_pages=5):
    print("Initializing Driver...")
    print(f"Using URL: {final_url}")
    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument("--window-size=1200,800")
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
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

            # Extract current page jobs
            job_cards = driver.find_elements(By.CSS_SELECTOR, "div.job")
            print(f"Found {len(job_cards)} jobs on {page}")
                
            for i, card in enumerate(job_cards, 1):
                # Skip if no title found (not a job card)
                
                #print(f"  Job {i}: {title[:30]}... | {company[:20]}... | {salary}")
                try:
                    # Try to find the title element
                    title_elems = card.find_elements(By.CSS_SELECTOR, "h3.s-18 a bdi")
                    if not title_elems:
                        # No title found, likely not a job card (could be ad or promo)
                        continue  # Skip this card

                    title = title_elems[0].text.strip()
                    company_elems = card.find_elements(By.CSS_SELECTOR, "div.cname a:first-child")
                    company = company_elems[0].text.strip() if company_elems else "Not found"

                    try:
                        salary = card.find_element(
                            By.CSS_SELECTOR, "span[data-toggle='tooltip'] span"
                        ).text.strip()
                    except:
                        salary = "Not listed"

                    all_jobs.append({
                        "Title": title,
                        "Company": company,
                        "Salary": salary
                    })
                except Exception as e:
                    print(f"  Error on job {i}: {str(e)}")
            # Stop if no more pages
            if len(job_cards) < 10:  # Assuming 10 jobs per page
                print("Reached last page")
                break
                
    except Exception as e:
        print(f"Critical error: {str(e)}")
        driver.save_screenshot("pagination_error.png")
    
    return pd.DataFrame(all_jobs)

# if __name__ == "__main__":
#     options = Options()
#     #options.add_argument('--headless')
#     options.add_argument('--disable-gpu')
#     options.add_argument("--window-size=1200,800")
#     options.add_experimental_option("excludeSwitches", ["enable-logging"])

#     driver = webdriver.Chrome(
#         service=Service(ChromeDriverManager().install()),
#         options=options
#     )

#     try:
#         time.sleep(2)
#         job = input("Enter job title (press Enter for default): ") or "Software Engineer"
#         city = input("Enter City (press Enter for default): ") or "Karachi"

#         final_url = get_search_url(driver, job_title=job, city=city)
#         df = scrape_all_rozee_pages(driver, final_url, max_pages=10)
#         print("\nFinal Results:")
#         print(f"Total jobs scraped: {len(df)}")
#         filename = f"rozee_{job.lower().replace(' ', '_')}_{city}_jobs.csv"
#         df.to_csv(filename, index=False)
#         print(f"Data saved to {filename}")
#     finally:
#         driver.quit()

def run_rozee_scraper(job="Software Engineer", city="Karachi", max_pages=10):
    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument("--window-size=1200,800")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    try:
        final_url = get_search_url(driver, job_title=job, city=city)
        df = scrape_all_rozee_pages(driver, final_url, max_pages=max_pages)
        filename = f"rozee_{job.lower().replace(' ', '_')}_{city}_jobs.csv"
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
        return df
    finally:
        driver.quit()