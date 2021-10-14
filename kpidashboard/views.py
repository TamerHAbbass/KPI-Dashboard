from django.shortcuts import render
from django.http import HttpResponse

data = [
    True, 'MCSS Nav Patient', 'MCSS Nav Callbacks',
     'MCSS Nav Nurse', 'MCSS Nav MCH', 'MCSS Nav MyChart',

    ]


agent_data = {
    "agent" : "Hector Salamanca",
    "executive" : "False",
    "talk_time" : {
        "total_talk_time": "05:34:01",
        "average_talk_time": "00:24:00"
    },
    "hold_time" : {
        "total_hold_time": "05:34:01",
        "average_hold_time": "00:24:00"
    },
    "after_call_work_time" : {
        "total_after_call_work_time" : "05:34:01",
        "average_after_call_work_time": "00:24:00"
    },
    "answered" : {
        "calls": "15/16",
        "callbacks": "7/9",
        "missed_calls": "1/34"
    },
    "average_speed_to_answer_calls" : {
        "last_call": "00:07",
        "all Calls": "00:15",
    },
    "minutes_in_each_status": {
        "Available" : 80,
        "Available, No ACD" : 5,
        "Lunch" : 60,
        "At a trai" : 0,
        "Additiona" : 18,
        "Out of Of" : 0,
        "ACD – Age" : 54
    }
}

# Create your views here.
def kpidashboard(request):
    context={
        "agent_data" : agent_data
    }
    return render(request,context=context,
        template_name="kpidashboard/dashboard.html",
        )

def kpidepartmentdashboard(request):
    context={
        'data':data,
    }
    return render(request, context=context,
        template_name="kpidashboard/departmentstatus.html",
    )

def agent(request):
    context={
        'data':data,
    }
    return render(request, context=context,
    template_name="kpidashboard/viewagent.html")


def department(request):
    context={
        'data':data,
    }
    return render(request, context=context,
    template_name="kpidashboard/viewdepartment.html")