import time


class Configuration:

    def __init__(self, socket, name):
        self.socket = socket
        self.name = name

    def sendCommand(self, command: str):
        print(command)
        self.socket.send(f"{command}\r".encode('utf-8'))
        time.sleep(0.5)
        #self.read_console()

    def writeConfig(self):
        print(f"{self.name} : Write configuration \n")
        self.sendCommand("end")  # On évite d'etre dans un mode non voulu
        self.sendCommand("write")
        self.sendCommand("")  # Pour envoyer un enter et confirmer l'écriture du fichier

    def globalConfigMode(self):
        self.sendCommand("")  # entrer
        self.sendCommand("ena")

    def configureTerminal(self):
        self.sendCommand("end")  # éviter de se retrouver dans un mode et ne pas exec les commandes
        self.sendCommand("configure terminal")

    def eraseRunningConfiguration(self):
        print(f"{self.name} : erase running configuration \n")
        self.globalConfigMode()
        self.configureTerminal()
        with open("default.cfg", "r") as default_config:
            for line in default_config.readlines():
                self.sendCommand(line)

    def changeHostname(self):
        self.configureTerminal()
        print(f"{self.name} : Change hostname \n")
        self.sendCommand(f"hostname {self.name}")
        self.sendCommand("end")

    def interInInterfaceMode(self, interface):
        self.configureTerminal()
        self.sendCommand(f"int {interface}")

    def saveExitInterfaceMode(self):
        self.sendCommand("no sh")
        self.sendCommand("end")

    def setIntDescription(self, interface, desc):
        print(f"{self.name} : Set description to {interface} : {desc} \n")
        self.interInInterfaceMode(interface)
        self.sendCommand(f"description \"{desc}\"")

    def setUpIPv4(self, interface, IPv4):
        print(f"{self.name} : Configure {interface} with {IPv4} \n")
        self.interInInterfaceMode(interface)
        self.sendCommand(f"ip add {IPv4[0]} {IPv4[1]}")
        self.saveExitInterfaceMode()


    def setstaticrouting(self,static_routing):
        print(f"{self.name} : set Static Routing \n")
        self.configureTerminal()
        for static in static_routing:
            self.sendCommand(f"ip route {static[0]} {static[1]} {static[2]}")

    def setospf(self,ospf_routing,network = None):
        print(f"{self.name} : set ospf Routing \n")
        self.configureTerminal()
        for ospf in ospf_routing:
            print(ospf)
            self.sendCommand(f"router ospf {ospf[0]}")
            self.sendCommand(f"router-id {ospf[1]}")
            if network != None:
                for ip in network:
                    self.sendCommand(f"network {ip[0]} {ip[1]} {ip[2]}")
            if "static" in ospf:
                self.sendCommand(f"redistribute {ospf[3]}")
            if "stub" in ospf:
                if len(ospf) >=5:
                    self.sendCommand(f"area {ospf[2]} {ospf[3]} {ospf[4]}")
                else:
                    self.sendCommand(f"area {ospf[2]} {ospf[3]}")
            elif "nssa" in ospf:
                if len(ospf) >= 5:
                    self.sendCommand(f"area {ospf[2]} {ospf[3]} default-information-orginate {ospf[4]}")
                else:
                    self.sendCommand(f"area {ospf[2]} {ospf[3]} default-information-orginate")
            


    def setospf_authentication(self,interface,ospf_auth_mode):
        print(f"{self.name} : ospf authentication {interface} \n")
        self.interInInterfaceMode(interface)
        if ospf_auth_mode[0] == "plain":
            self.sendCommand(f"ip ospf authentication-key {ospf_auth_mode[1]}")
            self.sendCommand(f"ip ospf authentication")
        elif ospf_auth_mode[0] == "md5":
            self.sendCommand(f"ip ospf message-digest-key {ospf_auth_mode[1]} md5 {ospf_auth_mode[2]} {ospf_auth_mode[3]}")
            self.sendCommand(f"ip ospf authentication message-digest")
        else:
            print(f"Error: Unknown authentication type for interface {interface}")
        

    def setbgp(self, bgp_routing,network = None):
        print(f"{self.name} : set bgp Routing \n")
        self.configureTerminal()
        for bgp in bgp_routing:
            print(bgp)
            self.sendCommand(f"router bgp {bgp[0]}")
            self.sendCommand(f"neighbor {bgp[1]} remote-as {bgp[2]}")
            if len(bgp) >= 4:
                self.sendCommand(f"neighbor {bgp[1]} ebgp-multihop {bgp[3]}")
            if network != None:
                for ip in network:
                    self.sendCommand(f"network {ip[0]} mask {ip[1]}")

    def setbgp_authentication(self, bgp_auth,network = None):
        print(f"{self.name} : set bgp Routing \n")
        self.configureTerminal()
        for bgp in bgp_auth:
            print(bgp)
            self.sendCommand(f"router bgp {bgp[0]}")
            self.sendCommand(f"neighbor {bgp[1]} remote-as {bgp[2]}")
            self.sendCommand(f"neighbor {bgp[1]} password {bgp[3]}")
            if len(bgp) >=5 and "passive" in bgp:
                self.sendCommand(f"neighbor {bgp[1]} transport connection-mode {bgp[4]}")
            else:
                if len(bgp) >= 5:
                    self.sendCommand(f"neighbor {bgp[1]} ebgp-multihop {bgp[4]}")
            if network != None:
                for ip in network:
                    self.sendCommand(f"network {ip[0]} mask {ip[1]}")

    
    def setgre(self, gre_tunnel):
        print(f"{self.name} : set bgp Routing \n")
        self.configureTerminal()
        for gre in gre_tunnel:
            print(gre)
            self.sendCommand(f"int tunnel {gre[0]}")
            self.sendCommand(f"tunnel source {gre[1]}")
            self.sendCommand(f"tunnel destination {gre[2]}")
            self.sendCommand(f"ip address {gre[3]} {gre[4]}")
    
    def setipsec(self,ipsec_conf):
        print(f"{self.name} : set IPSEC server configuration \n")
        self.configureTerminal()
        if "MAIN" == ipsec_conf["MODE"]:
            self.sendCommand("crypto isakmp aggressive-mode disable")
        self.sendCommand(f'crypto isakmp key 0 {ipsec_conf["PreShareKey"]} address 0.0.0.0')
        self.setphase1(ipsec_conf["ISAKMP"])
        self.sendCommand("crypto ipsec nat-transparency udp-encapsulation")
        self.setaccess_list(ipsec_conf["access-list_numder"],ipsec_conf["access-list"])
        self.setphase2(ipsec_conf["IPSEC"],ipsec_conf["map-names"],ipsec_conf["access-list_numder"])
        self.ipsec_appy(ipsec_conf["interfaceName"],ipsec_conf["map-names"])

    def ipsec_appy(self,interfacename,maps):
        self.sendCommand(f"int {interfacename}")
        self.sendCommand("no crypto map")
        self.sendCommand(f"crypto map {maps[2]}")
        self.sendCommand("exit")


    def setaccess_list(self,numder,acesslist):
        for access in acesslist:
            self.sendCommand(f"access-list {numder} permit ip {access[0]} {access[1]} {access[2]} {access[3]}")
    
    def setphase2(self,policy,maps,number):
        self.sendCommand(f"crypto ipsec transform-set {policy[0]} esp-{policy[1]} esp-{policy[2]}")
        self.sendCommand("mode tunnel")
        self.sendCommand("exit")
        self.sendCommand(f"crypto ipsec security-association lifetime seconds {policy[3]}")
        self.sendCommand(f'crypto dynamic-map {maps[0]} {maps[1]}')
        self.sendCommand(f"match address {number}")
        self.sendCommand(f"set pfs {policy[4]}")
        self.sendCommand(f"set transform-set {policy[0]}")
        self.sendCommand("exit")
        self.sendCommand(f"crypto map {maps[2]} {maps[3]} ipsec-isakmp dynamic {maps[1]}")

    
    def setphase1(self,policy):
        self.sendCommand(f"crypto isakmp policy {policy[0]}")
        self.sendCommand("authentication pre-share")
        self.sendCommand(f"encryption {policy[1]}")
        self.sendCommand(f'group {policy[2]}')
        self.sendCommand(f'hash {policy[3]}')
        self.sendCommand(f'lifetime {policy[4]}')
        self.sendCommand('exit')

    def read_console(self):
        while True:
            data =  self.socket.recv(1024)
            text = data.decode('latin-1')
            print(text)
        
    def saveconfiguration(self):
        print(f"{self.name} : save configuration \n")
        self.sendCommand("end")
        self.sendCommand("wr memory")


    #####################################################PC-configurations#################################

    def set_pc(self,pcconfig):
        self.sendCommand(f"ip {pcconfig['IPv4']}  {pcconfig['mask']}  {pcconfig['gateway']}\n")

    def set_pcv6(self,pcconfig):
        self.sendCommand(f"ip {pcconfig['IPv6']}  {pcconfig['gateway6']}\n")

    def save_pc(self):
        print(f"{self.name}: save configuration")
        self.sendCommand("save")

    #####################################################IPv6configurations#################################

    def setUpIPv6(self, interface, IPv6):
        print(f"{self.name} : Configure {interface} with {IPv6} \n")
        self.interInInterfaceMode(interface)
        self.sendCommand(f"ipv6 add {IPv6}")
        self.saveExitInterfaceMode()

    def activeIPv6(self):
        print(f"{self.name} : Enable IPv6 \n")
        self.configureTerminal()
        self.sendCommand("ipv6 unicast-routing")

    def setOSPFv3(self, ospf):
        print(f"{self.name} : set OSPFv3 \n")
        self.configureTerminal()
        self.activeIPv6()
        self.sendCommand(f"ipv6 router ospf {ospf[0]}")
        self.sendCommand(f"router-id {ospf[1]}")
        self.sendCommand("exit")
    
    def setstaticroutingv6(self,routing):
        print(f"{self.name} : set Static routing ipv6 \n")
        self.configureTerminal()
        self.activeIPv6()
        for route in routing:
            self.sendCommand(f"ipv6 route {route[0]} {route[1]}")

        

    def activeOSPFv3Interface(self, interface, OSPF_area):
        print(f"{self.name} : Active OSPFv3 on {interface} \n")
        self.interInInterfaceMode(interface)
        self.sendCommand(f"ipv6 ospf {OSPF_area[0]} area {OSPF_area[1]}")
        self.sendCommand("end")

    def setbgp6(self, bgp_routing,network = None):
        print(f"{self.name} : set bgp Routing \n")
        self.configureTerminal()
        for bgp in bgp_routing:
            print(bgp)
            self.sendCommand(f"router bgp {bgp[0]}")
            self.sendCommand(f"bgp router-id {bgp[1]}")
            self.sendCommand(f"neighbor {bgp[2]} remote-as {bgp[3]}")
            self.sendCommand("address-family ipv6 unicast")
            self.sendCommand(f"neighbor {bgp[2]} activate")
            if len(bgp) >= 5 :
                self.sendCommand(f"neighbor {bgp[2]} ebgp-multihop {bgp[4]}")
            if network != None:
                for ip in network:
                    self.sendCommand(f"network {ip[0]}")


    def setbgp6_authentication(self, bgp_auth,network = None):
        print(f"{self.name} : set bgp Routing \n")
        self.configureTerminal()
        for bgp in bgp_auth:
            print(bgp)
            self.sendCommand(f"router bgp {bgp[0]}")
            self.sendCommand(f"bgp router-id {bgp[1]}")
            self.sendCommand(f"neighbor {bgp[2]} remote-as {bgp[3]}")
            self.sendCommand("address-family ipv6 unicast")
            self.sendCommand(f"neighbor {bgp[2]} activate")
            self.sendCommand(f"neighbor {bgp[2]} password {bgp[4]}")
            if len(bgp) >=6 and "passive" in bgp:
                self.sendCommand(f"neighbor {bgp[2]} transport connection-mode {bgp[5]}")
            else:
                if len(bgp) >= 6:
                    self.sendCommand(f"neighbor {bgp[2]} ebgp-multihop {bgp[5]}")
            if network != None:
                for ip in network:
                    self.sendCommand(f"network {ip[0]}")
