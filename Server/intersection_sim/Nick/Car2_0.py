class Car:
    
    def __init__(self,num):
        self.num=num
    #set cars velocity
    def sv(self,vel):
        self.vel=float(vel)
    #get cars velocity    
    def gv(self):
        return(self.vel)
    #set position 
    def sp(self,pos):
        self.pos=float(pos)
    #get positon
    def gp(self):
        return(self.pos)
    #set time
    def st(self):
        self.t=self.pos/self.vel
    #get time
    def gt(self):
        return(self.t)
    #set all
    def sa(self,vel,pos):
        self.pos=float(pos)
        self.vel=float(vel)
        self.t=self.pos/self.vel
    #get all
    def ga(self):
        return(self.pos,self.vel,self.t)


#assume the car is 1 ft long
#assume the postion is meassured from the center of the intersection
    #to the front of the car
#assume c1 is on one road and c2 is on the other road

#must add priority manager
#must add feedback reaction
#must account for more cars 
#must handle N cars (up to saturation)

#suggestion peer to peer outside range (cars talk to the car in front and behind them)
#suggestion inside range use a server hosted by a car
#alternative suggestion inside range use a server hosted by an external server
#alternative suggestion using peer to peer communication to determine priority 
    #i.e. the car infront of you tells you what cars you need to look at on the other road
    #then peer to peer with the 4 relatvent cars 
    #the car infront of you, behind you, and the car that will pass through the intersection
    #before you and after you.




#create the first instance of a car
c1=Car(1)
#create second instance of a car
c2=Car(2)
#create an instance of car to switch 1 and 2 if neccessary
temp=Car(3)
#initialize time when car 2 enters region 0
time=0
#change in time 
deltat=.05
#initialize position and velocity for car 1 and 2
c1.sa(4,12)
c2.sa(4,11.999999999999)
#pull values from car instances
(p1,v1,t1)=c1.ga()
(p2,v2,t2)=c2.ga()
#distance declorating
dd=0
#time decelorating
td=0
switched=0
#switch cars if neccessary
if(p2>p1):
    temp=c2
    c2=c1
    c1=temp
    switched=1
    #while car 2 is in the intersection
d=(p1-p2)
while(c2.gp()>=-1):
    #get current values of all cars
    (p1,v1,t1)=c1.ga()
    (p2,v2,t2)=c2.ga()
    #get the time for car 2 to exit the intersection
    to2=(p2+1)/v2
    #if the space between the cars is less than 1.5 feet 
    if(v1*(t2-td)>1):
        #decelorate
        c1.sv(v1-(deltat))
        dd=dd+(v1*deltat)
        td=td+deltat
        #and update the time to intersection
        c1.st()
        c2.st()
        #if the distance is less than 3/4 required change and velocity is less than 4
    elif (v1*(t2-td)>1 and to2>td+(10*deltat)):
        #maintain speed
        #and update the time to intersection
        c1.st()
        c2.st()
    elif(t2<=td+10*deltat and v1<4):
        #accelorate
        c1.sv(v1+deltat)
        dd=dd-(v1*deltat)
        td=td-deltat
        c1.st()
        c2.st()
    else:
        c1.sv(4)
        c1.st()
        c2.st()
    #print useful information
    print ('for time',time)
    print (c1.ga())
    print (c2.ga())
    #update the positoin of each vehicle
    c1.sp(p1-(v1*deltat))
    c2.sp(p2-(v2*deltat))
    #update the time
    time=time+deltat

#switch the cars back if they were switched
if (switched==1):
    temp=c2
    c2=c1
    c1=temp
#update car positons
p1=c1.gp()
p2=c2.gp()
print ('for time', time)
print (c1.ga())
print (c2.ga())
#check if cars are far enough apart
if(abs(p1-p2)<1):
    print('\nfail')
else:
    print('\nsuccess')
