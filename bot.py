import logging, random
from html import escape
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import Application, ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes
from config import BOT_TOKEN

logging.basicConfig(format="%(asctime)s | %(levelname)s | %(name)s | %(message)s", level=logging.INFO)
logger = logging.getLogger("daneshban")

CATS = {
    "banking": ("🏦 بانکداری", [
        ("🏦 مبانی بانکداری", "بانک به عنوان واسطه مالی منابع را تجهیز و به متقاضیان تخصیص می‌دهد."),
        ("💳 سپرده‌ها", "سپرده‌ها از مهم‌ترین منابع بانک هستند و از نظر سررسید، نقدشوندگی و هزینه منابع بررسی می‌شوند."),
        ("💰 تسهیلات", "در تحلیل تسهیلات باید هدف تأمین مالی، توان بازپرداخت، وثایق و ریسک اعتباری بررسی شود."),
        ("🛡️ مدیریت ریسک", "ریسک اعتباری، بازار، نقدینگی و عملیاتی از حوزه‌های مهم مدیریت ریسک بانکی هستند."),
    ]),
    "commerce": ("🌍 تجارت و بازرگانی", [
        ("🌐 مبانی تجارت بین‌الملل", "تجارت بین‌الملل تحت تأثیر نرخ ارز، هزینه حمل، مقررات، ریسک کشور و شرایط پرداخت است."),
        ("📦 اینکوترمز", "اینکوترمز برخی مسئولیت‌ها، هزینه‌ها و ریسک‌های تحویل کالا را میان فروشنده و خریدار مشخص می‌کند."),
        ("💳 پرداخت بین‌المللی", "پیش‌پرداخت، حساب باز، وصول اسنادی و اعتبار اسنادی از روش‌های رایج پرداخت هستند."),
        ("🔗 زنجیره تأمین", "مدیریت زنجیره تأمین جریان کالا، اطلاعات و منابع را از تأمین‌کننده تا مشتری هماهنگ می‌کند."),
    ]),
    "management": ("📊 مدیریت", [
        ("🧭 اصول مدیریت", "برنامه‌ریزی، سازماندهی، رهبری و کنترل از کارکردهای اصلی مدیریت هستند."),
        ("🎯 برنامه‌ریزی", "برنامه‌ریزی مسیر رسیدن از وضعیت موجود به وضعیت مطلوب را مشخص می‌کند."),
        ("🧠 تصمیم‌گیری", "تصمیم‌گیری شامل شناسایی مسئله، بررسی گزینه‌ها، انتخاب، اجرا و ارزیابی است."),
        ("📈 کنترل", "کنترل با مقایسه عملکرد واقعی و اهداف، انحراف‌ها را شناسایی و اصلاح می‌کند."),
    ]),
    "economy": ("💰 اقتصاد و بازار", [
        ("📉 تورم", "تورم به افزایش عمومی و مستمر سطح قیمت‌ها گفته می‌شود."),
        ("💱 نرخ ارز", "نرخ ارز ارزش یک پول در برابر پول دیگر است و از عوامل اقتصادی و انتظارات اثر می‌پذیرد."),
        ("🏦 سیاست پولی", "سیاست پولی مجموعه اقدامات بانک مرکزی برای اثرگذاری بر شرایط پولی و مالی اقتصاد است."),
        ("📊 عرضه و تقاضا", "تعامل عرضه و تقاضا یکی از چارچوب‌های پایه تحلیل قیمت و مقدار در بازار است."),
    ]),
    "marketing": ("📈 بازاریابی و فروش", [
        ("🎯 STP", "STP شامل بخش‌بندی بازار، انتخاب بازار هدف و جایگاه‌یابی است."),
        ("4️⃣ 4P", "مدل کلاسیک 4P شامل Product، Price، Place و Promotion است."),
        ("🧠 رفتار مشتری", "شناخت نیاز، انگیزه و فرآیند تصمیم مشتری برای طراحی پیشنهاد ارزش ضروری است."),
        ("🛒 قیف فروش", "قیف فروش مسیر حرکت مخاطب از آگاهی و علاقه تا تصمیم و خرید را نشان می‌دهد."),
    ]),
}

