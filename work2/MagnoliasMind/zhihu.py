import time
import random
import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


target = "https://www.zhihu.com/topic/19550517/hot"  
ques = 20     
ans = 10        
outp = "zhihu_data.csv"
cookie = "zhihu_cookies.txt"  

def create_driver():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
   
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    return driver


def login_zhihu(driver):
    if os.path.exists(cookie):
        print("Cookie")
        driver.get("https://www.zhihu.com")
        time.sleep(5)
        with open(cookie, "r") as f:
            cookies = eval(f.read())
        for cookie in cookies:
            try:
                driver.add_cookie(cookie)
            except Exception:
                pass
        driver.refresh()
        time.sleep(5)
        if driver.find_elements(By.CSS_SELECTOR, ".AppHeader-login"):
            print("No login_zhihu")
            manual_login(driver)
        else:
            print("Yes login_zhihu")
    else:
        manual_login(driver)


def manual_login(driver):
    print("\n" + "=" * 50)
    print("scan")
    print("=" * 50)
    driver.get("https://www.zhihu.com/signin")
    input() 
    cookies = driver.get_cookies()
    with open(cookie, "w") as f:
        f.write(str(cookies))
    print("Yes manual_login")


def scroll_to_load(driver, target_count, item_selector, timeout=60):
    loaded = []
    last_h = 0
    wait = WebDriverWait(driver, timeout)
    
    while len(loaded) < target_count:
        scroll_distance = random.randint(300, 700)
        driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
        time.sleep(random.uniform(1.5, 3.0))
        
        try:
            elements = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, item_selector))
            )
            new_items = [e for e in elements if e not in loaded]
            loaded.extend(new_items)
            print(f"  scroll_to_load {len(loaded)}/{target_count}")
        except Exception:
            print("Exception in  scroll_to_load")
            
        current_h = driver.execute_script("return document.body.scrollHeight")
        if current_h == last_h and len(loaded) < target_count:
            print("No")
            break
        last_h = current_h
        
    return loaded[:target_count]


def extract_text(element):
    try:
        return element.text.strip()
    except Exception:
        return ""


def crawl_topic(driver):
    results = []
    print(f"\nloading")
    driver.get(target)
    time.sleep(3)
    
    question_links = scroll_to_load(
        driver, ques, 
        ".ContentItem-title a[data-zop-question]"
    )
    print(f"共{len(question_links)}个问题链接")
   
    for idx, q_link in enumerate(question_links):
        print(f"\n处理第 {idx+1}/{len(question_links)}个问题")
        try:
            q_url = q_link.get_attribute("href")
            driver.get(q_url)
            time.sleep(random.uniform(2, 4))

            q_title = extract_text(driver.find_element(By.CSS_SELECTOR, "h1.QuestionHeader-title"))
            q_detail = ""
            try:
                detail_el = driver.find_element(By.CSS_SELECTOR, ".QuestionRichText-content")
                q_detail = extract_text(detail_el)
            except Exception:
                pass
            answers = scroll_to_load(
                driver, ans,
                ".ContentItem-answer .RichText"
            )
            
            for a_idx, answer in enumerate(answers):
                answer_text = extract_text(answer)
                if answer_text:
                    results.append({
                        "问题名": q_title,
                        "问题具体内容": q_detail,
                        "回答信息": answer_text
                    })
                    #print(f"  Yes {a_idx+1}")
                    
        except Exception as e:
            print(f"Exception: No : {e}")
            continue

        time.sleep(random.uniform(3, 6))
    
    return results


def save_to_csv(data, filename):
    if not data:
        print("no data")
        return
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["问题名", "问题具体内容", "回答信息"])
        writer.writeheader()
        writer.writerows(data)
    print(f"\nsave{len(data)} in {filename}")


def main():
    driver = None
    try:
        driver = create_driver()
        login_zhihu(driver)
        data = crawl_topic(driver)
        save_to_csv(data, outp)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt")
    except Exception as e:
        print(f"Exception {e}")
    finally:
        if driver:
            input("\n ok")
            driver.quit()


if __name__ == "__main__":
    main()