# ohtuvarasto

[![CI](https://github.com/lottatoivanen/ohtuvarasto/actions/workflows/main.yml/badge.svg)](https://github.com/lottatoivanen/ohtuvarasto/actions/workflows/main.yml)

[![codecov](https://codecov.io/gh/lottatoivanen/ohtuvarasto/graph/badge.svg?token=GKYJENYL2K)](https://codecov.io/gh/lottatoivanen/ohtuvarasto)

## Web-käyttöliittymä

Ohtuvarasto sisältää nyt web-käyttöliittymän, joka mahdollistaa varastojen hallinnan selaimen kautta.

### Käynnistäminen

1. Asenna riippuvuudet:
```bash
poetry install
```

2. Käynnistä web-sovellus:
```bash
cd src
poetry run flask --app app run
```

Tai kehitystilassa debug-modella:
```bash
cd src
FLASK_DEBUG=true poetry run python app.py
```

3. Avaa selaimessa: http://127.0.0.1:5000

### Ominaisuudet

- **Varastojen hallinta:**
  - Useiden varastojen luominen (nimi, tilavuus, alkusaldo)
  - Kaikkien varastojen listaus etusivulla
  - Yksittäisen varaston tietosivu (saldo, tilavuus, vapaa tila)
  - Varaston nimen muokkaus
  - Varaston poistaminen

- **Varaston sisällön hallinta:**
  - Tavaroiden lisääminen varastoon
  - Tavaroiden ottaminen varastosta
  - Visuaalinen täyttöasteen indikaattori
  - Automaattinen tietojen päivitys toimintojen jälkeen

- **Validoinnit:**
  - Negatiivisia arvoja ei voi syöttää
  - Pakolliset kentät tarkistetaan
  - Käyttäjäystävälliset virheilmoitukset

### Tuotantoasennus

Tuotantokäytössä:
- Aseta ympäristömuuttuja `SECRET_KEY` turvalliseksi satunnaisarvoksi
- Älä käytä `FLASK_DEBUG=true` tuotannossa
- Käytä tuotantotason WSGI-palvelinta (esim. Gunicorn)
