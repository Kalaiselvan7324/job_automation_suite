# In tests/test_scraper.py
import pytest
from scrapers.bing_scraper import get_real_url, scrape_bing_jobs

# --- 1. Unit Test for the Helper Function ---
def test_get_real_url():
    """
    Tests if the URL decoding function works correctly.
    This test is fast and doesn't need a browser.
    """
    bing_url = "https://www.bing.com/ck/a?!&&p=some_encoded_stuff&u=a1aHR0cHM6Ly93d3cuZXhhbXBsZS5jb20vP2E9MSZiPTI&ntb=1"
    expected_url = "https://www.example.com/?a=1&b=2"
    assert get_real_url(bing_url) == expected_url

def test_get_real_url_with_no_param():
    """Tests that the function returns the original URL if 'u' param is missing."""
    normal_url = "https://www.google.com"
    assert get_real_url(normal_url) == normal_url

# --- 2. Integration Test using Mocking ---
def test_scraper_flow(mocker):
    """
    Tests the main scrape_bing_jobs function's flow without a real browser.
    'mocker' is a fixture from the pytest-mock library.
    """
    # We "mock" (fake) the webdriver, replacing it with a controllable object.
    mock_driver = mocker.MagicMock()
    mocker.patch('scrapers.bing_scraper.webdriver.Edge', return_value=mock_driver)

    # We also mock the file writing to avoid creating real CSVs during tests.
    mock_open = mocker.patch('builtins.open', mocker.mock_open())
    
    # Run our main function with test data
    scrape_bing_jobs(job_title="Test Job", target_count=1)

    # Assert that our fake browser was told to go to the correct, URL-encoded address
    mock_driver.get.assert_called_with("https://www.bing.com/jobs?q=Test%20Job&form=JOBL2S")
    
    # Assert that a CSV file was opened for writing with the correct dynamic name
    mock_open.assert_called_with('test_job_jobs.csv', 'w', newline='', encoding='utf-8')
    
    # Assert that the browser was properly closed at the end
    mock_driver.quit.assert_called_once()