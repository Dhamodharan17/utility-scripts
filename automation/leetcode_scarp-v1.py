from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Function to split text into lines of max 20 words
def split_into_lines(text, max_words=12):
    words = text.split()
    for i in range(0, len(words), max_words):
        yield " ".join(words[i:i + max_words])

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Open LeetCode Problems Page
driver.get("https://leetcode.com/problem-list/akzwstdi/")



def scarp_problem():
    # Fetch the elements
    # Wait for the problem content to load
    wait = WebDriverWait(driver, 10)
    problem_content_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-track-load='description_content']")))

    problem_content_elements = driver.find_elements(By.XPATH, "//div[@data-track-load='description_content']")

    # Debugging step: Check the number of elements
    print(f"Found {len(problem_content_elements)} elements")

    # Open the file in write mode
    with open('problem_content.txt', 'w', encoding='utf-8') as file:
        # Iterate over the elements and extract the innerHTML
        for div_element in problem_content_elements:
            div_content = div_element.get_attribute("innerHTML")  # Get the HTML content of the div
            
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(div_content, 'html.parser')
            
            # Handle <code> and <p> tags
            for code_tag in soup.find_all('code'):
                code_text = code_tag.get_text()  # Get text inside <code> tag
                code_tag.replace_with(code_text)  # Replace <code> tag with its text content
            
            # Extract and process <p> tags
            paragraphs = soup.find_all('p')
            for paragraph in paragraphs:
                paragraph_text = paragraph.get_text(separator=" ", strip=True)
                # Write in lines of max 20 words
                for line in split_into_lines(paragraph_text):
                    file.write(line + "\n")
            
            # Handle any remaining text outside <p> tags
            remaining_text = soup.get_text(separator=" ", strip=True)
            for line in split_into_lines(remaining_text):
                file.write(line + "\n")

    print("Scraping completed. Cleaned data written to problem_content.txt")

scarp_problem()
