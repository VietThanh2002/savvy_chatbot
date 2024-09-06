class PriceFormatter:
    @staticmethod
    def format_price(price):
        formatted_price = "{:,.0f}".format(price)  # Định dạng giá tiền với comma ngăn cách hàng nghìn và không có phần thập phân
        formatted_price += " ₫"  # Thêm ký hiệu VNĐ vào cuối giá tiền
        return formatted_price
