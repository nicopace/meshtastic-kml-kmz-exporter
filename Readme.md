# Meshtastic node db to KML/KMZ export script

## Description
Use this script if you want to export node db to KML/KMZ.

Than you can use this file to import waypoints to garmin/organicmaps/etc

## Usage
### Help output
```
python3  src/main.py --help
usage: main.py [-h] [-f FILENAME] [-F {auto,kml,kmz}] [-v]

This program connects to meshtastic node and export heared node list to KML/KMZ

options:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        filename to export
  -F {auto,kml,kmz}, --format {auto,kml,kmz}
                        auto - use format from extension
  -v, --verbose         Show more debug info

Feel free to contribute
```
### For beginers
1. Install dependencies
```
pip install -r requirements.txt
```
2. Run script
```
python src/main.py
```