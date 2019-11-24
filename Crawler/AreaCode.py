# author='lwz'
# coding:utf-8
# 提取统计局地区列表
import urllib.request
import re
import time
import os


# 进度类
class Position(object):
    def __init__(self, province=0, city=0, county=0, town=0):
        self.province = province 
        self.city = city
        self.county = county
        self.town = town
    
    def get_id(self):
        return self.province* 1000000 + self.city * 10000 + self.county * 100 + self.town

# 当前节点类
class CurrentPosition(Position):
    def __init__(self, province=0, city=0, county=0, town=0):
        super().__init__(province, city, county, town)
        self.province_num = 0
        self.city_num = 0
        self.county_num = 0
        self.town_num = 0
        self.province_name = ""
        self.city_name = ""
        self.county_name = ""
        self.town_name = ""

    def update_province(self, province_num=0, province=0, province_name=""):
        self.province = province
        self.city = 0
        self.county = 0
        self.town = 0
        self.province_name = province_name
        self.province_num = province_num
        print("{} province:{}/{}".format(province_name, province, province_num))
    
    def update_city(self, city_num=0, city=0, city_name=""):
        self.city = city
        self.county = 0
        self.town = 0
        self.city_name = city_name
        self.city_num = city_num
        print("province:{}/{} city:{}/{} {}-{}".format(self.province, self.province_num, 
        city, city_num, self.province_name, self.city_name))
    
    def update_county(self, county_num=0, county=0, county_name=""):
        self.county = county
        self.town = 0
        self.county_name = county_name
        self.county_num = county_num
        print("province:{}/{} city:{}/{} county:{}/{} {}-{}-{}".format(self.province, self.province_num, 
        self.city, self.city_num, county, county_num, self.province_name, self.city_name, self.county_name))
    
    def update_town(self, town_num=0, town=0, town_name=""):
        self.town = town
        self.town_name = town_name
        self.town_num = town_num
        print("province:{}/{} city:{}/{} county:{}/{} town:{}/{} {}-{}-{}-{}".format(self.province, self.province_num, 
        self.city, self.city_num, self.county, self.county_num, town, town_num, self.province_name, self.city_name, 
        self.county_name, town_name))

