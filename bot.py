# -*- coding: utf-8 -*-

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

from handlers.commerce import (
    show_commerce,
    show_category as show_commerce_category,
    show_lesson as show_commerce_lesson,
    start_quiz as start_commerce_quiz,
    answer_quiz as answer_commerce_quiz,
)


# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger("daneshban")


# =========================================================
# WELCOME TEXT
# =========================================================

WELCOME_TEXT = """
<b>🎓 به دانش‌بان خوش آمدید</b>

<b>دانش را به مهارت تبدیل کن.</b> 🚀

دانش‌بان یک پلتفرم تخصصی برای یادگیری، تمرین و سنجش مهارت است.

<b>🎓 مسیرهای آموزشی دانش‌بان:</b>

🏦 بانکداری
🌍 تجارت و بازرگانی
📊 مدیریت
💰 اقتصاد و بازار
📈 بازاریابی و فروش
🧠 مددکاری اجتماعی و روانشناسی

<b>🎯 مسیرهای سنجش:</b>

🎯 آزمون‌های تخصصی
🏆 آزمون‌های استخدامی
📈 تحلیل عملکرد
🏅 سطح‌بندی و امتیاز

<b>📚 امکانات:</b>

📖 آموزش تخصصی
📝 آزمون و تست
📂 جزوات و PDF
👤 پروفایل
📊 کارنامه

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
                "🧠 مددکاری اجتماعی و روانشناسی",
                callback_data="social_psychology",
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
# SIMPLE BACK BUTTON
# =========================================================

def home_keyboard() -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🏠 منوی اصلی",
                    callback_data="home",
                )
            ]
        ]
    )


# =========================================================
# START COMMAND
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
# HELP COMMAND
# =========================================================

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    if not update.effective_message:
        return

    text = """
<b>🆘 راهنمای دانش‌بان</b>

دانش‌بان برای یادگیری، تمرین و سنجش مهارت طراحی شده است.

<b>📚 آموزش</b>
مطالب تخصصی حوزه‌های مختلف.

<b>🎯 آزمون و تست</b>
آزمون‌های آموزشی و تخصصی.

<b>🏆 آزمون استخدامی</b>
مسیر آمادگی برای آزمون‌های استخدامی.

<b>📂 جزوات و PDF</b>
دسترسی به محتوای آموزشی و فایل‌های تخصصی.

<b>📈 کارنامه من</b>
نمایش عملکرد و نتایج آزمون‌ها.

<b>👤 پروفایل</b>
اطلاعات حساب و وضعیت کاربر.

<b>🤝 حمایت و پشتیبانی</b>
ارتباط با پشتیبانی دانش‌بان.
"""

    await update.effective_message.reply_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=main_menu_keyboard(),
    )


# =========================================================
# PLACEHOLDER SECTIONS
# =========================================================

SECTION_NAMES = {

    "education":
        "📚 آموزش تخصصی",

    "exams":
        "🎯 آزمون و تست",

    "banking":
        "🏦 بانکداری",

    "management":
        "📊 مدیریت",

    "economy":
        "💰 اقتصاد و بازار",

    "marketing":
        "📈 بازاریابی و فروش",

    "employment":
        "🏆 آزمون استخدامی",

    "social_psychology":
        "🧠 مددکاری اجتماعی و روانشناسی",

    "pdf":
        "📂 جزوات و PDF",

    "performance":
        "📈 کارنامه من",

    "profile":
        "👤 پروفایل",

    "support":
        "🤝 حمایت و پشتیبانی",
}


# =========================================================
# PLACEHOLDER HANDLER
# =========================================================

async def show_placeholder(
    query,
    title: str,
) -> None:

    text = f"""
<b>{title}</b>

🚧 این بخش در حال توسعه است.

ساختار دانش‌بان به‌صورت ماژولار طراحی شده تا هر بخش مستقل، قابل توسعه و قابل اتصال به سیستم آزمون و تحلیل عملکرد باشد.

<b>🚀 امکاناتی که در نسخه نهایی این بخش قرار می‌گیرد:</b>

