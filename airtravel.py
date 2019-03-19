
"""
__init__() is an initializer, not a constructor. It should not return anything.
polymorphism in python is achieved through duck typing. An objects fitness for purpose is determined at the time of use.
"""

class Flight:
    """
    A flight with a particular passenger aircraft.
    To use:
        f = Flight("BA758", Aircraft("G-EUPT", "Airbus A319", num_rows=22, num_seats_per_row=6))
    """

    def __init__(self, number, aircraft):
        if not number[:2].isalpha():
            raise ValueError("No airline code in '{}'".format(number))
        if not number[:2].isupper():
            raise ValueError("Invalid airline code '{}'".format(number))
        if not (number[2:].isdigit() and int(number[2:]) <= 9999):
            raise ValueError("Invalid route number '{}'".format(number))
        self._number = number
        self._aircraft = aircraft

        rows, seats = self._aircraft.seating_plan()  #((1,23), 'ABCDEF'). rows = (1,23) seats = 'ABCDEF'
        self._seating = [None] + [{letter: None for letter in seats} for _ in rows]  # _ is a dummy variable. we dont require row number. the 1st row is None
    
    def number(self):
        return self._number
    
    def airline(self):
        return self._number[:2]
    
    def aircraft_model(self):
        return self._aircraft.model()  # this model referes to the method in Aircraft
    
    def _parse_seat(self, seat):
        """
        Parse a seat designator into a valid row and letter.
        
        Args:
            seat: A seat designator such as 12F
        Returns:
            A tuple containing an integer and a string for row and seat.
        Usage:
            _parse_seat('12D')
        """
        row_numbers, seat_letters = self._aircraft.seating_plan()  #((1,23), 'ABCDEF'). rows = (1,23) seats = 'ABCDEF'

        letter = seat[-1] # '12D'[-1] = 'D'
        if letter not in seat_letters:
            raise ValueError("Invalid seat letter {}".format(letter))
        
        row_text = seat[:-1]  # '12D'[:-1] = '12'
        try:
            row = int(row_text)
        except ValueError:
            raise ValueError("Invalid seat row {}".format(row_text))
        
        if row not in row_numbers:  # 12 in range(1, 23) = True
            raise ValueError("Invalid row number {}".format(row))
        
        return row, letter
    
    def allocate_seat(self, seat, passenger):
        """
        Allocate a seat to a passenger.
        Args:
        
            seat: A seat designator such as '12C' or '21F'.
            passenger: The passenger's name
        Raises:
            ValueError: If the seat is unavailable.
        Usage:
            allocate_seat('12D', 'Regina Gurung')
        """
        row, letter = self._parse_seat(seat)  # 12, D

        if self._seating[row][letter] is not None:  # _seating = [None, {'A': None, 'B': None, 'C': None, 'D': None, 'E': None, 'F': None},
            raise ValueError("Seat {} already occupied.".format(seat))

        self._seating[row][letter] = passenger  # if no errors are raised, then a seat is assigned to the passenger. _seating[12]['D'] = 'Regina Gurung'
    
    def relocate_passenger(self, from_seat, to_seat):
        """
        Relocate a passenger to a different seat.
        Args:
            from_seat: The existing seat designator for the passenger to be moved.
            to_seat  : The new seat designator
        Usage:
            relocate_passenger('12D', '12F')
        """
        from_row, from_letter = self._parse_seat(from_seat)  # 12, 'D'
        if self._seating[from_row][from_letter] is None:
            raise ValueError("No passenger to relocate in seat {}".format(from_seat))

        to_row, to_letter = self._parse_seat(to_seat)  # 12, 'F'
        if self._seating[to_row][to_letter] is not None:  # seat is not empty.
            raise ValueError("Seat {} already occupied.".format(to_seat))

        self._seating[to_row][to_letter] = self._seating[from_row][from_letter]  # seating[12]['F'] = seating[12]['D']
        self._seating[from_row][from_letter] = None  # The old seat is now empty.
    
    def num_available_seats(self):
        """
        Same as doing:
            sum = 0
            for row in f._seating:
                if row is not None:
                    for s in row.values():
                        if s is None:
                            sum += 1
        """
        return sum(sum(1 for s in row.values() if s is None) for row in self._seating if row is not None)   # 'if row is not None' filters out the first None row.
    
    def make_boarding_cards(self, card_printer):
        """
        f = make_flights()
        f.make_boarding_cards(console_card_printer)
        """
        for passenger, seat in sorted(self._passenger_seats()):
            card_printer(passenger, seat, self.number(), self.aircraft_model)
    
    def _passenger_seats(self):
        """
        An iterable series of passenger seating allocations.
        """
        row_numbers, seat_letters = self._aircraft.seating_plan()  # comes from class Aircraft
        for row in row_numbers:
            for letter in seat_letters:
                passenger = self._seating[row][letter]
                if passenger is not None:
                    yield (passenger, "{}{}".format(row, letter)) 


class Aircraft:
    """
    This is the base class. All methods that are common to both classes, we will keep it here.
    """
    def __init__(self, registration):
        self._registration = registration
    
    def registration(self):
        return self._registration
    
    def num_seats(self):
        """
        Returns total number of seats in the plane.
        """
        rows, row_seats = self.seating_plan()  # this method is not available to this class. This needs to be inherited.
        return len(rows) * len(row_seats)


class AirbusA319(Aircraft):  # We can now use self.seating_plan() in the above code.
    
    def model(self):
        return "Airbus A319"

    def seating_plan(self):
        return range(1,23), "ABCDEF"
    

class Boeing777(Aircraft):
    
    def model(self):
        return "Boeing 777"

    def seating_plan(self):
        return range(1,56), "ABCDEFGHJK"
    

def make_flight():
    #f = Flight('BA758', Aircraft('G-EUPT', 'Airbus A319', num_rows=22, num_seats_per_row=6))
    f = Flight("BA758", AirbusA319("G-EUPT"))
    f.allocate_seat('12A', 'Regina Gurung')
    f.allocate_seat('15F', 'Hitender Gurung')
    f.allocate_seat('15E', 'Sabina Gurung')
    f.allocate_seat('1C', 'Ajay Gurung')
    f.allocate_seat('1D', 'Om Laxmi Gurung')

    g = Flight("AF72", Boeing777("F-GSPS"))
    g.allocate_seat('12A', 'Regina Smyth')
    g.allocate_seat('15F', 'Hitender Smyth')
    g.allocate_seat('15E', 'Sabina Smyth')
    g.allocate_seat('1C', 'Ajay Smyth')
    g.allocate_seat('1D', 'Om Laxmi Smyth')
    
    return f, g

def console_card_printer(passenger, seat, flight_number, aircraft):  # The card printer is polymorphic.
    output = " | Name: {0}"     \
             " | Flight: {1}"   \
             " | Seat: {2}"     \
             " | Aircraft: {3}" \
             " |".format(passenger, flight_number, seat, aircraft)
    banner = "+" + "-" * (len(output) - 2) + "+"
    border = "|" + " " * (len(output) - 2) + "|"
    lines = [banner, border, output, border, banner]
    card = "\n".join(lines)
    print(card)
    print()

"""
Usage:
    f = make_flight()
    f.make_boarding_cards(console_card_printer)

With new flight classes:
    f, g = make_flight()
    f.aircraft_model()
    g.aircraft_model()
    f.num_available_seats()
    g.num_available_seats()
"""
