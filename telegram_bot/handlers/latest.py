import math
from telegram import Update
from telegram.ext import ContextTypes
from ..config import PAGE_SIZE
from ..api_client import api_get
from ..keyboards import jobs_list_kb

def _page_meta(data: dict, page: int) -> tuple[int, bool]:
    count = data.get("count", 0)
    total_pages = math.ceil(count / PAGE_SIZE) if PAGE_SIZE else 1
    has_next = page < total_pages
    return count, has_next

async def latest_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    page = 1
    data = api_get("jobs/", params={"page": page})
    if not data:
        await update.message.reply_text("Hozircha ma'lumot yo‘q yoki API ishlamayapti.")
        return

    items = data.get("results", [])
    count, has_next = _page_meta(data, page)
    kb = jobs_list_kb(items, page, has_next)

    text_lines = [f"Topildi: *{count}* ta e'lon.  (page {page})"]
    for it in items:
        text_lines.append(f"• *{it['title']}* — _{it['company']}_")
    await update.message.reply_text(
        "\n".join(text_lines),
        parse_mode="Markdown",
        reply_markup=kb,
        disable_web_page_preview=True,
    )

async def latest_pager(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data_str = query.data  # e.g. "latest:page=2"
    try:
        page = int(data_str.split("page=")[1])
        if page < 1:
            page = 1
    except Exception:
        page = 1

    data = api_get("jobs/", params={"page": page})
    if not data:
        await query.edit_message_text("API xatosi yoki natija topilmadi.")
        return

    items = data.get("results", [])
    count, has_next = _page_meta(data, page)
    kb = jobs_list_kb(items, page, has_next)

    text_lines = [f"Topildi: *{count}* ta e'lon.  (page {page})"]
    for it in items:
        text_lines.append(f"• *{it['title']}* — _{it['company']}_")
    await query.edit_message_text(
        "\n".join(text_lines),
        parse_mode="Markdown",
        reply_markup=kb,
        disable_web_page_preview=True,
    )

async def job_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        job_id = int(query.data.split("job:")[1])
    except Exception:
        await query.edit_message_text("Noto‘g‘ri job ID.")
        return

    detail = api_get(f"jobs/{job_id}/")
    if not detail:
        await query.edit_message_text("Ma'lumot topilmadi")
        return

    text = (
        f"*{detail.get('title','') }* — _{detail.get('company','')}_\n\n"
        f"{detail.get('url','')}\n"
        f"Posted: `{detail.get('posted_at','')}`"
    )
    await query.edit_message_text(
        text, parse_mode="Markdown", disable_web_page_preview=True
    )
