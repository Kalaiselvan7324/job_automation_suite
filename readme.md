# Bing Job Scraper

This project scrapes job listings from Bing for a configurable list of job titles and saves the results into separate CSV files.

## Setup

1.  Ensure you have Python and Microsoft Edge installed.
2.  Install the required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```
3.  Modify the `job_titles` and `target_job_count` in the `config.json` file to suit your needs.

## How to Run

### To Run the Scraper

Execute the main script from the terminal in the `job_scraper_project` directory:

```bash
python main.py