from matplotlib.animation import FuncAnimation
import logging as log

from person import Person
from stadium import Stadium


def follows_covid_guidelines(stadium, x, y, current_family):
    if x - 1 >= 0 and not (not stadium[y][x - 1].has_occupant() or
                           stadium[y][x - 1].occupant.family_id == current_family["id"]):
        log.debug("fails %s at %s %s" % (1,x,y))
        return False
    if x - 2 >= 0 and not (stadium[y][x - 2].occupant is None or
                           stadium[y][x - 2].occupant.family_id == current_family["id"]):
        log.debug("fails %s at %s %s" % (2,x,y))
        return False
    if x + 1 < stadium.columns and not (stadium[y][x + 1].occupant is None or
                           stadium[y][x + 1].occupant.family_id == current_family["id"]):
        log.debug("fails %s at %s %s" % (3,x,y))
        return False
    if x + 2 < stadium.columns and not (stadium[y][x + 2].occupant is None or
                           stadium[y][x + 2].occupant.family_id == current_family["id"]):
        log.debug("fails %s at %s %s" % (4,x,y))
        return False
    if y - 1 >= 0 and not (stadium[y - 1][x].occupant is None or
                           stadium[y - 1][x].occupant.family_id == current_family["id"]):
        log.debug("fails %s at %s %s" % (51,x,y))
        return False
    if y + 1 < len(stadium) and not (stadium[y + 1][x].occupant is None or
                                     stadium[y + 1][x].occupant.family_id == current_family["id"]):
        log.debug("fails %s at %s %s" % (6, x, y))
        return False
    return True


def generate_seating(placing_order, rows, columns):
    def next_seat():
        nonlocal x
        nonlocal y
        nonlocal going_right

        if going_right:
            if x + 1 < stadium.columns:
                x += 1
            elif y + 1 < stadium.rows:
                y += 1
                x = 0  # x = stadium.columns - 1
                # going_right = False
            else:
                return False
        else:
            if x - 1 >= 0:
                x -= 1
            elif y + 1 < stadium.rows:
                y += 1
                x = 0
                going_right = True
            else:
                return False

        return True

    stadium = Stadium(rows, columns)
    y, x = 0, 0
    going_right = True
    for family in placing_order:
        log.debug("placing family %s" % family)
        for member_id in range(family["count"]):
            log.debug(" placing family member %s" % member_id)
            while not follows_covid_guidelines(stadium, x, y, family):
                # advance seat
                if not next_seat():
                    return stadium

            stadium[y][x].occupant = Person(family["id"], member_id)
            if not next_seat():
                return stadium

    return stadium


def compute_seating_cost(state, rows=0, columns=0):
    stadium = generate_seating(state.placing_order, rows=rows, columns=columns)
    return stadium.cost()

