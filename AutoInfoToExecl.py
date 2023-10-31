import pandas as pd
import os
import config
import merge
import argparse
"""
按照顺序执行，以后是否有优化（模块形式）？
开始选择较简陋，需要优化
把工具放到脚本同级目录，名称与config.py中名称一致
"""

class Run():
    def __init__(self,model,name):
        self.model = model
        self.name = name
    
    def start(self):
        if self.model == 0:
            #如果是无IP和域名直接调用ENscan,提取获取的域名信息
            cmd_ENscan = str(config.ENscan) + ' -n ' +self.name
            ENscan = os.system(cmd_ENscan)
        else:
            #创建总表，把域名导入
            merge.create_merge(self.name)
        #获取总表路径
        merge.get_root_file(self.name)

    def wr_oneforall(self):
        #把域名写入到oneforall目录下
        merge.exp_target('oneforall',self.model)

    def oneforall(self):
        cmd_Oneforall = f'python {str(config.Oneforall)} --targets {str(config.Oneforall_txt)} run'
        Oneforall = os.system(cmd_Oneforall)
        #把oneforall结果合并到总表中
        merge.Oneforall_to_merge()

    def wr_httpx(self):
    #把url写入到httpx目录下
        merge.exp_target('httpx')

    def httpx(self):
        cmd_httpx = f'{str(config.httpx)} -status-code -title -csv -o {str(config.httpx_out)}/{self.name}.csv -list {str(config.httpx_url)}'
        httpx = os.system(cmd_httpx)
        #把httpx结果合并到总表中
        merge.httpx_to_merger()

    def wr_ehole(self):
        #把存活的url结果写入到ehole目录下，进一步批量探测
        merge.exp_target('ehole')

    def ehole(self):
        """
        对于执行exe脚本，先切换到执行目录下再执行，否则无法调用同级目录下配置文件，系统会报错(python执行目录与脚本执行目录不同)
        os.system执行cd要加/d参数，不加参数，不改变工作目录。
        """
        cmd_ehole = f"cd /d {config.ehole_out} && ehole.exe finger -l {config.ehole_url} -o {config.ehole_out/'test.xlsx'}"
        ehole = os.system(cmd_ehole)
        #把ehole结果合并到总表中
        merge.ehole_to_merger()

def main():
    parse = argparse.ArgumentParser()
    parse.description = 'model 0无域名收集，mode 1有域名收集'
    parse.add_argument("-m","--input model",help="target model",dest="model",type=int,default=None)
    parse.add_argument("-n","--input name",help="target name",dest="name",type=str,default=None)
    args = parse.parse_args()
    go = Run(args.model,args.name)
    go.start()
    go.wr_oneforall()
    go.oneforall()
    go.wr_httpx()
    go.httpx()
    go.wr_ehole()
    go.ehole()
    
if __name__ == "__main__":
    main()