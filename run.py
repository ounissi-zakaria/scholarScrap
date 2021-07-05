import os
os.system("scrapy crawl scholars -a input=input.csv")
os.system("scrapy crawl papers -a input=scholars.csv")
os.remove("scholars.csv")
