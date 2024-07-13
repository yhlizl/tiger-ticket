import json
from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys



def save_cookies(driver, location):
    json.dump(driver.get_cookies(), open(location, 'w'))

def load_cookies(driver, location, url=None):
    if url is not None:
        driver.get(url)
    cookies = json.load(open(location))
    for cookie in cookies:
        driver.add_cookie(cookie)



# 讀取配置文件
with open('config.json', 'r') as f:
    config = json.load(f)

from selenium.webdriver.common.by import By
# 登入
def login(driver, username, password):
    # 嘗試載入 cookies
    try:
        load_cookies(driver, 'cookies.json', config['login_url'])
        print('載入 cookies 成功')
    except:
        print('載入 cookies 失敗，正在嘗試登入')
        # 打開登入頁面
        driver.get(config['login_url'])
        sleep(1)
        # 等待帳號輸入框出現並輸入帳號
        username_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div[2]/form/div/label[1]/div/div/div/input')))
        username_input.send_keys(username)
        sleep(1)
        # 等待密碼輸入框出現並輸入密碼
        password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div[2]/form/div/label[2]/div/div/div/input')))
        password_input.send_keys(password)
        sleep(1)
        # 等待登入按鈕出現並點擊
        login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/main/div/div[2]/form/div/div/button/span[2]')))
        login_button.click()
        sleep(20)
        print('登入成功')
        # 保存 cookies
        save_cookies(driver, 'cookies.json')

def search_ticket(driver):
    # 打開搜尋頁面
    driver.get(config['url'])
    sleep(1)

    # 根據 config['return_date'] 的值選擇不同的 XPath
    if config['return_date'] == "":
        xpath = '/html/body/div[1]/div/div/div[1]/div[2]/section[1]/div/div/div[2]/div[1]/form/div/fieldset[1]/div/div[2]/div[2]/label'
        print("選擇單程")
    else:
        xpath = '/html/body/div[1]/div/div/div[1]/div[2]/section[1]/div/div/div[2]/div[1]/form/div/fieldset[1]/div/div[2]/div[1]/label'
        print("選擇往返")
    # 等待元素出現並點擊
    is_return = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    is_return.click()

    # 出發的城市點擊下拉選單以打開選項
    dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/section[1]/div/div/div[2]/div[1]/form/div/fieldset[2]/div/div/div/div[1]')))
    dropdown.click()

    # 找到輸入框並輸入你的出發的城市
    input_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/section[1]/div/div/div[2]/div[1]/form/div/fieldset[2]/div/div/div/div[2]/input')))
    input_field.send_keys(config["departure"])

    # 按下Enter鍵來提交你的出發的城市
    input_field.send_keys(Keys.RETURN)
    # 點擊目的城市的下拉選單以打開選項
    destination_dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/section[1]/div/div/div[2]/div[1]/form/div/fieldset[3]/div/div/div/div[1]')))
    destination_dropdown.click()

    # 找到輸入框並輸入你的目的城市
    destination_input_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/section[1]/div/div/div[2]/div[1]/form/div/fieldset[3]/div/div/div/div[2]/input')))
    destination_input_field.send_keys(config["destination"])

    # 按下Enter鍵來提交你的目的城市
    destination_input_field.send_keys(Keys.RETURN)
    # 找到日期選擇器的元件，並點擊它以打開日期選擇器
    date_picker = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/section[1]/div/div/div[2]/div[1]/form/div/div/div/div/button')))
    date_picker.click()

    # 在日期選擇器中找到對應的日期元件
    # 注意：這裡假設你的 config["departure_date"] 是一個格式為 "m/d/yyyy" 的字串
    date_element_xpath = f'/html/body/div[1]/div/div/div[1]/div[2]/section[1]/div/div/div[2]/div[1]/form/div/div[1]/div/div/div//div[@aria-label="{config["departure_date"]}"]/span'    
    date_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, date_element_xpath)))
    print("找到日期元件")
    # 使用 JavaScript 來點擊該日期元件
    driver.execute_script("arguments[0].click();", date_element)
    print("點擊日期元件")

    if (config['return_date'] != ""):
        # 找到日期選擇器的元件，並點擊它以打開日期選擇器
        date_picker = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/section[1]/div/div/div[2]/div[1]/form/div/div[2]/div/div/button')))
        date_picker.click()
        # 在日期選擇器中找到對應的日期元件
        # 注意：這裡假設你的 config["return_date"] 是一個格式為 "m/d/yyyy" 的字串
        return_date_element_xpath = '/html/body/div[1]/div/div/div[1]/div[2]/section[1]/div/div/div[2]/div[1]/form/div/div[2]/div/div/div//div[@aria-label="' + config["return_date"] + '"]/span'
        return_date_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, return_date_element_xpath)))
        # 使用 JavaScript 來點擊該日期元件
        driver.execute_script("arguments[0].click();", return_date_element)
    # 找到乘客數量選擇器的元件，並點擊它以打開選擇器
    passenger_picker = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/section[1]/div/div/div[2]/div[1]/form/div/fieldset[4]/div/div/button')))
    passenger_picker.click()

    # 獲取當前的乘客數量
    current_ticket_count_xpath = '/html/body/div[1]/div/div/div[1]/div[2]/section[1]/div/div/div[2]/div[1]/form/div/fieldset[4]/div/div/ul/li[1]/div/div/output'
    current_ticket_count = int(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, current_ticket_count_xpath))).text)

    # 根據 config["ticket_count"] 的值調整乘客數量
    while current_ticket_count != config["ticket_count"]:
        if current_ticket_count < config["ticket_count"]:
            # 如果當前的乘客數量過少，則點擊增加按鈕
            increase_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/section[1]/div/div/div[2]/div[1]/form/div/fieldset[4]/div/div/ul/li[1]/div/div/button[2]')))
            increase_button.click()
        else:
            # 如果當前的乘客數量過多，則點擊減少按鈕
            decrease_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/section[1]/div/div/div[2]/div[1]/form/div/fieldset[4]/div/div/ul/li[1]/div/div/button[1]')))
            decrease_button.click()

        # 更新當前的乘客數量
        current_ticket_count = int(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, current_ticket_count_xpath))).text)
    print(("乘客數量調整完成"))
    # 點擊其他空白處關閉下拉選單
    # 找到頁面的 body 元件
    body = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body')))
    

    # 使用 JavaScript 來點擊 body 元件
    driver.execute_script("arguments[0].click();", body)
    # 找到優惠代碼的輸入框
    promo_code_input_field_xpath = '/html/body/div[1]/div/div/div[1]/div[2]/section[1]/div/div/div[2]/div[1]/form/div/fieldset[5]/div/input'
    promo_code_input_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, promo_code_input_field_xpath)))

    # 輸入你的優惠代碼
    promo_code_input_field.send_keys(config["promo_code"])
    # 找到開始搜尋航班的按鈕
    search_button_xpath = '/html/body/div[1]/div/div/div[1]/div[2]/section[1]/div/div/div[2]/div[1]/form/div/button'
    search_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, search_button_xpath)))

    # 點擊開始搜尋航班的按鈕
    search_button.click()
    

