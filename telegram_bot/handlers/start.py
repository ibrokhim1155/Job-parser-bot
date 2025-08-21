from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from ..config import BOT_USERNAME

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Salom! Men ish qidirishingizda yordamchi botman.\n\n"
        f"Qidirish uchun istalgan chatda:  @{BOT_USERNAME}\n"
        # "Yoki shu yerda:  /latest  so'nggi vakansiyalar.\n"
    )

    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🆕 So‘nggi vakansiyalar", callback_data="latest:page=1")],

        # # [InlineKeyboardButton("🆕 Latest (deep-link)", url=f"https://t.me/{BOT_USERNAME}?start=latest")]
    ])

    await update.message.reply_text(
        text,
        reply_markup=kb,
        disable_web_page_preview=True,
    )
