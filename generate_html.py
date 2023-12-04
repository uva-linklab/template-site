#!/usr/bin/env python3

import os
import pathlib

OUTDIR = "out/"

substitutions = {}

# Make sure the OUTDIR exists.
pathlib.Path(OUTDIR).mkdir(parents=True, exist_ok=True)


htmlfiles = []
htmlfiles.extend(pathlib.Path(".").glob("*.html"))
htmlfiles.extend(pathlib.Path("participants/").glob("*.html"))
htmlfiles.extend(pathlib.Path("photos/").glob("*.html"))
htmfiles_gen = pathlib.Path(".").glob("htm/*.htm")
htmfiles = pathlib.Path(".").glob("*.htm")

for htm in htmfiles_gen:
    with open(htm) as f:
        contents = f.read()
        substitutions[str(htm)[4:]] = contents

for htm in htmfiles:
    with open(htm) as f:
        contents = f.read()
        substitutions[str(htm)] = contents


for html in htmlfiles:
    print("Updating {}...".format(html))
    count = 0

    html_file = ""
    with open(html) as f:
        html_file = f.read()

    # Determine the directory depth for the base.
    dirdepth = str(html).count("/")
    base = "./"
    if dirdepth == 1:
        base = "../"

    for name, contents in substitutions.items():
        if name == "head.htm":
            contents = contents.replace(
                "<!-- base -->", '<base href="{}" />'.format(base)
            )

        start = "<!-- {} -->".format(name)

        print("  Looking for {}...".format(start), end="")

        sindex = html_file.find(start)

        if sindex > -1:
            print("found")
            sindex = html_file.find("\n", sindex)

            # Do any needed replacements to the substitution.
            subname = "<!-- {}".format(html)
            mindex = contents.find(subname)
            if mindex > -1:
                meindex = contents.find("-->", mindex)
                replacement = contents[mindex + len(subname) + 1 : meindex - 1]
                contents = contents[0:mindex] + replacement + contents[meindex + 3 :]

            # Remove all comments
            while True:
                cindex = contents.find("<!--")
                if cindex > -1:
                    ceindex = contents.find("-->")
                    contents = contents[0:cindex] + contents[ceindex + 3 :]
                else:
                    break

            out = html_file[0 : sindex + 1]
            out += contents
            out += html_file[sindex + 1 :]
            html_file = out

            count += 1
        else:
            print("")

    # Update file if there is a swap
    if count > 0:
        with open(os.path.join(OUTDIR, html), "w") as f:
            f.write(html_file)
