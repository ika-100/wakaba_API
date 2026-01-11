from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

user_memory = {}

class ChatRequest(BaseModel):
    user_id: str
    message: str

def wakaba_reply(message: str, user_id: str) -> str:
    EMPATHY = [
        "それはつらかったね。",
        "大変だったんだね。",
        "よく頑張ったと思う。",
        "無理しなくていいんだよ。"
    ]

    QUESTIONS = [
        "もう少し話してもいい？",
        "それって、いつ頃のこと？",
        "今はどんな気持ち？",
        "私でよければ聞くよ。"
    ]

    POSITIVE_WORDS = ["楽しい", "嬉しい", "よかった", "最高"]
    NEGATIVE_WORDS = ["疲れた", "つらい", "悲しい", "しんどい"]

    if user_id not in user_memory:
        user_memory[user_id] = message
        return f"そっか、{message}って言うんだね。よろしくね。"

    name = user_memory[user_id]

    if any(w in message for w in NEGATIVE_WORDS):
        return f"{name}、" + random.choice(EMPATHY) + random.choice(QUESTIONS)
    if any(w in message for w in POSITIVE_WORDS):
        return f"{name}、それはよかったね。" + random.choice(QUESTIONS)

    return f"{name}、うんうん。" + random.choice(QUESTIONS)

@app.post("/chat")
def chat(req: ChatRequest):
    reply = wakaba_reply(req.message, req.user_id)
    return {"reply": reply}
