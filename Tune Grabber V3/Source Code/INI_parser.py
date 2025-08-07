"""
Used to parse INI files. Data is stored as {section_name:{key:value, key, value}, section_name{key:value, key:value}},
or a double dictionary
"""

class INI():
    def __init__(self, filename):
        self.filename = filename
        self.data = self.read_settings()
    def read_settings(self):
        """
        Reads the ini file and returns a dictionary of sections and values
        """

        with open(self.filename, "r") as f:
            data = {}
            for line in f.readlines():
                line = line.strip()
                if line == "" or line[0] == ";":
                    continue
                elif line[0] == "[":
                    line = line[1: -1]
                    data.update({line:{}})
                    last = line  #keeps track of the last section in the dictionary
                else:
                    index = line.find("=")
                    key = line[:index]
                    value = line[index+1:]
                    data[last].update({key:value})

        return data
    
    def read(self):
        """
        Reads the ini file and returns a dictionary of sections and values
        """
        return self.read_settings
    
    def find_value(self, key, section="DEFAULT"):
        """
        Returns the value for a given key in a given section
        """

        return self.data[section][key]
    
    def find(self, key, section="DEFAULT"):
        """
        Returns the value for a given key in a given section
        """
        return self.find_value(key, section)
        
    def change_setting(self, key, value, section = "DEFAULT"):
        """
        Changes the settings in the object then overwrites the file
        """
        self.data[section][key] = value
        with open(self.filename, "w") as f:
            for section in self.data:
                f.write("[" + section + "]\n")
                for key in self.data[section]:
                    f.write(key + "=" + self.data[section][key] + "\n")
    
    def change(self,key,value,section="DEFAULT"):
        """
        Changes the settings in the object then overwrites the file
        """
        return self.change_setting(key, value, section)
    
    def __str__(self):
        return str(self.data)
    
    def __iter__(self, section="DEFAULT"):
        """
        Returns tuple key, value pair for all values in a given section
        """

        for key,value in self.data[section].items():
            yield key,value

    

if __name__ == "__main__":
    ini = INI("settings.ini")
    print(ini.data)
    print(ini.find_value("FilePath"))
    ini.change_setting("FilePath", "yes")
    print(ini.data)