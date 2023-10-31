from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parent

#enscan 执行目录和输出目录，可以在config中直接配置脚本所在同级目录
ENscan = ROOT_PATH/'tools/enscan/enscan.exe'
ENscan_result = ROOT_PATH/'tools/enscan/outs'

#oneforall执行目录，批量查询文件目录，结果目录
Oneforall = ROOT_PATH/'tools/OneForAll/oneforall.py'
Oneforall_txt = ROOT_PATH/'tools/OneForAll/domain.txt'
Oneforall_result = ROOT_PATH/'tools/OneForAll/results'

#httpx执行目录，批量查询文件目录，结果目录
httpx = ROOT_PATH/'tools/httpx/httpx.exe'
httpx_url = ROOT_PATH/'tools/httpx/urls.txt'
httpx_out = ROOT_PATH/'tools/httpx/'

#ehole执行目录，批量查询文件目录，结果目录
ehole = ROOT_PATH/'tools/EHole/ehole.exe'
ehole_url = ROOT_PATH/'tools/Ehole/urls.txt'
ehole_out = ROOT_PATH/'tools/Ehole'