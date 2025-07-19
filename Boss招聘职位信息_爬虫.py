"""
爬虫抓取boss直聘职位信息
drissionpage模块
1.打开浏览器，访问网站
2.获取数据
3.解析数据
4.保存数据
"""
# 第一次使用时配置浏览器地址
# from DrissionPage import ChromiumOptions
# # 请改为你电脑内Chrome可执行文件路径
# path = r'C:\Users\31587\AppData\Local\Google\Chrome\Application\chrome.exe'
# ChromiumOptions().set_browser_path(path).save()

# 1.打开浏览器，访问网站
# 导入自动化模块
from DrissionPage import ChromiumPage
# 导入格式化输出模块-方便查看数据
from pprint import pprint
# 导入csv模块保存数据
import csv
import time
# 创建文件
f=open('data_new.csv',mode='w',encoding='utf-8',newline='')
# 字典写入的方法-文件，字段名
csv_writer=csv.DictWriter(f,fieldnames=[
        '关键词',
        '职位',
        '薪资',
        '学历',
        '经验',
        '公司',
        '城市',
        '领域',
        '规模',
        '性质',
        '区域',
        '商圈',
        '纬度',
        '经度',
        '技能列表',
        '福利列表',
])
# 写入标头
csv_writer.writeheader()
# 打开浏览器(实例化一个浏览器对象)
dp = ChromiumPage()

# 2.获取数据
# a.通过元素定位，获取数据
# 通过元素面板-前端代码渲染后的
# 通过数据所在标签，进行定位获取标签里的内容（有时不适用-字体加密）
# b.监听数据包，获取数据
# 监听数据包链接特征，直接获取响应数据
# 监听要在执行动作之前-即访问网站之前
# 监听数据包
dp.listen.start('search/joblist.json')
# 访问网站
keywords = ["python", "java", "前端", "后端", "产品经理", "测试", "算法", "数据分析"]
cities = ["100010000"]

for keyword in keywords:
    for city in cities:
        url = f"https://www.zhipin.com/web/geek/jobs?query={keyword}&city={city}"
        dp.get(url)
# for keyword in keywords:
#     dp.get(f'https://www.zhipin.com/web/geek/jobs?query={keyword}&city=100010000')
# 循环翻页
    for page in range(1,6): # 20页大概2，300条数据 每个方向爬5页
        print(f'正在采集第{page}页的数据内容')
        # 等待数据包加载
        r=dp.listen.wait()
        # 获取响应数据
        json_data=r.response.body
        """3.解析数据"""
        # 获取的数据都是字典类型，那么解析数据首先需要
        # 字典取值-键值对取值
        # 提取职位信息所在列表
        jobList=json_data['zpData']['jobList']
        # 遍历提取列表里的元素
        for job in jobList:
            try:
                """在循环中提取每条职位消息内容"""
                dit={
                    '关键词': keyword,
                    '职位':job['jobName'],
                    '薪资':job['salaryDesc'],
                    '学历':job['jobDegree'],
                    '经验':job['jobExperience'],
                    '公司':job['brandName'],
                    '城市':job['cityName'],
                    '领域':job['brandIndustry'],
                    '规模':job['brandScaleName'],
                    '性质':job['brandStageName'],
                    '区域':job['areaDistrict'],
                    '商圈':job['businessDistrict'],
                    '纬度':job['gps']['latitude'],
                    '经度':job['gps']['longitude'],
                    '技能列表': ' '.join(job['skills']),
                    '福利列表': ' '.join(job['welfareList']),
                }
                # 写入数据
                csv_writer.writerow(dit)
                print(dit)
            except:
                pass
        # 5.批量采集数据-下滑进行翻页
        # 定位职位信息 针对元素进行下滑
        tab = dp.ele('css:.job-list-container')
        dp.scroll.to_bottom()  # 滑动整个页面
        # tab.scroll.to_bottom() # 滑动一部分
        time.sleep(2)  # 等待数据加载







