# -*- coding: utf-8 -*-

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode

from content.commerce import (
    COMMERCE,
    LESSONS,
    QUIZ,
)


# =========================================================
# COMMERCE MAIN MENU
# =========================================================

def commerce_menu() -> InlineKeyboardMarkup:

    keyboard = []

    for key, section in COMMERCE.items():

        keyboard.append([
            InlineKeyboardButton(
                section["title"],
                callback_data=f"comcat:{key}",
            )
        ])

    keyboard.append([
        InlineKeyboardButton(
            "🎯 آزمون جامع تجارت",
            callback_data="comquiz:start",
        )
    ])

    keyboard.append([
        InlineKeyboardButton(
            "🏠 منوی اصلی",
            callback_data="home",
        )
    ])

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# CATEGORY MENU
# =========================================================

def category_menu(key: str) -> InlineKeyboardMarkup:

    section = COMMERCE.get(key)

    if not section:
        return commerce_menu()

    keyboard = []

    for lesson_title, lesson_id in section["lessons"]:

        keyboard.append([
            InlineKeyboardButton(
                f"📖 {lesson_title}",
                callback_data=f"comlesson:{key}:{lesson_id}",
            )
        ])

    keyboard.append([
        InlineKeyboardButton(
            "🎯 آزمون این بخش",
            callback_data=f"comquiz:category:{key}",
        )
    ])

    keyboard.append([
        InlineKeyboardButton(
            "⬅️ تجارت و بازرگانی",
            callback_data="commerce",
        )
    ])

    keyboard.append([
        InlineKeyboardButton(
            "🏠 منوی اصلی",
            callback_data="home",
        )
    ])

    return InlineKeyboardMarkup(keyboard)


# =========================================================
# SHOW COMMERCE
# =========================================================

async def show_commerce(query):

    text = """
<b>🌍 آکادمی تجارت و بازرگانی دانش‌بان</b>

به بخش تخصصی تجارت و بازرگانی خوش آمدی. 🚀

در این بخش می‌توانی مسیرهای آموزشی زیر را دنبال کنی:

📘 مبانی تجارت و بازرگانی
🌐 تجارت بین‌الملل
📑 اینکوترمز
🚢 حمل‌ونقل و لجستیک
💳 روش‌های پرداخت
🏦 تأمین مالی تجارت
📦 صادرات
📥 واردات
🧾 اسناد تجاری
⚠️ مدیریت ریسک

همچنین می‌توانی در آزمون‌های تخصصی شرکت کنی.

<b>🎯 هدف دانش‌بان:</b>

دانش → تمرین → آزمون → مهارت
"""

    await query.edit_message_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=commerce_menu(),
    )


# =========================================================
# SHOW CATEGORY
# =========================================================

async def show_category(
    query,
    key: str,
):

    section = COMMERCE.get(key)

    if not section:

        await query.edit_message_text(
            "⚠️ بخش موردنظر پیدا نشد.",
            reply_markup=commerce_menu(),
        )

        return

    text = f"""
<b>{section["title"]}</b>

📚 درس‌های این بخش:

یکی از درس‌ها را انتخاب کن.
"""

    await query.edit_message_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=category_menu(key),
    )


# =========================================================
# SHOW LESSON
# =========================================================

async def show_lesson(
    query,
    key: str,
    lesson_id: str,
):

    section = COMMERCE.get(key)

    if not section:

        await query.edit_message_text(
            "⚠️ دسته آموزشی پیدا نشد.",
            reply_markup=commerce_menu(),
        )

        return

    if lesson_id not in LESSONS:

        await query.edit_message_text(
            "⚠️ محتوای این درس پیدا نشد.",
            reply_markup=category_menu(key),
        )

        return

    text = LESSONS[lesson_id]

    keyboard = [

        [
            InlineKeyboardButton(
                "🎯 آزمون این بخش",
                callback_data=f"comquiz:category:{key}",
            )
        ],

        [
            InlineKeyboardButton(
                "⬅️ بازگشت به درس‌ها",
                callback_data=f"comcat:{key}",
            )
        ],

        [
            InlineKeyboardButton(
                "🌍 تجارت و بازرگانی",
                callback_data="commerce",
            )
        ],

        [
            InlineKeyboardButton(
                "🏠 منوی اصلی",
                callback_data="home",
            )
        ],
    ]

    await query.edit_message_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# =========================================================
# GET QUESTIONS
# =========================================================

def questions_for(key=None):

    if key is None:
        return QUIZ

    section = COMMERCE.get(key)

    if not section:
        return []

    lesson_ids = {
        lesson_id
        for _, lesson_id in section["lessons"]
    }

    return [
        question
        for question in QUIZ
        if question["lesson"] in lesson_ids
    ]


# =========================================================
# START QUIZ
# =========================================================

async def start_quiz(
    query,
    context,
    key=None,
):

    questions = questions_for(key)

    if not questions:

        await query.edit_message_text(
            """
⚠️ هنوز سؤال کافی برای این بخش ثبت نشده است.

به‌زودی مجموعه تست‌های این قسمت تکمیل خواهد شد.
""",
            reply_markup=commerce_menu(),
        )

        return

    context.user_data["commerce_quiz"] = {

        "questions": questions,

        "index": 0,

        "score": 0,

        "category": key,

    }

    await send_question(
        query,
        context,
    )


