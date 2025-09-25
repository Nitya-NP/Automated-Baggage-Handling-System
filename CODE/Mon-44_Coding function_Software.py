# CODING FUNCTIONS
"""
Created on Sun Nov 10 02:28:07 2024
"""
import turtle
'''
Turtle set up for the graphical function
'''
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 200
WINDOW_TITLE = ""

# Set up the screen object
turtle.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
screen = turtle.Screen()
screen.title(WINDOW_TITLE)

#set the background color
screen.bgcolor("white")

t = turtle.Turtle()
t.color("black")



def passenger_data(): 
    """
    Parameter:- passenger data from a txt file 
    - makes a list of each line - which gives passengers information 
    - puts those list into one big 2-D list 
    returns that 2-D list
    output- [[Passenger 1 name, First letter of last name, Gate,Destination,Seating class, Arrival status, Baggage weight, Layover status]..]
    """
    
    passenger_list = []
    file= open("passenger_data_v2.txt", "r")    
    for line in file: #takes each line from file    
        line=line.strip().split(",")#splits them by comma
        data=[line[0], #first name
              line[1], #last name
              line[2], #gate
              line[3], #destination
              line[4], #seating_class
              line[5], #arrival status
              float(line[6]), #baggage weight
              line[7]] #layover
        passenger_list.append(data) #puts lists into a list
    file.close()
    return passenger_list



def fleet_data(): 
    """
    Parameter:- fleet data from a txt file 
    - makes a list of each line - which gives plane info 
    - puts those list into one 2-D list 
    returns that 2-D list
    output- [[Plane 1 model, Number of business seats, Number of economy seats, Total number of seats, Gate, Destination, Arrival status, Maximum baggage weight allowed per passenger]..]
    """    
    
    fleet_list = []
    file= open("fleet_data.txt", "r")
    for line in file: #takes each line from file
        line=line.strip().split(",")#splits them by comma
        data=[line[0], #plane model
              int(line[1]), #num of business seats
              int(line[2]), #num of economy seats
              int(line[3]), #num of total seats
              line[4], #gate
              line[5], #destination
              line[6], #arrival
              float(line[7])] #maximum baggage weight per passenger allowed
        fleet_list.append(data)#puts lists into a list
    file.close()
    return fleet_list


def daily_data(passenger_data): 
    """
    Parameter:- data from function passenger_data() 
    This function counts sold business and economy seats according to passengers gate no.
    - Gets the gate no. and seating class they are assigned to from passenger data. 
    - The function then updates the seat count (business or economy) for each gate no. based on the seating class of the passenger.
    
    Returns the 2-D list with the each list having gate no. and business, economy seat count
    output- [[gate no., business seat sold no., economy seat sold no.]..]
    """
  
    passenger_list= passenger_data
    total_seat=[]
    
    for passenger in passenger_list: # Loop through the passenger data
        gate= passenger[2]#gate no.
        seating_class = passenger[4]#seat_class
        found = False
        
        for s in total_seat:# Loop through the total_seat 
            if s[0] == gate: #checks if the gate already exist or not
                found = True #if it does than updates that gate no.
                if seating_class.upper() == 'B':
                    s[1] += 1 #updates the value 
                elif seating_class.upper() == 'E':
                    s[2] += 1 #updates the value
                break
        
        # If the gate is not found, add a new entry
        if not found:
            if seating_class.upper() == 'B':
                total_seat.append([gate, 1, 0])#creates a new list 
            elif seating_class.upper() == 'E':
                total_seat.append([gate, 0, 1])#creates a new list 
    
    return total_seat


def layover(passenger_data,fleet_data): 
    """
    Parameter:- passenger_data() and fleet_data()
    
    This function determines layover flights and passengers who have layovers
    -checks if passenger has layover and if so adds the passenger to a list 
    - it also tracks flights that has layover passengers are in that flight by matching their gate no. and updates the flight list
    
    Returns 2 2-D listss
    -flight_layover -[[Plane 1 model, Number of passengers with layover status]..]
    -passenger_layover [[Passenger 1 first name, intial of the last name, gate no.]..]
    """
    
    flight_layovers=[]
    passengers_layover=[]
    
    for passenger in passenger_data: # Loop through the passenger data
        
        if passenger[7]=="Layover": #checks if has layover or not
            info=[passenger[0],passenger[1],passenger[2]] 
            passengers_layover.append(info) #if it does than adds to the passenger_layover
            in_fleet=False
            
            for plane in fleet_data:  # Loop through the fleet data
                if passenger[2]==plane[4]: #checks if gate number matches
                    for flight in flight_layovers:
                        if flight[0]==plane[0]:#if flight name already in the flight_layover
                            flight[1]+=1 #than updates it
                            in_fleet=True
                    if not in_fleet: #if not then makes a new entry
                        info=[plane[0],1]
                        flight_layovers.append(info)
    
    return flight_layovers,passengers_layover
      


