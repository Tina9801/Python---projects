from lxml import etree
import requests

def get_url(url):
	resp = requests.get(url)
	fp = open('douban.html','w',encoding = 'utf-8')
	fp.write(resp.content.decode('utf-8'))
	html = 'douban.html'
	return html


def get_info(html):
	parser = etree.HTMLParser(encoding = 'utf-8')
	html = etree.parse(html,parser = parser)
	movies = html.xpath(".//ol[@class='grid_view']/li")
	movies_info = []
	for movie in movies:
		name = movie.xpath(".//span[@class = 'title']/text()")[0]
		link = movie.xpath(".//div[@class= 'pic']/a/@href")[0]
		movie_info = movie.xpath(".//p[@class='']/text()")[0]
		star = movie.xpath(".//div[@class='star']/span[@class='rating_num']/text()")[0]
		audience = movie.xpath(".//div[@class='star']/span[4]/text()")[0]
		quote = movie.xpath(".//span[@class = 'inq']/text()")[0]

		movie_info = {
		'name':name,
		'link':link,
		'movie_info':movie_info,
		'star':star,
		'audience':audience,
		'quote':quote
		}
		movies_info.append(movie_info)

	for movie_info in movies_info:
		print(movie_info)
		print('\n')


def spider():
	base_url = 'https://movie.douban.com/top250?start={}&filter='
	detail_urls = []
	for x in range(0,100,25):
		detail_url = base_url.format(x)
		detail_urls.append(detail_url)
	for detail_url in detail_urls:
		html = get_url(detail_url)
		get_info(html)



if __name__ == '__main__':
	spider()





