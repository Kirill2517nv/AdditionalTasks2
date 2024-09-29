import subprocess
import os
from termcolor import colored
import colorama

# Инициализируем colorama для корректного отображения цветов в Windows
colorama.init(autoreset=True)


# Функция для тестирования одного файла
def run_test(input_file: str, expected_output_file: str):
    # Нормализуем путь, чтобы слэши были в одном направлении
    input_file = os.path.normpath(input_file)
    expected_output_file = os.path.normpath(expected_output_file)

    # Чтение входных данных
    with open(input_file, 'r') as f_in:
        input_data = f_in.read()

    a = input_data.split()[1::]

    # Чтение ожидаемого результата
    with open(expected_output_file, 'r') as f_out:
        expected_output = f_out.read().strip()

    expected_n = int(expected_output.split()[0])
    expected_c = int(expected_output.split()[1])


    # Запуск task1.py с передачей данных через стандартный ввод
    result = subprocess.run(
        ['python', 'task3.py'],  # Команда для запуска
        input=input_data,  # Входные данные
        text=True,  # Для работы с текстовыми данными, а не байтами
        capture_output=True  # Захватить вывод программы
    )

    # Получаем результат программы (stdout) и удаляем лишние пробелы и символы новой строки
    program_output = result.stdout.strip()

    user_n = int(program_output.split()[0])
    user_c = int(program_output.split()[1])

    # Подсчет количества типов пирожных с количеством >= user_c
    count = sum(1 for x in a if int(x) >= user_c)

    # Проверка решения пользователя
    if count < user_n:
        print(colored(f"Test {input_file} failed.", "red"))
        print(colored(f"User answer: {user_n} types of cakes, {user_c} cakes of each type. "
               f"But there is only {count} types of cakes with number of cakes >= {user_c}", "yellow"))
        return False

    # Сравнение решения с правильным
    if user_n * user_c == expected_n * expected_c:
        print(colored(f"Test {input_file} passed.", "green"))
        return True
    elif user_n * user_c < expected_n * expected_c:
        print(colored(f"Test {input_file} failed.", "red"))
        print(colored("There is a better solution", "yellow"))
        return False
    else:
        print(colored(f"Test {input_file} failed.", "red"))
        print(colored("Answer is better than jury answer", "yellow"))
        return False


# Функция для запуска всех тестов
def run_all_tests():
    test_dir = './tests'  # Директория с тестами
    test_cases = [f[:-2] for f in os.listdir(test_dir) if
                  f.endswith('.a')]  # Список всех тестов по именам файлов без .a

    total_tests = len(test_cases)
    passed_tests = 0

    # Прогоняем каждый тест
    for test_case in test_cases:
        input_file = os.path.join(test_dir, test_case)
        expected_output_file = os.path.join(test_dir, test_case + '.a')

        # Если тест пройден, увеличиваем счетчик
        if run_test(input_file, expected_output_file):
            passed_tests += 1

    # Выводим итоговый результат
    print("\n" + "-" * 40)
    print(f"Total tests: {total_tests}")
    print(colored(f"Passed tests: {passed_tests}", "green"))
    print(colored(f"Failed tests: {total_tests - passed_tests}", "red"))
    if passed_tests == total_tests:
        print(colored("All tests passed!", "green", attrs=["bold"]))
    else:
        print(colored("Some tests failed.", "red", attrs=["bold"]))


if __name__ == "__main__":
    run_all_tests()
