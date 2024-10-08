import requests
import re
import base64
import logging
import time

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Fofa API 配置
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

urls = ["Hunan"]
channelsx = [
    "湖南卫视,http://8.8.8.8:8/udp/239.76.245.115:1234", "湖南经视,http://8.8.8.8:8/udp/239.76.245.116:1234",
    "湖南都市,http://8.8.8.8:8/udp/239.76.245.117:1234", "湖南电视剧,http://8.8.8.8:8/udp/239.76.245.118:1234",
    "湖南电影,http://8.8.8.8:8/udp/239.76.245.119:1234", "湖南娱乐,http://8.8.8.8:8/udp/239.76.245.121:1234",
    "湖南国际,http://8.8.8.8:8/udp/239.76.245.124:1234", "湖南公共,http://8.8.8.8:8/udp/239.76.245.123:1234",
    "CCTV1,http://8.8.8.8:8/udp/239.76.245.51:1234", "CCTV1,http://8.8.8.8:8/udp/239.76.246.151:1234",
    "CCTV2,http://8.8.8.8:8/udp/239.76.246.152:1234", "CCTV3,http://8.8.8.8:8/udp/239.76.246.153:1234",
    "CCTV4,http://8.8.8.8:8/udp/239.76.245.195:1234", "CCTV4,http://8.8.8.8:8/udp/239.76.246.154:1234",
    "CCTV5,http://8.8.8.8:8/udp/239.76.246.155:1234", "CCTV5+,http://8.8.8.8:8/udp/239.76.246.168:1234",
    "CCTV6,http://8.8.8.8:8/udp/239.76.246.156:1234", "CCTV7,http://8.8.8.8:8/udp/239.76.246.157:1234",
    "CCTV8,http://8.8.8.8:8/udp/239.76.246.158:1234", "CCTV9,http://8.8.8.8:8/udp/239.76.246.159:1234",
    "CCTV10,http://8.8.8.8:8/udp/239.76.246.160:1234", "CCTV11,http://8.8.8.8:8/udp/239.76.245.251:1234",
    "CCTV12,http://8.8.8.8:8/udp/239.76.246.162:1234", "CCTV13,http://8.8.8.8:8/udp/239.76.246.93:1234",
    "CCTV14,http://8.8.8.8:8/udp/239.76.246.164:1234", "CCTV15,http://8.8.8.8:8/udp/239.76.245.252:1234",
    "CCTV16,http://8.8.8.8:8/udp/239.76.246.98:1234", "CCTV17,http://8.8.8.8:8/udp/239.76.245.238:1234",
    "CCTV16 4K,http://8.8.8.8:8/udp/239.76.246.214:1234", "CCTV16 4k,http://8.8.8.8:8/udp/239.76.246.224:1234",
    "CCTV16 4k,http://8.8.8.8:8/udp/239.76.246.230:1234", "体育,http://8.8.8.8:8/udp/239.76.246.136:1234",
    "金鹰卡通,http://8.8.8.8:8/udp/239.76.245.120:1234", "金鹰纪实,http://8.8.8.8:8/udp/239.76.245.122:1234",
    "快乐垂钓,http://8.8.8.8:8/udp/239.76.245.127:1234", "湖南教育,http://8.8.8.8:8/udp/239.76.245.233:1234",
    "茶频道,http://8.8.8.8:8/udp/239.76.245.239:1234", "广东卫视,http://8.8.8.8:8/udp/239.76.245.189:1234",
    "东南卫视,http://8.8.8.8:8/udp/239.76.245.190:1234", "安徽卫视,http://8.8.8.8:8/udp/239.76.245.196:1234",
    "辽宁卫视,http://8.8.8.8:8/udp/239.76.245.197:1234", "江西卫视,http://8.8.8.8:8/udp/239.76.245.225:1234",
    "河北卫视,http://8.8.8.8:8/udp/239.76.245.199:1234", "贵州卫视,http://8.8.8.8:8/udp/239.76.245.198:1234",
    "江苏卫视,http://8.8.8.8:8/udp/239.76.246.181:1234", "东方卫视,http://8.8.8.8:8/udp/239.76.246.186:1234",
    "浙江卫视,http://8.8.8.8:8/udp/239.76.246.182:1234", "北京卫视,http://8.8.8.8:8/udp/239.76.246.184:1234",
    "天津卫视,http://8.8.8.8:8/udp/239.76.246.185:1234", "深圳卫视,http://8.8.8.8:8/udp/239.76.246.188:1234",
    "湖北卫视,http://8.8.8.8:8/udp/239.76.246.193:1234", "山东卫视,http://8.8.8.8:8/udp/239.76.246.195:1234",
    "黑龙江卫视,http://8.8.8.8:8/udp/239.76.246.200:1234", "吉林卫视,http://8.8.8.8:8/udp/239.76.246.201:1234",
    "河南卫视,http://8.8.8.8:8/udp/239.76.246.202:1234", "海南卫视,http://8.8.8.8:8/udp/239.76.246.203:1234",
    "四川卫视,http://8.8.8.8:8/udp/239.76.246.91:1234", "重庆卫视,http://8.8.8.8:8/udp/239.76.246.92:1234",
    "甘肃卫视,http://8.8.8.8:8/udp/239.76.246.94:1234", "中国教育,http://8.8.8.8:8/udp/239.76.245.192:1234",
    "长沙女姓,http://8.8.8.8:8/udp/239.76.245.23:1234", "长沙影视,http://8.8.8.8:8/udp/239.76.245.204:1234",
    "湘西综合,http://8.8.8.8:8/udp/239.76.245.208:1234", "湘西综合,http://8.8.8.8:8/udp/239.76.245.209:1234",
    "河南梨园,http://8.8.8.8:8/udp/239.76.245.179:1234", "武术世界,http://8.8.8.8:8/udp/239.76.245.181:1234",
    "张家界,http://8.8.8.8:8/udp/239.76.245.235:1234", "张家界综合,http://8.8.8.8:8/udp/239.76.245.234:1234",
    "CHC动作电影,http://8.8.8.8:8/udp/239.76.245.243:1234", "CHC高清电影,http://8.8.8.8:8/udp/239.76.245.242:1234",
    "CHC家庭影院,http://8.8.8.8:8/udp/239.76.245.241:1234", "快乐垂钓,http://8.8.8.8:8/udp/239.76.246.5:1234",
    "凤凰资讯,http://8.8.8.8:8/udp/239.76.246.8:1234", "凤凰中文,http://8.8.8.8:8/udp/239.76.246.7:1234",
    "湖南卫视,http://8.8.8.8:8/udp/239.76.246.101:1234", "湖南卫视,http://8.8.8.8:8/udp/239.76.246.100:1234",
    "湖南经视,http://8.8.8.8:8/udp/239.76.246.103:1234", "湖南国际,http://8.8.8.8:8/udp/239.76.246.102:1234",
    "湖南都市,http://8.8.8.8:8/udp/239.76.246.104:1234", "湖南娱乐,http://8.8.8.8:8/udp/239.76.246.105:1234",
    "湖南电影,http://8.8.8.8:8/udp/239.76.246.106:1234", "湖南公共,http://8.8.8.8:8/udp/239.76.246.109:1234",
    "湖南电视剧,http://8.8.8.8:8/udp/239.76.246.108:1234", "金鹰卡通,http://8.8.8.8:8/udp/239.76.246.107:1234",
    "金鹰纪实,http://8.8.8.8:8/udp/239.76.246.110:1234", "长沙政法,http://8.8.8.8:8/udp/239.76.246.122:1234",
    "长沙新闻,http://8.8.8.8:8/udp/239.76.246.121:1234", "健康电视,http://8.8.8.8:8/udp/239.76.246.127:1234",
    "欢笑剧场4K,http://8.8.8.8:8/udp/239.76.246.130:1234", "都市剧场,http://8.8.8.8:8/udp/239.76.246.215:1234",
    "极速汽车,http://8.8.8.8:8/udp/239.76.246.133:1234", "动漫秀场,http://8.8.8.8:8/udp/239.76.246.131:1234",
    "游戏风云,http://8.8.8.8:8/udp/239.76.246.132:1234", "凤凰中文,http://8.8.8.8:8/udp/239.76.246.134:1234",
    "凤凰中文,http://8.8.8.8:8/udp/239.76.253.135:9000", "凤凰资讯,http://8.8.8.8:8/udp/239.76.253.134:9000",
    "凤凰资讯,http://8.8.8.8:8/udp/239.76.246.135:1234", "体育,http://8.8.8.8:8/udp/239.76.253.136:9000",
    "全纪实,http://8.8.8.8:8/udp/239.76.246.137:1234", "法治天地,http://8.8.8.8:8/udp/239.76.246.138:1234",
    "生活时尚,http://8.8.8.8:8/udp/239.76.246.223:1234", "浏阳,http://8.8.8.8:8/udp/239.76.248.6:1234",
    "常德综合,http://8.8.8.8:8/udp/239.76.248.10:1234", "常德公共,http://8.8.8.8:8/udp/239.76.248.11:1234",
    "衡阳综合,http://8.8.8.8:8/udp/239.76.248.13:1234", "衡阳公共,http://8.8.8.8:8/udp/239.76.248.14:1234",
    "娄底综合,http://8.8.8.8:8/udp/239.76.248.18:1234", "娄底公共,http://8.8.8.8:8/udp/239.76.248.19:1234",
    "张家界综合,http://8.8.8.8:8/udp/239.76.252.234:9000", "张家界,http://8.8.8.8:8/udp/239.76.252.235:9000",
    "邵阳新闻,http://8.8.8.8:8/udp/239.76.248.23:1234", "永州新闻,http://8.8.8.8:8/udp/239.76.248.57:1234",
    "怀化综合,http://8.8.8.8:8/udp/239.76.255.12:9000", "金色夕阳,http://8.8.8.8:8/udp/239.76.254.43:9000",
    "CCTV第一剧场,http://8.8.8.8:8/udp/239.76.254.49:9000", "CCTV风云足球,http://8.8.8.8:8/udp/239.76.254.52:9000",
    "CCTV风云音乐,http://8.8.8.8:8/udp/239.76.254.51:9000", "CCTV风云剧场,http://8.8.8.8:8/udp/239.76.254.50:9000",
    "CCTV女姓时尚,http://8.8.8.8:8/udp/239.76.254.55:9000", "CCTV央视文化精品,http://8.8.8.8:8/udp/239.76.254.56:9000",
    "CCTV世界地理,http://8.8.8.8:8/udp/239.76.254.57:9000", "CCTV兵器科技,http://8.8.8.8:8/udp/239.76.254.59:9000",
    "CCTV央视台球,http://8.8.8.8:8/udp/239.76.254.58:9000", "CCTV怀旧剧场,http://8.8.8.8:8/udp/239.76.254.53:9000",
    "CCTV电视指南,http://8.8.8.8:8/udp/239.76.254.61:9000", "CCTV央视高尔夫,http://8.8.8.8:8/udp/239.76.254.62:9000",
    "北京少儿,http://8.8.8.8:8/udp/239.76.254.81:9000", "快乐垂钓,http://8.8.8.8:8/udp/239.76.253.5:9000",
    "湖南卫视,http://8.8.8.8:8/udp/239.76.253.101:9000", "湖南国际,http://8.8.8.8:8/udp/239.76.253.102:9000",
    "湖南卫视,http://8.8.8.8:8/udp/239.76.253.100:9000", "湖南经视,http://8.8.8.8:8/udp/239.76.253.103:9000",
    "湖南都市,http://8.8.8.8:8/udp/239.76.253.104:9000", "湖南娱乐,http://8.8.8.8:8/udp/239.76.253.105:9000",
    "湖南电影,http://8.8.8.8:8/udp/239.76.253.106:9000", "湖南电视剧,http://8.8.8.8:8/udp/239.76.253.108:9000",
    "金鹰卡通,http://8.8.8.8:8/udp/239.76.253.107:9000", "湖南公共,http://8.8.8.8:8/udp/239.76.253.109:9000",
    "金鹰纪实,http://8.8.8.8:8/udp/239.76.253.110:9000", "长沙新闻,http://8.8.8.8:8/udp/239.76.253.121:9000",
    "长沙政法,http://8.8.8.8:8/udp/239.76.253.122:9000", "欢笑剧场4K,http://8.8.8.8:8/udp/239.76.253.130:9000",
    "极速汽车,http://8.8.8.8:8/udp/239.76.253.133:9000", "动漫秀场,http://8.8.8.8:8/udp/239.76.253.131:9000",
    "凤凰中文,http://8.8.8.8:8/udp/239.76.253.135:9000", "凤凰资讯,http://8.8.8.8:8/udp/239.76.253.134:9000",
    "体育,http://8.8.8.8:8/udp/239.76.253.136:9000", "全纪实,http://8.8.8.8:8/udp/239.76.253.137:9000",
    "金色学堂,http://8.8.8.8:8/udp/239.76.253.139:9000", "法治天地,http://8.8.8.8:8/udp/239.76.253.138:9000",
    "CCTV1,http://8.8.8.8:8/udp/239.76.253.151:9000", "CCTV2,http://8.8.8.8:8/udp/239.76.253.152:9000",
    "CCTV3,http://8.8.8.8:8/udp/239.76.253.153:9000", "CCTV4,http://8.8.8.8:8/udp/239.76.253.154:9000",
    "CCTV5,http://8.8.8.8:8/udp/239.76.253.155:9000", "CCTV5+,http://8.8.8.8:8/udp/239.76.253.168:9000",
    "CCTV6,http://8.8.8.8:8/udp/239.76.253.156:9000", "CCTV7,http://8.8.8.8:8/udp/239.76.253.157:9000",
    "CCTV8,http://8.8.8.8:8/udp/239.76.253.158:9000", "CCTV9,http://8.8.8.8:8/udp/239.76.253.159:9000",
    "CCTV10,http://8.8.8.8:8/udp/239.76.253.160:9000", "CCTV12,http://8.8.8.8:8/udp/239.76.253.162:9000",
    "CCTV13,http://8.8.8.8:8/udp/239.76.253.93:9000", "CCTV14,http://8.8.8.8:8/udp/239.76.253.164:9000",
    "CCTV16,http://8.8.8.8:8/udp/239.76.253.98:9000", "CCTV16 4K,http://8.8.8.8:8/udp/239.76.253.214:9000",
    "CCTV16 4K,http://8.8.8.8:8/udp/239.76.254.200:9000", "CCTV16 4K,http://8.8.8.8:8/udp/239.76.253.224:9000",
    "CCTV16 4K,http://8.8.8.8:8/udp/239.76.253.230:9000", "江苏卫视,http://8.8.8.8:8/udp/239.76.253.181:9000",
    "浙江卫视,http://8.8.8.8:8/udp/239.76.253.182:9000", "北京卫视,http://8.8.8.8:8/udp/239.76.253.184:9000",
    "天津卫视,http://8.8.8.8:8/udp/239.76.253.185:9000", "东方卫视,http://8.8.8.8:8/udp/239.76.253.186:9000",
    "深圳卫视,http://8.8.8.8:8/udp/239.76.253.188:9000", "湖北卫视,http://8.8.8.8:8/udp/239.76.253.193:9000",
    "山东卫视,http://8.8.8.8:8/udp/239.76.253.195:9000", "黑龙江卫视,http://8.8.8.8:8/udp/239.76.253.200:9000",
    "吉林卫视,http://8.8.8.8:8/udp/239.76.253.201:9000", "河南卫视,http://8.8.8.8:8/udp/239.76.253.202:9000",
    "海南卫视,http://8.8.8.8:8/udp/239.76.253.203:9000", "四川卫视,http://8.8.8.8:8/udp/239.76.253.91:9000",
    "重庆卫视,http://8.8.8.8:8/udp/239.76.253.92:9000", "广西卫视,http://8.8.8.8:8/udp/239.76.254.54:9000",
    "陕西卫视,http://8.8.8.8:8/udp/239.76.254.76:9000", "云南卫视,http://8.8.8.8:8/udp/239.76.254.60:9000",
    "青海卫视,http://8.8.8.8:8/udp/239.76.254.132:9000", "甘肃卫视,http://8.8.8.8:8/udp/239.76.253.94:9000",
    "都市剧场,http://8.8.8.8:8/udp/239.76.253.215:9000", "生活时尚,http://8.8.8.8:8/udp/239.76.253.223:9000",
    "长沙女姓,http://8.8.8.8:8/udp/239.76.252.23:9000", "湖南卫视,http://8.8.8.8:8/udp/239.76.252.115:9000",
    "湖南经视,http://8.8.8.8:8/udp/239.76.252.116:9000", "湖南电视剧,http://8.8.8.8:8/udp/239.76.252.118:9000",
    "湖南电影,http://8.8.8.8:8/udp/239.76.252.119:9000", "金鹰卡通,http://8.8.8.8:8/udp/239.76.252.120:9000",
    "湖南公共,http://8.8.8.8:8/udp/239.76.252.123:9000", "湖南娱乐,http://8.8.8.8:8/udp/239.76.252.121:9000",
    "金鹰纪实,http://8.8.8.8:8/udp/239.76.252.122:9000", "湖南国际,http://8.8.8.8:8/udp/239.76.252.124:9000",
    "湖南都市,http://8.8.8.8:8/udp/239.76.252.117:9000", "快乐垂钓,http://8.8.8.8:8/udp/239.76.252.127:9000",
    "河南梨园,http://8.8.8.8:8/udp/239.76.252.179:9000", "文物宝库,http://8.8.8.8:8/udp/239.76.252.180:9000",
    "武术世界,http://8.8.8.8:8/udp/239.76.252.181:9000", "广东卫视,http://8.8.8.8:8/udp/239.76.252.189:9000",
    "东南卫视,http://8.8.8.8:8/udp/239.76.252.190:9000", "中国教育,http://8.8.8.8:8/udp/239.76.252.192:9000",
    "安徽卫视,http://8.8.8.8:8/udp/239.76.252.196:9000", "辽宁卫视,http://8.8.8.8:8/udp/239.76.252.197:9000",
    "河北卫视,http://8.8.8.8:8/udp/239.76.252.199:9000", "贵州卫视,http://8.8.8.8:8/udp/239.76.252.198:9000",
    "长沙影视,http://8.8.8.8:8/udp/239.76.252.204:9000", "湘西综合,http://8.8.8.8:8/udp/239.76.252.208:9000",
    "湘西公共,http://8.8.8.8:8/udp/239.76.252.209:9000", "湘西公共,http://8.8.8.8:8/udp/239.76.252.210:9000",
    "湖南教育,http://8.8.8.8:8/udp/239.76.252.233:9000","浏阳新闻,http://8.8.8.8:8/udp/239.76.255.6:9000",
    "湘西公共,http://8.8.8.8:8/udp/239.76.252.209:9000", "湘西公共,http://8.8.8.8:8/udp/239.76.252.210:9000",
    "湘西综合,http://8.8.8.8:8/udp/239.76.252.208:9000", "湘西综合,http://8.8.8.8:8/udp/239.76.245.208:1234",
    "衡阳公共,http://8.8.8.8:8/udp/239.76.255.14:9000", "衡阳综合,http://8.8.8.8:8/udp/239.76.255.13:9000",
    "衡阳县电视台,http://8.8.8.8:8/udp/239.76.255.26:9000", "邵阳公共,http://8.8.8.8:8/udp/239.76.255.22:9000",
    "邵阳综合,http://8.8.8.8:8/udp/239.76.255.21:9000", "娄底教育,http://8.8.8.8:8/udp/239.76.255.20:9000",
    "娄底综合,http://8.8.8.8:8/udp/239.76.255.18:9000", "娄底公共,http://8.8.8.8:8/udp/239.76.255.19:9000",
    "郴州综合,http://8.8.8.8:8/udp/239.76.253.75:9000", "张家界综合,http://8.8.8.8:8/udp/239.76.252.234:9000",
    "张家界公共,http://8.8.8.8:8/udp/239.76.252.235:9000", "怀化综合,http://8.8.8.8:8/udp/239.76.255.12:9000",
    "常德综合,http://8.8.8.8:8/udp/239.76.255.10:9000", "常德公共,http://8.8.8.8:8/udp/239.76.255.11:9000",
    "永州综合,http://8.8.8.8:8/udp/239.76.255.23:9000", "溆浦综合,http://8.8.8.8:8/udp/239.76.255.25:9000",
    "武冈综合,http://8.8.8.8:8/udp/239.76.255.29:9000", "新化,http://8.8.8.8:8/udp/239.76.255.31:9000",
    "津市,http://8.8.8.8:8/udp/239.76.255.30:9000", "桂东融媒,http://8.8.8.8:8/udp/239.76.253.231:9000",
    "道县综合,http://8.8.8.8:8/udp/239.76.255.28:9000", "永州公共,http://8.8.8.8:8/udp/239.76.255.24:9000",
    "株洲公共,http://8.8.8.8:8/udp/239.76.252.236:9000", "株洲综合,http://8.8.8.8:8/udp/239.76.255.1:9000",
    "湘潭公共,http://8.8.8.8:8/udp/239.76.255.5:9000", "湘潭综合,http://8.8.8.8:8/udp/239.76.255.4:9000",
    "益阳公共,http://8.8.8.8:8/udp/239.76.255.16:9000", "益阳综合,http://8.8.8.8:8/udp/239.76.255.15:9000",
    "岳阳综合,http://8.8.8.8:8/udp/239.76.255.7:9000", "岳阳科教,http://8.8.8.8:8/udp/239.76.255.9:9000",
    "岳阳公共,http://8.8.8.8:8/udp/239.76.255.8:9000",
]

