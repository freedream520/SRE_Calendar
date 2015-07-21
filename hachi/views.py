# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.utils import timezone
from hachi.common import *
from hachi.models import *
from hachi.forms import CalendarEventForm
import json, datetime
from time_bill import TimeBill

# Create your views here.
def full_calendar(request):
    """显示日程表
    """
    calendar_event_form = CalendarEventForm()
    return render_to_response('full_calendar.html',
        {'calendar_event_form':calendar_event_form},
    )

def create_event(request):
    """读取HTTP请求, 创建Event

    Returns:
        返回Json格式{
            'success' : true,
            'message' : '错误信息',
            'data' : {数据信息}
        }
    """
    if request.method == 'GET':
        try:
            calendar_event_form = CalendarEventForm(request.GET)
            if calendar_event_form.is_valid():
                calendar_event = calendar_event_form.save(commit=False)
                calendar_event.start_time = str(calendar_event.start_time).split('+')[0]
                calendar_event.end_time = str(calendar_event.end_time).split('+')[0]
                calendar_event.save()
                return HttpResponse(returnJson(True))
            else:
                raise Exception(calendar_event_form.errors)
        except Exception as e: 
            return HttpResponse(returnJson(False, "%s in create_event" % (e)))
    else:
        return HttpResponse(returnJson(False, "Request's method is not GET in create_event"))


def get_events(request):
    """获取start和end时间段内的全部Events

    Returns:
        返回Json格式的Events

        例子:
        [
            {
                'id' : 1,
                'title' : '搭建集群',
                'start' : '2015-07-19 10:12:00',
                'end' : '2015-07-19 10:30:00',
            },
            ....
        ]
    """
    if request.method == 'GET':
        start_time = request.GET['start']
        end_time = request.GET['end']
        try :
            calendar_events = CalendarEvent.objects.get_events_by_time(start_time, end_time)
            return HttpResponse(json.dumps(calendar_events))
        except Exception as e: 
            return HttpResponse(returnJson(False, "%s in get_events" % (e)))

def get_event_description(request):
    """返回event的description

    Returns:
        返回Json格式的description

        例子:
        {
            'success' : True,
            'message' : '',
            'data' : {
                'description' : '请使用如下机器:XXXX',
            }
        }
    """
    if request.method == 'GET':
        try:
            id = int(request.GET['id'])
            calendar_event = CalendarEvent.objects.get(id=id)
            return HttpResponse(returnJson(True, '', {
                'eventDescription' : calendar_event.description,
            }))
        except Exception as e :
            return HttpResponse(returnJson(False, "%s in get_event_description" % (e)))
    else : 
        return HttpResponse(returnJson(False, "Request's method is not GET in get_event_description"))

def product_time_bill(request):
    """展示Product的时间统计表
    """
    if request.method == 'GET':
        try:
            product_id = int(request.GET['id'])
            time_bill = TimeBill('2015-05-20', 5)
            weeklist = time_bill.get_weeklist()
            product_time_bill = time_bill.get_product_time_bill(product_id)
            product_average_time_bill = TimeBill.get_average_time_bill(product_time_bill)
            operation_total_time_list = TimeBill.get_operation_total_time_list(product_time_bill)

            return render_to_response('product_time_bill.html', {
                'weeklist' : weeklist, 
                'product_time_bill' : product_time_bill,
                'product_average_time_bill' : product_average_time_bill,
                'operation_total_time_list' : operation_total_time_list,
            })
        except Exception as e: 
            return HttpResponse(returnJson(False, "%s in product_time_bill" % (e)))
    else : 
        return HttpResponse(returnJson(False, "Request's method is not GET in product_time_bill"))

def time_bill(request):
    """展示Product的时间统计表
    """
    try:
        time_bill = TimeBill('2015-05-20', 5)
        weeklist = time_bill.get_weeklist()

        # 获取各产品线的time_bill
        all_products_time_bill = {}
        all_products_id = Product.objects.get_all_products_id()
        for product_id in all_products_id:
            product_name = Product.objects.get(id=product_id).name
            product_time_bill = time_bill.get_product_time_bill(product_id)
            product_average_time_bill = TimeBill.get_average_time_bill(product_time_bill)
            operation_total_time_list = TimeBill.get_operation_total_time_list(product_time_bill)

            all_products_time_bill[product_name] = {
                'product_time_bill' : product_time_bill,
                'product_average_time_bill' : product_average_time_bill,
                'operation_total_time_list' : operation_total_time_list,
            }

        # 获取各Operation总的time_bill 
        all_operation_time_bill = {}
        all_operations_id = Operation.objects.get_all_operations_id()
        for operation_id in all_operations_id:
            operation_time_bill = time_bill.get_operation_time_bill(operation_id)
            all_operation_time_bill[Operation.objects.get(id=operation_id).name] = operation_time_bill

        operation_average_time_bill = TimeBill.get_average_time_bill(all_operation_time_bill)
        operation_total_time_list = TimeBill.get_operation_total_time_list(all_operation_time_bill)

        all_products_time_bill['操作'] = {
            'product_time_bill' : all_operation_time_bill,
            'product_average_time_bill' : operation_average_time_bill,
            'operation_total_time_list' : operation_total_time_list,
        }

        # return HttpResponse(json.dumps(all_operation_time_bill)) 
        # return HttpResponse(json.dumps(all_products_time_bill))
        return render_to_response('time_bill.html', {
            'weeklist' : weeklist, 
            'all_products_time_bill' : all_products_time_bill, 
        })
    except Exception as e: 
        return HttpResponse(returnJson(False, "%s in time_bill" % (e)))

