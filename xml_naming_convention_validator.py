import xml.etree.ElementTree as ET
import re

fname = "5101000843.xml"

class xml_naming_convention_validator: 

    def test_HMSC(self, name):
        # BIOS
        bios_matchObj = re.search(r'(bios)', name, re.M | re.I)
        if bios_matchObj:
            print(bios_matchObj.group(), name)
            return True
        
        # Firmware
        firmware_matchObj = re.search(r'(firmware)', name, re.M | re.I)
        if firmware_matchObj:
            print(firmware_matchObj.group(), name)
            return True

        # Unsupported naming conventions
        print(name + " is not yet supported")
        return False

    def test_NOTE(self, name):
        # Banknote Acceptor
        bna_matchObj = re.search(r'(banknote acceptor)', name, re.M | re.I)
        if bna_matchObj:
            print(bna_matchObj.group(), name)
            return True
        else:
            return False

    def test_TICK(self, name):
        # Ticket Printer
        ticket_printer_matchObj = re.search(r'(ticket printer)', name, re.M | re.I)
        if ticket_printer_matchObj:
            print(ticket_printer_matchObj.group(), name)
            return True
        else:
            return False

    def test_MACH(self, name):
        # Machine
        machine_matchObj = re.search('(cabinet)', name, re.M | re.I)
        if machine_matchObj:
            print(machine_matchObj.group(), name)
            return True
        else:
            return False

    def test_MNTR(self, name):
        # Monitor
        monitor_matchObj = re.search('(monitor)', name, re.M | re.I)
        if monitor_matchObj:
            print(monitor_matchObj.group(), name)
            return True
        else:
            return False

    def test_TCHS(self, name):
        # Touch Screen
        touch_screen_matchObj = re.search('(touch screen)', name, re.M | re.I)
        if touch_screen_matchObj:
            print(touch_screen_matchObj.group(), name)
            return True
        else:
            return False
            
    def test(self, x):
        return {
            'HMSC': self.test_HMSC,
            'NOTE': self.test_NOTE,
            'TICK': self.test_TICK,
            'MACH': self.test_MACH,
            'MNTR': self.test_MNTR,
            'TCHS': self.test_TCHS,
            }.get(x)

    def validate_naming_convention(self, atype, aname):
        fn = self.test(atype)
        if fn:
            return(fn(aname))
        else:
            print("No tests implemented for: " + atype)
        return False

    def test_requirements(self, x):
        return {
            'NSV10': True,
            'NSV9': False,
            'NSV8': False,
            'NSV6': False, 
        }.get(x) 

    def validate_requirements(self, title, version):
        fn = self.test_requirements(title)
        if fn:
            return(fn) # todo: test version
        else:
            print("Invalid requirements")
            return False

    def suggest_naming_convention(self, atype, aname):
        suggested_name = "This requires a new name"

        return suggested_name

    def read_xml_file(self, root): 
        for recommended_product in root.findall('Recommended_Product'):
            # Requirements_Tested
            for requirements_tested in recommended_product.findall('Requirements_Tested'):
                requirements_title = requirements_tested.find('Title').text
                requirements_version = requirements_tested.find('Version').text

                valid_requirements = self.validate_requirements(requirements_title, requirements_version)
                if not valid_requirements:
                    print("Invalid Requirements: ", requirements_title, requirements_version)
                
            # Hardware
            for hardware_details in recommended_product.findall('Hardware_Details'):
                hardware_name = hardware_details.find('Hardware_Name').text
                hardware_type = hardware_details.find('Hardware_Type').text

                valid_name = self.validate_naming_convention(hardware_type, hardware_name)
                if not valid_name:
                    self.suggest_naming_convention(hardware_type, hardware_name)
                    
            # Software
            for software_details in recommended_product.findall('Software_Details'):
                software_name = software_details.find('Software_Name').text
                software_type = software_details.find('Software_Type').text

                valid_name = self.validate_naming_convention(software_type, software_name)
                if not valid_name:
                    self.suggest_naming_convention(software_type, software_name)
                    
    def __init__(self):
        self.tree = ET.parse(fname)
        self.root = self.tree.getroot() 
        self.read_xml_file(self.root)


def main(): 
    app = xml_naming_convention_validator() 

if __name__ == "__main__": main()
