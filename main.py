from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

# Load environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
AUTHORIZED_USER_ID = int(os.getenv("AUTHORIZED_USER_ID"))

app = FastAPI()
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

# ===== COMMAND HANDLERS =====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id != AUTHORIZED_USER_ID:
        await update.message.reply_text("❌ Access denied.")
        return
    
    await update.message.reply_text("🚀 SYC PILOT is LIVE!")

async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📍 Requesting phone location...")

async def battery(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔋 Checking battery status...")

async def ring(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔔 Ringing phone...")

async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📸 Taking photo...")

async def lock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔒 Locking phone...")

async def sos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🆘 SOS Alert Sent!")

# ===== REGISTER COMMANDS =====
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("location", location))
telegram_app.add_handler(CommandHandler("battery", battery))
telegram_app.add_handler(CommandHandler("ring", ring))
telegram_app.add_handler(CommandHandler("photo", photo))
telegram_app.add_handler(CommandHandler("lock", lock))
telegram_app.add_handler(CommandHandler("sos", sos))

# ===== START TELEGRAM BOT =====
@app.on_event("startup")
async def startup():
    await telegram_app.initialize()

# ===== TELEGRAM WEBHOOK =====
@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"ok": True}