'''
Created on Feb 19, 2014

@author: David Darling <david.darling@khepry.com>
'''
#!/usr/bin/python

import csv
import os
import platform
import random
import string
import subprocess
import time as tyme
import uuid

from collections import OrderedDict

from datetime import date
from datetime import time
from datetime import datetime

from dateutil import relativedelta

from pyjavaproperties import Properties


class StringUtils:

    __alphabeticChars = string.ascii_letters
    __numericChars = string.digits
    __hexDigits = string.hexdigits


    @staticmethod
    def randomAlpha(minLength, maxLength, chars=None):
        if not chars:
            chars = StringUtils.__alphabeticChars
        length = random.randrange(minLength, maxLength)
        return ''.join(random.choice(chars) for i in range(length))

    @staticmethod
    def randomAlphaNumeric(minLength, maxLength, chars=None):
        if not chars:
            chars = StringUtils.__alphabeticChars.join(StringUtils.__numericChars)
        length = random.randrange(minLength, maxLength)
        return ''.join(random.choice(chars) for i in range(length))

    @staticmethod
    def randomDate(minDate, maxDate):
        minOrdinal = minDate.toordinal()
        maxOrdinal = maxDate.toordinal()
        ordinal = random.randrange(minOrdinal, maxOrdinal)
        return date.fromordinal(ordinal)

    @staticmethod
    def randomDateTime(minDate, maxDate):
        minOrdinal = minDate.toordinal()
        maxOrdinal = maxDate.toordinal()
        ordinal = random.randrange(minOrdinal, maxOrdinal)
        tempDate = date.fromordinal(ordinal)
        hour = random.randrange(0, 23)
        minute = random.randrange(0, 59)
        second = random.randrange(0, 59)
        tempTime = time(hour, minute, second)
        return datetime.combine(tempDate, tempTime)
    
    @staticmethod
    def randomNumeric(minLength, maxLength, chars=None):
        if not chars:
            chars = StringUtils.__numericChars
        length = random.randrange(minLength, maxLength)
        return ''.join(random.choice(chars) for i in range(length))

    @staticmethod
    def randomRange(minValue, maxValue):
        return random.randrange(minValue, maxValue)
    