QUESTIONS = {
    "banking": [
        ("کدام مورد نقدشوندگی بالاتری دارد؟", ["وجه نقد","ملک","دارایی ثابت","کالای انبار"], 0, "وجه نقد سریع‌ترین شکل دارایی برای پرداخت است."),
        ("هدف اصلی اعتبارسنجی چیست؟", ["تبلیغات","برآورد توان بازپرداخت","تغییر نرخ ارز","طراحی شعبه"], 1, "اعتبارسنجی برای سنجش ریسک و توان بازپرداخت انجام می‌شود."),
        ("ریسک اعتباری با چه چیزی مرتبط است؟", ["عدم ایفای تعهد","رنگ لوگو","تبلیغات","طراحی محصول"], 0, "احتمال عدم ایفای تعهدات مالی، ریسک اعتباری ایجاد می‌کند."),
    ],
    "commerce": [
        ("اینکوترمز بیشتر چه چیزی را مشخص می‌کند؟", ["مسئولیت و ریسک تحویل","حقوق کارکنان","مالیات درآمد","ثبت برند"], 0, "اینکوترمز قواعدی درباره تحویل، هزینه و ریسک ارائه می‌کند."),
        ("سند رایج حمل دریایی چیست؟", ["بارنامه دریایی","شناسنامه","فیش حقوقی","کارت بانکی"], 0, "Bill of Lading از اسناد اصلی حمل دریایی است."),
        ("SCM بر چه چیزی تمرکز دارد؟", ["هماهنگی جریان کالا و اطلاعات","فقط تبلیغات","فقط استخدام","فقط حسابداری"], 0, "مدیریت زنجیره تأمین جریان کالا، اطلاعات و منابع را هماهنگ می‌کند."),
    ],
    "management": [
        ("کدام مورد وظیفه اصلی مدیریت است؟", ["برنامه‌ریزی","تفریح","خرید شخصی","طراحی شخصی"], 0, "برنامه‌ریزی یکی از کارکردهای اصلی مدیریت است."),
        ("کنترل مدیریتی برای چیست؟", ["مقایسه عملکرد با اهداف","افزایش هزینه","تغییر نام","حذف برنامه"], 0, "کنترل برای شناسایی انحراف از اهداف و اصلاح آن است."),
        ("تصمیم‌گیری یعنی چه؟", ["انتخاب میان گزینه‌ها","فقط تبلیغات","فقط فروش","فقط حسابداری"], 0, "تصمیم‌گیری فرآیند انتخاب گزینه مناسب است."),
    ],
    "economy": [
        ("تورم چیست؟", ["افزایش عمومی و مستمر قیمت‌ها","کاهش جمعیت","افزایش صادرات فقط","کاهش یک کالا"], 0, "تورم افزایش عمومی و مستمر سطح قیمت‌هاست."),
        ("افزایش نرخ بهره معمولاً چه اثری بر تقاضای وام دارد؟", ["کاهش","دو برابر","بی‌اثر","صفر"], 0, "افزایش هزینه تأمین مالی معمولاً تقاضای وام را کاهش می‌دهد."),
        ("عرضه و تقاضا برای تحلیل چیست؟", ["قیمت و مقدار بازار","رنگ سازمانی","استخدام","طراحی سایت"], 0, "عرضه و تقاضا چارچوب پایه تحلیل بازار است."),
    ],
    "marketing": [
        ("STP شامل چیست؟", ["بخش‌بندی، هدف‌گیری، جایگاه‌یابی","فروش، مالیات، تولید","حمل، بیمه، گمرک","حقوق، دستمزد، مالیات"], 0, "STP مخفف Segmentation, Targeting, Positioning است."),
        ("کدام مورد یکی از 4P است؟", ["Product","Payroll","Passport","Personnel"], 0, "Product، Price، Place و Promotion چهار عنصر کلاسیک هستند."),
        ("قیف فروش چه چیزی را نشان می‌دهد؟", ["مسیر تبدیل مخاطب به مشتری","مالیات","حمل کالا","ثبت شرکت"], 0, "قیف فروش مراحل حرکت مشتری تا خرید را نشان می‌دهد."),
    ],
}

