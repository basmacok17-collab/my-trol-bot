import asyncio
import random
import os  # Добавили импорт для чтения переменных окружения
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

# Безопасно берем токен из настроек хостинга FadeHost
TOKEN = os.getenv("8916760362:AAHf9caFm-LB2npmZMTzeIe5-OWIj2dsy24")

tasks = {}
last_activity = {}

phrases = [
    "у тебя мать сдохла",
    "ты уебище ебаное",
    "ты полный хуесос",
    "ты долбоёб ебаный",
    "ты пидор конченый",
    "твоя мать шлюха",
    "у тебя батя алкаш",
    "ты сын шлюхи",
    "ты малолетний гуслист",
    "ты баянист ебаный",
    "ты трёхсот килограммовая шлюха",
    "ты ходишь за сосисками в мясокомбинат",
    "ты король ничего",
    "ты впитал всё как лох",
    "ты в зеркальной броне сидишь",
    "ты с котом троллишься",
    "ты вылетишь в отборочном туре",
    "ты моя личная шестёрка",
    "ты задохлик ебаный",
    "ты заложник своего образа",
    "ты проиграл полностью",
    "ты сдавайся пидор",
    "ты ноль без палочки",
    "ты пустое место",
    "ты мусор канализационный",
    "ты говно сточное",
    "ты дно ебаное",
    "ты отстой полный",
    "ты клоун цирковой",
    "ты шапито ходячее",
    "ты баран тупой",
    "ты свинья жирная",
    "ты козёл вонючий",
    "ты петух дворовый",
    "ты тряпка мокрая",
    "ты мразь конченая",
    "ты тварь ебаная",
    "ты имбицил полный",
    "ты дебил натуральный",
    "ты придурок ебаный",
    "ты еблан чистый",
    "ты чмо болотное",
    "ты хуесос потомственный",
    "ты пидор ебаный",
    "ты лох полный",
    "у тебя мать шалава",
    "у тебя мать жирная",
    "у тебя мать трёхсот килограммовая",
    "твою мать в гроб положил",
    "твою мать ебал вчера",
    "я твою мать ебал",
    "я тебя разъебал",
    "я тебя уничтожил",
    "я король троллинга",
    "я повелитель ксививайда",
    "я в зеркальной броне",
    "я с котом сижу",
    "я впитал всё",
    "ты ничего не стоишь",
    "ты воздух пыль",
    "ты отброс общества",
    "ты отходы человеческие",
    "ты сгори в аду",
    "ты гори в геенне",
    "ты завали ебало",
    "ты курочка ряба",
    "ты ебаная шлюха",
    "ты жирная тварь",
    "ты тупой сын шлюхи",
    "ты испиздил похоронный баян",
    "ты пол монолога проиграл",
    "ты на гуслях междуножных",
    "ты с таким ебалом заходишь",
    "ты на баттл пришёл",
    "ты вылетишь сразу",
    "ты в отборочном туре",
    "ты нахуй иди",
    "ты проиграл всё",
    "ты капитулируй",
    "ты признай поражение",
    "ты мой раб",
    "ты моя шестёрка",
    "ты в клане бегаешь",
    "ты заложником образа",
    "ты тупого своего",
    "ты время вышло",
    "ты крик крик",
    "ты тук тук",
    "ты на яйца мои",
    "ты бочадон чёрный",
    "ты чернила пылятся",
    "ты блоки горят",
    "ты по комнате",
    "ты пускают тебя",
    "ты уже впитал",
    "ты полностью пидор"
]

