import asyncio
import os
import random
import re
from typing import List, Dict, Any

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton,
    FSInputFile
)

BOT_TOKEN = "8245340349:AAF2sB8Gn5dXiqQQ1ldxAHqk_wpsdcLrH2c"

bot = Bot(BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

PREPARATS_DIR = "preparats"

# РУССКИЕ НАЗВАНИЯ
RUS_NAMES = {
    "amiloidoz_pecheni": "Амилоидоз печени",
    "amiloidoz_pochki": "Амилоидоз почки",
    "amiloidoz_selezenki_sagovaya": "Амилоидоз селезёнки (саговая форма)",
    "amiloidoz_selezenki_salnaya": "Амилоидоз селезёнки (сальная форма)",
    "antrakoz_legkikh": "Антракоз лёгких",
    "buraya_induratsiya_legkogo": "Бурая индурация лёгкого",
    "buraya_induratsiya_pecheni": "Бурая индурация печени",
    "difteriticheskii_enterit": "Дифтеритический энтерит",
    "fibrinoznyi_perikardit": "Фибринозный перикардит",
    "gemorragicheskii_infarkt_legkogo": "Геморрагический инфаркт лёгкого",
    "gemorragicheskii_infarkt_pochki": "Геморрагический инфаркт почки",
    "gemorragicheskoe_vospalenie_kishechnika": "Геморрагическое воспаление кишечника",
    "gialinovo_kapelnaya_distrofiya_pochki": "Гиалиново-капельная дистрофия почки",
    "gialinoz_selezenki": "Гиалиноз селезёнки",
    "gialinoz_stenki_sosuda_matki": "Гиалиноз стенки сосуда матки",
    "gnoinyi_nefrit": "Гнойный нефрит",
    "hemosideroz_pecheni": "Гемосидероз печени",
    "hemosideroz_pecheni_muskatnaya": "Гемосидероз печени (мускатная печень)",
    "hemosideroz_selezenki_ge": "Гемосидероз селезёнки (ГЭ)",
    "hemosideroz_selezenki_perls": "Гемосидероз селезёнки (Перлс)",
    "ishemicheskii_infarkt_pochki": "Ишемический инфаркт почки",
    "ishemicheskii_infarkt_selezenki": "Ишемический инфаркт селезёнки",
    "khronicheskii_abscess_pecheni": "Хронический абсцесс печени",
    "khronicheskii_kataralnyi_enterit_ge": "Хронический катаральный энтерит (ГЭ)",
    "khronicheskii_kataralnyi_enterit_sudan": "Хронический катаральный энтерит (Судан III)",
    "khronicheskoe_venoznoe_polnokrovie_muskatnaya_pechen": "Хроническое венозное полнокровие (мускатная печень)",
    "kolloidnaya_distrofiya_shchitovidnoi": "Коллоидная дистрофия щитовидной железы",
    "krupoznaya_pnevmoniya": "Крупозная пневмония",
    "melanoz_pecheni": "Меланоз печени",
    "nekroticheskii_nefroz": "Некротический нефроз",
    "ostraya_zastoynaya_giperemiya_otek_legkikh": "Острая застойная гиперемия и отёк лёгких",
    "ostraya_zastoynaya_venoznaya_giperemiya_pecheni": "Острая застойная венозная гиперемия печени",
    "ostryi_seroznyi_gastrit": "Острый серозный гастрит",
    "serozno_gemorragicheskaya_pnevmoniya": "Серозно-геморрагическая пневмония",
    "seroznoe_vosp_legkikh": "Серозное воспаление лёгких",
    "smeshannyi_tromb": "Смешанный тромб",
    "tsenkerovskii_voskovidnyi_nekroz_myshc": "Ценкеровский (восковидный) некроз мышц",
    "tvorozhistyi_nekroz_legkikh_tb": "Творожистый некроз лёгких при туберкулёзе",
    "tvorozhistyi_nekroz_lymph_tb": "Творожистый (казеозный) некроз лимфоузла при туберкулёзе",
    "vakuolnaya_distrofiya_pochki": "Вакуольная дистрофия почки",
    "zernistaya_distrofiya_pecheni": "Зернистая дистрофия печени",
    "zernistaya_distrofiya_pochki": "Зернистая дистрофия почки",
    "zhirovaia_distrofiya_pecheni": "Жировая дистрофия печени"
}

SPECIMENS = []
user_state = {}


# ---------- загрузка файлов ----------
def load_specimens():
    groups = {}

    for fname in os.listdir(PREPARATS_DIR):
        if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        base = re.sub(r"[_\.\- ]?\d+$", "", fname.split(".")[0])
        full = os.path.join(PREPARATS_DIR, fname)

        groups.setdefault(base, []).append(full)

    specimens = []
    i = 1
    for base, imgs in groups.items():
        rus = RUS_NAMES.get(base, base)

        specimens.append({
            "id": i,
            "base": base,
            "name": rus,
            "images": sorted(imgs),
            "aliases": [rus, rus.lower()]
        })
        i += 1

    return specimens


# ---------- клавиатуры ----------
def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📚 Обучение")],
            [KeyboardButton(text="🧪 Тест (лёгкий)"),
             KeyboardButton(text="🔥 Тест (сложный)")]
        ],
        resize_keyboard=True
    )


