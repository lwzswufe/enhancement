# author='lwz'
# coding:utf-8
# 提取统计局地区列表
import urllib.request
import re
import time

SQL_FILENAME = ""
LOG_FILENAME = ""
BASE_URL = ""

def web_visit(urlstr='http://www.sse.com.cn/assortment/options/disclo/preinfo/', times=1):
    
    timestr = time.strftime("%H:%M:%S", time.localtime())
    try:
        unicode_data = urllib.request.urlopen(urlstr).read()
        webstr = unicode_data.decode('gbk', 'ignore')
    except Exception as err:
        log_str = "{} error in {}st visit:{}\n".format(timestr, times, urlstr)
        webstr = ""
    else:
        log_str = "{} successful    visit:{}\n".format(timestr, urlstr)
    # 写日志
    f_log = open(LOG_FILENAME, "a")
    f_log.write(log_str)
    f_log.close()
    return webstr


def web_read(urlstr='http://www.sse.com.cn/assortment/options/disclo/preinfo/'):
    for i in range(3):
        webstr = web_visit(urlstr, i+1)
        # 防止频繁访问
        time.sleep(1)
        if len(webstr) > 0:
            break
    return(webstr)


def get_url(webstr=""):
    '''
    <a href='11.html'>北京市
    510501000000
    从字符串里解析出名称与网页链接 若无网页链接 返回None
    '''
    words = webstr.split("'")
    if len(words) == 3:
        word = words[2][1:]
        url = words[1]
    else:
        word = words[0]
        url = None
    return word, url


def write_msg(data=()):
    '''
    '''
    ID, name, up_area, url = data
    f_sql = open(SQL_FILENAME, "a")
    s = "INSERT INTO FAS_COM_AREA VALUES ({}, {}, {});\n".format(ID, name, up_area)
    f_sql.write(s)
    f_sql.close()


def province_re(urlstr="", up_area=""):
    '''
    省 
    <td><a href='11.html'>北京市<br/></a></td>
    '''
    webstr = web_read(urlstr)
    pattern = re.compile(r"(?<=<td>)[^b]*(?=<br/></a></td>)")
    matchs = re.findall(pattern, string=webstr)
    for i, match in enumerate(matchs):
        name, url_suffix = get_url(match)
        # 省级ID是XX00 0000 0000
        ID = url_suffix[:2] + "0" * 10
        if up_area == "":
            print("{}\t{}".format(name, url_suffix))
        else:
            print("area:{} province:{}/{}".format(name, i+1, len(matchs)))
            url = BASE_URL + url_suffix
            write_msg((ID, name, up_area, urlstr))
            city_re(url, ID)


def city_re(urlstr="", up_area=""):
    '''
    市
    <tr class='citytr'><td><a href='11/1101.html'>110100000000</a></td><td><a href='11/1101.html'>市辖区</a></td></tr>
    <tr class='citytr'><td><a href='51/5101.html'>510100000000</a></td><td><a href='51/5101.html'>成都市</a></td></tr>
    '''
    webstr = web_read(urlstr)
    pattern_ID = re.compile(r"(?<=<tr class='citytr'><td>)[^d]*(?=</a></td><td>)")
    pattern_name = re.compile(r"(?<=</a></td><td>)[^d]*(?=</a></td></tr>)")
    match_ID = re.findall(pattern_ID, string=webstr)
    match_name = re.findall(pattern_name, string=webstr)
    assert len(match_ID) == len(match_name), "{} ID:{} != name:{}".format(urlstr, len(match_ID), len(match_name))

    for i in range(len(match_ID)):
        ID, url_suffix = get_url(match_ID[i])
        name, _ = get_url(match_name[i])
        if up_area == "":
            print("{}\t{}\t{}".format(ID, name, url_suffix))
        else:
            print("area:{} city:{}/{}".format(name, i+1, len(match_ID)))
            url = BASE_URL + url_suffix
            write_msg((ID, name, up_area, urlstr))
            county_re(url, ID)


