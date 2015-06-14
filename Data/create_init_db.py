#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Creates the sql script to initialize the database
# Reads the db.spec for the data model,
# and the engine.spec for the database specifics

import sys
import decimal
import statistics
import re

# Reads the database model
# Currently db.spec
def read_model(name):
    tables = dict()
    with open(name, 'r') as file:
        for line in file:
            parts = line.split(':')
            if len(parts) != 2:
                print("Wrong number of colons (:)s, should only be 1 on line {}".format(line))
                exit()
            table_name = parts[0]
            cols = parts[1].split(',')
            table_spec = dict()
            table_spec['TYPE_COLS'] = []
            table_spec['FOREIGN_KEYS'] = []
            for col in cols:
                if col[-1] == '0':
                    not_null = False
                    words = col[:-2].split()
                else:
                    not_null = True
                    words = col.split()
                if words[0] == "FOREIGN_KEY":
                    if len(words) == 2:
                        key_spec = [words[1]]
                    elif len(words) == 3:
                        key_spec = [words[1], words[2]]
                    else:
                        print("Error with foreign key {}".format(col))
                        exit()
                    table_spec['FOREIGN_KEYS'].append([key_spec,not_null])
                else:
                    type = words[0]
                    table_spec['TYPE_COLS'].append([words[1],not_null,words[0]])
            tables[table_name] = table_spec
    return tables
                

# Reads specification of translation
# into database-engine specifics
# Currently only mysql
def read_engine(name):
    specs = dict()
    with open(name, 'r') as file:
        line_no = 0
        for line in file:
            line_no += 1
            if len(line) > 0:
                parts = line.split(':')
                if len(parts) != 2:
                    print("Wrong number of colons (:)s, should only be 1 on line nr {} : of file {}: {}".format(line_no, name, line))
                    exit()
                specs[parts[0]] = parts[1][:-1]
    return specs

# Creates the init script as a string
def create_script(model, engine):
    script = ""
    for table in model.keys():
        table_script = "{} {} {}\n".format(engine['DROP_TABLE'], table, engine['LINE_TERM'])
        table_script += "{} {} (".format(engine['CREATE_TABLE'], table) +"\n"
        for col_desc in model[table]['TYPE_COLS']:
            col_name = col_desc[0]
            not_null = col_desc[1]
            table_script += "\t{} {}".format(col_name, engine['STRING_TYPE'])
            if not_null:
                table_script += " {} ".format(engine['NOT_NULL'])
            table_script += ",\n"
        table_script += "\t{} {},\n".format(engine['PRIMARY_KEY_NAME'], engine['PRIMARY_KEY_TYPE'])
        table_script += "\t{} \n".format(engine['PRIMARY_KEY_DECL'])
        table_script += ")" + engine['TABLE_SUFFIX'] + engine['LINE_TERM'] + "\n"
        script += table_script + "\n"
    return script


def main():
    if len(sys.argv) <= 2:
        print("Usage: {} db.spec mysql.spec".format(sys.argv[0]))
    model = read_model(sys.argv[1])
    engine = read_engine(sys.argv[2])
    init_script = create_script(model, engine)
    print(init_script)

main()
