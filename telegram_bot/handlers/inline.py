import math
from uuid import uuid4
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import ContextTypes
from ..config import PAGE_SIZE
from ..api_client import api_get

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query.strip()
    try:
        page = int(update.inline_query.offset or "1")
        if page < 1:
            page = 1
    except ValueError:
        page = 1

    params = {"page": page}
    if query:
        params["search"] = query

    data = api_get("jobs/", params=params)
    results = []
    if data:
        for item in data.get("results", []):
            detail = api_get(f"jobs/{item['id']}/") or item
            text = (
                f"*{detail.get('title','')}* — _{detail.get('company','')}_\n\n"
                f"{detail.get('url','')}\n"
                f"Posted: `{detail.get('posted_at','')}`"
            )
            results.append(
                InlineQueryResultArticle(
                    id=str(uuid4()),
                    title=f"{item.get('title','')} — {item.get('company','')}",
                    input_message_content=InputTextMessageContent(
                        text, parse_mode="Markdown", disable_web_page_preview=True
                    ),
                    description=item.get("url",""),
                )
            )

    next_offset = ""
    if data:
        count = data.get("count", 0)
        total_pages = math.ceil(count / PAGE_SIZE) if PAGE_SIZE else 1
        if page < total_pages:
            next_offset = str(page + 1)

    await update.inline_query.answer(
        results,
        cache_time=5,
        is_personal=True,
        next_offset=next_offset,
    )
