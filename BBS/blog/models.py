from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


# auth模块用户表
class UserInfo(AbstractUser):
    mobile_phone=models.BigIntegerField(null=True,blank=True)
    # auto_now_add=True自动添加
    create_time=models.DateTimeField(auto_now_add=True)
    # 添加头像字段,upload_to自动保存到指定文件夹,default设定默认图片
    avatar=models.FileField(upload_to="avatar/",default="avatar/default.png")
    # 博客表外键关联
    blog=models.OneToOneField(to="Blog",to_field="id",null=True)

    # 打印该对象时,显示username
    def __str__(self):
        return self.username

    # 在admin后台中,使表名为中文
    # class Meta:
    #     verbose_name='用户表'
    #     verbose_name_plural=verbose_name


# 博客表,个人站点表
class Blog(models.Model):
    # 站点名称
    site_name=models.CharField(max_length=32)
    # 站点标题
    site_title=models.CharField(max_length=32)
    # 个人主题,可以设置成站点的个性化样式css文件
    theme=models.CharField(max_length=32)

    def __str__(self):
        return self.site_name

# 分类表
class Category(models.Model):
    # 分类名称
    name=models.CharField(max_length=32)
    # 站点外键
    blog=models.ForeignKey(to="Blog",to_field="id",null=True)
    def __str__(self):
        return self.name


# 标签表
class Tag(models.Model):
    # 标签名称
    name=models.CharField(max_length=32)
    # 站点外键
    blog = models.ForeignKey(to="Blog", to_field="id", null=True)

    def __str__(self):
        return self.name

# 文章表
class Article(models.Model):
    # 文章标题
    title=models.CharField(max_length=64)
    # 文章概要
    summary=models.CharField(max_length=255)
    # 文章内容,用大文本字段TextField()
    content=models.TextField()
    # 文章创建时间
    var_time=models.DateTimeField(auto_now_add=True)
    # 文章分类,可以为空
    category=models.ForeignKey(to="Category",to_field='id',null=True)
    # 与标签表的多对多关联
    tag=models.ManyToManyField(to="Tag",through="ArticleToTag",through_fields=("article_id","tag_id"))
    # 文章表中添加评论数,方便查询
    comment_num=models.IntegerField(default=0)
    # 文章表中添加点赞数,方便查询
    up_num = models.IntegerField(default=0)
    # 文章表中添加点踩数,方便查询
    down_num = models.IntegerField(default=0)
    # 站点外键
    blog = models.ForeignKey(to='Blog', to_field='id', null=True)

    def __str__(self):
        return self.title



# 文章与标签的中间表
class ArticleToTag(models.Model):
    article_id=models.ForeignKey(to="Article",to_field="id")
    tag_id=models.ForeignKey(to="Tag",to_field="id")

# 点赞点踩表
class UpAndDown(models.Model):
    # 点击用户外键关联
    user=models.ForeignKey(to="UserInfo",to_field='id')
    # 点击的那篇文章外键关联
    article=models.ForeignKey(to="Article",to_field='id')
    # 点赞点踩用bool类型表示,True为赞,False为踩
    is_up=models.BooleanField()

# 评论表
class Comment(models.Model):
    # 评论用户外键关联
    user = models.ForeignKey(to="UserInfo", to_field='id')
    # 评论的那篇文章外键关联
    article = models.ForeignKey(to="Article", to_field='id')
    # 评论内容
    content = models.CharField(max_length=255)
    # 子评论自关联
    parent = models.ForeignKey(to='Comment', to_field='id', null=True,blank=True)
    # 评论创建时间
    comment_time = models.DateTimeField(auto_now_add=True)

