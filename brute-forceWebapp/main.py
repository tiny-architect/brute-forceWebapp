#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: lzy
# github:https://github.com/tiny-architect/brute-forceWebapp

import argparse
from module import tomcat

def banner():
    banner = """
        **************************************
        *         Brute-Force Web App        *
        *                                    *
        *                  version 1.0       *
        *                                lzy *
        **************************************
    """
    print(banner)

def main():
    banner()
    pararse = argparse.ArgumentParser()
    pararse.add_argument("-tt","--targettype",default="tomcat",help="default:tomcat")
    pararse.add_argument("-f","--urlsfile",type=str,required=True,dest="file",help="urls list file.")
    pararse.add_argument("-sd","--smalldic",type=str,default="./dic/account_small.txt",
                         help="'username:password' dictionary,each username with 5 passwords")
    pararse.add_argument("-bd","--bigdic",type=str,default="./dic/account_big.txt",
                         help="'username:password' dictionary,echo username with more then 5 passwords")
    options = pararse.parse_args()
    if options.targettype == "tomcat":
        if options.file:
            urls_file = options.file
        if options.smalldic:
            small_dic = options.smalldic
        if options.bigdic:
            big_dic = options.bigdic
        tomcat.tomcat_main(urls_file,small_dic,big_dic)
    else:
        print("Only supports tomcat now!")
main()