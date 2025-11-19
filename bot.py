import os
import random
from dataclasses import dataclass
from typing import List, Dict, Optional

import telebot
from telebot import types


# =========================
# НАСТРОЙКИ
# =========================

BOT_TOKEN = "8245340349:AAF2sB8Gn5dXiqQQ1ldxAHqk_wpsdcLrH2c"

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")


# =========================
# ДАННЫЕ О ПРЕПАРАТАХ
# =========================

@dataclass
class Preparat:
    id: str
    name: str
    category: str
    files: List[str]


# Загружаем все препараты (которые ты использовала)
PREPARATS: List[Preparat] = [
    # ————— Амилоидозы —————
    Preparat("amiloidoz_pecheni", "Амилоидоз печени", "Амилоидозы",
             ["amiloidoz_pecheni_1.jpeg", "amiloidoz_pecheni_2.jpeg", "amiloidoz_pecheni_3.jpeg"]),
    Preparat("amiloidoz_pochki", "Амилоидоз почки", "Амилоидозы",
             ["amiloidoz_pochki_1.jpeg", "amiloidoz_pochki_2.jpeg"]),
    Preparat("amiloidoz_selezenki_sagovaya", "Амилоидоз селезёнки («саговая» форма)", "Амилоидозы",
             ["amiloidoz_selezenki_sagovaya_1.jpeg", "amiloidoz_selezenki_sagovaya_2.jpeg"]),
    Preparat("amiloidoz_selezenki_salnaya", "Амилоидоз селезёнки («сальная» форма)", "Амилоидозы",
             ["amiloidoz_selezenki_salnaya_1.jpeg", "amiloidoz_selezenki_salnaya_2.jpeg", "amiloidoz_selezenki_salnaya_3.jpeg"]),

    # ————— Воспаление —————
    Preparat("serozno_gemorragicheskaya_pnevmoniya", "Серозно-геморрагическая пневмония", "Воспаление",
             ["serozno_gemorragicheskaya_pnevmoniya_1.jpeg",
              "serozno_gemorragicheskaya_pnevmoniya_2.jpeg",
              "serozno_gemorragicheskaya_pnevmoniya_3.jpeg"]),
    Preparat("seroznoe_vosp_legkikh", "Серозное воспаление лёгких", "Воспаление",
             ["seroznoe_vosp_legkikh_1.jpeg", "seroznoe_vosp_legkikh_2.jpeg", "seroznoe_vosp_legkikh_3.jpeg"]),
    Preparat("ostryi_seroznyi_gastrit", "Острый серозный гастрит", "Воспаление",
             ["ostryi_seroznyi_gastrit_1.jpeg", "ostryi_seroznyi_gastrit_2.jpeg",
              "ostryi_seroznyi_gastrit_3.jpeg", "ostryi_seroznyi_gastrit_4.jpeg"]),
    Preparat("krupoznaya_pnevmoniya", "Крупозная пневмония", "Воспаление",
             ["krupoznaya_pnevmoniya_1.jpeg", "krupoznaya_pnevmoniya_2.jpeg"]),

    # ————— Дистрофии —————
    Preparat("zernistaya_distrofiya_pochki", "Зернистая дистрофия почки", "Дистрофии",
             ["zernistaya_distrofiya_pochki_1.jpeg", "zernistaya_distrofiya_pochki_2.jpeg"]),
    Preparat("zernistaya_distrofiya_pecheni", "Зернистая дистрофия печени", "Дистрофии",
             ["zernistaya_distrofiya_pecheni_1.jpeg", "zernistaya_distrofiya_pecheni_2.jpeg"]),
    Preparat("gialinovo_kapelnaya_distrofiya_pochki", "Гиалиново-капельная дистрофия почки", "Дистрофии",
             ["gialinovo_kapelnaya_distrofiya_pochki_1.jpeg", "gialinovo_kapelnaya_distrofiya_pochki_2.jpeg",
              "gialinovo_kapelnaya_distrofiya_pochki_3.jpeg"]),

    # ————— Гиалинозы —————
    Preparat("gialinoz_stenki_sosuda_matki", "Гиалиноз стенки сосуда матки", "Гиалинозы",
             ["gialinoz_stenki_sosuda_matki_1.jpeg", "gialinoz_stenki_sosuda_matki_2.jpeg",
              "gialinoz_stenki_sosuda_matki_3.jpeg"]),
    Preparat("gialinoz_selezenki", "Гиалиноз селезёнки", "Гиалинозы",
             ["gialinoz_selezenki_1.jpeg", "gialinoz_selezenki_2.jpeg", "gialinoz_selezenki_3.jpeg"]),

    # ————— Пигменты —————
    Preparat("hemosideroz_pecheni", "Гемосидероз печени", "Пигменты",
             ["hemosideroz_pecheni_1.jpeg", "hemosideroz_pecheni_2.jpeg"]),
    Preparat("melanoz_pecheni", "Меланоз печени", "Пигменты",
             ["melanoz_pecheni_1.jpeg", "melanoz_pecheni_2.jpeg", "melanoz_pecheni_3.jpeg"]),
    Preparat("antrakoz_legkikh", "Антракоз лёгких", "Пигменты",
             ["antrakoz_legkikh_1.jpeg", "antrakoz_legkikh_2.jpeg", "antrakoz_legkikh_3.jpeg"]),

    # ————— Некрозы —————
    Preparat("nekroticheskii_nefroz", "Некротический нефроз", "Некроз",
             ["nekroticheskii_nefroz_1.jpeg", "nekroticheskii_nefroz_2.jpeg", "nekroticheskii_nefroz_3.jpeg"]),

    # ————— Кровообращение —————
    Preparat("buraya_induratsiya_pecheni", "Бурая индурация печени", "Кровообращение",
             ["buraya_induratsiya_pecheni_1.jpeg", "buraya_induratsiya_pecheni_2.jpeg"]),

    # ————— Инфаркты —————
    Preparat("ishemicheskii_infarkt_pochki", "Ишемический инфаркт почки", "Инфаркты",
             ["ishemicheskii_infarkt_pochki_1.jpeg", "ishemicheskii_infarkt_pochki_2.jpeg"]),

    # ————— Тромбоз —————
    Preparat("smeshannyi_tromb", "Смешанный тромб", "Тромбоз",
             ["smeshannyi_tromb_1.jpeg", "smeshannyi_tromb_2.jpeg"]),
]


