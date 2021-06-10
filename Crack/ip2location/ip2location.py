import re
import execjs
import requests


class GetIPInfo(object):

    def __init__(self):
        self.__get_local_url = "https://gwgp-kk6owjrbujz.i.bdcloudapi.com/aladdin/ip/query"
        self.__select_url = "https://gwgp-kk6owjrbujz.i.bdcloudapi.com/ip2location/retrieve"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
        }
        self.payload = {}

    def __get_timestamp(self, method, path):
        code = """
        function d(t, e) {
            var n = (65535 & t) + (65535 & e);
            return (t >> 16) + (e >> 16) + (n >> 16) << 16 | 65535 & n
        }
        function s(t, e, n, r, a, o) {
            return d((i = d(d(e, t), d(r, o))) << (s = a) | i >>> 32 - s, n);
            var i, s
        }
        function p(t, e, n, r, a, o, i) {
            return s(e & n | ~e & r, t, e, a, o, i)
        }
        function f(t, e, n, r, a, o, i) {
            return s(e & r | n & ~r, t, e, a, o, i)
        }
        function h(t, e, n, r, a, o, i) {
            return s(e ^ n ^ r, t, e, a, o, i)
        }
        function g(t, e, n, r, a, o, i) {
            return s(n ^ (e | ~r), t, e, a, o, i)
        }
        function c(t, e) {
            var n, r, a, o;
            t[e >> 5] |= 128 << e % 32,
            t[14 + (e + 64 >>> 9 << 4)] = e;
            for (var i = 1732584193, s = -271733879, c = -1732584194, u = 271733878, l = 0; l < t.length; l += 16)
                i = p(n = i, r = s, a = c, o = u, t[l], 7, -680876936),
                u = p(u, i, s, c, t[l + 1], 12, -389564586),
                c = p(c, u, i, s, t[l + 2], 17, 606105819),
                s = p(s, c, u, i, t[l + 3], 22, -1044525330),
                i = p(i, s, c, u, t[l + 4], 7, -176418897),
                u = p(u, i, s, c, t[l + 5], 12, 1200080426),
                c = p(c, u, i, s, t[l + 6], 17, -1473231341),
                s = p(s, c, u, i, t[l + 7], 22, -45705983),
                i = p(i, s, c, u, t[l + 8], 7, 1770035416),
                u = p(u, i, s, c, t[l + 9], 12, -1958414417),
                c = p(c, u, i, s, t[l + 10], 17, -42063),
                s = p(s, c, u, i, t[l + 11], 22, -1990404162),
                i = p(i, s, c, u, t[l + 12], 7, 1804603682),
                u = p(u, i, s, c, t[l + 13], 12, -40341101),
                c = p(c, u, i, s, t[l + 14], 17, -1502002290),
                i = f(i, s = p(s, c, u, i, t[l + 15], 22, 1236535329), c, u, t[l + 1], 5, -165796510),
                u = f(u, i, s, c, t[l + 6], 9, -1069501632),
                c = f(c, u, i, s, t[l + 11], 14, 643717713),
                s = f(s, c, u, i, t[l], 20, -373897302),
                i = f(i, s, c, u, t[l + 5], 5, -701558691),
                u = f(u, i, s, c, t[l + 10], 9, 38016083),
                c = f(c, u, i, s, t[l + 15], 14, -660478335),
                s = f(s, c, u, i, t[l + 4], 20, -405537848),
                i = f(i, s, c, u, t[l + 9], 5, 568446438),
                u = f(u, i, s, c, t[l + 14], 9, -1019803690),
                c = f(c, u, i, s, t[l + 3], 14, -187363961),
                s = f(s, c, u, i, t[l + 8], 20, 1163531501),
                i = f(i, s, c, u, t[l + 13], 5, -1444681467),
                u = f(u, i, s, c, t[l + 2], 9, -51403784),
                c = f(c, u, i, s, t[l + 7], 14, 1735328473),
                i = h(i, s = f(s, c, u, i, t[l + 12], 20, -1926607734), c, u, t[l + 5], 4, -378558),
                u = h(u, i, s, c, t[l + 8], 11, -2022574463),
                c = h(c, u, i, s, t[l + 11], 16, 1839030562),
                s = h(s, c, u, i, t[l + 14], 23, -35309556),
                i = h(i, s, c, u, t[l + 1], 4, -1530992060),
                u = h(u, i, s, c, t[l + 4], 11, 1272893353),
                c = h(c, u, i, s, t[l + 7], 16, -155497632),
                s = h(s, c, u, i, t[l + 10], 23, -1094730640),
                i = h(i, s, c, u, t[l + 13], 4, 681279174),
                u = h(u, i, s, c, t[l], 11, -358537222),
                c = h(c, u, i, s, t[l + 3], 16, -722521979),
                s = h(s, c, u, i, t[l + 6], 23, 76029189),
                i = h(i, s, c, u, t[l + 9], 4, -640364487),
                u = h(u, i, s, c, t[l + 12], 11, -421815835),
                c = h(c, u, i, s, t[l + 15], 16, 530742520),
                i = g(i, s = h(s, c, u, i, t[l + 2], 23, -995338651), c, u, t[l], 6, -198630844),
                u = g(u, i, s, c, t[l + 7], 10, 1126891415),
                c = g(c, u, i, s, t[l + 14], 15, -1416354905),
                s = g(s, c, u, i, t[l + 5], 21, -57434055),
                i = g(i, s, c, u, t[l + 12], 6, 1700485571),
                u = g(u, i, s, c, t[l + 3], 10, -1894986606),
                c = g(c, u, i, s, t[l + 10], 15, -1051523),
                s = g(s, c, u, i, t[l + 1], 21, -2054922799),
                i = g(i, s, c, u, t[l + 8], 6, 1873313359),
                u = g(u, i, s, c, t[l + 15], 10, -30611744),
                c = g(c, u, i, s, t[l + 6], 15, -1560198380),
                s = g(s, c, u, i, t[l + 13], 21, 1309151649),
                i = g(i, s, c, u, t[l + 4], 6, -145523070),
                u = g(u, i, s, c, t[l + 11], 10, -1120210379),
                c = g(c, u, i, s, t[l + 2], 15, 718787259),
                s = g(s, c, u, i, t[l + 9], 21, -343485551),
                i = d(i, n),
                s = d(s, r),
                c = d(c, a),
                u = d(u, o);
            return [i, s, c, u]
        }
        function u(t) {
            for (var e = "", n = 32 * t.length, r = 0; r < n; r += 8)
                e += String.fromCharCode(t[r >> 5] >>> r % 32 & 255);
            return e
        }
        function l(t) {
            var e = [];
            for (e[(t.length >> 2) - 1] = undefined,
            r = 0; r < e.length; r += 1)
                e[r] = 0;
            for (var n = 8 * t.length, r = 0; r < n; r += 8)
                e[r >> 5] |= (255 & t.charCodeAt(r / 8)) << r % 32;
            return e
        }
        function a(t) {
            for (var e, n = "0123456789abcdef", r = "", a = 0; a < t.length; a += 1)
                e = t.charCodeAt(a),
                r += n.charAt(e >>> 4 & 15) + n.charAt(15 & e);
            return r
        }
        function o(t) {
            return unescape(encodeURIComponent(t))
        }
        
        function getUTC(){
            var date = new Date(),
            year = date.getUTCFullYear(),
            month = (date.getUTCMonth() + 1).toString().padStart(2,'0'),
            day = date.getUTCDate().toString().padStart(2,'0'),
            hour = date.getUTCHours().toString().padStart(2,'0'),
            mintues = date.getUTCMinutes().toString().padStart(2,'0'),
            second = date.getUTCSeconds().toString().padStart(2,'0');
            return year + "-" + month + "-" + day + "T" + hour + ":" + mintues + ":" + second + "Z";
        }
        
        function run()
        {
            var time = getUTC();
            var t = "{method}{path}"+ time + "ieq%$jsaf23!@fkjwie"
            return time + "@" + a(u(c(l(o(t)), 8 * t.length)));
        }
        """.replace("{method}", method).replace("{path}", path)
        timestamp = execjs.compile(code).call('run')
        return timestamp

    def select(self, ip=None):
        send_url = self.__select_url if ip else self.__get_local_url
        if ip:
            self.headers['timestamp'] = self.__get_timestamp("POST", "/ip2location/retrieve")
            self.payload["ip"] = ip
            resp = requests.post(send_url, headers=self.headers, data=str(self.payload).replace("'", "\"")).json()
        else:
            self.headers['timestamp'] = self.__get_timestamp("GET", "/aladdin/ip/query")
            resp = requests.get(send_url, headers=self.headers).json()
        for k, v in resp.items():
            print(f'{k}:\t{v}')

    def run(self):
        mode = input("请选择功能：\n[1] 获取本机IP信息\n[2] 查询指定IP信息\n>>")
        ip = None
        while mode not in ["1", "2"]:
            mode = input("输入错误，请重新输入\n>>")
        if mode == "2":
            ip = input("请输入查询的ip地址\n>>")
            while not re.search(r'(([01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])\.){3}([01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])',
                                ip):
                ip = input("输入有误，请输入查询的ip地址\n>>")
        self.select(ip)


if __name__ == "__main__":
    GetIPInfo().run()
