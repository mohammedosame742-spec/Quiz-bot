import logging
import random
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8603168006:AAEcLrC7isNzcUPJJeVRBqt5KVLMWzpYF4c"

QUESTIONS = [
    {"q": "تُعرَّف القضية السكانية بأنها عدم التوازن بين عدد السكان والموارد المتاحة", "a": True},
    {"q": "من أبعاد المشكلة السكانية: الحجم، التوزيع، والخصائص", "a": True},
    {"q": "وادي النيل والدلتا من أكثر المناطق كثافة سكانية", "a": True},
    {"q": "الزيادة الطبيعية للسكان = المواليد - الوفيات", "a": True},
    {"q": "التعليم وخاصة تعليم الإناث من العوامل المؤثرة في خفض الخصوبة", "a": True},
    {"q": "من آثار الزيادة السكانية الضغط على الخدمات الصحية", "a": True},
    {"q": "سوء توزيع السكان يؤدي إلى اختلال التنمية الإقليمية", "a": True},
    {"q": "الفقر من العوامل المرتبطة بارتفاع معدلات الإنجاب", "a": True},
    {"q": "الهرم السكاني يعكس التركيب العمري والنوعي للسكان", "a": True},
    {"q": "ارتفاع نسبة صغار السن يزيد العبء على الاقتصاد", "a": True},
    {"q": "من سياسات الدولة لمواجهة الزيادة السكانية: التوعية", "a": True},
    {"q": "التمكين الاقتصادي للمرأة يساهم في خفض الإنجاب", "a": True},
    {"q": "الكثافة السكانية هي عدد السكان بالنسبة للمساحة", "a": True},
    {"q": "التكدس الحضري من نتائج سوء التوزيع السكاني", "a": True},
    {"q": "العشوائيات من مظاهر المشكلة السكانية", "a": True},
    {"q": "الهجرة الداخلية تؤدي إلى زيادة الضغط على المدن", "a": True},
    {"q": "الوعي السكاني عنصر أساسي في حل المشكلة", "a": True},
    {"q": "النمو السكاني السريع يعيق التنمية المستدامة", "a": True},
    {"q": "الاستثمار في رأس المال البشري يحول السكان إلى قوة منتجة", "a": True},
    {"q": "التوزيع العادل للسكان يقلل الضغط على الموارد", "a": True},
    {"q": "تقتصر المشكلة السكانية على ارتفاع عدد السكان فقط", "a": False},
    {"q": "يتركز السكان في مصر في مساحة كبيرة من الأرض", "a": False},
    {"q": "ارتفاع معدلات الخصوبة لا يؤثر على النمو السكاني", "a": False},
    {"q": "الهجرة لا تدخل ضمن عناصر النمو السكاني", "a": False},
    {"q": "العلاقة بين السكان والتنمية علاقة طردية دائماً", "a": False},
    {"q": "المواطنة تعني علاقة قانونية وسياسية بين الفرد والدولة", "a": True},
    {"q": "من حقوق المواطن الحق في التعليم", "a": True},
    {"q": "احترام القانون واجب على كل مواطن", "a": True},
    {"q": "المساواة أمام القانون من مبادئ المواطنة", "a": True},
    {"q": "التمييز يتعارض مع المواطنة", "a": True},
    {"q": "الانتخابات وسيلة لممارسة المواطنة", "a": True},
    {"q": "حرية التعبير من الحقوق الأساسية", "a": True},
    {"q": "الحفاظ على الممتلكات العامة واجب وطني", "a": True},
    {"q": "دفع الضرائب يدخل ضمن واجبات المواطن", "a": True},
    {"q": "الانتماء للوطن عنصر أساسي في المواطنة", "a": True},
    {"q": "الفساد يتفق مع مبادئ المواطنة", "a": False},
    {"q": "المواطنة لا ترتبط بالعدالة والمساواة", "a": False},
    {"q": "المواطنة تعني الانعزال عن قضايا المجتمع", "a": False},
    {"q": "المواطنة لا تشمل الالتزام بالقوانين", "a": False},
    {"q": "الفوضى تتفق مع المواطنة", "a": False},
    {"q": "يُعرَّف الفساد بأنه إساءة استخدام السلطة لتحقيق مصالح شخصية", "a": True},
    {"q": "من صور الفساد: الرشوة والمحسوبية", "a": True},
    {"q": "الشفافية من أهم آليات مكافحة الفساد", "a": True},
    {"q": "غياب المساءلة يؤدي إلى انتشار الفساد", "a": True},
    {"q": "الفساد يؤثر سلباً على التنمية الاقتصادية", "a": True},
    {"q": "الشفافية تعني إخفاء المعلومات", "a": False},
    {"q": "الفساد لا يؤثر على الاستثمار", "a": False},
    {"q": "الفساد ظاهرة فردية فقط", "a": False},
    {"q": "مكافحة الفساد مسؤولية الحكومة فقط", "a": False},
    {"q": "الأخلاق لا علاقة لها بمكافحة الفساد", "a": False},
    {"q": "التسامح قيمة إنسانية تقوم على احترام الآخرين", "a": True},
    {"q": "التسامح يعزز التعايش السلمي بين أفراد المجتمع", "a": True},
    {"q": "قبول الاختلاف من أهم مظاهر التسامح", "a": True},
    {"q": "الحوار من أدوات تعزيز التسامح", "a": True},
    {"q": "التسامح لا يعني التنازل عن الحقوق", "a": True},
    {"q": "التسامح يعني التخلي عن المبادئ", "a": False},
    {"q": "التسامح يشجع على الظلم", "a": False},
    {"q": "التسامح يضعف المجتمع", "a": False},
    {"q": "التسامح يزيد من النزاعات", "a": False},
    {"q": "التسامح يعني الاستسلام", "a": False},
    {"q": "العنف ضد المرأة انتهاك لحقوق الإنسان", "a": True},
    {"q": "يشمل العنف ضد المرأة أشكالاً جسدية ونفسية", "a": True},
    {"q": "العنف الأسري من صور العنف ضد المرأة", "a": True},
    {"q": "التعليم يسهم في الحد من العنف", "a": True},
    {"q": "القوانين تجرِّم العنف ضد المرأة", "a": True},
    {"q": "العنف النفسي لا يؤثر على الصحة النفسية", "a": False},
    {"q": "العنف ضد المرأة ظاهرة فردية فقط", "a": False},
    {"q": "العنف ضد المرأة مقبول ثقافياً", "a": False},
    {"q": "القوانين لا تحمي المرأة", "a": False},
    {"q": "العنف لا يؤثر على الأطفال", "a": False},
    {"q": "العولمة تعني تداخل العالم اقتصادياً وثقافياً", "a": True},
    {"q": "وسائل الاتصال ساعدت في انتشار العولمة", "a": True},
    {"q": "العولمة تؤدي إلى تبادل الثقافات", "a": True},
    {"q": "العولمة لها آثار إيجابية وسلبية", "a": True},
    {"q": "التكنولوجيا تعزز العولمة", "a": True},
    {"q": "العولمة تعني الانغلاق", "a": False},
    {"q": "العولمة لا تؤثر على الثقافة", "a": False},
    {"q": "العولمة ليس لها آثار سلبية", "a": False},
    {"q": "العولمة ظاهرة محلية فقط", "a": False},
    {"q": "العولمة لا تؤثر على التواصل", "a": False},
]