def get_cheapest_ticket(driver):
    # 等待搜尋結果頁面出現
    # 切換到新的分頁
    driver.switch_to.window(driver.window_handles[-1])
    print(driver.current_url)  # 打印當前頁面的 URL
    print(driver.title)  # 打印當前頁面的標題
    # 找到所有的 div 子元素
    print("等待搜尋結果頁面出現")
    next_button_xpath = '/html/body/div[1]/div/div[1]/footer/div/div[2]/button[2]/span[2]/span'
    WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.XPATH, next_button_xpath)))
    print("搜尋結果頁面出現")
    div_elements_xpath = '/html/body/div[1]/div/div[1]/div/main/div[2]/div[1]/div/div[@data-e2e-test-id]'
    WebDriverWait(driver, 300).until(EC.presence_of_all_elements_located((By.XPATH, div_elements_xpath)))
    div_elements = driver.find_elements(By.XPATH, div_elements_xpath)
    print(("找到去程機票", len(div_elements), "張"))
    # 遍歷 div 子元素
    for div_element in div_elements:
        # 等待時間元素出現
        time_xpath = './div[3]/div[2]/div[1]/div[1]/div/div[1]/div[1]'
        WebDriverWait(div_element, 10).until(EC.presence_of_element_located((By.XPATH, time_xpath)))
        # 獲取時間
        time_element = div_element.find_element(By.XPATH, time_xpath)
        time = time_element.text


        # 獲取價格
        price_xpath ='./div[3]/div[2]/div[2]/button/span[2]/div/div[1]/div/div/div/div[2]'
        WebDriverWait(div_element, 10).until(EC.presence_of_element_located((By.XPATH, price_xpath)))
        price_element = div_element.find_element(By.XPATH, price_xpath)
        price = price_element.text
        print(f'Time: {time}, Price: {price}')
# 購買機票
def buy_tickets(driver, ticket_count):
    # 這裡需要根據你的實際情況來填寫
    pass


options = webdriver.ChromeOptions()
options.add_argument("--incognito")  # 啟用無痕模式
# options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1024,768")
# 創建一個新的WebDriver實例
driver = webdriver.Chrome(options=options,service=Service(ChromeDriverManager().install()))
# 登入
login(driver, config['username'], config['password'])

# 搜索機票
search_ticket(driver)

# 等待新的分頁打開
WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

# 選最便宜的機票
get_cheapest_ticket(driver)

# 購買機票
# buy_tickets(driver, config['ticket_count'])
sleep(40)
# 關閉WebDriver實例
driver.quit()