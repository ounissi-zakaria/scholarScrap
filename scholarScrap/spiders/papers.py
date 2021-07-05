import scrapy
from ..items import PaperItem
import pandas as pd
from datetime import date
import json

class PapersSpider(scrapy.Spider):
    name = 'papers'
    allowed_domains = ['scholar.google.com']
    d = {}
    d["date"] = str(date.today())
    d["authors_ids"] = {}
    d["data"] = {}
    def start_requests(self):
        base_url = 'https://scholar.google.com'
        csv = pd.read_csv(self.input)
        for id, value in csv.iterrows():
            self.d["authors_ids"][value["full_name"]] = id
            self.d["data"][id] = []
            url = base_url + value["url"] + "&pagesize=100&cstart=%s"
            yield scrapy.Request(url % 0, meta={"page": 100,"url": url,"id":id})

    def parse(self, response):
        papers = response.css("tr.gsc_a_tr")
        empty = response.css("td.gsc_a_e")
        if not len(empty):
            for paper in papers:
                title = paper.css("a.gsc_a_at::text").get()
                url = paper.css("a.gsc_a_at::attr(data-href)").get()
                year = paper.css("span.gsc_a_h.gsc_a_hc.gs_ibl::text").get()
                citations = paper.css("a.gsc_a_ac.gs_ibl::text").get()

                item = {}
                item["title"] = title
                item["year"] = year
                item["citations"] = citations
                self.d["data"][response.meta["id"]].append(item)
                yield item
            yield scrapy.Request(response.meta["url"] % response.meta["page"], meta={"page":response.meta["page"] + 100, "url":response.meta["url"], "id":response.meta["id"]})


    def closed(self, reason):
        if reason == "finished":
            with open("output.json","w+") as f:
                json.dump(self.d,f)
