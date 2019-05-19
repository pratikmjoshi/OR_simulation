import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

n = input("Enter the desired number of weeks for simulation:")
n = int(n)
arrival = 0
departure=0
new_departure = 0
events = []
events.append(('Start',0))
while new_departure<n:
	x = np.random.exponential(1/50)
	y = np.random.exponential(1/140) #Sum of 2 poisson servers 70+70
	arrival+=x
	events.append(('A',arrival))
	new_departure = max(arrival,departure)+y
	events.append(('D',new_departure))
	departure=new_departure
events = sorted(events,key=lambda x:x[1])
events = [i for i in events if i[1]<n ]
events.append(('T',n)) 
print("First 10 events:")
print(events[:10])
data = pd.DataFrame(columns=['Time', 'Event', 'TBE','TNA','TND','TNS','TNQ','TTS','TTQ','SS','IT'],dtype=float)
net_profit=0
total_arrivals=0
total_deps = 0
total_system=0
total_queue=0
idle_time=0
server_state = 'I'
data.loc[0] = [0,'Start','-',0,0,0,0,0,0,'I',0]
for i in range(1,len(events)):
	if server_state=='I':
		idle_time+=events[i][1]-events[i-1][1]
	if events[i][0]=='A':
		total_arrivals+=1
		total_system+=1
		if server_state=='B':
			total_queue+=1
	elif events[i][0] == 'D':
		total_deps+=1
		total_system-=1
		if total_queue>0:
			total_queue-=1
	total_time_system=(total_queue+1)*(events[i][1]-events[i-1][1])
	total_time_queue=total_queue*(events[i][1]-events[i-1][1])
	data.loc[i] = [events[i][1],events[i][0],events[i][1]-events[i-1][1],total_arrivals,total_deps,total_system,total_queue,total_time_system,total_time_queue,server_state,idle_time]
	if total_system>0:
		server_state='B'
	else:
		server_state='I'
print("First 10 columns of simulation table")
print(data.head(10))
#print(data)
print("Mean number of cars:"+str(data['TNS'].mean())+' cars/week')
print("Mean time spent by cars:"+str(data['TTS'].mean())+' weeks/car')
print("Net profit by service centre:"+str(data['TTS'].sum()*-2500+300*n*7))
sns.lineplot(x='Time',y='TNS',data=data)
plt.show()
sns.lineplot(x='Time',y='TTS',data=data)
plt.show()
