from lxml import html
from urllib.request import urlopen
import json


MAIN_URL = "https://habrahabr.ru"


def request_page(url):
    page = html.parse(urlopen(url)).getroot()
    return page


main_page = request_page(MAIN_URL)
url_posts = main_page.xpath('//li/article[contains(@class, "post_preview")]/h2/a/@href')

id_post = [url.split('/')[-2] for url in url_posts]
pages = [request_page(url) for url in url_posts]


author = "//div[contains(@class, 'post__wrapper')]/header[contains(@class, 'post__meta')]" \
         "/a[contains(@class, 'post__user-info')]/span[contains(@class, 'user-info__nickname')]/text()"
rate = "//div[contains(@class, 'user-info__stats-item')]/div[contains(@class, 'stacked-counter__value_magenta')]/text()"
karma = "//div[contains(@class, 'user-info__stats-item')]/div[contains(@class, 'stacked-counter__value_green')]/text()"

title = "//div[contains(@class, 'post__wrapper')]/h1[contains(@class, 'post__title_full')]/span/text()"
text = "//div[contains(@class, 'post__text-html')]//text()"
img = "//div[contains(@class, 'post__text-html')]//img/@src"
date_time = "//div[contains(@class, 'post__wrapper')]/header[contains(@class, 'post__meta')]" \
            "/span[contains(@class, 'post__time')]/text()"
mark = "//div[contains(@class, 'post__wrapper')]/dl[contains(@class, 'post__tags')]" \
       "/dd[contains(@class, post__tags-list)]/ul//li/a/text()"
count_views = "//ul[contains(@class, 'post-stats_post')]/li/div[@class='post-stats__views']" \
              "/span[contains(@class, 'post-stats__views-count')]/text()"

post_dict = {}


i = 0
for p in pages:
    post = {'user': dict()}
    post['user']['nickname'] = p.xpath(author)[0]
    post['user']['rate'] = ''.join(p.xpath(rate))
    post['user']['karma'] = ''.join(p.xpath(karma))
    post['title'] = p.xpath(title)[0]
    post['text'] = ''.join(p.xpath(text))[:100]
    post['imgs'] = p.xpath(img)
    post['date_time'] = p.xpath(date_time)[0]
    post['mark'] = p.xpath(mark)
    post['count_views'] = p.xpath(count_views)[0]
    post_dict['post__{}'.format(id_post[i])] = post
    i = i + 1

with open("posts.json", "w", encoding="utf-8") as file:
    json.dump(post_dict, file, ensure_ascii=False)