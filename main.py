import flet as ft


def main(page: ft.Page):
    # Настройка страницы в стиле скриншота
    page.title = "Русская орфография"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.bgcolor = "#F5F5F5"

    # Переменные состояния
    current_topic = None
    current_mode = None
    current_word_index = 0
    score = 0

    # Данные приложения - темы и слова
    topics_data = {
        "Безударные гласные": {
            "rules": "Правило: Безударные гласные в корне слова проверяются ударением.",
            "words": [
                {"word": "тр_па", "options": ["а", "о"], "correct": "о", "full": "тропа"},
                {"word": "л_сной", "options": ["е", "и"], "correct": "е", "full": "лесной"},
                {"word": "в_дный", "options": ["о", "а"], "correct": "о", "full": "водный"}
            ]
        },
        "Парные согласные": {
            "rules": "Правило: Парные согласные в конце слова проверяются изменением формы слова.",
            "words": [
                {"word": "ду_", "options": ["п", "б"], "correct": "б", "full": "дуб"},
                {"word": "горо_", "options": ["т", "д"], "correct": "д", "full": "город"},
                {"word": "сапо_", "options": ["г", "к"], "correct": "г", "full": "сапог"}
            ]
        },
        "Разделительные Ъ и Ь": {
            "rules": "Правило: Разделительный Ъ пишется после приставок, оканчивающихся на согласную, перед буквами е, ё, ю, я.",
            "words": [
                {"word": "под_езд", "options": ["ъ", "ь"], "correct": "ъ", "full": "подъезд"},
                {"word": "в_юга", "options": ["ъ", "ь"], "correct": "ъ", "full": "въюга"},
                {"word": "об_явление", "options": ["ъ", "ь"], "correct": "ъ", "full": "объявление"}
            ]
        }
    }

    # Элементы интерфейса
    header = ft.Container(
        content=ft.Text(
            "Что нового, Артем!",
            size=24,
            weight=ft.FontWeight.BOLD,
            color="#2D3748"
        ),
        padding=ft.padding.only(bottom=30)
    )

    categories_text = ft.Container(
        content=ft.Text(
            "КАТЕГОРИИ",
            size=16,
            weight=ft.FontWeight.BOLD,
            color="#718096"
        ),
        padding=ft.padding.only(bottom=10)
    )

    # Функции для навигации
    def show_main_menu(e):
        page.clean()
        page.add(header, categories_text)
        for topic in topics_data.keys():
            page.add(create_topic_button(topic))

    def show_topic_menu(e, topic):
        nonlocal current_topic
        current_topic = topic
        page.clean()

        back_button = ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            on_click=lambda e: show_main_menu(e)
        )

        topic_header = ft.Container(
            content=ft.Text(
                topic,
                size=20,
                weight=ft.FontWeight.BOLD,
                color="#2D3748"
            ),
            padding=ft.padding.only(bottom=30)
        )

        page.add(ft.Row([back_button]), topic_header)

        # Кнопки для выбора режима
        study_button = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.BOOK, color="#4A5568", size=40),
                ft.Text("Изучить правила", size=16, weight=ft.FontWeight.BOLD)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            margin=10,
            bgcolor="white",
            border_radius=10,
            width=150,
            height=120,
            on_click=lambda e: show_rules(e, topic),
            ink=True
        )

        practice_button = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.PLAY_ARROW, color="#4A5568", size=40),
                ft.Text("Тренироваться", size=16, weight=ft.FontWeight.BOLD)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            margin=10,
            bgcolor="white",
            border_radius=10,
            width=150,
            height=120,
            on_click=lambda e: start_practice(e, topic),
            ink=True
        )

        buttons_row = ft.Row([study_button, practice_button], alignment=ft.MainAxisAlignment.CENTER)
        page.add(buttons_row)

    def show_rules(e, topic):
        page.clean()

        back_button = ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            on_click=lambda e: show_topic_menu(e, topic)
        )

        rules_header = ft.Container(
            content=ft.Text(
                f"Правила: {topic}",
                size=20,
                weight=ft.FontWeight.BOLD,
                color="#2D3748"
            ),
            padding=ft.padding.only(bottom=20)
        )

        rules_text = ft.Container(
            content=ft.Text(
                topics_data[topic]["rules"],
                size=16,
                color="#4A5568"
            ),
            padding=20,
            bgcolor="white",
            border_radius=10,
            margin=ft.margin.only(bottom=20)
        )

        examples_header = ft.Text("Примеры:", size=16, weight=ft.FontWeight.BOLD)

        examples_column = ft.Column()
        for word_data in topics_data[topic]["words"]:
            examples_column.controls.append(
                ft.Container(
                    content=ft.Text(
                        f"{word_data['word'].replace('_', word_data['correct'])}",
                        size=14,
                        color="#4A5568"
                    ),
                    padding=10,
                    bgcolor="#F7FAFC",
                    border_radius=5,
                    margin=ft.margin.only(bottom=5)
                )
            )

        start_practice_btn = ft.ElevatedButton(
            "Начать тренировку",
            on_click=lambda e: start_practice(e, topic),
            style=ft.ButtonStyle(
                color="white",
                bgcolor="#4C6EF5"
            ),
            width=200
        )

        page.add(
            ft.Row([back_button]),
            rules_header,
            rules_text,
            examples_header,
            examples_column,
            ft.Container(content=start_practice_btn, padding=20, alignment=ft.alignment.center)
        )

    def start_practice(e, topic):
        nonlocal current_topic, current_mode, current_word_index, score
        current_topic = topic
        current_mode = "practice"
        current_word_index = 0
        score = 0
        show_practice_word()

    def show_practice_word():
        page.clean()

        topic = current_topic
        word_data = topics_data[topic]["words"][current_word_index]

        progress = ft.Container(
            content=ft.Text(
                f"{current_word_index + 1}/{len(topics_data[topic]['words'])}",
                size=14,
                color="#718096"
            ),
            alignment=ft.alignment.center
        )

        word_display = ft.Container(
            content=ft.Text(
                word_data["word"],
                size=32,
                weight=ft.FontWeight.BOLD,
                color="#2D3748"
            ),
            padding=30,
            margin=20,
            alignment=ft.alignment.center,
            bgcolor="white",
            border_radius=15
        )

        options_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=20)

        for option in word_data["options"]:
            option_btn = ft.Container(
                content=ft.Text(
                    option,
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color="white"
                ),
                width=80,
                height=80,
                alignment=ft.alignment.center,
                bgcolor="#4C6EF5",
                border_radius=40,
                on_click=lambda e, opt=option: check_answer(e, opt),
                ink=True
            )
            options_row.controls.append(option_btn)

        page.add(progress, word_display, options_row)

    def check_answer(e, selected_option):
        nonlocal current_word_index, score

        topic = current_topic
        word_data = topics_data[topic]["words"][current_word_index]

        if selected_option == word_data["correct"]:
            score += 1
            current_word_index += 1

            if current_word_index < len(topics_data[topic]["words"]):
                show_practice_word()
            else:
                show_results()
        else:
            # Подсветка неправильного ответа
            e.control.bgcolor = "#E53E3E"
            page.update()

            # Показываем правильный ответ через секунду
            import time
            time.sleep(1)

            current_word_index += 1
            if current_word_index < len(topics_data[topic]["words"]):
                show_practice_word()
            else:
                show_results()

    def show_results():
        page.clean()

        topic = current_topic
        total_words = len(topics_data[topic]["words"])

        result_text = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.EMOJI_EVENTS, size=60, color="#F6AD55"),
                ft.Text(
                    "Тренировка завершена!",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color="#2D3748"
                ),
                ft.Text(
                    f"Результат: {score}/{total_words}",
                    size=20,
                    color="#4A5568"
                )
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=40,
            alignment=ft.alignment.center
        )

        restart_button = ft.ElevatedButton(
            "Повторить тренировку",
            on_click=lambda e: start_practice(e, topic),
            style=ft.ButtonStyle(
                color="white",
                bgcolor="#4C6EF5"
            ),
            width=200
        )

        back_button = ft.TextButton(
            "Вернуться к темам",
            on_click=show_main_menu
        )

        page.add(
            result_text,
            ft.Container(content=restart_button, padding=10, alignment=ft.alignment.center),
            ft.Container(content=back_button, padding=10, alignment=ft.alignment.center)
        )

    def create_topic_button(topic_name):
        return ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.BOOKMARK_BORDER, color="#4A5568"),
                ft.Text(topic_name, size=16, weight=ft.FontWeight.BOLD, color="#2D3748"),
                ft.Container(expand=True),
                ft.Text("3 слова", color="#718096")
            ]),
            padding=15,
            margin=ft.margin.only(bottom=10),
            bgcolor="white",
            border_radius=10,
            on_click=lambda e: show_topic_menu(e, topic_name),
            ink=True
        )

    # Запуск приложения с главным меню
    show_main_menu(None)


# Запуск приложения
# if __name__ == "__main__":
#     ft.app(target=main, view=ft.AppView.WEB_BROWSER),
if __name__ == "__main__":
    ft.app(
        target=main,
        view=ft.AppView.WEB_BROWSER,
        port=57097,
    )