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
                {'扩容' : [1, 2, 3, 4, 5...]},
                {'搭建' : [1, 2, 3, 4, 5...]},
                {'学习' : [1, 2, 3, 4, 5...]},
                ...
            ]     
        """
        all_operations_id = Operation.objects.get_all_operations_id()
        product_time_bill = {}
        for operation_id in all_operations_id:
            total_times = []
            for week in self.weeklist:
                total_time = CalendarEvent.objects.get_product_operation_total_time(product_id, operation_id, week['start'], week['end'])
                total_times.append(total_time) 
            product_time_bill[Operation.objects.get(id=operation_id).name] = total_times

        return product_time_bill 

    def get_operation_time_bill(self, operation_id):
        """返回weeklist段内各操作的用时

        Args:
            operation_id: int类似 Operation ID

        Returns: 
            operation_time_bill: 数据

            例子：
            {'扩容' : [1, 2, 3, 4, 5...]},
        """
        time_bill = []
        for week in self.weeklist:
            total_time = CalendarEvent.objects.get_operation_total_time(operation_id, week['start'], week['end'])
            time_bill.append(total_time)

        return time_bill

    def __translate_date(self, date):
        """将2015-07-19转成7月19

        Args:
            date: String类型, 例子: '2015-07-19'

        Returns:
            字符串 例子: '7月19'
        """
        # month = date.split('-')[1].strip('0')
        month = date.split('-')[1]
        day = date.split('-')[2]

        return "%s%s" % (month, day)

    def get_weeklist(self):
        """返回供highchart展示的weeklist

        Returns: 
            weeklist: 列表

            例子:['6月22-6月26', '6月29-7月03', '7月06-7月10', '7月13-7月17', '7月20-7月24', '7月27-7月31']
        """
        new_weeklist = []
        for time_zone in self.weeklist:
            # 将2015-07-19 00:00:00转成7月19
            start_time = self.__translate_date(time_zone['start'].split(' ')[0])
            end_time = self.__translate_date(time_zone['end'].split(' ')[0])
            new_weeklist.append("%s~%s" % (start_time, end_time))
        return new_weeklist 

    @staticmethod
    def get_average_time_bill(product_time_bill):
        """返回product_time_bill的平均time_bill

        Args:
            product_time_bill

            例子:
            {
                'DStream' : [1, 2, 3, 4, 5, 6],
                'Bigpipe' : [1, 2, 3, 4, 5, 6],
                'TM' : [1, 2, 3, 4, 5, 6],
                ......

            }

        Returns: 
            average_time_bill

            例子:
            [1, 2, 3, 4, 5, 6]
        """
        length = 0
        for operation,time_bill in product_time_bill.items():
            length = len(time_bill) 
            break

        average_time_bill = []
        for n in range(length):
            total_time = 0
            for operation,time_bill in product_time_bill.items():
                total_time += time_bill[n]
            average_time_bill.append(int(total_time))

        return average_time_bill

    @staticmethod
    def get_operation_total_time_list(product_time_bill):
        """返回product_time_bill每种operation总时间

        Args:
            product_time_bill

            例子:
            {
                'DStream' : [1, 2, 3, 4, 5, 6],
                'Bigpipe' : [1, 2, 3, 4, 5, 6],
                'TM' : [1, 2, 3, 4, 5, 6],
                ......

            }

        Returns: 
            average_time_bill

            例子:
            {
                'DStream' : 21,
                'Bigpipe' : 21,
                'TM' : 21,
                ......

            }
        """
        operation_total_time_list = {} 
        for operation,time_bill in product_time_bill.items():
            total_time = 0
            for time in time_bill:
                total_time += time
            operation_total_time_list[operation]  = total_time

        return operation_total_time_list
