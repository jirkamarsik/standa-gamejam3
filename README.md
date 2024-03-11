Standa Game Jam 3
-----------------

Budeš potřebovat Python 3 a knihovny Pillow (na renderování karet) a Pandas (na stažení a parseování CSV z Google Tabulek). Obojí se da nainstalovat přes `pip` skrz soubor `requirements.txt`:

```
pip install -r requirements.txt
```

V Ubuntu anebo jiných systémech s vlastní správou softwaru se tyhle balíčky instalují přes vlastní package manager, např.:

```
sudo apt install python3 python3-pil python3-pandas
```

Pak stačí už jen spustit buď `./make_tokens.py` pro vygenerování listů s tokenama,`./make_cards.py` pro vygenerování karet anebo `./stats.py` pro nějaké základní statistiky:

```
./make_tokens.py
./make_cards.py
./stats.py
```

Výsledná PDFka lze nalézt ve složce `./data/pdf`.