PREP_BY_ID = {p.id: p for p in PREPARATS}

CATEGORIES = sorted(set(p.category for p in PREPARATS))


# =========================
# СОСТОЯНИЯ ПОЛЬЗОВАТЕЛЕЙ
# =========================

user_state: Dict[int, Dict] = {}
user_stats: Dict[int, Dict] = {}


def get_stats(uid: int):
    if uid not in user_stats:
        user_stats[uid] = {"total": 0, "correct": 0, "wrong": 0, "errors": set()}
    return user_stats[uid]


# =========================
# КНОПКИ
# =========================

def main_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("📚 Обучение")
    kb.add("❓ Тест (варианты)", "⌨️ Тест (ввод)")
    kb.add("📊 Статистика", "🔁 Повторить ошибки")
    return kb


def training_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("➡️ Следующий")
    kb.add("⬅️ Назад к разделам")
    kb.add("🏠 Выйти в меню")
    return kb


# =========================
# ОБУЧЕНИЕ
# =========================

def start_training(uid: int, category: str):
    """Подготовка списка без повторов."""
    ids = [p.id for p in PREPARATS if p.category == category]
    random.shuffle(ids)
    user_state[uid] = {
        "mode": "train",
        "category": category,
        "remaining": ids,
    }


def get_next(uid: int) -> Optional[Preparat]:
    st = user_state.get(uid)
    if not st or st.get("mode") != "train":
        return None

    if not st["remaining"]:
        return None

    pid = st["remaining"].pop()
    st["current"] = pid
    return PREP_BY_ID[pid]


def send_prep(chat_id: int, prep: Preparat):
    bot.send_message(chat_id, f"<b>{prep.name}</b>", reply_markup=training_kb())
    for f in prep.files:
        path = os.path.join("preparats", f)
        if os.path.exists(path):
            with open(path, "rb") as p:
                bot.send_photo(chat_id, p)
        else:
            bot.send_message(chat_id, f"Файл отсутствует: {path}")


# =========================
# ТЕСТЫ
# =========================

def normalize(t: str):
    return t.lower().replace("ё", "е").strip()


def ask_mcq(chat_id, uid, from_errors=False):
    stats = get_stats(uid)

    if from_errors:
        if not stats["errors"]:
            bot.send_message(chat_id, "Пока нет ошибок 😊", reply_markup=main_kb())
            return
        pid = random.choice(list(stats["errors"]))
        prep = PREP_BY_ID[pid]
    else:
        prep = random.choice(PREPARATS)

    options = [prep] + random.sample([p for p in PREPARATS if p.id != prep.id], 3)
    random.shuffle(options)

    kb = types.InlineKeyboardMarkup()
    for p in options:
        kb.add(types.InlineKeyboardButton(text=p.name, callback_data=f"ans:{p.id}"))

    user_state[uid] = {"mode": "mcq", "correct": prep.id, "from_errors": from_errors}

    # фото
    path = os.path.join("preparats", prep.files[0])
    with open(path, "rb") as ph:
        bot.send_photo(chat_id, ph, caption="Что за препарат?", reply_markup=kb)


def ask_typing(chat_id, uid, from_errors=False):
    stats = get_stats(uid)

    if from_errors:
        if not stats["errors"]:
            bot.send_message(chat_id, "Пока нет ошибок 😊", reply_markup=main_kb())
            return
        pid = random.choice(list(stats["errors"]))
        prep = PREP_BY_ID[pid]
    else:
        prep = random.choice(PREPARATS)

    user_state[uid] = {"mode": "typing", "correct": prep.id, "from_errors": from_errors}

    # фото
    path = os.path.join("preparats", prep.files[0])
    with open(path, "rb") as ph:
        bot.send_photo(chat_id, ph)

    bot.send_message(chat_id, "Введите название препарата:")


