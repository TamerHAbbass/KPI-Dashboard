# from bs4 import BeautifulSoup
# import urllib.request



# source = urllib.request.urlopen('https://help.genesys.com/pureconnect/datadictionary/content/views/iagentqueuestats.html').read()
# soup = bs.BeautifulSoup(source,'lxml')
# print(soup)
"""
AbandonedAcd
    - The sum of the time in seconds all abandoned ACD interactions were in queue before they abandoned.

Acw
    - The sum of the time, in seconds, the agent spent in an After Call Work status, also known as wrap up time. The count starts when an interaction goes inactive, usually due to a local or remote disconnect, and ends when the agent leaves the After Call Work status. This value may or may not include non-ACD interactions depending on how the statuses are setup.
      Note tACW is the time in follow-up that is directly associated with an interaction. Follow-up without an ACD interaction (agent selected with no previously disconnected ACD interaction) will not be in tACW. The tACW value will only be recorded in rows of queue statistics directly associated with the interaction. It will not be in any other workgroup, media type, or skill associated rows.

AcwCalls
    - Sum of time, in seconds, the agent spent on outbound interactions during After Call Work time. Also see nAcwCalls.

AcwComplete
    - Counts the total ACW Time for the completed ACW sessions. This includes the total time for each session even if it spanned multiple statistic intervals.

AgentAcdLoggedIn
    - Sum of the time, in seconds, the agent was logged in, activated in the queue, and available to take interactions in a status that has the Status allows ACD calls box checked. By default, only the Available status has this box checked. All three conditions must be met to count toward tAgentAcdLoggedIn time. This column does not count the time an agent is actively engaged in ACD interactions, for example, talking on ACD calls. This statistic can be used to track Idle Time.

AgentAcdLoggedIn2
    - Same as tAgentAcdLoggedIn but the agent's status has no effect to this statistic.

AllAgentAvailable
    - Sum of tAgentAvailable for the current User (cName). Same as tAgentAvailable when cReportGroup = '*' for the cName in this interval.

AgentDnd
    - Sum of the time, in seconds, the agent was in a Do Not Disturb state. Also, tAgentDND is part of a set of values that must always sum up to tAgentLoggedIn. It is driven by the combination of ACD availability and client status.

AgentInAcw
    - Sum of the time, in seconds the agent was in an After Call Work state.
      Note tAgentInAcw is for the Workgroup and User rows of statistics that are associated with tACW, and will include the tACW time. For other rows, tACW will not be included in tAgentInAcw, but instead will be counted as ACD time of another Workgroup and be in tAgentOnOtherAcdCall and tAgentOtherBusy. For non-ACW time, manual follow-up not associated with an ACD interaction, the time in a follow-up status will be included in tAgentInAcw and tAgentStatusACW.

AgentLoggedIn
    - The time, in seconds, that the agent was logged in to the client. This time is divided between the agent's statuses in tAgentOnAcdCall, tAgentOnOtherAcdCal, tAgentInAcw, tAgentOnNonAcdCall, tAgentAvailable, tAgentDnd, and tAgentNotAvailable.
      The values in these status fields are adjusted up or down so their sum equals tAgentLoggedIn. Because rounding differences can cause loss of seconds whenever one time is summed as parts broken down by seconds, rounded values are adjusted to insure there is no difference in the sum.

AgentLoggedInDiluted
    - Not meaningful relative to an agent queue because an agent cannot be a member of more than one agent queue.

AgentNotAvailable
    - Sum of the time, in seconds, the agent was not available to take ACD interactions, but was logged in to the system.

AgentOnAcdCall
    - Sum of the time in seconds the agent was working on ACD connected interactions for the workgroup

AgentOnNonAcdCall
    - Sum of the time, in seconds the agent was working on non-ACD interactions.

AgentOnOtherAcdCall
    - Sum of the time in seconds the agent was working on ACD connected interactions for other workgroups

AgentOtherBusy
    - Sum of the time, in seconds, the agent was working on interactions (ACD and non-ACD) for queues other this one.

AgentStatusAcw
    - Sum of the time, in seconds, the agent was in an After call Work status as determined only by the current client status. If the current status is marked as ACW, then ACW time is accumulated. The value can differ from tAgentInAcw. If agents are allowed to set their status to an ACW status while on an ACD interaction, then they still accumulate time in tAgentOnAcdCall, but their status is ACW, so they will also accumulate tAgentStatusAcw.
      Note tAgentStatusACW is any time spent in a follow-up Status. This attribute is one of the agent only statistics so it is not found in rows of statistics below Work Group/Distribution Queue and User Queue, i.e., Media Type and Skill.

AgentStatusDnd
    - Sum of the time, in seconds, the agent was in a Do Not Disturb status as determined only by the current client status. If the current status is marked as DND, then DND time is accumulated. The value can differ from tAgentDND. If agents are allowed to set their status to a DND status while on an ACD interaction, then they still accumulate time in tAgentOnAcdCall, but their status is DND, so they will also accumulate tAgentStatusDND.

AgentTalk
    - Sum of time, in seconds, the agent was on ACD interactions from first Client_Connected until end of ACW for this queue.
      Note tAgentTalk is tTalkACD + tACW, and should be thought of as tHandleTime.

AlertedAcd
    - Sum of the time, in seconds, ACD interactions spent in an Alerting state on this user queue. Also referred to as Ring time.

AnsweredAcd
    - The sum of the time in seconds of all ACD interactions that were in queue before entering a Client_Connected state.

ExternToInternAcdCalls
    - Sum of seconds for ACD interactions from external locations to internal extensions.

FlowOutAcd
    - Sum of seconds ACD interactions were in queue before being counted in nFlowOutAcd. See nFlowOutAcd for more information.

HoldAcd
    - The sum of the time, in seconds, all ACD interactions spent on hold while in this queue.

InternToExternAcdCalls
    - Sum of seconds for ACD interactions from internal extensions to external locations.

InternToInternAcdCalls
    - Sum of seconds for ACD interactions from internal extensions to internal extensions. This includes ACD Interactions transferred between agents in the same distribution queue. Both agents are credited with the ACD interaction.

InternToInternCalls
    - Sum of seconds for all interactions from internal extensions to internal extensions.

StatusGroupFollowup
    - Sum of the time, in seconds, the agent was in any status that belongs to the status group Followup.
      A status group is any grouping of agent status messages. There are five predefined groups in CIC: Available, Break, Followup, Training, and Unavailable. Beyond just grouping statuses, status groups provide a way to track specific time in a status as part of the interval information of an agent or distribution queue. See the StatusGroup column in the AgentActivityLog table for more information.
      It is possible to define your own custom groups. See the online help in Interaction Administrator for more information. It is also possible to make the group to status mapping a one to one mapping. No grouping is actually forced, just encouraged.
      Note: For the IAgentQueueStats view, the tStatusGroupFollowup column will always be 0 (zero) in the workgroup row, and the value is populated only for the workgroup summary row.

StatusGroupTraining
    - Sum of time, in seconds, the agent was in any status that belongs to the status group Training.

TalkAcd
    - The sum of the time, in seconds, all ACD interactions spent from when they first entered a Client_Connected state until the time the ACD interactions went inactive or flowed out of the queue.
      It is possible to have talk time appear in an interval without having any new ACD interactions for that interval. The time comes from ACD interactions that connected in that interval.
      Interactions might have entered the queue in the previous interval. It is possible to have talk time on a chat. Think of tTalkAcd as the time an interaction is active with an agent.
      Note tTalkACD is the time an interaction is active with an agent, including any Hold time with the agent during the interaction.

TalkCompleteAcd
    - Counts the total talk time of a call in the period in which it completed, unlike tTalkAcd which counts the talk time for each period it is counted in.

"""


