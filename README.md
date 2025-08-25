Crawling the most popular Kurdish Kurmanji outlets for LLM datasets. You can check the dataset collected by this project [here](https://huggingface.co/datasets/muzaffercky/kurdish-kurmanji-news)

# Run

put the following environment variables to .env file

Get API key from https://scrapeops.io/app/headers
```
SCRAPEOPS_API_KEY=""
```

```
scrapy crawl xwebun -o {file}
```