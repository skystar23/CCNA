import socket
from Utilities.Cisco_Commands import Configuration
from Utilities.Driver_selenium import json_reading
from Utilities.Readconfigurations import Readconfigurations

def router_config1(conf):
    # print(conf)
    for routerName, routerConf in conf.items():
        print(f"routerName: {routerName}, routerConf: {routerConf}")
        if routerName != 'VPC':
            if routerName != "WiZNG-M":
                if isinstance(routerConf, dict):
                    routerManagementAddr = routerConf.get("IPaddr")
                    print(routerManagementAddr)
                    routerManagementPort = routerConf.get("port")
                else:
                    continue
                if not routerManagementAddr or not routerManagementPort:
                    print(f"Missing IP address or port for {routerName}, skipping.")
                    continue

                routerSocket = socket.socket()
                try:
                    routerSocket.connect((routerManagementAddr, routerManagementPort))
                    print(f"Connected to {routerName}")
                except ConnectionError:
                    print(f"Can't connect to {routerName}")
                    continue

                config = Configuration(routerSocket, routerName)
                config.globalConfigMode()

                if "static_routing" in routerConf:
                    config.setstaticrouting(routerConf["static_routing"])
                
                if "static_routingv6" in routerConf:
                    config.setstaticroutingv6(routerConf["static_routingv6"])

                if "ospf" in routerConf:
                    if "ospf_network" in routerConf:
                        config.setospf(routerConf["ospf"],routerConf["ospf_network"])
                    else:
                        config.setospf(routerConf["ospf"])

                if "ospfv3" in routerConf:
                    config.setOSPFv3(routerConf["ospfv3"])
                    

                if "ospf_authentication" in routerConf:
                    config.setospf_authentication(routerConf["ospf_authentication"])

                if "BGP" in routerConf:
                    if "BGP_Network" in routerConf:
                        config.setbgp(routerConf["BGP"],routerConf["BGP_Network"])
                    else:
                        config.setbgp(routerConf["BGP"])

                if "BGP_authentication" in routerConf:
                    if "BGP_Network" in routerConf:
                        config.setbgp_authentication(routerConf["BGP_authentication"],routerConf["BGP_Network"])
                    else:
                        config.setbgp_authentication(routerConf["BGP_authentication"])

                if "BGP" in routerConf:
                    if "next-hop-self" in routerConf:
                        config.se
                if "BGP6" in routerConf:
                    config.activeIPv6()
                    if "BGP6_Network" in routerConf:
                        config.setbgp6(routerConf["BGP6"],routerConf["BGP6_Network"])
                    else:
                        config.setbgp6(routerConf["BGP6"])

                if "BGP6_authentication" in routerConf:
                    config.activeIPv6()
                    if "BGP6_Network" in routerConf:
                        config.setbgp6_authentication(routerConf["BGP6_authentication"],routerConf["BGP6_Network"])
                    else:
                        config.setbgp6_authentication(routerConf["BGP6_authentication"])

                if "GRE" in routerConf:
                    config.setgre(routerConf["GRE"])
                
                if "IPSEC" in routerConf:
                    conf.setipesc(routerConf["IPSEC"])
                

                for interface in routerConf.get("interfaces", []):
                    if "IPv4" in interface:
                        config.setUpIPv4(interface["interfaceName"], interface["IPv4"])

                    if "IPv6" in interface:
                        config.setUpIPv6(interface["interfaceName"],interface["IPv6"])
                    
                    if "OSPF_area" in interface:
                        config.activeOSPFv3Interface(interface["interfaceName"],
                                            interface["OSPF_area"])
                    if "ospf_authentication" in interface:
                        config.setospf_authentication(interface["interfaceName"],
                                            interface["ospf_authentication"])


                # config.saveconfiguration()
                routerSocket.close()
        else:
            for pc, pcconfig in routerConf.items():
                pcManagementAddr = pcconfig.get("IPaddr")
                pcManagementPort = pcconfig.get("port")
                if not pcManagementAddr or not pcManagementPort:
                    print(f"Missing IP address or port for {pc}, skipping.")
                    continue

                routerSocket1 = socket.socket()
                try:
                    routerSocket1.connect((pcManagementAddr, pcManagementPort))
                    print(f"Connected to {pc}")
                except ConnectionError:
                    print(f"Can't connect to {pc}")
                    continue

                config1 = Configuration(routerSocket1, pc)
                
                if "IPv6" and "gateway6" in pcconfig:
                    config1.set_pcv6(pcconfig)
                
                if "IPv4" and "gateway" in pcconfig:
                    config1.set_pc(pcconfig)
                # config.save_pc()
                routerSocket1.close()


