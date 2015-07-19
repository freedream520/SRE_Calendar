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

def time_bill(request):
    """展示时间统计表
    """
    if request.method == 'GET':
        try:
            return render_to_response('time_bill.html')
        except Exception as e: 
            return HttpResponse(returnJson(False, "%s in time_bill" % (e)))
    else : 
        return HttpResponse(returnJson(False, "Request's method is not GET in time_bill"))

def test(request):
    time_bill = TimeBill('2015-07-21', 10)
    return HttpResponse(json.dumps(time_bill.get_product_time_bill(1)))

