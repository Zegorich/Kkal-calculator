import telebot
from telebot import types
import sqlite3
from DailyCaloriesIntake import *
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

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

# Инициализация бота с токеном
bot = telebot.TeleBot(token)

# Подключение к базе данных SQLite (используйте путь к вашей базе данных)
conn = sqlite3.connect('../fitness/db.sqlite3', check_same_thread=False)

# Создание объекта курсора для выполнения SQL-запросов
cursor = conn.cursor()

@bot.message_handler(commands=['start'])
def start_message(info):
    # SQL-запрос для проверки, существует ли пользователь в базе данных
    sql_query = """
                SELECT EXISTS (
                    SELECT 1
                    FROM calculator_user
                    WHERE telegram = ?
                );
            """
    user_id = info.chat.id  # Получение ID пользователя из чата

    # Приведение user_id к строке и выполнение SQL-запроса
    cursor.execute(sql_query, (str(user_id),))
    result = cursor.fetchone()[0]  # Получение результата запроса

    if result:
        # Пользователь зарегистрирован, создаем клавиатуру с кнопками "Профиль", "Еда" и "Калории"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Профиль")
        item2 = types.KeyboardButton("Еда")
        item3 = types.KeyboardButton("Калории")
        markup.add(item2)
        markup.add(item1)
        markup.add(item3)
        # Отправляем сообщение с приветственным текстом и клавиатурой
        bot.send_message(info.chat.id, registered_welcome_message, reply_markup=markup)
    else:
        # Пользователь не зарегистрирован, создаем клавиатуру с URL-кнопкой и кнопкой /start

        markup = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text="Перейти на сайт", url="http://127.0.0.1:80/")
        markup.add(url_button)
        start_button = types.KeyboardButton("/start")
        start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        start_markup.add(start_button)
        # Отправляем сообщение с клавиатурами для регистрации и перезапуска
        bot.send_message(info.chat.id, error_auth_message, reply_markup=markup)
        bot.send_message(info.chat.id, "Нажмите кнопку для начала:", reply_markup=start_markup)

@bot.message_handler(func=lambda message: message.text.lower() == "профиль")
def profile_message(message):
    user_id = message.chat.id  # Получение ID пользователя из чата
    # SQL-запрос для получения данных профиля пользователя
    sql_query = """
                SELECT first_name, last_name, age, sex, current_weight, desired_weight, email
                FROM calculator_user
                WHERE telegram = ?
                """
    cursor.execute(sql_query, (str(user_id),))  # Выполнение SQL-запроса
    profile_data = cursor.fetchone()  # Получение результата запроса

    if profile_data:
        # Если данные профиля найдены, формируем текст профиля
        (first_name, last_name, age, sex, current_weight, desired_weight, email) = profile_data
        profile_text = (
            f"👤 Имя: {first_name} {last_name}\n"
            f"🎂 Возраст: {age}\n"
            f"⚧️ Пол: {sex}\n"
            f"⚖️ Текущий вес: {current_weight} кг\n"
            f"🎯 Желаемый вес: {desired_weight} кг\n"
            f"📧 Email: {email}\n"
        )
        bot.send_message(message.chat.id, profile_text)  # Отправляем текст профиля пользователю
    else:
        bot.send_message(message.chat.id, "Профиль не найден.")  # Если профиль не найден, отправляем соответствующее сообщение


@bot.message_handler(func=lambda message: message.text.lower() == "еда")
def food_message(message):
    # Получение ID пользователя из чата
    user_id = message.chat.id

    # SQL-запрос для получения ID пользователя из таблицы calculator_user по telegram ID
    sql_query = """
                SELECT id
                FROM calculator_user
                WHERE telegram = ?
                """
    cursor.execute(sql_query, (str(user_id),))
    user_id = cursor.fetchone()[0]  # Извлечение первого элемента из результата запроса

    # SQL-запрос для получения данных о питании пользователя из таблицы calculator_usernutrition
    sql_query = """
                SELECT weight, meal, product_id
                FROM calculator_usernutrition
                WHERE user_id = ?
                """
    cursor.execute(sql_query, (str(user_id),))  # Выполнение SQL-запроса
    profile_data = cursor.fetchall()  # Получение всех результатов запроса

    if profile_data:
        # Словарь для преобразования meal в текст
        meal_dict = {1: 'завтрак', 2: 'обед', 3: 'ужин', 4: 'перекус'}

        # Если данные найдены, формируем текст для каждой записи
        food_text = "Ваш рацион питания:\n\n"
        for (weight, meal, product_id) in profile_data:
            meal_text = meal_dict.get(meal, 'неизвестный прием пищи')  # Преобразование значения meal в текст
            food_text += f"🍽️ Прием пищи: {meal_text}\n"
            food_text += f"⚖️ Вес: {weight} г\n"

            # SQL-запрос для получения имени продукта по product_id
            sql_query = """
                        SELECT name
                        FROM calculator_product
                        WHERE id = ?
                        """
            cursor.execute(sql_query, (str(product_id),))  # Выполнение SQL-запроса
            name = cursor.fetchone()[0]  # Извлечение имени продукта

            food_text += f"🆔 Продукт: {name}\n\n"

        # Отправка текста пользователю
        bot.send_message(message.chat.id, food_text)
    else:
        # Если данные не найдены, отправляем соответствующее сообщение
        bot.send_message(message.chat.id, "Информация о питании не найдена.")




        # Отправляем сообщение о рационе питания
    # bot.send_message(message.chat.id, food_ration_message)
@bot.message_handler(func=lambda message: message.text.lower() == "калории")
def send_activity_buttons(message):
    # Создаем клавиатуру с кнопками для выбора уровня активности
    keyboard = InlineKeyboardMarkup()
    keyboard.row(InlineKeyboardButton("Минимальная активность", callback_data='1.2'),
                 InlineKeyboardButton("Слабый уровень активности", callback_data='1.375'))
    keyboard.row(InlineKeyboardButton("Умеренный уровень активности", callback_data='1.55'),
                 InlineKeyboardButton("Тяжелая или трудоемкая активность", callback_data='1.7'))
    keyboard.row(InlineKeyboardButton("Экстремальный уровень", callback_data='1.9'))
    bot.send_message(message.chat.id, 'Выберите уровень активности:', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def button_callback(call):
    activity = float(call.data)  # Получаем выбранный уровень активности
    user_id = call.message.chat.id  # Получение ID пользователя из чата
    # SQL-запрос для получения данных профиля пользователя
    sql_query = """
                    SELECT age, sex, current_weight
                    FROM calculator_user
                    WHERE telegram = ?
                    """
    cursor.execute(sql_query, (str(user_id),))  # Выполнение SQL-запроса
    profile_data = cursor.fetchone()  # Получение результата запроса

    if profile_data:
        # Если данные профиля найдены, рассчитываем рекомендованное суточное потребление калорий
        (age, sex, current_weight) = profile_data
        height = 176  # Предполагаем, что рост фиксирован
        temp = DailyCaloriesIntake(age, current_weight, height, sex.lower(), activity)
        calories_intake = temp.calculate_calories_intake()
        result_text = f"🍏 Рекомендуемое суточное потребление калорий: {calories_intake} калорий 🥦"
        bot.send_message(user_id, result_text)  # Отправляем результат пользователю
    bot.delete_message(call.message.chat.id, call.message.message_id)  # Удаляем сообщение с кнопками


# Запуск бота в бесконечном цикле
bot.infinity_polling()