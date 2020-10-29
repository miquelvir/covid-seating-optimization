from dataclasses import dataclass

from person import Person


@dataclass
class Seat:
    occupant: Person = None
    blocked: bool = False

    def available(self):
        return self.occupant is None and not self.blocked

    def has_occupant(self):
        return self.occupant is not None

    def simple_graphic(self):
        return "-" if self.blocked else "_" if not self.occupant else "x"

    def complete_graphic(self):
        return "**********" if self.blocked else "__________" if not self.occupant else self.occupant.id_()

    def graphic(self, simple=True):
        if simple:
            return self.simple_graphic()
        return self.complete_graphic()

    def __eq__(self, other):
        if not isinstance(other, Seat):
            return False
        return self.occupant == other.occupant