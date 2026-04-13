#  ExpenseTracker — Viedais izdevumu izsekotājs

## Tehnoloģiju steks

| Slānis      | Tehnoloģija                              |
|-------------|------------------------------------------|
| Backend     | Python 3.10+, Django 4.2                 |
| Datubāze    | SQLite                                   |
| Frontend    | Django Templates, Bootstrap 5, Bootstrap Icons |
| Testi       | Django TestCase                          |

## Funkcionalitāte

- Reģistrācija, pieteikšanās un atteikšanās
- Transakciju pievienošana ar kategoriju, summu, datumu un aprakstu
- Personīgo transakciju saraksts ar kopējo atlikumu
- Transakciju rediģēšana un dzēšana
- Aizsardzība pret svešu datu piekļuvi
- Servera puses veidlapu validācija
- Notikumu reģistrēšana konsolē

## Ātrā palaišana

### 1. Klonēt repozitoriju

```bash
git clone https://github.com/jusu-lietotajvards/izdevumu-trakers.git
cd izdevumu-trakers
```

### 2. Izveidot un aktivizēt virtuālo vidi

```bash
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows
```

### 3. Uzstādīt atkarības

```bash
pip install -r requirements.txt
```

### 4. Lietot migrācijas

```bash
python manage.py migrate
```

### 5. Izveidot administratoru (pēc izvēles)

```bash
python manage.py createsuperuser
```

### 6. Palaist izstrādes serveri

```bash
python manage.py runserver
```

Lietotne pieejama: **http://127.0.0.1:8000/**

## Testu palaišana

```bash
python manage.py test transactions
```

## Projekta struktūra

```
expense_tracker/
├── expense_tracker/   # Django konfigurācija
│   ├── settings.py
│   └── urls.py
└── transactions/      # Galvenā lietotne
    ├── models.py
    ├── forms.py
    ├── views.py
    ├── urls.py
    ├── tests.py
    └── templates/
```
