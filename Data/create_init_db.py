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
    tables = []
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
            tables.append([table_name, table_spec])
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
    qu = engine['QUOTE']
    for table_spec in model:
        table_name = table_spec[0]
        script = "{} {}{}{} {}\n".format(engine['DROP_TABLE'], qu, table_name, qu, engine['LINE_TERM']) + script
    for table_spec in model:
        table_name = table_spec[0]
        table = table_spec[1]
        table_script = "{} {}{}{} (".format(engine['CREATE_TABLE'], qu, table_name, qu) +"\n"
        table_script += "\t{}{}{} {} {} {},\n".format(qu, engine['PRIMARY_KEY_NAME'], qu, engine['PRIMARY_KEY_TYPE'], engine['NOT_NULL'], engine['AUTO_INC'])
        for col_desc in table['TYPE_COLS']:
            col_name = col_desc[0]
            not_null = col_desc[1]
            table_script += "\t{}{}{} {}".format(qu, col_name, qu, engine['STRING_TYPE'])
            if not_null:
                table_script += " {}".format(engine['NOT_NULL'])
            table_script += ",\n"
        for fkey in table['FOREIGN_KEYS']:
            ref_table = fkey[0][0]
            not_null = fkey[1]
            if len(fkey[0]) == 2:
                col_name = fkey[0][1]
            elif len(fkey[0]) == 1:
                col_name = "{}_id".format(ref_table[:-1])
            else:
                print("Error in stored representation of foreign key {}.{}\n".format(table,ref_table))
                exit()
            table_script += "\t{0}{1}{0} {2} ".format(qu, col_name, engine['PRIMARY_KEY_TYPE'])
            if not_null:
                table_script += engine['NOT_NULL']
            table_script += ",\n"
            table_script += "\tFOREIGN KEY ({0}{1}{0}) REFERENCES {0}{2}{0}({0}{3}{0}),\n".format(qu, col_name, ref_table, engine['PRIMARY_KEY_NAME'])
        for c in ['created', 'modified']:
            table_script += "\t{0}{1}{0} {2},\n".format(qu, c, engine['DATETIME_TYPE'])
        table_script += "\t{1} ({0}{2}{0}) \n".format(qu, engine['PRIMARY_KEY_DECL'], engine['PRIMARY_KEY_NAME'])
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
