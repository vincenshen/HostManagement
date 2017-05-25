from django.shortcuts import render, HttpResponse, redirect, reverse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.hashers import make_password
# Create your views here.
from .models import Business, Host, UserInfo
import json


# 认证装饰器
class Auth(View):
    def dispatch(self, request, *args, **kwargs):
        user_obj = UserInfo.objects.filter(username=request.session.get("username")).first()
        if not user_obj:
            return redirect(reverse("login"))
        return super(Auth, self).dispatch(request, *args, **kwargs)


# 主页视图
class IndexView(Auth):
    def get(self, request):
        user = request.session.get("username")
        business_obj = Business.objects.all()
        user_obj = UserInfo.objects.all()
        hosts = Host.objects.filter(user__username=user)
        return render(request, "index.html", {
            "hosts": hosts,
            "business_obj": business_obj,
            "user_obj": user_obj
        })


# 登录视图
class LoginView(View):
    def get(self, request):
        return render(request, "login_register.html")

    def post(self, request):
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        print(request.POST)
        user_obj = UserInfo.objects.filter(username=username, password=password).first()
        response = {"status": True, "error": None}
        print("user", user_obj)
        if user_obj:
            request.session["username"] = username
            request.session["password"] = password
            return HttpResponse(json.dumps(response))
        # 返回ajax信息
        else:
            response["status"] = False
            response["error"] = "用户名或密码错误"
            return HttpResponse(json.dumps(response))


# 注销视图
class LogoutView(View):
    def get(self, request):
        request.session.flush()
        return redirect(reverse("index"))


# 注册视图
class RegisterView(View):
    def post(self, request):
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user_obj = UserInfo.objects.filter(username=username)
        response = {"status": True, "error": None}

        # 对ajax提交的用户判断是否已存在
        if user_obj:
            response["status"] = False
            response["error"] = "该用户名已存在"
            return HttpResponse(json.dumps(response))
        # 对ajax提交的用户和密码进行创建
        elif username and password:
            UserInfo.objects.create(username=username, password=password)
            return HttpResponse(json.dumps(response))
        else:
            return HttpResponse(json.dumps(response))


# 业务线管理视图
class BusinessCreate(Auth):
    def get(self, request):
        return render(request, "business_line_create.html")

    def post(self, request):
        name = request.POST.get("name", "")
        name_obj = Business.objects.filter(name=name).first()
        response = {"status": True, "error": None}

        # 对ajax提交的业务组判断是否已存在
        if name_obj:
            response["status"] = False
            response["error"] = "该业务组已存在"
            return HttpResponse(json.dumps(response))

        else:
            Business.objects.create(name=name)
            return HttpResponse(json.dumps(response))


# 主机创建视图
class HostCreateView(Auth):
    def get(self, request):
        business_obj = Business.objects.all()
        user_obj = UserInfo.objects.all()
        return render(request, "host_create.html", {
            "business_obj": business_obj,
            "user_obj": user_obj
        })

    def post(self, request):
        hostname = request.POST.get("hostname", "")
        ipaddress = request.POST.get("ipaddress", "")
        users = request.POST.getlist("owner[]", "")
        business_line = request.POST.get("business", "")
        response = {"status": True, "error": None}
        if hostname and ipaddress and users and business_line:
            host = Host.objects.create(hostname=hostname, address=ipaddress, business_id=business_line)
            host.user.add(*users)
            return HttpResponse(json.dumps(response))
        else:
            response["status"] = False
            response["error"] = "创建失败"
            return HttpResponse(json.dumps(response))


# 主机编辑视图
class HostEditView(Auth):
    def get(self, request, host_id):
        business_obj = Business.objects.all()
        user_obj = UserInfo.objects.all()
        host_obj = Host.objects.filter(id=host_id).first()
        return render(request, "host_edit.html", {
            "host_obj": host_obj,
            "business_obj": business_obj,
            "user_obj": user_obj
        })

    def post(self, request, host_id):
        hostname = request.POST.get("hostname", "")
        ipaddress = request.POST.get("ipaddress", "")
        users = request.POST.getlist("owner[]", "")
        business_line = request.POST.get("business", "")
        response = {"status": True, "error": None}
        if hostname and ipaddress and users and business_line:
            Host.objects.filter(id=host_id).update(hostname=hostname, address=ipaddress, business_id=business_line)
            host = Host.objects.filter(id=host_id)[0]
            for obj in users:
                user = UserInfo.objects.get(id=obj)
                host.user.add(user)
            return HttpResponse(json.dumps(response))
        else:
            response["status"] = False
            response["error"] = "创建失败"
            return HttpResponse(json.dumps(response))


# 主机删除视图
class HostDeleteView(Auth):
    def get(self, request, host_id):
        Host.objects.filter(id=host_id).delete()
        return redirect(reverse("index"))