import logging
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, InlineQueryHandler
)
from .config import BOT_TOKEN
from .handlers import start, latest_cmd, latest_pager, job_detail, inline_query

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("jobbot")

async def error_handler(update, context):
    log.exception("Update error: %s", context.error)

def run():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN not set")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("latest", latest_cmd))

    app.add_handler(CallbackQueryHandler(latest_pager, pattern=r"^latest:"))
    app.add_handler(CallbackQueryHandler(job_detail, pattern=r"^job:"))
    app.add_handler(InlineQueryHandler(inline_query))
    app.add_error_handler(error_handler)

    log.info("Bot started.")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    run()
