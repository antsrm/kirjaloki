# Kirjaloki

Sovelluksessa käyttäjät pystyvät jakamaan kirja-arvioitaan ja lukukokemuksiaan. Kirja-arviossa näkyvät esimerkiksi kirjan nimi, kirjailija, arvosana ja käyttäjän kirjoittama arvio.

## Sovelluksen toiminnot

- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan kirja-arvioita.
- Käyttäjä näkee sovellukseen lisätyt kirja-arviot.
- Käyttäjä pystyy etsimään kirja-arvioita hakusanalla.
- Sovelluksessa on käyttäjäsivut, jotka näyttävät käyttäjän lisäämät arviot ja tilastoja.
- Käyttäjä pystyy valitsemaan kirja-arviolle yhden tai useamman genren.
- Käyttäjä pystyy kommentoimaan omia ja muiden käyttäjien kirja-arvioita.

## Sovelluksen asennus

Asenna `flask`-kirjasto:

```bash
$ pip install flask
```

Luo tietokannan taulut:

```bash
$ sqlite3 database.db < schema.sql
```

Käynnistä sovellus:

```bash
$ flask run
```
