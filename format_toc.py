#!/usr/bin/env python
from __future__ import print_function
import re
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

header_rx = re.compile(r'^(#+) *(.+?) *(\1) *\n?$')
non_alpha_rx = re.compile(r'[^a-z0-9.]+')
def parse_header(line):
    m = header_rx.match(line)
    if not m: return None
    depth = len(m.group(1))
    title = m.group(2)
    anchor = non_alpha_rx.sub('-', title.lower())
    return depth, title, anchor

with open("toc.md", "wt") as outfile:
    for line in toc:
        header = parse_header(line)
        if header is not None:
            depth, title, anchor = header
            outfile.write("%s* [%s](#%s)\n" % ("    "*(depth-1), title, anchor))
    outfile.write("\n\n\n")
    # Print out all lines in the template, replacing `;sections` with lists of recipes.
    for line in toc:
        header = parse_header(line)
        if header is not None:
            depth, title, anchor = header
            outfile.write("<a name='%s'></a>\n" % anchor)
        if not line.startswith(";"):
            outfile.write(line)
            continue
        section = line[1:].strip()
        for recipe in sorted(recipes[section]):
            outfile.write("* %s\n" % recipe)

# pandoc -f markdown_github -t html --ascii -o toc.html toc.md
