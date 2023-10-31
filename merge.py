import pandas as pd
from pathlib import Path
import config
import glob
import time


ROOT_PATH = Path(__file__).resolve().parent

#有域名的，把域名写入到脚本同目录的urls.txt文件中，会自动创建汇总表
def create_merge(name):
    with open(ROOT_PATH/'urls.txt','r') as f:
        lines = f.readlines()
    lines = [url.replace('\n','') for url in lines]
    df = pd.DataFrame({'url':lines})
    df.to_excel(ROOT_PATH/'result/{}.xlsx'.format(name), index=False)

#根据名称获取创建的汇总表，获取汇总表路径
def get_root_file(name):
    global ROOT_FILE 
    ROOT_FILE = [str(f) for f in Path(ROOT_PATH/'result').glob(f"*"+name+"*.xlsx") if Path(f).is_file()][0]

#把ENscan中收集到的子域名，写入到oneforall的执行目录中
def exp_target(exname,domain=1):
    if exname == 'oneforall':
        #添加判断，如果无域名获取域名格式为enscan execl中格式，反之获取create_merge函数创建的execl格式域名数据
        if domain == 0:
            df = pd.read_excel(ROOT_FILE,sheet_name=1)
            subdomain = df.iloc[0:,2].values
        else:
            df = pd.read_excel(ROOT_FILE,sheet_name=0)
            subdomain = df.iloc[0:,0].values
        file_path = Path(config.Oneforall).parent/'domain.txt'
    elif exname == 'httpx':
        df = pd.read_excel(ROOT_FILE,sheet_name='subdomain')
        subdomain = df.iloc[0:,4].values
        file_path = Path(config.httpx_out)/'urls.txt'
    elif exname == 'ehole':
        df = pd.read_excel(ROOT_FILE,sheet_name='httpx_url')
        subdomain = df.iloc[0:,10].values
        file_path = Path(config.ehole_out)/'urls.txt'
    with open(file_path,'w') as f:
        for i in subdomain:
            f.write(i+'\n')

#根据时间获取文件夹下最新的文件
def get_new_file(path):
    if 'Ehole' in str(Path(path)):
        excel_files = Path(path).glob("*.xlsx")
    else:
        excel_files = Path(path).glob("*.csv")
    latest_excel_file = max(excel_files, key=lambda x: Path(x).stat().st_mtime)
    return latest_excel_file

def move_execl(move_path,sheetname):
    #移动表格
    if Path(move_path).suffix == ".csv" and 'OneForAll' in str(Path(move_path)):
        df_sheet1 = pd.read_csv(move_path,encoding='ANSI')  # 读取A文件的第一张工作表
    elif Path(move_path).suffix == ".csv" and 'httpx' in str(Path(move_path)):
        df_sheet1 = pd.read_csv(move_path,encoding='unicode_escape')
        #df_sheet1.drop(columns=['-','timestamp','asn','-','csp','tls','hash','extract_regex','cdn_name',-.1,'favicon'])
    elif Path(move_path).suffix == ".xlsx" and 'Ehole' in str(Path(move_path)):
        df_sheet1 = pd.read_excel(move_path,sheet_name=0)
    elif Path(move_path).suffix == ".xlsx":
        df_sheet1 = pd.read_excel(move_path,sheet_name=0)
    # 读取B文件中的内容
    existing_df = pd.read_excel(ROOT_FILE)
    # 将A文件中的内容追加到B文件
    with pd.ExcelWriter(ROOT_FILE, mode='a', engine='openpyxl') as writer:
        df_sheet1.to_excel(writer, sheet_name=sheetname, index=False, header=True)

#把oneforall中的结果合并到总表中
def Oneforall_to_merge():
    move_execl(get_new_file(config.Oneforall_result),sheetname='subdomain')
    print("已经将Oneforall结果整合到总表中。")
	time.sleep(1)

#把httpx的结果合并到总表中
def httpx_to_merger():
    move_execl(get_new_file(config.httpx_out),sheetname='httpx_url')
    print("已经将httpx结果整合到总表中。")
	time.sleep(1)

#把ehole的结果合并到总表中
def ehole_to_merger():
    move_execl(get_new_file(config.ehole_out),sheetname='cms')
    print("已经将ehole结果整合到总表中。")