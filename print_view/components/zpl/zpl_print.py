import os
from django.http import JsonResponse
from django.conf import settings
import win32print
import win32api
import logging

logger = logging.getLogger('django')
def replace_in_prn(file_path, old_string, new_string, output_file=None):
    # 读取 .prn 文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 替换指定的字符串
    new_content = content.replace(old_string, new_string)

    # 输出到新文件或覆盖原文件
    # output_file = output_file or file_path
    # with open(output_file, 'w', encoding='utf-8') as file:
        # file.write(new_content) 

    print(f"字符串替换完成，结果已保存至 {output_file}")

# 示例用法
# replace_in_prn('example.prn', '旧字符串', '新字符串', 'output.prn')
 
# zpl_print("模板名称"，打印机名称，打印份数，打印内容)
def zpl_print(template_name,printer_name,print_count,data):
    project_root = settings.BASE_DIR
    template_path  = os.path.join(project_root, "print_view", "template", template_name)
    # print(template_path)
    with open(template_path, 'r', encoding='utf-8') as file:
        content = file.read()
    # return
    # print(content)
    print_data = replace_content(content, print_count,data)
    
    # print(print_data)
    # code = '40'
    # message = '不是GET或POST请求！'
    #发送打印数据到打印机
    get_data = f"{template_name},{printer_name},{print_count},{data}"
    re_data = send_to_local_printer(printer_name,print_data,get_data)
    if re_data["success"]:
        
        # return_data =  {'template_name': template_name, 'printer_name': printer_name, 'data': print_data}
        return re_data
    else:
        return re_data
    # print(return_data)
    
# 3. 替换指定内容
def replace_content(content, print_count,data):
    for key, value in data.items():
        # 根据实际需要定义替换规则
        
        # placeholder = f'{{{{{key}}}}}'
        # print(placeholder)
        content = content.replace(key, value)
    # content = content.replace("PQ1", "PQ" + str(print_count))
    return content
def send_to_local_printer(printer_name, zpl_data,get_data):
    try:
        # get_data是前端传递过来的值
        # return {"success":True,"message":"数据已发送打印！","data":[]}

        printer_handle = win32print.OpenPrinter(printer_name)
        win32print.StartDocPrinter(printer_handle, 1, ("ZPL Document", None, "RAW"))
        win32print.StartPagePrinter(printer_handle)
        win32print.WritePrinter(printer_handle, zpl_data.encode('utf-8'))
        win32print.EndPagePrinter(printer_handle)
        win32print.EndDocPrinter(printer_handle)
        win32print.ClosePrinter(printer_handle)
        logger.info(f"已执行打印：{get_data}")
        return {"success":True,"message":"数据已发送打印！","data":[]}

        # print("打印数据已发送到本地打印机")
    except Exception as e:
        print(f"打印失败: {e}")
        logger.info(f"打印失败：{e},{get_data}")
        return {"success":False,"message":f"打印失败!{str(e)}","data":str(e)}
        # return {"success":False,"message":"数据已发送打印！","data":[]}
    