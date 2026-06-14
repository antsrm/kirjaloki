# Kirjaloki

Kirjaloki on sovellus, jossa käyttäjät voivat jakaa kirja-arvioitaan ja lukukokemuksiaan. Arvioissa näkyvät esimerkiksi kirjan nimi, kirjailija, arvosana, genret sekä käyttäjän kirjoittama arvio. Käyttäjät voivat myös kommentoida toistensa arvioita.

## Sovelluksen toiminnot

### Käyttäjät

- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy kirjautumaan ulos sovelluksesta.
- Jokaisella käyttäjällä on oma käyttäjäsivu.
- Käyttäjäsivulla näkyvät käyttäjän lisäämät arviot, arvioiden määrä, arvioiden keskiarvo sekä tilin luontipäivä.

### Kirja-arviot

- Käyttäjä pystyy lisäämään kirja-arvioita.
- Käyttäjä pystyy muokkaamaan omia kirja-arvioitaan.
- Käyttäjä pystyy poistamaan omia kirja-arvioitaan.
- Käyttäjä näkee kaikki sovellukseen lisätyt kirja-arviot.
- Jokaisella kirja-arviolla on oma sivunsa.
- Arvioihin voidaan liittää enintään kolme genreä.

### Genret ja haku

- Käyttäjä pystyy etsimään kirja-arvioita hakusanalla.
- Kirja-arvioita voidaan suodattaa genren perusteella.
- Arviossa näkyvät siihen liitetyt genret.

### Kommentit

- Käyttäjä pystyy kommentoimaan kirja-arvioita.
- Käyttäjä pystyy poistamaan omat kommenttinsa.
- Kommentit näkyvät arvioiden omilla sivuilla.

### Tietoturva

- Käyttäjät voivat muokata ja poistaa vain omia arvioitaan.
- Käyttäjät voivat poistaa vain omia kommenttejaan.
- Sovelluksessa on CSRF-suojaus lomakkeille.

## Sovelluksen asennus

Asenna Flask:

```bash
pip install flask
```

Luo tietokanta:

```bash
python init_db.py
```

Käynnistä sovellus:

```bash
python app.py
```

Avaa selain osoitteessa:

```text
http://127.0.0.1:5000
```

## Sovelluksen testaus

Sovellusta voi testata seuraavasti:

1. Luo uusi käyttäjätunnus.
2. Kirjaudu sisään.
3. Lisää uusi kirja-arvio.
4. Valitse arvioon yksi tai useampi genre.
5. Tarkista, että arvio näkyy Kirja-arviot-sivulla.
6. Avaa arvio sen omalle sivulle.
7. Lisää arvioon kommentti.
8. Muokkaa arvioa ja tarkista, että muutokset tallentuvat.
9. Poista kommentti.
10. Poista arvio.
11. Testaa hakutoimintoa hakusanalla.
12. Testaa genre-suodatusta Kirja-arviot-sivulla.
13. Avaa käyttäjäsivu ja tarkista, että käyttäjän tilastot näkyvät oikein.

## Tietokannan rakenne

Sovelluksessa on seuraavat taulut:

- `users` – käyttäjät
- `reviews` – kirja-arviot
- `genres` – genret
- `review_genres` – arvioiden ja genrejen liitokset
- `comments` – kommentit

## Huomioita

Tietokantatiedosto `database.db` luodaan paikallisesti eikä sitä tallenneta repositorioon.

Sovelluksen testaaja voi luoda oman tietokantansa suorittamalla komennon:

```bash
python init_db.py
```

Komento luo tietokannan sekä lisää sovelluksen käyttämät oletusgenret.