from unittest.mock import sentinel

'''
Get job number sent
what are the jobs doing in the manager.
What are users seeing in jetfile.
Is the import process completed.
Check vmotion (Work with vmware)
Turn off vmotion for a week or so.
Db maintenance.

'''


status = ["","","","TalkCompleteAcd"]

'''
{&#x27;agent&#x27;: {&#x27;totalTalkTime&#x27;: &#x27;01:13:32&#x27;, &#x27;averageTalkTime&#x27;: &#x27;00:03:30&#x27;, &#x27;interactionData&#x27;: {0: {&#x27;interaction&#x27;: {&#x27;InteractionIDKey&#x27;: &#x27;200119105920211227&#x27;, &#x27;StartDateTimeUTC&#x27;: datetime.datetime(2021, 12, 27, 16, 52, 27, 740000), &#x27;LastLocalUserId&#x27;: &#x27;Agent4&#x27;, &#x27;LastAssignedWorkgroupId&#x27;: &#x27;DPR Helpdesk&#x27;, &#x27;RemoteNumberCallId&#x27;: &#x27;+19495724223&#x27;, &#x27;RemoteName&#x27;: &#x27;RICHARDSON KOLB&#x27;, &#x27;InitiatedDateTimeUTC&#x27;: datetime.datetime(2021, 12, 27, 16, 52, 27, 740000), &#x27;ConnectionDateTimeUTC&#x27;: datetime.datetime(2021, 12, 27, 16, 52, 27, 787000), &#x27;TerminatedDateTimeUTC&#x27;: datetime.datetime(2021, 12, 27, 16, 53, 58, 398000), &#x27;LineDuration&#x27;: Decimal(&#x27;90658&#x27;), &#x27;CallEventLog&#x27;: &#x27;08:52:27: Initializing
08:52:27: Offering
08:52:27: ANI:  9495724223
08:52:27: DNIS:  9165772587
08:52:27: Call answered
08:52:27: DPR Incoming Call --&gt; IVR
08:52:27: DPR Open 6am - 10pm 7 days
08:52:28: DPR_IVR
08:52:28: Calls: 1
08:52:31: Asset &amp; ParkId unknown
08:52:33: Ticket#: T20211227.0061
08:52:33: WS_NewTicket: Success
08:52:39: Calls: 0
08:52:39: DPR Queues
08:52:39: DPR Open 6am - 10pm
08:52:39: 2b. DPR Helpdesk - Tier1 1st
08:52:39: Entered Workgroup DPR Helpdesk
08:52:39: Offering
08:52:39: ACD Skills Added: DPR 0s|DPR 30s|DPR 60s|DPR 90s
08:52:39: ACD interaction assigned to Agent4
08:52:39: ACD - Alerting: Agent4
08:52:39: Sent to user Agent4
08:52:39: Offering
08:52:39: Sent to station 15307126390
08:52:39: Alerting
08:53:08: Connected
08:53:08: ACD interaction connected to Agent4
08:53:08: ACD - Assigned: Agent4
08:53:58: Disconnected [Remote Disconnect]&#x27;}}, 1: {&#x27;interaction&#x27;: {&#x27;InteractionIDKey&#x27;: &#x27;200119106220211227&#x27;, &#x27;StartDateTimeUTC&#x27;: datetime.datetime(2021, 12, 27, 16, 57, 46, 339000), &#x27;LastLocalUserId&#x27;: &#x27;Agent4&#x27;, &#x27;LastAssignedWorkgroupId&#x27;: &#x27;DPR Helpdesk&#x27;, &#x27;RemoteNumberCallId&#x27;: &#x27;+17605256133&#x27;, &#x27;RemoteName&#x27;: &#x27;ELIZABETH PEACY&#x27;, &#x27;InitiatedDateTimeUTC&#x27;: datetime.datetime(2021, 12, 27, 16, 57, 46, 339000), &#x27;ConnectionDateTimeUTC&#x27;: datetime.datetime(2021, 12, 27, 16, 57, 46, 386000), &#x27;TerminatedDateTimeUTC&#x27;: datetime.datetime(2021, 12, 27, 16, 57, 59, 43000), &#x27;LineDuration&#x27;: Decimal(&#x27;12704&#x27;), &#x27;CallEventLog&#x27;: &#x27;08:57:46: Initializing
08:57:46: Offering
08:57:46: ANI:  7605256133
08:57:46: DNIS:  9165772587
08:57:46: Call answered
08:57:46: DPR Incoming Call --&gt; IVR
08:57:46: DPR Open 6am - 10pm 7 days
08:57:46: DPR_IVR
08:57:46: Calls: 1
08:57:50: Asset &amp; ParkId unknown
08:57:51: Ticket#: T20211227.0063
08:57:51: WS_NewTicket: Success
08:57:58: Calls: 0
08:57:58: DPR Queues
08:57:58: DPR Open 6am - 10pm
08:57:58: 2b. DPR Helpdesk - Tier1 1st
08:57:58: Entered Workgroup DPR Helpdesk
08:57:58: Offering
08:57:58: ACD Skills Added: DPR 0s|DPR 30s|DPR 60s|DPR 90s
08:57:58: ACD interaction assigned to Agent4
08:57:58: ACD - Alerting: Agent4
08:57:58: Sent to user Agent4
08:57:58: Offering
08:57:58: Sent to station 15307126390
08:57:58: Alerting
08:57:59: Disconnected [Remote Disconnect]&#x27;}}, 2: {&#x27;interaction&#x27;: {&#x27;InteractionIDKey&#x27;: &#x27;200119106520211227&#x27;, &#x27;StartDateTimeUTC&#x27;: datetime.datetime(2021, 12, 27, 17, 11, 43, 76000), &#x27;LastLocalUserId&#x27;: &#x27;Agent4&#x27;, &#x27;LastAssignedWorkgroupId&#x27;: &#x27;DPR Helpdesk&#x27;, &#x27;RemoteNumberCallId&#x27;: &#x27;+18316492907&#x27;, &#x27;RemoteName&#x27;: &#x27;Monterey CA&#x27;, &#x27;InitiatedDateTimeUTC&#x27;: datetime.datetime(2021, 12, 27, 17, 11, 43, 76000), &#x27;ConnectionDateTimeUTC&#x27;: datetime.datetime(2021, 12, 27, 17, 12, 14, 467000), &#x27;TerminatedDateTimeUTC&#x27;: datetime.datetime(2021, 12, 27, 17, 12, 51, 968000), &#x27;LineDuration&#x27;: Decimal(&#x27;68892&#x27;), &#x27;CallEventLog&#x27;: &#x27;09:11:43: Initializing
09:11:43: Entered Workgroup DPR Helpdesk
09:11:43: Sent to user Agent4
09:11:43: Outbound Call:  8316492907
09:11:52: Dialing
09:11:54: Proceeding
09:12:14: Connected
09:12:14: Call Connected
09:12:51: Disconnected [Local Disconnect]&#x27;}}, 3: {&#x27;interaction&#x27;: {&#x27;InteractionIDKey&#x27;: &#x27;200119107120211227&#x27;, &#x27;StartDateTimeUTC&#x27;: datetime.datetime(2021, 12, 27, 17, 16, 42, 535000), &#x27;LastLocalUserId&#x27;: &#x27;Agent4&#x27;, &#x27;LastAssignedWorkgroupId&#x27;: &#x27;DPR Helpdesk&#x27;, &#x27;RemoteNumberCallId&#x27;: &#x27;+15305506163&#x27;, &#x27;RemoteName&#x27;: &#x27;Truckee CA&#x27;, &#x27;InitiatedDateTimeUTC&#x27;: datetime.datetime(2021, 12, 27, 17, 16, 42, 535000), &#x27;ConnectionDateTimeUTC&#x27;: datetime.datetime(2021, 12, 27, 17, 17, 33, 832000), &#x27;TerminatedDateTimeUTC&#x27;: datetime.datetime(2021, 12, 27, 17, 17, 
'''






