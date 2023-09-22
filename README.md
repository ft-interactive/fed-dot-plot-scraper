Extracting the ["dot plot"](https://en.wikipedia.org/wiki/Fedspeak#Other_usage) economic projections posted online by the [Federal Open Market Committee](https://en.wikipedia.org/wiki/Federal_Open_Market_Committee)

Forked from [here](https://github.com/palewire/fed-dot-plot-scraper). Separating this out so that we can write some new methods to format things how we'll need for our charts.

- [Source](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm)
- [Latest scraped data](https://github.com/palewire/fed-dot-plot-scraper/blob/main/data/dotplot.csv)

## Usage

Clone the repository.

```bash
gh repo clone ft-interactive/fed-dot-plot-scraper
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
