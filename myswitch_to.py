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
        print(packet)
        if packet[0].dst in mymacs:
            forwardingTable[dev] = [packet[0].src, time.time()]
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

            #now = 
            #delList = []
            #for k, v in forwardingTable.items():
                #print("in update block k: "+str(k)+"  v: "+str(v[1])+"   lowest:"+str(lowest))
                #now = time.time()
                #if((time.time() - v[1]) <= 10):
                    #delList.append(k)
            #if(not (len(delList)==0)):
                   # for item in delList:
                        #if(item in forwardingTable):
                            #del forwardingTable[item]
                            #size = size - 1

            forwardingTable[dev] = [packet[0].src, time.time()]

            

            if(not found):
                for k, v in forwardingTable.items():
                    print("k: "+str(k)+"   dst, v: "+str(packet[0].dst)+",  "+str(v))
                    if(v[0] == packet[0].dst):
                        print("Sent on k: "+str(k))
                        net.send_packet(k, packet)
                        found = True

            

            if(not found):
                for intf in my_interfaces:
                    if dev != intf.name:
                        #print(intf.name, intf.ethaddr, intf.ipaddr, intf.netmask)
                        #probably where we add learning
                        log_debug ("Flooding packet {} to {}".format(packet, intf.name))
                        net.send_packet(intf.name, packet)
    net.shutdown()