📚 آموزش تخصصی
📝 آزمون
🎯 تست تصادفی
⏱ زمان‌سنج
📊 امتیاز و درصد
📈 تحلیل عملکرد
🏅 سطح‌بندی
📂 فایل و PDF
💎 محتوای ویژه

<i>دانش‌بان؛ دانش را به مهارت تبدیل کن.</i>
"""

    await query.edit_message_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=home_keyboard(),
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

    # جلوگیری از Loading ماندن دکمه
    try:
        await query.answer()
    except Exception:
        pass

    data = query.data

    logger.info(
        "CALLBACK | user_id=%s | data=%s",
        query.from_user.id,
        data,
    )

    # =====================================================
    # HOME
    # =====================================================

    if data == "home":

        await query.edit_message_text(
            WELCOME_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=main_menu_keyboard(),
        )

        return

    # =====================================================
    # COMMERCE MODULE
    # =====================================================

    if data == "commerce":

        await show_commerce(
            query
        )

        return

    # -----------------------------------------------------
    # COMMERCE CATEGORY
    # -----------------------------------------------------

    if data.startswith("comcat:"):

        key = data.split(
            ":",
            1,
        )[1]

        await show_commerce_category(
            query,
            key,
        )

        return

    # -----------------------------------------------------
    # COMMERCE LESSON
    # -----------------------------------------------------

    if data.startswith("comlesson:"):

        parts = data.split(
            ":",
            2,
        )

        if len(parts) != 3:

            await query.edit_message_text(
                "⚠️ درخواست درس نامعتبر است.",
                reply_markup=home_keyboard(),
            )

            return

        key = parts[1]

        lesson_id = parts[2]

        await show_commerce_lesson(
            query,
            key,
            lesson_id,
        )

        return

    # -----------------------------------------------------
    # COMMERCE QUIZ
    # -----------------------------------------------------

    if data == "comquiz:start":

        await start_commerce_quiz(
            query,
            context,
        )

        return

    # -----------------------------------------------------
    # COMMERCE CATEGORY QUIZ
    # -----------------------------------------------------

    if data.startswith(
        "comquiz:category:"
    ):

        key = data.split(
            ":",
            2,
        )[2]

        await start_commerce_quiz(
            query,
            context,
            key,
        )

        return

    # -----------------------------------------------------
    # COMMERCE ANSWER
    # -----------------------------------------------------

    if data.startswith("comans:"):

        answer_index = data.split(
            ":",
            1,
        )[1]

        await answer_commerce_quiz(
            query,
            context,
            answer_index,
        )

        return

    # =====================================================
    # OTHER SECTIONS
    # =====================================================

    if data in SECTION_NAMES:

        await show_placeholder(
            query,
            SECTION_NAMES[data],
        )

        return

    # =====================================================
    # UNKNOWN CALLBACK
    # =====================================================

    logger.warning(
        "UNKNOWN CALLBACK | user_id=%s | data=%s",
        query.from_user.id,
        data,
    )

    await query.edit_message_text(
        """
⚠️ این گزینه معتبر نیست.

لطفاً از منوی اصلی ادامه بده.
""",
        reply_markup=home_keyboard(),
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

    # -----------------------------------------------------
    # COMMANDS
    # -----------------------------------------------------

    application.add_handler(
        CommandHandler(
            "start",
            start_command,
        )
    )

    application.add_handler(
        CommandHandler(
            "help",
            help_command,
        )
    )

    # -----------------------------------------------------
    # CALLBACKS
    # -----------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )

    # -----------------------------------------------------
    # ERROR HANDLER
    # -----------------------------------------------------

    application.add_error_handler(
        error_handler
    )

    return application


# =========================================================
# MAIN
# =========================================================

def main() -> None:

    logger.info(
        "Starting Daneshban bot..."
    )

    application = create_application()

    application.run_polling(
        allowed_updates=Update.ALL_TYPES,

        # پیام‌های قدیمی Telegram
        # بعد از Deploy دوباره پردازش نمی‌شوند
        drop_pending_updates=True,
    )


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    main()