class Field:

    def __init__(self, name=None, dataType=None, minValue=None, maxValue=None, value=None):
        self.message = ""
        self.valid = True
        if name:
            self.name = name
        else:
            self.name = ""
        if dataType:
            self.dataType = dataType
        else:
            self.dataType = ""
        if minValue:
            self.minValue = minValue
        else:
            self.minValue = 5
        if maxValue:
            self.maxValue = maxValue
        else:
            self.maxValue = 10
        if value:
            self.value = value
        else:
            self.value = StringUtils.randomAlphaNumeric(self.minValue, self.maxValue)
        self.text = str(value)
    
    def toString(self):
        print ("Name: ", self.name, ", DataType: ", self.dataType, ", MinLength: ", self.minValue, ", MaxLength: ", self.maxValue, ", Value: ", self.value, ", Valid: ", self.valid)

    def random(self, minValue=None, maxValue=None, chars=None):
        dataType = self.dataType.lower()
        if not minValue:
            minValue = self.minValue
        if not maxValue:
            maxValue = self.maxValue
        if   dataType == "alpha":
            self.value = StringUtils.randomAlpha(minValue, maxValue, chars)
            self.text = str(self.value)
        elif dataType == "alphanumeric":
            self.value = StringUtils.randomAlphaNumeric(minValue, maxValue, chars)            
            self.text = str(self.value)
        elif dataType == "date":
            self.value = StringUtils.randomDate(minValue, maxValue)            
            self.text = str(self.value)
        elif dataType == "datetime":
            self.value = StringUtils.randomDateTime(minValue, maxValue)       
            self.text = self.value.isoformat()
        elif dataType == "numeric":
            self.value = StringUtils.randomNumeric(minValue, maxValue, chars)
            self.text = str(self.value)
        elif dataType == "range":
            self.value = StringUtils.randomRange(minValue, maxValue)
            self.text = str(self.value)
        elif dataType == "string":
            self.value = StringUtils.randomAlphaNumeric(minValue, maxValue, chars)            
            self.text = str(self.value)
        elif dataType == "uuid4":
            self.value = uuid.uuid4()            
            self.text = str(self.value)
        else:
            self.value = StringUtils.randomAlphaNumeric(minValue, maxValue, chars)            
            self.text = str(self.value)
        return self

    def capitalize(self):
        if self.valid:
            self.value = self.value.capitalize()
            self.text = str(self.value)
        return self

    def center(self, width, fillchar=None):
        if self.valid:
            self.value = self.value.center(width, fillchar)
            self.text = str(self.value)
        return self

    def concat(self, value):
        if self.valid:
            self.value += value
            self.text = str(self.value)
        return self
 
    def count(self, sub, start=None, end=None):
        if self.valid:
            self.value = self.value.count(sub, start, end)
            self.text = str(self.value)
        return self

    def days(self, date1, date2):
        if self.valid:
            delta = date1 - date2
            self.value = delta.days
            self.text = str(self.value)
        return self
 
    def endsWith(self, prefix, start=None, end=None):
        if self.valid:
            self.value = self.value.endswith(prefix, start, end)
            self.text = str(self.value)
        return self
 
    def find(self, sub, start=None, end=None):
        if self.valid:
            self.value = self.value.find(sub, start, end)
            self.text = str(self.value)
        return self
 
    def format(self, args, kwargs):
        if self.valid:
            self.value = self.value.format(args, kwargs)
            self.text = str(self.value)
        return self
 
    def index(self, sub, start=None, end=None):
        if self.valid:
            self.value = self.value.index(sub, start, end)
            self.text = str(self.value)
        return self
   
    def isAlphaNumeric(self):
        if self.valid:
            self.valid = self.value.isalnum()
            if not self.valid:
                self.message = "'{}'.isAlphaNumeric=FALSE".format(self.value)
        return self
    
    def isAlpha(self):
        if self.valid:
            self.valid = self.value.isalpha()
            if not self.valid:
                self.message = "'{}'.isAlpha=FALSE".format(self.value)
        return self
    
    def isLower(self):
        if self.valid:
            self.valid = self.value.islower()
            if not self.valid:
                self.message = "'{}'.isLower=FALSE".format(self.value)
        return self
    
    def isNumeric(self):
        if self.valid:
            self.valid = self.value.isdigit()
            if not self.valid:
                self.message = "'{}'.isNumeric=FALSE".format(self.value)
        return self
    
    def isSpace(self):
        if self.valid:
            self.valid = self.value.isspace()
            if not self.valid:
                self.message = "'{}'.isSpace=FALSE".format(self.value)
        return self
    
    def isTitle(self):
        if self.valid:
            self.valid = self.value.istitle()
            if not self.valid:
                self.message = "'{}'.isTitle=FALSE".format(self.value)
        return self
    
    def isUpper(self):
        if self.valid:
            self.valid = self.value.isupper()
            if not self.valid:
                self.message = "'{}'.isUpper=FALSE".format(self.value)
        return self

    def join(self, iterable):
        if self.valid:
            self.value = self.value.join(iterable)
            self.text = str(self.value)
        return self

    def lower(self):
        if self.valid:
            self.value = self.value.lower()
            self.text = str(self.value)
        return self

    def ljust(self, width, fillchar=None):
        if self.valid:
            self.value = self.value.ljust(width, fillchar)
            self.text = str(self.value)
        return self
    
    def lstrip(self):
        if self.valid:
            self.value = self.value.lstrip()
            self.text = str(self.value)
        return self

    def months(self, date1, date2):
        if self.valid:
            delta = relativedelta.relativedelta(date1, date2)
            self.value = (delta.years * 12) + delta.months
            self.text = str(self.value)
        return self

    def replace(self, old, new, count=None):
        if self.valid:
            self.value = self.value.replace(old, new, count)
            self.text = str(self.value)
        return self

    def rjust(self, width, fillchar=None):
        if self.valid:
            self.value = self.value.rjust(width, fillchar)
            self.text = str(self.value)
        return self

    def rstrip(self):
        if self.valid:
            self.value = self.value.rstrip()
            self.text = str(self.value)
        return self

    def startswith(self, prefix, start=None, end=None):
        if self.valid:
            self.value = self.value.startswith(prefix, start, end)
            self.text = str(self.value)
        return self

    def strip(self):
        if self.valid:
            self.value = self.value.strip()
            self.text = str(self.value)
        return self

    def swapcase(self):
        if self.valid:
            self.value = self.value.swapcase()
            self.text = str(self.value)
        return self

    def title(self):
        if self.valid:
            self.value = self.value.title()
            self.text = str(self.value)
        return self

    def upper(self):
        if self.valid:
            self.value = self.value.upper()
            self.text = str(self.value)
        return self

    def uuid4(self):
        # make a random UUID
        if self.valid:
            self.value = uuid.uuid4()
            self.text = str(self.value)
        return self
    
    def years(self, date1, date2):
        if self.valid:
            delta = relativedelta.relativedelta(date1, date2)
            self.value = delta.years
            self.text = str(self.value)
        return self

    def zfill(self, width):
        if self.valid:
            self.value = self.value.zfill(width)
            self.text = str(self.value)
        return self