WELCOME = """<b>🎓 به دانش‌بان خوش آمدید</b>

<b>دانش را به مهارت تبدیل کن.</b> 🚀

یک پلتفرم تخصصی برای یادگیری، تمرین و سنجش مهارت در:
🏦 بانکداری
🌍 تجارت و بازرگانی
📊 مدیریت
💰 اقتصاد و بازار
📈 بازاریابی و فروش
🏆 آزمون‌های استخدامی

از منوی زیر شروع کن 👇"""

def home():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📚 آموزش تخصصی", callback_data="education"), InlineKeyboardButton("🎯 آزمون و تست", callback_data="exams")],
        [InlineKeyboardButton("🏦 بانکداری", callback_data="learn:banking"), InlineKeyboardButton("🌍 تجارت و بازرگانی", callback_data="learn:commerce")],
        [InlineKeyboardButton("📊 مدیریت", callback_data="learn:management"), InlineKeyboardButton("💰 اقتصاد و بازار", callback_data="learn:economy")],
        [InlineKeyboardButton("📈 بازاریابی و فروش", callback_data="learn:marketing"), InlineKeyboardButton("🏆 آزمون استخدامی", callback_data="employment")],
        [InlineKeyboardButton("📂 جزوات و PDF", callback_data="pdf"), InlineKeyboardButton("📈 کارنامه من", callback_data="performance")],
        [InlineKeyboardButton("👤 پروفایل", callback_data="profile"), InlineKeyboardButton("🤝 پشتیبانی", callback_data="support")],
    ])

def back():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🏠 منوی اصلی", callback_data="home")]])

def category_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(CATS[k][0], callback_data=f"quiz:{k}")] for k in CATS
    ] + [[InlineKeyboardButton("🏠 منوی اصلی", callback_data="home")]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(WELCOME, parse_mode=ParseMode.HTML, reply_markup=home())

async def show_learning(q, key):
    title, lessons = CATS[key]
    rows = [[InlineKeyboardButton(title, callback_data="noop")]]
    for name, lesson_key in lessons:
        rows.append([InlineKeyboardButton(name, callback_data=f"lesson:{key}:{lesson_key}")])
    rows += [[InlineKeyboardButton("🎯 آزمون این حوزه", callback_data=f"quiz:{key}")],
             [InlineKeyboardButton("🏠 منوی اصلی", callback_data="home")]]
    await q.edit_message_text(
        f"<b>{title}</b>\n\n{CATS[key][1][0][1]}\n\nمبحث موردنظر را انتخاب کن:",
        parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(rows)
    )

async def send_question(q, context):
    quiz = context.user_data.get("quiz")
    if not quiz:
        await q.edit_message_text("⚠️ آزمون فعال نیست.", reply_markup=back()); return
    if quiz["i"] >= len(quiz["qs"]):
        total = len(quiz["qs"]); pct = quiz["correct"] / total * 100
        await q.edit_message_text(
            f"<b>🏁 آزمون تمام شد!</b>\n\n✅ صحیح: <b>{quiz['correct']} از {total}</b>\n📊 درصد: <b>{pct:.0f}%</b>\n⭐ امتیاز: <b>{quiz['score']}</b>",
            parse_mode=ParseMode.HTML, reply_markup=back()
        )
        context.user_data.pop("quiz", None); return
    quiz["answered"] = False
    item = quiz["qs"][quiz["i"]]
    keys = [[InlineKeyboardButton(f"{n+1}) {x}", callback_data=f"ans:{quiz['i']}:{n}")] for n,x in enumerate(item[1])]
    keys.append([InlineKeyboardButton("⛔ پایان آزمون", callback_data="cancel")])
    await q.edit_message_text(
        f"<b>🎯 {CATS[quiz['cat']][0]}</b>\n\nسوال <b>{quiz['i']+1}</b> از <b>{len(quiz['qs'])}</b>\n\n{item[0]}",
        parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keys)
    )

