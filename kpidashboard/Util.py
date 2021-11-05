import pyodbc
import time
import datetime


class ParseData:

    def __init__(self):

        self.status = None
        self.interaction = None
    

    def parseStatusData(self):

        stats = {}
        index = 0

        while index <= len(self.status)-1:

            temp = {
                "status": {},
            }

            temp["status"]["UserId"] = self.status[index][0]
            temp["status"]["SatusDateTime"] = self.status[index][1]
            temp["status"]["StatusKey"] = self.status[index][2]
            temp["status"]["EndDateTime"] = self.status[index][3]
            temp["status"]["StateDuration"] = self.status[index][4]

            stats[index] = temp
            index += 1
            
        self.status = stats
        return stats



    def parseInteractionData(self):
        if self.interaction:
            stats = {}
            index = 0
            minutes = (int(self.interaction[-1][9])//1000//60)
            seconds = int((self.interaction[-1][9])//1000%60)

            if len(f"{minutes}:{seconds}") < 6:
                lastCallData = f"0{minutes}:{seconds}"
            else:
                lastCallData = f"{minutes}:{seconds}"

            while index <= len(self.interaction)-1:
                temp = {
                    "interaction": {},
                }

                temp["interaction"]["InteractionIDKey"] = self.interaction[index][0]
                temp["interaction"]["StartDateTimeUTC"] = self.interaction[index][1]
                temp["interaction"]["LastLocalUserId"] = self.interaction[index][2]
                temp["interaction"]["LastAssignedWorkgroupId"] = self.interaction[index][3]
                temp["interaction"]["RemoteNumberCallId"] = self.interaction[index][4]
                temp["interaction"]["RemoteName"] = self.interaction[index][5]
                temp["interaction"]["InitiatedDateTimeUTC"] = self.interaction[index][6]
                temp["interaction"]["ConnectionDateTimeUTC"] = self.interaction[index][7]
                temp["interaction"]["TerminatedDateTimeUTC"] = self.interaction[index][8]
                temp["interaction"]["LineDuration"] = self.interaction[index][9]
                temp["interaction"]["CallEventLog"] = self.interaction[index][10]

                stats[index] = temp
                index += 1
            self.interaction = stats
            stats["lastCallLength"] = lastCallData
        else:
            self.interaction = 0

        return self.interaction


    def StatusCheck(self):
        statusStats = {}
        status = self.status

        for i, j in status.items():
            statusStats[j["status"]["StatusKey"].title()] = {
                "numberTimesEntered": 0,
                "totalTimeInStatus": 0,
            }

        for index, (i, j) in enumerate(status.items()):
    
            statusStats[j["status"]["StatusKey"].title()]["numberTimesEntered"] += 1

            statusStats[j["status"]["StatusKey"].title()]["totalTimeInStatus"] += int(((j["status"]["StateDuration"]/60)))
            statusStats[j["status"]["StatusKey"].title()]["unit"] = "minutes"

        return statusStats

    
    def lastCallDetails(self):
        return self.interaction["lastCallLength"]


class DataBase:

    def __init__(self, request):
        self.userrole = request.user.userrole
        self.Agent = None
        self.date = 0
        self.sqlConnection = 0
        self.TalkTime = 0
        self.AvgTalkTime = 0
        self.Interaction_Data = 0
        self.Status_Data = 0
        self.Org_Status_Data = 0
        self.Agent_Status_Data = {}
        self.Status_Workgroup_Data = 0
        self.Status_Stats = 0
        self.LastCallAnswerSpeed = 0
        self.AverageAnswerSpeed = 0
        self.HoldTime = 0
        self.AvgHoldTime = 0
        self.NumberOfInteractions = 0
        self.AfterCallWorkTime = 0
        self.AvgAfterCallWorkTime = 0
        self.NumberQueuedInteractions = 0
        self.NumberAnsweredQueuedInteractions = 0
        self.NumberAgentCallbacks = 0
        self.NumberCallbacks = 0
        self.NumberMissedQueuedInteractions = 0
        self.WorkgroupList = 0
        self.WorkgroupTalkTime = 0
        self.WorkgroupAvgTalkTime = 0
        self.WorkgroupHoldTime = 0
        self.WorkgroupAvgHoldTime = 0
        self.NumberOfWorkgroupInteractions = 0
        self.NumberOfConnectedWorkgroupInteractions = 0
        self.NumberWorkgroupMissedInteractions = 0
        self.WorkgroupAfterCallWorkTime = 0
        self.WorkgroupAvgAfterCallWorkTime = 0
        self.NumberOfConnectedWorkgroupInteractionsPercentage = 0
        self.NumberWorkgroupMissedInteractionsPercentage = 0
        self.WorkgroupStatusTitle = 0
        self.WorkgroupStatusTimes = [[' ']]
        self.WorkgroupConnectedNumberCallbacks = 0
        self.WorkgroupTotalNumberCallbacks = 0
        self.CallbackPercentage = 0
        self.WorkgroupNumberOfInteractions = 0
        self.WorkgroupLastCallAnswerSpeed = 0
        self.WorkgroupAverageAnswerSpeed = 0
        self.NumberAnsweredQueuedInteractionsPercentage = 0
        self.NumberMissedInteractionsPercentage = 0
        self.AgentCallbackPercentage = 0


    def connectToDatabase(self, server, database, username, password):
        cnxn = pyodbc.connect(f"DSN=IC_Server;UID={username};PWD={password}")
        self.sqlConnection = cnxn.cursor()


    def getDate(self, date):
        self.date = date
        if not date or ' ' == date:
            return datetime.datetime.now().strftime('%m/%d/%Y') 
        else:
            return datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%m/%d/%Y')


    def getInteractionData(self, user, days):
        if self.date and self.date != ' ':
            date = f"LIKE '{self.date}%'"
        else:
            date = f"> (select dateadd(day, -{days}, getdate()))"
        SQL_Agent_Interaction = f"SELECT InteractionIDKey, StartDateTimeUTC, LastLocalUserId, LastAssignedWorkgroupId, RemoteNumberCallId, RemoteName, InitiatedDateTimeUTC, ConnectedDateTimeUTC, TerminatedDateTimeUTC, LineDuration, CallEventLog  FROM InteractionSummary WHERE LastAssignedWorkgroupId IS NOT NULL AND MediaType=0 AND LastLocalUserId='{user}' AND InitiatedDateTimeUTC {date}"
        self.sqlConnection.execute(SQL_Agent_Interaction)
        self.Interaction_Data = self.sqlConnection.fetchall()
        if len(self.Interaction_Data):
            self.NumberOfInteractions = len(self.Interaction_Data)

        SQL_HOLD_TIME = f"SELECT SUM(tHeld), AVG(tHeld)  FROM InteractionSummary WHERE LastLocalUserId='{user}' AND MediaType=0 AND InitiatedDateTimeUTC {date};"
        self.sqlConnection.execute(SQL_HOLD_TIME)
        data = self.sqlConnection.fetchall()
        if data[0][0] != None:
            self.HoldTime = data[0][0]/1000
            self.AvgHoldTime = data[0][1]/1000



    def getAfterCallWorkTime(self, user, days):
        if self.date and self.date != ' ':
            date = f"LIKE '{self.date}%'"
        else:
            date = f"> (select dateadd(day, -{days}, getdate()))"
        
        SQL_Agent_Interaction = f"SELECT SUM(tACW), AVG(tACW) FROM InteractionSummary WHERE LastLocalUserId='{user}' AND StartDateTimeUTC {date}"
        self.sqlConnection.execute(SQL_Agent_Interaction)
        Time = self.sqlConnection.fetchall()[0]
        print(Time)
        if Time[0]:
            self.AfterCallWorkTime = Time[0]/1000
        if Time[1]:
            self.AvgAfterCallWorkTime = Time[1]/1000


    def getWorkgroupsAfterCallWorkTime(self, days):
        if self.date and self.date != ' ':
            date = f"LIKE '{self.date}%'"
        else:
            date = f"> (select dateadd(day, -{days}, getdate()))"

        SQL_Agent_Interaction = f"SELECT SUM(tAcw), AVG(tAcw) FROM IWrkgrpQueueStats WHERE cReportGroup!='*' AND dIntervalStart {date} AND tAcw!=0;"
        self.sqlConnection.execute(SQL_Agent_Interaction)
        data = self.sqlConnection.fetchall()[0]
        self.WorkgroupAfterCallWorkTime = data[0]
        self.WorkgroupAvgAfterCallWorkTime = data[1]


    def getAgentCallbackData(self, user, days):
        if self.date and self.date != ' ':
            date = f"LIKE '{self.date}%'"
        else:
            date = f"> (select dateadd(day, -{days}, getdate()))"
        
        SQL_Agent_Interaction = f"SELECT InteractionType FROM calldetail_viw WHERE InteractionType=6 AND LocalUserId='{user}' AND InitiatedDate {date};"
        self.sqlConnection.execute(SQL_Agent_Interaction)
        callback = self.sqlConnection.fetchall()
        self.NumberAgentCallbacks = len(callback)


    def getConnectedWorkgroupCallbackData(self, days):
        if self.date and self.date != ' ':
            date = f"LIKE '{self.date}%'"
        else:
            date = f"> (select dateadd(day, -{days}, getdate()))"

        SQL_Agent_Interaction = f"""
        SELECT * 
        FROM calldetail_viw 
        WHERE AssignedWorkGroup!='-' AND InteractionType=6 AND LocalUserId!='-' AND InitiatedDate {date};
        """
        self.sqlConnection.execute(SQL_Agent_Interaction)
        callback = self.sqlConnection.fetchall()
        self.WorkgroupConnectedNumberCallbacks = len(callback)


    def getWorkgroupCallbackData(self, days):
        if self.date and self.date != ' ':
            date = f"LIKE '{self.date}%'"
        else:
            date = f"> (select dateadd(day, -{days}, getdate()))"

        
        SQL_Agent_Interaction = f"""
        SELECT * 
        FROM calldetail_viw 
        WHERE AssignedWorkGroup!='-' AND InteractionType=6 AND InitiatedDate {date};
        """
        self.sqlConnection.execute(SQL_Agent_Interaction)
        callback = self.sqlConnection.fetchall()
        self.WorkgroupTotalNumberCallbacks = len(callback)


    def getCallbackData(self, days):
        if self.date and self.date != ' ':
            date = f"LIKE '{self.date}%'"
        else:
            date = f"> (select dateadd(day, -{days}, getdate()))"

        SQL_Agent_Interaction = f"SELECT InteractionType FROM calldetail_viw WHERE InteractionType=6 AND InitiatedDate {date};"
        self.sqlConnection.execute(SQL_Agent_Interaction)
        callback = self.sqlConnection.fetchall()
        self.NumberCallbacks = len(callback)


    def getNumberQueueInteractions(self, user, days):
        if self.date and self.date != ' ':
            date = f"LIKE '{self.date}%'"
        else:
            date = f"> (select dateadd(day, -{days}, getdate()))"
        
        SQL_Agent_Interaction = f"SELECT * FROM InteractionSummary WHERE LastLocalUserId='{user}' AND LastAssignedWorkgroupID IS NOT NULL AND  InitiatedDateTimeUTC {date};"
        self.sqlConnection.execute(SQL_Agent_Interaction)
        data = len(self.sqlConnection.fetchall())
        self.NumberQueuedInteractions = data            


    def getNumberAnsweredQueuedInteractions(self, user, days):
        if self.date and self.date != ' ':
            date = f"LIKE '{self.date}%'"
        else:
            date = f"> (select dateadd(day, -{days}, getdate()))"
        
        SQL_Agent_Interaction = f"SELECT * FROM InteractionSummary WHERE LastLocalUserId='{user}' AND LastAssignedWorkgroupID IS NOT NULL AND tConnected!=0 AND InitiatedDateTimeUTC {date};"
        self.sqlConnection.execute(SQL_Agent_Interaction)
        data = len(self.sqlConnection.fetchall())
        self.NumberAnsweredQueuedInteractions = data


    def getStatusData(self, user, days):
        if self.date and self.date != ' ':
            date = f"LIKE '{self.date}%'"
        else:
            date = f"> (select dateadd(day, -{days}, getdate()))"
        
        SQL_Agent_Status = f"SELECT UserId, StatusDateTime, StatusKey, EndDateTime, StateDuration FROM AgentActivityLog WHERE UserId='{user}'    AND StatusDateTime {date};"
        self.sqlConnection.execute(SQL_Agent_Status)
        self.Status_Data = self.sqlConnection.fetchall()
    

    def getOrgStatusData(self, days):
        if self.date and self.date != ' ':
            date = f"LIKE CONVERT(Datetime, CONVERT(varchar, '{self.date}', 103))"
        else:
            date = f"> (select dateadd(day, -{days}, getdate()))"
        
        SQL_Agent_Status = f"""
        SELECT StatusKey, 
            CONVERT(time(0), DATEADD(SECOND, SUM(StateDuration),0))
        FROM AgentActivityLog 
        WHERE StatusDateTime  {date}
        GROUP BY StatusKey
        """
        self.sqlConnection.execute(SQL_Agent_Status)
        self.Org_Status_Data = self.sqlConnection.fetchall()
    

    def getAgentStatusData(self, user, days):
        if self.date and self.date != ' ':
            date = f"LIKE '{self.date}%'"
        else:
            date = f"> (select dateadd(day, -{days}, getdate()))"
    
        SQL_Agent_Status = f"""
        SELECT StatusKey, 
            CONVERT(time(0), DATEADD(SECOND, SUM(StateDuration),0))
        FROM AgentActivityLog 
        WHERE UserId='{user}' AND StatusDateTime  {date}
        GROUP BY StatusKey
        """
        self.sqlConnection.execute(SQL_Agent_Status)
        self.Agent_Status_Data = self.sqlConnection.fetchall()
    
    def getWorkgroupStatusData(self):
        status = []
        SQL_Agent_Status = f"SELECT DISTINCT StatusKey FROM AgentActivityLog"
        self.sqlConnection.execute(SQL_Agent_Status)
        data = self.sqlConnection.fetchall()
        for i in data:
            status.append(i[0])
        self.Status_Workgroup_Data = status


    def getWorkgroups(self):
        workgroups = []
        SQL_Agent_Status = f"SELECT DISTINCT WorkGroup FROM UserWorkgroups"
        self.sqlConnection.execute(SQL_Agent_Status)
        data = self.sqlConnection.fetchall()
        for i in data:
            workgroups.append(i[0])
        self.WorkgroupList = workgroups


    def getWorkgroupTalkStats(self, days):
        if self.date and self.date != ' ':
            date = f"LIKE '{self.date}%'"
        else:
            date = f"> (select dateadd(day, -{days}, getdate()))"

        SQL_Agent_Status = f"SELECT SUM(tConnected), AVG(tConnected) FROM InteractionSummary WHERE MediaType=0 AND LastAssignedWorkgroupID IS NOT NULL AND InitiatedDateTimeUTC {date};"
        self.sqlConnection.execute(SQL_Agent_Status)
        data = self.sqlConnection.fetchall()[0]
        if data[0]:
            self.WorkgroupTalkTime = data[0]//1000
            self.WorkgroupAvgTalkTime = data[1]//1000
    

    def getWorkgroupHoldStats(self, days) :
        if self.date and self.date != ' ':
            date = f"LIKE '{self.date}%'"
        else:
            date = f"> (select dateadd(day, -{days}, getdate()))"

        SQL_Agent_Status = f"SELECT SUM(tHeld), AVG(tHeld) FROM InteractionSummary WHERE MediaType=0 AND LastAssignedWorkgroupID IS NOT NULL AND InitiatedDateTimeUTC {date};"
        self.sqlConnection.execute(SQL_Agent_Status)
        data = self.sqlConnection.fetchall()[0]
        if data[0]:
            self.WorkgroupHoldTime = data[0]//1000
            self.WorkgroupAvgHoldTime = data[1]//1000
    
    
    def getNumberWorkgroupInteractions(self, days) :
        if self.date and self.date != ' ':
            date = f"LIKE '{self.date}%'"
        else:
            date = f"> (select dateadd(day, -{days}, getdate()))"

        SQL_Agent_Status = f"SELECT tConnected FROM InteractionSummary WHERE LastAssignedWorkgroupID IS NOT NULL AND MediaType=0 AND InitiatedDateTimeUTC {date};"
        self.sqlConnection.execute(SQL_Agent_Status)
        data = self.sqlConnection.fetchall()
       
        self.NumberOfWorkgroupInteractions = len(data)

    
    def getWorkgroupStatusTitle(self) :

        SQL_Agent_Status = f"SELECT DISTINCT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='IWrkgrpQueueStats'"
        self.sqlConnection.execute(SQL_Agent_Status)
        data = self.sqlConnection.fetchall()
        self.WorkgroupStatusTitle = [i[0][1:] for i in data if i[0][0] == 't' or 'cName' == i[0]]


    def getWorkgroupStatusTimes(self, days):
        if self.date and self.date != ' ':
            date = f"LIKE CONVERT(Datetime, CONVERT(varchar, '{self.date}', 103))"
        else:
            date = f"> (select dateadd(day, -{days}, getdate()))"

        SQL_Agent_Status = f"""
        SELECT cName, 
            CONVERT(time(0), DATEADD(SECOND, SUM(tAbandonedAcd),0)), CONVERT(time(0), DATEADD(SECOND, SUM(tAcw),0)), CONVERT(time(0), DATEADD(SECOND, SUM(tAcwCalls),0)), CONVERT(time(0), DATEADD(SECOND, SUM(tAcwComplete),0)), CONVERT(time(0), DATEADD(SECOND, SUM(tAgentAcdLoggedIn),0)), 
            CONVERT(time(0), DATEADD(SECOND, SUM(tAgentAcdLoggedIn2),0)), CONVERT(time(0), DATEADD(SECOND, SUM(tAgentAvailable),0)), CONVERT(time(0), DATEADD(SECOND, SUM(tAgentDnd),0)), CONVERT(time(0), DATEADD(SECOND, SUM(tAgentInAcw),0)), CONVERT(time(0), DATEADD(SECOND, SUM(tAgentLoggedIn),0)), 
            CONVERT(time(0), DATEADD(SECOND, SUM(tAgentLoggedInDiluted),0)), CONVERT(time(0), DATEADD(SECOND, SUM(tAgentNotAvailable),0)), CONVERT(time(0), DATEADD(SECOND, SUM(tAgentOnAcdCall),0)), CONVERT(time(0), DATEADD(SECOND, SUM(tAgentOnNonAcdCall),0)), 
            CONVERT(time(0), DATEADD(SECOND, SUM(tAgentOnOtherAcdCall),0)), CONVERT(time(0), DATEADD(SECOND, SUM(tAgentOtherBusy),0)), CONVERT(time(0), DATEADD(SECOND, SUM(tAgentStatusAcw),0)), CONVERT(time(0), DATEADD(SECOND, SUM(tAgentStatusDnd),0)), 
            CONVERT(time(0), DATEADD(SECOND, SUM(tAgentTalk),0)), CONVERT(time(0), DATEADD(SECOND, SUM(tAlertedAcd),0)), CONVERT(time(0), DATEADD(SECOND, SUM(tAnsweredAcd),0)), CONVERT(time(0), DATEADD(SECOND, SUM(tExternToInternAcdCalls),0)), CONVERT(time(0), DATEADD(SECOND, SUM(tExternToInternCalls),0)), 
            CONVERT(time(0), DATEADD(SECOND, SUM(tFlowOutAcd),0)), CONVERT(time(0), DATEADD(SECOND, SUM(tGrabbedAcd),0)), CONVERT(time(0), DATEADD(SECOND, SUM(tHoldAcd),0)), CONVERT(time(0), DATEADD(SECOND, SUM(tInternToExternAcdCalls),0)), CONVERT(time(0), DATEADD(SECOND, SUM(tInternToExternCalls),0)), 
            CONVERT(time(0), DATEADD(SECOND, SUM(tInternToInternAcdCalls),0)), CONVERT(time(0), DATEADD(SECOND, SUM(tInternToInternCalls),0)), CONVERT(time(0), DATEADD(SECOND, SUM(tStatusGroupBreak),0)), CONVERT(time(0), DATEADD(SECOND, SUM(tStatusGroupFollowup),0)), 
            CONVERT(time(0), DATEADD(SECOND, SUM(tStatusGroupTraining),0)), CONVERT(time(0), DATEADD(SECOND, SUM(tSuspendedAcd),0)), CONVERT(time(0), DATEADD(SECOND, SUM(tTalkAcd),0)), CONVERT(time(0), DATEADD(SECOND, SUM(tTalkCompleteAcd),0)) 
        FROM IWrkgrpQueueStats
        WHERE dIntervalStart {date} 
        GROUP BY cName
        """
        print(SQL_Agent_Status)

        self.sqlConnection.execute(SQL_Agent_Status)
        data = self.sqlConnection.fetchall()
        self.WorkgroupStatusTimes = data
        print(self.WorkgroupStatusTimes)


    def getNumberConnectedWorkgroupInteractions(self, days) :
        if self.date and self.date != ' ':
            date = f"LIKE '{self.date}%'"
        else:
            date = f"> (select dateadd(day, -{days}, getdate()))"

        SQL_Agent_Status = f"SELECT * FROM InteractionSummary WHERE LastAssignedWorkgroupID IS NOT NULL AND MediaType=0 AND InitiatedDateTimeUTC {date} AND tConnected!=0;"
        self.sqlConnection.execute(SQL_Agent_Status) 
        self.NumberOfConnectedWorkgroupInteractions = len(self.sqlConnection.fetchall())


    def getTalkTIme(self, user, days):
        if self.date and self.date != ' ':
            date = f"LIKE '{self.date}%'"
        else:
            date = f"> (select dateadd(day, -{days}, getdate()))"
        
        SQL_Talk_Time = f"SELECT SUM(tConnected), AVG(tConnected)  FROM InteractionSummary WHERE MediaType=0 AND LastLocalUserId='{user}' AND LastAssignedWorkgroupID IS NOT NULL AND InitiatedDateTimeUTC {date};"
        self.sqlConnection.execute(SQL_Talk_Time)

        Time = self.sqlConnection.fetchall()
        
        if Time[0][0]:
            self.TalkTime = Time[0][0]/1000
        if Time[0][1]:
            self.AvgTalkTime = Time[0][1]/1000


    def getAnswerSpeedTime(self, user, days):
        if self.date and self.date != ' ':
            date = f"LIKE '{self.date}%'"
        else:
            date = f"> (select dateadd(day, -{days}, getdate()))"
        
        Answer_Speed_Time = f"SELECT AVG(tAlert) FROM InteractionSummary WHERE MediaType=0 AND LastAssignedWorkgroupID IS NOT NULL AND LastLocalUserId='{user}' AND StartDateTimeUTC {date};"
        self.sqlConnection.execute(Answer_Speed_Time)

        Time = self.sqlConnection.fetchall()
        


        Last_Call_Answer_Speed = f"SELECT tAlert FROM InteractionSummary WHERE MediaType=0 AND LastAssignedWorkgroupID IS NOT NULL AND LastLocalUserId='{user}' AND StartDateTimeUTC {date};"
        self.sqlConnection.execute(Last_Call_Answer_Speed)
        Time2 = self.sqlConnection.fetchall()


        if Time[0] and self.NumberOfInteractions:
            self.LastCallAnswerSpeed = Time2[0][0]/1000
            self.AverageAnswerSpeed = Time[0][0]/1000
    
    
    def getWorkgroupAnswerSpeedTime(self, days):
        if self.date and self.date != ' ':
            date = f"LIKE '{self.date}%'"
        else:
            date = f"> (select dateadd(day, -{days}, getdate()))"
        
        Answer_Speed_Time = f"SELECT AVG(tAlert) FROM InteractionSummary WHERE MediaType=0 AND LastAssignedWorkgroupID IS NOT NULL AND StartDateTimeUTC {date};"
        self.sqlConnection.execute(Answer_Speed_Time)
        Time = self.sqlConnection.fetchall()
        if Time[0][0]:
            self.WorkgroupAverageAnswerSpeed = Time[0][0]/1000



    def convertTimeUnit(self):
        self.AvgTalkTime = time.strftime('%H:%M:%S', time.gmtime(self.AvgTalkTime))
        self.LastCallAnswerSpeed = time.strftime('%H:%M:%S', time.gmtime(self.LastCallAnswerSpeed))
        self.TalkTime = time.strftime('%H:%M:%S', time.gmtime(self.TalkTime))
        self.HoldTime = time.strftime('%H:%M:%S', time.gmtime(self.HoldTime))
        self.AvgHoldTime = time.strftime('%H:%M:%S', time.gmtime(self.AvgHoldTime))
        self.WorkgroupTalkTime = time.strftime('%H:%M:%S', time.gmtime(self.WorkgroupTalkTime))
        self.WorkgroupAvgTalkTime = time.strftime('%H:%M:%S', time.gmtime(self.WorkgroupAvgTalkTime))
        self.WorkgroupHoldTime = time.strftime('%H:%M:%S', time.gmtime(self.WorkgroupHoldTime))
        self.WorkgroupAvgHoldTime = time.strftime('%H:%M:%S', time.gmtime(self.WorkgroupAvgHoldTime))
        self.AverageAnswerSpeed = time.strftime('%H:%M:%S', time.gmtime(self.AverageAnswerSpeed))
        self.AfterCallWorkTime = time.strftime('%H:%M:%S', time.gmtime(self.AfterCallWorkTime))
        self.AvgAfterCallWorkTime = time.strftime('%H:%M:%S', time.gmtime(self.AvgAfterCallWorkTime))
        self.WorkgroupAvgAfterCallWorkTime = time.strftime('%H:%M:%S', time.gmtime(self.WorkgroupAvgAfterCallWorkTime))
        self.WorkgroupAfterCallWorkTime = time.strftime('%H:%M:%S', time.gmtime(self.WorkgroupAfterCallWorkTime))
        self.WorkgroupAverageAnswerSpeed = time.strftime('%H:%M:%S', time.gmtime(self.WorkgroupAverageAnswerSpeed))



    def convertWorkgroupStatusTimes(self):
        times = []
        for count, i in enumerate(self.WorkgroupStatusTimes):
            times.append([])
            for j in i:
                if type(j) != str:
                    times[count].append(time.strftime('%H:%M:%S', time.gmtime(j)))
                else:
                    times[count].append(j)
        self.WorkgroupStatusTimes = times


    def getPercentageValues(self):
        if self.NumberOfWorkgroupInteractions:
            self.NumberOfConnectedWorkgroupInteractionsPercentage = ((self.NumberOfConnectedWorkgroupInteractions/self.NumberOfWorkgroupInteractions)*100)
            self.NumberWorkgroupMissedInteractionsPercentage = (((self.NumberOfWorkgroupInteractions-self.NumberOfConnectedWorkgroupInteractions)/self.NumberOfWorkgroupInteractions)*100)
            self.CallbackPercentage = ((self.WorkgroupTotalNumberCallbacks/self.NumberOfWorkgroupInteractions)*100)


    def getAgentPercentageValues(self):
        if self.NumberOfInteractions:
            self.NumberAnsweredQueuedInteractionsPercentage = ((self.NumberAnsweredQueuedInteractions/self.NumberOfInteractions)*100)
            self.NumberMissedInteractionsPercentage = (((self.NumberOfInteractions-self.NumberAnsweredQueuedInteractions)/self.NumberOfInteractions)*100)
            self.AgentCallbackPercentage = ((self.NumberAgentCallbacks/self.NumberOfInteractions)*100)
    

    def closeDataBaseConnection(self):
        self.sqlConnection.close()


    def __dict__(self):
        if self.userrole.supervisor:
            return {
                'totalTalkTime': self.TalkTime,
                'averageTalkTime': self.AvgTalkTime,
                'interactionData': self.Interaction_Data,
                'statusData': self.Agent_Status_Data,
                'Org_Status_Data': self.Org_Status_Data,
                'statusWorkgroupData': self.Status_Workgroup_Data,
                'status': self.Agent_Status_Data,
                'LastCallAnswerSpeed': self.LastCallAnswerSpeed,
                'AverageAnswerSpeed': self.AverageAnswerSpeed,
                'HoldTime': self.HoldTime,
                'AvgHoldTime': self.AvgHoldTime,
                'AfterCallWorkTime': self.AfterCallWorkTime,
                'AvgAfterCallWorkTime': self.AvgAfterCallWorkTime,
                'NumberAnsweredQueuedInteractions': self.NumberAnsweredQueuedInteractions,
                'CallbackPercentage': self.CallbackPercentage,
                'NumberAgentCallbacks': self.NumberAgentCallbacks,
                'NumberCallbacks': self.NumberCallbacks,
                'NumberQueuedInteractions': self.NumberOfInteractions,
                'NumberMissedQueuedInteractions': abs(self.NumberOfInteractions-self.NumberAnsweredQueuedInteractions),
                'WorkgroupData': self.WorkgroupList,
                'WorkgroupTalkTime': self.WorkgroupTalkTime,
                'WorkgroupAvgTalkTime': self.WorkgroupAvgTalkTime,
                'WorkgroupData': self.WorkgroupList,
                'WorkgroupHoldTime': self.WorkgroupHoldTime,
                'WorkgroupAvgHoldTime': self.WorkgroupAvgHoldTime,
                'WorkgroupAvgAfterCallWorkTime': self.WorkgroupAvgAfterCallWorkTime,
                'WorkgroupAfterCallWorkTime': self.WorkgroupAfterCallWorkTime,
                'NumberOfWorkgroupInteractions': self.NumberOfWorkgroupInteractions,
                'NumberOfConnectedWorkgroupInteractions': self.NumberOfConnectedWorkgroupInteractions,
                'NumberWorkgroupMissedInteractions': self.NumberOfWorkgroupInteractions-self.NumberOfConnectedWorkgroupInteractions,
                'NumberOfConnectedWorkgroupInteractionsPercentage': self.NumberOfConnectedWorkgroupInteractionsPercentage,
                'NumberWorkgroupMissedInteractionsPercentage': self.NumberWorkgroupMissedInteractionsPercentage,
                'WorkgroupStatusTitle': self.WorkgroupStatusTitle,
                'WorkgroupStatusTimes': self.WorkgroupStatusTimes,
                'WorkgroupTotalNumberCallbacks': self.WorkgroupTotalNumberCallbacks,
                'WorkgroupConnectedNumberCallbacks': self.WorkgroupConnectedNumberCallbacks,
                'WorkgroupAverageAnswerSpeed': self.WorkgroupAverageAnswerSpeed,
                'NumberAnsweredQueuedInteractionsPercentage': self.NumberAnsweredQueuedInteractionsPercentage,
                'NumberMissedInteractionsPercentage': self.NumberMissedInteractionsPercentage,
                'AgentCallbackPercentage': self.AgentCallbackPercentage
            }

        if self.userrole.agent:
            return {
                'totalTalkTime': self.TalkTime,
                'averageTalkTime': self.AvgTalkTime,
                'interactionData': self.Interaction_Data,
                'statusData': self.Agent_Status_Data,
                'statusWorkgroupData': self.Status_Workgroup_Data,
                'status': self.Agent_Status_Data,
                'LastCallAnswerSpeed': self.LastCallAnswerSpeed,
                'AverageAnswerSpeed': self.AverageAnswerSpeed,
                'NumberCallbacks': self.NumberCallbacks,
                'HoldTime': self.HoldTime,
                'AvgHoldTime': self.AvgHoldTime,
                'AfterCallWorkTime': self.AfterCallWorkTime,
                'AvgAfterCallWorkTime': self.AvgAfterCallWorkTime,
                'NumberAnsweredQueuedInteractions': self.NumberAnsweredQueuedInteractions,
                'NumberAgentCallbacks': self.NumberAgentCallbacks,
                'NumberQueuedInteractions': self.NumberQueuedInteractions,
                'NumberMissedQueuedInteractions': self.NumberQueuedInteractions-self.NumberAnsweredQueuedInteractions,
                'NumberAnsweredQueuedInteractionsPercentage': self.NumberAnsweredQueuedInteractionsPercentage,
                'NumberMissedInteractionsPercentage': self.NumberMissedInteractionsPercentage,
                'AgentCallbackPercentage': self.AgentCallbackPercentage
            }

