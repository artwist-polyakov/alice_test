# coding: utf-8
# Импортируем модули для работы с JSON и логами.
import logging
from typing import Dict, Any

# Импортируем подмодули FastAPI для запуска веб-сервиса.
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}


class Meta(BaseModel):
    locale: str
    timezone: str
    client_id: str
    interfaces: Dict[str, Any]


class User(BaseModel):
    user_id: str


class Application(BaseModel):
    application_id: str


class Session(BaseModel):
    message_id: int
    session_id: str
    skill_id: str
    user: User
    application: Application
    new: bool
    user_id: str


class NLU(BaseModel):
    tokens: list
    entities: list
    intents: dict


class RequestModel(BaseModel):
    command: str
    original_utterance: str
    nlu: NLU
    markup: Dict[str, bool]
    type: str


class RequestBody(BaseModel):
    meta: Meta
    session: Session
    request: RequestModel
    version: str


@app.post("/")
async def main(request: RequestBody):
    logging.info('Request: %r', request.dict())

    response = {
        "version": request.version,
        "session": {
            "message_id": request.session.message_id,
            "session_id": request.session.session_id,
            "skill_id": request.session.skill_id,
            "user_id": request.session.user_id
        },
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.dict(), response)

    logging.info('Response: %r', response)

    return JSONResponse(content=response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        sessionStorage[user_id] = {
            'suggests': [
                "Не хочу.",
                "Не буду.",
                "Отстань!",
            ]
        }

        res['response']['text'] = 'Привет! Купи слона!'
        res['response']['buttons'] = get_suggests(user_id)
        return

    # Обрабатываем ответ пользователя.
    if req['request']['original_utterance'].lower() in [
        'ладно',
        'куплю',
        'покупаю',
        'хорошо',
    ]:
        # Пользователь согласился, прощаемся.
        res['response']['text'] = 'Слона можно найти на Яндекс.Маркете!'
        return

    # Если нет, то убеждаем его купить слона!
    res['response']['text'] = 'Все говорят "%s", а ты купи слона!' % (
        req['request']['original_utterance']
    )
    res['response']['buttons'] = get_suggests(user_id)


def get_suggests(user_id):
    session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    # Убираем первую подсказку, чтобы подсказки менялись каждый раз.
    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    # Если осталась только одна подсказка, предлагаем подсказку
    # со ссылкой на Яндекс.Маркет.
    if len(suggests) < 2:
        suggests.append({
            "title": "Ладно",
            "url": "https://market.yandex.ru/search?text=слон",
            "hide": True
        })

    return suggests


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5555)