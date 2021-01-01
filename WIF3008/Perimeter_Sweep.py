import threading

import tello
import time
# import keyboard

# Create Billy
billy = tello.Tello()

# Travel to/from starting checkpoint 0 from/to the charging base
# TODO: settle tobase, get from user
frombase = ["forward", 50, "ccw", 150]
tobase = ["ccw", 150, "forward", 50]

# Flight path to Checkpoint 1 to 5 and back to Checkpoint 0 sequentially
checkpoint = [[1, "cw", 90, "forward", 100], [2, "ccw", 90, "forward", 80], [3, "ccw", 90, "forward", 40],
           [4, "ccw", 90, "forward", 40], [5, "cw", 90, "forward", 60], [0, "ccw", 90, "forward", 40]]

# TODO: reverse everything
backPath = [[1, "cw", 90, "forward", 100], [2, "ccw", 90, "forward", 80], [3, "ccw", 90, "forward", 40],
           [4, "ccw", 90, "forward", 40], [5, "cw", 90, "forward", 60], [0, "ccw", 90, "forward", 40]]


# """ Start new thread for receive Tello response message """
# t = Tello()
recvvThread = threading.Thread(target=billy.send("command", 3))
recvvThread.start()

while True:
    try:
        # Put Tello into command mode
        billy.send("command", 3)


        # Send the takeoff command
        billy.send("takeoff", 7)
        billy.send("streamon", 1)

        print("\n")

        # Start at checkpoint 1 and print destination
        print("From the charging base to the starting checkpoint of sweep pattern.\n")

        billy.send(frombase[0] + " " + str(frombase[1]), 4)
        billy.send(frombase[2] + " " + str(frombase[3]), 4)

        print("Current location: Checkpoint 0 " +  "\n")

        # Billy's flight path
        for i in range(len(checkpoint)):
            if i == len(checkpoint) - 1:
                print("Returning to Checkpoint 0. \n")

            billy.send(checkpoint[i][1] + " " + str(checkpoint[i][2]), 4)
            billy.send(checkpoint[i][3] + " " + str(checkpoint[i][4]), 4)

            print("Arrived at current location: Checkpoint " + str(checkpoint[i][0]) + "\n")
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


        # Close the socket
        # billy.sock.close()
        # break

    except KeyboardInterrupt:
        recvvThread.join()      #kalau boleh nak pause kejap
        recvThread = threading.Thread(target=billy.send("command", 3))
        recvThread.start()
        print("\n1.takeoff \n2. land \n3. ascend 30cm \n4. descend 30cm \n5. forward 30cm \n6. back 30cm \7. clockwise 30degree \n8. counter clockwise 30degree \n9. stop \n10. preplan")

        while True:
            try:
                # Get input from CLI
                msg = input()

                if msg == 1:
                    print("drone is preplan")  # recvThread.join()
                    billy.send("takeoff", 1) # sambung preplan

                if msg == 2:
                    billy.send("land", 3)
                if msg == 3:
                    billy.send("up 30", 1)
                if msg == 4:
                    billy.send("down 30", 1)
                if msg == 5:
                    billy.send("forward 30", 1)
                if msg == 6:
                    billy.send("back 30", 1)
                if msg == 7:
                    billy.send("cw 30", 1)
                if msg == 8:
                    billy.send("ccw 30", 1)
                if msg == 9:
                    billy.send("stop", 1)



            finally:
                break



        # continue


#manual control panel
# choose checkpoint
# choose speed(kiv)


#while no interrupt, proceed auto.
#if suspicious activity, security personal take over,
# click 1 untuk override, tambah speed 2x
# drone stop (hover)
# user control, mintak checkpoint/direction,unit , patah blk/nearest route
#overide stop
# auto jalan blk dari destination, if 0, land.

#!/usr/bin/python3
        # x = 0
        # # Get interruption
        # x = input("Enter username:")
        # print("Username is: " + x)

# #nanti letak gui? press 6 to interrupt?
# while x == 0:
# # Billy's flight path
#     for i in range(len(checkpoint)):
#         if i == len(checkpoint)-1:
#             print("Returning to Checkpoint 0. \n")
#
# # get user variable fromcheckpoint, tocheckpoint
#         billy.send(checkpoint[i][1] + " " + str(checkpoint[i][2]), 4)
#         billy.send(checkpoint[i][3] + " " + str(checkpoint[i][4]), 4)
#
#         print("Arrived at current location: Checkpoint " + str(checkpoint[i][0]) + "\n")
#         time.sleep(4)
#     if x == 6:
#         break
#
# if x == 6:
#     # get next checkpoint
#     billy.receive()
#     billy.send(tobase[0] + " " + str(tobase[1]), 4)




# todo while loop untuk manual input
# todo save last checkpoint