# =========================================================
# SEND QUESTION
# =========================================================

async def send_question(
    query,
    context,
):

    quiz = context.user_data.get(
        "commerce_quiz"
    )

    if not quiz:

        await query.edit_message_text(
            "⚠️ آزمون فعالی وجود ندارد.",
            reply_markup=commerce_menu(),
        )

        return

    questions = quiz["questions"]

    index = quiz["index"]

    if index >= len(questions):

        await finish_quiz(
            query,
            context,
        )

        return

    question = questions[index]

    keyboard = []

    for option_index, option in enumerate(
        question["options"]
    ):

        keyboard.append([
            InlineKeyboardButton(
                option,
                callback_data=f"comans:{option_index}",
            )
        ])

    keyboard.append([
        InlineKeyboardButton(
            "❌ خروج از آزمون",
            callback_data="commerce",
        )
    ])

    text = f"""
<b>🎯 آزمون تجارت و بازرگانی</b>

━━━━━━━━━━━━━━

📌 سؤال:

<b>{question["question"]}</b>

━━━━━━━━━━━━━━

📊 سؤال {index + 1} از {len(questions)}

💡 یکی از گزینه‌ها را انتخاب کن.
"""

    await query.edit_message_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# =========================================================
# ANSWER QUIZ
# =========================================================

async def answer_quiz(
    query,
    context,
    answer_index,
):

    quiz = context.user_data.get(
        "commerce_quiz"
    )

    if not quiz:

        await query.edit_message_text(
            "⚠️ آزمون فعال نیست.",
            reply_markup=commerce_menu(),
        )

        return

    try:

        answer_index = int(
            answer_index
        )

    except (TypeError, ValueError):

        await query.answer(
            "⚠️ پاسخ نامعتبر است.",
            show_alert=True,
        )

        return

    index = quiz["index"]

    questions = quiz["questions"]

    if index >= len(questions):

        await finish_quiz(
            query,
            context,
        )

        return

    question = questions[index]

    if (
        answer_index < 0
        or answer_index >= len(
            question["options"]
        )
    ):

        await query.answer(
            "⚠️ گزینه نامعتبر است.",
            show_alert=True,
        )

        return

    is_correct = (
        answer_index
        == question["answer"]
    )

    if is_correct:

        quiz["score"] += 1

        result_text = "✅ <b>پاسخ صحیح بود!</b>"

    else:

        correct_answer = question[
            "options"
        ][question["answer"]]

        result_text = (
            "❌ <b>پاسخ نادرست بود.</b>\n\n"
            f"✅ پاسخ صحیح: <b>{correct_answer}</b>"
        )

    quiz["index"] += 1

    if quiz["index"] >= len(questions):

        total = len(questions)

        score = quiz["score"]

        percent = round(
            (score / total) * 100
        )

        context.user_data[
            "commerce_last_result"
        ] = {

            "score": score,

            "total": total,

            "percent": percent,

        }

        explanation = question.get(
            "explanation",
            "",
        )

        keyboard = [

            [
                InlineKeyboardButton(
                    "🎯 آزمون دوباره",
                    callback_data="comquiz:start",
                )
            ],

            [
                InlineKeyboardButton(
                    "🌍 تجارت و بازرگانی",
                    callback_data="commerce",
                )
            ],

            [
                InlineKeyboardButton(
                    "🏠 منوی اصلی",
                    callback_data="home",
                )
            ],

        ]

        text = f"""
<b>🏁 آزمون به پایان رسید</b>

━━━━━━━━━━━━━━

{result_text}

━━━━━━━━━━━━━━

🏆 امتیاز:
<b>{score} از {total}</b>

📊 درصد:
<b>{percent}%</b>

━━━━━━━━━━━━━━

💡 <b>تحلیل پاسخ آخر:</b>

{explanation}
"""

        context.user_data.pop(
            "commerce_quiz",
            None,
        )

        await query.edit_message_text(
            text,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                keyboard
            ),
        )

        return

    # ادامه آزمون

    await query.answer(
        "پاسخ ثبت شد ✅"
    )

    await send_question(
        query,
        context,
    )


# =========================================================
# FINISH QUIZ
# =========================================================

async def finish_quiz(
    query,
    context,
):

    quiz = context.user_data.get(
        "commerce_quiz"
    )

    if not quiz:

        await query.edit_message_text(
            "⚠️ آزمون فعالی وجود ندارد.",
            reply_markup=commerce_menu(),
        )

        return

    total = len(
        quiz["questions"]
    )

    score = quiz["score"]

    percent = round(
        (score / total) * 100
    ) if total else 0

    context.user_data[
        "commerce_last_result"
    ] = {

        "score": score,

        "total": total,

        "percent": percent,

    }

    context.user_data.pop(
        "commerce_quiz",
        None,
    )

    keyboard = InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "🎯 آزمون دوباره",
                callback_data="comquiz:start",
            )
        ],

        [
            InlineKeyboardButton(
                "🌍 تجارت و بازرگانی",
                callback_data="commerce",
            )
        ],

        [
            InlineKeyboardButton(
                "🏠 منوی اصلی",
                callback_data="home",
            )
        ],

    ])

    text = f"""
<b>🏁 آزمون پایان یافت</b>

🏆 امتیاز:
<b>{score} از {total}</b>

📊 درصد:
<b>{percent}%</b>
"""

    await query.edit_message_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard,
    )
