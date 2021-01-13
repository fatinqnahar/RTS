
import threading

import tello
import time
# import keyboard

# Create Billy
billy = tello.Tello()

# Travel to/from starting checkpoint 0 from/to the charging base
# TODO: settle tobase, get from user
frombase = ["forward", 50, "ccw", 60]
tobase = ["ccw", 150, "forward", 50]

# Flight path to Checkpoint 1 to 5 and back to Checkpoint 0 sequentially
checkpoint = [[1, "cw", 90, "forward", 100], [2, "ccw", 90, "forward", 80], [3, "ccw", 90, "forward", 40],
           [4, "ccw", 90, "forward", 40], [5, "cw", 90, "forward", 60], [0, "ccw", 90, "forward", 40]]

# TODO: reverse everything
backPath = [[1, "cw", 90, "forward", 100], [2, "ccw", 90, "forward", 80], [3, "ccw", 90, "forward", 40],
           [4, "ccw", 90, "forward", 40], [5, "cw", 90, "forward", 60], [0, "ccw", 90, "forward", 40]]

backtoPP = []
recvvThread = threading.Thread(target=billy.send("command", 3))
recvvThread.start()
count = 0
newforward = 0
currentcp = []
current = 0
inputcount = 0
newdirection = ""
newdegree = 0
while True:
    try:
        # Put Tello into command mode
        # billy.send("command", 3)

        if count == 0:
            # Send the takeoff command
            billy.send("takeoff", 7)
            billy.send("streamon", 1)

            print("\n")

            # Start at checkpoint 1 and print destination
            print("From the charging base to the starting checkpoint of sweep pattern.\n")

            billy.send(frombase[0] + " " + str(frombase[1]), 4)
            billy.send(frombase[2] + " " + str(frombase[3]), 4)

            print("Current location: Checkpoint 0 " +  "\n")
            currentcp.append(0)
            # Billy's flight path

            for i in range(len(checkpoint)):
                if i == len(checkpoint) - 1:
                    print("Returning to Checkpoint 0. \n")

                billy.send(checkpoint[i][1] + " " + str(checkpoint[i][2]), 4)
                billy.send(checkpoint[i][3] + " " + str(checkpoint[i][4]), 4)

                print("Arrived at current location: Checkpoint " + str(checkpoint[i][0]) + "\n")
                currentcp.append(checkpoint[i][0])
                time.sleep(4)


            # Reach back at Checkpoint 0
            print("Complete sweep. Return to charging base.\n")
            billy.send(tobase[0] + " " + str(tobase[1]), 4)
            billy.send(tobase[2] + " " + str(tobase[3]), 4)


            # Turn to original direction before land
            print("Turn to original direction before land.\n")
            billy.send("cw 180", 4)

            # Land
            billy.send("land", 3)
            billy.send("streamoff", 1)

        else:
            for i in range(current, len(checkpoint)):

                if i == current:

                    for j in reversed(range(len(backtoPP))):
                        billy.send(backtoPP[j][0] + " " + str(backtoPP[j][1]), 4)
                        time.sleep(1)

                    billy.send(checkpoint[i][1] + " " + str(checkpoint[i][2]), 4)
                    billy.send(checkpoint[i][3] + " " + str(checkpoint[i][4]), 4)

                if i != current:
                    billy.send(checkpoint[i][1] + " " + str(checkpoint[i][2]), 4)
                    billy.send(checkpoint[i][3] + " " + str(checkpoint[i][4]), 4)

                print("Arrived at current location: Checkpoint " + str(checkpoint[i][0]) + "\n")
                currentcp.append(checkpoint[i][0])
                time.sleep(4)

            # Reach back at Checkpoint 0
            print("Complete sweep. Return to charging base.\n")
            billy.send(tobase[0] + " " + str(tobase[1]), 4)
            billy.send(tobase[2] + " " + str(tobase[3]), 4)

            # Turn to original direction before land
            print("Turn to original direction before land.\n")
            billy.send("cw 180", 4)

            # Land
            billy.send("land", 3)
            billy.send("streamoff", 1)

        break

    except KeyboardInterrupt:
        # backtoPP.append([newdirection, newdegree]) KIV
        backtoPP.clear()
        count += 1
        current = currentcp[len(currentcp)-1]
        recvvThread.join()
        recvThread = threading.Thread(target=billy.send("command", 3))
        recvThread.start()

        print("Current checkpoint: "+str(current))
        while True:
            try:
                # Get input from CLI
                while inputcount >= 0:
                    print("\n1. ascend 30cm \n2. descend 30cm \n3. forward 30cm \n4. back 30cm \n5. clockwise 30degree \n6. counter clockwise 30degree \n7. stop \n8. preplan")

                    msg = input()
                    inputcount += 1


                    if msg == "1":
                        billy.send("up 30", 4)
                    if msg == "2":
                        billy.send("down 30", 4)
                    if msg == "3":
                        billy.send("forward 30", 4)
                        # newforward = 30
                        backtoPP.append(["back", 30])
                    if msg == "4":
                        billy.send("back 30", 4)
                        # newforward = -30
                        backtoPP.append(["forward", 30])
                    if msg == "5":
                        billy.send("cw 30", 4)
                        backtoPP.append(["ccw", 30])
                    if msg == "6":
                        billy.send("ccw 30", 4)
                        backtoPP.append(["cw", 30])
                    if msg == "7":
                        billy.send("stop", 4)
                    if msg == "8":
                        break

                time.sleep(4)
                print("\n")
                print(backtoPP)

                print("Back to preplan route \n")
                time.sleep(2)


            finally:
                break



                # continue

   # break
#manual control panel
# choose checkpoint
