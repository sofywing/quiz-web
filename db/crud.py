import sqlite3

DB_NAME = 'quizes.db'
conn = None


def open():
    global conn, cursor
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

def close():
    global conn, cursor
    cursor.close()
    conn.close()

def create_tables():
    open()
    cursor.execute('''CREATE TABLE IF NOT EXISTS quiz (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR,
    description TEXT
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS questions ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question VARCHAR,
    answer VARCHAR,
    wrong1 VARCHAR,
    wrong2 VARCHAR,
    wrong3 VARCHAR
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS quiz_questions ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_id INTEGER,
    question_id INTEGER,
    FOREIGN KEY (quiz_id) REFERENCES quiz(id),
    FOREIGN KEY (question_id) REFERENCES questions(id)
    )''')

    conn.commit()
    close()
    
def add_quizes():
    open()
    quizes = [
        ("Історія України", "Перевір свої знання про ключові події, постаті та дати в історії України."),
        ("Наука та технології", "Тести про великі наукові відкриття, винаходи та сучасні технології."),
        ("Кіно та серіали", "Згадай відомі фільми, акторів і цитати з популярних стрічок."),
        ("Музика світу", "Вікторина про жанри, виконавців та хіти різних епох."),
        ("Географія планети", "Перевір, наскільки добре ти орієнтуєшся у країнах, столицях і природних чудесах світу.")
    ]

def add_questions():
    open()
    questions = [
    # Історія України
    ("Коли відбулася битва під Крутами?", "1918", "1920", "1917", "1919"),
    ("Хто був першим гетьманом Лівобережної України?", "Іван Брюховецький", "Богдан Хмельницький", "Іван Мазепа", "Петро Дорошенко"),
    ("Коли Україна проголосила незалежність?", "1991", "1990", "1992", "1989"),
    ("Яке місто було столицею УНР?", "Київ", "Харків", "Львів", "Полтава"),
    ("Хто був автором гімну України?", "Павло Чубинський", "Тарас Шевченко", "Іван Франко", "Леся Українка"),

    # Наука та технології
    ("Хто винайшов лампу розжарювання?", "Томас Едісон", "Нікола Тесла", "Олександр Белл", "Галілео Галілей"),
    ("Яка планета найближча до Сонця?", "Меркурій", "Венера", "Марс", "Земля"),
    ("Що є одиницею вимірювання електричного струму?", "Ампер", "Вольт", "Ом", "Ват"),
    ("Хто розробив теорію відносності?", "Альберт Ейнштейн", "Ісаак Ньютон", "Стівен Гокінг", "Майкл Фарадей"),
    ("Який елемент має хімічний символ 'O'?", "Кисень", "Золото", "Олово", "Осмій"),

    # Кіно та серіали
    ("Хто зіграв роль Гаррі Поттера?", "Деніел Редкліфф", "Елайджа Вуд", "Руперт Ґрінт", "Том Голланд"),
    ("Який фільм отримав «Оскар» за найкращий фільм у 1997 році?", "Титанік", "Форрест Ґамп", "Гладіатор", "Матриця"),
    ("Як називається планета, де відбуваються події у фільмі «Аватар»?", "Пандора", "Андромеда", "Альтаїр", "Нібіру"),
    ("У якому місті відбуваються події серіалу «Друзі»?", "Нью-Йорк", "Лос-Анджелес", "Чикаго", "Маямі"),
    ("Хто режисер фільму «Початок»?", "Крістофер Нолан", "Стівен Спілберг", "Джеймс Камерон", "Квентін Тарантіно"),

    # Музика світу
    ("Хто є автором пісні «Imagine»?", "Джон Леннон", "Пол Маккартні", "Елвіс Преслі", "Фредді Мерк’юрі"),
    ("Яка група створила альбом «The Dark Side of the Moon»?", "Pink Floyd", "Queen", "The Beatles", "Led Zeppelin"),
    ("Хто виконує пісню «Shape of You»?", "Ед Ширан", "Сем Сміт", "Шон Мендес", "Дрейк"),
    ("Яка країна виграла «Євробачення 2022»?", "Україна", "Італія", "Велика Британія", "Іспанія"),
    ("Який інструмент має клавіші та струни одночасно?", "Фортепіано", "Гітара", "Скрипка", "Арфа"),

    # Географія планети
    ("Яка ріка є найдовшою у світі?", "Ніл", "Амазонка", "Янцзи", "Міссісіпі"),
    ("Яка столиця Канади?", "Оттава", "Торонто", "Ванкувер", "Монреаль"),
    ("На якому материку знаходиться пустеля Сахара?", "Африка", "Азія", "Австралія", "Південна Америка"),
    ("Яка найвища гора на Землі?", "Еверест", "Кіліманджаро", "Монблан", "Мак-Кінлі"),
    ("Який океан є найбільшим за площею?", "Тихий", "Атлантичний", "Індійський", "Північний Льодовитий")
    ]

    cursor.executemany("""INSERT INTO questions (question, answer, wrong1, wrong2, wrong3) VALUES (?, ?, ?, ?, ?)""", questions)
    conn.commit()
    close()

def add_links():
    open()
    cursor.execute("PRAGMA foreign_keys=on")
    action = input("Додати зв'язок (y/n)")
    while action != "n":
        quiz_id = int(input("Введіть номер вікторини"))
        question_id = int(input("Введіть номер запитанння"))
        cursor.execute("""INSERT INTO quiz_questions (quiz_id, question_id) VALUES (?, ?)""", [quiz_id, question_id])
        conn.commit()
        action = input("Додати зв'язок? (y/n)")
    close()

def get_quizes():
    open()
    cursor.execute("SELECT * FROM quiz")
    quizes = cursor.fetchall()
    close()
    return quizes

def get_question_after(quiz_id=1, question_id=0):
   '''Повертає наступне питання до вибраної вікторини'''
   open()
   cursor.execute("""SELECT questions.id, questions.question, questions.answer, questions.wrong1, questions.wrong2, questions.wrong3
                  FROM questions, quiz_questions
                  WHERE quiz_questions.quiz_id = ? AND
                  quiz_questions.question_id > ? AND
                  quiz_questions.question_id = questions.id
                  ORDER BY quiz_questions.id""", (quiz_id, question_id))
  
   question = cursor.fetchone()
   close()
   return question

def check_right_answer(question_id, selected_answer):
    open()
    cursor.execute('''SELECT answer FROM questions WHERE id = ?''', 
    [question_id])
    right_answer = cursor.fetchone()[0]
    if selected_answer == right_answer:
        return True
    else:
        return False

   
def main():
    #create_tables()
    #add_quizes()
    #add_questions()
    add_links()

#main()