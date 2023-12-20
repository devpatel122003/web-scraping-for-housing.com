import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os

# Set up the driver



# Navigate to the website
# website_url = 'https://housing.com/buy-real-estate-surat'
# driver.get(website_url)
# time.sleep(1)
# driver.maximize_window()
# time.sleep(1)
# all_links = []
#
#
# def write_link_to_csv(link, csv_filename='all_project_links.csv'):
#     # Check if the CSV file exists
#     file_exists = os.path.isfile(csv_filename)
#
#     # If the file doesn't exist, create a new DataFrame with a column 'Link'
#     if not file_exists:
#         df = pd.DataFrame(columns=['Link'])
#     else:
#         # If the file exists, read the existing CSV into a DataFrame
#         df = pd.read_csv(csv_filename)
#
#     # Append the new link to the DataFrame
#     new_row = pd.DataFrame({'Link': [link]})
#     df = pd.concat([df, new_row], ignore_index=True)
#
#     # Write the DataFrame back to the CSV file
#     df.to_csv(csv_filename, index=False)
#
#     print(f"Link '{link}' has been written to {csv_filename}")
#
#
# def topproject():
#     # TOP PROJECTS
#     driver.execute_script("window.scrollTo(0, 1150);")
#     time.sleep(1)
#     # Find all <a> tags with the specified class names using XPath
#     class_names_xpath = '//a[contains(@class, "css-tlsx9j")]'
#     a_tags = driver.find_elements(By.XPATH, class_names_xpath)
#     # Print the href attribute of each matching <a> tag
#     for a_tag in a_tags:
#         write_link_to_csv(a_tag.get_attribute('href'))
#     time.sleep(1)
#
#
# def projectinfocus():
#     # PROJECTS IN FOCUS
#     driver.execute_script("window.scrollTo(1150, 1900);")
#     time.sleep(1)
#     # Find all <div> elements with the specified class names using XPath
#     div_class_names_xpath = '//div[contains(@class, "_vyqu5l") and contains(@class, "_e21p3n") and contains(@class, "_mkh2mm") and contains(@class, "_5jftgi") and contains(@class, "_h019bv") and contains(@class, "_ft8m1p81") and contains(@class, "_tcsk122m") and contains(@class, "_biqgftgi") and contains(@class, "_8kgnf6fq")]'
#     div_elements = driver.find_elements(By.XPATH, div_class_names_xpath)
#
#     # Iterate through each <div> element and find the <a> tags within it
#     for div_element in div_elements:
#         # Find all <a> tags within the current <div> using XPath
#         a_tags = div_element.find_elements(By.XPATH, './/a')
#
#         # Print the href attribute of each matching <a> tag
#         for a_tag in a_tags:
#             write_link_to_csv(a_tag.get_attribute('href'))
#     time.sleep(1)
#
#
# def featuredproject():
#     # Featured Projects
#     driver.execute_script("window.scrollTo(1900, 3000);")
#     time.sleep(1)
#
#     div_elements = driver.find_elements(By.CLASS_NAME, 'css-13o7eu2')
#     # css-13o7eu2
#     # css-uwwqev
#     # Iterate through each <div> element
#     for div_element in div_elements:
#         # Find all <a> tags within the current <div> element
#         a_tags = div_element.find_elements(By.TAG_NAME, 'a')
#
#         # Extract and print the href attribute of each matching <a> tag
#         for a_tag in a_tags:
#             write_link_to_csv(a_tag.get_attribute('href'))
#     time.sleep(1)
#
#
# def trendingproject():
#     # Trending Project
#     driver.execute_script("window.scrollTo(3700,4200);")
#     time.sleep(2)
#
#     div_elements = driver.find_elements(By.CLASS_NAME, 'css-13o7eu2')
#     # css-13o7eu2
#     # css-uwwqev
#     # Iterate through each <div> element
#     for div_element in div_elements:
#         # Find all <a> tags within the current <div> element
#         a_tags = div_element.find_elements(By.TAG_NAME, 'a')
#
#         # Extract and print the href attribute of each matching <a> tag
#         for a_tag in a_tags:
#             write_link_to_csv(a_tag.get_attribute('href'))
#     time.sleep(1)
#
#
# def getalllinks():
#     topproject()
#     projectinfocus()
#     featuredproject()
#     trendingproject()
#
# getalllinks()
#
# # _9s1ule
# # _9s1ule
#
# # Close the browser window
# driver.quit()

#
def scrape_website(url):
    # Initialize the Chrome webdriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    try:
        # Open the website
        driver.get(url)

        # Your scraping functions go here
        project_name = getprojectname(driver)
        contractor = getcontractor(driver)
        address = getaddress(driver)
        all_data = getalldata(driver)

        # Create a dictionary with the collected data
        data_dict = {'URL': url, 'Project Name': project_name, 'Contractor': contractor, 'Address': address, **all_data}
        # time.sleep(2)
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        data_dict = {'URL': url, 'Error': str(e)}

    finally:
        # Close the browser window
        driver.quit()
        # time.sleep(2)
    return data_dict

def getprojectname(driver):
    h1_element = driver.find_element(By.CSS_SELECTOR, 'h1.css-1hidc9c')
    return h1_element.text

def getcontractor(driver):
    span_element = driver.find_element(By.CSS_SELECTOR, 'span[data-q="dev-name"]')
    return span_element.text

def getaddress(driver):
    div_element = driver.find_element(By.CLASS_NAME, 'css-1ty5xzi')
    return div_element.text

def getalldata(driver):
    table_element = driver.find_element(By.CLASS_NAME, '_9s1ule')
    rows = table_element.find_elements(By.TAG_NAME, 'tr')
    data_dict = {}

    for row in rows[1:]:
        cells = row.find_elements(By.TAG_NAME, 'td')
        key = cells[0].text.strip()
        value = cells[1].text.strip()
        data_dict[key] = value

    return data_dict

# Read URLs from the input CSV file using pandas
input_csv_file = 'all_project_links.csv'
df_urls = pd.read_csv(input_csv_file)

# Initialize an empty list to store the collected data
data_list = []

# Iterate through each URL
for index, row in df_urls.iterrows():
    url = row['Link']
    data_dict = scrape_website(url)
    data_list.append(data_dict)
    time.sleep(2)
    # break

# Convert the list of dictionaries to a DataFrame
df_data = pd.DataFrame(data_list)

# Save the collected data to a new CSV file
output_csv_file = 'output_data.csv'
df_data.to_csv(output_csv_file, index=False)

print(f"Data collected from {len(df_urls)} URLs and saved to {output_csv_file}")