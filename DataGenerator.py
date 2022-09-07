"""
Created on Feb 19, 2014

@author: David Darling <david.darling@khepry.com>
"""

# !/usr/bin/python

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
    def random_alpha(min_length, max_length, chars=None, prefix=None, suffix=None):
        if not chars:
            chars = StringUtils.__alphabeticChars
        length = random.randrange(min_length, max_length)
        value = ''.join(random.choice(chars) for _ in range(length))
        if prefix:
            value = prefix + value
        if suffix:
            value = value + suffix
        return value

    @staticmethod
    def random_alphanumeric(min_length, max_length, chars=None, prefix=None, suffix=None):
        if not chars:
            chars = StringUtils.__alphabeticChars.join(StringUtils.__numericChars)
        length = random.randrange(min_length, max_length)
        value = ''.join(random.choice(chars) for _ in range(length))
        if prefix:
            value = prefix + value
        if suffix:
            value = value + suffix
        return value

    @staticmethod
    def random_date(min_date, max_date):
        min_ordinal = min_date.toordinal()
        max_ordinal = max_date.toordinal()
        ordinal = random.randrange(min_ordinal, max_ordinal)
        return date.fromordinal(ordinal)

    @staticmethod
    def random_datetime(min_date, max_date):
        min_ordinal = min_date.toordinal()
        max_ordinal = max_date.toordinal()
        ordinal = random.randrange(min_ordinal, max_ordinal)
        temp_date = date.fromordinal(ordinal)
        hour = random.randrange(0, 23)
        minute = random.randrange(0, 59)
        second = random.randrange(0, 59)
        temp_time = time(hour, minute, second)
        return datetime.combine(temp_date, temp_time)
    
    @staticmethod
    def random_numeric(min_length, max_length, chars=None, prefix=None, suffix=None, decimal_places=0):
        if not chars:
            chars = StringUtils.__numericChars
        length = random.randrange(min_length, max_length)
        value = ''.join(random.choice(chars) for _ in range(length))
        value = str(round(float(value), decimal_places))
        if prefix:
            value = prefix + value
        if suffix:
            value = value + suffix
        return value

    @staticmethod
    def random_range(min_value, max_value, prefix=None, suffix=None):
        value = str(random.randrange(min_value, max_value))
        if prefix:
            value = prefix + value
        if suffix:
            value = value + suffix
        return value

    @staticmethod
    def random_uniform(min_value, max_value, prefix=None, suffix=None, decimal_places=0):
        value = round(random.uniform(min_value, max_value), decimal_places)
        if prefix:
            value = prefix + value
        if suffix:
            value = value + suffix
        return value


