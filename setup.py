from DrissionPage import WebPage, ChromiumOptions, ChromiumPage
from DrissionPage.common import Keys
from DrissionPage.common import Actions
from DrissionPage import WebPage, ChromiumOptions
from DrissionPage.common import Keys
from DrissionPage.common import Actions
from DrissionPage.common import By
import time
import random
import json
import re
import unicodedata
import pandas as pd
import os
import csv
import asyncio
# def save_to_csv(filename, data):
#     # Create a dictionary from the provided name and url
  
    
#     # Convert the dictionary to a DataFrame
#     df = pd.DataFrame([data])
    
#     # Check if the file already exists
#     if os.path.isfile(filename):
#         # If the file exists, append the new data without writing the header
#         df.to_csv(filename, mode='a', header=False, index=False)
#     else:
#         # If the file does not exist, write the data with the header
#         df.to_csv(filename, mode='w', header=True, index=False)

def save_to_csv(filename, data):
    # if isinstance(data, dict):
    #     data = [data]  #
    df = pd.DataFrame(data)
    df.to_csv(filename, mode='w', header=True, index=False, encoding='utf-8')

def save_to_csv2(filename, data):
    # if isinstance(data, dict):
    #     data = [data]  #
    df = pd.DataFrame(data)
    df.to_csv(filename, mode='a', header=True, index=False, encoding='utf-8')
def convert_to_slug(name):
    name = unicodedata.normalize('NFKD', name)
    name = re.sub(r'[^\w\s-]', '', name)
    slug = re.sub(r'\s+', '-', name)
    return slug


ua = {'user_agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36',
 'viewport': {'width': 320, 'height': 658},
 'device_scale_factor': 4.5,
 'has_touch': True,
 }

viewport = ','.join(map(str, ua['viewport'].values()))
user_agent = ua['user_agent']



user_data_path = r'C:\Users\ADMIN\AppData\Local\Google\Chrome\User Data\Profile crawlshopee' 
co = ChromiumOptions()
co.set_user_data_path(user_data_path)
page = WebPage(chromium_options=co)
page.get('https://shopee.vn/')



