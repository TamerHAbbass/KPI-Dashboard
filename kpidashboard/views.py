from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse, Http404
import pyodbc
import datetime
import json
import threading
from .form import CustomReportRange
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .Util import ParseData, DataBase
from .secure_data import server, database, username, password


def agent(request):
    
    agent_data = {}
    user = request.user
    days = 1
    
    D = DataBase(request)
    D.connectToDatabase(server, database, username, password)
    D.getAfterCallWorkTime(user, days)
    D.getInteractionData(user, days)
    D.getStatusData(user, days)
    D.getTalkTIme(user, days)
    D.getAnswerSpeedTime(user, days)
    D.getNumberQueueInteractions(user, days)
    D.getNumberAnsweredQueuedInteractions(user, days)
    D.getAgentCallbackData(user, days)
    D.getAgentStatusData(user, days)
    D.getCallbackData(days)
    D.convertTimeUnit()
    P = ParseData()
    P.interaction = D.Interaction_Data
    P.status = D.Status_Data
    P.parseStatusData()
    P.parseInteractionData()
    D.Interaction_Data = P.interaction
    D.Status_Data = P.status
    D.Status_Stats = P.StatusCheck()
    D.getAgentPercentageValues()

    agent_data = D.__dict__()


    context = {
        "data": {
            'agent': agent_data
        }
    }

    D.closeDataBaseConnection()
    
    return render(request, context=context, template_name="kpidashboard/viewagent.html")


def department_load(request):

    if request.method == 'GET':
        dept_data = {}
        agent_data = {}
        user = request.user
        days = 1

        D = DataBase(request)
        D.connectToDatabase(server, database, username, password)
        D.getWorkgroups()
        D.getInteractionData(user, days)
        D.getWorkgroupStatusData()
        D.getNumberWorkgroupInteractions(days)
        D.getNumberConnectedWorkgroupInteractions(days)
        D.getWorkgroupTalkStats(days)
        D.getOrgStatusData(days)
        D.getWorkgroupHoldStats(days)
        D.getWorkgroupsAfterCallWorkTime(days)
        D.getWorkgroupStatusTitle()
        # D.getWorkgroupStatusTimes(days)
        D.getWorkgroupAnswerSpeedTime(days)
        D.getPercentageValues()
        D.convertTimeUnit()
        


        D1 = DataBase(request)
        D1.connectToDatabase(server, database, username, password)
        D1.getAfterCallWorkTime(user, days)
        D1.getInteractionData(user, days)
        D1.getStatusData(user, days)
        D1.getTalkTIme(user, days)
        D1.getAnswerSpeedTime(user, days)
        D1.getNumberQueueInteractions(user, days)
        D1.getNumberAnsweredQueuedInteractions(user, days)
        D1.getAgentCallbackData(user, days)
        D1.getCallbackData(days)
        D1.getAgentStatusData(user, days)
        D1.convertTimeUnit()
        P1 = ParseData()
        P1.interaction = D1.Interaction_Data
        P1.status = D1.Status_Data
        P1.parseStatusData()
        P1.parseInteractionData()
        D1.Interaction_Data = P1.interaction
        D1.Status_Data = P1.status
        D1.Status_Stats = P1.StatusCheck()
        D1.getAgentPercentageValues()

        dept_data = D.__dict__()
        agent_data = D1.__dict__()


        context = {
            "data": {
                'agent': agent_data,
                'dept': dept_data
            }
        }

        D.closeDataBaseConnection()
        D1.closeDataBaseConnection()

    

    return render(request, context=context, template_name="kpidashboard/viewdepartment_load.html")

