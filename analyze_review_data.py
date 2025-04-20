import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Đường dẫn đến file Excel
file_path = r"D:\Download\order_report_200.csv.xlsx"

df = pd.read_excel(file_path)

# Tính tổng tiền
df["total"] = df["price"] * df["quantity"]

# Gán nhãn cảm xúc theo rating
def label_sentiment(rating):
    if rating >= 4:
        return "positive"
    elif rating == 3:
        return "neutral"
    else:
        return "negative"

df["sentiment"] = df["rating"].apply(label_sentiment)

# Thiết lập style cho biểu đồ
sns.set(style="whitegrid")

# ===== 1. Biểu đồ phân phối rating =====
plt.figure(figsize=(6, 4))
sns.countplot(x="rating", data=df, hue="rating", palette="coolwarm", legend=False)
plt.title("Phân phối mức đánh giá (Rating)")
plt.xlabel("Rating")
plt.ylabel("Số lượng")
plt.tight_layout()
plt.savefig("rating_distribution.png")  # Lưu ảnh vào thư mục hiện tại
plt.close()
