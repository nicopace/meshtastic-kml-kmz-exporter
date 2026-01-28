import argparse
import os
import sys

import meshtastic
import meshtastic.serial_interface
import simplekml

parser = argparse.ArgumentParser(
    description="This program connects to meshtastic node and export heared node list to KML/KMZ",
    epilog="Feel free to contribute",
)
parser.add_argument(
    "-f",
    "--filename",
    required=False,
    default="-",
    help="filename to export, use - for stdout",
)
parser.add_argument(
    "-F",
    "--format",
    default="auto",
    choices=["auto", "kml", "kmz"],
    help="auto - use format from extension",
)
parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    help="Show more debug info",
)

args = parser.parse_args()

# Chose format to save
if args.format == "auto":
    args.format = os.path.splitext(args.filename)[1][1::]
if args.format not in ["kml", "kmz"]:
    print(
        f"Wrong file format `{args.format}`. Specify correct one with --format",
        file=sys.stderr,
    )
    exit(-1)


interface = meshtastic.serial_interface.SerialInterface()
print("Connected", file=sys.stderr)

kml = simplekml.Kml()
kml.document.name = "Meshtastic"
count = 0
for nodeid, node in interface.nodes.items():
    pos = None
    pos = node.get("position")
    if pos is None or "longitude" not in pos.keys() or "latitude" not in pos.keys():
        if args.verbose:
            print(
                f"Skip\t{nodeid}({node['user']['shortName']})\tno location data",
                file=sys.stderr,
            )
        continue

    if args.verbose:
        print(
            f"Add\t{nodeid}({node['user']['shortName']})\t{pos['longitude']}\t{pos['latitude']}",
            file=sys.stderr,
        )
    count += 1
    kml.newpoint(
        name=node["user"]["shortName"], coords=[(pos["longitude"], pos["latitude"])]
    )
print("Node list processed", file=sys.stderr)
print(f"Added {count}/{len(interface.nodes.items())} nodes", file=sys.stderr)

# Output to stdout if filename is '-'
if args.filename == "-":
    print(kml.kml(), end="")
    exit(0)

if args.format == "kml":
    kml.save(args.filename)
    print(f"Saved kml to {args.filename}", file=sys.stderr)
    exit(0)
if args.format == "kmz":
    kml.savekmz(args.filename)
    print(f"Saved kmz to {args.filename}", file=sys.stderr)
    exit(0)

exit(-2)