def department(request):

    if request.method == 'GET':
        
        dept_data = {}
        agent_data = {}
        user = request.user
        days = 1

        D = DataBase(request)
        D.connectToDatabase(server, database, username, password)
        D.getWorkgroups()
        D.getInteractionData(user, days)
        D.getWorkgroupStatusData()
        D.getNumberWorkgroupInteractions(days)
        D.getNumberConnectedWorkgroupInteractions(days)
        D.getWorkgroupTalkStats(days)
        D.getOrgStatusData(days)
        D.getWorkgroupHoldStats(days)
        D.getWorkgroupsAfterCallWorkTime(days)
        D.getWorkgroupStatusTitle()
        D.getWorkgroupStatusTimes(days)
        D.getWorkgroupAnswerSpeedTime(days)
        D.getPercentageValues()
        D.convertTimeUnit()
        

        D1 = DataBase(request)
        D1.connectToDatabase(server, database, username, password)
        D1.getAfterCallWorkTime(user, days)
        D1.getInteractionData(user, days)
        D1.getStatusData(user, days)
        D1.getTalkTIme(user, days)
        D1.getAnswerSpeedTime(user, days)
        D1.getNumberQueueInteractions(user, days)
        D1.getNumberAnsweredQueuedInteractions(user, days)
        D1.getAgentCallbackData(user, days)
        D1.getCallbackData(days)
        D1.getAgentStatusData(user, days)
        D1.convertTimeUnit()
        P1 = ParseData()
        P1.interaction = D1.Interaction_Data
        P1.status = D1.Status_Data
        P1.parseStatusData()
        P1.parseInteractionData()
        D1.Interaction_Data = P1.interaction
        D1.Status_Data = P1.status
        D1.Status_Stats = P1.StatusCheck()
        D1.getAgentPercentageValues()

        dept_data = D.__dict__()
        agent_data = D1.__dict__()


        context = {
            "data": {
                'agent': agent_data,
                'dept': dept_data
            }
        }

        D.closeDataBaseConnection()
        D1.closeDataBaseConnection()
    
    elif request.method == 'POST':
        dept_data = {}
        agent_data = {}
        days = 1
        user = ''
        date = ''

        if request.POST['data']:
            user = request.POST['data']
        else:
            user = request.user
        
        if request.POST['daterange']:
            date = request.POST['daterange']
        

        

        D = DataBase(request)

        
        D.getDate(date)
        D.connectToDatabase(server, database, username, password)
        D.getWorkgroups()
        D.getInteractionData(user, days)
        D.getWorkgroupStatusData()
        D.getOrgStatusData(days)
        D.getNumberWorkgroupInteractions(days)
        D.getNumberConnectedWorkgroupInteractions(days)
        D.getWorkgroupTalkStats(days)
        D.getWorkgroupHoldStats(days)
        D.getWorkgroupsAfterCallWorkTime(days)
        D.getWorkgroupStatusTitle()
        D.getWorkgroupStatusTimes(days)
        D.getWorkgroupAnswerSpeedTime(days)
        D.getConnectedWorkgroupCallbackData(days)
        D.getWorkgroupCallbackData(days)
        D.getPercentageValues()
        D.convertTimeUnit()


        D1 = DataBase(request)
        D1.getDate(date)
        D1.connectToDatabase(server, database, username, password)
        D1.getAfterCallWorkTime(user, days)
        D1.getInteractionData(user, days)
        D1.getStatusData(user, days)
        D1.getTalkTIme(user, days)
        D1.getAnswerSpeedTime(user, days)
        D1.getNumberQueueInteractions(user, days)
        D1.getNumberAnsweredQueuedInteractions(user, days)
        D1.getAgentCallbackData(user, days)
        D1.getCallbackData(days)
        D1.getAgentStatusData(user, days)
        D1.convertTimeUnit()
        P1 = ParseData()
        P1.interaction = D1.Interaction_Data
        P1.status = D1.Status_Data
        P1.parseStatusData()
        P1.parseInteractionData()
        D1.Interaction_Data = P1.interaction
        D1.Status_Data = P1.status
        D1.Status_Stats = P1.StatusCheck()
        D1.getAgentPercentageValues()


        dept_data = D.__dict__()
        agent_data = D1.__dict__()


        context = {
            "data": {
                'agent': agent_data,
                'dept': dept_data
            }
        }

        D.closeDataBaseConnection()
        D1.closeDataBaseConnection()

    return render(request, context=context, template_name="kpidashboard/viewdepartment.html")


    
def department_historical(request):
    print(dir(request))
    form = CustomReportRange()
    return render(request, context={'form':form}, template_name="kpidashboard/viewdepartment.html")