def next_btn(mode):
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="➡️ Далее", callback_data=f"next:{mode}")]]
    )


# ---------- HANDLERS ----------

@dp.message(CommandStart())
async def start(msg: Message):
    await msg.answer(
        "Привет! 👋\nВыбери режим:",
        reply_markup=main_menu()
    )


# ------- ОБУЧЕНИЕ -------
@dp.message(F.text == "📚 Обучение")
async def training(msg: Message):
    specimen = random.choice(SPECIMENS)

    # все фото
    for img in specimen["images"]:
        await msg.answer_photo(FSInputFile(img))

    await msg.answer(
        f"<b>{specimen['name']}</b>",
        reply_markup=next_btn("train")
    )


# ------- ЛЁГКИЙ ТЕСТ -------
@dp.message(F.text == "🧪 Тест (лёгкий)")
async def test_easy(msg: Message):
    specimen = random.choice(SPECIMENS)

    others = [s for s in SPECIMENS if s != specimen]
    distractors = random.sample(others, 3)

    variants = [specimen["name"]] + [d["name"] for d in distractors]
    random.shuffle(variants)

    user_state[msg.from_user.id] = {
        "mode": "easy",
        "correct": specimen["name"],
        "variants": variants
    }

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=v, callback_data=f"var:{i}")]
            for i, v in enumerate(variants)
        ]
    )

    await msg.answer_photo(
        FSInputFile(random.choice(specimen["images"])),
        caption="Выбери правильный вариант:",
        reply_markup=kb
    )


@dp.callback_query(F.data.startswith("var:"))
async def easy_answer(cb: CallbackQuery):
    st = user_state.get(cb.from_user.id)
    idx = int(cb.data.split(":")[1])
    chosen = st["variants"][idx]
    correct = st["correct"]

    if chosen == correct:
        txt = f"✅ Верно! Это <b>{correct}</b>"
    else:
        txt = f"❌ Неверно.\nТы выбрала: {chosen}\nПравильный ответ: <b>{correct}</b>"

    await cb.message.answer(txt, reply_markup=next_btn("easy"))
    await cb.answer()


# ------- СЛОЖНЫЙ ТЕСТ -------
@dp.message(F.text == "🔥 Тест (сложный)")
async def hard_test(msg: Message):
    specimen = random.choice(SPECIMENS)

    user_state[msg.from_user.id] = {
        "mode": "hard",
        "correct": specimen["name"]
    }

    await msg.answer_photo(
        FSInputFile(random.choice(specimen["images"])),
        caption="Введи название препарата:"
    )


@dp.message()
async def check_hard(msg: Message):
    st = user_state.get(msg.from_user.id)
    if not st or st["mode"] != "hard":
        return

    user = msg.text.strip().lower()
    correct = st["correct"].lower()

    if user == correct:
        txt = f"✅ Верно! Это <b>{st['correct']}</b>"
    else:
        txt = f"❌ Неверно.\nПравильный ответ: <b>{st['correct']}</b>"

    await msg.answer(txt, reply_markup=next_btn("hard"))


# ------- КНОПКА "ДАЛЕЕ" -------
@dp.callback_query(F.data.startswith("next:"))
async def next_action(cb: CallbackQuery):
    mode = cb.data.split(":")[1]
    if mode == "train":
        await training(cb.message)
    elif mode == "easy":
        await test_easy(cb.message)
    elif mode == "hard":
        await hard_test(cb.message)

    await cb.answer()


async def main():
    global SPECIMENS
    SPECIMENS = load_specimens()

    print(f"Загружено препаратов: {len(SPECIMENS)}")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
