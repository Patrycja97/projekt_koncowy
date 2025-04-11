from flask import Flask, render_template, request, redirect, session, url_for, g
import requests
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'tajny_klucz'
DATABASE = 'baza.db'

STORE_NAMES = {
    "1": "Steam",
    "2": "GamersGate",
    "3": "GreenManGaming",
    "4": "Amazon",
    "5": "GameStop",
    "6": "Direct2Drive",
    "7": "GoG",
    "8": "Electronic Arts",
    "9": "Get Games",
    "10": "Shiny Loot",
    "11": "Humble Store",
    "12": "Ubisoft Store",
    "13": "Fanatical",
    "14": "Gamesrocket",
    "15": "Games Republic",
    "16": "SilaGames",
    "17": "Playfield",
    "18": "ImperialGames",
    "19": "WinGameStore",
    "20": "FunStockDigital",
    "21": "GameBillet",
    "22": "Voidu",
    "23": "Epic Games Store",
    "24": "Razer Game Store",
    "25": "Gamesplanet",
    "26": "Gamesload",
    "27": "2Game",
    "28": "IndieGala",
    "29": "Blizzard Shop",
    "30": "AllYouPlay"
}

STORE_LOGOS = {
    "1": "https://www.cheapshark.com/img/stores/logos/0.png",
    "2": "https://www.cheapshark.com/img/stores/logos/1.png",
    "3": "https://www.cheapshark.com/img/stores/logos/2.png",
    "4": "https://www.cheapshark.com/img/stores/logos/3.png",
    "5": "https://www.cheapshark.com/img/stores/logos/4.png",
    "6": "https://www.cheapshark.com/img/stores/logos/5.png",
    "7": "https://www.cheapshark.com/img/stores/logos/6.png",
    "8": "https://1000logos.net/wp-content/uploads/2020/09/EA-Desktop-Origin-Logo.png",
    "9": "https://www.cheapshark.com/img/stores/logos/8.png",
    "10": "https://www.cheapshark.com/img/stores/logos/9.png",
    "11": "https://www.cheapshark.com/img/stores/logos/10.png",
    "12": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Ubisoft_logo.svg/225px-Ubisoft_logo.svg.png",
    "13": "https://www.cheapshark.com/img/stores/logos/14.png",
    "14": "https://www.cheapshark.com/img/stores/logos/15.png",
    "15": "https://www.cheapshark.com/img/stores/logos/16.png",
    "16": "https://www.cheapshark.com/img/stores/logos/17.png",
    "17": "https://www.cheapshark.com/img/stores/logos/18.png",
    "18": "https://www.cheapshark.com/img/stores/logos/19.png",
    "19": "https://www.cheapshark.com/img/stores/logos/20.png",
    "20": "https://www.cheapshark.com/img/stores/logos/21.png",
    "21": "https://www.cheapshark.com/img/stores/logos/22.png",
    "22": "https://www.cheapshark.com/img/stores/logos/23.png",
    "23": "https://www.cheapshark.com/img/stores/logos/24.png",
    "24": "https://www.cheapshark.com/img/stores/logos/25.png",
    "25": "https://www.cheapshark.com/img/stores/logos/26.png",
    "26": "https://www.cheapshark.com/img/stores/logos/27.png",
    "27": "https://www.cheapshark.com/img/stores/logos/28.png",
    "28": "https://www.cheapshark.com/img/stores/logos/29.png",
    "29": "https://www.cheapshark.com/img/stores/logos/30.png",
    "30": "https://www.cheapshark.com/img/stores/logos/31.png"
}

# Funkcje bazy danych
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Inicjalizacja bazy danych
def init_db():
    if not os.path.exists(DATABASE):
        with sqlite3.connect(DATABASE) as db:
            cursor = db.cursor()
            cursor.execute('''CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )''')
            cursor.execute('''CREATE TABLE search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                query TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )''')
            cursor.execute('''CREATE TABLE favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                game_id TEXT,
                game_title TEXT,
                price TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )''')
            db.commit()

# Strona główna
@app.route('/')
def index():
    return render_template('index.html')

# Rejestracja
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        db = get_db()
        db.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        db.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

# Logowanie
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id, password FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            return redirect(url_for('index'))
    return render_template('login.html')

# Wylogowanie
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Dodawanie do ulubionych
@app.route('/dodaj_ulubione', methods=['POST'])
def dodaj_ulubione():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    game_id = request.form['game_id']
    title = request.form['title']
    price = request.form['price']
    db = get_db()
    db.execute("INSERT INTO favorites (user_id, game_id, game_title, price) VALUES (?, ?, ?, ?)",
               (session['user_id'], game_id, title, price))
    db.commit()
    return redirect(url_for('ulubione'))

# Ulubione gry
@app.route('/ulubione')
def ulubione():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT game_title, price FROM favorites WHERE user_id = ?", (session['user_id'],))
    gry = cursor.fetchall()
    return render_template('ulubione.html', gry=gry)

# Historia wyszukiwań
@app.route('/historia')
def historia():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT query, timestamp FROM search_history WHERE user_id = ? ORDER BY timestamp DESC", (session['user_id'],))
    historia = cursor.fetchall()
    return render_template('historia.html', historia=historia)

# Wyniki wyszukiwania
@app.route('/wyniki')
def wyniki():
    query = request.args.get('q')
    page = int(request.args.get('page', 1))
    limit = 10
    if not query:
        return redirect(url_for('index'))
    url = f"https://www.cheapshark.com/api/1.0/games?title={query}&limit={limit}&pageNumber={page - 1}"
    response = requests.get(url)
    gry = response.json()

    # Sortowanie po najniższej cenie
    gry.sort(key=lambda x: float(x['cheapest']) if x['cheapest'] else float('inf'))

    kurs_response = requests.get("https://api.nbp.pl/api/exchangerates/rates/A/USD/?format=json")
    kurs_json = kurs_response.json()
    kurs_usd_pln = kurs_json['rates'][0]['mid']

    for gra in gry:
        try:
            usd = float(gra['cheapest'])
            gra['cheapest_pln'] = round(usd * kurs_usd_pln, 2)
        except (KeyError, ValueError):
            gra['cheapest_pln'] = None

    if 'user_id' in session:
        db = get_db()
        db.execute("INSERT INTO search_history (user_id, query) VALUES (?, ?)", (session['user_id'], query))
        db.commit()

    return render_template('wyniki.html', gry=gry, query=query, page=page)

# Szczegóły gry
@app.route('/gra/<game_id>')
def gra_szczegoly(game_id):
    url = f"https://www.cheapshark.com/api/1.0/games?id={game_id}"
    response = requests.get(url)
    dane = response.json()

    kurs_response = requests.get("https://api.nbp.pl/api/exchangerates/rates/A/USD/?format=json")
    kurs_json = kurs_response.json()
    kurs_usd_pln = kurs_json['rates'][0]['mid']

    for oferta in dane.get('deals', []):
        try:
            usd = float(oferta['price'])
            oferta['price_pln'] = round(usd * kurs_usd_pln, 2)
        except (KeyError, ValueError):
            oferta['price_pln'] = None
        oferta['store_name'] = STORE_NAMES.get(oferta['storeID'], f"Sklep #{oferta['storeID']}")
        oferta['store_logo'] = STORE_LOGOS.get(oferta['storeID'])

    return render_template('szczegoly.html', gra=dane)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)