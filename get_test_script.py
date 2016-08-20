# -*- coding: utf-8 -*-
from os import system

from selenium import webdriver
import get_test_script_cfg

VERSION = '1.0.0'
__author__ = 'Aleksandr Jashhuk, Zoer, R5AM, www.r5am.ru'
# Нужно поставить с сайта https://sourceforge.net/projects/pywin32/files/pywin32/Build%20220/
#   pywin32-220.win-amd64-py2.7.exe


def main():
    clear_console()  # Очистить консоль

    # Выбор сиписка серверов из конфига
    print
    for counter, server in enumerate(get_test_script_cfg.monitor_hosts):
        print '\t\t"' + str(counter + 1) + '" - for server:', server
    print '\nChoose a Monitor-server:',
    server_name = mini_switch(raw_input(), range(len(get_test_script_cfg.monitor_hosts)))
    print 'You chose the server: ' + server_name + '\n'

    # Ввод номера тест-скрипта
    print 'Input number of test-script (1...10000):',
    test_number = 0
    try:
        test_number = int(raw_input())
    except ValueError:
        print 'You need to enter an integer from 1 to 10000. Bye.'
        exit(1)

    # Проверка допустимого значения номера тест-скрипта
    status = valid_range(1, 10000, test_number)
    if not status:
        print "An out of range number. You need to enter an integer from 1 to 10000. Bye."
        exit(1)

    print 'Start scraping...'

    # Selenium-ом на сервер Мониторинга
    driver = webdriver.PhantomJS(executable_path='drivers\\phantomjs')
    # driver = webdriver.Chrome(executable_path='drivers\\chromedriver.exe')
    # driver = webdriver.Firefox()
    # driver = webdriver.Ie()
    # driver.set_window_size(1900, 1000)
    # driver.maximize_window()

    full_server_name = 'http://' + server_name
    driver.get(full_server_name)

    # Пока не найдём элемент или 10 секунд (10 сек - для всех, до отмены, глобально)
    driver.implicitly_wait(10)

    # Доступен ли сервер
    result = driver.title
    if result != u'Мониторинг':
        print 'Website or page is unavailable.'
        exit(1)

    # Логинимся
    username_field = driver.find_element_by_xpath('.//*[@id="inputLogin"]')
    username_field.send_keys(get_test_script_cfg.user_name)
    password_field = driver.find_element_by_xpath('.//*[@id="inputPassword"]')
    password_field.send_keys(get_test_script_cfg.user_pswd)
    driver.find_element_by_xpath('.//*[@id="doLogin"]').click()

    # Поиск test-script
    search_field = driver.find_element_by_xpath('.//input[@type="search"]')
    search_field.send_keys(test_number)
    driver.find_element_by_xpath('.//a[@href="#test-detail-' + str(test_number) + '"]').click()
    driver.find_element_by_xpath('.//a[@href="#test-edit-' + str(test_number) + '"]').click()

    # Поиск кода теста
    test_code = driver.find_element_by_xpath('.//textarea[@id ="code"]').get_attribute('value')

    # Запись файла test-script
    test_code_file_name = 'U' + str(test_number) + '.online.xml'
    try:
        test_code_file = open(test_code_file_name, 'w')
        test_code_file.write(test_code.encode('utf-8'))         # Писать файл в UTF-8
        test_code_file.close()
    except IOError:
        print 'Error writing file ' + test_code_file_name + '.'
        driver.quit()
        exit(1)

    print 'File \"' + test_code_file_name + '\" written successfully.'

    driver.quit()


# Проверка диапазона допустимых значений
def valid_range(minimum, maximum, variable):
    if (variable >= minimum) and (variable <= maximum):
        result = True
    else:
        result = False
    return result


def mini_switch(case, menu_numbers):
    for number in menu_numbers:
        if case == str(number + 1):
            server_name = get_test_script_cfg.monitor_hosts[number]
            return server_name
    print "An out of range number. Bye."
    exit(1)


# Очистка консоли в Windows
def clear_console():
        system('cls')


if __name__ == '__main__':
    main()
