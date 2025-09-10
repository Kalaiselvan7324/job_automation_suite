# In scrapers/bing_scraper.py

# --- IMPORTS ---
import csv
import time
import urllib.parse
import base64
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# --- HELPER FUNCTION ---
def get_real_url(redirect_url: str) -> str:
    """Parses a Bing redirect URL to extract and decode the real destination URL."""
    try:
        parsed_url = urllib.parse.urlparse(redirect_url)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        if 'u' in query_params:
            encoded_url = query_params['u'][0]
            if encoded_url.startswith('a1'):
                encoded_url = encoded_url[2:]
            
            # Add padding if necessary
            missing_padding = len(encoded_url) % 4
            if missing_padding:
                encoded_url += '=' * (4 - missing_padding)
            
            decoded_url = base64.b64decode(encoded_url).decode('utf-8')
            return decoded_url
    except Exception:
        return redirect_url # Return original if parsing fails
    return redirect_url

# --- MAIN SCRAPER FUNCTION ---
def scrape_bing_jobs(job_title: str, target_count: int):
    """
    Scrapes Bing for a specific job title until the target count is reached.
    Saves the results to a CSV file named after the job title.
    """
    print(f"\n▶️ Starting scrape for: '{job_title}'")
    
    # --- SETUP THE WEB DRIVER ---
    service = Service() 
    driver = webdriver.Edge(service=service)
    driver.maximize_window()

    # --- DYNAMIC URL AND FILENAME ---
    query = urllib.parse.quote(job_title) # Make the job title URL-safe
    url = f"https://www.bing.com/jobs?q={query}&form=JOBL2S"
    # Create a clean filename (e.g., "python_developer_in_tamil_nadu_jobs.csv")
    filename = f"{job_title.replace(' ', '_').lower()}_jobs.csv"

    driver.get(url)
    wait = WebDriverWait(driver, 15)

    # --- PREPARE THE CSV FILE ---
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['S.No', 'Name', 'Description', 'Apply Link'])

        job_count = 0
        scraped_job_ids = set()

        # --- MAIN INFINITE SCROLL & SCRAPE LOOP ---
        # This is your original logic, now inside this function
        while job_count < target_count:
            job_elements = driver.find_elements(By.CLASS_NAME, "jb_jlc")
            print(f"   DEBUG: Found {len(job_elements)} job elements using class 'jb_jlc'.")
            if len(job_elements) == len(scraped_job_ids):
                print("   Scrolling to load more jobs...")
                last_height = driver.execute_script("return document.body.scrollHeight")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                
                try:
                    time.sleep(3) # Wait for page to load
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        print("   Reached the end of the job list for this title.")
                        break
                except TimeoutException:
                    print("   No new jobs loaded. Reached the end.")
                    break
            
            details_panel_element = None
            for job in job_elements:
                if job_count >= target_count:
                    break
                
                job_id = job.get_attribute('data-jobid')
                if job_id in scraped_job_ids:
                    continue

                print(f"   Processing Job #{job_count + 1}...")
                try:
                    driver.execute_script("arguments[0].click();", job)
                    
                    if details_panel_element:
                        wait.until(EC.staleness_of(details_panel_element))

                    details_panel_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "jb_l2_jbpnl")))
                    
                    name = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "jbpnl_title"))).text
                    
                    cleaned_description = "Description not found."
                    try:
                        desc_element = driver.find_element(By.CLASS_NAME, "jbpnl_description_blk")
                        cleaned_description = ' '.join(desc_element.text.split())
                    except NoSuchElementException:
                        pass

                    final_url = "Apply link not found."
                    try:
                        apply_container = driver.find_element(By.ID, "jb_Apply")
                        apply_link = apply_container.find_element(By.TAG_NAME, "a").get_attribute('href')
                        final_url = get_real_url(apply_link)
                    except NoSuchElementException:
                        pass

                    writer.writerow([job_count + 1, name, cleaned_description, final_url])
                    print(f"   ✅ Scraped: {name}")
                    job_count += 1
                    scraped_job_ids.add(job_id)

                except Exception as e:
                    print(f"   ❌ Error processing a job, skipping. Details: {e}")
                    scraped_job_ids.add(job_id) # Add to set to avoid retrying a broken element

    # --- CLEANUP ---
    driver.quit()
    print(f" Scraping for '{job_title}' complete! Data saved to {filename}")