# Реалізувати у вигляді окремих функцій користувача:
# виведення на екран усіх значень словника;
# додавання (видалення) нового запису до (зі) словника;
# перегляд вмісту словника за відсортованими ключами (перетворити об’єкт подання ключів у список або скористатися функцією sorted, застосувавши її до словника, або об’єкту, який повертає метод keys); 
#Задано дані про n = 10 учнів класу: прізвище, ім’я, по батькові, дата народження (рік, номер місяця і число). Скласти програму, яка визначає, чи є в класі учні, в яких сьогодні день народження, і якщо так, то вивести їх ім'я та прізвище. 

from datetime import date, datetime

today = date.today()
today_without_year = today.strftime("%m-%d")

def get_valid_date():
  birth_day = int(input("Enter birth day (1-31) "))
  birth_month = int(input("Enter birth month (1-12) "))
  birth_year = int(input("Enter birth year (1900) "))
  return f"{birth_year}-{birth_month:02d}-{birth_day:02d}"

children_class = {
    "0989876565": {"last_name": "Шевченко", "first_name": "Тарас", "patronymic": "Григорович", "birth_date": "2007-09-28"},
    "0989876566": {"last_name": "Коваленко", "first_name": "Олександр", "patronymic": "Іванович", "birth_date": "2008-10-01"},
    "0989876567": {"last_name": "Мельник", "first_name": "Анна", "patronymic": "Сергіївна", "birth_date": "2008-09-25"},
    "0989876568": {"last_name": "Лисенко", "first_name": "Богдан", "patronymic": "Миколайович", "birth_date": "2008-09-29"},
    "0989876569": {"last_name": "Бондаренко", "first_name": "Максим", "patronymic": "Олегович", "birth_date": "2008-03-25"},
    "0989876515": {"last_name": "Ткаченко", "first_name": "Марія", "patronymic": "Василівна", "birth_date": "2008-03-09"},
    "0989876562": {"last_name": "Кравченко", "first_name": "Дмитро", "patronymic": "Андрійович", "birth_date": "2008-01-09"},
    "0989876563": {"last_name": "Оліник", "first_name": "Софія", "patronymic": "Михайлівна", "birth_date": "2008-08-09"},
    "0989876561": {"last_name": "Мороз", "first_name": "Артем", "patronymic": "Володимирович", "birth_date": "2008-04-09"},
    "0989876575": {"last_name": "Сидоренко", "first_name": "Вікторія", "patronymic": "Павлівна", "birth_date": "2008-07-09"}
}

# виведення на екран усіх значень словника
def show_keys(array):
  for key, value in array.items():
    print(f"Phone: {key}, {value}")

# додавання (видалення) нового запису до (зі) словника
def add_child(array):
  phone = input("Enter phone ")
  last_name = input("Enter last name ")
  first_name = input("Enter first name ")
  patronymic = input("Enter patronymic ")
  data = {
    "last_name": last_name,
    "first_name": first_name,
    "patronymic": patronymic,
    "birth_date": get_valid_date()
  }
  if not phone in array:
    array[phone] = data
  if phone in array:
    print("This child is already exist in list !")

# учні, в яких сьогодні день народження, то вивести їх ім'я та прізвище
def todays_birtdays(array):
  birthday_is = False
  children = array.values()
  for child in children:
    birthday = child.get("birth_date")
    if birthday:
      today_birth = birthday[-5:] == today_without_year
      if today_birth:
        birthday_is = True
        print(f"Happy birthday: {child.get("first_name")} {child.get("last_name")} !!")
  if not birthday_is:
    print("No one has a birthday today ... ")

# Функція яка визначає вік учня
def get_student_age(array):
    phone = input("Enter phone to check age: ")
    if phone in array:
        birth_str = array[phone]["birth_date"]
        birth_date = datetime.strptime(birth_str, "%Y-%m-%d").date()
        
        today = date.today()
        # Розраховуємо вік, віднімаючи 1, якщо день народження в цьому році ще не настав
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        first_name = array[phone]["first_name"]
        last_name = array[phone]["last_name"]
        print(f"{first_name} {last_name} is {age} years old.")
    else:
        print("Child not found!")

# виклик функцій
todays_birtdays(children_class)
add_child(children_class)
show_keys(children_class)
get_student_age(children_class)

# Додаткова функція:
# додати поле з визначенням віку учня. Виконав: Олег Борозняк
