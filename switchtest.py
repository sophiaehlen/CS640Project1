#!/usr/bin/env python

import sys
from switchyard.lib.address import *
from switchyard.lib.packet import *
from switchyard.lib.common import *
from switchyard.lib.testing import *

def mk_pkt(hwsrc, hwdst, ipsrc, ipdst, reply=False):
    ether = Ethernet()
    ether.src = EthAddr(hwsrc)
    ether.dst = EthAddr(hwdst)
    ether.ethertype = EtherType.IP

    ippkt = IPv4()
    ippkt.srcip = IPAddr(ipsrc)
    ippkt.dstip = IPAddr(ipdst)
    ippkt.protocol = IPProtocol.ICMP
    ippkt.ttl = 32

    icmppkt = ICMP()
    if reply:
        icmppkt.icmptype = ICMPType.EchoReply
    else:
        icmppkt.icmptype = ICMPType.EchoRequest

    return ether + ippkt + icmppkt

def switch_tests():
    s = Scenario("learning switch tests")
    s.add_interface('eth0', '10:00:00:00:00:01') # add interface to switch
    s.add_interface('eth1', '10:00:00:00:00:02')
    s.add_interface('eth2', '10:00:00:00:00:03')
    s.add_interface('eth3', '10:00:00:00:00:04')
    s.add_interface('eth4', '10:00:00:00:00:04')
    s.add_interface('eth5', '10:00:00:00:00:05')

    # test case 1: a frame with broadcast destination should get sent out
    # all ports except ingress
    # mk_pkt(from, to, IP from, IP to)  
    # Note: "ff:ff:ff:ff:ff:ff" is the broadcast
    testpkt = mk_pkt("30:00:00:00:00:02", "ff:ff:ff:ff:ff:ff", "172.16.42.2", "255.255.255.255")
    s.expect(PacketInputEvent("eth1", testpkt, display=Ethernet), "An Ethernet frame with a broadcast destination address should arrive on eth1")
    s.expect(PacketOutputEvent("eth0", testpkt, "eth2", testpkt, "eth3", testpkt, "eth4", testpkt, "eth5", testpkt, display=Ethernet), "The Ethernet frame with a broadcast destination address should be forwarded out ports eth0,2,3,4,5")


# broadcast
    testpkt = mk_pkt("20:00:00:00:00:03", "ff:ff:ff:ff:ff:ff", "172.16.42.3", "255.255.255.255")
    s.expect(PacketInputEvent("eth3", testpkt, display=Ethernet), "An Ethernet frame with a broadcast destination address should arrive on eth3")
    s.expect(PacketOutputEvent("eth0", testpkt, "eth1", testpkt, "eth2", testpkt, "eth4", testpkt, "eth5", testpkt, display=Ethernet), "The Ethernet frame with a broadcast destination address should be forwarded out ports eth0,1,2,4,5")



    # the forwarding table should contain [eth1, "30:00:00:00:00:02"]

    # test case 2: a frame with any unicast address except one assigned to hub
    # interface should be sent out all ports except ingress
    reqpkt = mk_pkt("20:00:00:00:00:01", "30:00:00:00:00:02", '192.168.1.100','172.16.42.2')
    s.expect(PacketInputEvent("eth0", reqpkt, display=Ethernet), "An Ethernet frame from 20:00:00:00:00:01 to 30:00:00:00:00:02 should arrive on eth0") 
    s.expect(PacketOutputEvent("eth1", reqpkt, display=Ethernet), "Ethernet frame destined for 30:00:00:00:00:02 should be sent to eth1") 

    reqpkt = mk_pkt("20:00:00:00:00:02", "30:00:00:00:00:02", '192.168.1.100', '172.16.42.2')
    s.expect(PacketInputEvent("eth0", reqpkt, display=Ethernet), "An Ethernet frame from 20:00:00:00:00:02 to 30:00:00:00:00:02 should arrive on eth0")
    s.expect(PacketOutputEvent("eth1", reqpkt, display=Ethernet), "Ethernet frame destined for 30:00:00:00:00:02 should be sent to eth1")


# build size of ft:
    reqpkt = mk_pkt("20:00:00:00:00:03", "30:00:00:00:00:02", '192.168.1.101', '172.16.42.2')
    s.expect(PacketInputEvent("eth0", reqpkt, display=Ethernet), "Ethernet frame from 20:00:00:00:00:03 to 30:00:00:00:00:02 should arrive on eth0")
    s.expect(PacketOutputEvent("eth1", reqpkt, display=Ethernet), "Ethernet frame destined for 30:00:00:00:00:02 should be sent to eth1")


#    resppkt = mk_pkt("30:00:00:00:00:02", "20:00:00:00:00:01", '172.16.42.2', '192.168.1.100', reply=True) #reply expected
#    s.expect(PacketInputEvent("eth1", resppkt, display=Ethernet), "An Ethernet frame from 30:00:00:00:00:02 to 20:00:00:00:00:01 should arrive on eth1")
#    s.expect(PacketOutputEvent("eth0", resppkt, "eth2", resppkt, display=Ethernet), "Ethernet frame destined to 20:00:00:00:00:01 should be flooded out eth0 and eth2")

    # the forwarding table should contain {eth1: "30:00:00:00:00:02", eth0: "20:00:00:00:00:01"}

    # test case 3: a frame with dest address of one of the interfaces should
    # result in nothing happening
    reqpkts = mk_pkt("20:00:00:00:00:01", "10:00:00:00:00:03", '192.168.1.100','172.16.42.2')
    s.expect(PacketInputEvent("eth2", reqpkts, display=Ethernet), "An Ethernet frame should arrive on eth2 with destination address the same as eth2's MAC address")
    s.expect(PacketInputTimeoutEvent(1.0), "The hub should not do anything in response to a frame arriving with a destination address referring to the hub itself.")
    return s

scenario = switch_tests()
