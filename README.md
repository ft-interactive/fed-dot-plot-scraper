Extracting economic projections posted online by the Federal Reserve's Open Markets Committee

* [Source](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm)
* [Scraped data](https://github.com/palewire/fed-dot-plot-scraper/blob/main/data/dotplot.csv)

## Usage

Clone the repository.

```bash
gh repo clone palewire/fed-dot-plot-scraper
```

Move into the directory.

```bash
cd fed-dot-plot-scraper
```

Install the dependencies.

```bash
pipenv install --dev
```

Run the scraper.

```bash
pipenv run python -m src.scrape
```

That will output a CSV to the shell. You can write it to a file like this:

```bash
pipenv run python -m src.scrape > output.csv
```
