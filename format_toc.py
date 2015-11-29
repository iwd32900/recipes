#!/usr/bin/env python
from __future__ import print_function
from collections import defaultdict

# Read the table of contents template
toc = list(open("toc_template.md", "rt"))

# Read the list of recipes and sort into categories/sections
recipes = defaultdict(list)
for linenum0, line in enumerate(open("recipes.txt", "rt")):
    fields = [f.strip() for f in line.split(";")]
    if not fields:
        continue
    if len(fields) < 2:
        print("Line %i: no categories assigned" % linenum0+1)
        continue
    recipe = fields[0]
    for category in fields[1:]:
        recipes[category].append(recipe)

# Compare sections used in the TOC to sections used by recipes
used_sections = set(recipes)
toc_sections = set(line[1:].strip() for line in toc if line.startswith(";"))

if toc_sections - used_sections:
    print("Sections with no recipes:")
    for section in toc_sections - used_sections:
        print("    %s" % section)

if used_sections - toc_sections:
    print("Sections not used in the table of contents:")
    for section in used_sections - toc_sections:
        print("    %s" % section)

with open("toc.md", "wt") as outfile:
    for line in toc:
        if not line.startswith(";"):
            outfile.write(line)
            continue
        section = line[1:].strip()
        for recipe in sorted(recipes[section]):
            outfile.write("* %s\n" % recipe)