def oversold(passenger_data, fleet_data, daily_data): 
    """
    Parameter:- passenger_data(), fleet_data(),daily_data()
    This function checks for oversold seats in both business and economy classes for each flight.
    
    It compares the number of seats sold for each flight( from`daily_data) with the overall capacity
    of the plane (from `fleet_data`) and checks if any seats are oversold. if there are then calculates how many and add that to a list
    -(this function doesnt use passenger_data as it is already in the daily_data and the information we need are already provided by fleet_data and daily_data)
    
    Returns two 2-D lists: 
    -business class oversold count- [[Plane 1 model, Number of oversold business seats]..]
    -economy class oversold count- [[Plane 1 model, Number of oversold economy seats]..]
    """

    oversold_business = []  
    oversold_economy = []  
    

    for flight in fleet_data: # Loop through the fleet data
        plane_model = flight[0] 
        business_capacity = flight[1]
        economy_capacity = flight[2]
        gate = flight[4] 
        
        for daily in daily_data: # Loop through the daily  data
            if daily[0] == gate: #checks if gate no. matches in daily_data 
                
                business_sold = daily[1]  
                economy_sold = daily[2]
                
                #compares 2 values and gets the max value (if its less than 0 then returns just 0) 
                business_oversold = max(0, business_sold - business_capacity) 
                economy_oversold = max(0, economy_sold - economy_capacity)
                
                #puts into a list
                oversold_business.append([plane_model, business_oversold])
                oversold_economy.append([plane_model, economy_oversold])

    return oversold_business, oversold_economy



def overweight(passenger_data,fleet_data): 

    """
    Parameter: passenger_data(), fleet_data()
    This function finds how many passengers baggage are overweight by taking the max limit of the plane from fleet_data and comparing that to passenger baggage weight.
    if the weight exceed the max weight limit then adds that passenger to a list 
    and according to the plane model it incrementing overweight_count and adds that to a list
    
    Returns 2 2-D lists
    - overweight passengers in the flight- [[plane model, overweight passenger count]..]
    - overweight passengers- [[first name, intials of the last name, gate no., amount of weight exceeded]..]
    """

    overweight_passengers = []
    overweight_flights = []  
    
    # Loop through the fleet data to check overweight luggage
    for plane in fleet_data:
        plane_model = plane[0]  # Plane model in fleet data
        max_weight_limit = plane[7]# Max weight limit based on the 8th column
        gate=plane[4]
        overweight_count = 0  # Counter for overweight passengers for this plane
        
        # Loop through the passenger data
        for passenger in passenger_data:
            if passenger[2]==gate: #if the gate no. of passenger and plan matches
                luggage_weight = passenger[6]  # Luggage weight passenger have
           
                if luggage_weight > max_weight_limit: # Check if the luggage exceeds the max weight limit
                    exceeded_amount = luggage_weight - max_weight_limit
                 
                #adding that to overweight_passenger list with passenger name and ID
                    found=False
                    for i in overweight_passengers:
                        found=False
                    
                    #if the name is already in the list, than it doesn't add that again in the list
                        if passenger[0] == i[0]:
                            found=True
                            break
                
                    if not found:
                        overweight_passengers.append([ 
                        passenger[0],  # First name
                        passenger[1],  # intial of the Last name
                        passenger[2],  # Gate no.
                        round(exceeded_amount, 1)  # How much they exceeded the weight limit, rounded to 1 decimal place
                ])  
                
                    #Incrementing overweight_count
                    overweight_count += 1
        
                
        
        #add total overweight count to overweight_flights with the plane model
        overweight_flights.append([plane_model, overweight_count])
    
    
    return overweight_flights, overweight_passengers

def graphical_Mon_44(oversold_data,overweight_data,layover_data):
    """
    Parameter: oversold_data(), overweight_data(), layover_data()
    This function basically prints an output from oversold, overweight and layover
    for each plane model it gives- oversold business seats, oversold economy seats, overweight baggages and layover passengers
    by using turtle it displays an graphical output with all this information in row of rectangles

    """
    
    oversold_B_data,oversold_E_data=oversold_data
    overweight_flight_data,overweight_passenger_data=overweight_data
    layover_flight_data,layover_passenger_data=layover_data
    
    result_list=[]

    #compares plane model name
    for OSB in oversold_B_data:
        for OSE in oversold_E_data:
            for OW in overweight_flight_data:
                for LO in layover_flight_data:
                    if OSB[0]==OSE[0]==OW[0]==LO[0]: #if they match than adds that plane model info to a list
                        result_list.append([OSB[0], OSB[1],OSE[1],OW[1],LO[1]]) 
                        #[plane model, oversold business seat, oversold economy seat, overweight baggage, total layover passengers]
                        
                        
    #print(result_list) #Testing purposes
                       
    # Initialize the turtle graphics
    t.speed(0)                    
                   
    #Initializing x and y           
    x = -SCREEN_WIDTH / 2 + 30
    y = SCREEN_HEIGHT / 2 - 30
    
    
    for item in result_list:
        t.up()
        t.goto(x, y)
        t.down()
        
        #creates a rectangle for the title- plane model name
        t.color("lightblue")  
        t.begin_fill()
        
        # Draw rectangle
        for _ in range(2):
            t.forward(140)
            t.right(90)
            t.forward(50)
            t.right(90)
        t.end_fill()
        
        #adds the title
        t.color("black")
        t.up()
        t.forward(70)  
        t.right(90)
        t.forward(25)
        
        #This writes the plane model in the blue rectangle
        t.write(item[0], align="center",  font=("Comic Sans MS", 10, "bold"))
        t.backward(25)
        t.left(90)
        t.backward(50)
        
        # Write additional information below the blue rectangle
        t.right(90)
        t.forward(120)
        t.left(90)
        t.forward(50)
        t.write(f"\nOversold Business Seats: {item[1]} \nOversold Economy Seats: {item[2]} \nOverweight Bags: {item[3]} \nLayover Passengers: {item[4]}", align="center",  font=("Comic Sans MS", 8, "normal"))
        
        #moving x position to write the next entry
        x += 170 
    
    t.hideturtle()
      
graphical_Mon_44(oversold(passenger_data(), fleet_data(), daily_data(passenger_data())),overweight(passenger_data(),fleet_data()),layover(passenger_data(), fleet_data()))







