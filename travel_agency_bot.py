from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
)
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    Defaults,
)
import os

# ==============================
# ✅ CONFIG
# ==============================
# 1) Put your BotFather token here OR set environment variable TELEGRAM_BOT_TOKEN
TOKEN = os.getenv("angelswingsint", "7405344536:AAFWG9yaSc-Wt_-j26YowynR4S6ujZjrQPc")

# 2) Agency info (edit as needed)
AGENCY = {
    "name": "Angel's Wings",
    "phone": "+880101641591041",
    "whatsapp": "+8801977802655",
    "email": "angelswingsshanto@gmail.com",
    "address_bn": "বাসাতি কনডোমিনিয়াম (৩য় তলা), বাড়ি ১৫, রোড ১৭, বনানী সি/এ, ঢাকা-১২১৩, বাংলাদেশ",
    # Optional Google Maps link (edit with your exact map link if you have one)
    "maps": "https://maps.google.com/?q=Basati+Condominium,+House+15,+Road+17,+Banani+C/A,+Dhaka+1213",
}

# 3) Sample media / images (replace with your own hosted URLs)
IMAGES = {
    "banner": "https://images.unsplash.com/photo-1502920917128-1aa500764b8a",  # airplane wing
    "thailand": "https://images.unsplash.com/photo-1519125323398-675f0ddb6308",
    "malaysia": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee",
    "dubai": "https://images.unsplash.com/photo-1505764706515-aa95265c5abc",
}

# ==============================
# 🌐 Simple i18n (Bangla/English)
# ==============================

def t(key: str, lang: str = "bn") -> str:
    texts = {
        "welcome_bn": """
<b>👋 স্বাগতম {name}!</b>\nআমাদের প্রফেশনাল ট্রাভেল এজেন্সি বটে আপনাকে স্বাগতম।\nনিচের মেনু থেকে একটি অপশন বাছাই করুন।
""",
        "welcome_en": """
<b>👋 Welcome {name}!</b>\nWelcome to our professional travel agency bot.\nPlease choose an option from the menu below.
""",
        "menu_bn": "মেনু",
        "menu_en": "Menu",
        "flight_bn": "✈️ ফ্লাইট ইনফো",
        "flight_en": "✈️ Flight Info",
        "hotel_bn": "🏨 হোটেল বুকিং",
        "hotel_en": "🏨 Hotel Booking",
        "tour_bn": "🌴 ট্যুর প্যাকেজ",
        "tour_en": "🌴 Tour Packages",
        "visa_bn": "🛂 ভিসা ইনফো",
        "visa_en": "🛂 Visa Info",
        "address_bn": "🏢 ঠিকানা",
        "address_en": "🏢 Address",
        "contact_bn": "📞 যোগাযোগ",
        "contact_en": "📞 Contact Us",
        "language_bn": "🌐 Language / ভাষা",
        "flight_text_bn": (
            "<b>✈️ আমাদের ফ্লাইট ডিল:</b>\n\n"
            "• ঢাকা → দুবাই (OW): <b>BDT 35,000</b> থেকে\n"
            "• ঢাকা → ব্যাংকক (RT): <b>BDT 28,500</b> থেকে\n"
            "• ঢাকা → কুয়ালালামপুর (RT): <b>BDT 26,000</b> থেকে\n\n"
            "বুকিংয়ের জন্য যোগাযোগ করুন: {phone} / WhatsApp: {whatsapp}"
        ),
        "flight_text_en": (
            "<b>✈️ Our Flight Deals:</b>\n\n"
            "• Dhaka → Dubai (OW): <b>from BDT 35,000</b>\n"
            "• Dhaka → Bangkok (RT): <b>from BDT 28,500</b>\n"
            "• Dhaka → Kuala Lumpur (RT): <b>from BDT 26,000</b>\n\n"
            "For booking, contact: {phone} / WhatsApp: {whatsapp}"
        ),
        "hotel_text_bn": (
            "<b>🏨 হোটেল বুকিং:</b>\n\n"
            "• Bangkok Grand Hotel — <b>BDT 5,000/night</b>\n"
            "• Dubai Luxury Inn — <b>BDT 8,000/night</b>\n"
            "• Kuala Star Suites — <b>BDT 6,200/night</b>\n\n"
            "লোকেশন ও কনফার্মেশনের জন্য ইনবক্স করুন।"
        ),
        "hotel_text_en": (
            "<b>🏨 Hotel Booking:</b>\n\n"
            "• Bangkok Grand Hotel — <b>BDT 5,000/night</b>\n"
            "• Dubai Luxury Inn — <b>BDT 8,000/night</b>\n"
            "• Kuala Star Suites — <b>BDT 6,200/night</b>\n\n"
            "Message us for location and confirmation."
        ),
        "tour_text_bn": (
            "<b>🌴 ট্যুর প্যাকেজ:</b>\nআপনার পছন্দের দেশের প্যাকেজ দেখতে নিচের বাটনগুলো ব্যবহার করুন।"
        ),
        "tour_text_en": (
            "<b>🌴 Tour Packages:</b>\nUse the buttons below to view packages by destination."
        ),
        "visa_text_bn": (
            "<b>🛂 ভিসা ইনফো:</b>\n\n"
            "• Thailand Tourist Visa — <b>BDT 4,500</b> | Processing: 5–7 days\n"
            "• Malaysia Tourist Visa — <b>BDT 6,000</b> | Processing: 5–10 days\n"
            "• UAE (Dubai) Tourist Visa — <b>BDT 8,000</b> | Processing: 3–5 days\n"
            "• Singapore Tourist Visa — <b>BDT 9,500</b> | Processing: 7–10 days\n\n"
            "নোট: ডকুমেন্টস ও ফি পরিবর্তন হতে পারে — ইনবক্সে কনফার্ম করুন।"
        ),
        "visa_text_en": (
            "<b>🛂 Visa Info:</b>\n\n"
            "• Thailand Tourist Visa — <b>BDT 4,500</b> | Processing: 5–7 days\n"
            "• Malaysia Tourist Visa — <b>BDT 6,000</b> | Processing: 5–10 days\n"
            "• UAE (Dubai) Tourist Visa — <b>BDT 8,000</b> | Processing: 3–5 days\n"
            "• Singapore Tourist Visa — <b>BDT 9,500</b> | Processing: 7–10 days\n\n"
            "Note: Docs & fees may change — please confirm in chat."
        ),
        "address_text_bn": (
            "<b>🏢 আমাদের ঠিকানা:</b>\n{address}\n\n"
            "📍 Google Maps: {maps}"
        ),
        "address_text_en": (
            "<b>🏢 Our Address:</b>\n{address}\n\n"
            "📍 Google Maps: {maps}"
        ),
        "contact_text_bn": (
            "<b>📞 যোগাযোগ:</b>\n"
            "• ফোন: {phone}\n"
            "• WhatsApp: {whatsapp}\n"
            "• ইমেইল: {email}"
        ),
        "contact_text_en": (
            "<b>📞 Contact Us:</b>\n"
            "• Phone: {phone}\n"
            "• WhatsApp: {whatsapp}\n"
            "• Email: {email}"
        ),
        "tour_buttons_bn": [
            ("🇹🇭 থাইল্যান্ড", "tour_th"),
            ("🇲🇾 মালয়েশিয়া", "tour_my"),
            ("🇦🇪 দুবাই", "tour_ae"),
        ],
        "tour_buttons_en": [
            ("🇹🇭 Thailand", "tour_th"),
            ("🇲🇾 Malaysia", "tour_my"),
            ("🇦🇪 Dubai", "tour_ae"),
        ],
        "back_bn": "⬅️ ব্যাক",
        "back_en": "⬅️ Back",
    }
    return texts.get(f"{key}_{lang}", texts.get(key, key))


