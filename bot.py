import asyncio
import random
from dataclasses import dataclass
from typing import List, Dict
from difflib import SequenceMatcher

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

# ============================================================
#   ТОКЕН
# ============================================================
BOT_TOKEN = "8245340349:AAF2sB8Gn5dXiqQQ1ldxAHqk_wpsdcLrH2c"

# ============================================================
#   ДАННЫЕ О ПРЕПАРАТАХ
# ============================================================

BASE_URL = "https://raw.githubusercontent.com/lapinaalina845-ux/tg-pathanat-bot/main/preparats/"

@dataclass
class Preparat:
    id: str
    name: str
    category: str
    files: List[str]

# ---------- СПИСОК ПРЕПАРАТОВ ----------
PREPARATS: List[Preparat] = [
    # --- Амилоидозы ---
    Preparat(
        id="amiloidoz_pecheni",
        name="Амилоидоз печени",
        category="Амилоидозы",
        files=[
            "amiloidoz_pecheni_1.jpeg",
            "amiloidoz_pecheni_2.jpeg",
            "amiloidoz_pecheni_3.jpeg",
        ],
    ),
    Preparat(
        id="amiloidoz_pochki",
        name="Амилоидоз почки",
        category="Амилоидозы",
        files=[
            "amiloidoz_pochki_1.jpeg",
            "amiloidoz_pochki_2.jpeg",
        ],
    ),
    Preparat(
        id="amiloidoz_selezenki_sagovaya",
        name="Амилоидоз селезёнки («саговая» форма)",
        category="Амилоидозы",
        files=[
            "amiloidoz_selezenki_sagovaya_1.jpeg",
            "amiloidoz_selezenki_sagovaya_2.jpeg",
        ],
    ),
    Preparat(
        id="amiloidoz_selezenki_salnaya",
        name="Амилоидоз селезёнки («сальная» форма)",
        category="Амилоидозы",
        files=[
            "amiloidoz_selezenki_salnaya_1.jpeg",
            "amiloidoz_selezenki_salnaya_2.jpeg",
            "amiloidoz_selezenki_salnaya_3.jpeg",
        ],
    ),

    # --- Воспаление ---
    Preparat(
        id="serozno_gemorragicheskaya_pnevmoniya",
        name="Серозно-геморрагическая пневмония",
        category="Воспаление",
        files=[
            "serozno_gemorragicheskaya_pnevmoniya_1.jpeg",
            "serozno_gemorragicheskaya_pnevmoniya_2.jpeg",
            "serozno_gemorragicheskaya_pnevmoniya_3.jpeg",
        ],
    ),
    Preparat(
        id="seroznoe_vosp_legkikh",
        name="Серозное воспаление лёгких",
        category="Воспаление",
        files=[
            "seroznoe_vosp_legkikh_1.jpeg",
            "seroznoe_vosp_legkikh_2.jpeg",
            "seroznoe_vosp_legkikh_3.jpeg",
        ],
    ),
    Preparat(
        id="ostryi_seroznyi_gastrit",
        name="Острый серозный гастрит",
        category="Воспаление",
        files=[
            "ostryi_seroznyi_gastrit_1.jpeg",
            "ostryi_seroznyi_gastrit_2.jpeg",
            "ostryi_seroznyi_gastrit_3.jpeg",
            "ostryi_seroznyi_gastrit_4.jpeg",
        ],
    ),
    Preparat(
        id="krupoznaya_pnevmoniya",
        name="Крупозная пневмония",
        category="Воспаление",
        files=[
            "krupoznaya_pnevmoniya_1.jpeg",
            "krupoznaya_pnevmoniya_2.jpeg",
        ],
    ),
    Preparat(
        id="fibrinoznyi_perikardit",
        name="Фибринозный перикардит",
        category="Воспаление",
        files=[
            "fibrinoznyi_perikardit_1.jpeg",
            "fibrinoznyi_perikardit_2.jpeg",
            "fibrinoznyi_perikardit_3.jpeg",
        ],
    ),
    Preparat(
        id="difteriticheskii_enterit",
        name="Дифтеритический энтерит",
        category="Воспаление",
        files=[
            "difteriticheskii_enterit_1.jpeg",
            "difteriticheskii_enterit_2.jpeg",
        ],
    ),
    Preparat(
        id="gemorragicheskoe_vospalenie_kishechnika",
        name="Геморрагическое воспаление кишечника",
        category="Воспаление",
        files=[
            "gemorragicheskoe_vospalenie_kishechnika_1.jpeg",
            "gemorragicheskoe_vospalenie_kishechnika_2.jpeg",
            "gemorragicheskoe_vospalenie_kishechnika_3.jpeg",
        ],
    ),
    Preparat(
        id="gnoinyi_nefrit",
        name="Гнойный нефрит",
        category="Воспаление",
        files=[
            "gnoinyi_nefrit_1.jpeg",
            "gnoinyi_nefrit_2.jpeg",
            "gnoinyi_nefrit_3.jpeg",
            "gnoinyi_nefrit_4.jpeg",
        ],
    ),
    Preparat(
        id="khronicheskii_abscess_pecheni",
        name="Хронический абсцесс печени",
        category="Воспаление",
        files=[
            "khronicheskii_abscess_pecheni_1.jpeg",
        ],
    ),
    Preparat(
        id="khronicheskii_kataralnyi_enterit_ge",
        name="Хронический катаральный энтерит (гематоксилин-эозин)",
        category="Воспаление",
        files=[
            "khronicheskii_kataralnyi_enterit_ge_1.jpeg",
            "khronicheskii_kataralnyi_enterit_ge_2.jpeg",
            "khronicheskii_kataralnyi_enterit_ge_3.jpeg",
            "khronicheskii_kataralnyi_enterit_ge_4.jpeg",
        ],
    ),
    Preparat(
        id="khronicheskii_kataralnyi_enterit_sudan",
        name="Хронический катаральный энтерит (Судан III)",
        category="Воспаление",
        files=[
            "khronicheskii_kataralnyi_enterit_sudan_1.jpeg",
            "khronicheskii_kataralnyi_enterit_sudan_2.jpeg",
            "khronicheskii_kataralnyi_enterit_sudan_3.jpeg",
        ],
    ),

    # --- Дистрофии ---
    Preparat(
        id="zernistaya_distrofiya_pochki",
        name="Зернистая дистрофия почки",
        category="Дистрофии",
        files=[
            "zernistaya_distrofiya_pochki_1.jpeg",
            "zernistaya_distrofiya_pochki_2.jpeg",
        ],
    ),
    Preparat(
        id="zernistaya_distrofiya_pecheni",
        name="Зернистая дистрофия печени",
        category="Дистрофии",
        files=[
            "zernistaya_distrofiya_pecheni_1.jpeg",
            "zernistaya_distrofiya_pecheni_2.jpeg",
        ],
    ),
    Preparat(
        id="gialinovo_kapelnaya_distrofiya_pochki",
        name="Гиалиново-капельная дистрофия почки",
        category="Дистрофии",
        files=[
            "gialinovo_kapelnaya_distrofiya_pochki_1.jpeg",
            "gialinovo_kapelnaya_distrofiya_pochki_2.jpeg",
            "gialinovo_kapelnaya_distrofiya_pochki_3.jpeg",
        ],
    ),
    Preparat(
        id="vakuolnaya_distrofiya_pochki",
        name="Вакуольная дистрофия почки",
        category="Дистрофии",
        files=[
            "vakuolnaya_distrofiya_pochki_1.jpeg",
        ],
    ),
    Preparat(
        id="kolloidnaya_distrofiya_shchitovidnoi",
        name="Коллоидная дистрофия щитовидной железы",
        category="Дистрофии",
        files=[
            "kolloidnaya_distrofiya_shchitovidnoi_1.jpeg",
            "kolloidnaya_distrofiya_shchitovidnoi_2.jpeg",
        ],
    ),
    Preparat(
        id="zhirovaia_distrofiya_pecheni",
        name="Жировая дистрофия печени",
        category="Дистрофии",
        files=[
            "zhirovaia_distrofiya_pecheni_1.jpeg",
            "zhirovaia_distrofiya_pecheni_2.jpeg",
        ],
    ),

    # --- Гиалиноз ---
    Preparat(
        id="gialinoz_stenki_sosuda_matki",
        name="Гиалиноз стенки сосуда матки",
        category="Гиалинозы",
        files=[
            "gialinoz_stenki_sosuda_matki_1.jpeg",
            "gialinoz_stenki_sosuda_matki_2.jpeg",
            "gialinoz_stenki_sosuda_matki_3.jpeg",
        ],
    ),
    Preparat(
        id="gialinoz_selezenki",
        name="Гиалиноз селезёнки",
        category="Гиалинозы",
        files=[
            "gialinoz_selezenki_1.jpeg",
            "gialinoz_selezenki_2.jpeg",
            "gialinoz_selezenki_3.jpeg",
        ],
    ),

    # --- Пигменты ---
    Preparat(
        id="hemosideroz_pecheni",
        name="Гемосидероз печени",
        category="Пигменты",
        files=[
            "hemosideroz_pecheni_1.jpeg",
            "hemosideroz_pecheni_2.jpeg",
        ],
    ),
    Preparat(
        id="hemosideroz_pecheni_muskatnaya",
        name="Гемосидероз печени («мускатная печень»)",
        category="Пигменты",
        files=[
            "hemosideroz_pecheni_muskatnaya_1.jpeg",
            "hemosideroz_pecheni_muskatnaya_2.jpeg",
            "hemosideroz_pecheni_muskatnaya_3.jpeg",
        ],
    ),
    Preparat(
        id="hemosideroz_selezenki_ge",
        name="Гемосидероз селезёнки (гематоксилин-эозин)",
        category="Пигменты",
        files=[
            "hemosideroz_selezenki_ge_1.jpeg",
            "hemosideroz_selezenki_ge_2.jpeg",
            "hemosideroz_selezenki_ge_3.jpeg",
            "hemosideroz_selezenki_ge_4.jpeg",
        ],
    ),
    Preparat(
        id="hemosideroz_selezenki_perls",
        name="Гемосидероз селезёнки (Перлс)",
        category="Пигменты",
        files=[
            "hemosideroz_selezenki_perls_1.jpeg",
            "hemosideroz_selezenki_perls_2.jpeg",
            "hemosideroz_selezenki_perls_3.jpeg",
            "hemosideroz_selezenki_perls_4.jpeg",
        ],
    ),
    Preparat(
        id="melanoz_pecheni",
        name="Меланоз печени",
        category="Пигменты",
        files=[
            "melanoz_pecheni_1.jpeg",
            "melanoz_pecheni_2.jpeg",
            "melanoz_pecheni_3.jpeg",
        ],
    ),
    Preparat(
        id="antrakoz_legkikh",
        name="Антракоз лёгких",
        category="Пигменты",
        files=[
            "antrakoz_legkikh_1.jpeg",
            "antrakoz_legkikh_2.jpeg",
            "antrakoz_legkikh_3.jpeg",
        ],
    ),

    # --- Некроз ---
    Preparat(
        id="nekroticheskii_nefroz",
        name="Некротический нефроз",
        category="Некроз",
        files=[
            "nekroticheskii_nefroz_1.jpeg",
            "nekroticheskii_nefroz_2.jpeg",
            "nekroticheskii_nefroz_3.jpeg",
        ],
    ),
    Preparat(
        id="tvorozhistyi_nekroz_lymph_tb",
        name="Творожистый некроз лимфоузла (туберкулёз)",
        category="Некроз",
        files=[
            "tvorozhistyi_nekroz_lymph_tb_1.jpeg",
            "tvorozhistyi_nekroz_lymph_tb_2.jpeg",
        ],
    ),
    Preparat(
        id="tsenkerovskii_voskovidnyi_nekroz_myshc",
        name="Ценкеровский некроз мышц",
        category="Некроз",
        files=[
            "tsenkerovskii_voskovidnyi_nekroz_myshc_1.jpeg",
            "tsenkerovskii_voskovidnyi_nekroz_myshc_2.jpeg",
        ],
    ),
    Preparat(
        id="tvorozhistyi_nekroz_legkikh_tb",
        name="Творожистый некроз лёгких (туберкулёз)",
        category="Некроз",
        files=[
            "tvorozhistyi_nekroz_legkikh_tb_1.jpeg",
            "tvorozhistyi_nekroz_legkikh_tb_2.jpeg",
        ],
    ),

    # --- Кровообращение ---
    Preparat(
        id="buraya_induratsiya_pecheni",
        name="Бурая индурация печени",
        category="Кровообращение",
        files=[
            "buraya_induratsiya_pecheni_1.jpeg",
            "buraya_induratsiya_pecheni_2.jpeg",
        ],
    ),
    Preparat(
        id="ostraya_zastoynaya_venoznaya_giperemiya_pecheni",
        name="Острая застойная венозная гиперемия печени",
        category="Кровообращение",
        files=[
            "ostraya_zastoynaya_venoznaya_giperemiya_pecheni_1.jpeg",
            "ostraya_zastoynaya_venoznaya_giperemiya_pecheni_2.jpeg",
        ],
    ),
    Preparat(
        id="khronicheskoe_venoznoe_polnokrovie_muskatnaya_pechen",
        name="Хроническое венозное полнокровие печени («мускатная печень»)",
        category="Кровообращение",
        files=[
            "khronicheskoe_venoznoe_polnokrovie_muskatnaya_pechen_1.jpeg",
            "khronicheskoe_venoznoe_polnokrovie_muskatnaya_pechen_2.jpeg",
        ],
    ),
    Preparat(
        id="ostraya_zastoynaya_giperemiya_otek_legkikh",
        name="Острая застойная гиперемия и отёк лёгких",
        category="Кровообращение",
        files=[
            "ostraya_zastoynaya_giperemiya_otek_legkikh_1.jpeg",
            "ostraya_zastoynaya_giperemiya_otek_legkikh_2.jpeg",
        ],
    ),
    Preparat(
        id="buraya_induratsiya_legkogo",
        name="Бурая индурация лёгкого",
        category="Кровообращение",
        files=[
            "buraya_induratsiya_legkogo_1.jpeg",
            "buraya_induratsiya_legkogo_2.jpeg",
        ],
    ),

    # --- Инфаркты ---
    Preparat(
        id="ishemicheskii_infarkt_pochki",
        name="Ишемический инфаркт почки",
        category="Инфаркты",
        files=[
            "ishemicheskii_infarkt_pochki_1.jpeg",
            "ishemicheskii_infarkt_pochki_2.jpeg",
        ],
    ),
    Preparat(
        id="ishemicheskii_infarkt_selezenki",
        name="Ишемический инфаркт селезёнки",
        category="Инфаркты",
        files=[
            "ishemicheskii_infarkt_selezenki_1.jpeg",
            "ishemicheskii_infarkt_selezenki_2.jpeg",
        ],
    ),
    Preparat(
        id="gemorragicheskii_infarkt_pochki",
        name="Геморрагический инфаркт почки",
        category="Инфаркты",
        files=[
            "gemorragicheskii_infarkt_pochki_1.jpeg",
            "gemorragicheskii_infarkt_pochki_2.jpeg",
            "gemorragicheskii_infarkt_pochki_3.jpeg",
        ],
    ),
    Preparat(
        id="gemorragicheskii_infarkt_legkogo",
        name="Геморрагический инфаркт лёгкого",
        category="Инфаркты",
        files=[
            "gemorragicheskii_infarkt_legkogo_1.jpeg",
            "gemorragicheskii_infarkt_legkogo_2.jpeg",
        ],
    ),

    # --- Тромбоз ---
    Preparat(
        id="smeshannyi_tromb",
        name="Смешанный тромб",
        category="Тромбоз",
        files=[
            "smeshannyi_tromb_1.jpeg",
            "smeshannyi_tromb_2.jpeg",
        ],
    ),
]

