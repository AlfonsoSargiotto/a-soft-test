import os
import json
from xml.etree import ElementTree as ET
from models import Seat

file_name = 'seatmap1.xml'  # this will me received from CLI
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
service_tag = f'{ota_uri}Service'
fee_tag = f'{ota_uri}Fee'
taxes_tag = f'{ota_uri}Taxes'

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
                              ----> Service:
                                  ----> Fee(attribs: Amount, CurrencyCode):
                                      ----> Taxes(attribs: Amount, CurrencyCode)


'''


all_tags = root.findall('.//')  # find all the SeatMap tags
# print (all_tags)
body = root.findall(body_tag)

ota = root.find(f'.//{ota_tag}')
# print (ota)

seat_map_responses = ota.find(seat_map_responses_tag)
seat_map_response = seat_map_responses.find(seat_map_response_tag)
seat_map_details = seat_map_response.find(seat_map_details_tag)
cabin_classes = seat_map_details.findall(cabin_class_tag)

all_seats = []
all_seats_json = []

for cabin_class in cabin_classes:
    rows_info = cabin_class.findall(row_info_tag)
    for row_info in rows_info:
        cabin_type = row_info.attrib.get('CabinType')
        seats_info = row_info.findall(seat_info_tag)
        for seat_info in seats_info:
            summary = seat_info.find(summary_tag)
            available_ind = summary.attrib.get('AvailableInd')
            if available_ind == 'true':
                available_ind = True
            else:
                available_ind = False

            service = seat_info.find(service_tag)
            final_price = '-'
            if service:
                fee = service.find(fee_tag)
                fee_amt = float(fee.attrib.get('Amount'))
                fee_currency = fee.attrib.get('CurrencyCode')
                taxes = fee.find(taxes_tag)
                taxes_amt = float(taxes.attrib.get('Amount'))
                final_price = taxes_amt + fee_amt
            seat_number = summary.attrib.get('SeatNumber')
            seat = Seat(seat_number, "Seat", final_price,
                        cabin_type, available_ind)
            all_seats.append(seat)


for seat in all_seats:
    json_seat = (seat.__dict__)
    all_seats_json.append(json_seat)

with open('seatmap1.json', 'w', encoding='utf8') as f:
    json.dump(all_seats_json, f, ensure_ascii=False, indent=4)