# ==============================
# 🧠 Helpers
# ==============================

def lang_of(user_data: dict) -> str:
    return user_data.get("lang", "bn")


def main_menu_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t("flight", lang), callback_data="flight")],
        [InlineKeyboardButton(t("hotel", lang), callback_data="hotel")],
        [InlineKeyboardButton(t("tour", lang), callback_data="tour")],
        [InlineKeyboardButton(t("visa", lang), callback_data="visa")],
        [InlineKeyboardButton(t("address", lang), callback_data="address")],
        [InlineKeyboardButton(t("contact", lang), callback_data="contact")],
        [InlineKeyboardButton(t("language_bn"), callback_data="language")],
    ])


def tour_menu_kb(lang: str) -> InlineKeyboardMarkup:
    buttons = t("tour_buttons", lang)
    rows = [[InlineKeyboardButton(lbl, callback_data=data)] for (lbl, data) in buttons]
    rows.append([InlineKeyboardButton(t("back", lang), callback_data="menu")])
    return InlineKeyboardMarkup(rows)


# ==============================
# 🎯 Handlers
# ==============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    # default language Bangla
    context.user_data.setdefault("lang", "bn")
    lang = lang_of(context.user_data)

    # Send banner image (optional)
    if IMAGES.get("banner"):
        try:
            await update.message.reply_photo(
                IMAGES["banner"],
                caption=(t("welcome", lang).format(name=user.first_name or "")),
                parse_mode=ParseMode.HTML,
                reply_markup=main_menu_kb(lang),
            )
            return
        except Exception:
            pass

    # Fallback if photo fails
    await update.message.reply_text(
        t("welcome", lang).format(name=user.first_name or ""),
        parse_mode=ParseMode.HTML,
        reply_markup=main_menu_kb(lang),
    )


async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = lang_of(context.user_data)
    query = update.callback_query
    await query.answer()
    await query.edit_message_caption(
        caption=t("welcome", lang).format(name=update.effective_user.first_name or ""),
        parse_mode=ParseMode.HTML,
        reply_markup=main_menu_kb(lang),
    ) if query.message.caption else await query.edit_message_text(
        text=t("welcome", lang).format(name=update.effective_user.first_name or ""),
        parse_mode=ParseMode.HTML,
        reply_markup=main_menu_kb(lang),
    )