def county_re(urlstr="", up_area=""):
    '''
    区县
    <tr class='countytr'><td>510501000000</td><td>市辖区</td></tr>
    <tr class='countytr'><td><a href='05/510502.html'>510502000000</a></td><td><a href='05/510502.html'>江阳区</a></td></tr>
    '''
    webstr = web_read(urlstr)
    # 匹配无链接地区
    pattern_ID = re.compile(r"(?<=<tr class='countytr'><td>)\d*(?=</td><td>)")
    pattern_name = re.compile(r"(?<=\d</td><td>)[^<]*(?=</td></tr>)")
    match_ID = re.findall(pattern_ID, string=webstr)
    match_name = re.findall(pattern_name, string=webstr)
    assert len(match_ID) == len(match_name), "{} ID:{} != name:{}".format(urlstr, len(match_ID), len(match_name))
    for i in range(len(match_ID)):
        ID = match_ID[i]
        name = match_name[i]
        if up_area == "":
            print("{}\t{}".format(ID, name))
        else:
            write_msg((ID, name, up_area, urlstr))
    # 匹配有链接地区
    pattern_ID = re.compile(r"(?<=<tr class='countytr'><td>)[^d]*(?=</a></td><td>)")
    pattern_name = re.compile(r"(?<=</a></td><td>)[^d]*(?=</a></td></tr>)")
    match_ID = re.findall(pattern_ID, string=webstr)
    match_name = re.findall(pattern_name, string=webstr)
    assert len(match_ID) == len(match_name), "{} ID:{} != name:{}".format(urlstr, len(match_ID), len(match_name))
    for i in range(len(match_ID)):
        ID, url_suffix = get_url(match_ID[i])
        name, _ = get_url(match_name[i])
        if up_area == "":
            print("{}\t{}\t{}".format(ID, name, url_suffix))
        else:
            print("area:{} county:{}/{}".format(name, i+1, len(match_ID)))
            url = BASE_URL + url_suffix[3:5] + "/" + url_suffix
            write_msg((ID, name, up_area, urlstr))
            town_re(url, ID)


def town_re(urlstr="", up_area=""):
    '''
    乡镇
    <tr class='towntr'><td><a href='08/110108001.html'>110108001000</a></td><td><a href='08/110108001.html'>万寿路街道办事处</a></td></tr>
    '''
    webstr = web_read(urlstr)
    pattern_ID = re.compile(r"(?<=<tr class='towntr'><td>)[^d]*(?=</a></td><td>)")
    pattern_name = re.compile(r"(?<=</a></td><td>)[^d]*(?=</a></td></tr>)")
    match_ID = re.findall(pattern_ID, string=webstr)
    match_name = re.findall(pattern_name, string=webstr)
    assert len(match_ID) == len(match_name), "{} ID:{} != name:{}".format(urlstr, len(match_ID), len(match_name))
    return_list = []
    for i in range(len(match_ID)):
        ID, url_suffix = get_url(match_ID[i])
        name, _ = get_url(match_name[i])
        if up_area == "":
            print("{}\t{}\t{}".format(ID, name, url_suffix))
        else:
            print("area:{} town:{}/{}".format(name, i+1, len(match_ID)))
            url = BASE_URL + url_suffix[3:5] + "/" + url_suffix[5:7] + "/" + url_suffix
            write_msg((ID, name, up_area, urlstr))
            village_re(url, ID)


def village_re(urlstr="", up_area=""):
    '''
    村 居委会
    <tr class='villagetr'><td>110108003001</td><td>111</td><td>海军机关大院社区居委会</td></tr>
    '''
    webstr = web_read(urlstr)
    pattern_ID = re.compile(r"(?<=<tr class='villagetr'><td>)\d{12}(?=</td><td>)")
    pattern_type = re.compile(r"(?<=\d{12}</td><td>)\d{3}(?=</td><td>)")
    pattern_name = re.compile(r"(?<=\d{12}</td><td>\d{3}</td><td>)[^<]*(?=</td></tr>)")
    match_ID = re.findall(pattern_ID, string=webstr)
    match_name = re.findall(pattern_name, string=webstr)
    match_type = re.findall(pattern_type, string=webstr)
    assert len(match_ID) == len(match_name), "{} ID:{} != name:{}".format(urlstr, len(match_ID), len(match_name))
    assert len(match_name) == len(match_type), "{} ID:{} != name:{}".format(urlstr, len(match_type), len(match_name))
    return_list = []
    for i in range(len(match_ID)):
        ID = match_ID[i]
        typecode = match_type[i]
        name = match_name[i]
        if up_area == "":
            print("{}\t{}\t{}".format(ID, typecode, name))
        else:
            write_msg((ID, name, up_area, None))


def test():
    # 省份爬取测试
    url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/index.html"
    province_re(url)
    # 城市爬取测试
    url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/51.html"
    city_re(url)
    # 区县爬取测试
    url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/51/5101.html"
    county_re(url)
    # 乡镇爬取测试
    url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/51/01/510121.html"
    town_re(url)
    # 村 居委会 爬取测试
    url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/51/01/21/510121105.html"
    url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/11/01/02/110102007.html"
    village_re(url)


def main():
    f_sql = open(SQL_FILENAME, "w")
    f_log = open(LOG_FILENAME, "w")
    f_sql.close()
    f_log.close()
    try:
        url = BASE_URL + "index.html"
        province_re(url, up_area="S")
    except AssertionError as err:
        print(err)
    except Exception as err:
        print(err)
    else:
        print("program successful end")
    f_sql = open(SQL_FILENAME, "a")
    f_sql.write("commit")
    f_sql.close()
    f_log.close()


if __name__ == "__main__":
    SQL_FILENAME="C:\\data\\AreaCode.txt"
    LOG_FILENAME="C:\\data\\log.txt"
    BASE_URL="http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/"
    # test()
    main()
