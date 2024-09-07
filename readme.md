
# 开发文档
# 本服务基于 Django 框架实现，有意学习可移步CSDN
https://blog.csdn.net/qq_41710802/article/details/138891582
## 驱动相关
    pip install pywin32
## 开发环境启动
python manage.py runserver 0.0.0.0:8004
## api地址
http://localhost:8003/api/af_admin/print/
## 实现原理
    替换指令集的 以字段命名变量 或者 数据
    前端传递json数据举例
    可以多条数据 打印
    {
    "template_name":"TP01.prn",
    "printer_name":"打印机名称",
    "print_count":1,
    "data":[
            {
                "Barcode":"A202408056"
            },
             {
                "Barcode":"A202408057"
            }
    ]
}
## 设置为windows服务自动启动
django_service.py 文件是为了将运行环境安装为windows的服务
安装为服务
python django_service.py install
# 后续开源 自己开发的生产管理系统 
前端使用 js库：vue3.0 +
PC前端UI:element plus  
H5移动前端UI：nutui  (京东UI)
前端表格库：vxe-table
后端：
python +django
持久层 redis  .....
已实现钉钉通知相关、用友U9C erpOPENapi对接相关、通用型编号生成器等等。
