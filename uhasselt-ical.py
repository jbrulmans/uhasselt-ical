#!/bin/env python3.0
import sys
import argparse as ap
from icalendar import Calendar, Event


def main():
    # Set up the parser of the arguments
    parser = init_arg_parser()
    # Parse arguments
    args = parser.parse_args()
    # Try opening the specified input file
    f = open_file(args.input)
    # Parse the file and filter the required events/courses
    data = filter_courses(f, args.courses)
    # Write the data to a new .ics file
    write_calendar(data, args.output)


def filter_courses(f, courses):
    try:
        # Read the calendar provided to the program
        fcal = Calendar.from_ical(f.read())
        # Empty calendar which will be filled with the filtered results
        data = Calendar()
        # Go through all events and compare them to the specified filters
        for component in fcal.walk():
            # Calendar information found, copy this to the new calendar
            if component.name == "VCALENDAR":
                data.add('version', component.get('version'))
                data.add('prodid', component.get('prodid'))
                data.add('method', component.get('method'))
                data.add('calscale', component.get('calscale'))
                data.add('x-wr-calname', component.get('x-wr-calname'))
                data.add('x-wr-timezone', component.get('x-wr-timezone'))
                data.add('x-wr-caldesc', component.get('x-wr-caldesc'))
                data.add('x-published-ttl', component.get('x-published-ttl'))
            # Event found, check if this has to be filtered out
            if component.name == "VEVENT":
                summary = component.get('summary').lower()
                desc = component.get('description').lower()
                for course in courses:
                    if course.lower() in summary or course.lower() in desc:
                        data.add_component(component)
                        break
        return data
    except:
        e = sys.exc_info()[0]
        print('Something went wrong while parsing the .ics file: ', e)


def open_file(path):
    try:
        if not path.lower().endswith('.ics'):
            raise ap.ArgumentTypeError(path)
        f = open(path, "r")
        return f
    except ap.ArgumentTypeError:
        print('The specified file is not an .ics file: ', path)
    except FileNotFoundError:
        print('The specified file does not exist: ', path)
    except IOError:
        print('Cannot read the specified file: ', path)


def write_calendar(data, output):
    try:
        with open(output, 'wb') as f:
            f.write(data.to_ical())
    except IOError:
        e = sys.exc_info()[0]
        print('Something went wrong while trying to write the new calendar file:\n', e)


def init_arg_parser():
    parser = ap.ArgumentParser()
    parser.add_argument('input', metavar='input', type=str, help='input file name (.ics)')
    parser.add_argument('courses', metavar='courses', nargs='+', help='names of courses which have to be filtered out')
    parser.add_argument('-o', '--output', help='output file name', default='output.ics')
    return parser


if __name__ == "__main__":
    main()