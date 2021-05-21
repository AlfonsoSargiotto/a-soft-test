import os
import json
from xml.etree import ElementTree as ET
from models import Seat

def seat_map_parser_2(file_name):

  full_file_path = os.path.abspath(os.path.join('data', file_name))

  tree = ET.parse(full_file_path)

  root = tree.getroot()

  base_uri = "{http://www.iata.org/IATA/EDIST/2017.2}"
  seat_map_tag = f'{base_uri}SeatMap'
  cabin_tag = f'{base_uri}Cabin'
  segment_ref_tag = f'{base_uri}SegmentRef'
  row_tag = f'{base_uri}Row'
  number_tag = f'{base_uri}Number'
  seat_tag = f'{base_uri}Seat'
  column_tag = f'{base_uri}Column'
  offer_item_refs_tag = f'{base_uri}OfferItemRefs'
  a_la_carte_offer_tag = f'{base_uri}ALaCarteOffer'
  a_la_carte_offer_item_tag = f'{base_uri}ALaCarteOfferItem'
  unit_price_detail_tag = f'{base_uri}UnitPriceDetail'
  total_amount_tag = f'{base_uri}TotalAmount'
  simple_currency_price = f'{base_uri}SimpleCurrencyPrice'

  '''
  # Seat structure design:

    ----> SeatMap:
        ----> Segment Ref
        ----> Cabin:
            ----> Row:
                ----> Number
                ----> Seat:
                    ----> Column
                    ----> OfferItemRefs

  # Price:
    ----> ALaCarteOffer:
        ----> ALaCarteOfferItem (OfferItemID):
            ----> Elegibility:
                ----> SegmentRefs
                ----> UnitPriceDetail:
                    ----> TotalAmount:
                        ----> SimpleCurrencyPrice (code: currency type)


  ToDo ->get the price: search for all ALaCarteOfferItem tags and work with them: need to get the Code(currecy) and txt

  '''

  def get_price(OfferItemRefs):
    total_price = '-'
    all_offer_items = root.findall(
        f'{a_la_carte_offer_tag}/{a_la_carte_offer_item_tag}')  # get all Offers ID's
    for offer_item in all_offer_items:  # iterate
      attribute = (offer_item.attrib.get('OfferItemID'))  # get ID
      if attribute == OfferItemRefs:
        currency_price = offer_item.find(
            f'{unit_price_detail_tag}/{total_amount_tag}/{simple_currency_price}')
        price = currency_price.text
        currency = currency_price.attrib.get('Code')
        price = float(price)
        if currency == 'GBP':
          price = "£{:,.2f}".format(price)
        else:
          price = "US${:,.2f}".format(price)

        total_price = f'{price}'

    return total_price

  #######

  cabins = []
  rows = []
  seats_map = root.findall(seat_map_tag)  # find all the SeatMap tags

  all_seats = []
  all_seats_json = []

  for seat_map in seats_map:  # loop over all SeatMap tags
    # search for Cabin tag. Each SeatMap has 1 Cabin tag
    cabins = seat_map.find(cabin_tag)
    rows = cabins.findall(row_tag)  # search all Row tags inside cabin
    segment_ref = seat_map.find(segment_ref_tag)  # this is to get ...?
    for row in rows:  # iterate over them to get:
      number = row.find(number_tag)  # the Number tag
      seats = row.findall(seat_tag)  # and the Seat Tags
      for seat in seats:  # now we get every Seat tag in each Row
        column = seat.find(column_tag)  # for the moment we need the Column tag
        offer_ref = None
        price = '-'
        # this is to get the price reference
        offer_item_refs = seat.find(offer_item_refs_tag)
        if offer_item_refs is not None:  # if it has a reference
          offer_ref = offer_item_refs.text  # we take the text  from it
          price = get_price(offer_ref)
          print(price)
        # here we build the seat_id with column+number
        seat_id = f'{column.text}{number.text}'
        x_seat = Seat(seat_id, 'Seat', price, 1, True)  # build the Seat Object
        all_seats.append(x_seat)  # add it to the list

  for seat in all_seats:
    json_seat = (seat.__dict__)
    all_seats_json.append(json_seat)
    print(json_seat)

  with open('seatmap2.json', 'w', encoding='utf8') as f:
    json.dump(all_seats_json, f, ensure_ascii=False, indent=4)
