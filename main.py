from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,    
    ContextTypes,
)
from decouple import config


BOT_TOKEN = config("BOT_TOKEN")

# Хранилища для имен пользователей и их состояний
user_names = {}
user_states = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.message.from_user
    user_name = user.username or user.first_name or "друг"
    user_names[chat_id] = user_name

    # Приветственное сообщение
    welcome_text = (
    f"Привет, @{user_name}!\n"
    "Будущий курьер Яндекс Еды!\n"
    "В этом боте ты сможешь всё узнать об этой работе\n"
    "и уже завтра выполнить свой первый заказ."
    )
    keyboard = create_main_keyboard()

    # картинку
    try:
        await context.bot.send_photo(chat_id, photo=open("preview.png", "rb"))
    except Exception as e:
        print(f"Ошибка отправки изображения: {e}")

    # текст с клавиатурой
    await context.bot.send_message(chat_id, text=welcome_text, reply_markup=keyboard)
    user_states[chat_id] = "MAIN_MENU"


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id, "Чтобы перезапустить бота, введите команду /start.")


async def registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = "Выберите опцию ниже для получения информации о регистрации."
    keyboard = create_registration_keyboard()
    await context.bot.send_message(chat_id, text=text, reply_markup=keyboard)
    user_states[chat_id] = "REGISTRATION_MENU"


async def correct_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = (
    "🔑 Наша специальная ссылка для регистрации — https://ya.cc/6MqBN5\n"
    "💸 Пройдите регистрацию по этой ссылке и начните зарабатывать с нами!\n"
    "🚀 Не упустите шанс стать частью нашей команды! "
    )
    await context.bot.send_message(chat_id, text=text, reply_markup=add_back_button())
    user_states[chat_id] = "CORRECT_REGISTRATION"


async def detailed_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = (
    "✨ Стать нашим партнером — просто! ✨ Для того чтобы начать зарабатывать с нами, пройдите процесс регистрации по нашей специальной ссылке в разделе 'ЗАРЕГИСТРИРОВАТЬСЯ'. Это не обходимо для того , чтобы закрепиться именно за нами и в дальнешейм получить бонус за заказы ;)\n"
    "👥 После этого вы станете нашим партнером и сможете получать бонусы за выполненные заказы!💡 Простой шаг — и вы на пути к отличным заработкам!Не упустите шанс стать частью нашей команды! 💪 Отличные условия для наших клиентов! 👨‍💻 30 выполненных заказов — 2,000 тыс. 🔧 70 выполненных заказов — 5,000 тыс. 🏆 Более 110 выполненных заказов — 7,000 тыс.\n"
    "P.S (все зависит от вашего города , выше были указаны актуальнвые значения для м.о , в некоторых регионах бонус намного больше ;) ")
    await context.bot.send_message(chat_id, text=text, reply_markup=add_back_button())
    user_states[chat_id] = "DETAILED_INFO"


async def about_us(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = (
    "❓ Наверняка у вас возник вопрос: Кто мы такие? С радостью отвечаем!\n"
    "🙌 Мы — действующий партнер Яндекс Еды по привлечению курьеров, и наша цель — помочь вам начать зарабатывать с нами!\n"
    ". 💼 Что мы предлагаем?\n"
    "- 🎁 Приветственный бонус за регистрацию только по специальной ссылке!\n"
    "- 📚 Поделимся полезными фишками и лайфхаками для работы.\n"                                                    
    "- 🤝 Будем сопровождать вас на каждом шаге, помогая освоиться и достигать успеха!Мы ценим ваш труд и готовы поддерживать вас на пути к выгодному заработку. Регситрийтесь по ссылке в разделе 'РЕГИСТРАЦИЯ' и начните уже сегодня! 🚀"
    )

    try:
        await context.bot.send_photo(chat_id, photo=open("about_us.png", "rb"))
    except Exception as e:
        print(f"Ошибка отправки изображения: {e}")
    await context.bot.send_message(chat_id, text=text, reply_markup=add_back_button())





async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id, "Неизвестная команда. Чтобы перезапустить бота, введите /start.")


def add_back_button():
    keyboard = [[KeyboardButton("Назад")]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)


def create_main_keyboard():
    keyboard = [
        [KeyboardButton("Регистрация"), KeyboardButton("Подробные условия")],
        [KeyboardButton("О нас"), KeyboardButton("Помощь")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)


def create_registration_keyboard():
    keyboard = [
        [KeyboardButton("Зарегистрироваться"), KeyboardButton("Подробные условия")],
        [KeyboardButton("Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)



async def help_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Устанавливаем состояние "HELP_MENU" для пользователя
    user_states[chat_id] = "HELP_MENU"

    # Сообщение с кнопкой "Назад"
    text = (
    "💬 Наш менеджер — @yandex_helper1\n"
    "🤝 Присоединяйтесь к нашему уютному чату с курьерами: https://t.me/+uhKGYmcOyigzNDAy Здесь вы найдете поддержку, общение с коллегами и все необходимые советы для успешной работы! 🌟"
    )
    await context.bot.send_message(chat_id, text=text, reply_markup=add_back_button())


async def handle_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    state = user_states.get(chat_id, "MAIN_MENU")

    if state == "HELP_MENU":
        await start(update, context)
    elif state in ["CORRECT_REGISTRATION", "DETAILED_INFO"]:
        await registration(update, context)
    elif state == "REGISTRATION_MENU":
        await start(update, context)
    else:
        await start(update, context)


def main():
    # Создаем приложение
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("Регистрация"), registration))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("Зарегистрироваться"), correct_registration))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("Подробные условия"), detailed_registration))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("О нас"), about_us))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("Помощь"), help_message))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("Назад"), handle_back)) 
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_command))

    print("запущен!")
    application.run_polling()



 
if __name__ == "__main__":
    main()
