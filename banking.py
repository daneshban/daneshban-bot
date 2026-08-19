# banking.py
# DANESHBAN | دانش‌بان
# Banking Education Module

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


BANKING_HEADER = """
🏦 <b>دانش‌بان | مرکز تخصصی بانکداری</b>

دانش تخصصی بانکداری را از مفاهیم پایه تا مباحث پیشرفته یاد بگیر،
تمرین کن و با آزمون‌های تخصصی میزان آمادگی خودت را بسنج.

━━━━━━━━━━━━━━━━━━
📚 آموزش تخصصی
🧠 مفاهیم کاربردی
🎯 آزمون‌های استاندارد
📊 تحلیل عملکرد
💼 آمادگی آزمون استخدامی بانک‌ها
━━━━━━━━━━━━━━━━━━
"""


def banking_menu():
    keyboard = [
        [
            InlineKeyboardButton("📘 مبانی بانکداری", callback_data="banking_basics"),
            InlineKeyboardButton("💳 سپرده‌ها", callback_data="banking_deposits"),
        ],
        [
            InlineKeyboardButton("💰 تسهیلات بانکی", callback_data="banking_facilities"),
            InlineKeyboardButton("📑 قراردادهای بانکی", callback_data="banking_contracts"),
        ],
        [
            InlineKeyboardButton("⚖️ قوانین بانکی", callback_data="banking_laws"),
            InlineKeyboardButton("🧾 چک و اسناد", callback_data="banking_checks"),
        ],
        [
            InlineKeyboardButton("🛡️ مبارزه با پولشویی", callback_data="banking_aml"),
            InlineKeyboardButton("📊 اعتبارسنجی", callback_data="banking_credit"),
        ],
        [
            InlineKeyboardButton("💻 بانکداری الکترونیک", callback_data="banking_electronic"),
            InlineKeyboardButton("⚠️ مدیریت ریسک", callback_data="banking_risk"),
        ],
        [
            InlineKeyboardButton("🏛️ بانک مرکزی", callback_data="banking_central"),
            InlineKeyboardButton("☪️ بانکداری اسلامی", callback_data="banking_islamic"),
        ],
        [
            InlineKeyboardButton("🎯 آزمون بانکداری", callback_data="banking_quiz"),
            InlineKeyboardButton("💼 آزمون استخدامی بانک‌ها", callback_data="banking_employment"),
        ],
        [
            InlineKeyboardButton("🔙 بازگشت به منوی اصلی", callback_data="main_menu"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


BANKING_BASICS = """
📘 <b>مبانی بانکداری</b>

در این بخش با مفاهیم پایه و ضروری نظام بانکی آشنا می‌شوی.

🔹 مفهوم بانک و نظام بانکی
🔹 انواع بانک‌ها
🔹 وظایف بانک‌ها
🔹 منابع و مصارف بانک
🔹 عملیات بانکی
🔹 خلق پول و نقش بانک‌ها
🔹 نقدینگی
🔹 نرخ سود و نرخ بهره
🔹 ساختار نظام بانکی

💡 <b>نکته آزمونی:</b>
شناخت دقیق منابع و مصارف بانک‌ها یکی از مباحث مهم در آزمون‌های استخدامی بانک‌هاست.
"""


BANKING_DEPOSITS = """
💳 <b>سپرده‌های بانکی</b>

سپرده‌ها یکی از مهم‌ترین منابع تأمین مالی بانک‌ها هستند.

📌 <b>انواع مهم سپرده:</b>

🔹 سپرده قرض‌الحسنه جاری
🔹 سپرده قرض‌الحسنه پس‌انداز
🔹 سپرده سرمایه‌گذاری کوتاه‌مدت
🔹 سپرده سرمایه‌گذاری بلندمدت

📊 <b>نکات مهم:</b>

• تفاوت سپرده‌های قرض‌الحسنه و سرمایه‌گذاری
• نحوه تجهیز منابع
• نقش سپرده‌ها در عملیات بانکی
• هزینه تجهیز منابع
• مدیریت منابع و نقدینگی
"""


BANKING_FACILITIES = """
💰 <b>تسهیلات بانکی</b>

تسهیلات، یکی از مهم‌ترین بخش‌های عملیات بانکی و منبع درآمد بانک‌هاست.

🔹 تسهیلات قرض‌الحسنه
🔹 فروش اقساطی
🔹 جعاله
🔹 مشارکت مدنی
🔹 مضاربه
🔹 اجاره به شرط تملیک
🔹 سلف
🔹 مرابحه

🎯 <b>برای آزمون استخدامی:</b>

درک تفاوت قراردادها، کاربرد هر قرارداد و ویژگی‌های اصلی آن‌ها اهمیت زیادی دارد.
"""


BANKING_CONTRACTS = """
📑 <b>قراردادهای بانکی</b>

در نظام بانکداری بدون ربا، تسهیلات در قالب عقود و قراردادهای مشخص ارائه می‌شوند.

📌 مهم‌ترین عقود:

1️⃣ مشارکت مدنی
2️⃣ مضاربه
3️⃣ جعاله
4️⃣ فروش اقساطی
5️⃣ اجاره به شرط تملیک
6️⃣ سلف
7️⃣ مرابحه
8️⃣ قرض‌الحسنه

🧠 پیشنهاد دانش‌بان:
برای هر عقد، «تعریف + کاربرد + طرفین قرارداد + موضوع قرارداد» را یاد بگیر.
"""


BANKING_LAWS = """
⚖️ <b>قوانین و مقررات بانکی</b>

در این بخش با مباحث مهم حقوق و مقررات بانکی آشنا می‌شوی.

🔹 قوانین پولی و بانکی
🔹 مقررات بانک مرکزی
🔹 مقررات تسهیلات
🔹 مقررات حساب‌ها
🔹 مقررات چک
🔹 حقوق مشتریان بانک
🔹 الزامات مبارزه با پولشویی
🔹 مقررات نظارتی

⚠️ قوانین و مقررات ممکن است تغییر کنند؛
برای مباحث آزمونی باید همیشه آخرین نسخه منابع بررسی شود.
"""


BANKING_CHECKS = """
🧾 <b>چک و اسناد بانکی</b>

چک یکی از مهم‌ترین ابزارهای پرداخت و اسناد تجاری است.

📌 مباحث:

🔹 مفهوم چک
🔹 انواع چک
🔹 چک صیادی
🔹 ثبت و انتقال چک
🔹 تأیید و استعلام
🔹 برگشت چک
🔹 مسئولیت صادرکننده
🔹 حقوق دارنده چک

🎯 <b>نکته:</b>
سؤالات مربوط به چک و مقررات جدید آن می‌تواند در آزمون‌های استخدامی اهمیت داشته باشد.
"""


BANKING_AML = """
🛡️ <b>مبارزه با پولشویی | AML</b>

مبارزه با پولشویی یکی از بخش‌های مهم نظام بانکی و نظارت مالی است.

🔹 مفهوم پولشویی
🔹 مراحل پولشویی
🔹 شناسایی مشتری | KYC
🔹 معاملات مشکوک
🔹 گزارش‌دهی
🔹 کنترل‌های داخلی
🔹 ریسک مشتری
🔹 الزامات نظارتی

🔐 هدف:
جلوگیری از سوءاستفاده از شبکه بانکی برای فعالیت‌های غیرقانونی.
"""


BANKING_CREDIT = """
📊 <b>اعتبارسنجی و مدیریت اعتبار</b>

اعتبارسنجی به بانک کمک می‌کند توان و ریسک بازپرداخت مشتری را ارزیابی کند.

🔹 اعتبار مشتری
🔹 سابقه اعتباری
🔹 توان بازپرداخت
🔹 ریسک اعتباری
🔹 وثایق
🔹 رتبه اعتباری
🔹 نکول
🔹 مدیریت مطالبات

💡 <b>اصل مهم:</b>
هرچه ریسک اعتباری مشتری دقیق‌تر ارزیابی شود،
تصمیم‌گیری تسهیلاتی نیز اصولی‌تر خواهد بود.
"""


BANKING_ELECTRONIC = """
💻 <b>بانکداری الکترونیک</b>

بانکداری مدرن بدون خدمات الکترونیکی قابل تصور نیست.

🔹 اینترنت‌بانک
🔹 همراه‌بانک
🔹 کارت‌های بانکی
🔹 درگاه پرداخت
🔹 پرداخت الکترونیکی
🔹 انتقال وجه
🔹 امنیت تراکنش‌ها
🔹 بانکداری دیجیتال
🔹 فین‌تک

🚀 مسیر آینده:
حرکت از بانکداری سنتی به سمت بانکداری دیجیتال و داده‌محور.
"""


BANKING_RISK = """
⚠️ <b>مدیریت ریسک بانکی</b>

بانک‌ها با انواع مختلفی از ریسک مواجه هستند.

📌 مهم‌ترین ریسک‌ها:

🔴 ریسک اعتباری
🔵 ریسک بازار
🟡 ریسک نقدینگی
🟢 ریسک عملیاتی
🟣 ریسک نرخ سود
⚫ ریسک فناوری و امنیت

🎯 هدف مدیریت ریسک:
کاهش زیان‌های احتمالی و افزایش ثبات و پایداری بانک.
"""


BANKING_CENTRAL = """
🏛️ <b>بانک مرکزی</b>

بانک مرکزی در نظام پولی و بانکی نقش کلیدی دارد.

🔹 سیاست پولی
🔹 کنترل نقدینگی
🔹 نظارت بر بانک‌ها
🔹 انتشار پول
🔹 مدیریت ذخایر
🔹 تنظیم مقررات بانکی
🔹 ثبات پولی و مالی

📈 یکی از موضوعات مهم اقتصادی:
ارتباط سیاست پولی با تورم، نرخ سود و نقدینگی.
"""


BANKING_ISLAMIC = """
☪️ <b>بانکداری اسلامی</b>

بانکداری اسلامی بر مبنای عقود شرعی و اصول مالی اسلامی شکل گرفته است.

🔹 قرض‌الحسنه
🔹 مشارکت
🔹 مضاربه
🔹 جعاله
🔹 فروش اقساطی
🔹 اجاره به شرط تملیک
🔹 مرابحه
🔹 سلف

📚 این بخش برای آزمون‌های استخدامی بانک‌ها اهمیت ویژه‌ای دارد.
"""


BANKING_EMPLOYMENT = """
💼 <b>آمادگی آزمون استخدامی بانک‌ها</b>

اینجا قرار است برای آزمون‌های استخدامی بانک‌ها
هدفمند و مرحله‌به‌مرحله آماده شوی.

🎯 امکانات:

📚 آموزش مباحث تخصصی
📝 تست‌های چهارگزینه‌ای
⏱️ زمان‌سنج آزمون
🎲 سوالات تصادفی
📊 محاسبه درصد
🏆 امتیاز و رتبه
📈 تحلیل عملکرد
🧠 تقویت سرعت پاسخ‌گویی
🎤 آمادگی مصاحبه

━━━━━━━━━━━━━━━━━━

🏦 بانک‌های هدف می‌توانند شامل:
بانک ملی
بانک ملت
بانک تجارت
بانک صادرات
بانک رفاه کارگران
بانک شهر
بانک مسکن
بانک کشاورزی
بانک سپه
بانک قرض‌الحسنه مهر ایران

━━━━━━━━━━━━━━━━━━

🚀 <b>دانش‌بان؛ مسیر آمادگی حرفه‌ای برای آزمون‌های بانکی</b>
"""


BANKING_QUIZ = """
🎯 <b>آزمون تخصصی بانکداری</b>

آماده‌ای سطح دانش بانکداری خودت را بسنجی؟

در آزمون‌های دانش‌بان:

⏱️ زمان پاسخ‌گویی داری
🎲 سؤالات به‌صورت تصادفی انتخاب می‌شوند
📊 درصد و امتیاز محاسبه می‌شود
✅ پاسخ صحیح نمایش داده می‌شود
💡 پاسخ تشریحی ارائه می‌شود
📈 عملکردت تحلیل می‌شود

👇 یکی از آزمون‌ها را انتخاب کن:
"""


BANKING_QUESTIONS = [
    {
        "question": "کدام گزینه از مهم‌ترین وظایف بانک‌ها محسوب می‌شود؟",
        "options": [
            "تجهیز و تخصیص منابع",
            "تولید کالا",
            "تعیین مالیات",
            "صدور شناسنامه",
        ],
        "answer": 0,
        "explanation": "بانک‌ها منابع مالی را تجهیز کرده و در قالب‌های مختلف به متقاضیان تخصیص می‌دهند.",
    },
    {
        "question": "کدام مورد از عقود مورد استفاده در نظام بانکداری بدون ربا است؟",
        "options": [
            "مشارکت مدنی",
            "مالیات مستقیم",
            "تأمین اجتماعی",
            "بیمه شخص ثالث",
        ],
        "answer": 0,
        "explanation": "مشارکت مدنی یکی از عقود مورد استفاده در نظام بانکداری بدون رباست.",
    },
    {
        "question": "KYC در نظام بانکی بیشتر به چه مفهومی اشاره دارد؟",
        "options": [
            "شناخت مشتری",
            "مدیریت نقدینگی",
            "محاسبه سود",
            "مدیریت بازار",
        ],
        "answer": 0,
        "explanation": "KYC مخفف Know Your Customer و به معنای شناخت مشتری است.",
    },
]


BANKING_TEXTS = {
    "banking_basics": BANKING_BASICS,
    "banking_deposits": BANKING_DEPOSITS,
    "banking_facilities": BANKING_FACILITIES,
    "banking_contracts": BANKING_CONTRACTS,
    "banking_laws": BANKING_LAWS,
    "banking_checks": BANKING_CHECKS,
    "banking_aml": BANKING_AML,
    "banking_credit": BANKING_CREDIT,
    "banking_electronic": BANKING_ELECTRONIC,
    "banking_risk": BANKING_RISK,
    "banking_central": BANKING_CENTRAL,
    "banking_islamic": BANKING_ISLAMIC,
    "banking_employment": BANKING_EMPLOYMENT,
    "banking_quiz": BANKING_QUIZ,
}


async def show_banking_menu(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query

    if query:
        await query.answer()
        await query.edit_message_text(
            BANKING_HEADER,
            reply_markup=banking_menu(),
            parse_mode="HTML",
        )
    else:
        await update.message.reply_text(
            BANKING_HEADER,
            reply_markup=banking_menu(),
            parse_mode="HTML",
        )


async def handle_banking_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "banking_menu":
        await query.edit_message_text(
            BANKING_HEADER,
            reply_markup=banking_menu(),
            parse_mode="HTML",
        )
        return

    if data in BANKING_TEXTS:
        keyboard = [
            [
                InlineKeyboardButton(
                    "🏦 منوی بانکداری",
                    callback_data="banking_menu",
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 منوی اصلی",
                    callback_data="main_menu",
                )
            ],
        ]

        await query.edit_message_text(
            BANKING_TEXTS[data],
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML",
        )
        return
