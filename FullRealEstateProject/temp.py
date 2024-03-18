from selenium import webdriver
from time import sleep
import requests
import json

# 2Captcha's API key
api_key = '813fc4ffea2bc4d91059d4510b39e180'

# Start webdriver
driver = webdriver.Firefox()
driver.get('https://www.google.com/recaptcha/api2/demo')

# Get the site key of reCAPTCHA
site_key = driver.find_element_by_class_name('g-recaptcha').get_attribute('data-sitekey')

# Send a request to 2Captcha to solve reCAPTCHA
response = requests.post('http://2captcha.com/in.php', data={
    'key': api_key,
    'method': 'userrecaptcha',
    'googlekey': site_key,
    'pageurl': 'https://www.google.com/recaptcha/api2/demo',
    'json': 1
})

# Get the request ID from 2Captcha
request_id = json.loads(response.text)['request']

# Wait for 2Captcha to solve reCAPTCHA
while True:
    response = requests.get(f'http://2captcha.com/res.php?key={api_key}&action=get&id={request_id}&json=1')
    result = json.loads(response.text)

    if result['status'] == 1:
        # Enter the solution into reCAPTCHA
        driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML="{result["request"]}";')
        sleep(2)
        driver.find_element_by_id('recaptcha-demo-submit').click()
        break

    sleep(5)