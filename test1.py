import os
import json
from xml.etree import ElementTree as ET
from models import Seat

file_name = 'seatmap1.xml' # this will me received from CLI
full_file_path = os.path.abspath(os.path.join('data', file_name))

tree = ET.parse(full_file_path)

root = tree.getroot()

base_uri = "{http://schemas.xmlsoap.org/soap/envelope/}"
ota_uri = "{http://www.opentravel.org/OTA/2003/05/common/}"
body_tag = f'{base_uri}Body'
ota_tag = f'{ota_uri}OTA_AirSeatMapRS'
seat_map_responses_tag = f'{ota_uri}SeatMapResponses'
seat_map_response_tag = f'{ota_uri}SeatMapResponse'
seat_map_details_tag = f'{ota_uri}SeatMapDetails'
cabin_class_tag = f'{ota_uri}CabinClass'
row_info_tag = f'{ota_uri}RowInfo'
seat_info_tag = f'{ota_uri}SeatInfo'
summary_tag = f'{ota_uri}Summary'

'''
# Seat structure design:

  ----> Body:
      ----> SeatMapResponses:
          ----> SeatMapResponse:
              ----> SeatMapDetails:
                  ----> CabinClass:
                      ----> RowInfo (attrib:CabinType):
                      ----> SeatInfo (attrib:SeatNumber):
                          ----> Summary (attribs:AvaiableInd,SeatNumber):

'''


all_tags = root.findall('.//') # find all the SeatMap tags
# print (all_tags)
body = root.findall(body_tag)

ota = root.find(f'.//{ota_tag}')
# print (ota)

seat_map_responses = ota.find(seat_map_responses_tag)
# print (seat_map_responses)

seat_map_response = seat_map_responses.find(seat_map_response_tag)
# print (seat_map_response)

seat_map_details = seat_map_response.find(seat_map_details_tag)
# print (seat_map_details)

cabin_classes = seat_map_details.findall(cabin_class_tag)

# print (cabin_classes)

all_seats = []
all_seats_json = []

for cabin_class in cabin_classes:
    # print (cabin_class.attrib['Layout'])
    rows_info = cabin_class.findall(row_info_tag)
    for row_info in rows_info:
        cabin_type = row_info.attrib.get('CabinType')
        # print (cabin_type)
        seats_info = row_info.findall(seat_info_tag)
        for seat_info in seats_info:
            summary =seat_info.find(summary_tag)
            available_ind = summary.attrib.get('AvailableInd')
            seat_number = summary.attrib.get('SeatNumber')
            seat = Seat(seat_number, "Seat", 1, cabin_type, True)
            all_seats.append(seat)
            # print (seat_number)



for seat in all_seats:
    json_seat = (seat.__dict__)
    all_seats_json.append(json_seat)
    print (json_seat)


with open('seatmap1.json', 'w', encoding='utf8') as f:
    json.dump(all_seats_json, f, ensure_ascii=False, indent=4)