async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = lang_of(context.user_data)

    data = query.data
    if data == "menu":
        return await show_menu(update, context)

    if data == "language":
        # toggle language
        context.user_data["lang"] = "en" if lang == "bn" else "bn"
        lang = lang_of(context.user_data)
        return await show_menu(update, context)

    if data == "flight":
        text = t("flight_text", lang).format(**AGENCY)
    elif data == "hotel":
        text = t("hotel_text", lang)
    elif data == "tour":
        text = t("tour_text", lang)
        kb = tour_menu_kb(lang)
        return await _edit(query, text, kb)
    elif data == "visa":
        text = t("visa_text", lang)
    elif data == "address":
        text = t("address_text", lang).format(address=AGENCY["address_"+lang], maps=AGENCY["maps"]) if f"address_{lang}" in AGENCY else t("address_text", lang).format(address=AGENCY["address_bn"], maps=AGENCY["maps"])
    elif data == "contact":
        text = t("contact_text", lang).format(**AGENCY)
    elif data in ("tour_th", "tour_my", "tour_ae"):
        return await send_tour_package(query, lang, data)
    else:
        text = "Unknown option"

    await _edit(query, text, main_menu_kb(lang))


async def _edit(query, text: str, kb: InlineKeyboardMarkup):
    # edit caption if message has photo caption; else edit text
    if query.message.photo:
        try:
            await query.edit_message_caption(caption=text, parse_mode=ParseMode.HTML, reply_markup=kb)
            return
        except Exception:
            pass
    await query.edit_message_text(text=text, parse_mode=ParseMode.HTML, reply_markup=kb)


# ===== Tour package sender =====
async def send_tour_package(query, lang: str, code: str):
    if code == "tour_th":
        title_bn = "🇹🇭 থাইল্যান্ড ৫ দিন ৪ রাত"
        title_en = "🇹🇭 Thailand 5D4N"
        price = "BDT 50,000"
        photo = IMAGES.get("thailand")
        highlights_bn = "ব্যাংকক + পাতায়া, হোটেল, ব্রেকফাস্ট, এয়ারপোর্ট ট্রান্সফার"
        highlights_en = "Bangkok + Pattaya, hotel, breakfast, airport transfers"
    elif code == "tour_my":
        title_bn = "🇲🇾 মালয়েশিয়া ৪ দিন ৩ রাত"
        title_en = "🇲🇾 Malaysia 4D3N"
        price = "BDT 40,000"
        photo = IMAGES.get("malaysia")
        highlights_bn = "কুয়ালালামপুর সিটি ট্যুর, গেন্টিং, হোটেল, ব্রেকফাস্ট"
        highlights_en = "Kuala Lumpur city tour, Genting, hotel, breakfast"
    else:  # tour_ae
        title_bn = "🇦🇪 দুবাই ৫ দিন ৪ রাত"
        title_en = "🇦🇪 Dubai 5D4N"
        price = "BDT 65,000"
        photo = IMAGES.get("dubai")
        highlights_bn = "ডেজার্ট সাফারি, ডাউনটাউন, মেরিনা ক্রুজ, হোটেল"
        highlights_en = "Desert safari, Downtown, Marina cruise, hotel"

    if lang == "bn":
        caption = (
            f"<b>{title_bn}</b>\n"
            f"প্যাকেজ মূল্য: <b>{price}</b>\n"
            f"ইনক্লুডেড: {highlights_bn}\n\n"
            f"বুকিং: {AGENCY['phone']} / WhatsApp: {AGENCY['whatsapp']}"
        )
    else:
        caption = (
            f"<b>{title_en}</b>\n"
            f"Package Price: <b>{price}</b>\n"
            f"Includes: {highlights_en}\n\n"
            f"Booking: {AGENCY['phone']} / WhatsApp: {AGENCY['whatsapp']}"
        )

    kb = InlineKeyboardMarkup([[InlineKeyboardButton(t("back", lang), callback_data="tour")]])

    # Try to edit to a photo if current message has photo or send new photo otherwise
    try:
        if query.message.photo:
            await query.edit_message_media(
                media=InputMediaPhoto(media=photo, caption=caption, parse_mode=ParseMode.HTML),
                reply_markup=kb,
            )
        else:
            # send a new photo message and keep old message
            await query.message.reply_photo(photo=photo, caption=caption, parse_mode=ParseMode.HTML, reply_markup=kb)
    except Exception:
        await query.message.reply_text(caption, parse_mode=ParseMode.HTML, reply_markup=kb)


# ==============================
# 🚀 App bootstrap
# ==============================

def main():
    if not TOKEN or TOKEN == "PUT_YOUR_BOT_TOKEN_HERE":
        raise RuntimeError("Please set TELEGRAM_BOT_TOKEN env var or put your bot token in TOKEN.")

    app = ApplicationBuilder().token(TOKEN).defaults(Defaults(parse_mode=ParseMode.HTML)).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(on_button))

    print("✅ Travel Agency Bot is running… Press CTRL+C to stop.")
    app.run_polling(close_loop=False)


if __name__ == "__main__":
    main()

