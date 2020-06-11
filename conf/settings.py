#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os
import redis
import json

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

"""
自添加USER_AGENT请按照已有数据的格式来添加
"""

USER_AGENT = [
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Tri dent/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)',
    'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64;Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
    'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.33 Safari/534.3 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)'
]

false = False
null = None
true = True

# 目标数据的模板样本
TARGET_LIST = [

]


LOG_LEVEL = logging.ERROR

LOG_PATH = 'error.log'

# redis数据库连接池
'可以自行设置为其他的数据库'
# POOL = redis.ConnectionPool(host='127.0.0.1', max_connections=80, decode_responses=True, db=1)  # 测试时存储的数据库
# FIRST_POOL = redis.ConnectionPool(host='127.0.0.1', max_connections=80, decode_responses=True, db=2)  # 第一次清洗之后的数据
# SECOND_POOL = redis.ConnectionPool(host='127.0.0.1', max_connections=80, decode_responses=True, db=3)  # 第二次清洗之后的数据

# 新的存储池
POOL = redis.ConnectionPool(host='127.0.0.1', max_connections=80, decode_responses=True, db=4)  # 测试时存储的数据库
FIRST_POOL = redis.ConnectionPool(host='127.0.0.1', max_connections=80, decode_responses=True, db=5)  # 第一次清洗之后的数据
SECOND_POOL = redis.ConnectionPool(host='127.0.0.1', max_connections=80, decode_responses=True, db=6)  # 第二次清洗之后的数据

# mysql数据库相关

REMOTE_MYSQL_HOST = '127.0.0.1'
REMOTE_MYSQL_PORT = 3306
REMOTE_MYSQL_USER = 'root'
REMOTE_MYSQL_PASSWORD = ''
REMOTE_MYSQL_DB = '' # 留空


# 携程池个数
GEVENT_POOL = 15

# 页码结束页
PAGE = 10

# 过去最长时间，从当前日期到过去的最长天数，只取最近几天的数据，单位：天

LANG_TIME = 31

# 定时相关

# 定时存入队列
APS_QUEUE_INTERVAL = 30

# 定时存入redis数据库
APS_REDIS_INTERVAL = 60

# 定时运行，20分钟轮询一次
RUN_INTERVAL = 20

# 过滤关键词
FILTER_KEYWORDS = {

}

# 过滤长度

MIN_LENGTH = 100

