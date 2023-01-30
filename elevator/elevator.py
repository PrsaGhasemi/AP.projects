import numpy as np

class Passenger(object):
    def __init__(self,enter_floor,target_floor,name):
        '''
        Passsegner class attributes
        '''
        self.enter_floor = enter_floor
        self.target_floor = target_floor
        self.name = name
        if enter_floor < target_floor:
            self.state = 'up'
        elif enter_floor > target_floor:
            self.state = 'down'
        else:
            raise ValueError('Passenger {} does not need elevatpr.'.format(name) )
        self.waiting_time=0
    
    def getName(self):
        return self.name

    def getState(self):
        return self.state
    
    def getEnterFloor(self):
        return self.enter_floor
    
    def getTargetFloor(self):
        return self.target_floor
    
    def getWaitingTime(self):
        return self.waiting_time
    
    def updateWaitingTime(self):
        self.waiting_time = self.getWaitingTime() + 1

class ElevatorTarget(object):
    def __init__(self, floor, state):
        self.floor = floor
        self.state = state
        
    def __str__(self):
        return '- ({},{})'.format(self.floor, self.state)
        
    def getFloor(self):
        return self.floor
    
    def getState(self):
        return self.state
    
    
    def distance(self, end, min_floor, max_floor):
        if self.getState() == 'up':
            if end.getState() == 'up':
                if self.getFloor() <= end.getFloor():
                    return  end.getFloor() - self.getFloor()
                else:
                    return (max_floor-min_floor)*2-self.getFloor()+end.getFloor()
                
            elif end.getState()=='down':
                return max_floor * 2 - self.getFloor()-end.getFloor()

            elif end.getState()==None:
                if self.getFloor()<=end.getFloor():
                    return  end.getFloor() - self.getFloor()
                else:
                    return max_floor*2-self.getFloor()-end.getFloor()

        elif self.getState()=='down':
            if end.getState()=='up':
                return self.getFloor() + end.getFloor() - min_floor * 2
            
            elif end.getState()=='down':
                if self.getFloor()>=end.getFloor():
                    return self.getFloor()-end.getFloor()
                else:
                    return (max_floor-min_floor)*2 + self.getFloor() - end.getFloor()
                
            elif end.getState() == None:
                if self.getFloor()>=end.getFloor():
                    return  self.getFloor()-end.getFloor()
                else:
                    return self.getFloor()+end.getFloor()-min_floor*2
        
        elif self.getState() == None:
            return abs(end.getFloor() - self.getFloor())
        
class BasicElevator(object):
    
    def __init__(self, min_floor, max_floor):
        self.max_floor=max_floor
        self.min_floor=min_floor
        self.current_floor=min_floor
        self.state=None
        self.target_list = []
        self.travel_distance = 0
    
    def getMaxFloor(self):
        return self.max_floor
    
    def getMinFloor(self):
        return self.min_floor
    
    def getState(self):
        return self.state
    
    def setState(self, new_state):
        '''
        Args:
        new_state: string 'up','down' or None when standby
        '''
        self.state = new_state
    
    def getCurrentFloor(self):
        return self.current_floor
    
    def updateCurrentFloor(self):
        if self.getState()=='up':
            if self.getCurrentFloor() == self.getMaxFloor():
                raise ValueError('Exceed max floor')    
            else: self.current_floor=self.getCurrentFloor()+1
                
        if self.getState()=='down':
            if self.getCurrentFloor()==self.getMinFloor():
                raise ValueError('Exceed min floor')    
            else: self.current_floor=self.getCurrentFloor()-1
    
    def getTargetList(self):
        return self.target_list
    
    def setTargetList(self,new_list):
        self.target_list = new_list
    
    def checkTargetList(self):
        '''
        eliminate reached target from top of the target list
        '''
        old_list = self.getTargetList()
        current_floor = self.getCurrentFloor()
        current_state = self.getState()
        
        if old_list == []:
            pass
        
        elif old_list[0].getFloor() == current_floor:
            self.setTargetList(old_list.copy()[1:])
            if old_list[0].getState() != None:
                self.setState(old_list[0].getState())
        
        if self.getTargetList() == []:
            self.setState(None)
                
    def addTargetList(self, new_target):
        '''
        Args:
        new_target: a ElevatorTarget object
        '''
        old_list = self.getTargetList()
        current_state = ElevatorTarget(self.getCurrentFloor(), self.getState())
        min_floor = self.getMinFloor()
        max_floor = self.getMaxFloor()
            
        if new_target.getFloor() not in [target.getFloor() for target in old_list]:
            old_list.append(new_target)
            new_list = [old_list[i] for i in np.argsort([current_state.distance(i,min_floor,max_floor) for i in old_list])]
            self.setTargetList(new_list)
            
        else:
            new_list=[]
            for target in old_list:
                if target.getFloor() == new_target.getFloor():
                    if target.getState() == None:
                        new_list.append(new_target)
                    elif new_target.getState() == None:
                        new_list.append(target)
                    elif new_target.getState() == target.getState():
                        new_list.append(target)
                    else:
                        new_list.append(target)
                        new_list.append(new_target)
                else:
                    new_list.append(target)
                    
            ordered_list=[new_list[i] for i in np.argsort([current_state.distance(i,min_floor,max_floor) for i in new_list])]
            self.setTargetList(ordered_list)
                            
    def passengerTakeOff(self, current_passenger):
        '''
        Args:
        current_passenger: a list of passengers in this elevator'''
        new_passenger=[]
        tookoff_passenger=[]
        for passenger in current_passenger:
            if passenger.getTargetFloor() == self.getCurrentFloor():
                #print('- Passenger took off:',passenger.getName())
                #print('- Total waiting time:',passenger.getWaitingTime())
                #print(passenger.getName(),passenger.getWaitingTime())
                tookoff_passenger.append(passenger)
            else:
                new_passenger.append(passenger)
        return (new_passenger,tookoff_passenger)
    
    def passengerTakeOn(self,waiting_passenger):
        '''
        Args:
        waiting_passenger: a dictionary with floor as keys and list of passengers as values
        
        Returns:
        a tuple (list of new passenger,dictionary of new waiting passenger)
        '''
        new_waiting_passenger = []
        new_takeon_passenger = []
        floor = self.getCurrentFloor()
        
        if self.getTargetList() == []:
            return ([], waiting_passenger)
            
        elif floor != self.getTargetList()[0].getFloor():
            return ([], waiting_passenger)
        
        elif waiting_passenger[floor] == []:
            return ([], waiting_passenger)
        
        else:
            for passenger in waiting_passenger[floor]:
                if passenger.getState() == self.getTargetList()[0].getState():
                    new_takeon_passenger.append(passenger)
                else:
                    new_waiting_passenger.append(passenger)              
            waiting_passenger[floor] = new_waiting_passenger
            return (new_takeon_passenger, waiting_passenger)
        
    def updateState(self):
        if self.getTargetList() == []:
            pass
        else:
            next_target = self.getTargetList()[0]
            current_floor = self.getCurrentFloor()
            if current_floor > next_target.getFloor():
                self.setState('down')
            elif current_floor < next_target.getFloor():
                self.setState('up')
            else:
                self.setState(next_target.getState())
    
    def getDistance(self):
        return self.travel_distance
    
    def updateDistance(self):
        if self.getState() != None:
            self.travel_distance=self.getDistance() + 1