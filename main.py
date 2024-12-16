"""Устанавливаем два пакета: собственно сам fastapi и сервер - uvicorn
запуск сервера командой - uvicorn main:app --reload, где main - имя файла с кодом.
Доки к нашему API смотрим в браузере по адресу http://127.0.0.1:8000/docs"""

# импортируем фреймворк и тип значений для доп.описания
from fastapi import FastAPI, Query

# импортируем тип значений optional и базовый класс объектов из библиотеки pydantic
from typing import Optional
from pydantic import BaseModel



# создаем объект приложения FastAPI
app = FastAPI()

# создаем корневой эндпоинт, на который будут отправлять GET-запрос
@app.get('/')
async def home():
    return {'Hello!': 'You just made a GET-request to the Raven-API'}


@app.get('/new_data')
async def new_data():
    return {'data': 'new_data'}


# словарь с книгами
bookshelf = {
    1: {
        'book': 'Spiral Dynamics',
        'price': 950.0,
        'author': 'Don Bek',
    },
    2: {
        'book': 'Solaris',
        'price': 360.0,
        'author': 'Stanislav Lem',
    }
}



# класс-модель новой книги, для добавления в наш словарь bookshelf
class BookInfo(BaseModel):
    book: str
    price: float
    # переменная author будет опциональной, тип строка, значение по умолчанию None
    author: Optional[str] = None


# класс-модель для обновления информации о книге
class UpdateBook(BaseModel):
    book: Optional[str] = None
    price: Optional[float] = None
    author: Optional[str] = None


# эндпоинт возвращающий инфо о книге по ключу
@app.get('/get-book/{book_id}')
async def get_book(book_id: int):
    return bookshelf[book_id]


# создаем POST-эндпоинт
@app.post('/create-book/{book_id}')
# ожидаем на вход от пользователя целое число и СЛОВАРЬ по шаблону BookInfo
async def create_book(book_id: int, new_book: BookInfo):
    # проверяем что такой книги нет в словаре, если существует, вернем ошибку
    if book_id in bookshelf:
        return {'Error': 'book already exists'}
    # добавляем новую книгу СЛОВАРЕМ
    bookshelf[book_id] = new_book
    # возвращаем новую созданную книгу
    return bookshelf[book_id]


# PUT-эндпойнт
@app.put('/update-book/{book_id}')
async def update_book(book_id: int, upd_book: UpdateBook):
    # проверяем на наличие изменяемой книге в словаре bookshelf, если книги с таким id там нет, вернем ошибку
    if book_id not in bookshelf:
        return {'Error': 'Book ID does not exists'}
    # делаем проверки, чтобы можно было обновить только те данные, что были переданы пользователем в метод PUT
    if upd_book.book != None:
        bookshelf[book_id].book = upd_book.book
    if upd_book.price != None:
        bookshelf[book_id].price = upd_book.price
    if upd_book.author != None:
        bookshelf[book_id].author = upd_book.author
    # вернем параметры измененной книги
    return bookshelf[book_id]


# DELETE - эндпойнт
@app.delete('/delete-book')
# сразу опишем в документации, что id книги должно быть целым числом больше нуля
def delete_book(book_id: int = Query(..., description='The book id must be greater than zero')):
    if book_id not in bookshelf:
        return {'Error': 'Book ID does not exists'}
    del bookshelf[book_id]
    return {'Done': 'The book successfully deleted'}