# 城市字段
CITYLIST = {
    "北京": {'东城', '西城', '朝阳', '丰台', '石景山', '海淀', '顺义', '通州', '大兴', '房山', '门头沟', '昌平', '平谷', '密云', '怀柔', '延庆'},
    "上海": {'黄浦', '徐汇', '长宁', '静安', '普陀', '虹口', '杨浦', '闵行', '宝山', '嘉定', '浦东新区', '金山', '松江', '青浦', '奉贤', '崇明'},
    "天津": {'和平', '河东', '河西', '南开', '河北', '红桥', '东丽', '西青', '津南', '北辰', '武清', '宝坻', '滨海新', '宁河', '静海'},
    "重庆": {'万州', '涪陵', '渝中', '大渡口', '江北', '沙坪坝', '九龙坡', '南岸', '北碚', '綦江', '大足', '渝北', '巴南', '黔江', '长寿', '江津', '合川',
           '永川', '南川', '璧山', '铜梁', '潼南', '荣昌'},
    "安徽": {
        "合肥", "芜湖", "蚌埠", "淮南", "马鞍山", "淮北", "铜陵", "安庆", "黄山", "滁州", "阜阳", "宿州", "六安", "亳州", "池州", "宣城", "巢湖", "桐城",
        "天长", "明光", "界首", "宁国"
    },
    "福建": {
        "福州", "厦门", "莆田", "三明", "泉州", "漳州", "南平", "龙岩", "宁德", "福清", "长乐", "永安", "石狮", "晋江", "南安", "龙海", "邵武", "武夷山",
        "建瓯", "漳平", "福安", "福鼎"
    },
    "广东": {
        "广州", "韶关", "深圳", "珠海", "汕头", "佛山", "江门", "湛江", "茂名", "肇庆", "惠州", "梅州", "汕尾", "河源", "阳江", "清远", "东莞", "中山",
        "潮州", "揭阳", "云浮", "乐昌", "南雄", "台山", "开平", "鹤山", "恩平", "廉江", "雷州", "吴川", "高州", "化州", "信宜", "四会", "兴宁", "陆丰",
        "阳春", "英德", "连州", "普宁", "罗定"
    },
    "广西": {
        "南宁", "柳州", "桂林", "梧州", "北海", "防城港", "钦州", "贵港", "玉林", "百色", "贺州", "河池", "来宾", "崇左", "岑溪", "东兴", "桂平", "北流",
        "靖西", "宜州", "合山", "凭祥"
    },
    "贵州": {
        "贵阳", "六盘水", "遵义", "安顺", "毕节", "铜仁", "清镇", "赤水", "仁怀", "兴义", "凯里", "都匀", "福泉"
    },
    "甘肃": {
        "兰州", "嘉峪关", "金昌", "白银", "天水", "武威", "张掖", "平凉", "酒泉", "庆阳", "定西", "陇南", "玉门", "敦煌", "临夏", "合作"
    },
    "海南": {
        "海口", "三亚", "三沙", "儋州", "五指山", "琼海", "文昌", "万宁", "东方"
    },
    "河南": {
        "郑州", "开封", "洛阳", "平顶山", "安阳", "鹤壁", "新乡", "焦作", "濮阳", "许昌", "漯河", "三门峡", "南阳", "商丘", "信阳", "周口", "驻马店", "巩义",
        "荥阳", "新密", "新郑", "登封", "偃师", "舞钢", "汝州", "林州", "卫辉", "辉县", "沁阳", "孟州", "禹州", "长葛", "义马", "灵宝", "邓州", "永城",
        "项城", "济源"
    },
    "黑龙江": {"哈尔滨", "齐齐哈尔", "鸡西", "鹤岗", "双鸭山", "大庆", "伊春", "佳木斯", "七台河", "牡丹江", "黑河", "绥化", "尚志", "五常", "讷河", "虎林", "密山",
            "铁力", "同江", "富锦", "抚远", "绥芬河", "海林", "宁安", "穆棱", "东宁", "北安", "五大连池", "安达", "肇东", "海伦"},
    "湖北": {
        "武汉", "黄石", "十堰", "宜昌", "襄阳", "鄂州", "荆门", "孝感", "荆州", "黄冈", "咸宁", "随州", "大冶", "丹江口", "宜都", "当阳", "枝江", "老河口",
        "枣阳", "宜城", "钟祥", "应城", "安陆", "汉川", "石首", "洪湖", "松滋", "麻城", "武穴", "赤壁", "广水", "恩施", "利川", "仙桃", "潜江", "天门"
    },
    "湖南": {
        "长沙", "株洲", "湘潭", "衡阳", "邵阳", "岳阳", "常德", "张家界", "益阳", "郴州", "永州", "怀化", "娄底", "浏阳", "醴陵", "湘乡", "韶山", "耒阳",
        "常宁", "武冈", "汨罗", "临湘", "津", "", "沅江", "资兴", "洪江", "冷水江", "涟源", "吉首", "宁乡"
    },
    "河北": {
        "石家庄", "唐山", "秦皇岛", "邯郸", "邢台", "保定", "张家口", "承德", "沧州", "廊坊", "衡水", "辛集", "晋州", "新乐", "遵化", "迁安", "武安", "南宫",
        "沙河", "涿州", "定州", "安国", "高碑店", "泊头", "任丘", "黄骅", "河间", "霸州", "三河", "深州"
    },
    "江苏": {
        "南京", "无锡", "徐州", "常州", "苏州", "南通", "连云港", "淮安", "盐城", "扬州", "镇江", "泰州", "宿迁", "江阴", "宜兴", "新沂", "邳州", "溧阳",
        "常熟", "张家港", "昆山", "太仓", "启东", "如皋", "海门", "东台", "仪征", "高邮", "丹阳", "扬中", "句容", "兴化", "靖江", "泰兴"
    },
    "江西": {
        "南昌", "景德镇", "萍乡", "九江", "新余", "鹰潭", "赣州", "吉安", "宜春", "抚州", "上饶", "乐平", "瑞昌", "共青城", "庐山", "贵溪", "瑞金", "井冈山",
        "丰城", "樟树", "高安", "德兴"
    },
    "吉林": {
        "长春", "四平", "辽源", "通化", "白山", "松原", "白城", "榆树", "德惠", "蛟河", "桦甸", "舒兰", "磐石", "公主岭", "双辽", "梅河口", "集安",
        "临江", "扶余", "洮南", "大安", "延吉", "图们", "敦化", "珲春", "龙井", "和龙"
    },
    "辽宁": {
        "沈阳", "大连", "鞍山", "抚顺", "本溪", "丹东", "锦州", "营口", "阜新", "辽阳", "盘锦", "铁岭", "朝阳", "葫芦岛", "新民", "瓦房店", "庄河", "海城",
        "东港", "凤城", "凌海", "北镇", "盖州", "大石桥", "灯塔", "调兵山", "开原", "北票", "凌源", "兴城"
    },
    "宁夏": {
        "银川", "石嘴山", "吴忠", "固原", "中卫", "灵武", "青铜峡"
    },
    "内蒙古": {
        "呼和浩特", "包头", "乌海", "赤峰", "通辽", "鄂尔多斯", "呼伦贝尔", "巴彦淖尔", "乌兰察布", "霍林郭勒", "满洲里", "牙克石", "扎兰屯", "额尔古纳", "根河", "丰镇",
        "乌兰浩特", "阿尔山", "二连浩特", "锡林浩特"
    },
    "青海": {
        "西宁", "海东", "玉树", "格尔木", "德令哈"
    },
    "山东": {
        "济南", "青岛", "淄博", "枣庄", "东营", "烟台", "潍坊", "济宁", "泰安", "威海", "日照", "临沂", "德州", "聊城", "滨州", "菏泽", "章丘", "胶州",
        "即墨", "平度", "莱西", "滕州", "龙口", "莱阳", "莱州", "蓬莱", "招远", "栖霞", "海阳", "青州", "诸城", "寿光", "安丘", "高密", "昌邑", "曲阜",
        "邹城", "新泰", "肥城", "荣成", "乳山", "乐陵", "禹城", "临清"
    },
    "山西": {
        "太原", "大同", "阳泉", "长治", "晋城", "朔州", "晋中", "运城", "忻州", "临汾", "吕梁", "古交", "潞城", "高平", "介休", "永济", "河津", "原平",
        "侯马", "霍州", "孝义", "汾阳"
    },
    "陕西": {
        "西安", "铜川", "宝鸡", "咸阳", "渭南", "延安", "汉中", "榆林", "安康", "商洛", "兴平", "韩城", "华阴"
    },
    "四川": {
        "成都", "自贡", "攀枝花", "泸州", "德阳", "绵阳", "广元", "遂宁", "内江", "乐山", "南充", "眉山", "宜宾", "广安", "达州", "雅安", "巴中", "资阳",
        "都江堰", "彭州", "邛崃", "崇州", "简阳", "广汉", "什邡", "绵竹", "江油", "峨眉山", "阆中", "华蓥", "万源", "马尔康", "康定", "西昌", "隆昌", '阿坝'
    },
    "新疆": {
        "乌鲁木齐", "克拉玛依", "吐鲁番", "哈密", "昌吉", "阜康", "博乐", "阿拉山口", "库尔勒", "阿克苏", "阿图什", "喀什", "和田", "伊宁", "奎屯", "霍尔果斯",
        "塔城", "乌苏", "阿勒泰", "石河子", "阿拉尔", "图木舒克", "五家渠", "北屯", "铁门关", "双河", "可克达拉", "昆玉"
    },
    "西藏": {
        "拉萨", "日喀则", "山南", "林芝", "昌都", "那曲", "阿里", "日土", "改则"
    },
    "云南": {
        "昆明", "曲靖", "玉溪", "保山", "昭通", "丽江", "普洱", "临沧", "安宁", "宣威", "腾冲", "楚雄", "个旧", "开远", "蒙自", "弥勒", "文山", "景洪",
        "大理", "瑞丽", "芒", "香格里拉"
    },
    "浙江": {
        "杭州", "宁波", "温州", "嘉兴", "湖州", "绍兴", "金华", "衢州", "舟山", "台州", "丽水", "建德", "余姚", "慈溪", "奉化", "瑞安", "乐清", "海宁",
        "平湖", "桐乡", "诸暨", "嵊州", "兰溪", "义乌", "东阳", "永康", "江山", "温岭", "临海", "龙泉"
    },
    "香港": {'中西区', '东区', '南区', '湾仔区', '九龙城区', '观塘区', '深水埗区', '黄大仙区', '油尖旺区', '离岛区', '葵青区', '北区', '西贡区', '沙田区', '大埔区',
           '荃湾区', '屯门区', '元朗区'},
    "澳门": {'花地玛堂', '圣安多尼堂', '大堂', '望德堂', '风顺堂', '嘉模堂', '圣方济各堂', '路氹城'},
    "台湾": {'台北', '新北', '桃园', '台中', '台南', '高雄'},
}

