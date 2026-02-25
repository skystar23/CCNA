import configparser


class Readconfigurations:
    def __init__(self, filename):
        self.config = configparser.ConfigParser()
        self.config.read(f'./Sourcepagesdata/{filename}.ini')

    def get_values(self, section, key):
        return self.config[section][key]

    @staticmethod
    def load_sections_from_ini(filename):
        config = configparser.ConfigParser()
        config.read(f'./Sourcepagesdata/{filename}.ini')  # Replace with the correct path to your .ini file
        return config.sections()

    @staticmethod
    def check_required_sections(filename,required_sections):
        sections = []
        available_sections = Readconfigurations.load_sections_from_ini(filename)  # Read available sections from INI
        for section in required_sections:
            if section not in available_sections:
                sections.append(section)
        return all(section in available_sections for section in required_sections),sections

    def set_values(self,filename,section,key,value):
        self.config.set(section,key,value)
        # Write the updated configuration back to the .ini file
        with open(f'./Sourcepagesdata/{filename}.ini', 'w') as configfile:
            self.config.write(configfile)


class Readtestdata:
    def __init__(self, filename):
        self.config = configparser.ConfigParser()
        self.config.optionxform = str
        self.config.read(f'./Testdata/{filename}.ini')

    def get_values(self, section, key):
        return self.config[section][key]

    def get_key_value(self,section):
        if section in self.config:
            Data_dic = {key: value for key, value in self.config.items(section )}
            return Data_dic