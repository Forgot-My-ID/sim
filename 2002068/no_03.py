import random


total_cost = 0
total_income = 0
total_profit_loss = 0  
num_games = 10  

for game in range(num_games):
    h = 0  
    t = 0  
    cost = 0 
    while True:
        cost += 1 
        total_cost += 1
        
        
        roll = random.randint(1, 6)
        
       
        if roll % 2 == 0: 
            h += 1
        else:  
            t += 1
        
       
        dif = abs(h - t)
        
        
        if dif >= 20:
            total_income += 20  
            print(f"Game {game+1}: Game over after {cost} rolls. Won $20 (Cost was ${cost})")
            break  

   
    game_profit_loss = 20 - cost  
    total_profit_loss += game_profit_loss


print(f'Total Cost: ${total_cost} | Total Income: ${total_income}')
print(f'Total Profit/Loss: ${total_profit_loss}')