# 爬取数据类
class Spider(object):
    def __init__(self, sql_filename="", log_filename ="", base_url ="", visit_time_interval=0.5,
                start_pos=Position(0, 0, 0, 0), end_pos=Position(34, 0, 0, 0)):
        self.sql_filename = sql_filename
        self.log_filename = log_filename
        self.base_url = base_url
        self.visit_time_interval = visit_time_interval
        self.start_pos = start_pos
        self.pos = CurrentPosition(0, 0, 0, 0)
        self.end_pos = end_pos

    def web_visit(self, urlstr='http://www.sse.com.cn/assortment/options/disclo/preinfo/', times=1):
        '''
        访问url 获取数据
        '''
        timestr = time.strftime("%H:%M:%S", time.localtime())
        try:
            unicode_data = urllib.request.urlopen(urlstr).read()
            webstr = unicode_data.decode('gbk', 'ignore')
        except Exception as err:
            log_str = "{} error in {}st visit:{}\n".format(timestr, times, urlstr)
            webstr = ""
        else:
            log_str = "{} successful    visit:{}\n".format(timestr, urlstr)
        # 写日志path
        if os.path.exists(self.log_filename):
            f_log = open(self.log_filename, "a")
            f_log.write(log_str)
            f_log.close()
        else:
            print(log_str)
        webstr = webstr.replace("\n", "")
        webstr = webstr.replace("\r", "")
        return webstr

    def web_read(self, urlstr='http://www.sse.com.cn/assortment/options/disclo/preinfo/'):
        for i in range(3):
            webstr = self.web_visit(urlstr, i+1)
            # 防止频繁访问
            time.sleep(self.visit_time_interval)
            if len(webstr) > 0:
                break
        return(webstr)

    def get_url(self, webstr=""):
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

    def write_msg(self, data=()):
        '''
        '''
        ID, name, up_area, url = data
        f_sql = open(self.sql_filename, "a")
        s = "INSERT INTO FAS_COM_AREA VALUES ('{}', '{}', '{}');\n".format(ID, name, up_area)
        f_sql.write(s)
        f_sql.close()

    def province_re(self, urlstr="", up_area=""):
        '''
        省 
        <td><a href='11.html'>北京市<br/></a></td>
        '''
        webstr = self.web_read(urlstr)
        pattern = re.compile(r"(?<=<td>)[^b]*(?=<br/></a></td>)")
        matchs = re.findall(pattern, string=webstr)
        # 判断是否需要从指定位置开始爬取
        if self.start_pos.province > 0:
            i = start_pos.province - 1
            start_province = start_pos.province - 1
        else:
            i = 0
            start_province = -1
        # 开始爬取省份
        while i < len(matchs):
            match = matchs[i]
            name, url_suffix = self.get_url(match)
            # 省级ID是XX00 0000 0000
            ID = url_suffix[:2] + "0" * 10
            if up_area == "":
                print("{}\t{}".format(name, url_suffix))
            else:
                self.pos.update_province(len(matchs), i+1, name)
                if self.pos.get_id() >= self.end_pos.get_id():
                    return
                url = self.base_url + url_suffix
                if i == start_province:
                    self.city_re(url, ID, False)
                else:
                    self.write_msg((ID, name, up_area, urlstr))
                    self.city_re(url, ID)
            i += 1

    def city_re(self, urlstr="", up_area="", is_write=True):
        '''
        市
        <tr class='citytr'><td><a href='11/1101.html'>110100000000</a></td><td><a href='11/1101.html'>市辖区</a></td></tr>
        <tr class='citytr'><td><a href='51/5101.html'>510100000000</a></td><td><a href='51/5101.html'>成都市</a></td></tr>
        '''
        webstr = self.web_read(urlstr)
        pattern_ID = re.compile(r"(?<=<tr class='citytr'><td>)[^d]*(?=</a></td><td>)")
        pattern_name = re.compile(r"(?<=</a></td><td>)[^d]*(?=</a></td></tr>)")
        match_ID = re.findall(pattern_ID, string=webstr)
        match_name = re.findall(pattern_name, string=webstr)
        assert len(match_ID) == len(match_name), "{} ID:{} != name:{}".format(urlstr, len(match_ID), len(match_name))

        # 判断是否需要从指定位置开始爬取
        if not is_write and self.start_pos.city > 0:
            i = self.start_pos.city - 1
            start_city = self.start_pos.city - 1
        else:
            i = 0
            start_city = -1

        while i < len(match_ID):
            ID, url_suffix = self.get_url(match_ID[i])
            name, _ = self.get_url(match_name[i])
            if up_area == "":
                print("{}\t{}\t{}".format(ID, name, url_suffix))
            else:
                self.pos.update_city(len(match_ID), i+1, name)
                if self.pos.get_id() >= self.end_pos.get_id():
                    return
                url = self.base_url + url_suffix
                if i == start_city:
                    self.county_re(url, ID, False)
                else:
                    self.write_msg((ID, name, up_area, urlstr))
                    self.county_re(url, ID)
            i += 1


    def county_re(self, urlstr="", up_area="", is_write=True):
        '''
        区县
        <tr class='countytr'><td>510501000000</td><td>市辖区</td></tr>
        <tr class='countytr'><td><a href='05/510502.html'>510502000000</a></td><td><a href='05/510502.html'>江阳区</a></td></tr>
        '''
        webstr = self.web_read(urlstr)
        # 东莞市等部分城市 市下面设乡镇 不设区县
        if webstr.find("<tr class='townhead'>") > 0:
            if up_area != "":
                self.pos.update_county(1, 1, "市直辖乡镇")
            town_re(urlstr, up_area)
            return
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
                if is_write or self.start_pos.county <= 0:
                    self.write_msg((ID, name, up_area, urlstr))
        # 判断是否需要从指定位置开始爬取
        if not is_write and self.start_pos.county > 0:
            i = self.start_pos.county - 1
            start_county = self.start_pos.county - 1
        else:
            i = 0
            start_county = -1
        # 匹配有链接地区
        pattern_ID = re.compile(r"(?<=<tr class='countytr'><td>)[^d]*(?=</a></td><td>)")
        pattern_name = re.compile(r"(?<=</a></td><td>)[^d]*(?=</a></td></tr>)")
        match_ID = re.findall(pattern_ID, string=webstr)
        match_name = re.findall(pattern_name, string=webstr)
        assert len(match_ID) == len(match_name), "{} ID:{} != name:{}".format(urlstr, len(match_ID), len(match_name))
        while i < len(match_ID):
            ID, url_suffix = self.get_url(match_ID[i])
            name, _ = self.get_url(match_name[i])
            if up_area == "":
                print("{}\t{}\t{}".format(ID, name, url_suffix))
            else:
                self.pos.update_county(len(match_ID), i+1, name)
                if self.pos.get_id() > self.end_pos.get_id():
                    return
                url = self.base_url + url_suffix[3:5] + "/" + url_suffix
                if i == start_county:
                    self.town_re(url, ID, False)
                else:
                    self.write_msg((ID, name, up_area, urlstr))
                    self.town_re(url, ID)
            i += 1


    def town_re(self, urlstr="", up_area="", is_write=True):
        '''
        爬取乡镇
        <tr class='towntr'><td><a href='08/110108001.html'>110108001000</a></td><td><a href='08/110108001.html'>万寿路街道办事处</a></td></tr>
        '''
        webstr = self.web_read(urlstr)
        pattern_ID = re.compile(r"(?<=<tr class='towntr'><td>)[^d]*(?=</a></td><td>)")
        pattern_name = re.compile(r"(?<=</a></td><td>)[^d]*(?=</a></td></tr>)")
        match_ID = re.findall(pattern_ID, string=webstr)
        match_name = re.findall(pattern_name, string=webstr)
        assert len(match_ID) == len(match_name), "{} ID:{} != name:{}".format(urlstr, len(match_ID), len(match_name))
        # 判断是否需要从指定位置开始爬取
        if not is_write and self.start_pos.town > 0:
            i = self.start_pos.town - 1
            start_town = self.start_pos.town - 1
        else:
            i = 0
            start_town = -1
        # 爬取乡镇
        while i < len(match_ID):
            ID, url_suffix = self.get_url(match_ID[i])
            name, _ = self.get_url(match_name[i])
            if up_area == "":
                print("{}\t{}\t{}".format(ID, name, url_suffix))
            else:
                self.pos.update_town(len(match_ID), i, name)
                if self.pos.get_id() > self.end_pos.get_id():
                    return
                if url_suffix[7:9] == "00":
                    url = self.base_url + url_suffix[3:5] + "/" + url_suffix
                else:
                    url = self.base_url + url_suffix[3:5] + "/" + url_suffix[5:7] + "/" + url_suffix
                if i == start_town:
                    pass
                else:
                    self.write_msg((ID, name, up_area, urlstr))
                self.village_re(url, ID)
            i += 1


    def village_re(self, urlstr="", up_area=""):
        '''
        爬取村 居委会
        <tr class='villagetr'><td>110108003001</td><td>111</td><td>海军机关大院社区居委会</td></tr>
        '''
        webstr = self.web_read(urlstr)
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
                self.write_msg((ID, name, up_area, None))


