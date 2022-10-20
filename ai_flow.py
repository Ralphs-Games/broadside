

    while run_def_AI:
        if harborCheckedforRedScum == 0:
            for i in range (1,11):  # search by ship, check red fleet (1-10)
                if pieceArray[i].p_row_num > 0 and pieceArray[i].p_row_num < 7:  # check for red ships in the harbor

                    #find a ship & move it to empty row, esp row #1, if any are empty
                    for i in range (1,5):  # for rows 1 - 4
                        if numInRow[i] == 0:
                            for j in range (2,7):  # for rows 2 - 6
                                if numInRow[j] > 0:
                                    for k in range (11,21):  # search blue fleet
                                        if pieceArray[k].p_row_num == j:  # check for blue ships in row j
                                            break
                            for j in range (2,7):  # for rows 2 - 6
                                if numInRow[j] > 1:
                            for j in range (1,7):  # for rows 1 - 6
                                if numInRow[j] > 2:
                            moveCheck()
                            if moveValid == 1:
                                shipNumLookup()
                                #run_def_AI = False
                                break

                    #RH try this...
                    if enemy_row == 1:
                        for i in range (11,21):  # search blue fleet
                            if pieceArray[i].p_row_num == 1:   # check for blue ships in row 1 if Red there
                                    new_sq_col = enemy_col + 2
                                    new_sq_col = enemy_col - 2
                                moveCheck()
                                if moveValid == 1:
                                    shipNumLookup()
                                    click.play()
                                    #run_def_AI = False
                                    break

                    for j in range (11,21):  # search by ship, check blue fleet (11-20)
                    #    if enemy_row == 1:
                    #        if pieceArray[j].p_row_num == 1:   # check for blue ships in row 1 if Red there
                        # check for crossing the T attacks...
                        if pieceArray[j].p_row_num == enemy_row - 1:  # check for blue ships in adjacent row
                            if pieceArray[i].direction == 0 or pieceArray[i].direction == 180:
                                print("T attack!")
                                moveCheck()
                                if moveValid == 1:
                                    break
                        if pieceArray[j].p_row_num == enemy_row + 1:  # check for blue ships in adjacent row
                        if pieceArray[j].p_col_num == enemy_col - 1:  # check for blue ships in adjacent col
                        if pieceArray[j].p_col_num == enemy_col + 1:  # check for blue ships in adjacent col

                    # end 1st inside for loop

                    if moveValid == 0:

                        for j in range (11,21):  # search by ship, check blue fleet (11-20)
                            # no T attacks, now check for broadside attacks...
                            if pieceArray[j].p_row_num == enemy_row - 1:  # check for blue ships in adjacent row
                                moveCheck()
                                if moveValid == 1:
                                    break
                            if pieceArray[j].p_row_num == enemy_row + 1:  # check for blue ships in adjacent row
                            if pieceArray[j].p_col_num == enemy_col - 1:  # check for blue ships in adjacent col
                            if pieceArray[j].p_col_num == enemy_col + 1:  # check for blue ships in adjacent col
                    # end 2nd inside for loop

                #print("Red fleet inside the harbor, done checking for an attack move:")
                # AI result?
                if moveValid == 1:
                    break
                elif moveValid == 0:
                    print("AI can't find an attack move... check next red ship...")
                    #harborCheckedforRedScum = 1
                    sq_row = 0     # reset to new click mode
                    sq_col = 0
                    shipNumLookup()  # to clear it

            # end for loop
            harborCheckedforRedScum = 1
            print("done checking for Red fleet inside the harbor...")
            if moveValid == 1:
                shipNumLookup()
                run_def_AI = False
            elif moveValid == 0:
                print("# AI can't find an attack move...")
                print("trying the list instead...")

        ##################################
        elif harborCheckedforRedScum == 1:

            if AImoveIndex < AImoveIndexSize:   # we have index moves left
                for i in range(AImoveIndex,AImoveIndexSize):
                    shipNumLookup()
                    if shipSelected > 10:
                        AImoveIndex = i
                        break  # out of for loop
                if shipSelected > 10:
                    moveCheck()
                    if moveValid == 1:
                        AImoveIndex = AImoveIndex + 1
                        run_def_AI = False
                    elif moveValid == 0:
                        print("try again...")
                        AImoveIndex = AImoveIndex + 1
                    if AImoveIndex == (AImoveIndexSize - 1):   # can't increment any further
                        print("list moves maxxed out... this is the last one")

                elif shipSelected <= 10:
                    AImoveIndex = AImoveIndex + 1
                    sq_row = 0     # reset to new click mode
                    sq_col = 0
                    shipNumLookup()  # to clear it

            elif AImoveIndex == AImoveIndexSize:   # can't increment any further  # see if there are any other defensive moves we can make...

                # move to cover the merchant ships: row 0, col 4/6/8/10
                print("move to cover the merchant ships...")
                for j in range (4,12,2):   # for cols 4,6,8,10
                    shipNumLookup()
                    if pieceArray[shipSelected].shipType == 3:  # merchant in that square (column)
                        sq_row = 1
                        sq_col = j
                        shipNumLookup()
                        if pieceArray[shipSelected].shipType == 0:  # no ship covering
                            for i in range (11,21):    # check blue ships
                                if pieceArray[shipSelected].p_col_num == j and pieceArray[i].p_row_num != 1:  # move up in same column to cover
                                    moveCheck()
                                    if moveValid == 1:
                                        click.play()
                                        run_def_AI = False   # ends the while loop! RH
                                        break
                                elif pieceArray[shipSelected].p_col_num != j and pieceArray[i].p_row_num == 1:  # move in same row to cover
                                    moveCheck()
                                    if moveValid == 1:
                                        click.play()
                                        run_def_AI = False   # ends the while loop! RH
                                        break

                # if Red in row 1 check for blue ships there, move to block access to merchants
                if enemy_row == 1:
                    for i in range (11,21):  # search blue fleet
                        if pieceArray[i].p_row_num == 1:   
                            if pieceArray[i].p_col_num > enemy_col:
                                new_sq_col = enemy_col + 2
                            elif pieceArray[i].p_col_num < enemy_col:
                                new_sq_col = enemy_col - 2
                            moveCheck()
                            if moveValid == 1:
                                click.play()
                                run_def_AI = False   # ends the while loop! RH
                                break


                # check blue fleet (11-20) to find empty rows in the harbor
                numInRow = [0,0,0,0,0,0,0]  # 7 members for rows 1 - 6
                for i in range (11,21):  
                    for j in range (1,7):  # for rows 1 - 6
                        if pieceArray[i].p_row_num == j:  # check for blue ships in row 1
                            numInRow[j] = numInRow[j] + 1

                #find a ship & move it to empty row, esp row #1, if any are empty
                for i in range (1,5):  # for rows 1 - 4
                    if numInRow[i] == 0:
                        for j in range (2,7):  # for rows 5 - 6
                            if numInRow[j] > 0:
                                for k in range (11,21):  # search blue fleet
                                    if pieceArray[k].p_row_num == j:  # check for blue ships in row j
                                        new_sq_row = i
                                        break
                        for j in range (2,7):  # for rows 1 - 6
                            if numInRow[j] > 1:
                                for k in range (11,21):  # search blue fleet
                                    if pieceArray[k].p_row_num == j:  # check for blue ships in row j
                                        new_sq_row = i
                                        break
                        for j in range (1,7):  # for rows 1 - 6
                            if numInRow[j] > 2:
                                for k in range (11,21):  # search blue fleet
                                    if pieceArray[k].p_row_num == j and pieceArray[k].num_masts > 1:  # check for blue ships in row j
                                        new_sq_row = i
                                        break
                        moveCheck()
                        if moveValid == 1:
                            click.play()
                            run_def_AI = False   # ends the while loop! RH
                            break
                        elif moveValid == 0:
                            print("trying again...")
                            shipNumLookup()  # to clear it

                # or else free up defenders in entrances...
                if moveValid == 0:
                    shipNumLookup()
                    if shipSelected > 10:
                    else: 
                        shipNumLookup()
                        if shipSelected > 10:
                        else: 
                            shipNumLookup()
                            if shipSelected > 10:
                moveCheck()
                if moveValid == 1:
                    click.play()
                    run_def_AI = False   # ends the while loop! RH
                # time killing moves...
                elif moveValid == 0:
                    if moveValid == 0:
                        shipNumLookup()
                        if shipSelected > 10:
                        else: 
                            shipNumLookup()
                            if shipSelected > 10:
                    moveCheck()
                    if moveValid == 1:
                        click.play()
                        run_def_AI = False
                    elif moveValid == 0:
                        print("AI is all out of ideas...")
                        shipNumLookup()
                        run_def_AI = False   # ends the while loop! RH


                ## reset to new click mode if no move found
                #new_sq_row = 0
                #new_sq_col = 0
                #sq_row = 0     
                #sq_col = 0
                #run_def_AI = False

    # end while run_def_AI
# end Defensive_AI():
