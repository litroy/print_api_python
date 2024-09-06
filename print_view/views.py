import json
import os
from django.views.decorators.csrf import csrf_exempt
from .components.zpl.zpl_print import  zpl_print
from django.http import HttpResponse, JsonResponse
from django.views import View
import logging
logger = logging.getLogger('django')
print_key = "bq3Czj6zVe9fhMJ9tUvF0E3fXo5kwgyz"
@csrf_exempt
def get_print_data(request):
    if request.method =='POST':
        # 判断POST请求
        data = json.loads(request.body)
        print(data)
        if  'print_key' in data:
            if data['print_key'] ==  print_key:
                logger.info('开始执行打印')
                
                count =  0
                for item in data["data"]:
                    # count += 1
                    logger.info(item)
                    # zpl_print(模板名称，打印机名称，打印数量，数据)
                    response = zpl_print(data["template_name"],data["printer_name"],data["print_count"],item)
                    print(response)
                    if response["success"]:
                         count += 1
                if count > 0:
                    count_diff = len(data["data"]) - count
                    if count_diff >  0 :
                         message = f'打印成功{count}个,失败{count_diff}个！'
                    else:
                         message = f'打印成功{count}个！'
                        
                    code = '00'
                    # message = f'打印成功{count}个,失败{}！'
                    return_data =  {'success':True,'code': code, 'message': message, 'data': []}
                    return JsonResponse(return_data)
                else:
                    code = '10'
                    message = '执行失败！'
                    return_data =  {'success':False,'code': code, 'message': message, 'data': []}
                    return JsonResponse(return_data)
                
                # return zpl_print(data["template_name"],data["printer_name"],data["print_count"],data["data"])
            else:
                logger.info('print_key错误')
                code = '40'
                message = '密钥错误！'
                return_data =  {'success':False,'code': code, 'message': message, 'data': []}
                return JsonResponse(return_data)
        else:
            logger.info('没有print_key！')
            code = '40'
            message = '没有print_key！'
            return_data =  {'success':False,'code': code, 'message': message, 'data': []}
            return JsonResponse(return_data)
    else:
        logger.info(f"不是POST请求！")
        code = '20'
        message = '不是POST请求！'
        return_data =  {'success':False,'code': code, 'message': message, 'data': []}
        return JsonResponse(return_data)
    # print('dayin')
