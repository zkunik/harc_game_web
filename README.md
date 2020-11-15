# Aplikacja webowa do HarcApo 2.0

Aplikacja stworzona jako wsparcie do prowadzenia akcji harcerskiej HarcApo 2.0 przez
Zielonogórski Hufiec Harcerzy Topór (Związek Harcerstwa Rzeczypospolitej).

## Uruchomienie aplikacji na środowisku lokalnym

Instrukcja przygotowana pod Linuxa, Python w wesji 3.6 bądź wyższej.

Jeśli chcesz uruchomić aplikację w Dockerze, zobacz poniżej.

Stworzenie środowiska:

```shell
make venv
```

Przygotowanie bazy danych i dodanie przykładowych wartości do bazy (przed pierwszym startem i po każdej zmianie modeli aplikacji):

```shell
make dev-prepare
```

Uruchomienie aplikacji (na adresie 127.0.0.1:8000 bądź innym, podanym w terminalu)

```shell
make run
```

Uruchomienie testów

```shell
make test
```

## Uruchomienie aplikacji w Dockerze

Zbuduj obraz aplikacji:

```shell
docker build -t harcgameweb .
```

Uruchom testy:

```shell
docker run --rm -it harcgameweb make test
```

Uruchom aplikację:

```shell
docker run --rm -it -p 8000:8000 harcgameweb
```

## Czyszczenie środowiska lokalnego

Usuń wszystkie pliki załadowane przez formularz (upload plików) w aplikacji:
```shell
make clean-media
```

Usuń bazę danych i wszystkie pliki migracji:
```shell
make clean-db
```

Uruchom powyższe komendy za jednym razem:
```shell
make clean
```
