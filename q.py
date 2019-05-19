import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

n = input("Enter the desired number of weeks for simulation:")
n = int(n)
data = pd.DataFrame(columns=['Week No.', 'Initial No. of Cars at Service Centre', 'Cars arriving','Cars serviced by Station 1','Cars serviced by Station 2','Final No. of Cars','Mean No. of Cars','Mean time spent by cars','Lost Cost','Rent','Net profit by service centre'])
net_profit = 0
net_cars = 0
for i in range(n):
	initial_cars = net_cars
	car_arrival = np.random.poisson(50)
	service_times = np.random.exponential(1/70,car_arrival)
	duration=1.00000
	s1=[]
	sum1=0
	s2=[]
	sum2=0
	j=0
	while duration>0 and j!=car_arrival:
		if len(s1)==0:
			s1.append(service_times[j])
			duration-=service_times[j]
			sum1+=service_times[j]
		elif len(s2)==0:
			s2.append(service_times[j])
			duration-=service_times[j]
			sum2+=service_times[j]
		elif sum1 >= sum2:
			s2.append(service_times[j])
			duration-=service_times[j]
			sum2+=service_times[j]
		else:
			s1.append(service_times[j])
			duration-=service_times[j]
			sum1+=service_times[j]
		j+=1
	net_cars += car_arrival - (len(s1)+len(s2))
	lost_cost = net_cars*2500
	rent = 7*300
	net_profit += (rent-lost_cost)
	mean_no_of_cars = (sum([1/i for i in s1])+sum([1/i for i in s2]))/(len(s1)+len(s2))
	mean_time = (sum(s1)+sum(s2))/(len(s1)+len(s2))
	data.loc[i] = [i,initial_cars,car_arrival,len(s1),len(s2),net_cars,mean_no_of_cars,mean_time,lost_cost,rent,net_profit]

#print(data)
print("Total Mean number of cars:"+str(data['Mean No. of Cars'].mean())+' cars/week')
print("Total Mean time spent by cars:"+str(data['Mean time spent by cars'].mean())+' weeks/car')
print("Net profit by service centre:"+str(data['Net profit by service centre'].iloc[-1]))
sns.lineplot(x='Week No.',y='Mean No. of Cars',data=data)
plt.show()
sns.lineplot(x='Week No.',y='Mean time spent by cars',data=data)
plt.show()
