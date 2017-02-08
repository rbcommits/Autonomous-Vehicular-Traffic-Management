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

#assume car 2 is in front

#create the first instance of a car
c1=Car(1)
#create second instance of a car
c2=Car(2)
#initialize time when car 2 enters region 0
time=0
#change in time 
deltat=0.1

#initialize position and velocity for car 1 and 2
c1.sa(4,40)
c2.sa(4,37)
#pull values from car instances
(p1,v1,t1)=c1.ga()
(p2,v2,t2)=c2.ga()
switched=0
#store values for future use
p1l=40
p2l=37
v1l=4
v2l=4

#simulation
sim=0
k=0

#loop run on car 1
while(sim<120):
    print 'simulation time', sim
    print 'time', time
    #get current values of all cars
    (p1,v1,t1)=c1.ga()
    (p2,v2,t2)=c2.ga()
    #if the distance to the next car is too small
    if (p1<p2+3):
        #if v2 slows down
        if(v2<=v2l and v1>=v2):
            v1l=v1                  #to be shared with the car behind it
            c1.sv(v1-deltat)        #note the change of v1 is always the same as v2
            print 'if 1'
        #this case should never happen
        elif(v2>v2l and v1>=v2):
            v1l=v1                  #to be shared with the car behind it
            c1.sv(v1-deltat)
            print'if 2'
        #this case should never happen
        elif(v2<=v2l and v1<v2):
            v1l=v1                  #to be shared with the car behind it
            c1.sv(v1+deltat)
            print 'if 3'
        elif(v2>v2l and v1<v2):
            v1l=v1                  #to be shared with the car behind it
            c1.sv(v1+deltat)
            print 'if 4'
    #simulate v2 slowing down to test v1
    if(sim>k+90 and sim<k+110):
        if(sim>=k+90 and sim<k+100):
            v2l=v2
            c2.sv(v2-deltat)
        elif(sim>=k+100 and sim<k+109):
            v2l=v2
            c2.sv(v2+deltat)
        elif(sim==k+110):
            v2l=v2
            c2.v2(4)
            k=k+100
    sim=sim+1
    #print useful information
    print c1.ga()
    print c2.ga()
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
print c1.ga()
print c2.ga()
#check if cars are far enough apart
if(abs(p1-p2)<2.9):
    print'\nfail'
else:
    print'\nsuccess'
