# Radio-scraper

### Table of contents
- [Function](#Function)
- [Exporter](#Exporter)

### Function
The files in the `function` directory are responsible for scraping the data from the api. They were deployed to a GCP cloud function, which is scheduled to run every 3 minutes. It saves the data to a Firestore database.

### Exporter
This script is responsible for fetching the data from the firestore api and exporting them to a `.csv` file for further analysis.