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

# co.set_headless(False)

# co.set_user_agent(user_agent=user_agent)
# # # co.set_no_js(True)
# co.set_argument('--window-size', viewport)
# co.set_no_imgs(True)
# co.set_mute(True)
page = WebPage(chromium_options=co)


# page.get('https://shopee.vn/verify/traffic/error?home_url=https%3A%2F%2Fshopee.vn&is_logged_in=true&tracking_id=343261ea249-6a3c-48c2-b2b4-927dab878339&type=1')
# with open('./cookies.json', 'r') as file:
#     cookies = json.load(file)
# for cookie in cookies:
#     page.set.cookies(cookie)
  
# def logout(page):

#     page.get('https://shopee.vn/verify/traffic/error?home_url=https%3A%2F%2Fshopee.vn&is_logged_in=true&tracking_id=343261ea249-6a3c-48c2-b2b4-927dab878339&type=1')

#     sign = (By.XPATH,"/html/body/div[1]/div/div[2]/div/div/div/div[1]/div[3]/button")
#     button = page.ele(sign)
#     button.click()



# async def login_cookie(page):
#     with open('cookies.json', 'r') as file:
#         cookies = json.load(file)
#     for cookie in cookies:
#         page.set.cookies(cookie)


def get_category():
    page.set.load_mode.none()  # Set the load mode to none
    page.listen.start('/api/v4/pages/get_homepage_category_list') 
    page.get('https://shopee.vn/')  
    packet = page.listen.wait()  
    page.stop_loading()  
    response_body = packet.response.body
    category_list = response_body['data']['category_list']
    for category in category_list:
        print(category)
        cate_name =  category['display_name']
        slug_cate = convert_to_slug(category['display_name'])
        cate_id =  category['catid']
        url = "https://shopee.vn/{}-cat.{}".format(slug_cate,cate_id)
        save_to_csv("catemain.csv",cate_name,url)
      


async def get_cate_child_and_list_data_shop_sales(page,url):
    time.sleep(1)
    page_nice = 0
    check_page = True
    data = []
    #check_page  = true
    while(check_page == True):
        page.set.load_mode.none()  # Set the load mode to none
        #api sản phẩm bán chạy  (lưu lại id shop để tý get vào shop lấy all thông tin)
        page.listen.start('/api/v4/search/search_items?by=sales')
        #api cate con
        # #lấy tất cả danh mục con
        # page.listen.start('https://shopee.vn/api/v4/pages/get_sub_category_list?')
    

       
        url_new =  url+"?page={}&sortBy=sales".format(page_nice)
        print(url_new)
    
        page.get(str(url_new))  


        packet = page.listen.wait()  
     
        page.stop_loading()  
        response_body = packet.response.body
        time.sleep(3)
        # print(response_body['items'][0]['item_basic'])
        try:
            if(len(response_body['items'])):
            
                page_nice = page_nice + 1
                for item in response_body['items']:
                    # print(item)
                    shopid = item['item_basic']['shopid']
                    itemid= item['item_basic']['itemid']
                    name= item['item_basic']['name']
                    sold= item['item_basic']['sold']
                    brand  = item['item_basic']['brand']
                    historical_sold = item['item_basic']['historical_sold']
                    discount = item['item_basic']['discount']
                    price_min = item['item_basic']['price_min']
                    price_max = item['item_basic']['price_max']
                    rating = item['item_basic']['item_rating']
                    price =item['item_basic']['price']
                    urlx = "https://shopee.vn/abc-i.{}.{}".format(shopid,itemid)
                    #url https://shopee.vn/abc-i.499999587.27251289777  .shopid.itemid
                    #trong url có cả thông tin shop
                    # print(shopid,itemid, name)

                    items = {
                        "shopid":shopid,
                        "itemid":itemid,
                        "name": name,
                        "sold": sold,
                        "brand":brand,
                        "historical_sold": historical_sold,
                        "discount":discount,
                        "price_min": price_min,
                        "price_max":price_max,
                        "rating": rating,
                        "price": price,
                        "url" : urlx
                    
                    }
                    data.append(items)
                    
            else:
                print("hết page")
                check_page = False
                break
        except:
            time.sleep(60)
            print("vui lòng nhập captcha or  login account")
      
    return data
    