mirror_replies = [
    "я в зеркальной броне",
    "я в зеркальном мире"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🚀 Запустить", callback_data="btn_trol"),
            InlineKeyboardButton("🛑 Остановить", callback_data="btn_stop")
        ],
        [
            InlineKeyboardButton("🔌 Подключить", callback_data="btn_connect")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_text = (
        "👋 <b>Привет! Я бот TrolGenerator.</b>\n\n"
        "Я создан для генерации мемов и веселого флуда в чатах.\n\n"
        "Вы можете управлять мной кнопками ниже или командами:\n"
        "🔹 /trol — запустить троллинг\n"
        "🔹 /stop — остановить троллинг"
    )
    await update.message.reply_text(
        text=welcome_text,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

async def troll_loop(chat_id, bot):
    recent_phrases = []

    while True:
        last = last_activity.get(chat_id)
        if last and datetime.now() - last > timedelta(minutes=10):
            if chat_id in tasks:
                tasks[chat_id].cancel()
            await bot.send_message(chat_id=chat_id, text="🛑 Авто-стоп: 10 минут тишины")
            break

        available = [p for p in phrases if p not in recent_phrases]
        if not available:
            available = phrases.copy()
            recent_phrases.clear()

        phrase = random.choice(available)
        recent_phrases.append(phrase)
        if len(recent_phrases) > 18:
            recent_phrases.pop(0)

        words = phrase.split()
        for word in words:
            await bot.send_message(chat_id=chat_id, text=word)
            await asyncio.sleep(0.09)

async def trol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    last_activity[chat_id] = datetime.now()

    if chat_id in tasks and not tasks[chat_id].done():
        await update.message.reply_text("Уже запущено 😎")
        return
    tasks[chat_id] = asyncio.create_task(troll_loop(chat_id, context.bot))
    await update.message.reply_text("🔥 Троллинг запущен!")

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    task = tasks.get(chat_id)
    if task and not task.done():
        task.cancel()
        await update.message.reply_text("🛑 Троллинг остановлен")
    else:
        await update.message.reply_text("Троллинг сейчас не запущен")

async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    chat_id = update.effective_chat.id
    last_activity[chat_id] = datetime.now()

    if chat_id in tasks and not tasks[chat_id].done():
        reply = random.choice(mirror_replies)
        await context.bot.send_message(chat_id=chat_id, text=reply)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    last_activity[chat_id] = datetime.now()

    if query.data == "btn_trol":
        if chat_id in tasks and not tasks[chat_id].done():
            await query.message.reply_text("Уже запущено 😎")
        else:
            tasks[chat_id] = asyncio.create_task(troll_loop(chat_id, context.bot))
            await query.message.reply_text("🔥 Троллинг запущен через меню")

    elif query.data == "btn_stop":
        task = tasks.get(chat_id)
        if task and not task.done():
            task.cancel()
            await query.message.reply_text("🛑 Троллинг остановлен через меню")
        else:
            await query.message.reply_text("Троллинг сейчас не запущен")

    elif query.data == "btn_connect":
        # Показываем выбор платформы
        keyboard = [
            [InlineKeyboardButton("📱 iOS", callback_data="connect_ios")],
            [InlineKeyboardButton("🤖 Android", callback_data="connect_android")],
            [InlineKeyboardButton("💻 Компьютер", callback_data="connect_pc")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
            "Выбери свою платформу:",
            reply_markup=reply_markup
        )

    elif query.data == "connect_ios":
        text = (
            "<b>Подключение на iOS</b>\n\n"
            "1. Открой <b>Настройки</b>\n"
            "2. В правом верхнем углу нажми <b>Изменить</b>\n"
            "3. Найди <b>Автоматизация чатов</b>\n"
            "4. Введи <code>@TrolGenerator_official_bot</code>\n"
            "5. Нажми <b>Добавить</b>\n\n"
            "Готово!"
        )
        keyboard = [
            [InlineKeyboardButton("📂 Открыть настройки", url="tg://settings")]
        ]
        await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    elif query.data == "connect_android":
        text = (
            "<b>Подключение на Android</b>\n\n"
            "1. Открой <b>Настройки</b>\n"
            "2. Нажми <b>Аккаунт</b>\n"
            "3. Найди <b>Автоматизация чатов</b>\n"
            "4. Введи <code>@TrolGenerator_official_bot</code>\n"
            "5. Нажми <b>Добавить</b>\n\n"
            "Готово!"
        )
        keyboard = [
            [InlineKeyboardButton("📂 Открыть настройки", url="tg://settings")]
        ]
        await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

    elif query.data == "connect_pc":
        text = (
            "<b>Подключение на компьютере</b>\n\n"
            "1. Нажми слева на <b>три полосочки</b> (☰)\n"
            "2. Выбери <b>Настройки</b>\n"
            "3. Нажми <b>Мой профиль</b>\n"
            "4. Найди <b>Автоматизация чатов</b>\n"
            "5. Введи <code>@TrolGenerator_official_bot</code>\n"
            "6. Нажми <b>Добавить</b>\n\n"
            "Готово!"
        )
        keyboard = [
            [InlineKeyboardButton("📂 Открыть настройки", url="tg://settings")]
        ]
        await query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

def main():
    if not TOKEN:
        raise ValueError("Ошибка: Переменная TOKEN не задана в настройках хостинга!")
        
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("trol", trol))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CallbackQueryHandler(button_click))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))
    print("TrolGenerator запущен!")
    
    # Запуск бота с автоматическим сбросом старых сообщений
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
