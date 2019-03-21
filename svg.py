
import requests
import re

from lxml import etree


# 获取http://www.dianping.com/shop/67408602
def da_request():
    url = 'http://www.dianping.com/shop/67408602'
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"
    }
    rensponse = requests.get(url, headers=headers)
    if rensponse.status_code == 200:
        return rensponse.content.decode('utf8')
    return None


# 解析详情页面，并且获取矢量图连接
def da_response(html):
    svg_tel = re.compile('<d class="(.*?)"></d>', re.S)
    svg_tel = re.findall(svg_tel, html)
    tel = [tel.strip() for tel in svg_tel][12:]
    # ['zogwtn', 'zog0xa', 'zogom2', 'zogom2', 'zogf54', 'zogf54', 'zogf54', 'zogf54', 'zogtr3', 'zoggvv', 'zogtr3']

    svg_url = re.compile('<link rel="stylesheet" type="text/css" href="//s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/(.*?).css">', re.S)
    svg_url = re.findall(svg_url, html)
    url = [url.strip() for url in svg_url]
    # url = 'http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/' + url[0] + '.css'
    # //s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/d89007046ea2f67c77f0c084d48476b0.css
    # print(url)

# # # 页面有验证，提前赋值，以便于往后的测试 xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    tel = ['zogwtn', 'zog0xa', 'zogom2', 'zogom2', 'zogf54', 'zogf54', 'zogf54', 'zogf54', 'zogtr3', 'zoggvv', 'zogtr3']
    url = 'http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/d89007046ea2f67c77f0c084d48476b0.css'

    # 请求svg_url详情页面
    htmll = url_request(url)
    url_response(htmll, tel)



# 2,===================================================
def url_request(url):
    url = url
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"
    }
    rensponse = requests.get(url, headers=headers)
    if rensponse.status_code == 200:
        return rensponse.content.decode('utf8')
    return None


#
def url_response(htmll, tel):
    # print(htmll)
    tel_url = re.compile('d\[class\^="zog"\]\{width: .*?;height: .*?;margin-top: .*?;background-image: url\(//s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/(.*?).svg\);', re.S)
    tel_url = re.findall(tel_url, htmll)
    tel_u = [tel_u.strip() for tel_u in tel_url]
    print(tel_u)   # f8350660159e938ca81d948ca9d0d555

    tel_svg_url = 'http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/' + tel_u[0] + '.svg'
    # //s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/f8350660159e938ca81d948ca9d0d555.svg

    svg_list = []
    for t in tel:
        num = '%s{background:(.*?) (.*?)px;}'%t
        t_svg = re.compile(num, re.S)
        x_svg,y_svg = re.findall(t_svg, htmll)[0]
        list1 = [x_svg,y_svg]
        svg_list.append(list1)
    print(svg_list)

    # 通过tel_svg_url请求电话号码编码详情页面
    htmlll = tel_svg_request(tel_svg_url)
    # 获取电话编码详情页面
    tel_svg_response(htmlll, svg_list)


# =======================================================================
# 通过tel_svg_url请求电话号码编码详情页面
def tel_svg_request(tel_svg_url):
    url = tel_svg_url
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"
    }
    rensponse = requests.get(url, headers=headers)
    if rensponse.status_code == 200:
        return rensponse.content.decode('utf8')
    return None


# 获取电话编码详情页面
def tel_svg_response(htmlll, svg_list):
    tel_text = re.compile('<text x=".*?" y=".*?">(.*?)</text>', re.S)
    tel_text = re.findall(tel_text, htmlll)
    tel_t = [tel_t.strip() for tel_t in tel_text][-1]
    print(tel_t) #最后一行电话编码内容：295627081238518460474235

    i = 0
    tel_svg_num = ''
    # 遍历每一个svg矢量图位移
    for svg in svg_list:
        # 切割，却前面的数值
        s = svg[0].split('.')[0]
        # print(s)
        # 通过运算得出一个值
        tel_s = (int(s) + 8)/(-14)
        # print(tel_s)
        # 如果是第三位就添加'_'
        if i == 3:
            tel_svg_num += ' '
            # 通过tel_s就是下标，获取最后一行字符串下标对应的元素，就是电话号码
            tel_svg_num += tel_t[int(tel_s)]
        else:
            # 通过tel_s就是下标，获取最后一行字符串下标对应的元素，就是电话号码
            tel_svg_num += tel_t[int(tel_s)]
        i += 1
    # 电话号码
    print(tel_svg_num)


def main():
    html = da_request()
    da_response(html)


if __name__ == '__main__':
    main()