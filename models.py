class Seat:  
  id = None
  type = None
  price = None
  cabin_class = None
  availability = None

  def __init__( self, id, type, price, cabin_class, availability ):
    self.id = id
    self.type = type
    self.price = price
    self.cabin_class = cabin_class
    self.availability = availability

  def __repr__(self):
    return f"Seat('{self.id}', '{self.type}', '{self.price}', '{self.cabin_class}', '{self.availability}')"