import json
import os
import csv
from datetime import datetime


class Note:
    def __init__(self, id, title, content):
        self.id = id
        self.title = title
        self.content = content
        self.timestamp = datetime.now()


class Task:
    def __init__(self, id, title, description, priority, due_date):
        self.id = id
        self.title = title
        self.description = description
        self.done = False  # По умолчанию задача не выполнена
        self.priority = priority
        self.due_date = due_date


class Contact:
    def __init__(self, id, name, phone, email):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email


class FinanceRecord:
    def __init__(self, id, amount, category, date, description):
        self.id = id
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description


class PersonalAssistant:
    def __init__(self):
        self.notes = []
        self.tasks = []
        self.contacts = []
        self.finances = []

        self.load_data()

    def load_data(self):
        if os.path.exists('notes.csv'):
            with open('notes.csv', 'r') as f:
                reader = csv.reader(f, delimiter=' ', quotechar='|')
                self.notes = [row for row in reader]
        if os.path.exists('tasks.json'):
            with open('tasks.json', 'r') as f:
                self.tasks = json.load(f)
        if os.path.exists('contacts.json'):
            with open('contacts.json', 'r') as f:
                self.contacts = json.load(f)
        if os.path.exists('finance.json'):
            with open('finance.json', 'r') as f:
                self.finances = json.load(f)

    def save_tasks(self):
        with open('tasks.json', 'w') as f:
            json.dump(self.tasks, f)

    def save_contacts(self):
        with open('contacts.json', 'w') as f:
            json.dump(self.contacts, f)

    def save_finances(self):
        with open('finance.json', 'w') as f:
            json.dump(self.finances, f)

    def main_menu(self):
        while True:
            print("Добро пожаловать в Персональный помощник!")
            print("Выберите действие:")
            print("1. Управление заметками")
            print("2. Управление задачами")
            print("3. Управление контактами")
            print("4. Управление финансовыми записями")
            print("5. Калькулятор")
            print("6. Выход")

            choice = input("Ваш выбор: ")
            if choice == '1':
                self.manage_notes()
            elif choice == '2':
                self.manage_tasks()
            elif choice == '3':
                self.manage_contacts()
            elif choice == '4':
                self.manage_finances()
            elif choice == '5':
                self.calculator()
            elif choice == '6':
                break
            else:
                print("Некорректный ввод, попробуйте снова.")

    # Методы управления заметками

    def manage_notes(self):
        while True:
            print("\nУправление заметками:")
            print("1. Создать новую заметку")
            print("2. Просмотреть список заметок")
            print("3. Просмотреть подробности заметки")
            print("4. Редактировать заметку")
            print("5. Удалить заметку")
            print("6. Экспорт заметок в CSV")
            print("7. Импорт заметок из CSV")
            print("8. Назад")

            choice = input("Ваш выбор: ")
            if choice == '1':
                self.create_note()
            elif choice == '2':
                self.view_notes()
            elif choice == '3':
                self.view_note_details()
            elif choice == '4':
                self.edit_note()
            elif choice == '5':
                self.delete_note()
            elif choice == '6':
                self.export_notes_to_csv()
            elif choice == '7':
                self.import_notes_from_csv()
            elif choice == '8':
                break
            else:
                print("Некорректный ввод, попробуйте снова.")

    def create_note(self):
        title = input("Введите заголовок заметки: ")
        content = input("Введите содержимое заметки: ")

        note_id = sum(1 for line in self.notes) + 1
        new_note = Note(note_id, title, content)

        self.notes.append(new_note.__dict__)
        self.export_notes_to_csv()

        print("Заметка успешно создана!")

    def view_notes(self):
        if not self.notes:
            print("Список заметок пуст.")
            return

        for note in self.notes:
            print(f"{note['id']}. {note['title']} (Создано: {note['timestamp']})")

    def view_note_details(self):
        note_id = int(input("Введите ID заметки для просмотра: "))

        for note in self.notes:
            if note['id'] == note_id:
                print(f"Заголовок: {note['title']}")
                print(f"Содержимое: {note['content']}")
                print(f"Дата создания/изменения: {note['timestamp']}")
                return

        print("Заметка не найдена.")

    def edit_note(self):
        note_id = int(input("Введите ID заметки для редактирования: "))
        for note in self.notes:
            if note['id'] == note_id:
                new_title = input("Введите новый заголовок (оставьте пустым для сохранения): ")
                new_content = input("Введите новое содержимое (оставьте пустым для сохранения): ")
                if new_title:
                    note['title'] = new_title
                if new_content:
                    note['content'] = new_content

                note['timestamp'] = datetime.now()
                self.export_notes_to_csv()
                print("Заметка успешно обновлена!")
                return

        print("Заметка не найдена.")

    def delete_note(self):
        note_id = int(input('Введите ID заметки для удаления :'))
        for i, note in enumerate(self.notes):
            if note['id'] == note_id:
                del self.notes[i]
                self.export_notes_to_csv()

                print("Заметка успешно удалена!")
                return

        print("Заметка не найдена.")

    def export_notes_to_csv(self):
        with open('notes_export.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            writer.writerow(['ID', 'Title', 'Content', 'Timestamp'])

            for note in self.notes:
                writer.writerow([note['id'], note['title'], note['content'], note['timestamp']])

        print("Заметки успешно экспортированы в notes_export.csv.")

    def import_notes_from_csv(self):
        filename = input("Введите имя CSV-файла для импорта: ")
        try:
            with open(filename, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    row['id'] = int(row['ID'])
                    row['timestamp'] = datetime.now()

                    self.notes.append(row)

                self.export_notes_to_csv()

                print(f"Заметки успешно импортированы из {filename}.")

        except FileNotFoundError:
            print(f"Файл {filename} не найден.")

        # Методы управления задачами

    def manage_tasks(self):
        while True:
            print("\nУправление задачами:")
            print("1. Добавить новую задачу")
            print("2. Просмотреть задачи")
            print("3. Отметить задачу как выполненную")
            print("4. Редактировать задачу")
            print("5. Удалить задачу")
            print("6. Экспорт задач в CSV")
            print("7. Импорт задач из CSV")
            print("8. Назад")

            choice = input("Ваш выбор: ")
            if choice == '1':
                self.create_task()
            elif choice == '2':
                self.view_tasks()
            elif choice == '3':
                self.mark_task_as_done()
            elif choice == '4':
                self.edit_task()
            elif choice == '5':
                self.delete_task()
            elif choice == '6':
                self.export_tasks_to_csv()
            elif choice == '7':
                self.import_tasks_from_csv()
            elif choice == '8':
                break
            else:
                print("Некорректный ввод, попробуйте снова.")

    def create_task(self):
        title = input("Введите название задачи: ")
        description = input("Введите описание задачи: ")
        priority = input("Выберите приоритет (Высокий/Средний/Низкий): ")
        due_date = input("Введите срок выполнения (ДД-ММ-ГГГГ): ")

        task_id = len(self.tasks) + 1
        new_task = Task(task_id, title, description, priority, due_date)

        self.tasks.append(new_task.__dict__)
        self.save_tasks()

        print("Задача успешно добавлена!")

    def view_tasks(self):
        if not self.tasks:
            print("Список задач пуст.")
            return

        for task in self.tasks:
            status = "Выполнена" if task['done'] else "Не выполнена"
            print(f"{task['id']}. {task['title']} - {status} (Приоритет: {task['priority']}, Срок: {task['due_date']})")

    def mark_task_as_done(self):
        task_id = int(input("Введите ID задачи для отметки как выполненной: "))

        for task in self.tasks:
            if task['id'] == task_id and not task['done']:
                task['done'] = True  # Отметить задачу как выполненную
                self.save_tasks()

                print(f"Задача '{task['title']}' отмечена как выполненная!")
                return

        print(f"Задача с ID {task_id} не найдена или уже выполнена.")

    def edit_task(self):
        task_id = int(input("Введите ID задачи для редактирования: "))

        for task in self.tasks:
            if task['id'] == task_id:
                new_title = input(f"Введите новое название задачи (текущая: {task['title']}): ") or task['title']
                new_description = input(f"Введите новое описание задачи (текущее: {task['description']}): ") or task['description']
                new_priority = input(f"Выберите новый приоритет (текущий: {task['priority']}): ") or task['priority']
                new_due_date = input(f"Введите новый срок выполнения (текущий: {task['due_date']}): ") or task['due_date']

                task.update({
                    'title': new_title,
                    'description': new_description,
                    'priority': new_priority,
                    'due_date': new_due_date,
                })

                self.save_tasks()

                print(f"Задача '{new_title}' успешно обновлена!")
                return

        print(f"Задача с ID {task_id} не найдена.")

    def delete_task(self):
        task_id = int(input("Введите ID задачи для удаления: "))

        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                del self.tasks[i]
                self.save_tasks()

                print(f"Задача '{task['title']}' успешно удалена!")
                return

        print(f"Задача с ID {task_id} не найдена.")

    def export_tasks_to_csv(self):
        with open('tasks_export.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            writer.writerow(['ID', 'Title', 'Description', 'Done', 'Priority', 'Due Date'])

            for task in self.tasks:
                writer.writerow([task['id'], task['title'], task['description'], task['done'], task['priority'],
                                 task['due_date']])

        print("Задачи успешно экспортированы в tasks_export.csv.")

    def import_tasks_from_csv(self):
        filename = input("Введите имя CSV-файла для импорта задач: ")

        try:
            with open(filename, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    row['id'] = int(row['ID'])
                    row['done'] = row.get('Done').strip().lower() == "true"

                    # Добавляем новую задачу в список и сохраняем в файл tasks.json
                    row.pop('Done')  # Удаляем временный ключ Done из словаря перед добавлением

                    row.update({'description': row.get('Description'),
                                'priority': row.get('Priority'),
                                'due_date': row.get('Due Date')})

                    del row["Description"]
                    del row["Priority"]
                    del row["Due Date"]

                    # Добавляем новую задачу в список и сохраняем в файл tasks.json.
                    row.update({'done': False})  # Устанавливаем статус по умолчанию False.

                    if not any(task["id"] == row["id"] for task in self.tasks):
                        self.tasks.append(row)

                # Сохраняем изменения в файл tasks.json.
                self.save_tasks()
                print(f"Задачи успешно импортированы из {filename}.")

        except FileNotFoundError:
            print(f"Файл {filename} не найден.")

    # Методы управления контактами
    def manage_contacts(self):
        while True:
            print("\nУправление контактами:")
            print("1. Добавить новый контакт")
            print("2. Поиск контакта")
            print("3. Редактировать контакт")
            print("4. Удалить контакт")
            print("5. Экспорт контактов в CSV")
            print("6. Импорт контактов из CSV")
            print("7. Назад")

            choice = input("Ваш выбор:")
            if choice == '1':
                self.create_contact()
            elif choice == '2':
                self.search_contact()
            elif choice == '3':
                self.edit_contact()
            elif choice == '4':
                self.delete_contact()
            elif choice == '5':
                self.export_contacts_to_csv()
            elif choice == '6':
                self.import_contacts_from_csv()
            elif choice == '7':
                break
            else:
                print("Некорректный ввод , попробуйте снова.")

    def create_contact(self):
        name = input("Введите имя контакта: ")
        phone = input("Введите номер телефона: ")
        email = input("Введите адрес почты: ")

        contact_id = len(self.contacts) + 1
        new_contact = Contact(contact_id, name, phone, email)

        self.contacts.append(new_contact.__dict__)
        self.save_contacts()

        print("Контакт успешно создан!")

    def search_contact(self):
        search_query = input("Введите имя или номер телефона для поиска:")
        found_contacts = [contact for contact in self.contacts if
                          search_query.lower() in contact['name'].lower() or search_query in contact['phone']]
        if not found_contacts:
            print("Контакты не найдены.")
            return

        for contact in found_contacts:
            print(f"{contact['id']} - {contact['name']} - {contact['phone']} - {contact['email']}")

    def edit_contact(self):
        contact_id = int(input("Введите ID контакта для редактирования:" ))
        for contact in self.contacts:
            if contact['id'] == contact_id:
                new_name = input(f"Введите новое имя контакта(текущее:{contact['name']}):") or contact['name']
                new_phone = input(f"Введите новый номер телефона(текущий:{contact['phone']}):") or contact['phone']
                new_email = input(f"Введите новый адрес электронной почты(текущий:{contact['email']}):") or contact['email']

                contact.update({'name': new_name, 'phone': new_phone, 'email': new_email})
                self.save_contacts()
                print(f'Контакт {new_name} успешно обновлён!')
                return
        print('Контакт не найден')

    def delete_contact(self):
        contact_id = int(input("Введите ID контакта для удаления:"))
        for i, contact in enumerate(self.contacts):
            if contact['id'] == contact_id:
                del self.contacts[i]
                self.save_contacts()

                print(f"Контакт'{contact['name']}'успешно удален!")
                return

        print(f"Контакт с ID {contact_id} не найден.")

    def export_contacts_to_csv(self):
        with open('contacts_export.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Name', 'Phone', 'Email'])
            for contact in self.contacts:
                writer.writerow([contact['id'], contact['name'], contact['phone'], contact['email']])
        print("Контакты успешно экспортированы в contacts_export.csv.")

    def import_contacts_from_csv(self):
        filename = input("Введите имя CSV-файла для импорта: ")
        try:
            with open(filename, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    row['id'] = int(row['ID'])
                    self.contacts.append(row)

                self.save_contacts()
                print(f"Контакты успешно импортированы из {filename}.")

        except FileNotFoundError:
            print(f"Файл {filename} не найден.")

    # Методы управления финансовыми записями
    def manage_finances(self):
        while True:
            print("\nУправление финансовыми записями:")
            print("1. Добавить новую запись")
            print("2. Просмотреть все записи")
            print("3. Генерация отчета")
            print("4. Удалить запись")
            print("5. Экспорт финансовых записей в CSV")
            print("6. Импорт финансовых записей из CSV")
            print("7. Назад")

            choice = input("Ваш выбор: ")
            if choice == '1':
                self.create_finance_record()
            elif choice == '2':
                self.view_finance_records()
            elif choice == '3':
                self.generate_financial_report()
            elif choice == '4':
                self.delete_finance_record()
            elif choice == '5':
                self.export_finances_to_csv()
            elif choice == '6':
                self.import_finances_from_csv()
            elif choice == '7':
                break
            else:
                print("Некорректный ввод, попробуйте снова.")

    def create_finance_record(self):
        amount = float(input("Введите сумму операции (положительное число для доходов, отрицательное для расходов): "))
        category = input("Введите категорию операции: ")
        date = input("Введите дату операции (ДД-ММ-ГГГГ): ")
        description = input("Введите описание операции: ")

        finance_id = len(self.finances) + 1
        new_record = FinanceRecord(finance_id, amount, category, date, description)

        self.finances.append(new_record.__dict__)
        self.save_finances()
        print("Финансовая запись успешно добавлена!")

    def view_finance_records(self):
        if not self.finances:
            print("Список финансовых записей пуст.")
            return

        for record in self.finances:
            sign = "+" if record['amount'] > 0 else "-"
            amount_str = f"{sign}{abs(record['amount'])}"
            print(f"{record['id']}. {amount_str} - {record['category']} (Дата: {record['date']}, Описание: {record['description']})")

    def generate_financial_report(self):
        start_date_str = input("Введите начальную дату (ДД-ММ-ГГГГ): ")
        end_date_str = input("Введите конечную дату (ДД-ММ-ГГГГ): ")

        start_date = datetime.strptime(start_date_str, "%d-%m-%Y")
        end_date = datetime.strptime(end_date_str, "%d-%m-%Y")

        total_income = sum(record['amount'] for record in self.finances if
                           record['amount'] > 0 and start_date <= datetime.strptime(record['date'],
                                                                                    "%d-%m-%Y") <= end_date)
        total_expense = sum(record['amount'] for record in self.finances if
                            record['amount'] < 0 and start_date <= datetime.strptime(record['date'],
                                                                                     "%d-%m-%Y") <= end_date)

        balance = total_income + total_expense

        report_filename = f'report_{start_date_str}_{end_date_str}.csv'

        with open(report_filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            writer.writerow(['Общий доход', 'Общие расходы', 'Баланс'])
            writer.writerow([total_income, abs(total_expense), balance])

        print(f"Финансовый отчет за период с {start_date_str} по {end_date_str}:")
        print(f"- Общий доход: {total_income} руб.")
        print(f"- Общие расходы: {abs(total_expense)} руб.")
        print(f"- Баланс: {balance} руб.")

    def delete_finance_record(self):
        finance_id = int(input("Введите ID записи для удаления:"))

        for i, record in enumerate(self.finances):
            if record['id'] == finance_id:
                del self.finances[i]
                self.save_finances()  # Сохраняем изменения.
                print(f"Запись с ID'{finance_id}'успешно удалена!")
                return

        print(f"Запись с ID{finance_id}не найдена.")

    def export_finances_to_csv(self):
        with open('finances_export.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Amount', 'Category', 'Date', 'Description'])
            for record in self.finances:
                writer.writerow([record['id'], record['amount'], record['category'], record['date'], record['description']])
        print("Финансовые записи успешно экспортированы в finances_export.csv.")

    def import_finances_from_csv(self):
        filename = input("Введите имя CSV-файла для импорта:")
        try:
            with open(filename, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    row['id'] = int(row['ID'])
                    row['amount'] = float(row['Amount'])
                    row['date'] = row['Date']
                    row['description'] = row['Description']
                    self.finances.append(row)

                self.save_finances()
                print(f"Финансовые записи успешно импортированы из {filename}.")

        except FileNotFoundError:
            print(f"Файл {filename} не найден.")

    def calculator(self):
        while True:
            expression = input("Введите выражение(или'выход'для выхода):")
            if expression.lower() == 'выход':
                break
            try:
                result = eval(expression)
                print(f"Результат:{result}")

            except Exception as e:
                print(f"Ошибка:{e}")


if __name__ == "__main__":
    Assistant = PersonalAssistant()
    Assistant.main_menu()