user_sessions = {}

def get_session(user_id):
    if user_id not in user_sessions:
        user_sessions[user_id] = {
            "questions": [], "current": 0,
            "score": 0, "total": 0, "active": False
        }
    return user_sessions[user_id]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("▶️ 10 أسئلة", callback_data="quiz_10")],
        [InlineKeyboardButton("▶️ 20 سؤالاً", callback_data="quiz_20")],
        [InlineKeyboardButton("▶️ كل الأسئلة", callback_data="quiz_all")],
    ]
    await update.message.reply_text(
        "🎓 *مرحباً بك في اختبار القضايا*\n\n"
        f"📚 إجمالي الأسئلة: *{len(QUESTIONS)} سؤال*\n"
        "اختر عدد الأسئلة:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    session = get_session(user_id)
    data = query.data

    if data.startswith("quiz_"):
        shuffled = random.sample(QUESTIONS, len(QUESTIONS))
        count = data.split("_")[1]
        if count == "10":
            session["questions"] = shuffled[:10]
        elif count == "20":
            session["questions"] = shuffled[:20]
        else:
            session["questions"] = shuffled
        session["current"] = 0
        session["score"] = 0
        session["total"] = len(session["questions"])
        session["active"] = True
        await send_question(query, session)

    elif data in ["true", "false"] and session.get("active"):
        idx = session["current"] - 1
        if idx < 0 or idx >= len(session["questions"]):
            return
        q = session["questions"][idx]
        user_answer = data == "true"
        correct = q["a"]
        if user_answer == correct:
            session["score"] += 1
            result_text = "✅ *إجابة صحيحة!*"
        else:
            correct_text = "صح ✅" if correct else "غلط ❌"
            result_text = f"❌ *إجابة خاطئة!*\nالصواب: {correct_text}"

        await query.edit_message_text(
            f"{result_text}\n\nالنتيجة: {session['score']}/{session['current']}",
            parse_mode="Markdown"
        )
        await asyncio.sleep(0.8)
        if session["current"] < session["total"]:
            await send_question(query, session)
        else:
            await show_result(query, session)

async def send_question(query, session):
    idx = session["current"]
    q = session["questions"][idx]
    session["current"] += 1
    keyboard = [[
        InlineKeyboardButton("✅ صح", callback_data="true"),
        InlineKeyboardButton("❌ غلط", callback_data="false"),
    ]]
    await query.message.reply_text(
        f"❓ *سؤال {session['current']}/{session['total']}*\n\n{q['q']}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def show_result(query, session):
    score = session["score"]
    total = session["total"]
    percent = int(score / total * 100)
    if percent >= 90: grade = "🏆 ممتاز"
    elif percent >= 75: grade = "🥇 جيد جداً"
    elif percent >= 60: grade = "🥈 جيد"
    elif percent >= 50: grade = "🥉 مقبول"
    else: grade = "❌ يحتاج مراجعة"
    session["active"] = False
    keyboard = [[InlineKeyboardButton("🔄 اختبار جديد", callback_data="quiz_10")]]
    await query.message.reply_text(
        f"🎉 *انتهى الاختبار!*\n\n"
        f"✅ الصح: {score}/{total}\n"
        f"📊 النسبة: {percent}%\n"
        f"التقدير: {grade}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

if __name__ == "__main__":
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("✅ البوت شغال...")
    app.run_polling(drop_pending_updates=True)
