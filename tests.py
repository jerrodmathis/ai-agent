from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file


def test_get_files_info():
    print('Result for current directory:')
    print(get_files_info('calculator', '.'))

    print("Result for 'pkg' directory:")
    print(get_files_info('calculator', 'pkg'))

    print("Result for 'bin' directory:")
    print(get_files_info('calculator', '/bin'))

    print("Result for '../' directory:")
    print(get_files_info('calculator', '../'))


def test_get_file_content():
    print('Result for lorem text:')
    print(get_file_content('calculator', 'lorem.txt'))

    print('Result for current directory:')
    print(get_file_content('calculator', 'main.py'))

    print("Result for 'pkg' directory:")
    print(get_file_content('calculator', 'pkg/calculator.py'))

    print("Result for 'bin' directory:")
    print(get_file_content('calculator', '/bin/cat'))

    print("Result for '../' directory:")
    print(get_file_content('calculator', 'pkg/does_not_exist.py'))


def test_write_file():
    print('Result for lorem.txt:')
    print(write_file('calculator', 'lorem.txt', "wait, this isn't lorem ipsum"))

    print('Result for morelorem.txt')
    print(write_file('calculator', 'pkg/morelorem.txt', 'lorem ipsum dolor sit amet'))

    print('Result for /tmp/temp.txt')
    print(write_file('calculator', '/tmp/temp.txt', 'this should not be allowed'))


if __name__ == "__main__":
    test_write_file()
