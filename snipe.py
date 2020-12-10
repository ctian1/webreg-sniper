from PyWebReg.WebReg import WebReg
import sys,os

### CONFIG

TO_DROP = ['34320', '34324']
TARGET = '34250'
LABS = '34251'

UCI_ID = "user"
UCI_PW = "password"

CHROMEDRIVER = "/absolute/path/to/chromedriver"

###


wr = WebReg(CHROMEDRIVER, headless=False).login(UCI_ID, UCI_PW)

def shutdown():
    wr._show_study_list()
    print(wr.get_study_list())
    wr.logout()
    sys.exit()


def drop_courses(courses):
    dropped = []
    for course in courses:
        res = wr.drop_course(course)
        if res == -1:
            print(f"Couldn't drop course {course}")
        else:
            dropped.append(course)
    return dropped

def add_courses(courses):
    added = []
    for course in courses:
        res = wr.add_course(course)
        if res == -1:
            print(f"Couldn't add course {course}")
        else:
            added.append(course)
    return added

open_target = wr.list_open_sections(TARGET)
if not open_target:
    print("Spot not found")
else:
    open_labs = wr.list_open_sections(LABS)
    if not open_labs:
        print("Spot not found")
    else:
        # both open
        print("Found spots:")
        print(open_target)
        print(open_labs)

        print()

        print(f"Dropping {TO_DROP}")

        res_drop = drop_courses(TO_DROP)
        if res_drop != TO_DROP:
            print(f"Failed to drop, cleaning up")
            add_courses(res_drop)
            shutdown()

        to_add = [open_target[0][0], open_labs[0][0]]

        print(f"Adding {to_add}")

        res_add = add_courses(to_add)

        if res_add != to_add:
            print(f"Failed to add, cleaning up")
            drop_courses(res_add)
            add_courses(TO_DROP)
            shutdown()

        print("Success!")

        shutdown()