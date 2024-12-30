from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import pandas as pd

# 1. Khai báo biến Service với đường dẫn đến chromedriver của bạn
service = Service("C:/Users/Admin/Documents/chromedriver-win64/chromedriver.exe")


# 2. Khởi tạo browser
browser = webdriver.Chrome(service=service)

# 3. Mở Facebook và đăng nhập
browser.get("http://facebook.com")
txtUser = browser.find_element(By.ID, "email")
txtUser.send_keys("")  # Thay bằng email thật
txtPass = browser.find_element(By.ID, "pass")
txtPass.send_keys("") # thay pass
txtPass.send_keys(Keys.ENTER)

# 4. Đợi trang load xong
sleep(20)

# 5. Mở bài viết
browser.get("https://www.facebook.com/permalink.php?story_fbid=pfbid0TwJKKza7BB4oYi27aGDK5HjvtpqpuHjZza1XJdEka7ePhqw3W58TMZoFUmsw7weWl&id=100086902014121&__cft__[0]=AZXFzpqyuI2z3FRqXAOskLDvlEK-FrAGMz1QNgjFl6xhs0JXz7hi5eGJB7rSsoTN3Py2MTZVMCQJU3vd5JC3fGm7hgemMM3KJVSr4GcA-EOAu0GoQlLQoz_wP_FdC_KT9pSBHxyKmkmFYbaPCFcDAKqY5MFtjp6FO3JET0qLNo2CTiqBMKTNgaG40UnFDuRruppIw99KGOdG3j9diz1aBWsysSVxa7A3V8OPiYA0h73A4aN8y4Pc2TfLuvuz3yrEfs8&__tn__=%2CO%2CP-R")
sleep(20)  # Tăng thời gian chờ sau khi mở trang

# Lưu trữ dữ liệu
comments_data = []
seen_comments = set()

# Hàm cuộn và thu thập bình luận
def scroll_and_collect_comments():
    last_height = browser.execute_script("return document.body.scrollHeight")  # Lấy chiều cao hiện tại của trang
    while True:
        try:
            # Tìm tất cả các bình luận hiện tại
            comment_list = browser.find_elements(By.CSS_SELECTOR, ".x1n2onr6.x1ye3gou.x1iorvi4")
            for comment in comment_list:
                try:
                    # Lấy nội dung bình luận
                    content = comment.find_element(By.CSS_SELECTOR, ".xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x1vvkbs")
                    comment_text = content.text.strip()
                    
                    # Kiểm tra trùng lặp
                    if comment_text and comment_text not in seen_comments:
                        seen_comments.add(comment_text)
                        comments_data.append(comment_text)
                        print(comment_text)
                except Exception as e:
                    print("Lỗi khi lấy bình luận:", e)
                    continue

            # Cuộn xuống
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Cuộn xuống dưới cùng
            sleep(3)  # Đợi một chút để nội dung mới tải

            # Kiểm tra chiều cao mới của trang
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:  # Nếu chiều cao không thay đổi, không còn bình luận mới
                break
            last_height = new_height  # Cập nhật chiều cao

        except Exception as e:
            print("Lỗi trong quá trình cuộn:", e)
            break

# Gọi hàm cuộn và thu thập
scroll_and_collect_comments()

# Lưu bình luận vào file CSV
csv_path = "C:/Users/Admin/Documents/XU LY NGON NGU TU NHIEN HUST/NLP-main/crawler_facebook_comment-master/data.csv"
df = pd.DataFrame(comments_data, columns=["Comment"])
try:
    df.to_csv(csv_path, mode='a+', index=False, encoding="utf-8", header=False)
except FileNotFoundError:
    df.to_csv(csv_path, index=False, encoding="utf-8")

sleep(5)
# Đóng trình duyệt
browser.close()