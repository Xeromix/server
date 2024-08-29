from flask import Flask, jsonify, request
import json

app = Flask(__name__)


@app.route('/api/mods')
def mods():
    with open("mods.json", "r") as f:
        data = f.read()
    return jsonify(json.loads(data))

import random

def generate_readable_nickname():
    adjectives = [
        "Смешной", "Умный", "Светлый", "Тёмный", "Скорый", 
        "Весёлый", "Мудрый", "Сильный", "Творческий", "Смелый",
        "Ласковый", "Грустный", "Яркий", "Независимый", "Тихий",
        "Храбрый", "Тёплый", "Добрый", "Загадочный", "Творческий",
        "Сказочный", "Лёгкий", "Секретный", "Необычный", "Чудесный"
    ]

    nouns = [
        "Лев", "Кот", "Дракон", "Феникс", "Слон", 
        "Заяц", "Тигр", "Дельфин", "Панда", "Орёл",
        "Кит", "Сова", "Медведь", "Кролик", "Лиса",
        "Волк", "Собака", "Курица", "Черепаха", "Енот",
        "Лошадь", "Петух", "Рысь", "Бобер", "Аист"
    ]

    numbers = str(random.randint(1, 99))

    nickname = f"{random.choice(adjectives)}_{random.choice(nouns)}_{numbers}"
    return nickname
import time


@app.route('/api/getNickname/<hwid>')
def getNickname(hwid):
    with open("users.json", "r") as f:
        data = json.loads(f.read())
        if hwid in data:
            userName = data[hwid]
        else:
            generatedNickname = generate_readable_nickname()
            data[hwid] = generatedNickname
            userName = generatedNickname
            with open('users.json', "w") as f:
                json.dump(data, f)
        return {"nickname": userName}

@app.route('/api/mods/<mod>/addComment/<text>/<hwid>/<rating>/<version>')
def addComment(mod, text, hwid, rating, version):
    with open("users.json", "r") as f:
        data = json.loads(f.read())
        if hwid in data:
            userName = data[hwid]
        else:
            generatedNickname = generate_readable_nickname()
            data[hwid] = generatedNickname
            userName = generatedNickname
            with open('users.json', "w") as f:
                json.dump(data, f)
    with open('otzivi.json', 'r') as f:
        data = f.read()
        data = json.loads( data)
        comments = 0
        if mod not in data:
            data[mod] = []
            data[mod].append({"HWID": hwid, "text": text, "rating": int(rating), "version": version, "username": userName, "timestamp": time.time()+10800})
            comments = len(data[mod])
        else:
            for aboba in data[mod]:
                print(aboba)
                if aboba["HWID"] == hwid and aboba["version"] == version:
                    return jsonify({"error": 1})
            data[mod].append({"HWID": hwid, "text": text, "rating": int(rating), "version": version, "username": userName, "timestamp": time.time()+10800})
            comments = len(data[mod])

    with open('otzivi.json', 'w') as f:
        json.dump(data, f)
            
    with open("mods.json", "r") as f:
        dataNew = json.loads(f.read())
        for negr in dataNew:
            print(negr)
            if negr["name"] == mod:
                negr["totalRating"] += int(rating)
                negr["rating"] = negr["totalRating"] / comments
        with open("mods.json", 'w') as f:
            json.dump(dataNew, f, indent=4)

    
                    
    return jsonify({"error": 0})


@app.route('/api/mods/<mod>/Comments')
def ReadComments(mod):
    with open('otzivi.json', 'r') as f:
        data = json.loads(f.read())
        if mod not in data:
            return jsonify([])
        else:
            return data[mod][::-1]


app.run(host='0.0.0.0', port=8443)