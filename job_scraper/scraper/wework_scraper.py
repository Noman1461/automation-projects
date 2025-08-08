from requests_html import HTMLSession
import pandas as pd
from datetime import datetime
import logging
import os

log_dir = os.path.join(os.path.dirname(__file__), '../logs')
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, 'job_scraper.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

BASE_URL = "https://weworkremotely.com/remote-jobs"

def scrape_jobs():
    session = HTMLSession()

    try:
        logging.info("Starting job scraping...")
        response = session.get(BASE_URL)
        response.html.render(timeout=20)
        logging.info(f"Fetched HTML content from {BASE_URL}")

        # 🔧 The main job listings are under section with class "jobs"
        job_sections = response.html.find("section.jobs")

        if not job_sections:
            logging.warning("No job sections found.")
            return pd.DataFrame()

        jobs = []

        for section in job_sections:
            category_header = section.find("h2", first=True)
            category = category_header.text if category_header else "Unknown"

            job_posts = section.find("li")

            for post in job_posts:
                # skip footer or view-all links
                if "view-all" in post.attrs.get("class", []):
                    continue

                link_elem = post.find("a", first=True)
                company_elem = post.find("span.company", first=True)
                title_elem = post.find("span.title", first=True)
                location_elem = post.find("span.region.company", first=True)

                jobs.append({
                    "category": category,
                    "title": title_elem.text if title_elem else "N/A",
                    "company": company_elem.text if company_elem else "N/A",
                    "location": location_elem.text if location_elem else "Worldwide",
                    "url": "https://weworkremotely.com" + link_elem.attrs["href"] if link_elem else "N/A",
                    "scraped_at": datetime.now().isoformat()
                })

        logging.info(f"Scraped {len(jobs)} jobs successfully.")
        return pd.DataFrame(jobs)

    except Exception as e:
        logging.error(f"Error during scraping: {str(e)}")
        return pd.DataFrame()