AgentAvailable
AgentDnd 
AgentLoggedIn
AgentLoggedInDiluted
AgentNotAvailable 
AgentOnNonAcdCall 
AgentTalk
AgentAcdLoggedIn
AgentAcdLoggedIn2
AlertedAcd
AnsweredAcd  
ExternToInternCalls
InternToExternCalls
TalkAcd
TalkCompleteAcd


Hostname Site
ABT-VMC-01 AB Tools

COLO-UCVM-00 Future Ford
COLO-UCVM-01 Future Ford

krw-esx-01 Kodiak Roofing 
krw-esx-02 Kodiak Roofing 
SPK-ESE-01 Kodiak Roofing 
SPK-ESX-02 Kodiak Roofing 

l39-sac-ucs-1 Stationary Engineers Local 39
l39-sf-ucs-1 Stationary Engineers Local 39

SA-ESXi1 MJH
SA-ESXi2 MJH
SA-ESXi3 MJH
vc-sacramento MJH
vc-stockton MJH
esxi01.mjhallandcompany.com MJH
esxi02.mjhallandcompany.com MJH
esxi03.mjhallandcompany.com MJH
esxi04.mjhallandcompany.com MJH

dc1host01 Teamsos Internal
dc1host02 Teamsos Internal
dc1host03 Teamsos Internal
dc2host01 Teamsos Internal
dc2host02 Teamsos Internal
dc2host03 Teamsos Internal
sos-cld-vc01 Teamsos Internal