# 省、自治区名，作为验证

CITY_PROVINCE = {'宁夏', '湖北', '海南', '广西', '重庆', '甘肃', '湖南', '贵州', '河南', '云南', '山西', '福建', '安徽', '辽宁', '澳门', '西藏', '江西',
                 '黑龙江', '青海', '上海', '天津', '河北', '吉林', '山东', '内蒙古', '陕西', '北京', '四川', '新疆', '浙江', '台湾', '广东', '香港', '江苏'}

# 平级地区名，方便后续验证地区是否正常

CITY_WORDS = {'伊犁哈萨克', '永城', '锡林浩特', '眉山', '郑州', '长垣', '玉溪', '琼海', '莆田', '自贡', '邵东', '海东', '兴化', '新泰', '淄博', '吴川', '广东',
              '榆林', '周口', '高密', '涟源', '铜川', '驻马店', '广水', '梧州', '青岛', '武夷山', '湖南', '平湖', '迁安', '汨罗', '阳泉', '金华', '洮南',
              '吉林', '岑溪', '句容', '三河', '宣城', '东台', '双河', '上海', '嫩江', '娄底', '荥阳', '临夏州', '营口', '牡丹江', '舟山', '岳阳', '龙港',
              '泰兴', '二连浩特', '大石桥', '黄山', '呼和浩特', '莱西', '抚远', '北票', '枣阳', '江西', '舞钢', '高州', '常州', '连州', '汝州', '登封',
              '阿坝', '铁力', '平顶山', '南宁', '根河', '保山', '红河州', '哈尔滨', '漳平', '铁岭', '项城', '肇庆', '公主岭', '雷州', '任丘', '苏州', '泰州',
              '万宁', '南宫', '和田', '海西州', '朔州', '安阳', '东兴', '博乐', '四会', '山南', '龙海', '敦煌', '怒江州', '江门', '金昌', '临海', '汉川',
              '武穴', '南平', '株洲', '鸡西', '韶关', '甘孜州', '湘潭', '绥芬河', '商丘', '兴义', '连云港', '荆州', '侯马', '大冶', '嵊州', '果洛州', '宜昌',
              '东方', '凌源', '当阳', '丹东', '华阴', '衢州', '虎林', '韩城', '青州', '黑河', '遵化', '孟州', '呼伦贝尔', '长葛', '德阳', '仙桃', '磐石',
              '汕头', '合山', '盘州', '安康', '梅河口', '成都', '双辽', '阜新', '杭州', '可克达拉', '孝义', '临夏', '神木', '赤壁', '遂宁', '巴中', '西安',
              '张家界', '蓬莱', '伊宁', '栖霞', '承德', '绍兴', '黄南州', '丹江口', '信宜', '浏阳', '大庆', '马鞍山', '宣威', '吴忠', '潜江', '宜兴', '景洪',
              '彭州', '济宁', '平凉', '三沙', '水富', '尚志', '晋城', '鄂尔多斯', '十堰', '六盘水', '新乐', '三门峡', '蒙自', '昆明', '海阳', '建瓯', '林芝',
              '辽源', '都匀', '临湘', '华亭', '常宁', '同江', '北流', '扬中', '湖州', '个旧', '常德', '广安', '射洪', '新疆', '应城', '太原', '永州',
              '晋中', '宝鸡', '瑞金', '普宁', '牙克石', '海南', '潮州', '石狮', '辽阳', '兴城', '邳州', '灯塔', '喀左', '阿克苏', '上饶', '酒泉', '张家港',
              '洪湖', '雅安', '昌吉州', '霸州', '穆棱', '海口', '北京', '威海', '广德', '普洱', '资阳', '阳江', '云浮', '永济', '江阴', '海城', '邛崃',
              '五家渠', '乌兰浩特', '双鸭山', '大理州', '利川', '迪庆州', '乐平', '浙江', '咸宁', '东港', '乐昌', '蛟河', '石河子', '抚州', '凯里', '本溪',
              '盖州', '铜陵', '霍州', '林州', '高安', '津', '济南', '合作', '河南', '格尔木', '宿迁', '靖江', '凌海', '潜山', '调兵山', '荆门', '绵竹',
              '大连', '濮阳', '海南州', '惠州', '湘西州', '阿勒泰', '曲靖', '南安', '阿图什', '焦作', '阆中', '英德', '漳州', '平度', '瑞丽', '汕尾', '定西',
              '吐鲁番', '安宁', '贵溪', '奎屯', '陕西', '包头', '兴平', '盘锦', '那曲', '邹城', '临沧', '河间', '延边州', '石首', '昭通', '江山', '钟祥',
              '天门', '沧州', '巴音郭楞州', '白城', '瑞昌', '忻州', '丽水', '长治', '四川', '通化', '龙泉', '文山州', '恩施州', '博尔塔拉', '七台河', '安国',
              '舒兰', '黔西南', '鄂州', '茫崖', '开平', '三明', '鞍山', '额尔古纳', '老河口', '洪江', '荣成', '芒', '南京', '江苏', '界首', '扶余', '简阳',
              '弥勒', '汾阳', '阿拉尔', '柳州', '榆树', '海林', '玉门', '巢湖', '东莞', '大理', '彬州', '醴陵', '河池', '集安', '乌海', '鹤壁', '高邮',
              '庆阳', '怀仁', '湛江', '东阳', '辽宁', '昌邑', '青海', '都江堰', '昌都', '淮南', '黄冈', '珲春', '樟树', '凉山州', '宁夏', '永康', '潍坊',
              '讷河', '安丘', '龙口', '井冈山', '桦甸', '六安', '内蒙古', '滨州', '广汉', '常熟', '攀枝花', '铜仁', '日照', '永安', '肇东', '河北', '五大连池',
              '富锦', '沙河', '温州', '陇南', '恩施', '定州', '禹城', '重庆', '敦化', '乐山', '图们', '松原', '银川', '衡水', '开原', '五常', '开封',
              '耒阳', '慈溪', '阳春', '肥城', '玉树州', '德宏州', '邢台', '哈密', '楚雄', '玉林', '晋州', '巩义', '新余', '白银', '达州', '仁怀', '临江',
              '泰安', '徐州', '铁门关', '滁州', '香格里拉', '子长', '德兴', '商洛', '赤水', '崇左', '天长', '泸水', '宜春', '禹州', '乐陵', '高平', '西双版纳',
              '白山', '武冈', '凭祥', '黔东南', '百色', '防城港', '西藏', '济源', '秦皇岛', '泸州', '乌兰察布', '绥化', '资兴', '明光', '珠海', '胶州', '贵阳',
              '化州', '黑龙江', '巴彦淖尔', '抚顺', '洛阳', '大同', '玉树', '三亚', '南昌', '安达', '拉萨', '康定', '江油', '丹阳', '陆丰', '吉首', '宁国',
              '凤城', '佛山', '枝江', '中山', '南充', '广西', '高碑店', '西宁', '隆昌', '塔城', '曲阜', '山东', '甘南州', '东宁', '淮安', '黄骅', '天水',
              '诸城', '深圳', '北屯', '滦州', '兴仁', '黔南', '偃师', '新郑', '长沙', '宁波', '山西', '恩平', '通辽', '西昌', '宁安', '钦州', '沈阳',
              '万源', '朝阳', '无锡', '和龙', '原平', '襄阳', '海宁', '清远', '芜湖', '泉州', '烟台', '丽江', '四平', '漠河', '启东', '汉中', '德惠',
              '开远', '德令哈', '武安', '玉环', '扎兰屯', '东营', '灵宝', '揭阳', '福建', '毕节', '赤峰', '冷水江', '乌苏', '莱州', '鹤山', '乳山', '河源',
              '吕梁', '保定', '如皋', '合肥', '古交', '溧阳', '许昌', '涿州', '内江', '义乌', '北安', '临沂', '廊坊', '嘉兴', '葫芦岛', '宜宾', '唐山',
              '天津', '张家口', '齐齐哈尔', '腾冲', '广州', '兴宁', '池州', '来宾', '台州', '佳木斯', '喀什', '楚雄州', '庄河', '卫辉', '台山', '龙岩', '邓州',
              '昆玉', '麻城', '新民', '长春', '武威', '桂林', '九江', '松滋', '荔浦', '招远', '文山', '临汾', '海安', '乐清', '扬州', '延吉', '锦州',
              '延安', '贵州', '霍尔果斯', '儋州', '宜城', '云南', '信阳', '咸阳', '库尔勒', '北海', '日喀则', '广元', '诸暨', '宜都', '海门', '临清',
              '霍林郭勒', '安顺', '兰溪', '吉安', '辛集', '桂平', '瓦房店', '甘肃', '益阳', '石嘴山', '瑞安', '滕州', '廉江', '邹平', '乌鲁木齐', '海北州',
              '仪征', '图木舒克', '宿州', '华蓥', '阿尔山', '建德', '枣庄', '伊春', '桐城', '孝感', '昌吉', '宁德', '义马', '安庆', '梅州', '福州', '马尔康',
              '五指山', '温岭', '安陆', '贵港', '湖北', '平泉', '深州', '茂名', '福清', '文昌', '石家庄', '新密', '菏泽', '阜阳', '韶山', '中卫', '固原',
              '武汉', '泊头', '太仓', '兰州', '运城', '郴州', '新沂', '庐山', '什邡', '随州', '海伦', '南雄', '淮北', '赣州', '蚌埠', '漯河', '鹤岗',
              '灵武', '怀化', '亳州', '厦门', '邯郸', '晋江', '罗定', '沅江', '共青城', '崇州', '介休', '聊城', '寿光', '余姚', '贺州', '鹰潭', '邵武',
              '遵义', '昆山', '峨眉山', '绵阳', '沁阳', '丰城', '靖西', '福鼎', '阜康', '张掖', '安徽', '克拉玛依', '克孜勒苏', '盐城', '龙井', '德州',
              '青铜峡', '衡阳', '福安', '福泉', '南通', '满洲里', '莱阳', '大安', '渭南', '嘉峪关', '阿拉山口', '南阳', '邵阳', '河津', '黄石', '密山', '京山'}