# ============================================================
#   СТРУКТУРА ПО КАТЕГОРИЯМ
# ============================================================

SECTIONS: Dict[str, List[Preparat]] = {}

for p in PREPARATS:
    SECTIONS.setdefault(p.category, []).append(p)

# ============================================================
#   ИНИЦИАЛИЗАЦИЯ БОТА
# ============================================================
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ============================================================
#   ГЛАВНОЕ МЕНЮ
# ============================================================

def home_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📚 Режим обучения", callback_data="learn")],
        [InlineKeyboardButton(text="🎲 Случайный препарат", callback_data="random")],
        [InlineKeyboardButton(text="🧪 Тест", callback_data="test_menu")],
    ])

def sections_kb():
    kb = []
    for name in SECTIONS:
        kb.append([InlineKeyboardButton(text=name, callback_data=f"sec_{name}")])
    kb.append([InlineKeyboardButton(text="🏠 Домой", callback_data="home")])
    return InlineKeyboardMarkup(inline_keyboard=kb)

def learn_nav_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➡️ Следующий", callback_data="next")],
        [InlineKeyboardButton(text="🔙 К разделам", callback_data="learn")],
        [InlineKeyboardButton(text="🏠 Домой", callback_data="home")],
    ])

def test_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1️⃣ Варианты ответов", callback_data="test_var")],
        [InlineKeyboardButton(text="2️⃣ Ввод ответа", callback_data="test_write")],
        [InlineKeyboardButton(text="📊 Ошибки", callback_data="test_err")],
        [InlineKeyboardButton(text="🏠 Домой", callback_data="home")],
    ])

