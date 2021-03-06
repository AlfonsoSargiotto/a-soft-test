import argparse
from utilities import seat_map_parser_2

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", type=str,
                    help="Name of the file. Must be in 'data' folder")
parser.add_argument("-v", "--verbosity",
                    help="E.g: python3 seatmap_parser.py --filename seatmap1.xml ", action="store_true")

args = parser.parse_args()

seat_map_parser_2(args.filename)