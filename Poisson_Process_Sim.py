#Simulating Poisson Process
import random as rd
import math as mt
import matplotlib.pyplot as plt
import statistics as stat
import numpy as np
import matplotlib.animation as animation
from itertools import count

    
#Use numpy to simulate a regular poisson process at lambda=5
rng = np.random.default_rng(300)
sim_poisson = rng.poisson(lam=5 , size= 1000)
print(sim_poisson)

#Calculate how the mean and variancechanges overtime
def fisher_calculator(sim):
    val_list=[]
    mean_arrival = []
    var_arrival = []
    fisher_index_classic =[]
    for i in range(len(sim)):
        val_list.append(sim[i])
        mean_arrival.append(stat.mean(val_list))
        if i == 0:
            var_arrival.append(0)
        else:
            var_arrival.append(stat.variance(val_list))
        fisher_index_classic.append(var_arrival[i]/mean_arrival[i])
    return mean_arrival , fisher_index_classic
    

fisher_poisson = fisher_calculator(sim_poisson)


#Still plot of classic poisson
plt.plot(fisher_poisson[1])
plt.axhline(y=1, color='r', linestyle='-')
plt.title("Fisher Index of Dispersion of classic Poisson Process")
plt.xlabel("Time")
plt.ylabel("Dispersion")
plt.show()


#animate this plot
x=[]
y=[]
fig,ax = plt.subplots()
ax.plot(x,y)

counter = count(0,10)

def update(i):
    index = next(counter)
    x.append(index)
    y.append(fisher_poisson[1][index])
    plt.cla()
    ax.plot(x,y)

ani = animation.FuncAnimation(fig=fig , func=update,interval = 100)
plt.show()


#To simulate the underdispersed model we simply shift our poisson out put up by l
def under_dispersed(list,l):
    under_disp_data = list + l
    return under_disp_data

under_sim = under_dispersed(sim_poisson , l=1)

#Use the fisher_calculator function to get the dispersion plot
under_fisher = fisher_calculator(under_sim)






#Still plot of underdispersed fisher index at l=1
plt.plot(under_fisher[1])
plt.axhline(y=5/6, color='r', linestyle='-')
plt.title("Fisher Index of Dispersion of Falling Factorial Poisson Process ")
plt.xlabel("Time")
plt.ylabel("Dispersion")
plt.show()


#Animate this plot
x=[]
y=[]
fig,ax = plt.subplots()
ax.plot(x,y)
ax.set_title("Classic Poisson Dispersion Plot")
counter = count(0,10)

def update(i):
    index = next(counter)
    x.append(index)
    y.append(under_fisher[1][index])
    plt.cla()
    ax.plot(x,y)

ani1 = animation.FuncAnimation(fig=fig , func=update,interval = 100)
plt.title("Classic Poisson")
plt.show()

#We observe slight under dispersion.  We can run this experiment with l=2 
under_sim_2= under_dispersed(sim_poisson , l=2)
under_fisher_2 = fisher_calculator(under_sim_2)




#Still plot of underdispersed fisher plot at l=2
plt.plot(under_fisher_2[1])
plt.axhline(y=5/7, color='r', linestyle='-')
plt.title("Fisher Index of Dispersion of Falling Factorial Poisson Process at l=2")
plt.xlabel("Time")
plt.ylabel("Dispersion")
plt.show()

#Animate this plot
x=[]
y=[]
fig,ax = plt.subplots()
ax.plot(x,y)

counter = count(0,10)

def update(i):
    index = next(counter)
    x.append(index)
    y.append(under_fisher_2[1][index])
    plt.cla()
    ax.plot(x,y)

ani2 = animation.FuncAnimation(fig=fig , func=update,interval = 100)
plt.show()


#We can also do the same for l=5
under_sim_5= under_dispersed(sim_poisson , l=5)
under_fisher_5 = fisher_calculator(under_sim_5)



#Still plot
plt.plot(under_fisher_5[1])
plt.axhline(y=5/10, color='r', linestyle='-')
plt.title("Fisher Index of Dispersion of Falling Factorial Poisson Process at l=5")
plt.xlabel("Time")
plt.ylabel("Dispersion")
plt.show()



#Animate this plot
x=[]
y=[]
fig,ax = plt.subplots()
ax.plot(x,y)

counter = count(0,10)

def update(i):
    index = next(counter)
    x.append(index)
    y.append(under_fisher_5[1][index])
    plt.cla()
    ax.plot(x,y)

ani3 = animation.FuncAnimation(fig=fig , func=update,interval = 100)
plt.show()