# ============================================================
#   ХРАНЕНИЕ СОСТОЯНИЯ
# ============================================================

USER = {}

def get_user(uid):
    if uid not in USER:
        USER[uid] = {
            "mode": None,
            "section": None,
            "index": 0,
            "used_random": set(),
            "errors": []
        }
    return USER[uid]

# ============================================================
#   ОБРАБОТКА /start
# ============================================================

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("👋 Привет! Выбери режим:", reply_markup=home_kb())

# ============================================================
#   РЕЖИМ ОБУЧЕНИЯ
# ============================================================

@dp.callback_query(lambda c: c.data == "learn")
async def learn(call: types.CallbackQuery):
    await call.message.edit_text("Выберите раздел:", reply_markup=sections_kb())
    await call.answer()

@dp.callback_query(lambda c: c.data.startswith("sec_"))
async def choose_section(call: types.CallbackQuery):
    uid = call.from_user.id
    section = call.data[4:]
    u = get_user(uid)

    u["mode"] = "learn"
    u["section"] = section
    u["index"] = 0

    await send_prep(call, section, 0)

async def send_prep(call, section, index):
    items = SECTIONS[section]

    if index >= len(items):
        await call.message.edit_text(
            f"🎉 Вы прошли раздел *{section}*!",
            reply_markup=sections_kb()
        )
        return

    prep = items[index]
    url = BASE_URL + random.choice(prep.files)

    await call.message.edit_photo(
        photo=url,
        caption=f"**{prep.name}**\nРаздел: {section}",
        parse_mode="Markdown",
        reply_markup=learn_nav_kb()
    )

