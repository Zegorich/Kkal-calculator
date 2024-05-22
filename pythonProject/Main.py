import telebot
from telebot import types
import sqlite3




# Загрузка токена из файла config.cfg
with open('config.cfg') as f:
    token = f.readline().strip()

# Глобальные переменные для приветственного сообщения зарегистрированным пользователям
registered_welcome_message = (
    "🎉 Приветствуем вас, дорогие пользователи! 🎉\n\n"
    "Вы уже зарегистрированы в нашем фитнес-боте. Выберите действие, нажав на кнопку \"Профиль\"."
)

# Глобальные переменные для сообщения об ошибке аутентификации
error_auth_message = (
    "🏋️‍♀️ **Добро пожаловать в фитнес-бот!** 🏋️‍♂️\n\n"
    "📌 **Для начала пользования зарегистрируйтесь на нашем сайте прямо сейчас: "
)

# Глобальная переменная для сообщения о рационе питания
food_ration_message = "рацион еды хз что"

bot = telebot.TeleBot(token)

# Подключение к базе данных PostgreSQL

# Создаем подключение к базе данных (файл my_database.db будет создан)
conn = sqlite3.connect('../db.sqlite3', check_same_thread=False)


# Создание объекта курсора для выполнения SQL-запросов
cursor = conn.cursor()

@bot.message_handler(commands=['start'])
def start_message(info):
    sql_query = """
                SELECT EXISTS (
                    SELECT 1
                    FROM calculator_user
                    WHERE telegram = ?
                );
            """

    user_id = info.chat.id

    # Приведение user_id к строке
    cursor.execute(sql_query, (str(user_id),))

    result = cursor.fetchone()[0]

    if result:
        # Создаем клавиатуру
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Профиль")
        item2 = types.KeyboardButton("Еда")
        markup.add(item2)
        markup.add(item1)
        # Отправляем сообщение с приветственным текстом и клавиатурой
        bot.send_message(info.chat.id, registered_welcome_message, reply_markup=markup)
    else:
        print (user_id)
        # Создаем объект клавиатуры с URL кнопкой и кнопкой /start
        markup = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text="Перейти на сайт", url="https://www.example.com")
        markup.add(url_button)

        # Добавляем кнопку /start
        start_button = types.KeyboardButton("/start")

        # Создаем клавиатуру и добавляем кнопку /start
        start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        start_markup.add(start_button)

        # Отправляем сообщение с клавиатурами
        bot.send_message(info.chat.id, error_auth_message, reply_markup=markup)
        bot.send_message(info.chat.id, "Нажмите кнопку для начала:", reply_markup=start_markup)


@bot.message_handler(func=lambda message: message.text.lower() == "профиль")
def profile_message(message):
    user_id = message.chat.id
    sql_query = """
                SELECT first_name, last_name, age, sex, current_weight, desired_weight, email
                FROM calculator_user
                WHERE telegram = ?
                """

    cursor.execute(sql_query, (str(user_id),))
    profile_data = cursor.fetchone()

    if profile_data:
        (first_name, last_name, age, sex, current_weight, desired_weight,
         email) = profile_data

        # Формируем текст профиля
        profile_text = (
            f"👤 Имя: {first_name} {last_name}\n"
            f"🎂 Возраст: {age}\n"
            f"⚧️ Пол: {sex}\n"
            f"⚖️ Текущий вес: {current_weight} кг\n"
            f"🎯 Желаемый вес: {desired_weight} кг\n"
            f"📧 Email: {email}\n"
        )

        bot.send_message(message.chat.id, profile_text)
    else:
        bot.send_message(message.chat.id, "Профиль не найден.")


@bot.message_handler(func=lambda message: message.text.lower() == "еда")
def food_message(message):
    bot.send_message(message.chat.id, food_ration_message)

bot.infinity_polling()
