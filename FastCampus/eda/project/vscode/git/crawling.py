# paperswithcode의 method/category/model 을 포함한 데이터셋 취득 (웹크롤)
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup 
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome()
driver.get('https://paperswithcode.com/methods')
data_list = []  
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

tmp1=4
while True: # 1,2번   
    try:
        click1_selector = f'body > div.container > div.container.content.content-buffer > div.infinite-container.featured-methods > div:nth-child({tmp1}) > div > h4 > a'
        temp_categories = driver.find_element(By.CSS_SELECTOR,click1_selector) #
    except NoSuchElementException:       
            break
    driver.execute_script("arguments[0].click();", temp_categories)
    tmp1 +=3
    time.sleep(1.5)
    
    # 클릭으로 인한 페이지 업데이트
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    method_selector = 'body > div.container.content.content-buffer > div > div.title.browse-methods-title > div:nth-child(2) > div > h1'
    method_name = soup.select(method_selector)
    if not method_name:
        break
    method = method_name[0].text.strip().replace('\n','')
    print('method: ',method)
    
    tmp2 = 3
    while True: # 3,4번
        try:
            click2_selector = f'body > div.container.content.content-buffer > div > div.infinite-container.featured-methods > div:nth-child({tmp2}) > a'
            temp_model = driver.find_element(By.CSS_SELECTOR,click2_selector)
        except NoSuchElementException: 
            break
        driver.execute_script("arguments[0].click();", temp_model)
        tmp2 += 3
        time.sleep(1.5)
        
        # 페이지 업데이트
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        #here
        category_selector = 'body > div.container.content.content-buffer > div.mobile-width > div.artefact-header > h1'
        category_name = soup.select(category_selector)
        if not category_name:
            break
        category = category_name[0].text.split("\xa0")[0].strip()
        print('category: ',category)

        model_list = []
        tmp3 = 1
        while True: # 5번
            model_selector = f'#methodsTable > tbody > tr:nth-child({tmp3}) > td:nth-child(1) > div.method-image > a'
            model_name = soup.select(model_selector) 
            if not model_name:
                break
            model = model_name[0].text.strip().replace('\n', '')
            model_list.append(model)
            print("model: ",model)
            tmp3 += 1
            
        data_list.append([method,category,', '.join(model_list)])
        
        driver.back()
    driver.back()

# 데이터를 CSV 파일로 저장
with open('cw_paperswithcode.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['method', 'category', 'model'])  # 헤더 추가
    csv_writer.writerows(data_list)  # 데이터 추가
