#!/usr/bin/env python3

'''
Ethernet learning switch in Python: HW3.

Note that this file currently has the code to implement a "hub"
in it, not a learning switch.  (I.e., it's currently a switch
that doesn't learn.)
'''
from switchyard.lib.address import *
from switchyard.lib.packet import *
from switchyard.lib.common import *
import time



def switchy_main(net):
    my_interfaces = net.interfaces() 
    print("\nmy_interfaces: " + str(my_interfaces))
    mymacs = [intf.ethaddr for intf in my_interfaces]
    print("mymacs: " + str(mymacs) + "\n")
    size = 0
    srclist = list()
    devlist = list()
    #timelist = []
    print("hi")
    start_time = time.time()
    print("slkdfjasdlkjfalskdjf")
    while True:
        #global ft
        try:
            dev,packet = net.recv_packet() #try to receive a pkt from any available device, block until one is received
            print("dev: " + dev)
        except NoPackets:
            continue
        except Shutdown:
            return
       
        print("help")

        log_debug ("In {} received packet {} on {}".format(net.name, packet, dev))
        if packet[0].dst in mymacs:  # TODO write a test to see what happens when pkt intended for it
            log_debug ("Packet intended for me")
            print("packet intended for me")

 

        else:
         
            if (str(packet[0].dst) == "ff:ff:ff:ff:ff:ff"):
                print("broadcast address")
                
                for intf in my_interfaces:
                    if dev != intf.name:
                        #print(intf.name)
                        log_debug ("Flooding packet {} to {}".format(packet, intf.name))
                        net.send_packet(intf.name, packet) #send packet from current int port
                        break

            print("got to 1")
            # table update block, size check
      
            # check if the ft contains the source address
            if ((packet[0].src) in srclist):
                print("sourcelist contains " + packet[0].src + " already")

                # check which index the source is at in srclist
                for i, j in enumerate(srclist):
                   if (j == packet[0].src):
                       ind = i
                       # check the port at the same index in the devlist
                       if (devlist[i] == dev):
                           # reset time elapsed in timelist to 0
                           start_time = time.time()
                       # if not the same then update the src address & update time
                       else:
                           srclist[i] = packet[0].src
                           start_time = time.time()

            # if not found, then add it
            else:
                print("added to ft: "+ dev)
                devlist.append(dev)
                srclist.append(packet[0].src)
                #timelist.append(0)

            
            # check if entry for destination exists in the forwarding table
            if ((packet[0].dst) in srclist):
                for i,j in enumerate(srclist): # find index of the destination
                   if (j == packet[0].dst):
                       ind = i
                       # get the device for that destination address
                       device = devlist[i]
                       # forward packet
                       net.send_packet(device, packet)
                
            else:
                # broadcast to all ports except on the incoming port
                log_debug ("Flooding packet {} to {}".format(packet, intf.name))
                net.send_packet(intf.name, packet) #send packet from current int port
       
        current_time = time.time()
        diff = current_time - start_time
        print (diff)
        if diff > 10:
            # if 10 seconds have elapsed, remove an entry from the list
            devlist.pop(0)
            srclist.pop(0)

       # print("printing entire ft...")
       # for n in enumerate(srclist):
       #     print("src: "+srclist[n]+ " dev: "+devlist[n])


       # TODO if destination is that broadcast address, then send it out over everything
    net.shutdown()