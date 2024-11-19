from rich.console import Console
from rich.table import Table
from random import choice
from rich import color
import inquirer
import os


def show_table(title, columns, rows, rows_to_display=10):
    table = Table(title=title)  
    for header in columns:
        table.add_column(header, justify="left", style=choice(list(color.ANSI_COLOR_NAMES.keys())), no_wrap=True)  
    for row in rows[:rows_to_display]:
        table.add_row(row)
    console = Console()
    console.print(table)


def get_cardinality(list_to_check):
    counts = dict()
    for item in list_to_check:
        if item in counts:
            counts[item] += 1
        else:
            counts[item] = 1
    return counts


def create_one_hot_columns(column, cardinality):
    new_column = []
    indexing = {}
    counter = 0
    for item in cardinality:
        indexing[item] = counter
        counter += 1
    for data in column:
        new_column.append(indexing[data])
    return new_column


def create_float_column(column):
    return [float(c) for c in column]


def create_int_column(column):
    return [int(c) for c in column]


def fill_nulls(column, value):
    t = type(value)
    new_column = []
    for d in column:
        if len(d) > 0:
            new_column.append(t(d))
        else:
            value
    return new_column


def analyze(folder="."):
    print("This module analyzes a CSV wit headers with the intent of preparing it for data science.")
    filename = inquirer.list_input("What file do you want to explore?", choices=[f for f in os.listdir(folder) if f[-3:] == 'csv'])
    print("--------------")
    lines = open(filename, "r").read().split("\n")
    headers = lines.pop(0).split(",")
    lines = [line.split(",") for line in lines]
    total_lines = len(lines)
    lines.pop()
    data_types = ["throw away", "float()", "int()", "one-hot encode", "ask again later", "fill nulls", "clean"]
    column_transforms = []
    for header_index in range(len(headers)):
        values = [line[header_index] for line in lines]
        show_table("Column number " + str(header_index) + " of " + str(len(headers)) + ", Named: [bold]" + headers[header_index], [headers[header_index]], values, 15)
        cardinality = get_cardinality(values)
        print(headers[header_index], "with cardinality", len(cardinality.keys()))
        answers = ["All", "Top # only", "Bottom # only", "None, skip"]
        to_print = inquirer.list_input("How much of the cardinality do you want to print?", choices=answers)
        if to_print == answers[3]:
            pass
        else:
            if to_print == answers[0]:
                amount = len(cardinality)
            else:
                amount = int(inquirer.text("How much of the cardinality would you like to print? (from 0 to " + str(len(cardinality)) + ")"))
            cardinality_as_list = [[cardinality[k], k] for k in cardinality.keys()]
            cardinality_as_list.sort()
            if to_print != answers[2]:
                cardinality_as_list.reverse()
            for item in cardinality_as_list[:amount]:
                print(item[1], "appears", item[0], "times")
        column_transforms.append(inquirer.list_input("What kind of data is this?", choices=data_types))
    for index in range(len(headers)):
        print(column_transforms[index], headers[index])
    

if __name__ == "__main__":
    analyze()
