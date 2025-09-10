import json
from scrapers.bing_scraper import scrape_bing_jobs

def main():
    # Load configuration from the JSON file
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Error: config.json not found. Please create it.")
        return
        
    job_titles_to_scrape = config.get("job_titles", [])
    target_count = config.get("target_job_count", 50)

    if not job_titles_to_scrape:
        print("No job titles found in config.json. Exiting.")
        return

    # Loop through each job title and run the scraper
    for title in job_titles_to_scrape:
        try:
            scrape_bing_jobs(job_title=title, target_count=target_count)
        except Exception as e:
            print(f"\n--- A error occurred while scraping for '{title}' ---")
            print(f"ERROR: {e}")
            print("--- Moving to the next job title. ---\n")
    
    print("\n Scraping completed for all job titles.")

if __name__ == "__main__":
    main()