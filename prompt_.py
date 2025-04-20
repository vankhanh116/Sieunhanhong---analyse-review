

def get_system_prompt() -> str:
    template = """
        Dưới đây là các ví dụ về việc trích xuất chủ đề (topic) từ review:
        Review: "Áo thun rất mềm, mặc thoải mái"  
        Topics: ["chất liệu", "sự thoải mái"]

        Review: "Shop giao hàng quá lâu, tôi phải chờ 5 ngày"  
        Topics: ["giao hàng", "thời gian"]
        
        Review: "{review}"  
        Topics:
        """
    return template


