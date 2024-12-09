import requests
import concurrent.futures

# 输入文件路径和输出文件路径
input_file = "links.txt"  # 存放所有链接
valid_links_file = "valid_links.txt"  # 存放有效链接
invalid_links_file = "invalid_links.txt"  # 存放无效链接

def test_link(link):
    """测试单个链接是否有效"""
    try:
        response = requests.get(link, timeout=5)  # 设置超时为 5 秒
        # RTP 流可能不会返回标准 HTTP 状态码，这里简单判断连接是否成功
        if response.status_code == 200 or response.content:
            return link, True
    except requests.exceptions.RequestException:
        pass
    return link, False

def main():
    # 加载链接
    with open(input_file, "r") as f:
        links = [line.strip() for line in f if line.strip()]
    
    valid_links = []
    invalid_links = []
    
    # 使用线程池并发测试链接
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        future_to_link = {executor.submit(test_link, link): link for link in links}
        for future in concurrent.futures.as_completed(future_to_link):
            link, is_valid = future.result()
            if is_valid:
                valid_links.append(link)
            else:
                invalid_links.append(link)
    
    # 保存结果
    with open(valid_links_file, "w") as f:
        f.write("\n".join(valid_links))
    
    with open(invalid_links_file, "w") as f:
        f.write("\n".join(invalid_links))
    
    print(f"测试完成：有效链接 {len(valid_links)} 条，无效链接 {len(invalid_links)} 条")

if __name__ == "__main__":
    main()
