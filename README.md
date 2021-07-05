# scholarScrap
A google scholar scraper that takes names of researchers and writes a JSON with all their published work 
## Requirements 
Install python 3 and install the pandas and scrapy 

```
pip install scrapy
pip install pandas
```

## Usage 
` python run.py `

the script expects a CSV file named `input.csv`. Each line of the CSV should follow the following format:

`full_name,auth`

Where  `full_name` is the name of the researcher and `auth` is the site of their institution.

For example:
```
full_name,auth
Djamel Samai, univ-ouargle.dz
Azzedin benlamoudi, univ-ouargle.dz
abdelmalik taleb ahmed, uphf.fr
```