@dp.callback_query(lambda c: c.data == "next")
async def next_prep(call: types.CallbackQuery):
    uid = call.from_user.id
    u = get_user(uid)

    if u["mode"] != "learn":
        await call.answer("Выберите раздел!", show_alert=True)
        return

    u["index"] += 1
    await send_prep(call, u["section"], u["index"])
    await call.answer()

# ============================================================
#   СЛУЧАЙНЫЙ ПРЕПАРАТ
# ============================================================

@dp.callback_query(lambda c: c.data == "random")
async def random_prep(call: types.CallbackQuery):
    uid = call.from_user.id
    u = get_user(uid)

    all_items = PREPARATS
    used = u["used_random"]

    available = [p for p in all_items if p.id not in used]

    if not available:
        await call.message.edit_text("🎉 Все препараты уже просмотрены!", reply_markup=home_kb())
        return

    prep = random.choice(available)
    used.add(prep.id)

    url = BASE_URL + random.choice(prep.files)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Ещё", callback_data="random")],
        [InlineKeyboardButton(text="🏠 Домой", callback_data="home")]
    ])

    await call.message.edit_photo(photo=url, caption=f"Случайный препарат:\n**{prep.name}**", parse_mode="Markdown", reply_markup=kb)
    await call.answer()

# ============================================================
#   ТЕСТЫ
# ============================================================

