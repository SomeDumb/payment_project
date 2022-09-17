# Payment project
## Реализованные бонусные задачи
* Запуск используя Docker
* Использование environment variables
* Просмотр Django Моделей в Django Admin панели
* Запуск приложения на удаленном сервере, доступном для тестирования
* Модель Order, в которой можно объединить несколько Item и сделать платёж в Stripe на содержимое Order c общей стоимостью всех Items
* Добавить поле Item.currency

> Была реализована еще одна задача не отраженная в тз: <br/>
> При каждом нажатии на кнопку "купить" актуализируется цена на сервисе stripe, при необходимости.

## Модели

> Подразумевается что у каждого item есть хотя бы одна цена в рублях, в противном случае при попытке покупки произойдёт ошибка.
> При создании цены в отличной от рубля валюте данная цена будет добавлена в поле currency_options на сервисе stripe. В дальнейшем stripe будет принимать решение о том в какой валюте показать цену пользователю.

![api_item](https://user-images.githubusercontent.com/48497047/190868816-f4a29c07-203d-469b-855e-8bb41a3f759a.png)

## Endpoints
> Так как в тз не было требования для создания и редактирования 
> Item и Order при помощи API, данный функционал не был реализован.

[Ссылка на развернутый проект на heroku](https://intense-dusk-74168.herokuapp.com)
> username: username <br/>
> password: password

* /order/<int:id>
* /buy/<int:id>

## Запуск

### Prod

Для развертывания на heroku был использован файл [heroku.yml](https://github.com/SomeDumb/payment_project/blob/main/heroku.yml).
Было создано приложение на сервисе heroku и установлен плагн.

```sh
heroku create
heroku stack:set container -a <APP_NAME>
heroku plugins:install @heroku-cli/plugin-manifest
```

Далее необходимо было подключить git и установить Postgres:
```sh
heroku git:remote -a <APP_NAME>
heroku addons:create heroku-postgresql:hobby-dev -a <APP_NAME>
```

После проделанных манипуляций необходимо задать переменные окружения на сервисе heroku. 
> Это можно сделать либо через настроки приложения на сайте heroku
> Либо через командкую строку при помощи heroku-cli

Необходимые для работы проекта переменные окружения:
1. CSRF_TRUSTED_ORIGINS
> Список который должен включать ссылку на приложение
2. DEBUG
3. DJANGO_ALLOWED_HOSTS
> Список который должен включать ссылку на приложение
4. SECRET_KEY
5. SQL_ENGINE
6. STRIPE_KEY

После всего проделанного оставалось выполнить миграцию, создасть superuser и проект был готов.

```sh
heroku run python manage.py migrate
heroku run python manage.py createsuperuser -a <APP_NAME>
```

### Dev

Для запуска проекта локально был создан файл [docker-compose](https://github.com/SomeDumb/payment_project/blob/main/docker-compose.yml).
Чтобы запустить проект необходимо лишь создать файл .env.dev в корне с проектом и выполнить одну команду
> [Пример файла](https://github.com/SomeDumb/payment_project/blob/main/.env_example)
```sh
docker-compose up
```
