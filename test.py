from selenium import webdriver
from selenium.webdriver.firefox.service import Service

# Specify the path to the geckodriver executable
geckodriver_path = 'C:\geckodriver.exe'

# Create Firefox options
firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument('-headless')  # Run Firefox in headless mode

# Create the geckodriver service
service = Service(geckodriver_path)

# Create the Firefox driver with the service and options
driver = webdriver.Firefox(service=service, options=firefox_options)

# Open a website
driver.get('https://www.youtube.com')

# Perform actions or assertions on the webpage

# Quit the driver
driver.quit()
