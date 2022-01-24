# What?

Scraping script and view file for Lost Vault mobile game.

If you'd like to try the game by yourself, feel free to use my promo code: IDLBFH

You'll get some free coins (and I'll receive some too!)

# Ok, but how into running this?

First create your `.env` file and put your tribe name in there, as in sample example!
```
cp .env.sample .env
```

Get Python3, and provide neccessary dependencies:

```bash
pip install beautifulsoup4
```

and you are good to go. To scrap data simply use `python scrap_LV_data.py`.

To run simplest webserver and view data, type `python -m http.server 8080` and visit `localhost:8080` from your browser.
