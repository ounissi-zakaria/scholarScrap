# scholarScrap
A google scholar scraper that takes names of researchers and writes a JSON with all their published work
## Requirements
Install python 3 and install the pandas and scrapy

```
pip install scrapy
pip install pandas
```

## Usage
` python -m scrapy crawl scholars -a input=<input csv> `

Or

` scrapy crawl scholars -a input=<input csv> `

the script takes a CSV file as input. Each line of the CSV should follow the following format:

`full_name,auth`

Where  `full_name` is the name of the researcher and `auth` is the site of their institution.

For example:
```
full_name,auth
Djamel Samai, univ-ouargla.dz
Azzedine benlamoudi, univ-ouargla.dz
abdelmalik taleb ahmed, uphf.fr
```