def test():
    spider = Spider()
    # 省份爬取测试
    url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/index.html"
    spider.province_re(url)
    # 城市爬取测试
    
    url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/51.html"
    spider.city_re(url)
    # 区县爬取测试
    url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/44/4419.html"
    url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/51/5101.html"
    spider.county_re(url)
    # 乡镇爬取测试
    url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/51/01/510121.html"
    spider.town_re(url)
    # 村 居委会 爬取测试
    url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/51/01/21/510121105.html"
    url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/11/01/02/110102007.html"
    url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/37/15/22/371522004.html"
    spider.village_re(url)


def main(sql_filename, log_filename, base_url, start_pos, end_pos):
    if (start_pos.province <= 0):
        f_sql = open(sql_filename, "w")
        f_log = open(log_filename, "w")
        f_sql.close()
        f_log.close()
    try:
        url = base_url + "index.html"
        spider = Spider(log_filename=log_filename, sql_filename=sql_filename, base_url=base_url, 
                        visit_time_interval=0.33, start_pos=start_pos, end_pos=end_pos)
        spider.province_re(url, up_area="S")
    except AssertionError as err:
        print(err)
    except Exception as err:
        print(err)
    else:
        print("program successful end")
    f_sql = open(sql_filename, "a")
    f_sql.write("commit")
    f_sql.close()


if __name__ == "__main__":
    sql_filename="D:\\data\\AreaCode.txt"
    log_filename="D:\\data\\log.txt"
    base_url="http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/"
    # test()
    # 设置起始爬取的位置
    start_pos = Position(province=8, city=9, county=0, town=0)
    # 设置终止爬取的位置
    end_pos = Position(province=13, city=2, county=0, town=0)
    main(sql_filename, log_filename, base_url, start_pos, end_pos)
