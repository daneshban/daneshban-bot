import logging

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

from config import BOT_TOKEN


# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger("daneshban")


# =========================================================
# TEXTS
# =========================================================

WELCOME_TEXT = """
<b>🎓 به دانش‌بان خوش آمدید</b>

<b>دانش را به مهارت تبدیل کن.</b> 🚀

دانش‌بان یک پلتفرم تخصصی برای یادگیری، تمرین و سنجش مهارت در حوزه‌های:

🏦 بانکداری
🌍 بازرگانی و تجارت
📊 مدیریت
💰 اقتصاد و بازار
📈 بازاریابی و فروش
🎯 آزمون‌های تخصصی
🏆 آزمون‌های استخدامی

است.

از منوی زیر مسیر موردنظر خودت را انتخاب کن.
"""


# =========================================================
# MAIN MENU
# =========================================================

def main_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                "📚 آموزش تخصصی",
                callback_data="education",
            ),
            InlineKeyboardButton(
                "🎯 آزمون و تست",
                callback_data="exams",
            ),
        ],
        [
            InlineKeyboardButton(
                "🏦 بانکداری",
                callback_data="banking",
            ),
            InlineKeyboardButton(
                "🌍 تجارت و بازرگانی",
                callback_data="commerce",
            ),
        ],
        [
            InlineKeyboardButton(
                "📊 مدیریت",
                callback_data="management",
            ),
            InlineKeyboardButton(
                "💰 اقتصاد و بازار",
                callback_data="economy",
            ),
        ],
        [
            InlineKeyboardButton(
                "📈 بازاریابی و فروش",
                callback_data="marketing",
            ),
            InlineKeyboardButton(
                "🏆 آزمون استخدامی",
                callback_data="employment",
            ),
        ],
        [
            InlineKeyboardButton(
                "📂 جزوات و PDF",
                callback_data="pdf",
            ),
            InlineKeyboardButton(
                "📈 کارنامه من",
                callback_data="performance",
            ),
        ],
        [
            InlineKeyboardButton(
                "👤 پروفایل",
                callback_data="profile",
            ),
            InlineKeyboardButton(
                "🤝 حمایت و پشتیبانی",
                callback_data="support",
            ),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# START
# =========================================================

async def start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if not update.effective_message:
        return

    user = update.effective_user

    logger.info(
        "START | user_id=%s | username=%s",
        user.id if user else "unknown",
        user.username if user else "unknown",
    )

    await update.effective_message.reply_text(
        WELCOME_TEXT,
        parse_mode=ParseMode.HTML,
        reply_markup=main_menu_keyboard(),
    )


# =========================================================
# HELP
# =========================================================

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if not update.effective_message:
        return

    text = """
<b>🆘 راهنمای دانش‌بان</b>

از منوی اصلی می‌توانی به بخش‌های مختلف دسترسی داشته باشی.

📚 آموزش
🎯 آزمون
🏆 آزمون استخدامی
📂 جزوات و PDF
📈 تحلیل عملکرد
👤 پروفایل
🤝 پشتیبانی

اگر در هر بخشی مشکلی داشتی، از گزینه «حمایت و پشتیبانی» استفاده کن.
"""

    await update.effective_message.reply_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=main_menu_keyboard(),
    )


# =========================================================
# CALLBACK HANDLER
# =========================================================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    query = update.callback_query

    if query is None:
        return

    await query.answer()

    data = query.data

    logger.info(
        "CALLBACK | user_id=%s | data=%s",
        query.from_user.id,
        data,
    )

    if data == "home":
        await query.edit_message_text(
            WELCOME_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=main_menu_keyboard(),
        )
        return

    section_names = {
        "education": "📚 آموزش تخصصی",
        "exams": "🎯 آزمون و تست",
        "banking": "🏦 بانکداری",
        "commerce": "🌍 تجارت و بازرگانی",
        "management": "📊 مدیریت",
        "economy": "💰 اقتصاد و بازار",
        "marketing": "📈 بازاریابی و فروش",
        "employment": "🏆 آزمون استخدامی",
        "pdf": "📂 جزوات و PDF",
        "performance": "📈 کارنامه من",
        "profile": "👤 پروفایل",
        "support": "🤝 حمایت و پشتیبانی",
    }

    if data in section_names:
        title = section_names[data]

        text = f"""
<b>{title}</b>

این بخش در حال آماده‌سازی است. 🚀

ساختار این قسمت به‌صورت تخصصی و ماژولار طراحی خواهد شد تا آموزش، آزمون، اطلاعات کاربر و عملکرد سیستم از یکدیگر جدا باشند.

<i>دانش‌بان؛ دانش را به مهارت تبدیل کن.</i>
"""

        back_keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🏠 منوی اصلی",
                        callback_data="home",
                    )
                ]
            ]
        )

        await query.edit_message_text(
            text,
            parse_mode=ParseMode.HTML,
            reply_markup=back_keyboard,
        )
        return

    # جلوگیری از گیر کردن Callbackهای ناشناخته
    logger.warning(
        "UNKNOWN CALLBACK | user_id=%s | data=%s",
        query.from_user.id,
        data,
    )

    await query.edit_message_text(
        "⚠️ این گزینه دیگر معتبر نیست.\n\nلطفاً از منوی اصلی ادامه بده.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🏠 منوی اصلی",
                        callback_data="home",
                    )
                ]
            ]
        ),
    )


# =========================================================
# ERROR HANDLER
# =========================================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    logger.error(
        "Unhandled exception",
        exc_info=context.error,
    )


# =========================================================
# APPLICATION
# =========================================================

def create_application() -> Application:
    application = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start_command)
    )

    application.add_handler(
        CommandHandler("help", help_command)
    )

    application.add_handler(
        CallbackQueryHandler(button_handler)
    )

    application.add_error_handler(error_handler)

    return application


# =========================================================
# MAIN
# =========================================================

def main() -> None:
    logger.info("Starting Daneshban bot...")

    application = create_application()

    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()
