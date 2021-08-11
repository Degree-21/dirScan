import queue
import requests
import threading
import random
import re
import multiprocessing
from Log import set_log



class DirScan:

    scan_host_name = ''
    scan_code = [200]
    queues = object
    limit = 8
    ip_list = {}

    def __init__(self, host_name='http://www.baidu.com', file_path='./御剑字典/',IsFile=bool(None)):
        self.scan_host_name = host_name
        self.queues = queue.Queue()
        self.get_all_file(file_path=file_path,IsFile=IsFile)
        self.get_ip()

    # 获取目录下面所有的文件名称
    def get_all_file(self, file_path,IsFile):
        if IsFile:
            self.file_list = file_path        
            return file_path
        else:
            file_list = [file_path + file for file in os.listdir(file_path)]
            self.file_list = file_list
            return file_list

    # 把所有key放入到队列里面
    def get_all_scan_key(self):
        for key in self.file_list:
            fd = open(key, "r",)
            print(key)
            while 1:
                buffer = fd.read(1024)
                if not buffer:
                    break
                result = buffer.split('\n')
                for res in result:
                    self.queues.put(res)
        return

    # 多进程扫描
    def scan_dir_helps(self):
        print("""
            扫描进程创建中........
        """)
        pool = multiprocessing.Pool(processes=3)
        list_scan = []
        self.get_all_scan_key()
        while self.queues.qsize() > 0:
            # while threading.active_count() < self.limit:
            key = self.queues.get()
            print(key)
            list_scan.append(pool.apply_async(self.scan_dir(key)))
            # , args = (key,)
        pool.join()
                # threads = threading.Thread(target=self.scan_dir, args=(key,))
                # threads.start()

    # 扫描
    def scan_dir(self, key):
        if 'http://' or 'https://' not in self.scan_host_name:
            host_addr = f"http://{self.scan_host_name}/{key}"
        else:
            host_addr = f"{self.scan_host_name}/{key}"

        # keys = random.choice(list(self.ip_list))
        # port_str = keys + ':' + self.ip_list[keys]
        # proxies = {
        #     'http': port_str
        # }
        try:
            # r = requests.get(url=host_addr, headers=self.get_user_agent(), proxies=proxies)
            r = requests.get(url=host_addr, headers=self.get_user_agent())
            print (r)
            
            if r.status_code in self.scan_code:
                # 写日志
                msg = {host_addr: r.status_code}
                file_name = self.scan_host_name.replace('http://', '')
                file_name = file_name.replace('https://', '')
                set_log(msg, file_name)
                print(msg)
                return msg
            
        except Exception as e:
            print(host_addr, "无法访问")

            
    @staticmethod
    def get_user_agent():
        user_agent_list = [
            {'User-Agent': 'Mozilla/4.0 (Mozilla/4.0; MSIE 7.0; Windows NT 5.1; FDM; SV1; .NET CLR 3.0.04506.30)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; en) Opera 11.00'},
            {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9.0.2) Gecko/2008092313 Ubuntu/8.04 (hardy) Firefox/3.0.2'},
            {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-GB; rv:1.9.1.15) Gecko/20101027 Fedora/3.5.15-1.fc12 Firefox/3.5.15'},
            {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.551.0 Safari/534.10'},
            {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.2) Gecko/2008092809 Gentoo Firefox/3.0.2'},
            {'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/7.0.544.0'},
            {'User-Agent': 'Opera/9.10 (Windows NT 5.2; U; en)'},
            {'User-Agent': 'Mozilla/5.0 (iPhone; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko)'},
            {'User-Agent': 'Opera/9.80 (X11; U; Linux i686; en-US; rv:1.9.2.3) Presto/2.2.15 Version/10.10'},
            {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5'},
            {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9b3) Gecko/2008020514 Firefox/3.0b3'},
            {'User-Agent': 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_4_11; fr) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16'},
            {'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)'},
            {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; X11; Linux x86_64; en) Opera 9.60'},
            {'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_2; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.366.0 Safari/533.4'},
            {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.51'}
        ]
        return random.choice(user_agent_list)

    # 代理ip
    def get_ip(self):
    # def get_ip():
        urls = "https://www.kuaidaili.com/free/inha/1/"
        str_html = requests.get(urls)
        str_text = str_html.text
        regex = re.compile('<td data-title="IP">(.*)</td>')
        ips = regex.findall(str_text)
        port_regex = re.compile('<td data-title="PORT">(.*)</td>')
        ports = port_regex.findall(str_text)
        ip_arr = {ips[key]:ports[key] for key in range(len(ips)) }

        # keys = random.choice(list(ip_arr))
        # port_str = "http://" + keys + ':' + ip_arr[keys]
        # proxies = {
        #     'http': port_str
        # }
        # print(proxies)
        # res = requests.get('http://www.baidu.com', proxies=proxies)
        # print(res)

        self.ip_list = ip_arr
        return self.ip_list


if __name__ == "__main__":
    import argparse
    import os
    parser = argparse.ArgumentParser(description='The script for dirScan')

    try:
        parser.add_argument("-url","--url", help='hostname or website name')
        parser.add_argument("-path","--path",help='directory path')
        parser.add_argument("-f","--IsFile",help='whether path is file or not',default=False)
        args = parser.parse_args()
        url = args.url
        path = args.path
        file = args.IsFile
        
    except:
        print("param is wrong !")
        os._exit(0)

    print("""
          ___  __       _  _                                 
         |__ \/_ |     | |(_)                                
            ) || |   __| | _  _ __   ___   __ _   ___  _ __  
           / / | |  / _` || || '__| / __| / _` | / __|| '_ \ 
          / /_ | | | (_| || || |    \__ \| (_| || (__ | | | |
         |____||_|  \__,_||_||_|    |___/ \__,_| \___||_| |_|
    """)

    dirScan = DirScan(file_path=path, host_name=url, IsFile=file)
    dirScan.scan_dir_helps()
    # DirScan.get_ip()

