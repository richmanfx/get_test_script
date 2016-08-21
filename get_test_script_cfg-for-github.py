# -*- coding: utf-8 -*-
#
# Кортеж серверов Мониторингов для скрапинга тест-скриптов
#
monitor_hosts = (
    'localhost:9191',
    '192.168.10.219:8080',
)

# Аккаунт для Мониторингов
user_name = 'username'
user_pswd = 'password'

# Папка для файлов test-скриптов
test_script_file_path = 'c:\\STORAGE\\PROGRA\\Work\\TumenEPGU\\tests\\'

# Поддерживаемые браузеры - раскомментировать один!
# browser = 'phantomjs'
# browser = 'chrome'
browser = 'firefox'

# Размер окна браузера, например, (1024, 768)
# Если закомментировать, то будет максимальный размер окна
browser_size = (1900, 850)
