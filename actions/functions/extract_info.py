import re

def extract_email_and_phone(message):
      # Regex cho địa chỉ email
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    # Regex cho số điện thoại bắt đầu với 0 và có 10 chữ số
    phone_pattern = r'\b0\d{9}\b'
    
    email = re.search(email_pattern, message)
    phone = re.search(phone_pattern, message)
    
    return email.group(), phone.group()

# Ví dụ sử dụng
# message = "Bạn có thể liên hệ tôi qua email vthanhb2014610@gmail.com hoặc số điện thoại 0767957642."
# emails, phones = extract_email_and_phone(message)

# print("Email:", emails)
# print("Số điện thoại:", phones)