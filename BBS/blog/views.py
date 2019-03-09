from django.shortcuts import render, HttpResponse, redirect
from blog import re_forms
from blog import models
from django.http import JsonResponse
import random, json
from PIL import Image, ImageDraw, ImageFont
# 以二进制或字符串保存在内存中
from io import BytesIO, StringIO
# auth组件
from django.contrib import auth
# 分页组件
from django.core.paginator import Paginator
# ORM的F查询,直接查找字段的值
from django.db.models import F
# 事务处理模块,使得数据库保存失败有回滚作用
from django.db import transaction
# 登入装饰器
from django.contrib.auth.decorators import login_required
# 多用于爬虫的模块,html的解析
from bs4 import BeautifulSoup
# 视图函数局部禁用csrf,csrf_protect:局部使用,csrf_exempt:局部禁用
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import os
from BBS import settings
from django.views import View
from rest_framework import serializers, viewsets, routers

# Create your views here.
def user2(request):
    if request.method=="GET":
        dic={"status":200,"name":"maple","age":18}
        return HttpResponse(json.dumps(dic))
    elif request.method=="POST":
        dic={"status":200,"msg":"修改成功"}
        return JsonResponse(dic)

class Users(View):
    def get(self,request):
        dic = {"status": 200, "name": "maple", "age": 18}
        return HttpResponse(json.dumps(dic))
    def post(self,request):
        dic = {"status": 200, "msg": "修改成功"}
        return JsonResponse(dic)




def register(request):
    if request.method == "GET":
        reg_form = re_forms.RegForm()
        return render(request, "register.html", locals())
    if request.is_ajax():
        response = {"status": 100, "msg": None}
        # 把前端数据通过forms进行过滤
        reg_form = re_forms.RegForm(request.POST)
        # 开启过滤
        if reg_form.is_valid():
            # 通过过滤的数据
            form_data = reg_form.cleaned_data
            # 删除确认密码数据
            form_data.pop("re_password")
            # 获取头像图片
            img_file = request.FILES.get('img_file')
            print(img_file)
            # 判断头像是否有,没有使用字段设置默认的
            if img_file:
                form_data['avatar'] = img_file
            # 注意用create_user
            res = models.UserInfo.objects.create_user(**form_data)
            response["msg"] = "注册成功"
        else:
            response["msg"] = reg_form.errors
            response["status"] = 101
        return JsonResponse(response)


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    if request.is_ajax():
        response = {"status": 100, "msg": None}
        name = request.POST.get('name')
        password = request.POST.get('password')
        code = request.POST.get('valid_code')
        valid_code = request.session.get("valid_code")
        print(code, valid_code)
        if code.upper() == valid_code.upper():
            # 得用auth组件查询
            user = auth.authenticate(username=name, password=password)
            print(user)
            if user:
                response["msg"] = "登入成功"
                # 很重要,将user保存到request中
                auth.login(request, user)
            else:
                response["msg"] = "用户名或密码错误!"
                response["status"] = 101
        else:
            response["msg"] = "验证码错误!"
            response["status"] = 102
        return JsonResponse(response)


def index(request):
    if request.method == "GET":
        article_list = models.Article.objects.all().order_by("id")
        num = models.Article.objects.count()
        # 将文章分成每页3篇,就是一本书
        try:
            paginator = Paginator(article_list, 3)
            # 获取前端请求的页数,需要给一个默认页数
            current_page = request.GET.get("page", 1)
            current_page = int(current_page)
            # 生成page对象,就是一页
            page = paginator.page(current_page)
            # 判断总页数是否大于5
            if paginator.num_pages > 5:
                # 点击页数是否小于等于3
                if current_page <= 3:
                    # 生成一个1到5的区间
                    page_range = range(1, 6)
                #     当前页数大于最大页数减2
                elif current_page + 2 >= paginator.num_pages:
                    # 生成一个最大页数减4,到最大页数加1的区间
                    page_range = range(paginator.num_pages - 4, paginator.num_pages + 1)
                else:
                    # 生成一个点击页数减2,到点击页数加2的区间,
                    page_range = range(current_page - 2, current_page + 3)
            else:
                # 前端显示5页
                page_range = paginator.page_range
        except Exception as e:
            print(e)

        return render(request, "index.html", locals())


def login_out(request):
    auth.logout(request)
    return redirect("/index/")


def home(request):
    return redirect("/index/")


def change_password(request):
    # 判断是否登入状态
    if request.user.is_authenticated():
        if request.method == "GET":
            return render(request, "change_password.html")
        else:
            response = {"status": 100, "msg": None}
            old_password = request.POST.get("old_password")
            new_password = request.POST.get("new_password")
            renew_password = request.POST.get("renew_password")
            if request.user.check_password(old_password):
                if not new_password:
                    response["status"] = 102
                    response["msg"] = "新密码不能为空"
                elif new_password != renew_password:
                    response["status"] = 103
                    response["msg"] = "两次密码不一致"
                else:
                    request.user.set_password(new_password)
                    request.user.save()
                    auth.logout(request)
                    response["msg"] = "密码修改成功"
            else:
                response["status"] = 101
                response["msg"] = "旧密码错误"
            return JsonResponse(response)
    else:
        return redirect("/index/")