# 远程代理获取地址
PROXY_HOST = ''
PROXY_PORT = 0
PROXY_TOKEN = ''
PROXY_COUNT = ''

# aes加密的key
AES_KEY = 'qnbyzzwmdgghmcnm'

JS = '''
        var biRadixBase = 2;
        var biRadixBits = 16;
        var bitsPerDigit = biRadixBits;
        var biRadix = 1 << 16; // = 2^16 = 65536
        var biHalfRadix = biRadix >>> 1;
        var biRadixSquared = biRadix * biRadix;
        var maxDigitVal = biRadix - 1;
        var maxInteger = 9999999999999998; 


        var maxDigits;
        var ZERO_ARRAY;
        var bigZero, bigOne;

        function setMaxDigits(value)
        {
            maxDigits = value;
            ZERO_ARRAY = new Array(maxDigits);
            for (var iza = 0; iza < ZERO_ARRAY.length; iza++) ZERO_ARRAY[iza] = 0;
            bigZero = new BigInt();
            bigOne = new BigInt();
            bigOne.digits[0] = 1;
        }

        setMaxDigits(20);
        var dpl10 = 15;
        var lr10 = biFromNumber(1000000000000000);
        function BigInt(flag)
        {
            if (typeof flag == "boolean" && flag == true) {
                this.digits = null;
            }
            else {
                this.digits = ZERO_ARRAY.slice(0);
            }
            this.isNeg = false;
        }
        function biFromDecimal(s)
        {
            var isNeg = s.charAt(0) == '-';
            var i = isNeg ? 1 : 0;
            var result;
            // Skip leading zeros.
            while (i < s.length && s.charAt(i) == '0') ++i;
            if (i == s.length) {
                result = new BigInt();
            }
            else {
                var digitCount = s.length - i;
                var fgl = digitCount % dpl10;
                if (fgl == 0) fgl = dpl10;
                result = biFromNumber(Number(s.substr(i, fgl)));
                i += fgl;
                while (i < s.length) {
                    result = biAdd(biMultiply(result, lr10),
                                   biFromNumber(Number(s.substr(i, dpl10))));
                    i += dpl10;
                }
                result.isNeg = isNeg;
            }
            return result;
        }
        function biCopy(bi)
        {
            var result = new BigInt(true);
            result.digits = bi.digits.slice(0);
            result.isNeg = bi.isNeg;
            return result;
        }
        function biFromNumber(i)
        {
            var result = new BigInt();
            result.isNeg = i < 0;
            i = Math.abs(i);
            var j = 0;
            while (i > 0) {
                result.digits[j++] = i & maxDigitVal;
                i = Math.floor(i / biRadix);
            }
            return result;
        }

        function reverseStr(s)
        {
            var result = "";
            for (var i = s.length - 1; i > -1; --i) {
                result += s.charAt(i);
            }
            return result;
        }

        var hexatrigesimalToChar = new Array(
         '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
         'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
         'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
         'u', 'v', 'w', 'x', 'y', 'z'
        );

        function biToString(x, radix)
            // 2 <= radix <= 36
        {
            var b = new BigInt();
            b.digits[0] = radix;
            var qr = biDivideModulo(x, b);
            var result = hexatrigesimalToChar[qr[1].digits[0]];
            while (biCompare(qr[0], bigZero) == 1) {
                qr = biDivideModulo(qr[0], b);
                digit = qr[1].digits[0];
                result += hexatrigesimalToChar[qr[1].digits[0]];
            }
            return (x.isNeg ? "-" : "") + reverseStr(result);
        }

        function biToDecimal(x)
        {
            var b = new BigInt();
            b.digits[0] = 10;
            var qr = biDivideModulo(x, b);
            var result = String(qr[1].digits[0]);
            while (biCompare(qr[0], bigZero) == 1) {
                qr = biDivideModulo(qr[0], b);
                result += String(qr[1].digits[0]);
            }
            return (x.isNeg ? "-" : "") + reverseStr(result);
        }

        var hexToChar = new Array('0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                                  'a', 'b', 'c', 'd', 'e', 'f');

        function digitToHex(n)
        {
            var mask = 0xf;
            var result = "";
            for (i = 0; i < 4; ++i) {
                result += hexToChar[n & mask];
                n >>>= 4;
            }
            return reverseStr(result);
        }

        function biToHex(x)
        {
            var result = "";
            var n = biHighIndex(x);
            for (var i = biHighIndex(x); i > -1; --i) {
                result += digitToHex(x.digits[i]);
            }
            return result;
        }

        function charToHex(c)
        {
            var ZERO = 48;
            var NINE = ZERO + 9;
            var littleA = 97;
            var littleZ = littleA + 25;
            var bigA = 65;
            var bigZ = 65 + 25;
            var result;

            if (c >= ZERO && c <= NINE) {
                result = c - ZERO;
            } else if (c >= bigA && c <= bigZ) {
                result = 10 + c - bigA;
            } else if (c >= littleA && c <= littleZ) {
                result = 10 + c - littleA;
            } else {
                result = 0;
            }
            return result;
        }

        function hexToDigit(s)
        {
            var result = 0;
            var sl = Math.min(s.length, 4);
            for (var i = 0; i < sl; ++i) {
                result <<= 4;
                result |= charToHex(s.charCodeAt(i))
            }
            return result;
        }

        function biFromHex(s)
        {
            var result = new BigInt();
            var sl = s.length;
            for (var i = sl, j = 0; i > 0; i -= 4, ++j) {
                result.digits[j] = hexToDigit(s.substr(Math.max(i - 4, 0), Math.min(i, 4)));
            }
            return result;
        }

        function biFromString(s, radix)
        {
            var isNeg = s.charAt(0) == '-';
            var istop = isNeg ? 1 : 0;
            var result = new BigInt();
            var place = new BigInt();
            place.digits[0] = 1; // radix^0
            for (var i = s.length - 1; i >= istop; i--) {
                var c = s.charCodeAt(i);
                var digit = charToHex(c);
                var biDigit = biMultiplyDigit(place, digit);
                result = biAdd(result, biDigit);
                place = biMultiplyDigit(place, radix);
            }
            result.isNeg = isNeg;
            return result;
        }

        function biDump(b)
        {
            return (b.isNeg ? "-" : "") + b.digits.join(" ");
        }

        function biAdd(x, y)
        {
            var result;

            if (x.isNeg != y.isNeg) {
                y.isNeg = !y.isNeg;
                result = biSubtract(x, y);
                y.isNeg = !y.isNeg;
            }
            else {
                result = new BigInt();
                var c = 0;
                var n;
                for (var i = 0; i < x.digits.length; ++i) {
                    n = x.digits[i] + y.digits[i] + c;
                    result.digits[i] = n % biRadix;
                    c = Number(n >= biRadix);
                }
                result.isNeg = x.isNeg;
            }
            return result;
        }

        function biSubtract(x, y)
        {
            var result;
            if (x.isNeg != y.isNeg) {
                y.isNeg = !y.isNeg;
                result = biAdd(x, y);
                y.isNeg = !y.isNeg;
            } else {
                result = new BigInt();
                var n, c;
                c = 0;
                for (var i = 0; i < x.digits.length; ++i) {
                    n = x.digits[i] - y.digits[i] + c;
                    result.digits[i] = n % biRadix;
                    // Stupid non-conforming modulus operation.
                    if (result.digits[i] < 0) result.digits[i] += biRadix;
                    c = 0 - Number(n < 0);
                }
                // Fix up the negative sign, if any.
                if (c == -1) {
                    c = 0;
                    for (var i = 0; i < x.digits.length; ++i) {
                        n = 0 - result.digits[i] + c;
                        result.digits[i] = n % biRadix;
                        // Stupid non-conforming modulus operation.
                        if (result.digits[i] < 0) result.digits[i] += biRadix;
                        c = 0 - Number(n < 0);
                    }
                    // Result is opposite sign of arguments.
                    result.isNeg = !x.isNeg;
                } else {
                    // Result is same sign.
                    result.isNeg = x.isNeg;
                }
            }
            return result;
        }

        function biHighIndex(x)
        {
            var result = x.digits.length - 1;
            while (result > 0 && x.digits[result] == 0) --result;
            return result;
        }

        function biNumBits(x)
        {
            var n = biHighIndex(x);
            var d = x.digits[n];
            var m = (n + 1) * bitsPerDigit;
            var result;
            for (result = m; result > m - bitsPerDigit; --result) {
                if ((d & 0x8000) != 0) break;
                d <<= 1;
            }
            return result;
        }

        function biMultiply(x, y)
        {
            var result = new BigInt();
            var c;
            var n = biHighIndex(x);
            var t = biHighIndex(y);
            var u, uv, k;

            for (var i = 0; i <= t; ++i) {
                c = 0;
                k = i;
                for (j = 0; j <= n; ++j, ++k) {
                    uv = result.digits[k] + x.digits[j] * y.digits[i] + c;
                    result.digits[k] = uv & maxDigitVal;
                    c = uv >>> biRadixBits;
                    //c = Math.floor(uv / biRadix);
                }
                result.digits[i + n + 1] = c;
            }
            // Someone give me a logical xor, please.
            result.isNeg = x.isNeg != y.isNeg;
            return result;
        }

        function biMultiplyDigit(x, y)
        {
            var n, c, uv;

            result = new BigInt();
            n = biHighIndex(x);
            c = 0;
            for (var j = 0; j <= n; ++j) {
                uv = result.digits[j] + x.digits[j] * y + c;
                result.digits[j] = uv & maxDigitVal;
                c = uv >>> biRadixBits;
                //c = Math.floor(uv / biRadix);
            }
            result.digits[1 + n] = c;
            return result;
        }

        function arrayCopy(src, srcStart, dest, destStart, n)
        {
            var m = Math.min(srcStart + n, src.length);
            for (var i = srcStart, j = destStart; i < m; ++i, ++j) {
                dest[j] = src[i];
            }
        }

        var highBitMasks = new Array(0x0000, 0x8000, 0xC000, 0xE000, 0xF000, 0xF800,
                                     0xFC00, 0xFE00, 0xFF00, 0xFF80, 0xFFC0, 0xFFE0,
                                     0xFFF0, 0xFFF8, 0xFFFC, 0xFFFE, 0xFFFF);

        function biShiftLeft(x, n)
        {
            var digitCount = Math.floor(n / bitsPerDigit);
            var result = new BigInt();
            arrayCopy(x.digits, 0, result.digits, digitCount,
                      result.digits.length - digitCount);
            var bits = n % bitsPerDigit;
            var rightBits = bitsPerDigit - bits;
            for (var i = result.digits.length - 1, i1 = i - 1; i > 0; --i, --i1) {
                result.digits[i] = ((result.digits[i] << bits) & maxDigitVal) |
                                   ((result.digits[i1] & highBitMasks[bits]) >>>
                                    (rightBits));
            }
            result.digits[0] = ((result.digits[i] << bits) & maxDigitVal);
            result.isNeg = x.isNeg;
            return result;
        }

        var lowBitMasks = new Array(0x0000, 0x0001, 0x0003, 0x0007, 0x000F, 0x001F,
                                    0x003F, 0x007F, 0x00FF, 0x01FF, 0x03FF, 0x07FF,
                                    0x0FFF, 0x1FFF, 0x3FFF, 0x7FFF, 0xFFFF);

        function biShiftRight(x, n)
        {
            var digitCount = Math.floor(n / bitsPerDigit);
            var result = new BigInt();
            arrayCopy(x.digits, digitCount, result.digits, 0,
                      x.digits.length - digitCount);
            var bits = n % bitsPerDigit;
            var leftBits = bitsPerDigit - bits;
            for (var i = 0, i1 = i + 1; i < result.digits.length - 1; ++i, ++i1) {
                result.digits[i] = (result.digits[i] >>> bits) |
                                   ((result.digits[i1] & lowBitMasks[bits]) << leftBits);
            }
            result.digits[result.digits.length - 1] >>>= bits;
            result.isNeg = x.isNeg;
            return result;
        }

        function biMultiplyByRadixPower(x, n)
        {
            var result = new BigInt();
            arrayCopy(x.digits, 0, result.digits, n, result.digits.length - n);
            return result;
        }

        function biDivideByRadixPower(x, n)
        {
            var result = new BigInt();
            arrayCopy(x.digits, n, result.digits, 0, result.digits.length - n);
            return result;
        }

        function biModuloByRadixPower(x, n)
        {
            var result = new BigInt();
            arrayCopy(x.digits, 0, result.digits, 0, n);
            return result;
        }

        function biCompare(x, y)
        {
            if (x.isNeg != y.isNeg) {
                return 1 - 2 * Number(x.isNeg);
            }
            for (var i = x.digits.length - 1; i >= 0; --i) {
                if (x.digits[i] != y.digits[i]) {
                    if (x.isNeg) {
                        return 1 - 2 * Number(x.digits[i] > y.digits[i]);
                    } else {
                        return 1 - 2 * Number(x.digits[i] < y.digits[i]);
                    }
                }
            }
            return 0;
        }

        function biDivideModulo(x, y)
        {
            var nb = biNumBits(x);
            var tb = biNumBits(y);
            var origYIsNeg = y.isNeg;
            var q, r;
            if (nb < tb) {
                // |x| < |y|
                if (x.isNeg) {
                    q = biCopy(bigOne);
                    q.isNeg = !y.isNeg;
                    x.isNeg = false;
                    y.isNeg = false;
                    r = biSubtract(y, x);
                    // Restore signs, 'cause they're references.
                    x.isNeg = true;
                    y.isNeg = origYIsNeg;
                } else {
                    q = new BigInt();
                    r = biCopy(x);
                }
                return new Array(q, r);
            }

            q = new BigInt();
            r = x;

            // Normalize Y.
            var t = Math.ceil(tb / bitsPerDigit) - 1;
            var lambda = 0;
            while (y.digits[t] < biHalfRadix) {
                y = biShiftLeft(y, 1);
                ++lambda;
                ++tb;
                t = Math.ceil(tb / bitsPerDigit) - 1;
            }
            r = biShiftLeft(r, lambda);
            nb += lambda; // Update the bit count for x.
            var n = Math.ceil(nb / bitsPerDigit) - 1;

            var b = biMultiplyByRadixPower(y, n - t);
            while (biCompare(r, b) != -1) {
                ++q.digits[n - t];
                r = biSubtract(r, b);
            }
            for (var i = n; i > t; --i) {
            var ri = (i >= r.digits.length) ? 0 : r.digits[i];
            var ri1 = (i - 1 >= r.digits.length) ? 0 : r.digits[i - 1];
            var ri2 = (i - 2 >= r.digits.length) ? 0 : r.digits[i - 2];
            var yt = (t >= y.digits.length) ? 0 : y.digits[t];
            var yt1 = (t - 1 >= y.digits.length) ? 0 : y.digits[t - 1];
                if (ri == yt) {
                    q.digits[i - t - 1] = maxDigitVal;
                } else {
                    q.digits[i - t - 1] = Math.floor((ri * biRadix + ri1) / yt);
                }

                var c1 = q.digits[i - t - 1] * ((yt * biRadix) + yt1);
                var c2 = (ri * biRadixSquared) + ((ri1 * biRadix) + ri2);
                while (c1 > c2) {
                    --q.digits[i - t - 1];
                    c1 = q.digits[i - t - 1] * ((yt * biRadix) | yt1);
                    c2 = (ri * biRadix * biRadix) + ((ri1 * biRadix) + ri2);
                }

                b = biMultiplyByRadixPower(y, i - t - 1);
                r = biSubtract(r, biMultiplyDigit(b, q.digits[i - t - 1]));
                if (r.isNeg) {
                    r = biAdd(r, b);
                    --q.digits[i - t - 1];
                }
            }
            r = biShiftRight(r, lambda);
            // Fiddle with the signs and stuff to make sure that 0 <= r < y.
            q.isNeg = x.isNeg != origYIsNeg;
            if (x.isNeg) {
                if (origYIsNeg) {
                    q = biAdd(q, bigOne);
                } else {
                    q = biSubtract(q, bigOne);
                }
                y = biShiftRight(y, lambda);
                r = biSubtract(y, r);
            }
            // Check for the unbelievably stupid degenerate case of r == -0.
            if (r.digits[0] == 0 && biHighIndex(r) == 0) r.isNeg = false;

            return new Array(q, r);
        }

        function biDivide(x, y)
        {
            return biDivideModulo(x, y)[0];
        }

        function biModulo(x, y)
        {
            return biDivideModulo(x, y)[1];
        }

        function biMultiplyMod(x, y, m)
        {
            return biModulo(biMultiply(x, y), m);
        }

        function biPow(x, y)
        {
            var result = bigOne;
            var a = x;
            while (true) {
                if ((y & 1) != 0) result = biMultiply(result, a);
                y >>= 1;
                if (y == 0) break;
                a = biMultiply(a, a);
            }
            return result;
        }

        function biPowMod(x, y, m)
        {
            var result = bigOne;
            var a = x;
            var k = y;
            while (true) {
                if ((k.digits[0] & 1) != 0) result = biMultiplyMod(result, a, m);
                k = biShiftRight(k, 1);
                if (k.digits[0] == 0 && biHighIndex(k) == 0) break;
                a = biMultiplyMod(a, a, m);
            }
            return result;
        }
        function RSAKeyPair(encryptionExponent, decryptionExponent, modulus)
        {
            this.e = biFromHex(encryptionExponent);
            this.d = biFromHex(decryptionExponent);
            this.m = biFromHex(modulus);			
            this.digitSize = 2 * biHighIndex(this.m) + 2;
            this.chunkSize = this.digitSize - 11; 
            this.radix = 16;
            this.barrett = new BarrettMu(this.m);
        }
        function twoDigit(n)
        {
            return (n < 10 ? "0" : "") + String(n);
        }
        function encryptedString(key, s)
        {
            if (key.chunkSize > key.digitSize - 11)
            {
                return "Error";
            }
            var a = new Array();
            var sl = s.length;
            var i = 0;
            while (i < sl) {
                a[i] = s.charCodeAt(i);
                i++;
            }
            var al = a.length;
            var result = "";
            var j, k, block;
            for (i = 0; i < al; i += key.chunkSize) {
                block = new BigInt();
                j = 0;

                var x;
                var msgLength = (i+key.chunkSize)>al ? al%key.chunkSize : key.chunkSize;
                var b = new Array();
                for (x=0; x<msgLength; x++)
                {
                    b[x] = a[i+msgLength-1-x];
                }
                b[msgLength] = 0; // marker
                var paddedSize = Math.max(8, key.digitSize - 3 - msgLength);

                for (x=0; x<paddedSize; x++) {
                    b[msgLength+1+x] = Math.floor(Math.random()*254) + 1; // [1,255]
                }
                // It can be asserted that msgLength+paddedSize == key.digitSize-3
                b[key.digitSize-2] = 2; // marker
                b[key.digitSize-1] = 0; // marker

                for (k = 0; k < key.digitSize; ++j) 
                {
                    block.digits[j] = b[k++];
                    block.digits[j] += b[k++] << 8;
                }
                var crypt = key.barrett.powMod(block, key.e);
                var text = key.radix == 16 ? biToHex(crypt) : biToString(crypt, key.radix);
                result += text + " ";
            }
            return result.substring(0, result.length - 1); // Remove last space.
        }
        function decryptedString(key, s)
        {
            var blocks = s.split(" ");
            var result = "";
            var i, j, block;
            for (i = 0; i < blocks.length; ++i) {
                var bi;
                if (key.radix == 16) {
                    bi = biFromHex(blocks[i]);
                }
                else {
                    bi = biFromString(blocks[i], key.radix);
                }
                block = key.barrett.powMod(bi, key.d);
                for (j = 0; j <= biHighIndex(block); ++j) {
                    result += String.fromCharCode(block.digits[j] & 255,
                                                  block.digits[j] >> 8);
                }
            }
            // Remove trailing null, if any.
            if (result.charCodeAt(result.length - 1) == 0) {
                result = result.substring(0, result.length - 1);
            }
            return result;
        }
        function BarrettMu(m)
        {
            this.modulus = biCopy(m);
            this.k = biHighIndex(this.modulus) + 1;
            var b2k = new BigInt();
            b2k.digits[2 * this.k] = 1; // b2k = b^(2k)
            this.mu = biDivide(b2k, this.modulus);
            this.bkplus1 = new BigInt();
            this.bkplus1.digits[this.k + 1] = 1; // bkplus1 = b^(k+1)
            this.modulo = BarrettMu_modulo;
            this.multiplyMod = BarrettMu_multiplyMod;
            this.powMod = BarrettMu_powMod;
        }
        function BarrettMu_modulo(x)
        {
            var q1 = biDivideByRadixPower(x, this.k - 1);
            var q2 = biMultiply(q1, this.mu);
            var q3 = biDivideByRadixPower(q2, this.k + 1);
            var r1 = biModuloByRadixPower(x, this.k + 1);
            var r2term = biMultiply(q3, this.modulus);
            var r2 = biModuloByRadixPower(r2term, this.k + 1);
            var r = biSubtract(r1, r2);
            if (r.isNeg) {
                r = biAdd(r, this.bkplus1);
            }
            var rgtem = biCompare(r, this.modulus) >= 0;
            while (rgtem) {
                r = biSubtract(r, this.modulus);
                rgtem = biCompare(r, this.modulus) >= 0;
            }
            return r;
        }
        function BarrettMu_multiplyMod(x, y)
        {
            var xy = biMultiply(x, y);
            return this.modulo(xy);
        }
        function BarrettMu_powMod(x, y)
        {
            var result = new BigInt();
            result.digits[0] = 1;
            var a = x;
            var k = y;
            while (true) {
                if ((k.digits[0] & 1) != 0) result = this.multiplyMod(result, a);
                k = biShiftRight(k, 1);
                if (k.digits[0] == 0 && biHighIndex(k) == 0) break;
                a = this.multiplyMod(a, a);
            }
            return result;
        }
    '''

# OCR引擎位置
OCR_PATH = 'C://Program Files//Tesseract-OCR//tesseract.exe'
