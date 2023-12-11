# Blogicum

Blogicum - сайт, где пользователи создают свои страницы и публикуют посты. Каждый пост имеет категорию (путешествия, кулинария и др.) и опциональную локацию. Пользователи могут просматривать посты по категориям, заходить на чужие страницы, читать и комментировать посты.

## Как запустить проект

Клонируем себе репозиторий:

```
git clone git@github.com:AnastasDan/blogicum.git
```

Переходим в директорию:

```
cd blogicum
```

Cоздаем и активируем виртуальное окружение:

* Если у вас Linux/MacOS:

    ```
    python3 -m venv venv
    ```

    ```
    source venv/bin/activate
    ```

* Если у вас Windows:

    ```
    python -m venv venv
    ```

    ```
    source venv/Scripts/activate
    ```

Устанавливаем зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Создаем файл .env и заполняем его. Список данных указан в файле env.example.

Выполняем миграции:

```
python manage.py migrate
```

Запускаем проект:

```
python manage.py runserver
```

## Автор проекта

[Anastas Danielian](https://github.com/AnastasDan)