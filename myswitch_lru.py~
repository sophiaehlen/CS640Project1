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

forwardingTable = {}

def switchy_main(net):
    my_interfaces = net.interfaces() 
    mymacs = [intf.ethaddr for intf in my_interfaces]
    size = 0
    while True:
        global forwardingTable
        
        try:
            dev,packet = net.recv_packet()
        except NoPackets:
            continue
        except Shutdown:
            return
        print ("\n")
        log_debug ("In {} received packet {} on {}".format(net.name, packet, dev))
        if packet[0].dst in mymacs:
            log_debug ("Packet intended for me")
            
        else:
            found = False
            if(str(packet[0].dst) == "ff:ff:ff:ff:ff:ff"):
                print("boadcast address")
                found = True
                for intf in my_interfaces:
                    if dev != intf.name:
                        log_debug ("Flooding packet {} to {}".format(packet, intf.name))
                        net.send_packet(intf.name, packet)
 
            if(size >= 5):
                if(dev in forwardingTable):
                    print("oh well")
                    #forwardingTable[dev] = [packet[0].src, time.time()]
                else:
                    lowestname = " name "
                    lowest = time.time()
                    for k, v in forwardingTable.items():
                        print("in update block k: "+str(k)+"  v: "+str(v[1])+"   lowest:"+str(lowest))
                        if(v[1] < lowest):
                            lowest = v[1]
                            lowestname = k
                            print("new lowest: "+str(lowest)+"   new lowestname: "+str(lowestname))
                    del forwardingTable[lowestname]
                    forwardingTable[dev] = [packet[0].src, time.time()]
            else:
                if(dev not in forwardingTable):
                    size = size + 1
                forwardingTable[dev] = [packet[0].src, time.time()]

            if(packet[0].src == packet[0].dst):
                found = True

            highestName = "name"
            highest = 0
            delList = []
            if(not found):
                for k, v in forwardingTable.items():
                    print("k: "+str(k)+"   dst, v: "+str(packet[0].dst)+",  "+str(v))
                    if(v[0] == packet[0].dst):
                        found = True
                        print(str(k)+"   highest: "+str(highest)+"  v[1]:"+str(v[1]))
                        if(highest < v[1]):
                            print ("highestName: "+highestName+"  highest:"+str(highest))
                            if(not (highest==0)):
                                #del forwardingTable[highestName]
                                delList.append(highestName)
                                highestName = k
                                highest = v[1]
                                print("new HighestName: "+highestName+"  highest:"+str(highest))
                            else:
                                highestName = k
                                highest = v[1]
                                print("ELSE: new HighestName: "+highestName+"  highest:"+str(highest))
                        else: #highest > v[1]
                            print("else")
                            delList.append(k)
                if(found):
                    print("Sent on k: "+str(k)+"  /  highestName: "+highestName)
                    net.send_packet(highestName, packet)
                    if(not (len(delList)==0)):
                        for item in delList:
                            if(item in forwardingTable):
                                del forwardingTable[item]
                                size = size - 1

            print("\n")
            for k,v in forwardingTable.items():
                print("k: "+str(k)+"   v: "+str(v))

            if(not found):
                for intf in my_interfaces:
                    if dev != intf.name:
                        #print(intf.name, intf.ethaddr, intf.ipaddr, intf.netmask)
                        #probably where we add learning
                        log_debug ("Flooding packet {} to {}".format(packet, intf.name))
                        net.send_packet(intf.name, packet)
    net.shutdown()
