import os
import argparse

import meshtastic
import meshtastic.serial_interface

import simplekml

parser = argparse.ArgumentParser(
    description = 'This program connects to meshtastic node and export heared node list to KML/KMZ',
    epilog = 'Feel free to contribute',
)
parser.add_argument('-f', '--filename',
    required = False,
    default = 'nodedb.kml',
    help = 'filename to export',
)
parser.add_argument('-F', '--format',
    default = 'auto',
    choices = ['auto', 'kml', 'kmz'],
    help = 'auto - use format from extension',
)
parser.add_argument('-v', '--verbose',
    action = 'store_true',
    help = 'Show more debug info',
)

args = parser.parse_args()

# Chose format to save
if(args.format == 'auto'):
    args.format = os.path.splitext(args.filename)[1][1::]
if(args.format not in ['kml', 'kmz']):
    print(f'Wrong file format `{args.format}`. Specify correct one with --format')
    exit(-1)


interface = meshtastic.serial_interface.SerialInterface()
print('Connected')

kml = simplekml.Kml()
kml.document.name = 'Meshtastic'
count = 0
for nodeid, node in interface.nodes.items():
    pos = None
    pos = node.get('position')
    if pos is None or 'longitude' not in pos.keys() or 'latitude' not in pos.keys():
        if(args.verbose):
            print(f'Skip\t{nodeid}({node['user']['shortName']})\tno location data')
        continue

    if(args.verbose):
        print(f'Add\t{nodeid}({node['user']['shortName']})\t{pos['longitude']}\t{pos['latitude']}')
    count += 1
    kml.newpoint(
                name=node['user']['shortName'],
                coords=[(pos['longitude'], pos['latitude'])]
                )
print('Node list processed')
print(f'Added {count}/{len(interface.nodes.items())} nodes')

if(args.format == 'kml'):
    kml.save(args.filename)
    print(f'Saved kml to {args.filename}')
    exit(0)
if(args.format == 'kmz'):
    kml.savekmz(args.filename)
    print(f'Saved kmz to {args.filename}')
    exit(0)

exit(-2)