# async 
async def get_shop_and_item(shopid,itemid):
    time.sleep(1)
    page.set.load_mode.none()  # Set the load mode to none
    #api sản phẩm bán chạy  (lưu lại id shop để tý get vào shop lấy all thông tin)
    #https://shopee.vn/api/v4/pdp/get_rw?shop_id=395312479&item_id=12609480554&detail_level=0
    # chi tiết /api/v4/pdp/get_pc?
    page.listen.start('/api/v4/pdp/get_')
   
    url =  "https://shopee.vn/abc-i.{}.{}".format(shopid,itemid)
    page.get(url)  
    packet = page.listen.wait()  
    page.stop_loading()  
    response_body = packet.response.body
   
    # print(response_body)

    #info shop 
    data = []
    try:
        if(len(response_body['data'])):
        

            #item thì items
            # print(response_body['data']['item']['item_id'])
            # print(response_body['data']['item']['shop_id'])
            #brand
            # print(response_body['data']['item']['brand'])
            # #img
            # print(response_body['data']['item']['image'])
            # #mo ta
            # print(response_body['data']['item']['description'])

            # #shop
            # print(response_body['data']['shop_detailed']['name'])  
            # print(response_body['data']['shop_detailed']['account'])
            # print(response_body['data']['shop_detailed']['place'])
            # print(response_body['data']['shop_detailed']['rating_bad'])
            # print(response_body['data']['shop_detailed']['rating_good'])
            # print(response_body['data']['shop_detailed']['rating_normal'])
            # print(response_body['data']['shop_detailed']['rating_star'])
            # print(response_body['data']['shop_detailed']['item_count'])
            # print(response_body['data']['shop_detailed']['shop_location'])
            # print(response_body['data']['shop_detailed']['sold_total'])


            data_x = {
                "shopid": shopid,
                "itemid": itemid,
                "brand": (response_body['data']['item']['brand']),
                "image":(response_body['data']['item']['image']),
                "desscription":(response_body['data']['item']['description']),
                "name_shop":(response_body['data']['shop_detailed']['name'])  ,
                "place":(response_body['data']['shop_detailed']['place']) ,
                "rating_bad":(response_body['data']['shop_detailed']['rating_bad']),
                "rating_good":(response_body['data']['shop_detailed']['rating_good']),
                "rating_normal":(response_body['data']['shop_detailed']['rating_normal']),
                "rating_star":(response_body['data']['shop_detailed']['rating_star']),
                "item_count":(response_body['data']['shop_detailed']['item_count']),
                "shop_location":(response_body['data']['shop_detailed']['shop_location']),
                "sold_total":(response_body['data']['shop_detailed']['sold_total']),
                "urlshop":"https://shopee.vn/{}".format((response_body['data']['shop_detailed']['name']) )

            }

            data.append(data_x)
          
        return data
    except:
        print("antibot2")

        time.sleep(60)
        print("vui lòng nhập captcha")
      





async def run_main(page):
    csv_file_path = 'v.csv'
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  
        for row in reader:
            url, sub_dir, main_dir = row

            # Kiểm tra và tạo thư mục Thoi Trang Nam nếu chưa tồn tại
            if not os.path.exists(main_dir) :
                os.makedirs(main_dir)
                print(f"Thư mục '{main_dir}' đã được tạo.")    
                # lần đầu
            else:
                print(f"Thư mục '{main_dir}' đã tồn tại.")
                #các lần sau
                full_path =""

            
                if(sub_dir != "cate"):
                    full_path = os.path.join(main_dir, sub_dir)

         
            
                if not os.path.exists(full_path):
                    os.makedirs(full_path)

                    print(f"Thư mục con '{sub_dir}' trong '{main_dir}' đã được tạo.")

                        #tiến hành lấy data
                    print(row[0])

                    data = await get_cate_child_and_list_data_shop_sales(page,str(row[0]))

                    save_to_csv(os.path.join(full_path, "list_item.csv"), data)
                    # print('aaaaaaa',data)

                    for item in data:
                        data_shop = await get_shop_and_item(item['shopid'],item['itemid'])
                        # print(data_shop)
                        save_to_csv2(os.path.join(full_path, "data_shop.csv"), data_shop)
                        time.sleep(2)
                 
                    print("hoàn thành",sub_dir,main_dir)

               

if __name__ == "__main__":
    asyncio.run(run_main(page))