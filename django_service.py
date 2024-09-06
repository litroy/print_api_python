import os
import sys
import win32serviceutil
import win32service
import win32event
import time
from django.core.wsgi import get_wsgi_application

class DjangoService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'print Service'
    _svc_display_name_ = 'print Service'
    _svc_description_ = 'python打印服务'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_running = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.is_running = False
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        # 获取脚本路径和项目根目录
        script_path = os.path.abspath(sys.argv[0])
        current_dir = os.path.dirname(script_path)
        project_root = os.path.abspath(os.path.join(current_dir, '..'))

        # 切换到项目根目录并更新 sys.path
        os.chdir(project_root)
        sys.path.append(project_root)

        # 设置 Django 环境变量
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'print_api.settings')

        # 启动 WSGI 应用程序
        application = get_wsgi_application()

        while self.is_running:
            try:
                # 此处可以集成 WSGI 服务器，例如使用 Waitress
                from waitress import serve
                serve(application, host='0.0.0.0', port=8003)
            except Exception as e:
                # 捕获并记录异常
                print(f"Error: {e}")
            time.sleep(10)

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(DjangoService)
