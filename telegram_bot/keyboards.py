from typing import List, Tuple
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def jobs_list_kb(items: List[dict], page: int, has_next: bool) -> InlineKeyboardMarkup:
    rows = []
    for item in items:
        title = item.get("title", "Job")
        url = item.get("url")
        job_id = item.get("id")
        rows.append([
            InlineKeyboardButton(text=title[:32], callback_data=f"job:{job_id}"),
            InlineKeyboardButton(text="Open", url=url) if url else InlineKeyboardButton(text="Detail", callback_data=f"job:{job_id}")
        ])

    pager = []
    if page > 1:
        pager.append(InlineKeyboardButton("« Prev", callback_data=f"latest:page={page-1}"))
    if has_next:
        pager.append(InlineKeyboardButton("Next »", callback_data=f"latest:page={page+1}"))
    if pager:
        rows.append(pager)

    return InlineKeyboardMarkup(rows)
