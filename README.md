# Radio-scraper

### Table of contents
- [Function](#Function)
- [Exporter](#Exporter)
- [Vizualisation](#Vizualisation)
- [Takeaways](#Takeaways)

### Function
The files in the `function` directory are responsible for scraping the data from the api. They were deployed to a GCP cloud function, which is scheduled to run every 3 minutes. It saves the data to a Firestore database.

### Exporter
This script is responsible for fetching the data from the firestore api and exporting them to a `.csv` file for further analysis. This `.csv` is then read again by `wrangler.py` and the song and artist name are added seperately in a new column. Then `spotify.py` takes that csv and gets song features like `danceability` or `energy` from the spotify api and saves them to another `.csv`

### Vizualisation
The visualisation was done using seaborn, matplotlib and pandas.

### Takeaways
The correlations between song `energy`, `tempo`, etc... from the spotify features API and the time when the songs were played is very low, and I could not distinguish any pattern. I expected to be able to see that the songs got faster towards the weekend for example. This was absolutely not the case.

More interesting conclusions could be made about the target audience of a radio station by analysing the most played artists and songs. `radiowien` is geared more towards older people while `kronehit` plays only modern artists and songs. `oe3` is an interesting mix which I can only attribute to them having days where they play older and days where they play newer songs (`funky friday` would be on such a day).
