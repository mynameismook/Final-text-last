# sentiment_model.py

from pythainlp.tokenize import word_tokenize

def predict_sentiment(text):
    words = word_tokenize(text, engine='newmm')  # ใช้ newmm ในการตัดคำ

    positive_words = ["ชอบ", "ดี", "อร่อย", "เยี่ยม", "ฟิน", "สุดยอด"]
    negative_words = ["ไม่ชอบ", "แย่", "ห่วย", "แย่มาก", "ขม", "เลี่ยน"]

    pos = any(word in words for word in positive_words)
    neg = any(word in words for word in negative_words)

    if pos and not neg:
        return "บวก"
    elif neg and not pos:
        return "ลบ"
    elif pos and neg:
        return "กลาง"
    else:
        return "กลาง"