class Field:

    def __init__(self,
                 name=None,
                 data_type=None,
                 min_value=None,
                 max_value=None,
                 value=None,
                 prefix=None,
                 suffix=None,
                 decimal_places=0):
        self.message = ""
        self.valid = True
        self.prefix = prefix
        self.suffix = suffix
        self.decimal_places = decimal_places
        if name:
            self.name = name
        else:
            self.name = ""
        if data_type:
            self.data_type = data_type
        else:
            self.data_type = ""
        if min_value:
            self.min_value = min_value
        else:
            self.min_value = 5
        if max_value:
            self.max_value = max_value
        else:
            self.max_value = 10
        if value:
            self.value = value
        else:
            self.value = StringUtils.random_alphanumeric(self.min_value,
                                                         self.max_value,
                                                         prefix=self.prefix,
                                                         suffix=self.suffix)
        self.text = str(value)
    
    def to_string(self):
        print("name: ", self.name,
              ", data_type: ", self.data_type,
              ", min_length: ", self.min_value,
              ", max_length: ", self.max_value,
              ", value: ", self.value,
              ", valid: ", self.valid)

    def random(self, min_value=None, max_value=None, chars=None, prefix=None, suffix=None, decimal_places=0):
        data_type = self.data_type.lower()
        if not min_value:
            min_value = self.min_value
        if not max_value:
            max_value = self.max_value
        if data_type == "alpha":
            self.value = StringUtils.random_alpha(min_value, max_value, chars, prefix, suffix)
            self.text = str(self.value)
        elif data_type == "alphanumeric":
            self.value = StringUtils.random_alphanumeric(min_value, max_value, chars, prefix, suffix)
            self.text = str(self.value)
        elif data_type == "date":
            self.value = StringUtils.random_date(min_value, max_value)
            self.text = str(self.value)
        elif data_type == "datetime":
            self.value = StringUtils.random_datetime(min_value, max_value)
            self.text = self.value.isoformat()
        elif data_type == "numeric":
            self.value = StringUtils.random_numeric(min_value, max_value, chars, prefix, suffix, decimal_places)
            self.text = str(self.value)
        elif data_type == "rangeint":
            self.value = StringUtils.random_range(min_value, max_value, prefix, suffix)
            self.text = str(self.value)
        elif data_type == "rangefloat":
            self.value = StringUtils.random_uniform(min_value, max_value, prefix, suffix, decimal_places)
            self.text = str(self.value)
        elif data_type == "string":
            self.value = StringUtils.random_alphanumeric(min_value, max_value, chars, prefix, suffix)
            self.text = str(self.value)
        elif data_type == "uuid4":
            self.value = uuid.uuid4()            
            self.text = str(self.value)
        else:
            self.value = StringUtils.random_alphanumeric(min_value, max_value, chars, prefix, suffix)
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
 
    def ends_with(self, prefix, start=None, end=None):
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
   
    def is_alphanumeric(self):
        if self.valid:
            self.valid = self.value.isalnum()
            if not self.valid:
                self.message = "'{}'.isAlphaNumeric=FALSE".format(self.value)
        return self
    
    def is_alpha(self):
        if self.valid:
            self.valid = self.value.isalpha()
            if not self.valid:
                self.message = "'{}'.isAlpha=FALSE".format(self.value)
        return self
    
    def is_lower(self):
        if self.valid:
            self.valid = self.value.islower()
            if not self.valid:
                self.message = "'{}'.isLower=FALSE".format(self.value)
        return self
    
    def is_numeric(self):
        if self.valid:
            self.valid = self.value.isdigit()
            if not self.valid:
                self.message = "'{}'.isNumeric=FALSE".format(self.value)
        return self
    
    def is_space(self):
        if self.valid:
            self.valid = self.value.isspace()
            if not self.valid:
                self.message = "'{}'.isSpace=FALSE".format(self.value)
        return self
    
    def is_title(self):
        if self.valid:
            self.valid = self.value.istitle()
            if not self.valid:
                self.message = "'{}'.isTitle=FALSE".format(self.value)
        return self
    
    def is_upper(self):
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

    def random_from_list(self, list_values: list):
        if self.valid:
            self.value = random.choice(list_values)
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

    def starts_with(self, prefix, start=None, end=None):
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
        
    def add_field(self,
                  name,
                  data_type=None,
                  min_value=None,
                  max_value=None,
                  value=None,
                  prefix=None,
                  suffix=None,
                  decimal_places=2):
        field = Field(name, data_type, min_value, max_value, value, prefix, suffix, decimal_places)
        self.fields[name] = field
        return field

    def get_field(self, name):
        field = self.fields.get(name)
        return field

    def to_csv_header(self, col_separator=','):
        # join the field values together, removing the last colSeparator when finished
        return "".join([field.name + col_separator for field in self.fields.values()])[:-1]
    
    def to_csv_values(self, col_separator=','):
        # join the field values together, removing the last colSeparator when finished
        return "".join([field.text + col_separator for field in self.fields.values()])[:-1]

    def to_string(self):
        for elem in self.fields.values():
            elem.toString()


class XampleRecord(Record):
    def __init__(self):
        super().__init__()
        record = Record()
        record.add_field("UUID4", "UUID4").random()
        record.add_field("Alpha", "Alpha").random(20, 25)
        record.add_field("AlphaNumeric", "AlphaNumeric").random()
        record.add_field("Numeric", "Numeric").random()
        record.add_field("String", "String").random()
        record.add_field("Range", "Range").random(12, 24)
        record.add_field("Date", "Date").random(date(1980, 1, 1), date(2000, 12, 31))
        record.add_field("DateTime", "DateTime").random(date(1980, 1, 1), date(2000, 12, 31))
        record.add_field("AgeInYears", "Numeric").years(date.today(), record.get_field("Date").value)
        record.add_field("AgeInMonths", "Numeric").months(date.today(), record.get_field("Date").value)
        record.add_field("AgeInDays", "Numeric").days(date.today(), record.get_field("Date").value)


