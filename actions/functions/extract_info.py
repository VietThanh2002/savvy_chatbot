import re

def extract_email_phone_order(message):
    # Regex cho địa chỉ email
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    # Regex cho số điện thoại bắt đầu với 0 và có 10 chữ số
    # phone_pattern = r'\b0\d{9}\b'
    
    # Regex cho mã đơn hàng là số nguyên bắt đầu từ 1 (không bắt đầu bằng 0)
    order_pattern = r'\b[1-9]\d*\b'

    emails = re.findall(email_pattern, message)
    # phones = re.findall(phone_pattern, message)
    orders = re.findall(order_pattern, message)

    return emails, phones, orders

# Ví dụ sử dụng
message = "Đơn hàng của tôi là 1223124124 123456 và bạn có thể liên hệ qua email vthanhb2014610@gmail.com hoặc số điện thoại 0767957642."
emails, phones, orders = extract_email_phone_order(message)

print("Email:", emails)
# print("Số điện thoại:", phones)
print("Mã đơn hàng:", orders)