def query_fofa(region):
    results = []
    urls_all = []

    for url in urls:
        url_0 = str(base64.b64encode((f'"Rozhuk" && region="{url}" && org="Chinanet"').encode("utf-8")), "utf-8")
        url_64 = f'https://fofa.info/result?qbase64={url_0}'
        logging.info(f"查询网址: {url_64}")

        try:
            response = requests.get(url_64, headers=headers, timeout=15)
            response.raise_for_status()
            logging.info(f"{url} 访问成功")

            pattern = r'href="(http://\d+\.\d+\.\d+\.\d+:\d+)"'
            page_urls = re.findall(pattern, response.text)
            for urlx in page_urls:
                try:
                    response = requests.get(url=urlx + '/stat', timeout=1)
                    response.raise_for_status()
                    page_content = response.text
                    if 'connections online' in page_content:
                        urls_all.append(urlx)
                        logging.info(f"{urlx} 可以访问")
                except requests.RequestException:
                    continue
        except requests.RequestException:
            logging.error(f"{url_64} 访问失败")
            continue

    urls_all = set(urls_all)  # 去重得到唯一的URL列表
    for urlx in urls_all:
        channel = [f'{name},{url.replace("http://8.8.8.8:8", urlx)}' for name, url in
                   [line.strip().split(',') for line in channelsx]]
        results.extend(channel)

    results = sorted(results)
    return results

