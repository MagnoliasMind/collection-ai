import requests
import csv
import os
import time

list_api = "https://summer.ospp.ac.cn/org/projectlist?lang=zh&pageNum=1&pageSize=50" 
detail_api = "https://summer.ospp.ac.cn/org/prodetail/26c280001?lang=zh&list=pro" 
outp = "ospp_2025_projects.csv"
pdf = "pdfs"
pages = 5  

def get_project_list(page=1, page_size=20):
    payload = {
        "page": page,
        "pageSize": page_size
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
    }
    resp = requests.post(list_api, json=payload, headers=headers, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    return data.get("data", {}).get("records", [])


def get_project_detail(project_id):
    params = {"id": project_id}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"
    }
    resp = requests.get(detail_api, params=params, headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.json().get("data", {})


def download_pdf(url, filename):
    if not url:
        return
    os.makedirs(pdf, exist_ok=True)
    filepath = os.path.join(pdf, filename)
    if os.path.exists(filepath):
        print(f"  exists {filename}")
        return
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        with open(filepath, "wb") as f:
            f.write(resp.content)
        print(f"download_pdf {filename}")
    except Exception as e:
        print(f" Exception: download_pdf {e}")


def main():
    all_projects = []

    for page in range(1, pages + 1):
        print(f"in {page}/{pages}")
        items = get_project_list(page=page)
        if not items:
            print("not items")
            break

        for item in items:
            project_id = item.get("id")
            name = item.get("name", "")
            difficulty = item.get("difficulty", "")
            tags = ", ".join(item.get("techTags", []))

            detail = {}
            try:
                detail = get_project_detail(project_id)
                time.sleep(2)
            except Exception as e:
                print(f"fetch  Exception({name}): {e}")

            description = detail.get("description", "")
            output_requirement = detail.get("outputRequirement", "")
            pdf_url = detail.get("proposalUrl", "")

            record = {
                "项目名": name,
                "项目难度": difficulty,
                "技术领域标签": tags,
                "项目简述": description,
                "项目产出要求": output_requirement,
                "PDF链接": pdf_url
            }
            all_projects.append(record)
            print(f" Yes {name} [{difficulty}]")

            if pdf_url:
                safe_name = name.replace("/", "_").replace("\\", "_")[:80]
                download_pdf(pdf_url, f"{safe_name}.pdf")

        time.sleep(5) 

    if all_projects:
        fieldnames = ["项目名", "项目难度", "技术领域标签", "项目简述", "项目产出要求", "PDF链接"]
        with open(outp, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_projects)
        print(f"\nsave {len(all_projects)} in {outp}")
    else:
        print("no save")


if __name__ == "__main__":
    main()