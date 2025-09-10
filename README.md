# Bing Job Scraper

The **Bing Job Scraper** is a Python project that automates job searching by extracting job listings from **Bing search results**.  
It is **configurable**: you can specify job titles and the number of jobs to fetch in the `config.json` file.  
The scraper runs via **Selenium WebDriver** and saves the results in **CSV format** for further analysis.

---

## 🚀 Features
- ✅ Scrapes job listings from **Bing**
- ✅ Configurable job titles and job count (`config.json`)
- ✅ Saves results into **separate CSV files** (per job title)
- ✅ Error handling ensures one failure doesn’t stop the script
- ✅ Modular design: `main.py` (orchestration) + `bing_scraper.py` (scraping logic)
- ✅ Includes **unit tests** and **integration tests** with `pytest`

---

## 📂 Project Structure
job_scraper_project/
│── main.py                # Entry point, orchestrates scraping  
│── config.json            # Configuration file with job titles & target count  
│── scrapers/  
│     └── bing_scraper.py  # Contains Bing scraping logic  
│── tests/  
│     └── test_scraper.py  # Unit + integration tests for the scraper  
│── requirements.txt       # Python dependencies  
│── output/                # Folder where CSV files are saved  
│── README.md              # Project documentation  

---

## ⚙️ Setup

### Prerequisites
- Python 3.x  
- Microsoft Edge (or Chrome, depending on driver setup)  
- WebDriver (EdgeDriver or ChromeDriver) installed  

### Installation
# Clone or download the repository  
git clone https://github.com/your-username/job_scraper_project.git  
cd job_scraper_project  

---

## 🛠 Configuration (`config.json`)

{
  "target_job_count": 50,
  "job_titles": [
    "Python Developer in Tamil Nadu",
    "Fullstack Developer in Tamil Nadu",
    "Cybersecurity Engineer in Tamil Nadu",
    "Mechanical CAD Engineer in Tamil Nadu",
    "ANSYS Engineer in Tamil Nadu",
    "PLC Programmer in Tamil Nadu",
    "CNC Operator in Tamil Nadu"
  ]
}

- **`target_job_count`** → Number of jobs to fetch for each title  
- **`job_titles`** → List of job roles (with optional location)  

---

## ▶️ Running the Scraper
python main.py

This will:  
1. Read the configuration from `config.json`  
2. Scrape jobs for each title using **Bing search**  
3. Save results into separate CSV files under `/output/`  

---

## 📜 Code Overview

### `main.py`
- Loads job titles and job count from `config.json`  
- Calls `scrape_bing_jobs()` from `bing_scraper.py` for each title  
- Handles errors gracefully and continues with the next job  

### `bing_scraper.py`
- Uses Selenium WebDriver to open Bing  
- Searches for job queries (e.g., “Python Developer in Tamil Nadu jobs”)  
- Extracts details:  
  - Job Title  
  - Company  
  - Location  
  - Link  
- Saves results into a CSV file named after the job role  

---

## 📊 Output

- Results are saved in the `output/` folder.  
- Each job title has a **separate CSV file**.  

**Example (`Python_Developer_in_Tamil_Nadu.csv`):**

Title,Company,Location,Link  
Python Developer,ABC Pvt Ltd,Chennai,https://...  
Python Engineer,XYZ Solutions,Coimbatore,https://...  

---

## 🧪 Testing

This project includes **unit tests** and **integration tests** written with `pytest`.  

### Running Tests
# Install test dependencies (pytest + pytest-mock)  
pip install pytest pytest-mock  

# Run all tests  
pytest tests/  

---

### Test Coverage

- **Unit Tests (`test_get_real_url`)**  
  - Validates the helper function that decodes real job URLs from Bing.  
  - Ensures proper handling when parameters are missing.  

- **Integration Test (`test_scraper_flow`)**  
  - Uses `pytest-mock` to simulate Selenium WebDriver.  
  - Verifies scraper flow without opening a real browser.  
  - Checks that CSV writing, URL generation, and browser cleanup work correctly.  

---

## 🛡 Error Handling
- If `config.json` is missing → prints an error and exits  
- If scraping fails for one job title → logs the error and moves to the next  
- Ensures **full scraping run** even if some jobs fail  

---

## 🔮 Future Enhancements
- Add support for other portals (LinkedIn, Indeed, Naukri)  
- Add filters (experience, salary, job type)  
- Export to databases (MySQL, MongoDB)  
- Build a web-based UI for running and monitoring scrapers  

---

📌 **Authors**: Arunbalaji and Kalaiselvan
