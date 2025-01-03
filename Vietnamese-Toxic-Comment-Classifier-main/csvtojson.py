import csv
import json

def make_json(csvFilePath, jsonFilePath):
    # Tạo một list để chứa dữ liệu
    data = []
    
    # Mở file CSV với mã hóa UTF-8 và xử lý BOM nếu có
    with open(csvFilePath, encoding='utf-8-sig') as csvf:
        csvReader = csv.DictReader(csvf)
        
        # Duyệt qua từng hàng và thêm vào list
        for rows in csvReader:
            print(rows)  # Kiểm tra từng hàng
            data.append(rows)  # Thêm từng hàng vào list

    # Mở file JSON để ghi dữ liệu
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        json.dump(data, jsonf, indent=4, ensure_ascii=False)
        
# Đường dẫn file CSV và JSON
csvFilePath = r'C:/Users/Admin/Documents/XU LY NGON NGU TU NHIEN HUST/NLP-main/crawler_facebook_comment-master/data.csv'
jsonFilePath = r'Names.json'

# Gọi hàm để chuyển đổi CSV sang JSON
make_json(csvFilePath, jsonFilePath)
