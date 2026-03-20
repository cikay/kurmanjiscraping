# Kurmanji Scraping (legacy)

This repository is an **older, outlet-specific Scrapy project** focused on crawling a handful of Kurdish (Kurmanji) news sites with per-site spiders.

If you’re starting a new crawl today, prefer the newer project:

- Recommended: [kurdish_scrapy](https://github.com/cikay/kurdish_scrapy)
- Why it’s better:
  - Crawls **arbitrary domains** from a simple JSON list (not one spider per outlet)
  - Uses **sitemap-first** crawling with a **recursive fallback**
  - Extracts clean article text via **Trafilatura**
  - Filters results by Kurdish variants using **FastText language ID**
  - Supports `kmr_Latn` (Kurmanji), `ckb_Arab` (Sorani), `diq_Latn` (Zazaki)
  - Optional ScrapeOps user-agent rotation


## Dataset

An example dataset produced from this repo is published here:
https://huggingface.co/datasets/muzaffercky/kurdish-kurmanji-news

## Running this repo (if you still need it)

### Prerequisites

- Python 3.12 (see `Pipfile`)
- Pipenv
- Optional: ScrapeOps API key (user-agent rotation)

### Setup

Create a `.env` file (don’t commit secrets):

```bash
SCRAPEOPS_API_KEY="your_api_key_here"
```

### Run a spider

Example:

```
scrapy crawl xwebun -o {file}
```