class NventoryRecord(Record):
    def __init__(self):
        super().__init__()
        record = Record()
        record.add_field("inventory_id", "AlphaNumeric").random(5, 10, prefix="LG")
        record.add_field("producer", "Alpha").random_from_list(['ab', 'fx', 'gr', 'mg', 'wd', 'xx'])
        record.add_field("grading_lab_code", "Alpha").random_from_list(['GCAL', 'IGI'])
        record.add_field("grading_lab_report_id", "AlphaNumeric").random(10, 15)
        record.add_field("grading_lab_report_date", "Date").random(date(2010, 1, 1), date.today())
        record.add_field("stone_type_code", "Alpha").random_from_list(['LabGrown', 'Lab Grown', 'LAB GROWN', 'LabCreated', 'LABCREATED'])
        record.add_field("production_location", "AlphaNumeric").random_from_list(['ND', 'Surat', 'WD_Maryland', 'Nesher Israel', 'SCS-RD'])
        record.add_field("production_date", "Date").random(date(2010, 1, 1), date.today())
        record.add_field("date_of_shipping_from_producer", "Date").random(date(2010, 1, 1), date.today())
        record.add_field("carat_wt_pregraded", "RangeFloat").random(1, 15, decimal_places=2)
        record.add_field("shape_code_pregraded", "AlphaNumber").random(2, 10)
        record.add_field("measure_1_pregraded", "RangeFloat").random(1, 10, decimal_places=2)
        record.add_field("measure_2_pregraded", "RangeFloat").random(1, 10, decimal_places=2)
        record.add_field("measure_3_pregraded", "RangeFloat").random(1, 10, decimal_places=2)
        record.add_field("cutter_code", "AlphaNumeric").random_from_list(['Self', 'ABC', 'DEF'])
        record.add_field("cutter_location_code", "AlphaNumeric").random_from_list(['Self', 'ABC', 'DEF'])
        record.add_field("date_of_receipt_at_cutter", "Date").random(date(2010, 1, 1), date.today())
        record.add_field("date_of_shipping_from_cutter", "Date").random(date(2010, 1, 1), date.today())
        record.add_field("mother_stone_id", "AlphaNumeric").random(5, 10)
        record.add_field("mother_stone_carat_wt_as_grown", "RangeFloat").random(0.5, 15, decimal_places=2)
        record.add_field("mother_stone_carat_wt_as_cored", "RangeFloat").random(0.5, 15, decimal_places=2)
        record.add_field("mother_stone_machine_id", "AlphaNumeric").random(5, 10)
        record.add_field("soft_deleted", "Alpha").random_from_list(['false', 'true'])


def main():
    
    properties = Properties()
    properties_file_path = "PyDataGenerator.properties"
    if properties_file_path.startswith('~'):
        properties_file_path = os.path.expanduser(properties_file_path)
    properties.load(open(properties_file_path))
    properties.list()

    global_path = '/home/khepry/PyDataGenerator/temp/'
    os.makedirs(global_path, exist_ok=True)

    max_rows = int(properties.getProperty('max_rows'))
    max_xls_rows = int(properties.getProperty('max_xls_rows'))

    global_path = properties.getProperty('global_path')
    os.makedirs(global_path, exist_ok=True)
    target_name = properties.getProperty('target_name')
    
    print("-- operating system --")
    print(platform.system())
    
    print("-- processing messages --")
    
    if platform.system() == 'Windows':
        xls_pgm_path = '"/Program Files/Microsoft Office 15/root/office15/EXCEL.EXE"'
        txt_pgm_path = '"/Program Files (x86)/Notepad++/notepad++.exe"'
    else:
        xls_pgm_path = "libreoffice"
        txt_pgm_path = "gedit"
    
    tgt_file_full_path = os.path.abspath(global_path + target_name)
    tgt_file = open(tgt_file_full_path, 'w', newline='')

    bgn_time = tyme.time()

    rows = 0
    
    try:
        writer = csv.writer(tgt_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for i in range(0, max_rows):
            rows += 1

            # DONE: Modify methods and variables for PEP-8 compliance
            # DONE: Tweak static/validate_csv_templates as needed
            # DONE: Add prefix, suffix, and decimal_places logic to field values
            # TODO: Tweak the following "record" using additional Record classes
            # TODO: Convert PyDataGenerator.properties to ENV file

            record = NventoryRecord()

            if i == 0:
                writer.writerow([key for key in record.fields.keys()])
            writer.writerow([field.text for field in record.fields.values()])
            
    finally:
        tgt_file.close()

    end_time = tyme.time()

    elapsed_time = end_time - bgn_time

    print("{:,}".format(rows) + ' records processed in ' + "{:,.4f}".format(elapsed_time) + ' seconds at ' + "{:,.4f}".format(rows / elapsed_time) + ' rows/second.')

    if platform.system() == 'Windows':
        if rows < max_xls_rows:
            subprocess.call(xls_pgm_path + ' "' + tgt_file_full_path + '"')
        else:
            subprocess.call(txt_pgm_path + ' "' + tgt_file_full_path + '"')
    else:
        if rows < max_xls_rows:
            subprocess.call([xls_pgm_path, tgt_file_full_path])
        else:
            subprocess.call([txt_pgm_path, tgt_file_full_path])


if __name__ == '__main__':
    main()        
