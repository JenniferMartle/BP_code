import scrapy
import pandas as pd


class BooksSpider(scrapy.Spider):
    name = 'books'
    # custom_settings = {'CONCURRENT_REQUESTS': '1'}
    # inlezen df
    df = pd.read_csv('titles.csv', low_memory=False)
    rate = 10000
    df = df[10000:]
    print(df)
    # isbn gekend: 220.994

    # ISBNS = pd.DataFrame(
    #     df[df['isbn'] != 'nan'].isbn.dropna().unique(), columns=['isbn'])
    # ISBNS = ISBNS[150000:]
    # print(ISBNS)
    # ISBNS.reset_index(inplace=True)
    # isbn niet gekend: 334390
    # titles = pd.DataFrame(
    #     df[df['isbn'] == 'nan'].title.dropna().unique(), columns=['title'])
    # titles.reset_index(inplace=True)

    # counter = 0
    start_urls = []

    # for ISBN in ISBNS['isbn']:
    #     start_urls.append(
    #         r'https://www.goodreads.com/search?utf8=%E2%9C%93&q={}&search_type=books&search%5Bfield%5D=on'.format(ISBN))

    for title in df['title']:
        title = title.split('/')[0]
        start_urls.append(
            r'https://www.goodreads.com/search?utf8=%E2%9C%93&q={}&search_type=books&search%5Bfield%5D=on'.format(title))

    def parse(self, response, **kwargs):
        if 'search' in response.request.url and 'rank=1' not in response.request.url:
            book_page = "https://www.goodreads.com/" + \
                str(response.xpath('//a[@class="bookTitle"]/@href').get())
            yield response.follow(book_page, self.parse, meta={'link': response.request.url})

        else:
            url = response.meta.get('link')
            title = url.split('&q=')[1]
            title = title.split('&search_type')[0]
            title = title.replace('%20', ' ')
            yield{
                'title': title,
                'pages': response.xpath(
                    '//p[@data-testid="pagesFormat"]/text()').get(),
                'rating': response.xpath(
                    '//div[@class="RatingStatistics__rating"]/text()').get(),
                'count_ratings': response.xpath(
                    '//span[@data-testid="ratingsCount"]/text()').get(),
                'count_reviews': response.xpath(
                    '//span[@data-testid="reviewsCount"]/text()').get(),
                'genres': response.xpath(
                    '//div[@data-testid="genresList"]//span/text()').getall(),
                'perc_5stars': response.xpath(
                    '//div[@data-testid="labelTotal-5"]/text()').get(),
                'perc_4stars': response.xpath(
                    '//div[@data-testid="labelTotal-4"]/text()').get(),
                'perc_3stars': response.xpath(
                    '//div[@data-testid="labelTotal-3"]/text()').get(),
                'perc_2stars': response.xpath(
                    '//div[@data-testid="labelTotal-2"]/text()').get(),
                'perc_1stars': response.xpath(
                    '//div[@data-testid="labelTotal-1"]/text()').get(),
                'count_books_author': response.xpath(
                    '//div[@class="FeaturedPerson__infoPrimary"]//span[@class="Text Text__body3 Text__subdued"]/text()').get(),
                'count_followers_author': response.xpath(
                    '//div[@class="FeaturedPerson__infoPrimary"]//span[@class="Text Text__body3 Text__subdued"]//span/text()').get(),
                'author': response.xpath(
                    '//span[@data-testid="name"]/text()').get(),
                'publisher': response.xpath(
                    'substring-before(substring-after(//script[@id="__NEXT_DATA__"]//text(), "publisher"), ",")').get(),
                'awards': response.xpath(
                    'substring-before(substring-after(//script[@id="__NEXT_DATA__"]//text(), "awardsWon"), "],")').get(),
                'pub_year': response.xpath(
                    '//p[@data-testid="publicationInfo"]/text()').get()
            }
    #         self.ISBNS.at[self.counter, 'pages'] = response.xpath(
    #             '//p[@data-testid="pagesFormat"]/text()').get()
    #         self.ISBNS.at[self.counter, 'rating'] = response.xpath(
    #             '//div[@class="RatingStatistics__rating"]/text()').get()
    #         self.ISBNS.at[self.counter, 'count_ratings'] = response.xpath(
    #             '//span[@data-testid="ratingsCount"]/text()').get()
    #         self.ISBNS.at[self.counter, 'count_reviews'] = response.xpath(
    #             '//span[@data-testid="reviewsCount"]/text()').get()
    #         self.ISBNS.at[self.counter, 'genres'] = str(response.xpath(
    #             '//div[@data-testid="genresList"]//span/text()').getall())
    #         self.ISBNS.at[self.counter, 'perc_5stars'] = response.xpath(
    #             '//div[@data-testid="labelTotal-5"]/text()').get()
    #         self.ISBNS.at[self.counter, 'perc_4stars'] = response.xpath(
    #             '//div[@data-testid="labelTotal-4"]/text()').get()
    #         self.ISBNS.at[self.counter, 'perc_3stars'] = response.xpath(
    #             '//div[@data-testid="labelTotal-3"]/text()').get()
    #         self.ISBNS.at[self.counter, 'perc_2stars'] = response.xpath(
    #             '//div[@data-testid="labelTotal-2"]/text()').get()
    #         self.ISBNS.at[self.counter, 'perc_1stars'] = response.xpath(
    #             '//div[@data-testid="labelTotal-1"]/text()').get()
    #         self.ISBNS.at[self.counter, 'count_books_author'] = response.xpath(
    #             '//div[@class="FeaturedPerson__infoPrimary"]//span[@class="Text Text__body3 Text__subdued"]/text()').get()
    #         self.ISBNS.at[self.counter, 'count_followers_author'] = response.xpath(
    #             '//div[@class="FeaturedPerson__infoPrimary"]//span[@class="Text Text__body3 Text__subdued"]//span/text()').get()
    #         self.ISBNS.at[self.counter, 'author'] = response.xpath(
    #             '//span[@data-testid="name"]/text()').get()
    #         self.ISBNS.at[self.counter, 'publisher'] = response.xpath(
    #             'substring-before(substring-after(//script[@id="__NEXT_DATA__"]//text(), "publisher"), ",")').get()
    #         self.ISBNS.at[self.counter, 'awards'] = response.xpath(
    #             'substring-before(substring-after(//script[@id="__NEXT_DATA__"]//text(), "awardsWon"), "],")').get()
    #         self.ISBNS.at[self.counter, 'pub_year'] = response.xpath(
    #             '//p[@data-testid="publicationInfo"]/text()').get()

    #         print(self.counter)
    #         self.counter += 1

    # def closed(self, reason):
    #     # DIT DOEN WNR ALLES GESCRAPET IS
    #     # df = pd.concat([self.df, self.titlesDF])
    #     self.ISBNS.to_csv('goodreads_ISBNS_{}.csv'.format(self.rate))
