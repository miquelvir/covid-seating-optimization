from dataclasses import dataclass


@dataclass
class Person:
    family_id: str
    family_member_id: int

    def id_(self):
        return self.family_id, self.family_member_id

    def __eq__(self, other):
        if not isinstance(other, Person):
            return False
        return self.id_ == other.id_