@dp.callback_query(lambda c: c.data == "test_menu")
async def test_menu(call: types.CallbackQuery):
    await call.message.edit_text("Выбери режим теста:", reply_markup=test_menu_kb())
    await call.answer()

# ---------- тест с вариантами

@dp.callback_query(lambda c: c.data == "test_var")
async def test_var(call: types.CallbackQuery):
    uid = call.from_user.id
    u = get_user(uid)

    target = random.choice(PREPARATS)
    u["test_target"] = target.name

    variants = {target.name}
    while len(variants) < 4:
        variants.add(random.choice(PREPARATS).name)

    variants = list(variants)
    random.shuffle(variants)

    kb = []
    for v in variants:
        kb.append([InlineKeyboardButton(text=v, callback_data=f"ans_{v}")])

    kb.append([InlineKeyboardButton(text="🏠 Домой", callback_data="home")])

    url = BASE_URL + random.choice(target.files)

    await call.message.edit_photo(
        photo=url,
        caption="Выберите название препарата:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=kb)
    )
    await call.answer()

@dp.callback_query(lambda c: c.data.startswith("ans_"))
async def check_var(call: types.CallbackQuery):
    uid = call.from_user.id
    u = get_user(uid)

    answer = call.data[4:]
    correct = u.get("test_target")

    if answer == correct:
        text = "✅ Правильно!"
    else:
        text = f"❌ Неверно\nПравильный ответ: *{correct}*"
        u["errors"].append(correct)

    await call.message.edit_text(text, parse_mode="Markdown", reply_markup=test_menu_kb())
    await call.answer()

