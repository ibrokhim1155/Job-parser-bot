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
        line = f"• *{it['title']}* — _{it['company']}_"
        if it.get("location_country"):
            line += f" ({it['location_country']})"
        if it.get("job_type"):
            line += f" [{it['job_type']}]"
        text_lines.append(line)

    await update.message.reply_text(
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
        f"Posted: `{detail.get('posted_at','')}`\n"
    )
    if detail.get("location_country"):
        text += f"{detail['location_country']}\n"
    if detail.get("job_type"):
        text += f"{detail['job_type']}\n"

    await query.edit_message_text(
        text, parse_mode="Markdown", disable_web_page_preview=True
    )
