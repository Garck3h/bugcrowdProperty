# -*- coding:utf-8 -*-
import json
import random
from time import sleep
import httpx
import pandas as pd

def getTarget():
    #获取范围从1到9的整数，这里就是1-9页的数据
    for i in range(1,10):
        url = f'https://bugcrowd.com/programs.json?vdp[]=false&sort[]=promoted-desc&hidden[]=false&page[]={i}'
        print("第"+ str(i) +"页："+url)
        # 请求发送
        response = httpx.get(url=url, headers=headers,timeout=None,verify=False)
        # 获取响应数据
        json_data = json.loads(response.text)
        #因为返回的是json，所以比较好处理直接通过for输出我们想要的目标
        for program in json_data["programs"]:
            #获取了资产（公司）的名称
            program_url = program.get("program_url")
            if program_url:
                #根据资产构建获取URL的api
                programUrlEnd = "https://bugcrowd.com" + program_url+"/target_groups"
                # 获取每个目标的Api，如特斯拉的资产Api
                getTargetApi(program_url,programUrlEnd)
        #随机延迟一下，时间是4-15s这个区间
        time = random.randint(4,16)
        print("延迟"+str(time)+"s")
        sleep(time)
        print("\n")


def getTargetApi(program_url,url):
    #根据资产名称的接口获取能够获取资产的API
    print("资产名："+program_url.replace("/", ""))
    print("探测获取API："+url)
    response = httpx.get(url=url, headers=headers, timeout=None,verify=False)
    print("状态："+str(response.status_code))
    #如果不能资产名称的接口，就忽略掉，这里只要成功200的
    if response.status_code == 200:
        targetApiArry = []
        #这里是存储了能获取到资产的公司的名称（或项目名称）
        programNameArry.append(program_url.replace("/", ""))
        #拿到了获取资产的结果
        json_data = json.loads(response.text)
        for targets in json_data["groups"]:
            #也是json格式的数据，我们把想要的拿出来
            targets_url = targets.get("targets_url")
            if targets_url:
                targets_url = "https://bugcrowd.com" + targets_url
                print("Api："+ targets_url)
                targetApiArry .append(targets_url)
        #封装为一个字典，每一个资产对应属于自己的接口
        targetApiDit[program_url.replace("/", "")] = targetApiArry
    print("\n")


def getTargetUrl():
    #遍历我们上面拿到的一个字典，里面存储着项目名称以及能够获取到测试URL的接口
    for key, values in targetApiDit.items():
        print("当前资产："+key)
        #定义一个空数组，循环一次就清空一次，同时下面也会同步写入到一个新的字典里面，实现了每个项目名称所对应的测试URL
        TargetUrl = []
        for value in values:
            #进行请求获取测试URL的API
            response = httpx.get(url=value, headers=headers, timeout=None,verify=False)
            #获取响应数据
            json_data = json.loads(response.text)
            #遍历一下，拿到uri
            for uri in json_data["targets"]:
                uri_url = uri.get("uri")
                if uri_url:
                    #把同一个项目的URI存到这个数组里面
                    TargetUrl.append(uri_url)
                    #把所有的URI都存到这个数组里面，下面直接调用就输出了一个全部URI的txt文件
                    MergeTxt.append(uri_url)
        #根据测试项目做为key，所属项目的测试URI做为value 构造成一个新的字典，下面写到Excel的时候用到
        resultXlsxDit[key] = TargetUrl

def outPutMergeTxt():
    # 打开文本文件进行写入
    with open('output.txt', 'w') as file:
        # 将数组中的每个元素写入文本文件的新行中
        for item in MergeTxt:
            file.write(str(item) + '\n')

def outPutXlsx():
    # 将字典转换为DataFrame
    df = pd.DataFrame(pd.DataFrame.from_dict(resultXlsxDit, orient='index').values.T,
                      columns=list(resultXlsxDit.keys()))  # 防止输入的数值长度不一样的时候会崩掉
    # 将DataFrame保存为XLSX文件
    df.to_excel('output.xlsx', engine='xlsxwriter',index=False)


if __name__ == '__main__':
    # #存储目标的名称
    programNameArry = []
    #存储目标的名称和每个目标的api
    targetApiDit = {}
    #存储着所有获取到到目标URL，后面调用它直接输出一个txt
    MergeTxt = []
    #存储着，资产的公司为key，其资产为value的字典
    resultXlsxDit = {}

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 SLBrowser/8.0.0.2242 SLBChan/10'
        , 'Accept': '*/*'}
    #获取目标；如：特斯拉、某gov等
    getTarget()
    #根据上述的Api，进行访问获取得到资产URL
    getTargetUrl()
    #根据每个目标获取到的资产输出为txt
    outPutMergeTxt()
    #合并所有内容输出为Excel
    outPutXlsx()



