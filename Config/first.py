from Utilities.GNS3_controller import GNS3Project
from Utilities.GNS3_Automation import router_config
from Utilities.Cisco_Commands import *         
from Utilities.Driver_selenium import json_reading

class First:
    def project_setup_teardown(self, projectname):
        self.project = GNS3Project(project_name=projectname)
       

    def config(self):
        self.project_setup_teardown('BGP_1')
        self.project.start()          
        gns3_info = json_reading('./GNS3_data/ip_address_config.json')
        router_config(gns3_info)


if __name__ == "__main__":
    f = First()         
    f.config()           
   