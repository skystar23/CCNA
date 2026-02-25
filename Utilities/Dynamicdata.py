import ipaddress
import string
import time
import secrets
import socket
import struct


class Dynamicdata:
    @staticmethod
    def dateandtime():
        """Get Data and time of local Pc with seconds"""
        return str(time.strftime("%d/%m/%Y, %H:%M:%S", time.localtime()))

    def generate_ip_address(self):
        """Generate ip address without 0.0.0.0 ,255.255.255.255 and below 223 ips only"""
        k = ".".join(str(secrets.randbelow(255)) for _ in range(4))
        if k == "0.0.0.0":
            return self.generate_ip_address()
        elif k == "255.255.255.255":
            return self.generate_ip_address()
        else:
            y = k.split(".")
            if int(y[0]) > 223:
                return self.generate_ip_address()
            else:
                return k

    @staticmethod
    def generate_port_number_with_range():
        """Generate port number with range and single number ex:5(or)1:100"""
        port = ["range", "single"]
        port_type = secrets.choice(port)
        if port_type == "single":
            return str(secrets.randbelow(65534)+1)
        else:
            start = secrets.randbelow(65534)+1
            end = secrets.randbelow(65535 -start)+start
            return f'{start}:{end}'

    @staticmethod
    def generate_port_number():
        """Generate port number with single number ex:5"""
        return str(secrets.randbelow(65534)+1)

    @staticmethod
    def generate_port_number_only_range():
        """Generate port number with range number ex:5:6525"""
        start = secrets.randbelow(65534)+1
        end = secrets.randbelow(65534)+start
        return f'{start}:{end}'

    def valid_ports(self, start, end, single):
        """Checks port is valid for range"""
        if single >= start and end <= single:
            single = secrets.randbelow(65534)+1
            single = self.valid_ports(start, end, single)
        return single

    def valid_single_port(self, start, end):
        """Checks port start and end is equal or not """
        if start == end:
            end = secrets.randbelow(65534)+1
            end = self.valid_single_port(start, end)
        return end

    def generate_port_number_multiple_cases(self):
        """Generate port with range ,single or both cases"""
        port = ["range", "single", "Both"]
        port_type = secrets.choice(port)
        if port_type == "single":
            return str(secrets.randbelow(65534)+1)
        elif port_type == "range":
            start = secrets.randbelow(65534)+1
            end = secrets.randbelow(65534)+1+start
            return f'{start}:{end}'
        else:
            sequence = ["range-range", "range-single", "single-range", "single-single"]
            sequence_type = secrets.choice(sequence)
            if sequence_type == "range-range":
                start = secrets.randbelow(65534)+1
                end = secrets.randbelow(65534)+1+start
                start1 = secrets.randbelow(65534)+1
                start1 = self.valid_ports(start, end, start1)
                end1 = secrets.randbelow(65534)+1+start1
                return f'{start}:{end},{start1}:{end1}'
            elif sequence_type == "range-single":
                start = secrets.randbelow(65534)+1
                end = secrets.randbelow(65534)+1+start
                single = secrets.randbelow(65534)+1
                single = self.valid_ports(start, end, single)
                return f'{start}:{end},{single}'
            elif sequence_type == "single-range":
                start = secrets.randbelow(65534)+1
                end = secrets.randbelow(65534)+1+start
                single = secrets.randbelow(65534)+1
                single = self.valid_ports(start, end, single)
                return f'{single},{start}:{end}'
            else:
                start = secrets.randbelow(65534)+1
                end = secrets.randbelow(65534)+1
                end = self.valid_single_port(start, end)
                return f'{start},{end}'

    @staticmethod
    def invaild_ip_generator():
        """Generate invalid ip length"""
        return ".".join(str(secrets.randbelow(255)) for _ in range(secrets.randbelow(2)+1))

    @staticmethod
    def alpha():
        """Generate only single character"""
        return ''.join(secrets.choice(string.ascii_letters))

    @staticmethod
    def numeric():
        """Generate alpha_numeric character"""
        return ''.join(secrets.choice(string.digits))

    @staticmethod
    def specialcharacters():
        """Generate alpha_numeric character"""
        return ''.join(secrets.choice(string.punctuation))

    @staticmethod
    def alpha_numeric():
        """Generate alpha_numeric character"""
        return ''.join(secrets.choice(string.digits + string.ascii_letters))

    @staticmethod
    def alpha_specialcharacters():
        """Generate alpha_numeric character"""
        return ''.join(secrets.choice(string.punctuation + string.ascii_letters))

    @staticmethod
    def numeric_specialcharacters():
        """Generate alpha_numeric character"""
        return ''.join(secrets.choice(string.punctuation + string.digits))

    def alpha_numeric_ip(self):
        """Generate alpha numeric ip address"""
        return ".".join(self.alpha_numeric() for _ in range(4))

    def network_ip(self, mask):
        """Generate Network for the given subnetmask"""
        ip = self.generate_ip_address()
        network = ipaddress.IPv4Network(f'{ip}/{mask}', strict=False)
        return str(network.network_address)

    @staticmethod
    def network_ip_above_224(mask):
        """Generate Network ip address above 224 for the given subnetmask,"""
        ip = ".".join(str(secrets.randbelow(31)+224) for _ in range(4))
        network = ipaddress.IPv4Network(f'{ip}/{mask}', strict=False)
        return str(network.network_address)
    
    def network_compare(self,ip,mask):
        network = ipaddress.IPv4Network(f'{ip}/{mask}', strict=False)
        if str(network.network_address) == ip:
            ip = self.network_compare(self.generate_ip_address(),mask)
        return ip
            

    @staticmethod
    def genetrate_network(mask, ip):
        """Generate Network ip for given ip address and subnetmask """
        network = ipaddress.IPv4Network(f'{ip}/{mask}', strict=False)
        return str(network.network_address)


    def classlesssubnetmask(self):
        """Generate classless subnetmask"""
        return self.subnetmask(str(secrets.randbelow(31)+1))
    
    @staticmethod
    def subnetmask(prefix_length):
        # Create a 32-bit mask with 'prefix_length' number of 1's, followed by 0's
        # Convert the mask to dotted decimal format
        return socket.inet_ntoa(struct.pack('!I', (0xFFFFFFFF << (32 - int(prefix_length))) & 0xFFFFFFFF))


    def domainname_generator(self):
        """Generate Domain name with chars and digits"""
        k = ".".join(self.domainname_alphanumeric() for _ in range(secrets.randbelow(1)+2))
        k += f'.{self.domainname()}'
        return k

    def domainname(self):
        """Generate Domain name with chars """
        return "".join(self.alpha() for _ in range(secrets.randbelow(4)+3))

    def domainname_alphanumeric(self):
        return "".join(self.alpha_numeric() for _ in range(secrets.randbelow(4)+3))

    def domainname_hyphen(self):
        """Generate Domain name with chars and hyphen"""
        return "-".join(self.domainname() for _ in range(secrets.randbelow(1)+2))

    def domainname_generator_with_hyphen(self, position):
        """Generate Domain name with chars and hyphen at particular position"""
        k = ''
        if position.upper() == "START":
            k += f'-{self.domainname_generator()}'
        elif position.upper() == "END":
            k += f'{self.domainname_generator()}-'
        elif position.upper() == "MIDDLE":
            k += f'{self.domainname()}.{self.domainname()}.{self.domainname_hyphen()}.{self.domainname_hyphen()}'
        elif position.upper() == "NUMBER":
            k += f'{secrets.randbelow(9)}{self.domainname_generator()}'
        elif position.upper() == "END-NUMBER":
            original_string = self.domainname_alphanumeric()
            pos = secrets.randbelow(len(original_string))
            original_string = original_string[:pos] + str(secrets.choice(string.digits)) + original_string[pos:]
            k += f'{self.domainname_generator()}.{original_string}'
        else:
            k += f'{self.domainname()}.{self.domainname()}--{self.domainname()}.{self.domainname()}'
        return k

    def allcharatersname(self):
        """used to generate string with chars,digits and special chars"""
        letters = string.ascii_letters
        digits = string.digits
        special_chars = string.punctuation
        alphabet = letters + digits + special_chars
        pwd = ''
        for _ in range(secrets.randbelow(3)+2):
            pwd += ''.join(secrets.choice(alphabet))
        if '-' in pwd:
            return self.allcharatersname()
        elif '.' in pwd:
            return self.allcharatersname()
        else:
            return pwd

    def invalid_domainname_generator(self):
        """generate invalid domain names"""
        return ".".join(self.alpha_numeric() for _ in range(secrets.randbelow(6)+1))

    def alpha_ip(self):
        """Generate ip with chars"""
        return ".".join(self.alpha() for _ in range(secrets.randbelow(2)+3))

    @staticmethod
    def generate_protocol():
        """Generate protocol for NAT and Traffic rules"""
        return secrets.choice(['TCP', 'UDP', 'ICMP', 'Any', "TCP, UDP"])

    def generate_instance_name_alphabets(self, length):
        """Generate instance name with chars and digits"""
        return "".join(self.alpha() for _ in range(length))

    def generate_instance_name_numbers(self, length):
        """Generate instance name with chars and digits"""
        return "".join(self.numeric() for _ in range(length))

    def generate_instance_name_specialcharacters(self, length):
        """Generate instance name with special characters, excluding certain ones."""

        exclude = ["\\", ".", "\'", "#", "\"", '=', ':']
        pwd = ''
        i = 0
        while i < length:
            k = secrets.choice(string.punctuation)
            if k not in exclude:
                pwd += ''.join(k)
                i += 1
        return pwd

    def generate_instance_name_alpha_numeric(self, length):
        """Generate instance name with chars and digits"""
        return "".join(self.alpha_numeric() for _ in range(length))

    def generate_instance_name_alpha_specialcharacters(self, length):
        """Generate instance name with chars and digits"""
        alphabet = string.ascii_letters + string.punctuation
        exclude = ["\\", ".", "\'", "#", "\"", '=', ':']
        pwd = ''
        i = 0
        while i < length:
            k = secrets.choice(alphabet)
            if k not in exclude:
                pwd += ''.join(k)
                i += 1
        return pwd

    def generate_instance_name_numeric_specialcharacters(self, length):
        """Generate instance name with chars and digits"""
        alphabet = string.digits + string.punctuation
        exclude = ["\\", ".", "\'", "#", "\"", '=', ':']
        pwd = ''
        i = 0
        while i < length:
            k = secrets.choice(alphabet)
            if k not in exclude:
                pwd += ''.join(k)
                i += 1
        return pwd

    def generate_instance_name_alpha_numeric_specialcharters(self, length):
        """Generate instance name with chars,digit and special chars """
        alphabet = string.ascii_letters + string.digits + string.punctuation
        exclude = ["\\", ".", "\'", "#", "\"", '=', ':']
        pwd = ''
        i = 0
        while i < length:
            k = secrets.choice(alphabet)
            if k not in exclude:
                pwd += ''.join(k)
                i += 1
        return pwd

    @staticmethod
    def random_insertion_in_string(instance, charter):
        """used for inserting char in sting at random position"""
        position = secrets.randbelow(len(instance) - 1)
        return instance[:position] + str(charter) + instance[position + 1:]

    def generate_ip_address_with_slash(self):
        """Generate ip address with slash ex: a.b.c.d/s"""
        ip = self.generate_ip_address()
        mask = secrets.randbelow(32)
        return f'{ip}/{mask}'

    def generate_ipaddress_with_both(self):
        """Generate ip address with slash and not slash ex: a.b.c.d/s or a.b.c.d"""
        type = ['slash', 'without slash']
        iptype = secrets.choice(type)
        if iptype == "slash":
            return self.generate_ip_address_with_slash()
        else:
            return self.generate_ip_address()

    @staticmethod
    def generate_mac_address():
        """"Generate mac address """
        mac = [secrets.randbelow(0xFF) for _ in range(6)]  # Randomly generate 6 bytes
        mac[0] &= 0xFE  # Set the first byte's LSB to 0 for a locally administered MAC address
        return ''.join(['{:02X}'.format(x) for x in mac])  # Convert the list of bytes to a colon-separated string
    
    @staticmethod
    def generate_mac_address_with_colon():
        """"Generate mac address """
        mac = [secrets.randbelow(0xFF) for _ in range(6)]  # Randomly generate 6 bytes
        mac[0] &= 0xFE  # Set the first byte's LSB to 0 for a locally administered MAC address
        return ':'.join(['{:02X}'.format(x) for x in mac])  # Convert the list of bytes to a colon-separated string

    def instance_name_generator(self, generator_type, maxlength, lenght_type="Random"):
        if lenght_type == "Random":
            length = secrets.randbelow(maxlength)
        else:
            length = maxlength
        if generator_type.lower() == "alphabets":
            return self.generate_instance_name_alphabets(length)
        elif generator_type.lower() == "numbers":
            return self.generate_instance_name_numbers(length)
        elif generator_type.lower() == 'specialcharacters':
            return self.generate_instance_name_specialcharacters(length)
        elif generator_type.lower() == "alpha_numeric":
            return self.generate_instance_name_alpha_numeric(length)
        elif generator_type.lower() == "alpha_specialcharacters":
            return self.generate_instance_name_alpha_specialcharacters(length)
        elif generator_type.lower() == "numeric_specialcharacters":
            return self.generate_instance_name_numeric_specialcharacters(length)
        elif generator_type.lower() == "alpha_numeric_specialcharters":
            return self.generate_instance_name_alpha_numeric_specialcharters(length)

    def random_instance_name_generator(self, length):
        type = "".join(secrets.choice(["alphabets", "numbers","alpha_numeric"]))
        return self.instance_name_generator(generator_type=type, maxlength=length)



    def generate_ip_address_with_slash_notation(self,netmask):
        """Generate ip address with slash ex: a.b.c.d/s"""
        ip = self.generate_ip_address()
        if netmask != 33:
            return f'{ip}/{netmask}'
        else:
            return self.generate_ip_address()

    def generate_ipaddress_with_both_notation(self,mask_range):
        """Generate ip address with slash and not slash ex: a.b.c.d/s or a.b.c.d"""
        objtype = ['slash', 'without slash']
        iptype =secrets.choice(objtype)
        if iptype == "slash":
            return self.generate_ip_address_with_slash_notation(mask_range)
        else:
            return self.generate_ip_address()