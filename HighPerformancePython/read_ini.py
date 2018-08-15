# author='lwz'
# coding:utf-8
'''
[section]
name=value
或者
name: value
"#" 和";" 表示注释

[DEFAULT] #设置默认的变量值，初始化

[My Section]
foodir: %(dir)s/whatever
dir=frob
long: this value continues
   in the next line
在调用这三个函数时，切记这三个函数会将调用optionxform()，在传递键值对数据时，会将键名 全部转化为小写

ConfigParser.Error	所有异常的基类
ConfigParser.NoSectionError	指定的section没有找到
ConfigParser.DuplicateSectionError	调用add_section() 时，section名称已经被使用
ConfigParser.NoOptionError	指定的参数没有找到
ConfigParser.InterpolationError	当执行字符串插值时出现问题时，出现异常的基类
ConfigParser.InterpolationDepthError	当字符串插值无法完成时，因为迭代次数超过了最大的范围，所以无法完成。InterpolationError的子类
InterpolationMissingOptionError	当引用的选项不存在时，会出现异常。InterpolationError的子类
ConfigParser.InterpolationSyntaxError	当产生替换的源文本不符合所需的语法时，就会出现异常。InterpolationError的子类。
ConfigParser.MissingSectionHeaderError	当试图解析一个没有分段标题的文件时，会出现异常。
ConfigParser.ParsingError	当试图解析文件时发生错误时，会出现异常
ConfigParser.MAX_INTERPOLATION_DEPTH	当raw参数为false时，get()的递归插值的最大深度。这只适用于ConfigParser类
参见 https://blog.csdn.net/miner_k/article/details/77857292
'''
import configparser


def get_ini():
    fn = ".//pip//pip.ini.txt"
    config = configparser.ConfigParser()
    with open(fn, 'r', encoding='utf-8') as f:
        config.read_file(f)
    return config


def read_ini(config):
    str_ = config.get("global", "index-url")        # 获取[global]部分index-url的值
    print(str_)


if __name__ == "__main__":
    config = get_ini()
    read_ini(config)
