import scrapy
import pandas as pd
from datetime import date
import json

class ScholarsSpider(scrapy.Spider):
    name = 'scholars'
    allowed_domains = ['scholar.google.com']
    base_url = "https://scholar.google.com"

    d = {}
    d["date"] = str(date.today())
    d["authors_ids"] = {}
    d["data"] = {}

    def start_requests(self):
        scholar_base_url = 'https://scholar.google.com/citations?view_op=search_authors&mauthors=%s'
        csv = pd.read_csv(self.input)
        for id, value in csv.iterrows():
            url = scholar_base_url % value["full_name"].replace(" ","+")
            yield scrapy.Request(url, callback=self.parse_scholars, meta={"full_name":value["full_name"], "auth":value["auth"], "id": id})

    def parse_scholars(self, response):
        scholars = response.css("div.gs_ai_t")
        for scholar in scholars:
            scholar_auth = scholar.css("div.gs_ai_eml::text").get()
            if response.meta["auth"] in scholar_auth:
                scholar_url = scholar.css("h3 a::attr(href)").get()
                self.d["authors_ids"][response.meta["full_name"]] = response.meta["id"]
                self.d["data"][response.meta["id"]] = []
                url = self.base_url + scholar_url + "&pagesize=100&cstart=%s"
                yield scrapy.Request(url % 0, callback=self.parse_papers, meta={"page": 100, "url": url, "id":response.meta["id"]})
                break


    def parse_papers(self, response):
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
            yield scrapy.Request(response.meta["url"] % response.meta["page"], callback=self.parse_papers, meta={"page":response.meta["page"] + 100, "url":response.meta["url"], "id":response.meta["id"]})

    def closed(self, reason):
        if reason == "finished":
            with open("output.json","w+") as f:
                json.dump(self.d,f)
