import scrapy
import pandas as pd


class ISBNSpider(scrapy.Spider):
    name = 'ISBN'

    # inlezen df
    df = pd.read_csv('SPL_dataset.csv', low_memory=False,
                     index_col='Unnamed: 0')

    # isbn niet gekend
    ISBNgekend = df[df['isbn'].notna()]
    titlesDF = df[~df.title.isin(ISBNgekend.title)]
    # DIT DOEN WNR ALLES GESCRAPET IS
    # df = df[df.title.isin(ISBNgekend.title)]
    titlesDF = pd.DataFrame(titlesDF.title.unique(), columns=['title'])
    rate = 100000
    titlesDF = titlesDF[rate:]
    titlesDF.reset_index(inplace=True)
    titles = titlesDF['title']

    start_urls = []

    for title in titles:
        title = title.replace('/', '')
        title = title.replace('.', '')
        start_urls.append(
            r'https://bookscouter.com/search?query={}&type=sell'.format(title))

        counter = 0

    def parse(self, response, **kwargs):
        if 'search' in response.request.url:
            self.titlesDF.at[self.counter, "isbn"] = response.xpath(
                '//*[@id="__next"]//main//div[2]//div//div//a[1]//div//div[2]//div//div[2]//div[2]//span/text()').get()
        else:
            self.titlesDF.at[self.counter, "isbn"] = response.xpath(
                '//*[@id="__next"]/main//section[1]//div//div//div//div//div[2]//div[1]//div//div[1]//div[2]//h2//span/text()').get()
        self.counter += 1
        print(self.counter)

    def closed(self, reason):
        # DIT DOEN WNR ALLES GESCRAPET IS
        # df = pd.concat([self.df, self.titlesDF])
        self.titlesDF.to_csv('SPL_dataset_ISBNS{}.csv'.format('rest'))
