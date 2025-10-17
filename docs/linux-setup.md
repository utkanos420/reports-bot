<div align=center>
    <img src="https://kappa.lol/TSkVyU" alt="Logo" width="80" height="80">
    <h3 align=center> КСИПТ репорт бот</h3>
    <p align=center>Бот для связи c системнымы администраторами</p>
</div>

## Установка бота на Linux

Работа бота протестирована на следующей операционной системе:

[![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=Ubuntu&logoColor=white)](#)

### 1. Скачивание репозитория

```
git clone https://github.com/utkanos420/ksipt-bot.git
```

### 2. Установка Docker

```
sudo apt install -y ca-certificates curl gnupg lsb-release
```

```
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Необходимо удостоверится, что Docker успешно установлен, перед тем как выполнять следующие шаги

### 3. Установка Redis

```
docker run -d --name redis -p 6379:6379 redis
```

Если контейнер успешно развернут, он должен отображаться в выводе команды:

```
docker ps
```

### 4. Создание виртуального окружения Python

Необходимо перейти в корень установленного репозитория

Установка дополнительных пакетов Python, если не установлены по умолчанию:

```
sudo apt install python3-venv python3-pip
```

Создать окружение:

```
python3 -m venv .venv
```

где `.venv` - название окружения

Включить окружение:

```
source .venv/bin/activate
```

Если окружение включено, в терминале появится соотвествующий префикс

### 5. Установка зависимостей Python

```
pip install -r requirements.txt
```

### 6. Создание и настройка .env файла

В папке **bot** необходимо создать файл `.env`, и привести его к следующему виду:

```
bot_api_key=xxx
bot_admin_id=xxx
```

где: 

* bot_api_key - API-токен telegram-бота
* bot_admin_id - telegram-ID администратора бота

### Настройка credentials.json

Чтобы связать бота с Google Sheets, в файл `credentials.json` необходимо вставить ваш ключ от **Google Cloud**, с интеграцией **Google Sheets** и **Google Drive**

### Запуск бота

Необходимо перейти в папку `app`:

```
cd app
```

И запустить скрипт:

```
python3 main.py
```

### Дополнительно

Чтобы бот мог отправлять сообщения администратору, тот должен зарегистрироваться в самом боте, используя команду `/start'

## Обратная связь

* [![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?logo=telegram&logoColor=white)](#) @utkanos420
* [![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?&logo=discord&logoColor=white)](#) @utkanos420