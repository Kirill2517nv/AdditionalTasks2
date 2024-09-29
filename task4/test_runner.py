import subprocess
import os
from termcolor import colored
import colorama

# Инициализируем colorama для корректного отображения цветов в Windows
colorama.init(autoreset=True)

MAX_MOVES = 100000

def check_move(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    return (dx == 1 and dy == 2) or (dx == 2 and dy == 1)

# Функция для тестирования одного файла
def run_test(input_file: str, expected_output_file: str):
    # Нормализуем путь, чтобы слэши были в одном направлении
    input_file = os.path.normpath(input_file)
    expected_output_file = os.path.normpath(expected_output_file)

    # Чтение входных данных
    with open(input_file, 'r') as f_in:
        input_data = f_in.read()

    x_finish = int(input_data.split()[0])
    y_finish = int(input_data.split()[1])

    # Чтение ожидаемого результата
    with open(expected_output_file, 'r') as f_out:
        expected_output = f_out.read().strip()

    # Запуск task1.py с передачей данных через стандартный ввод
    result = subprocess.run(
        ['python', 'task4.py'],  # Команда для запуска
        input=input_data,  # Входные данные
        text=True,  # Для работы с текстовыми данными, а не байтами
        capture_output=True  # Захватить вывод программы
    )

    # Получаем результат программы (stdout) и удаляем лишние пробелы и символы новой строки
    program_output = result.stdout.strip()

    x, y = 0, 0  # Начальные координаты
    moves = 0  # Счетчик ходов

    massiv = [int(x) for x in program_output.split()]
    massiv_x = massiv[::2]
    massiv_y = massiv[1::2]

    i = 0
    # Чтение и проверка ходов пользователя
    while i < len(massiv_x):
        next_x = massiv_x[i]
        next_y = massiv_y[i]
        moves += 1

        # Проверка на превышение допустимого числа ходов
        if moves > MAX_MOVES:
            print(colored(f"Test {input_file} failed.", "red"))
            print(colored(f"Total number of moves greater than {MAX_MOVES}", "red"))
            return False

        # Проверка корректности хода коня
        if not check_move(x, y, next_x, next_y):
            print(colored(f"Test {input_file} failed.", "red"))
            print(colored(f"Wrong move #{moves}: from ({x}, {y}) to ({next_x}, {next_y})", "red"))
            return False

        x, y = next_x, next_y
        i += 1

    # Проверка финальной позиции
    if x != x_finish or y != y_finish:
        print(colored(f"Test {input_file} failed.", "red"))
        print(colored(f"Final position of knight is incorrect: knight in the "
                      f"({x}, {y}), but finish position is ({x_finish}, {y_finish})", "red"))
        return False

    # Если все проверки пройдены
    print(colored(f"Test {input_file} passed.", "green"))
    return True


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
