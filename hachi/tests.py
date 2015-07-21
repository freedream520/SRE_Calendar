# -*- coding: utf-8 -*-
from django.test import TestCase
from hachi.models import *
from hachi.time_bill import *
import datetime

class CalendarTestCase(TestCase):
    """TimeBill的测试
    """
    def setUp(self):
        """拿一个遥远的日子来测试 2015-06-00
        """
        # 插入Product
        for n in range(1, 6):
            product = Product(id=n, name="product_%d" % n)
            product.save()

        # 插入Operation
        for n in range(1, 6):
            operation = Operation(id=n, name="operation_%d" % n)
            operation.save()

        # 插入Event
        calendar_event = CalendarEvent()
        calendar_event.name = '测试1'
        calendar_event.product_id = 1
        calendar_event.operation_id = 1
        calendar_event.username = 'chenhuan'
        calendar_event.start_time = datetime.datetime.strptime("2015-05-26 01:00:00", '%Y-%m-%d %H:%M:%S')
        calendar_event.end_time = datetime.datetime.strptime('2015-05-26 02:30:00', '%Y-%m-%d %H:%M:%S')
        calendar_event.save()

        calendar_event = CalendarEvent()
        calendar_event.name = '测试2'
        calendar_event.product_id = 1
        calendar_event.operation_id = 2
        calendar_event.username = 'chenhuan'
        calendar_event.start_time = datetime.datetime.strptime("2015-06-01 01:00:00", '%Y-%m-%d %H:%M:%S')
        calendar_event.end_time = datetime.datetime.strptime('2015-06-01 02:00:00', '%Y-%m-%d %H:%M:%S')
        calendar_event.save()

        calendar_event = CalendarEvent()
        calendar_event.name = '测试2'
        calendar_event.product_id = 1
        calendar_event.operation_id = 2
        calendar_event.username = 'chenhuan'
        calendar_event.start_time = datetime.datetime.strptime("2015-06-06 01:00:00", '%Y-%m-%d %H:%M:%S')
        calendar_event.end_time = datetime.datetime.strptime('2015-06-06 02:00:00', '%Y-%m-%d %H:%M:%S')
        calendar_event.save()

        calendar_event = CalendarEvent()
        calendar_event.name = '测试3'
        calendar_event.product_id = 1
        calendar_event.operation_id = 4
        calendar_event.username = 'chenhuan'
        calendar_event.start_time = datetime.datetime.strptime("2015-06-11 01:00:00", '%Y-%m-%d %H:%M:%S')
        calendar_event.end_time = datetime.datetime.strptime('2015-06-11 02:00:00', '%Y-%m-%d %H:%M:%S')
        calendar_event.save()

        calendar_event = CalendarEvent()
        calendar_event.name = '测试4'
        calendar_event.product_id = 1
        calendar_event.operation_id = 5
        calendar_event.username = 'chenhuan'
        calendar_event.start_time = datetime.datetime.strptime("2015-06-16 01:00:00", '%Y-%m-%d %H:%M:%S')
        calendar_event.end_time = datetime.datetime.strptime('2015-06-16 02:00:00', '%Y-%m-%d %H:%M:%S')
        calendar_event.save()

    def test_insert_product(self):
        """测试插入product是否成功
        """
        product = Product.objects.all()
        count = len(product)
        self.assertEqual(count, 5)

    def test_insert_operation(self):
        """测试插入Operation是否成功
        """
        operation = Operation.objects.all()
        count = len(operation)
        self.assertEqual(count, 5)

    def test_insert_calendarevnet(self):
        """测试插入CalendarEvent是否成功
        """
        calendar_events = CalendarEvent.objects.all()
        count = len(calendar_events)
        self.assertEqual(count, 5)

    def test_get_product_operation_total_time(self):
        """测试CalendarEvetnManager.get_product_operation_total_time()
        """
        total_time = CalendarEvent.objects.get_product_operation_total_time(1, 
            1, "2015-05-20 00:00:00", "2015-06-15 00:00:00")
        self.assertEqual(total_time, 1.5)

        total_time = CalendarEvent.objects.get_product_operation_total_time(1, 
            2, "2015-05-20 00:00:00", "2015-06-01 00:00:00")
        self.assertEqual(total_time, 0)

        total_time = CalendarEvent.objects.get_product_operation_total_time(2, 
            2, "2015-05-20 00:00:00", "2015-06-15 00:00:00")
        self.assertEqual(total_time, 0)

    def test_get_all_operations_id(self): 
        """测试OperationManager.test_get_all_operations_id()
        """
        all_operations_id = Operation.objects.get_all_operations_id()
        self.assertEqual(all_operations_id, [1, 2, 3, 4, 5])

    def test_get_product_time_bill(self):
        """测试TimeBill.get_product_time_bill(product)函数
        """
        result = {
            '1': [1.5, 0, 0, 0, 0],
            '2': [0, 1, 1, 0, 0],
            '3': [0, 0, 0, 0, 0],
            '4': [0, 0, 0, 1, 0],
            '5': [0, 0, 0, 0, 1],
        }
        time_bill = TimeBill('2015-05-20', 5)
        self.assertEqual(time_bill.get_product_time_bill(1), result)



