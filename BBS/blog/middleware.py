# -*- coding: utf-8 -*-
"""
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""





# class RequestBlockingMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         ip = request.META.get("REMOTE_ADDR")
#         visit_time = time.time()
#         if ip not in visit_ip_pool:
#             visit_ip_pool[ip] = [visit_time]
#         else:
#             # 将访问的ip时间插入到对应ip的key值列表的第一位置,如{"127.0.0.1":[时间1,时间2]}
#             visit_ip_pool[ip].insert(0, visit_time)
#         # 取出IP的时间列表
#         ip_lst = visit_ip_pool[ip]
#         # 第一次访问时间与最后访问时间的差值
#         timecha = ip_lst[0] - ip_lst[-1]
#         print('BEFORE:', ip, '访问次数:', len(ip_lst), '时间差', timecha)
#         # 如果列表没有值,pop()会报错
#         # IndexError: pop from empty list
#         while ip_lst and timecha > 30:
#             # 如果差值大于30秒,删除列表中最后的访问时间,就是最早的访问时间
#             ip_lst.pop()
#         #  差值小于30秒,且访问次数大于20次就提示
#         if timecha<30 and len(ip_lst) > 20:
#             return HttpResponse("访问过于频繁...")
#         print('BEFORE:', ip, '访问次数:', len(ip_lst), '时间差', timecha)


import time
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
# 访问IP池
visit_ip_pool = {}
class RequestBlockingMiddleware(MiddlewareMixin):
    def process_request(self,request):
        # 获取访问者IP
        ip=request.META.get("REMOTE_ADDR")
        # 获取访问当前时间
        visit_time=time.time()
        # 判断如果访问IP不在池中,就将访问的ip时间插入到对应ip的key值列表,如{"127.0.0.1":[时间1]}
        if ip not in visit_ip_pool:
            visit_ip_pool[ip]=[visit_time]
            return None
        # 然后在从池中取出时间列表
        history_time = visit_ip_pool.get(ip)
        # 循环判断当前ip的时间列表，有值，并且当前时间减去列表的最后一个时间大于60s，把这种数据pop掉，这样列表中只有60s以内的访问时间，
        while history_time and visit_time-history_time[-1]>60:
            history_time.pop()
        # 如果访问次数小于10次就将访问的ip时间插入到对应ip的key值列表的第一位置,如{"127.0.0.1":[时间2,时间1]}
        print(history_time)
        if len(history_time)<30:
            history_time.insert(0, visit_time)
            return None
        else:
            # 如果大于10次就禁止访问
            return HttpResponse("访问过于频繁,还需等待%s秒才能继续访问"%int(60-(visit_time-history_time[-1])))


