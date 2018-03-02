shapes =    {  
        "O":{
            0: [[1,1],[1,1]],
            1: [[1,1],[1,1]],
            2: [[1,1],[1,1]],
            3: [[1,1],[1,1]]
            },
        "I":{
            0: [[1,1,1,1]],
            1: [[1],[1],[1],[1]],
            2: [[1,1,1,1]],
            3: [[1],[1],[1],[1]]
            },
        "Z":{
            0: [[1,1,0],[0,1,1]],
            1: [[0,1],[1,1],[1,0]],
            2: [[1,1,0],[0,1,1]],
            3: [[0,1],[1,1],[1,0]]
            },
        "S":{
            0: [[0,1,1],[1,1,0]],
            1: [[1,0],[1,1],[0,1]],
            2: [[0,1,1],[1,1,0]],
            3: [[1,0],[1,1],[0,1]]
            },
        "T":{
            0: [[1,1,1],[0,1,0]],
            1: [[0,1],[1,1],[0,1]],
            2: [[0,1,0],[1,1,1]],
            3: [[1,0],[1,1],[1,0]]
            },
        "L":{
            0: [[1,1,1],[1,0,0]],
            1: [[1,1],[0,1],[0,1]],
            2: [[0,0,1],[1,1,1]],
            3: [[1,0],[1,0],[1,1]]
            },
        "J":{
            0: [[1,1,1],[0,0,1]],
            1: [[0,1],[0,1],[1,1]],
            2: [[1,0,0],[1,1,1]],
            3: [[1,1],[1,0],[1,0]]
            }
        }
        
space = []
space.append([0,0,0,0,0,0,0,0,0,0])
space.append([0,0,0,0,0,0,0,0,0,0])
space.append([0,0,0,0,0,0,0,0,0,0])
space.append([0,0,0,0,0,0,0,0,0,0])
space.append([0,0,0,0,0,0,0,0,0,0])
space.append([0,0,0,0,0,0,0,0,0,0])
space.append([0,0,0,0,0,0,0,0,0,0])
space.append([0,0,0,0,0,0,0,0,0,0])
space.append([0,0,0,0,0,0,0,0,0,0])
space.append([0,0,0,0,0,0,0,0,0,0])
space.append([0,0,0,0,0,0,0,0,0,0])
space.append([0,0,0,0,0,0,0,0,0,0])
space.append([0,0,0,0,0,0,0,0,0,0])
space.append([0,0,0,0,0,0,0,0,0,0])
space.append([0,0,0,0,0,0,0,0,0,0])
space.append([0,0,0,0,0,0,0,0,0,0])
space.append([0,0,0,0,0,0,0,0,0,0])
space.append([0,0,0,0,0,0,0,0,0,0])
space.append([0,0,0,0,0,0,0,0,0,0])
space.append([0,0,0,0,0,0,0,0,0,0])
def zoid_place( col, rot, row, zoid, space):
        if (zoid == "I") and (rot == 1 or rot ==3):
            row+=3

        elif (zoid == "J") and (rot == 1 or rot == 3):
            row+=2
        elif (zoid == "J" ):
            row+=1

        elif (zoid == "L") and (rot == 1 or rot == 3):
            row+=2
        elif (zoid == "L" ):
            row+=1
        
        elif (zoid == "S") and (rot == 1 or rot == 3):
            row+=2
        elif (zoid == "S"):
            row+=1
        
        elif (zoid == "Z") and (rot == 1 or rot ==3):
            row+=2
        elif (zoid == "Z"):
            row+=1
        
        elif (zoid == "T") and (rot == 1 or rot == 3):
            row+=2
        elif (zoid == "T"):
            row+=1

        elif (zoid == "O"):
            row+=1

        x = col
        y = len(space) - row - 1
        ix = x
        iy = y
        ends_game = False
        for i in shapes[zoid][rot]: 
            for j in i:
                if iy < 0:
                    ends_game = True
                if j != 0 and iy >= 0:
                    # print("stamping",iy,ix)
                    space[iy][ix] = 2
                ix += 1
            ix = x
            iy += 1
        
        return space




### if you replace the 
#print(zoid_place(4,0,15,"J",space))