def check_download_speed(ip_list):
    speeds = []

    for ip in ip_list:
        start_time = time.time()
        try:
            response = requests.get(f"{ip}/stat", timeout=5)
            response.raise_for_status()
            elapsed_time = time.time() - start_time
            # 速度计算
            speed = 1 / elapsed_time if elapsed_time > 0 else 0
            speeds.append((ip, speed))
            logging.info(f"{ip} 下载速度: {speed:.2f} MB/s")
        except requests.RequestException:
            logging.error(f"{ip} 下载失败")
            continue

    # 根据速度排序，选取前三个最快的
    speeds.sort(key=lambda x: x[1], reverse=True)
    return speeds[:3]

def save_to_playlist(all_channels):
    with open('播放列表.m3u', 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")  # M3U 文件头
        for name, url in all_channels:
            f.write(f"#EXTINF:-1,{name}\n{url}\n")
    logging.info("所有频道已保存至播放列表文件：播放列表.m3u")

if __name__ == "__main__":
    channels = query_fofa("Hunan")
    if channels:
        logging.info("开始检测下载速度...")
        fastest_ips = check_download_speed([url.split(',')[1] for url in channels])
        
        # 将所有频道写入播放列表
        save_to_playlist(channels)
    else:
        logging.warning("没有找到可用的频道。")
