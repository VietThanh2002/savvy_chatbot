class PriceFormatter:
    def format_price(price):
        # Kiểm tra và lấy phần tử đầu tiên nếu price là danh sách hoặc tuple
        if isinstance(price, (list, tuple)):
            price = price[0]
        
        formatted_price = f"{price:,.0f}đ"
        return formatted_price.replace(",", ".")

    # Ví dụ sử dụng
    # price = [360000]  # Giả sử đây là danh sách trả về từ truy vấn
    # formatted_price = format_price(price)
    # print(formatted_price)  # Output: 360.000đ