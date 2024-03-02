from selenium.webdriver.common.by import By
from difflib import SequenceMatcher

import requests
import itertools
import time
import random
import subprocess
import socket

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def compare_names(name1, name2):
    # Normalize the strings to lowercase
    name1 = name1.lower()
    name2 = name2.lower()

    # Tokenize the names
    tokens1 = name1.split()
    tokens2 = name2.split()

    # Compare each token with all tokens in the other name
    scores = [similar(t1, t2) for t1, t2 in itertools.product(tokens1, tokens2)]

    # Calculate the average similarity
    if scores:
        average_similarity = sum(scores) / len(scores)
    else:
        average_similarity = 0

    return average_similarity

def random_wait(v):
    wait_time = v * 0.35
    random_wait_time = random.uniform(v - wait_time, v + wait_time)
    print(f"Waiting for {random_wait_time} seconds")
    time.sleep(random_wait_time)


def wait_for_internet_connection():
    while True:
        try:
            # Try to connect to a well-known website
            socket.create_connection(("www.google.com", 80))
            print("Internet connection is available")
            break
        except OSError:
            print("Waiting for internet connection...")
            time.sleep(5)


def change_ip():
    pass
    # subprocess.run(["C:\\Program Files\\NordVPN\\NordVPN.exe", '-c', '-g', "United States"])
    # wait_for_internet_connection()


def check_for_captcha():
    random_wait(2)
    
    try:
        challenge_text = self.driver.find_element(By.XPATH, '//*[@id="challenge-running"]').text

        while True:
            if input("Press enter when the challenge is solved") == "":
                break

        return True

    except:
        return False

def compare_names(name1, name2):
    # Normalize the strings to lowercase
    name1 = name1.lower()
    name2 = name2.lower()

    # Tokenize the names
    tokens1 = name1.split()
    tokens2 = name2.split()

    # Compare each token with all tokens in the other name
    scores = [similar(t1, t2) for t1, t2 in itertools.product(tokens1, tokens2)]

    # Calculate the average similarity
    if scores:
        average_similarity = sum(scores) / len(scores)
    else:
        average_similarity = 0

    return average_similarity


def check_if_company(name):
    # Common words and suffixes in company names
    company_keywords = ["Inc", "Corporation", "Corp", "Company", "Co", "Ltd", "LLC", "Group", "Partners", "Enterprises", "L.P."]

    # Simple check if the name contains any company keyword
    if any(keyword in name for keyword in company_keywords):
        return False

    return True