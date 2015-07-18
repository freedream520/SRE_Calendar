#-*- coding: utf-8 -*-
"""
该模块用于生成highchart统计所需要的各种数据

Authors: chenhuan(chenhuan0102@126.com)
Date:    2015/07/18 22:15:00
"""
import datetime
from hachi.models import *

class TimeBill:
    """Time Bill用于生成Highchart所需的数据

    Attributes:
        begin_date: 展示的第一天
        count: 展示的总周数
    """

    def __init__(self, begin_date, count):
        """初始化函数

        Args:
            begin_date: 开始展示的第一天
            count: 展示的周数
            weeklist: 展示每周的时间段
        """
        self.begin_date = begin_date
        self.count = count
        self.weeklist = self.__create_week_list()

    def __create_week_list(self):
        """ 生成从begin_date开始连续周的列表

        Args:
            begin_date: String类型, 例如: '2015-07-20'
            count: 生成周的个数

        Returns: 
            List类型, 从大于等于begin_date的第一个周一开始
            例如:

            [
                {'begin':'2015-07-20','end':'2015-07-26'},
                {'begin':'2015-07-27','end':'2015-08-02'},
                ...
            ]
        """
        # 获取比begin_date大的第一个周一
        begin_date = datetime.datetime.strptime(self.begin_date, "%Y-%m-%d")
        weekday = begin_date.weekday()
        if weekday != 0:
            begin_date = begin_date + datetime.timedelta(days=(7 - weekday))

        weeklist = []
        # str to datetime.datetime
        count = self.count
        while count != 0:
            end_date = begin_date + datetime.timedelta(days=4)
            weeklist.append({
                # datetime.datetime to str
                'start' : datetime.datetime.strftime(begin_date, '%Y-%m-%d %H:%M:%S'),
                'end' : datetime.datetime.strftime(end_date, '%Y-%m-%d %H:%M:%S'),
            })
            begin_date = end_date + datetime.timedelta(days=1)
            count -= 1
        return weeklist
    
    def get_product_time_bill(self, product_id):
        """获取product的timeBill

        Args:
            product_id: int类似 Product ID

        Returns: 
            product_time_bill: 数据

            例子：
            [
                {'扩容ID' : [1, 2, 3, 4, 5...]},
                {'搭建ID' : [1, 2, 3, 4, 5...]},
                {'学习ID' : [1, 2, 3, 4, 5...]},
                ...

            ]     
        """
        # 获取全部operations ID
        all_operations_id = Operation.objects.get_all_operations_id()

        product_time_bill = [] 
        for operation_id in all_operations_id:
            total_times = []
            for week in self.weeklist:
                total_time = CalendarEvent.objects.get_event_time(product_id, 
                    operation_id, week['start'], end['end'])
                total_times.append(total_time) 
            product_time_bill.append({str(operation_id) : total_times}) 

        return product_time_bill 









