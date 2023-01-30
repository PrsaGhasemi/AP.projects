import time
from tkinter import *
from elevator import *
import random


def timesteps(n, elevator):
    min_floor = elevator.getMinFloor()
    max_floor = elevator.getMaxFloor()
    counter = 0
    waiting_passenger = {}
    for i in range(min_floor, max_floor + 1):
        waiting_passenger[i] = []
    passenger_1 = []
    
    master = Tk()
    w = Canvas(master, width=1000, height=520)
    w.pack()
    w.create_rectangle(70, 10, 170, 510, fill = "white")
    
    for i in range(1, 10):
        w.create_line(70, 50 * i + 10, 170, 50 * i + 10)
        
    for i in range(10):
        w.create_text(20, 50 * i + 18, anchor = NW, text = str(10-i) + 'F', font = ('Arial', 15))
        
    w.create_text(480, 30, anchor = NW, text = 'Passengers take off: ')
    w.create_text(480, 150, anchor = NW, text = 'Passengers take on: ')
    w.create_text(480, 270, anchor = NW, text = 'Passengers in the elevator: ')
    
    master.update()
    
    for i in range(n):
        timestep_label = w.create_text(480, 10, anchor = NW, text='Timestep ' + str(i))
        
        elevator.updateCurrentFloor()
        
        floor = elevator.getCurrentFloor()
        elevator_sqr = w.create_rectangle(72, (10 - floor) * 50 + 12, 168, (10 - floor) * 50 + 58, fill = "violet")
        
        elevator.updateDistance()

        draw_passenger_wait = []
        text_passenger_wait = []
        for f in waiting_passenger:
            for i, p in enumerate(waiting_passenger[f]):
                row = i // 3
                col = i % 3
                draw_passenger_wait.append(w.create_rectangle(172+col*100, 
                                                              (10-f)*50+12+row*25, 
                                                              192+col*100,
                                                              (10-f)*50+32+row*25, 
                                                              fill = "red"))
                text_passenger_wait.append(w.create_text(200+col*100,
                                                         (10-f)*50+12+row*25,
                                                         anchor=NW,
                                                         text=p.getName()+'-'+p.getState()))
        
        draw_passenger_on = []
        text_passenger_on = []
        for i,p in enumerate(passenger_1):
            row = i // 4
            col = i % 4
            draw_passenger_on.append(w.create_rectangle(75+col*10,
                                                        (10-floor)*50+15+row*10,
                                                        85+col*10,
                                                        (10-floor)*50+25+row*10,
                                                        fill = 'blue'))
            text_passenger_on.append(w.create_text(480, 
                                           290+20*i, 
                                           anchor=NW,
                                           text=p.getName()+' heading to '+str(p.getTargetFloor())+'F'))
        master.update()
        time.sleep(1)
        
        passenger_1, tookoff_passenger = elevator.passengerTakeOff(passenger_1)
        
        for p in draw_passenger_on:
            w.delete(p)
        for p in text_passenger_on:
            w.delete(p)
            
        draw_passenger_off = []
        
        for i, p in enumerate(tookoff_passenger):
            draw_passenger_off.append(w.create_text(480, 
                                                    50+20*i, 
                                                    anchor=NW,
                                                    text=p.getName()+' waited for '+str(p.getWaitingTime())+' s'))
        
        draw_passenger_on = []
        text_passenger_on = []
        for i, p in enumerate(passenger_1):
            row = i // 4
            col = i % 4
            draw_passenger_on.append(w.create_rectangle(75+col*10,
                                                        (10-floor)*50+15+row*10,
                                                        85+col*10,
                                                        (10-floor)*50+25+row*10,fill = 'blue'))
            text_passenger_on.append(w.create_text(480, 
                                                   290+20*i, 
                                                   anchor=NW,
                                                   text=p.getName()+' heading to '+str(p.getTargetFloor())+'F'))
            
        master.update()
        time.sleep(1)
        
        new_takeon, waiting_passenger = elevator.passengerTakeOn(waiting_passenger)
                
        new_target_text = []
        for i, p in enumerate(new_takeon):
            row = (i+len(passenger_1)) // 4
            col = (i+len(passenger_1)) % 4
            draw_passenger_on.append(w.create_rectangle(75+col*10,
                                                        (10-floor)*50+15+row*10,
                                                        85+col*10,
                                                        (10-floor)*50+25+row*10,
                                                        fill = 'blue'))
            new_target_text.append(w.create_text(480, 
                                                 170+20*i, 
                                                 anchor=NW,
                                                 text=p.getName()+' heading to '+str(p.getTargetFloor())+'F'))
            text_passenger_on.append(w.create_text(480, 
                                                   290+20*(i+len(passenger_1)), 
                                                   anchor=NW,
                                                   text=p.getName()+' heading to '+str(p.getTargetFloor())+'F'))
        passenger_1 = passenger_1 + new_takeon
        
        elevator.checkTargetList()
        
        for new_passenger in new_takeon:
            elevator.addTargetList(ElevatorTarget(new_passenger.getTargetFloor(),None))
        
        if random.random() > 0.5:
            enter_floor = int(min_floor+np.floor(random.random()*(max_floor-min_floor)))
            target_floor = int(min_floor+np.floor(random.random()*(max_floor-min_floor)))
            if enter_floor != target_floor:
                name = 'p'+ str(counter)
                counter += 1
                person = Passenger(enter_floor, target_floor, name)
                elevator.addTargetList(ElevatorTarget(person.getEnterFloor(), person.getState()))
                waiting_passenger[enter_floor] = waiting_passenger[enter_floor] + [person]
        
        for p in draw_passenger_wait:
            w.delete(p)    
        for p in text_passenger_wait:
            w.delete(p)
            
        draw_passenger_wait = []
        text_passenger_wait = []
        for f in waiting_passenger:
            for i, p in enumerate(waiting_passenger[f]):
                row = i // 3
                col = i % 3
                draw_passenger_wait.append(w.create_rectangle(172+col*100, 
                                                              (10-f)*50+12+row*25, 
                                                              192+col*100,
                                                              (10-f)*50+32+row*25, 
                                                              fill = "red"))
                text_passenger_wait.append(w.create_text(200+col*100,
                                                         (10-f)*50+12+row*25,
                                                         anchor=NW,
                                                         text=p.getName()+'-'+p.getState()))
        master.update()
        time.sleep(1)

        elevator.updateState()
        
        for f in waiting_passenger:
            temp = []
            for passenger in waiting_passenger[f]:
                passenger.updateWaitingTime()
                temp.append(passenger)
            waiting_passenger[f] = temp      
        
        w.delete(timestep_label)
        w.delete(elevator_sqr)
        for p in draw_passenger_on:
            w.delete(p)
        
        for p in draw_passenger_off:
            w.delete(p)
        
        for p in new_target_text:
            w.delete(p)
        
        for p in draw_passenger_wait:
            w.delete(p)
            
        for p in text_passenger_wait:
            w.delete(p)
        
        for p in text_passenger_on:
            w.delete(p)
                                    
        
    mainloop()