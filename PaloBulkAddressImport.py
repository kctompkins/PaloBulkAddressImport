import ntpath
import csv
import netmaskdictionary
import sys

# Import Dictionary of netmasks in CIDR
netmaskDict = netmaskdictionary.netmaskDict

print('Input the file location in full directory format, IE: C:\\temp\\file.txt')
fileLocation = input('Location of Bulk Import CSV File: ')
# Save file directory for use in writing output file at the end of the script
fileDir = ntpath.dirname(fileLocation)

print('If the addresses will be imported into Panorama, enter the Device Group. Otherwise, leave the device group blank.')
deviceGroup = input('Device Group (leave blank if there is no Panorama): ')

#Turn CSV into a nested dictionary
addressDict = {}
try:
    with open(fileLocation) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            tempDict = {}
            for i in row.keys():
                tempDict[i]= row[i]
            addressDict[line_count]= tempDict
            line_count += 1
    print(f'Processed {len(addressDict)} lines from CSV File')
except FileNotFoundError:
    print('FileNotFoundError: ', sys.exc_info()[1])
except OSError:
    print('OSError: ', sys.exc_info()[1])
except:
    print(f'Error: Unknown error processing CSV file {fileLocation}', sys.exc_info()[0])

#Generate Palo Alto set commands for addresses and append to list
try:
    setAddress = ""
    output = []
    line_count = 0
    if not deviceGroup:
        for address in addressDict:
            setAddress = 'set address "'+addressDict[line_count]['name']+'"'
            if addressDict[line_count]['description'] != "":
                setAddress = setAddress+' description "'+addressDict[line_count]['description']+'"'
            if addressDict[line_count]['tag'] != "":
                setAddress = setAddress+' tag '+addressDict[line_count]['tag']
            setAddress = setAddress+' ip-netmask '+addressDict[line_count]['address']
            if addressDict[line_count]['netmask'] == '255.255.255.255':
                setAddress = setAddress+'\n'
            else:
                setAddress = setAddress+netmaskDict[addressDict[line_count]['netmask']]+'\n'
            output.append(setAddress)
            line_count += 1
    else:
        for address in addressDict:
            setAddress = 'set device-group '+deviceGroup+' address "'+addressDict[line_count]['name']+'"'
            if addressDict[line_count]['description'] != "":
                setAddress = setAddress+' description "'+addressDict[line_count]['description']+'"'
            if addressDict[line_count]['tag'] != "":
                setAddress = setAddress+' tag '+addressDict[line_count]['tag']
            setAddress = setAddress+' ip-netmask '+addressDict[line_count]['address']
            if addressDict[line_count]['netmask'] == '255.255.255.255':
                setAddress = setAddress+'\n'
            else:
                setAddress = setAddress+netmaskDict[addressDict[line_count]['netmask']]+'\n'                  
            output.append(setAddress)
            line_count += 1
except:
    print(f'Error: Failed to generate set commands at line {line_count}')    
    print(sys.exc_info()[0], sys.exc_info()[1])

# Save set commands to output file
try:
    with open(fileDir+'\\'+'output.txt', 'w+') as file_handler:
        for item in output:
            file_handler.write('{}'.format(item))
except:
    print(f'Error: Unable to write addresses to file')
    print(sys.exc_info()[0], sys.exc_info()[1])