# ---------- тест с вводом ответа

@dp.callback_query(lambda c: c.data == "test_write")
async def test_write(call: types.CallbackQuery):
    uid = call.from_user.id
    u = get_user(uid)
    u["mode"] = "test_write"

    target = random.choice(PREPARATS)
    u["test_target"] = target.name

    url = BASE_URL + random.choice(target.files)

    await call.message.edit_photo(
        photo=url,
        caption="Введите название препарата:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Домой", callback_data="home")]
        ])
    )
    await call.answer()

@dp.message()
async def test_write_answer(message: Message):
    uid = message.from_user.id
    u = get_user(uid)

    if u.get("mode") != "test_write":
        return

    correct = u.get("test_target")
    user_text = message.text.strip().lower()

    ratio = SequenceMatcher(None, user_text, correct.lower()).ratio()

    if ratio > 0.7:
        await message.answer(f"✅ Верно!\nСовпадение: {ratio:.2f}", reply_markup=test_menu_kb())
    else:
        u["errors"].append(correct)
        await message.answer(
            f"❌ Неверно!\nПравильный ответ: *{correct}*\nСовпадение: {ratio:.2f}",
            parse_mode="Markdown",
            reply_markup=test_menu_kb()
        )

# ---------- ошибки

@dp.callback_query(lambda c: c.data == "test_err")
async def test_err(call: types.CallbackQuery):
    uid = call.from_user.id
    u = get_user(uid)

    if not u["errors"]:
        text = "Ошибок нет — отлично! 🎉"
    else:
        text = "Ваши ошибки:\n" + "\n".join(f"— {e}" for e in u["errors"])

    await call.message.edit_text(text, reply_markup=test_menu_kb())
    await call.answer()

# ============================================================
#   КНОПКА ДОМОЙ
# ============================================================

@dp.callback_query(lambda c: c.data == "home")
async def home(call: types.CallbackQuery):
    await call.message.edit_text("Главное меню:", reply_markup=home_kb())
    await call.answer()

# ============================================================
#   ЗАПУСК
# ============================================================

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
