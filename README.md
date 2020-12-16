# PaloBulkAddressImport
Convert CSV of Addresses/Subnets to Palo Alto set format commands to bulk import into PAN-OS or Panorama

Input CSV should be formatted like this example:

name,description,address,netmask,tag
object1,first,10.1.2.1,255.255.255.0,
object2,Multi-word description,1.2.3.4,255.255.255.255,Host
Third Object,,10.0.0.0,255.255.0.0,Network

Resulting output (if running for Panorama):

set device-group DG-Name address "object1" description "first" ip-netmask 10.1.2.1/24
set device-group DG-Name address "object2" description "Multi-word description" tag Host ip-netmask 1.2.3.4
set device-group DG-Name address "Third Object" tag Network ip-netmask 10.0.0.0/16

Resulting output (if no Panorama Device Group):

set address "object1" description "first" ip-netmask 10.1.2.1/24
set address "object2" description "Multi-word description" tag Host ip-netmask 1.2.3.4
set address "Third Object" tag Network ip-netmask 10.0.0.0/16