def change_avatar(request):
    # 判断是否登入状态
    if request.user.is_authenticated():
        if request.method == "GET":
            return render(request, "change_avatar.html")
        else:
            response = {"status": 100, "msg": None}
            img_file = request.FILES.get("img_file")
            if not img_file:
                response["msg"] = "你没有上传头像"
                response["status"] = 101
            else:
                request.user.avatar = img_file
                request.user.save()
                response["msg"] = "更新头像成功"
            return JsonResponse(response)
    else:
        return redirect("/index/")


def blog_site(request, username, *args, **kwargs):
    user = models.UserInfo.objects.filter(username=username).first()
    if not user:
        return render(request, "error.html")
    # 获取blog对象
    blog = user.blog

    if blog:
        # 从blog对象反向查询出所有的文章
        article_list = blog.article_set.all()
        # 分类查询
        if kwargs:
            condition = kwargs.get("condition")
            param = kwargs.get("param")
            # 如果是文章分类,查询出所有的
            if condition == "category":
                # 过滤出该分类的文章
                article_list = article_list.filter(category_id=param)
            # 如果是标签分类
            elif condition == "tag":
                # 获取标签对象,原因是文章与标签是多对多关系
                tag = models.Tag.objects.filter(pk=param).first()
                # 过滤出该标签下的文章
                article_list = article_list.filter(tag=tag)
            else:
                # 时间月份的分类,先切割出年和月
                try:
                    year_month = param.split("-")
                    year = year_month[0]
                    month = year_month[1]
                    # 过滤出年和月的文章
                    article_list = article_list.filter(var_time__year=year, var_time__month=month)
                except Exception as e:
                    print(e)

    return render(request, 'blog_site.html', locals())


def article_detail(request, username, article_id):
    article = models.Article.objects.filter(pk=article_id).first()
    comment_list = models.Comment.objects.filter(article_id=article_id)
    if request.method == "GET":
        if article:
            return render(request, 'blog_article.html', locals())
        else:
            return redirect('/error/')


def diggit(request):
    if request.is_ajax():
        response = {'status': 100, 'msg': None}
        if request.user.is_authenticated():
            article_id = request.POST.get("article_id")
            is_up = request.POST.get("is_up")
            # 将字符串转成bool
            is_up = json.loads(is_up)
            # 查询文章和用户有没有点赞过
            res = models.UpAndDown.objects.filter(article_id=article_id, user=request.user)
            # 如果没有就添加到数据库
            if not res:
                # 如果是True就是点赞
                if is_up:
                    # 查询那篇文章,跟新点赞数
                    models.Article.objects.filter(pk=article_id).update(up_num=F("up_num") + 1)
                    response["msg"] = "点赞成功"
                else:
                    models.Article.objects.filter(pk=article_id).update(down_num=F("down_num") + 1)
                    response["msg"] = "点踩成功"
                # 文章表更新后,再更新点赞表
                models.UpAndDown.objects.create(user=request.user, article_id=article_id, is_up=is_up)
            else:
                response["msg"] = "你已经点过了"
                response["status"] = 101
        else:
            response["msg"] = "请先登入"
            response["status"] = 102
        return JsonResponse(response)


def comment(request):
    # try:
    if request.is_ajax():
        response = {'status': 100, 'msg': None}
        if request.user.is_authenticated():
            article_id = request.POST.get("article_id")
            content = request.POST.get("content")
            parent_id = request.POST.get("parent_id")
            with transaction.atomic():
                res = models.Comment.objects.create(user=request.user, article_id=article_id, content=content,
                                                    parent_id=parent_id)
                models.Article.objects.filter(pk=article_id).update(comment_num=F("comment_num") + 1)
                if parent_id:
                    response["parent_username"] = res.parent.user.username
            print(321)
            response["msg"] = "评论成功"
            response["username"] = request.user.username
            response["content"] = content
            # json不能序列化时间对象,转成字符串格式
            response["reply_time"] = res.comment_time.strftime("%Y-%m-%d %X")
        else:
            response["msg"] = "请先登入"
            response["status"] = 101
        # except Exception as e:
        #     print(e)
        #     response['msg']=str(e)
        #     response['status']=102
        return JsonResponse(response)


@login_required(login_url="/login/")
def backend(request):
    if request.method == "GET":
        article_list = models.Article.objects.filter(blog=request.user.blog)
        return render(request, "backends/backend.html", locals())


