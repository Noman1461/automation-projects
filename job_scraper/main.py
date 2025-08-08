from scraper.scrape_Rozee import run_rozee_scraper

if __name__ == "__main__":
    job = input("Enter job title (press Enter for default): ") or "Software Engineer"
    city = input("Enter City (press Enter for default): ") or "Karachi"
    run_rozee_scraper(job, city, max_pages=10)