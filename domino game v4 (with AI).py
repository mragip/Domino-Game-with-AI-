domino_set = []
domino = []

# Creating domino set
drawcond = []
for i in range(0,7):
    for j in range(0,7):
        domino = [i,j]
        if j >= i:
            domino_set.append(domino)
import random
random.shuffle(domino_set)

# Game loop starts
while True:
    #Distribution of domino pieces
    stockset = domino_set[0:14]
    computerset = domino_set[14:21]
    playerset = domino_set[21:9999]

    #Chosing who has the highest pair which ll be the snake piece
    #Player who doesn't have highest snake starts first
    computermax = []
    for i in computerset:
        if i[0] == i[1]:
            computermax.append(i)

    playermax = []
    snake = []
    for i in playerset:
        if i[0] == i[1]:
            playermax.append(i)

    if len(playermax) and len(computermax) == 0:        
        continue

    elif len(playermax) == 0 and len(computermax) != 0:
        snake.append(max(computermax))
        computerset.remove(max(computermax))
        status = "player"
        break

    elif len(playermax) != 0 and len(computermax) == 0:
        snake.append(max(playermax))
        playerset.remove(max(playermax))
        status = "computer"
        break

    elif max(playermax) > max(computermax):
        snake.append(max(playermax))
        playerset.remove(max(playermax))
        status = "computer"
        break

    else:
        snake.append(max(computermax))
        computerset.remove(max(computermax))
        status = "player"
        break

# Winner is the one who consume all pieces in hand
while len(computerset) >= 0 and len(playerset) >= 0:

    #Game screen
    print(70 * "=")
    print("Stock size:", len(stockset))
    print("Computer pieces:", len(computerset))
    print("")

    if len(snake) <= 6:
        print("".join(map(str,snake)))
    else:
        print("".join(map(str,snake[0:3])) + "..." + "".join(map(str,snake[-3::])))
    print("")
    print("Your pieces:")


    if len(playerset) > 0:
        enumplayer = enumerate(playerset)
        for count, i in enumplayer:
            print(f"{count + 1}:{i}")
        print("")

    #Defining end game status, winners and draws      
    if len(snake) >= 8:
        for i in snake:    
            if snake[0][0] == i[0]:
                drawcond.append(i[0])
            if snake[0][0] == i[1]:
                drawcond.append(i[1])
    
    if (snake[0][0] == snake[-1][-1] and len(drawcond) == 8):        
        print("Status: The game is over. It's a draw!")
        break
    
    if len(stockset) == 0:
        print("Status: The game is over. It's a draw!")
        break
    
    elif len(playerset) == 0:
        print("")
        print("Status: The game is over. You won!")
        break

    elif len(computerset) == 0:
        print("")
        print("Status: The game is over. The computer won!")
        break

    #Defining player's each movements placements on snake 
    if status == "player":
        print("Status: It's your turn to make a move. Enter your command.")
        
        while True:
            try:
                pmove = int(input())
            except Exception:
                print("Invalid input. Please try again.")
                continue
            else:
                if abs(pmove) > len(playerset):
                    print("Invalid input. Please try again.")
                    continue       

                elif pmove == 0:
                    stpiece = stockset[random.randint(0,len(stockset)-1)]
                    stockset.remove(stpiece)
                    playerset.append(stpiece)

                elif pmove > 0:
                    if snake[-1][-1] != playerset[pmove - 1][0] and snake[-1][-1] != playerset[pmove - 1][1]: 
                        print("Illegal move. Please try again.")
                        continue
                    
                    elif snake[-1][-1] == playerset[pmove - 1][0]:
                        snake.append(playerset[pmove - 1])
                        del playerset[pmove - 1]

                    elif snake[-1][-1] == playerset[pmove - 1][1]:
                        rot1 = [playerset[pmove - 1][1], playerset[pmove - 1][0]]
                        snake.append(rot1)
                        del playerset[pmove - 1]          

                elif pmove < 0:
                    if snake[0][0] != playerset[abs(pmove) - 1][0] and snake[0][0] != playerset[abs(pmove) -1][1]:
                        print("Illegal move. Please try again.")
                        continue

                    elif snake[0][0] == playerset[abs(pmove) - 1][1]:
                        snake.insert(0,playerset[abs(pmove) -1])
                        del playerset[abs(pmove) - 1]

                    elif snake[0][0] == playerset[abs(pmove) - 1][0]:
                        rot2 = [playerset[abs(pmove) -1][1], playerset[abs(pmove) -1][0]]
                        snake.insert(0,rot2)
                        del playerset[abs(pmove) - 1]                                        
                break

        status = "computer"

    #Defining computer's each movements and its placements on snake
    elif status == "computer":        
        cmovel = [] #possible movement list in hand
        csignl = ["","-"]
        rot3 = [] 
        rot4 = []
        cmovelsc = [] #score list of each number in cmovel

        #score dictionary for each number on pieces
        score = {0:5, 1:3, 2:3, 3:1, 4:3, 5:3, 6:0}
        
        for i,j in computerset:                       
            if snake[-1][-1] == i or snake[0][0] == i or snake[-1][-1] == j or snake[0][0] == j:
                cmovel.append([i,j])
        
        for i,j in cmovel:
            indsc = score[i] + score[j]
            cmovelsc.append(indsc)
           
        #Computer selects highest scored piece to decide movement
        if len(cmovel) != 0:
            cmove = cmovel[cmovelsc.index(max(cmovelsc))]
            print("cmove",cmove)

            if snake[-1][-1] == cmove[0]:
                snake.append(cmove)
                computerset.remove(cmove)

            elif snake[-1][-1] == cmove[1]:
                rot3 = [cmove[1],cmove[0]]
                snake.append(rot3)
                computerset.remove(cmove)

            elif snake[0][0] == cmove[1]:
                snake.insert(0,cmove)
                computerset.remove(cmove)                   

            elif snake[0][0] == cmove[0]:
                rot4 = [cmove[1],cmove[0]]
                snake.insert(0,rot4)
                computerset.remove(cmove)

        if len(cmovel) == 0:
            stpiece = stockset[random.randint(0,len(stockset)-1)]
            stockset.remove(stpiece)
            computerset.append(stpiece)
                               
        cmovel.clear()
        cstop = input("Status: Computer is about to make a move. Press Enter to continue...\n")
        if cstop == "":
            status = "player"
