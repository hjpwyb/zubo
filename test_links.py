import requests

INPUT_FILE = "live.txt"
VALID_FILE = "valid_links.txt"
INVALID_FILE = "invalid_links.txt"

def extract_links(file_path):
    """提取链接"""
    links = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("http://") or line.startswith("https://"):
                links.append(line.split("$")[0])  # 去掉结尾标记
    return links

def test_link(link):
    """测试链接是否有效"""
    try:
        response = requests.head(link, timeout=10)
        return response.status_code == 200
    except requests.RequestException:
        return False

def save_results(valid_links, invalid_links):
    """保存测试结果"""
    with open(VALID_FILE, "w", encoding="utf-8") as vf:
        vf.write("\n".join(valid_links))
    with open(INVALID_FILE, "w", encoding="utf-8") as ivf:
        ivf.write("\n".join(invalid_links))

def main():
    print("开始提取链接...")
    links = extract_links(INPUT_FILE)
    print(f"共找到 {len(links)} 个链接，开始测试...")

    valid_links = []
    invalid_links = []

    for link in links:
        if test_link(link):
            valid_links.append(link)
        else:
            invalid_links.append(link)
        print(f"测试: {link} - {'有效' if link in valid_links else '无效'}")

    print("测试完成，正在保存结果...")
    save_results(valid_links, invalid_links)
    print(f"有效链接: {len(valid_links)} 条")
    print(f"无效链接: {len(invalid_links)} 条")

if __name__ == "__main__":
    main()
