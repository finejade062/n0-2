import csv
import yaml
import math
import sys
import argparse
import numpy as np
from pathlib import Path
#引用内容

#定义读取yaml的函数
def read_yaml(comein):
  text=Path(comein)
  if not text.exists():
    print("错误，yaml文件不存在,程序停止")
    sys.exit(1)
  f=open(text,"r",encoding="utf-8")
  inyaml=yaml.safe_load(f)
  f.close()
  if inyaml is None:
      print("任务内容为空")
      sys.exit(1)
  print("任务要求：")
  print(inyaml)
  return inyaml
#定义读取read_csv的方程
def read_csv(enter,col_x,col_y):
    word = Path(enter)
    if not word.exists():
        print("错误,csv文件不存在,程序停止")
        sys.exit(1)
    f = open(word, "r", encoding="utf-8", newline="")
    reader = csv.DictReader(f)
    header = next(reader, None)
    rows = [row for row in reader]
    f.close()
    if col_x not in header or col_y not in header:
        missing=[]
        if col_x not in header:
            missing.append(col_x)
        if col_y not in header:
            missing.append(col_y)
        print(f"发现csv缺少列:{missing},程序结束")
        sys.exit(1)
    x_data = [float(row[col_x]) for row in rows]
    y_data = [float(row[col_y]) for row in rows]
    return x_data, y_data
def r(x, y,verbose=False):
    n = len(x)
    if n == 0:
        print("错误，数据为空，程序停止")
        sys.exit(1)
    if len(x) != len(y):
        print("错误，两列长度不一致，程序停止")
        sys.exit(1)

    average_x = sum(x) / n
    average_y = sum(y) / n
    if verbose:
        print(f"n = {n}")
        print(f"mean_x = {average_x:.2f}")
        print(f"mean_y = {average_y:.2f}")
    s_xy = sum((xi - average_x) * (yi - average_y) for xi, yi in zip(x, y))
    s_xx = sum((xi - average_x) ** 2 for xi in x)
    s_yy = sum((yi - average_y) ** 2 for yi in y)

    dividend= math.sqrt(s_xx * s_yy)
    if dividend == 0:
        print("错误,某列方差为0,程序停止")
        sys.exit(1)
    return s_xy/ dividend

#验证结果
def vs(x,y):
     me_r = r(x,y)
     np_r = np.corrcoef(x, y)[0,1]
     if abs(me_r - np_r) < 1e-10:
         print(f"r = {me_r}")
     else:
         print("错误")

#主体内容
def main():
    parser = argparse.ArgumentParser(description="相关系数计算程序")
    parser.add_argument("--config", required=True, help="yaml配置文件路径")
    args = parser.parse_args()
    CONFIG_PATH = Path(args.config)
    try:
        task=read_yaml(CONFIG_PATH)
        csv_path = CONFIG_PATH.parent / task["input_csv"]
        x_data, y_data = read_csv(csv_path,task["columns"]["x"],task["columns"]["y"])
        task_info = task.get("task", {})
        task_name = task_info.get("name")
        if task_name != "corr_analysis":
            print(f"错误，不支持的任务类型：{task_name}，程序停止")
            sys.exit(1)
        verbose = bool(task_info.get("verbose", False))
        me_r = r(x_data, y_data,verbose=verbose)
        print(f"计算得到相关系数 r = {me_r:.2f}")
        vs(x_data, y_data)
    except Exception as e:
        print(f"错误""{e}")
        sys.exit(1)

if __name__ =="__main__":
    main()
#防止引用时直接启动程序