import scrapy
import pandas as pd

class ScholarsSpider(scrapy.Spider):
    name = 'scholars'
    allowed_domains = ['scholar.google.com']
    items = []
    def start_requests(self):
        base_url = 'https://scholar.google.com/citations?view_op=search_authors&mauthors=%s'
        csv = pd.read_csv(self.input)
        for i, value in csv.iterrows():
            url = base_url % value["full_name"].replace(" ","+")
            yield scrapy.Request(url, meta={"full_name":value["full_name"], "auth":value["auth"]})

    def parse(self, response):
        scholars = response.css("div.gs_ai_t")
        for scholar in scholars:
            scholar_auth = scholar.css("div.gs_ai_eml::text").get()
            if response.meta["auth"] in scholar_auth:
                item = []
                item.append(response.meta["full_name"])
                item.append(response.meta["auth"])
                item.append(scholar.css("h3 a::attr(href)").get())
                self.items.append(item)
                yield
                break
    def closed(self, reason):
        if reason == "finished":
            df = pd.DataFrame(self.items,columns=["full_name", "auth", "url"])
            df.to_csv("scholars.csv", index=False)
