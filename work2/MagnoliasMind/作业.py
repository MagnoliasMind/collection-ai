import requests
from bs4 import BeautifulSoup
import re
import time
import csv
import os
from urllib.parse import urljoin, urlparse

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}
Attach_dir = "教务通知"
os.makedirs(Attach_dir,exist_ok = True)
CSV_file = "教务通知2.0.csv"



def clean_text (text):
    if not text:
        return ""
    text = re.sub(r"\s+","",text)
    return text.strip()
    
def get_attach_info(attach_url, attach_name):
   
    try:
        full_attach_url = urljoin("https://jwch.fzu.edu.cn/", attach_url)
        attach_path = urlparse(full_attach_url).path
        attach_code = attach_path.split("/")[-1].split(".")[0] if attach_path else ""
       
        download_count = re.findall(r"downloads=(\d+)", full_attach_url)
        download_count = download_count[0] if download_count else "0"
        
        return {
            "附件名": clean_text(attach_name),
            "附件下载次数": download_count
        }
    except Exception as e:
        print(f"提取附件信息失败【{attach_name}】：{str(e)[:50]}")
        return {
            "附件名": clean_text(attach_name),
            "附件下载次数": "0"
        }
def parse_noti_det(detail_url, notice_title):
    try:
        response = requests.get(detail_url, headers=headers, timeout=20)
        response.encoding = "utf-8"
        
        soup = BeautifulSoup(response.text, "html.parser")
        attachments = []
        
        attach_tags = soup.find_all("a", href=re.compile(r"\.(pdf|doc|xlsx)"))
        
        
        for tag in attach_tags:
            attach_name = tag.get_text(strip=True) or f"未命名附件_{len(attachments)+1}"
            attach_href = tag.get("href")
            if attach_href:
                
                attach_info = get_attach_info(attach_href, attach_name)
                attachments.append(attach_info)
        
        return {
            "附件列表": attachments  
        }
    except Exception as e:
        print(f"详情页解析失败【{detail_url}】：{str(e)[:50]}")
        return {"附件列表": []}


def parse_single_page(page_url):
    try:
        response = requests.get(page_url, headers=headers, timeout=10)
        if response.status_code == 404:
            return []
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "html.parser")
        
        all_items = soup.find_all("li")
        page_notices = []
        
        for item in all_items:
            try:
               
                date_tag = item.find("span", class_="doclist_time")
                date = clean_text(date_tag.get_text()) if date_tag else ""
                
              
                item_text = item.get_text(strip=True)
                publisher = ""
                if "【" in item_text and "】" in item_text:
                    publisher = item_text.split("】")[0].split("【")[-1]
                publisher = clean_text(publisher)
                
               
                title_tag = item.find("a")
                title = clean_text(title_tag.get_text()) if title_tag else ""
                detail_href = title_tag.get("href") if title_tag else ""
                detail_url = f"https://jwch.fzu.edu.cn/{detail_href}" if detail_href else ""
                
                
                if not (title and date and detail_url):
                    continue
                
                
                detail_info = parse_noti_det(detail_url, title)
                
               
                attach_names = []
                attach_counts = []
                for attach in detail_info["附件列表"]:
                    attach_names.append(attach["附件名"])
                    attach_counts.append(attach["附件下载次数"])
                
               
                notice_data = {
                    "通知人": publisher,
                    "标题": title,
                    "日期": date,
                    "附件名": "|".join(attach_names),
                    "附件下载次数": "|".join(attach_counts),
                }
                page_notices.append(notice_data)
                
                time.sleep(0.5)  
            except Exception as e:
                print(f"单条通知解析失败：{str(e)[:50]}")
                continue
        return page_notices
    except Exception as e:
        print(f"页面解析失败【{page_url}】：{str(e)[:50]}")
        return []

    
def never_gonna_give_a_page_up(target_page = 10):  
    all_notices = [] 
    cur_page = 1      
    
   
    while cur_page <= target_page:
        page_url = f"https://jwch.fzu.edu.cn/gsgg/{cur_page}.htm"
       
        print(f"\n---------- 爬第{cur_page}页（累计{len(all_notices)}条）----------")
        
       
        page_notices = parse_single_page(page_url)
        if not page_notices:
            print(f"第{cur_page}页空的，继续爬下一页~")  
        else:
            all_notices.extend(page_notices)
        
        cur_page += 1  
        time.sleep(1)
    

    print(f"\n已爬完了{target_page}页，共{len(all_notices)}条。下班（^-^)！")
    
    return all_notices

def save_to_csv(notices):
    
    if not notices:
        print(" 无数据可保存！")
        return
    
   
    fieldnames = [
        "通知人", "标题", "日期", 
        "附件名", "附件下载次数"
    ]
    
    
    with open(CSV_file, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()  
        writer.writerows(notices)  
    
    print(f"\n数据已保存到：{CSV_file}")
    print(f"共{len(notices)}条通知")
    
    total_attach = sum(len(notice["附件名"].split("|")) for notice in notices if notice["附件名"])
    print(f"共{total_attach}个附件")
    
if __name__ == "__main__":
    
    test_url = "https://jwch.fzu.edu.cn/gsgg.htm"
    test_response = requests.get(test_url, headers=headers, timeout=10)
    if test_response.status_code != 200:
        print("无法访问福大教务网")
    else:
        print("成功连接,开始爬...")
        
        all_notices = never_gonna_give_a_page_up(target_page=10)
        
        save_to_csv(all_notices)