def time_bill_by_echart(request):
    """展示Product的时间统计表
    """
    try:
        time_bill = TimeBill('2015-05-20', 5)
        weeklist = time_bill.get_weeklist()

        # 获取各产品线的time_bill
        all_products_time_bill = {}
        all_products_id = Product.objects.get_all_products_id()
        for product_id in all_products_id:
            product_name = Product.objects.get(id=product_id).name
            product_time_bill = time_bill.get_product_time_bill(product_id)
            product_average_time_bill = TimeBill.get_average_time_bill(product_time_bill)
            operation_total_time_list = TimeBill.get_operation_total_time_list(product_time_bill)

            all_products_time_bill[product_name] = {
                'product_time_bill' : product_time_bill,
                'product_average_time_bill' : product_average_time_bill,
                'operation_total_time_list' : operation_total_time_list,
            }

        # 获取各Operation总的time_bill 
        all_operation_time_bill = {}
        all_operations_id = Operation.objects.get_all_operations_id()
        for operation_id in all_operations_id:
            operation_time_bill = time_bill.get_operation_time_bill(operation_id)
            all_operation_time_bill[Operation.objects.get(id=operation_id).name] = operation_time_bill

        operation_average_time_bill = TimeBill.get_average_time_bill(all_operation_time_bill)
        operation_total_time_list = TimeBill.get_operation_total_time_list(all_operation_time_bill)

        all_products_time_bill['操作'] = {
            'product_time_bill' : all_operation_time_bill,
            'product_average_time_bill' : operation_average_time_bill,
            'operation_total_time_list' : operation_total_time_list,
        }

        all_operations_name = json.dumps(Operation.objects.get_all_operations_name(), ensure_ascii=False)

        # return HttpResponse(all_operations_name) 
        # return HttpResponse(json.dumps(all_operations_name, ensure_ascii=False))
        # return HttpResponse(json.dumps(all_operation_time_bill)) 
        # return HttpResponse(json.dumps(all_products_time_bill))
        return render_to_response('time_bill_by_echart.html', {
            'weeklist' : weeklist, 
            'all_operations_name' : all_operations_name,
            'all_products_time_bill' : all_products_time_bill, 
        })
    except Exception as e: 
        return HttpResponse(returnJson(False, "%s in time_bill" % (e)))

def test(request):
    """各种测试函数
    """
    """
    for product_id in range(2, 6):
        calendar_event = CalendarEvent()
        calendar_event.name = '测试1'
        calendar_event.product_id = product_id
        calendar_event.operation_id = 6
        calendar_event.username = 'chenhuan'
        calendar_event.start_time = datetime.datetime.strptime("2015-05-26 01:00:00", '%Y-%m-%d %H:%M:%S')
        calendar_event.end_time = datetime.datetime.strptime('2015-05-26 02:30:00', '%Y-%m-%d %H:%M:%S')
        calendar_event.save()

        calendar_event = CalendarEvent()
        calendar_event.name = '测试2'
        calendar_event.product_id = product_id
        calendar_event.operation_id = 2
        calendar_event.username = 'chenhuan'
        calendar_event.start_time = datetime.datetime.strptime("2015-06-01 01:00:00", '%Y-%m-%d %H:%M:%S')
        calendar_event.end_time = datetime.datetime.strptime('2015-06-01 02:00:00', '%Y-%m-%d %H:%M:%S')
        calendar_event.save()

        calendar_event = CalendarEvent()
        calendar_event.name = '测试2'
        calendar_event.product_id = product_id
        calendar_event.operation_id = 1
        calendar_event.username = 'chenhuan'
        calendar_event.start_time = datetime.datetime.strptime("2015-06-06 01:00:00", '%Y-%m-%d %H:%M:%S')
        calendar_event.end_time = datetime.datetime.strptime('2015-06-06 02:00:00', '%Y-%m-%d %H:%M:%S')
        calendar_event.save()

        calendar_event = CalendarEvent()
        calendar_event.name = '测试3'
        calendar_event.product_id = product_id
        calendar_event.operation_id = 3
        calendar_event.username = 'chenhuan'
        calendar_event.start_time = datetime.datetime.strptime("2015-06-11 01:00:00", '%Y-%m-%d %H:%M:%S')
        calendar_event.end_time = datetime.datetime.strptime('2015-06-11 02:00:00', '%Y-%m-%d %H:%M:%S')
        calendar_event.save()

        calendar_event = CalendarEvent()
        calendar_event.name = '测试4'
        calendar_event.product_id = product_id
        calendar_event.operation_id = 4
        calendar_event.username = 'chenhuan'
        calendar_event.start_time = datetime.datetime.strptime("2015-06-16 04:00:00", '%Y-%m-%d %H:%M:%S')
        calendar_event.end_time = datetime.datetime.strptime('2015-06-16 06:00:00', '%Y-%m-%d %H:%M:%S')
        calendar_event.save()
    time_bill = TimeBill('2015-05-20', 5)
    product_time_bill = time_bill.get_product_time_bill(1)
    average_time_bill = TimeBill.get_average_time_bill(product_time_bill)
    operation_total_time_list = TimeBill.get_operation_total_time_list(product_time_bill)
    # return HttpResponse(json.dumps(time_bill.get_weeklist()))
    # return HttpResponse(json.dumps(average_time_bill))
    return HttpResponse(json.dumps(operation_total_time_list))
    """
    # return HttpResponse(json.dumps(['陈欢', '姜虹']))