#plot the final model for overdispersion
def rise_pmf1(n , lambd):
    f = ((mt.exp(lambd) - 1)**(-1))*((lambd**(n+1))/mt.factorial(n+1))
    return f

def over_poisson(lamb , iterations ,f):
    #Create an empty list to store the various cdf values and the number of arrivals
    arrivals =[]
    cdf_set = []
    fisher_dispersion = []
    mean_arrival = []
    x = 0 
    #We need 100 instances of the pdf, then we increment each time
    for i in range(0 , 100):
        y = f(i , lamb)
        x += y
        cdf_set.append(x)

    #Create a uniform random variable outputs values from 0 to 1np.random.seed()
    np.random.seed(300)
    prob = np.random.uniform(0 , 1 , iterations)
    for i in range(iterations):
        #Output random probability from 0 to 1s
        
        prob_value = prob[i]
        #Match this probability the accumlated CDF list 
        #Brute force way of doing it
        for j in range(len(cdf_set)):
            if prob_value < cdf_set[j]:
                arrivals.append(j)
                break
    #Calculate dispersion over time
    for i in range(len(arrivals)):
        if stat.mean(arrivals[0:i+1]) == 0 or i == 0 :
            fisher_dispersion.append(0)
        else:
            fisher_dispersion.append(stat.variance(arrivals[0:i+1])/stat.mean(arrivals[0:i+1]))

    for i in range(len(arrivals)):
        mean_arrival.append(stat.mean(arrivals[0:i+1]))

    return arrivals , fisher_dispersion ,mean_arrival

h = over_poisson(5 , 1000 , rise_pmf1)





#Still plot
plt.plot(h[1])
plt.axhline(y=1.15, color='r', linestyle='-')
plt.title("Dispersion of Inverse Rising Factorial Poisson Process at l=1")
plt.xlabel("time")
plt.ylabel("Fisher Index of Dispersion")


plt.show()

#Animate this plot
x=[]
y=[]
fig,ax = plt.subplots()
ax.plot(x,y)

counter = count(0,10)

def update(i):
    index = next(counter)
    x.append(index)
    y.append(h[1][index])
    plt.cla()
    ax.plot(x,y)

ani4 = animation.FuncAnimation(fig=fig , func=update,interval = 100)
plt.show()

#One can observe overdispersion (line is increasing at a faster rate with overdispersion
##See what happens when we increase our l value to 2
def rise_pmf2(n , lambd):
    f = ((mt.exp(lambd) - 1-((lambd**2)/mt.factorial(2)))**(-1))*((lambd**(n+2))/mt.factorial(n+2))
    return f


#See what happens when we increase our l value to 5

def rise_pmf5(n , lambd):
    f = ((mt.exp(lambd) - 1-((lambd**2)/mt.factorial(2))-((lambd**3)/mt.factorial(3))-((lambd**4)/mt.factorial(4)))**(-1))*((lambd**(n+5))/mt.factorial(n+5))
    return f



#Still plot
h2 = over_poisson(5,1000,rise_pmf2)
plt.plot(h2[1])
plt.axhline(y=1.15, color='r', linestyle='-')
plt.title("Dispersion of Inverse Rising Factorial Poisson Process at l=2")
plt.xlabel("time")
plt.ylabel("Fisher Index of Dispersion")

plt.show()

#Animate this plot
x=[]
y=[]
fig,ax = plt.subplots()
ax.plot(x,y)

counter = count(0,10)

def update(i):
    index = next(counter)
    x.append(index)
    y.append(h2[1][index])
    plt.cla()
    ax.plot(x,y)

ani5 = animation.FuncAnimation(fig=fig , func=update,interval = 100)
plt.show()



h5 = over_poisson(5,1000,rise_pmf5)
plt.plot(h5[1])
plt.axhline(y=1.6, color='r', linestyle='-')
plt.title("Dispersion of Inverse Rising Factorial Poisson Process at l=5")
plt.xlabel("time")
plt.ylabel("Fisher Index of Dispersion")

plt.show()


#Animate this plot
x=[]
y=[]
fig,ax = plt.subplots()
ax.plot(x,y)

counter = count(0,10)

def update(i):
    index = next(counter)
    x.append(index)
    y.append(h5[1][index])
    plt.cla()
    ax.plot(x,y)

ani6 = animation.FuncAnimation(fig=fig , func=update,interval = 100)
plt.show()


#We see that as we increase l, we increase our dipersion (steeper line)
    




        


   






    




