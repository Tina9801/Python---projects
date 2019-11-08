from lxml import etree
import requests
import re

base_url = 'https://join.qq.com/post.php?tid=5&pid=2'
head_url = 'https://join.qq.com/'
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}

def get_urls():
	resp = requests.post(base_url,headers = headers)
	html = etree.HTML(resp.text)
	urls = html.xpath("//li[@class='nav_left']//li/a/@href")
	type_urls = []
	for url in urls:
		type_url = head_url + url
		type_urls.append(type_url)

	detail_urls = []
	for type_url in type_urls:
		resp = requests.post(type_url,headers = headers)
		html = etree.HTML(resp.text)
		urls = html.xpath("//ul[@class='tab clearfix']//a/@href")
		for url in urls:
			detail_url = head_url + url
			detail_urls.append(detail_url)
	return detail_urls


def get_job_info(detail_urls):
	jobs = []
	for detail_url in detail_urls:
		resp = requests.post(detail_url,headers = headers)
		html = etree.HTML(resp.text)
		# print(type(html))


		trs = html.xpath("//div[@class='technology-con pt30']|//div[@class='item mt30']")
		job = {}
		for tr in trs:
			# print(type(tr))
			attributes = tr.xpath(".//div[@class='title']/text()")
			for attribute in attributes:
				if attribute == "岗位方向":
					content = tr.xpath(".//span[@class='selected']/text()")[0]

				elif attribute == "岗位要求":
					content_list = tr.xpath("./div[@class='contxt mt10']/text()")
					content_str = ""
					for content in content_list:
						content_str = content_str + content
					ret = re.match("(\s*)(.*)(\s*)",content_str)
					content = ret.group(2)

				else:
					content_list = tr.xpath("./div[@class='contxt mt10']/text()")
					if len(content_list) == 0:
						content = content_list
					else:
						content_str = content_list[0]
						ret = re.search("(\s*)(.*)(\s*)",content_str)
						content = ret.group(2)
				job[attribute] = content
		jobs.append(job)
		# break

	# 打印列表
	i = 1
	for job in jobs:
		print(i)
		if '暂无发布的职位' in job.keys():
			pass
		else:
			for key,value in job.items():
				print(str(key)+":"+str(value))
				i += 1
		print("\n")
		


		




if __name__ == '__main__':
	detail_urls = get_urls()
	get_job_info(detail_urls)