# =========================
# ХЕНДЛЕРЫ
# =========================

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет! Выбирай режим 🧬", reply_markup=main_kb())


# ——— ОБУЧЕНИЕ ———

@bot.message_handler(func=lambda m: m.text == "📚 Обучение")
def menu_training(m):
    kb = types.InlineKeyboardMarkup()
    for c in CATEGORIES:
        kb.add(types.InlineKeyboardButton(text=c, callback_data=f"cat:{c}"))
    bot.send_message(m.chat.id, "Выбери раздел:", reply_markup=kb)


@bot.callback_query_handler(func=lambda c: c.data.startswith("cat:"))
def pick_cat(cb):
    cat = cb.data.split(":", 1)[1]
    uid = cb.from_user.id

    start_training(uid, cat)
    prep = get_next(uid)

    bot.answer_callback_query(cb.id, f"Раздел: {cat}")

    if prep:
        send_prep(cb.message.chat.id, prep)
    else:
        bot.send_message(cb.message.chat.id, "В разделе нет препаратов.", reply_markup=main_kb())


@bot.message_handler(func=lambda m: m.text == "➡️ Следующий")
def next_one(m):
    uid = m.from_user.id
    prep = get_next(uid)

    if not prep:
        bot.send_message(m.chat.id, "Раздел пройден 🎉", reply_markup=main_kb())
        return

    send_prep(m.chat.id, prep)


@bot.message_handler(func=lambda m: m.text == "⬅️ Назад к разделам")
def back_to_cats(m):
    user_state.pop(m.from_user.id, None)
    menu_training(m)


@bot.message_handler(func=lambda m: m.text == "🏠 Выйти в меню")
def exit_to_menu(m):
    user_state.pop(m.from_user.id, None)
    bot.send_message(m.chat.id, "Возврат в меню 😊", reply_markup=main_kb())


# ——— Тест (варианты) ———

@bot.message_handler(func=lambda m: m.text == "❓ Тест (варианты)")
def test_mcq(m):
    ask_mcq(m.chat.id, m.from_user.id)


@bot.message_handler(func=lambda m: m.text == "🔁 Повторить ошибки")
def test_errors(m):
    ask_mcq(m.chat.id, m.from_user.id, from_errors=True)


@bot.callback_query_handler(func=lambda c: c.data.startswith("ans:"))
def answer(cb):
    uid = cb.from_user.id
    st = user_state.get(uid)

    if not st or st.get("mode") != "mcq":
        bot.answer_callback_query(cb.id, "Вопрос устарел")
        return

    chosen = cb.data.split(":", 1)[1]
    correct = st["correct"]
    from_errors = st["from_errors"]

    stats = get_stats(uid)
    stats["total"] += 1

    if chosen == correct:
        bot.answer_callback_query(cb.id, "Верно!")
        stats["correct"] += 1
        stats["errors"].discard(correct)
    else:
        bot.answer_callback_query(cb.id, "Неверно 😢")
        stats["wrong"] += 1
        stats["errors"].add(correct)

    ask_mcq(cb.message.chat.id, uid, from_errors)


# ——— Тест (ввод) ———

@bot.message_handler(func=lambda m: m.text == "⌨️ Тест (ввод)")
def test_typing(m):
    ask_typing(m.chat.id, m.from_user.id)


@bot.message_handler(
    func=lambda m: user_state.get(m.from_user.id, {}).get("mode") == "typing"
)
def typing_answer(m):
    uid = m.from_user.id
    st = user_state[uid]
    correct = PREP_BY_ID[st["correct"]]
    stats = get_stats(uid)

    user = normalize(m.text)
    right = normalize(correct.name)

    stats["total"] += 1

    words = [w for w in right.split() if len(w) > 3]

    if any(w in user for w in words):
        stats["correct"] += 1
        stats["errors"].discard(correct.id)
        bot.send_message(m.chat.id, f"✅ Правильно! Это <b>{correct.name}</b>.")
    else:
        stats["wrong"] += 1
        stats["errors"].add(correct.id)
        bot.send_message(m.chat.id, f"❌ Неверно!\nПравильный ответ: <b>{correct.name}</b>.")

    ask_typing(m.chat.id, uid, st["from_errors"])


# ——— Статистика ———

@bot.message_handler(func=lambda m: m.text == "📊 Статистика")
def stats_cmd(m):
    s = get_stats(m.from_user.id)

    acc = round(s["correct"] * 100 / s["total"], 1) if s["total"] else 0

    bot.send_message(
        m.chat.id,
        f"<b>Статистика:</b>\n"
        f"Всего вопросов: <b>{s['total']}</b>\n"
        f"Правильно: <b>{s['correct']}</b>\n"
        f"Ошибок: <b>{s['wrong']}</b>\n"
        f"Точность: <b>{acc}%</b>\n"
        f"В списке ошибок: <b>{len(s['errors'])}</b>",
        reply_markup=main_kb(),
    )


# =========================
# ЗАПУСК
# =========================

print("Бот запущен")
bot.infinity_polling()
    
    

    
    