async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    d = q.data or ""
    if d == "home":
        context.user_data.pop("quiz", None); await q.edit_message_text(WELCOME, parse_mode=ParseMode.HTML, reply_markup=home()); return
    if d == "noop": return
    if d == "education":
        rows = [[InlineKeyboardButton(CATS[k][0], callback_data=f"learn:{k}")] for k in CATS]
        rows.append([InlineKeyboardButton("🏠 منوی اصلی", callback_data="home")])
        await q.edit_message_text("<b>📚 آموزش تخصصی</b>\n\nحوزه موردنظر را انتخاب کن:", parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(rows)); return
    if d.startswith("learn:"):
        await show_learning(q, d.split(":")[1]); return
    if d.startswith("lesson:"):
        _, cat, idx = d.split(":")
        lesson = next((x[1] for x in CATS[cat][1] if x[0] == idx), None)
        # idx is a compact key in this version; map by position if needed
        lessons = CATS[cat][1]
        pos = int(idx) if idx.isdigit() else 0
        text = lessons[pos][1] if pos < len(lessons) else lessons[0][1]
        await q.edit_message_text(f"<b>{CATS[cat][0]}</b>\n\n{text}", parse_mode=ParseMode.HTML, reply_markup=back()); return
    if d == "exams":
        await q.edit_message_text("<b>🎯 مرکز آزمون دانش‌بان</b>\n\nموضوع آزمون را انتخاب کن:", parse_mode=ParseMode.HTML, reply_markup=category_menu()); return
    if d.startswith("quiz:"):
        cat = d.split(":")[1]
        qs = random.sample(QUESTIONS[cat], min(5, len(QUESTIONS[cat])))
        context.user_data["quiz"] = {"cat":cat, "qs":qs, "i":0, "correct":0, "score":0, "answered":False}
        await send_question(q, context); return
    if d.startswith("ans:"):
        quiz = context.user_data.get("quiz")
        if not quiz: await q.answer("آزمون فعال نیست.", show_alert=True); return
        _, i, opt = d.split(":"); i=int(i); opt=int(opt)
        if i != quiz["i"] or quiz["answered"]:
            await q.answer("این سوال دیگر فعال نیست.", show_alert=True); return
        item = quiz["qs"][i]; quiz["answered"]=True; ok=opt==item[2]
        if ok: quiz["correct"]+=1; quiz["score"]+=10
        quiz["i"]+=1
        result = "✅ <b>پاسخ درست است!</b>" if ok else "❌ <b>پاسخ نادرست است.</b>"
        await q.edit_message_text(f"{result}\n\n💡 <b>توضیح:</b> {item[3]}\n\n⭐ امتیاز: <b>{quiz['score']}</b>", parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("➡️ سوال بعدی", callback_data="next")]])); return
    if d == "next":
        await send_question(q, context); return
    if d == "cancel":
        context.user_data.pop("quiz", None); await q.edit_message_text("⛔ آزمون متوقف شد.", reply_markup=home()); return
    if d == "employment":
        await q.edit_message_text("<b>🏆 آزمون استخدامی</b>\n\nاین بخش برای دروس تخصصی، هوش، آزمون جامع و شبیه‌سازی استخدامی طراحی شده است.\n\nدر نسخه بعدی بانک سوالات اختصاصی و منابع رسمی هر آزمون اضافه می‌شود.", parse_mode=ParseMode.HTML, reply_markup=category_menu()); return
    if d == "pdf":
        await q.edit_message_text("<b>📂 جزوات و PDF</b>\n\nمنابع رایگان و PDFهای تخصصی پولی در این بخش قرار می‌گیرند.\n\n🔒 پرداخت و تحویل خودکار فایل را بعد از پایدار شدن هسته ربات اضافه می‌کنیم.", parse_mode=ParseMode.HTML, reply_markup=back()); return
    if d == "support":
        await q.edit_message_text("<b>🤝 پشتیبانی دانش‌بان</b>\n\nگزارش خطا، پیشنهاد محتوا و درخواست همکاری را می‌توانیم به شناسه پشتیبانی متصل کنیم.", parse_mode=ParseMode.HTML, reply_markup=back()); return
    if d in ("performance","profile"):
        await q.edit_message_text("<b>📈 کارنامه و پروفایل</b>\n\nهسته ثبت نتایج در مرحله بعد به‌صورت کامل به پایگاه داده متصل می‌شود.", parse_mode=ParseMode.HTML, reply_markup=back()); return
    if d.startswith("learn:"): return
    await q.edit_message_text("⚠️ گزینه معتبر نیست.", reply_markup=back())

async def error_handler(update, context):
    logger.exception("Unhandled error", exc_info=context.error)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CallbackQueryHandler(callback))
    app.add_error_handler(error_handler)
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__ == "__main__":
    main()
