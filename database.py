# coding=utf-8
import sqlite3
import sys
from contextlib import closing

print sys.getdefaultencoding()
locationDict = {"1": u"上海"}
regionDict = \
    {"r1": u"卢湾区",
     "r2": u"徐汇区",
     "r3": u"静安区",
     "r4": u"长宁区",
     "r5": u"浦东新区",
     "r6": u"黄浦区",
     "r7": u"普陀区",
     "r8": u"闸北区",
     "r9": u"虹口区",
     "r10": u"杨浦区",
     "r12": u"闵行区",
     "r13": u"宝山区",
     "r5937": u"松江区",
     "r5939": u"青浦区",
     "r8846": u"奉贤区",
     "r8847": u"金山区",
     "r5938": u"嘉定区",
     "c3580": u"崇明县", }
categoryDict = {
    "20": u"购物",
    "10": u"美食",
    "30": u"休闲娱乐",
    "40": u"会议宴会",
    "50": u"丽人",
    "60": u"酒店",
    "70": u"亲子",
    "80": u"生活服务",
    "90": u"家装",
}
subcategoryDict = {
    "g114": u"韩国料理",
    "g101": u"本帮江浙菜",
    "g113": u"日本菜",
    "g132": u"咖啡厅",
    "g112": u"小吃快餐",
    "g117": u"面包甜点",
    "g110": u"火锅",
    "g116": u"西餐",
    "g111": u"自助餐",
    "g103": u"粤菜",
    "g508": u"烧烤",
    "g102": u"川菜",
    "g115": u"东南亚菜",
    "g109": u"素菜",
    "g106": u"东北菜",
    "g104": u"湘菜",
    "g248": u"云南菜",
    "g3243": u"新疆菜",
    "g251": u"海鲜",
    "g26481": u"西北菜",
    "g203": u"蟹宴",
    "g107": u"台湾菜",
    "g105": u"贵州菜",
    "g108": u"清真菜",
    "g118": u"其他",
    "g133": u"酒吧",
    "g246": u"湖北菜",
    "g247": u"江西菜",
    "g249": u"闽菜",
    "g250": u"创意菜",
    "g252": u"其他中餐",
    "g311": u"北京菜",
    "g26482": u"徽菜",
    "g26484": u"山西菜",
    "g135": u"KTV",
    "g141": u"足疗按摩",
    "g140": u"洗浴",
    "g20041": u"私人影院",
    "g5672": u"温泉",
    "g20042": u"网吧网咖",
    "g144": u"DIY手工坊",
    "g20040": u"轰趴馆",
    "g2754": u"密室",
    "g20038": u"采摘/农家乐",
    "g6694": u"桌面游戏",
    "g32732": u"棋牌室",
    "g137": u"游乐游艺",
    "g134": u"茶馆",
    "g156": u"桌球馆",
    "g20039": u"真人CS",
    "g2827": u"中医养生",
    "g142": u"文化艺术",
    "g136": u"电影院",
    "g26490": u"更多休闲娱乐",
    "g165": u"婚宴",
    "g3014": u"会议培训",
    "g3016": u"活动聚会",
    "g3018": u"宴请招待",
    "g1040": u"星级酒店",
    "g1191": u"特色餐厅",
    "g2738": u"婚礼会所",
    "g2740": u"游轮婚礼",
    "g157": u"美发",
    "g158": u"美容/SPA",
    "g33761": u"美甲美睫",
    "g148": u"瑜伽",
    "g149": u"舞蹈",
    "g2898": u"纹绣",
    "g159": u"瘦身纤体",
    "g493": u"纹身",
    "g2572": u"祛痘",
    "g183": u"整形",
    "g2790": u"产后塑形",
    "g6700": u"个性写真",
    "g26465": u"小区",
    "g237": u"银行",
    "g181": u"医院",
    "g4607": u"快照/冲印",
    "g26117": u"居家维修",
    "g195": u"家政",
    "g835": u"通信营业厅",
    "g612": u"体检中心",
    "g197": u"旅行社",
    "g980": u"售票点",
    "g836": u"房屋地产",
    "g2929": u"搬家",
    "g32742": u"物流快递",
    "g2932": u"管道疏通",
    "g120": u"服饰鞋包",
    "g187": u"超市便利店",
    "g119": u"综合商场",
    "g235": u"药店",
    "g125": u"亲子购物",
    "g27809": u"儿童服饰",
    "g27810": u"玩具",
    "g27811": u"宝宝用品",
    "g27812": u"孕产用品",
    "g128": u"眼镜店",
    "g123": u"化妆品",
    "g122": u"珠宝饰品",
    "g6715": u"黄金珠宝",
    "g6716": u"精工名表",
    "g6717": u"流行饰品",
    "g26085": u"花店",
    "g124": u"数码产品",
    "g121": u"运动户外",
    "g127": u"书店",
    "g126": u"家居建材",
    "g6828": u"厨房卫浴",
    "g6827": u"家具",
    "g6829": u"家纺/床上用品",
    "g6830": u"更多家居用品",
    "g20020": u"客厅卧室主材",
    "g20022": u"墙面材料",
    "g20023": u"智能家居",
    "g20025": u"管线辅料",
    "g32703": u"家居软装",
    "g32705": u"家用电器",
    "g129": u"特色集市",
}


fileNames = ["data/dianping_beauty_geocoding.csv",
             "data/dianping_conference_geocoding.csv",
             "data/dianping_entertainment_geocoding.csv",
             "data/dianping_food_geocoding.csv",
             "data/dianping_life_service_geocoding.csv",
             "data/dianping_shopping_geocoding.csv",]
conn = sqlite3.connect("store.db")
for fileName in fileNames:
    with open(fileName, 'r') as f:
        f.next()
        count = 1
        try:
            while True:
                print count
                r = f.next().rstrip("\n").split(",")
                if len(r) > 10:
                    address = "".join(r[5:-5])
                else:
                    address = r[5]
                location, region, category, subcategory, address, name, lng, lat, confidence = \
                        locationDict[r[0]], regionDict[r[1]], categoryDict[r[2]], subcategoryDict[r[3]], \
                        r[5], r[6], r[7], r[8], r[9]
                if lng != "None":
                    execsql = """insert into store (location,region,category,subcategory,address,name,lng,lat,confidence) values ("{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}","{9}")""".format(
                        str(count), location, region, category, subcategory, address, name, lng, lat, confidence)
                    conn.execute(execsql)
                count += 1
                conn.commit()
        except sqlite3.OperationalError:
            print count
            for i in r:
                print i
            pass
        except StopIteration:
            print 'write over ~'
