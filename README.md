# Kirjaloki

Sovelluksessa käyttäjät pystyvät jakamaan kirja-arvioitaan ja lukukokemuksiaan. Kirja-arviossa näkyvät esimerkiksi kirjan nimi, kirjailija, arvosana ja käyttäjän kirjoittama arvio.

## Sovelluksen toiminnot

- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan omia kirja-arvioitaan.
- Käyttäjä näkee kaikkien käyttäjien lisäämät kirja-arviot.
- Käyttäjä pystyy etsimään kirja-arvioita hakusanalla.
- Käyttäjä näkee arvion kirjoittajan käyttäjätunnuksen.
- Vain arvion kirjoittaja pystyy muokkaamaan tai poistamaan oman arvionsa.

## Sovelluksen asennus

Asenna tarvittavat kirjastot:

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

Avaa selain osoitteeseen:

```text
http://127.0.0.1:5000
```

## Sovelluksen testaus

1. Luo uusi käyttäjätunnus valitsemalla **Luo tunnus**.
2. Kirjaudu sisään luomallasi tunnuksella.
3. Lisää uusi kirja-arvio.
4. Tarkista, että arvio näkyy kirja-arvioiden listauksessa.
5. Muokkaa lisäämääsi arviota.
6. Poista lisäämäsi arvio.
7. Lisää useita arvioita ja testaa hakutoimintoa.
8. Kirjaudu ulos ja varmista, että uuden arvion lisääminen vaatii kirjautumisen.

## Huomioita

Tietokantatiedosto `database.db` luodaan paikallisesti eikä sitä tallenneta repositorioon. Sovelluksen testaaja voi luoda oman tietokantansa suorittamalla komennon:

```bash
python init_db.py
```