class Record:
    
    fields = OrderedDict()

    def __init__(self):
        self.fields.clear()
        
    def addField(self, name, dataType=None, minLength=None, maxLength=None, value=None):
        field = Field(name, dataType, minLength, maxLength, value)
        self.fields[name] = field
        return field

    def getField(self, name):
        field = self.fields.get(name)
        return field

    def toCsvHeader(self, colSeparator):
        # join the field values together, removing the last colSeparator when finished
        return "".join([field.name + colSeparator for field in self.fields.values()])[:-1]
    
    def toCsvValues(self, colSeparator):
        # join the field values together, removing the last colSeparator when finished
        return "".join([field.text + colSeparator for field in self.fields.values()])[:-1]

    def toString(self):
        for elem in self.fields.values():
            elem.toString()


def main():
    
    properties = Properties()
    properties_file_path = "/PyDataGenerator.properties"
    if properties_file_path.startswith('~'):
        properties_file_path = os.path.expanduser(properties_file_path)
    properties.load(open(properties_file_path))
    properties.list()

    maxRows = 100
    maxXlsRows = 10000
    
    globalPath = '/home/khepry/PyDataGenerator/temp/'
    os.makedirs(globalPath, exist_ok=True)

    targetName = 'dataGenerator.csv'

    maxRows = int(properties.getProperty('maxRows'))
    maxXlsRows = int(properties.getProperty('maxXlsRows'))

    globalPath = properties.getProperty('globalPath')
    os.makedirs(globalPath, exist_ok=True)
    targetName = properties.getProperty('targetName')
    
    print("-- operating system --")
    print(platform.system())
    
    print("-- processing messages --")
    
    if platform.system() == 'Windows':
        xlsPgmPath = '"/Program Files/Microsoft Office 15/root/office15/EXCEL.EXE"'
        txtPgmPath = '"/Program Files (x86)/Notepad++/notepad++.exe"'
    else:
        xlsPgmPath = "libreoffice"
        txtPgmPath = "gedit"
    
    tgtFileFullPath = os.path.abspath(globalPath + targetName)
    tgtFile = open(tgtFileFullPath, 'w', newline='')

    bgnTime = tyme.time()

    rows = 0
    
    try:
        writer = csv.writer(tgtFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for i in range(0, maxRows):
            rows += 1

            # TODO: Tweak static/validate_csv_templates as needed
            # TODO: Soft-code the following "record" using a YAML file
            # TODO: Convert PyDataGenerator.properties to ENV file

            record = Record()
            record.addField("UUID4", "UUID4").random()
            record.addField("Alpha", "Alpha").random(20, 25)
            record.addField("AlphaNumeric", "AlphaNumeric").random()
            record.addField("Numeric", "Numeric").random()
            record.addField("String", "String").random()
            record.addField("Range", "Range").random(12, 24)
            record.addField("Date", "Date").random(date(1980,1,1), date(2000,12,31))
            record.addField("DateTime", "DateTime").random(date(1980,1,1), date(2000,12,31))
            record.addField("AgeInYears", "Numeric").years(date.today(), record.getField("Date").value)
            record.addField("AgeInMonths", "Numeric").months(date.today(), record.getField("Date").value)
            record.addField("AgeInDays", "Numeric").days(date.today(), record.getField("Date").value)
                
            if i == 0:
                writer.writerow([key for key in record.fields.keys()])
            writer.writerow([field.text for field in record.fields.values()])
            
    finally:
        tgtFile.close()

    endTime = tyme.time()

    elapsedTime = endTime - bgnTime

    print("{:,}".format(rows) + ' records processed in ' + "{:,.4f}".format(elapsedTime) + ' seconds at ' + "{:,.4f}".format(rows / elapsedTime) + ' rows/second.')

    if (platform.system() == 'Windows'):
        if (rows < maxXlsRows):
            subprocess.call(xlsPgmPath + ' "' + tgtFileFullPath + '"')
        else:
            subprocess.call(txtPgmPath + ' "' + tgtFileFullPath + '"')
    else:
        if (rows < maxXlsRows):
            subprocess.call([xlsPgmPath, tgtFileFullPath])
        else:
            subprocess.call([txtPgmPath, tgtFileFullPath])


if __name__ == '__main__':
    main()        
