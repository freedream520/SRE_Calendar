# -*- coding: utf-8 -*-
from django.db import models
from django.db import connection
import datetime

# Create your models here.
class ProductManager(models.Manager):
    """ProductManager
    """

    def get_all_products_id(self):
        """返回所有Product的ID

        Returns:
            all_products_id: 列表
        """
        all_products = Product.objects.all()

        all_products_id = []
        for product in all_products:
            all_products_id.append(product.id)

        return all_products_id 

class Product(models.Model):
    """Product产品线
    """
    name = models.CharField(max_length=255)
    objects = ProductManager()

    def __unicode__(self):
        return self.name

class OperationManager(models.Manager):
    """Operartion的Manager
    """

    def get_all_operations_id(self):
        """返回所有Operation的ID

        Returns: 
            all_operations_id: 列表
        """
        all_operations = super(OperationManager, self).all()

        all_operations_id = []
        for operation in all_operations:
            all_operations_id.append(operation.id)

        return all_operations_id

class Operation(models.Model):
    """操作类型
    """
    name = models.CharField(max_length=255)
    objects = OperationManager()

    def __unicode__(self):
        return self.name

class CalendarEventManager(models.Manager):
    """CalendarEvent的Manager
    """

    def get_events_by_time(self, start_time, end_time):
        """返回start_time和end_time之间的全部events

        Args:
            start_time: string 例子: 2015-07-18
            end_time: string 例子: 2015-07-19

        Returns:
            calendar_events: 列表
            例子:
            [
                {
                    'id':1, 
                    'title':'扩容', 
                    'start':'2015-07-18 00:00:00', 
                    'end':'2015-07-18 01:00:00'
                },
                ...
            ]
        """
        start_time = "%s 00:00:00" % (start_time)
        end_time = "%s 00:00:00" % (end_time)

        cursor = connection.cursor()
        sql = 'SELECT id,name,start_time,end_time,description FROM hachi_calendarevent WHERE start_time >= "%s" AND end_time <= "%s"; ' % (start_time, end_time)

        cursor.execute(sql)
        calendar_events = []
        for row in cursor.fetchall():
            start_time = row[2].strftime("%Y-%m-%d %H:%M:%S")
            end_time = row[3].strftime("%Y-%m-%d %H:%M:%S")
            calendar_event = {
                'id' : row[0],
                'title' : row[1],
                'start' : start_time,
                'end' : end_time,
            }
            calendar_events.append(calendar_event)
            
        return calendar_events() 

    def get_product_operation_total_time(self, product_id, operation_id, start_time, end_time):
        """返回product在start_time和end_time时间段内，operation类型操作占用总时间

        Args: 
            product_id: int类型
            operation_id: int类型
            start_time: string类型, 例子: "2015-07-19 00:00:00"
            end_time: string类型, 例子: "2015-07-19 02:00:00"

        Returns:
            float类型: 2.5小时
        """
        cursor = connection.cursor()
        sql = 'SELECT start_time,end_time FROM hachi_calendarevent WHERE product_id = %d AND operation_id = %d AND start_time >= "%s" AND end_time <= "%s"; ' % (product_id, operation_id, start_time, end_time)

        cursor.execute(sql)
        total_time =  datetime.timedelta(0)
        for row in cursor.fetchall():
            start_time = row[0]
            end_time = row[1]
            total_time += end_time - start_time

        if total_time.total_seconds() == 0:
            return 0.1
        else: 
            return total_time.total_seconds()/3600

    def get_operation_total_time(self, operation_id, start_time, end_time):
        """返回operation在start_time和end_time之间的总书剑

        Args: 
            operation_id: int类型
            start_time: string类型, 例子: "2015-07-19 00:00:00"
            end_time: string类型, 例子: "2015-07-19 02:00:00"

        Returns:
            float类型: 2.5小时
        """
        cursor = connection.cursor()
        sql = 'SELECT start_time,end_time FROM hachi_calendarevent WHERE operation_id = %d AND start_time >= "%s" AND end_time <= "%s"; ' % (operation_id, start_time, end_time)

        cursor.execute(sql)
        total_time =  datetime.timedelta(0)
        for row in cursor.fetchall():
            start_time = row[0]
            end_time = row[1]
            total_time += end_time - start_time

        if total_time.total_seconds() == 0:
            return 0.1
        else: 
            return total_time.total_seconds()/3600
       
class CalendarEvent(models.Model):
    """CalendarEvent
    """
    name = models.CharField(max_length=255)
    product = models.ForeignKey(Product)
    operation = models.ForeignKey(Operation)
    description = models.TextField(max_length=255)
    username = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    objects = CalendarEventManager()

    def __unicode__(self):
        return self.name