@login_required(login_url="/login/")
def add_article(request):
    if request.method == "GET":
        tags = models.Tag.objects.filter(blog=request.user.blog)
        categorys = models.Category.objects.filter(blog=request.user.blog)
        return render(request, "backends/add_article.html", locals())
    else:
        title = request.POST.get("title")
        content = request.POST.get("content")
        tag_id = request.POST.get("tag")
        category_id = request.POST.get("category")
        # 解析html内容
        soup = BeautifulSoup(content, "html.parser")
        # 查询所有的html标签
        tags = soup.find_all()
        for tag in tags:
            # 防止xss攻击,删除script标签
            if tag.name == "script":
                # 删除标签
                tag.decompose()
        #         获取150个字符
        summary = soup.text[0:150]
        with transaction.atomic():
            res = models.Article.objects.create(title=title, summary=summary, content=str(soup),
                                                blog=request.user.blog, category_id=category_id, )
            models.ArticleToTag.objects.create(article_id_id=res.pk, tag_id_id=tag_id)
        return redirect("/backend/")


@login_required(login_url="/login/")
def modification_article(request):
    if request.method == "GET":
        article_id = request.GET.get("article_id")
        article = models.Article.objects.filter(pk=article_id).first()
        article_to_tag = models.ArticleToTag.objects.filter(article_id=article_id).first()
        tags = models.Tag.objects.filter(blog=request.user.blog)
        categorys = models.Category.objects.filter(blog=request.user.blog)
        return render(request, "backends/modification_article.html", locals())
    else:
        title = request.POST.get("title")
        article_id = request.POST.get("article_id")
        content = request.POST.get("content")
        tag_id = request.POST.get("tag")
        category_id = request.POST.get("category")
        # 解析html内容
        soup = BeautifulSoup(content, "html.parser")
        # 查询所有的html标签
        tags = soup.find_all()
        for tag in tags:
            # 防止xss攻击,删除script标签
            if tag.name == "script":
                # 删除标签
                tag.decompose()
        #         获取150个字符
        summary = soup.text[0:150]
        with transaction.atomic():
            models.Article.objects.filter(pk=article_id).update(title=title, summary=summary,
                                                                category_id=category_id, content=str(soup))
            models.ArticleToTag.objects.filter(article_id_id=article_id).update(tag_id_id=tag_id)
        return redirect("/backend/")


@login_required(login_url="/login/")
def delete_article(request):
    article_id = request.GET.get("article_id")
    with transaction.atomic():
        # 删除文章
        models.Article.objects.filter(pk=article_id).delete()
        # 注意还得删除文章对应的点赞数据和评论数据
        models.Comment.objects.filter(article_id=article_id).delete()
        models.UpAndDown.objects.filter(article_id=article_id).delete()
        # 删除标签分类中间表里的数据
        models.ArticleToTag.objects.filter(article_id_id=article_id).delete()
    return redirect("/backend/")


@csrf_exempt
def add_img(request):
    file = request.FILES.get("imgFile")
    # 文件夹路径
    path = os.path.join(settings.BASE_DIR, "media", "article_img", request.user.username)
    print(path)
    if not os.path.exists(path):
        os.makedirs(path)
    # 图片路径
    img_path = os.path.join(path, file.name)
    with open(img_path, "wb")as f:
        for line in file:
            f.write(line)
        response = {"error": 0, "url": "/media/article_img/%s/%s" % (request.user.username, file.name)}
    return JsonResponse(response)


def error(request):
    return render(request, 'error.html')


# 随机图片验证码
def get_valid_code(request):
    # 随机字母数字
    def rndChar():
        char_num = random.randint(0, 9)
        # 大写字母
        char_upper = chr(random.randint(65, 90))
        # 小写字母
        char_lower = chr(random.randint(97, 122))
        # 随机抽取一个数字或字母
        char_str = str(random.choice([char_num, char_upper, char_lower]))
        return char_str

    # 随机颜色1,颜色淡
    def rndColor1():
        return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

    # 随机颜色2,颜色深
    def rndColor2():
        return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

    # 创建image对象,就是画纸
    width = 60 * 5
    height = 60
    image = Image.new('RGB', (width, height), rndColor1())
    # 创建font对象,用来选择字体
    font = ImageFont.truetype(r"static/font/calligraph421-bt-roman.woff.ttf", 40)
    # 创建draw对象,就是画板
    draw = ImageDraw.Draw(image)

    # 输出文字
    random_code = ''
    for t in range(5):
        # 写入的随机数字字母
        char_str = rndChar()
        # 元组参数是写入的位置,x,y轴,char_str输入的文字,font字体,fill背景颜色
        draw.text((60 * t + 10, 5), char_str, font=font, fill=rndColor2())
        random_code += char_str

    # 划线
    for i in range(5):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        # x1, y1, x2, y2分别是线的开始位置和结束位置坐标
        draw.line((x1, y1, x2, y2), fill=rndColor1())

    # 画点
    for i in range(30):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor1())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rndColor1())

    # 验证码保存到session中
    request.session['valid_code'] = random_code
    # 将图片保存到内存中
    f = BytesIO()
    image.save(f, 'jpeg')
    data = f.getvalue()
    return HttpResponse(data)
