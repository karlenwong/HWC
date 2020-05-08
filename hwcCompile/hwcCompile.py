#! /usr/bin/python3

import sys

from parser import parse



def parse_options():
    opts = { "debug"  : None,   # if not None, is the point to stop and dump state
             "infile" : None,   # must be specified on command line
             "outfile": None    # if not specified, will default to infile_name.wire
           }

    while len(sys.argv) > 1:
        if sys.argv[1].startswith("--debug="):
            phase = sys.argv[1][8:]
            sys.argv = sys.argv[:1] + sys.argv[2:]

        elif sys.argv[1][0] == '-':
            print("ERROR: Unrecognized flag: {}".format(sys.argv[1]))
            sys.exit(1)

        else:
            if opts["infile"] is not None:
                print("ERROR: Multiple input filenames detected.")
                sys.exit(1)
            if len(sys.argv) > 2:
                print("ERROR: The input file must be the last argument on the command line.")
                sys.exit(1)
            opts["infile"] = sys.argv[1]

    # TEMPORARY
    opts["infile"] = "/dev/fd/0"
    # TEMPORARY
    opts["outfile"] = "dummy_output_file.wire"

    return opts



if __name__ == "__main__":
    opts = parse_options()


    infile = open(opts["infile"])
    if infile is None:
        print("ERROR: Could not open the infile '{}'".format(opts["infile"]))
        sys.exit(1)

    root_file = parse(infile)
    if root_file is None:
        sys.exit(1)    # the parse function is responsible for printing out error messages
    if opts["debug"] == "parse":
        root_file.dump()
        sys.exit(0)


    for phase in [10,20,30,35,40]:
        if root_file.do_phase(phase) is False:
            TODO
        if opts["debug"] == "semantic_phase{}".format(phase):
            root_file.dump()
            sys.exit()


    TODO    # port this over from the C code below


#	/* look up the name 'main'.  If it doesn't exist, then report an
#	 * error to the user.  If it's not a part, then also report an error.
#	 */
#	HWC_Nameable *thing = nameScope_search(fileScope, "main");
#
#	if (thing == NULL)
#	{
#		fprintf(stderr, "%s: File does not include a type 'main', cannot compile.\n", bisonParse_filename);
#		return 1;
#	}
#	if (thing->part == NULL)
#	{
#		fprintf(stderr, "%s: 'main' is not a part declaration, cannot compile.\n", bisonParse_filename);
#		return 1;
#	}
#
#
#	/* build the wiring diagram! */
#	HWC_Wiring *wiring = buildWiringDiagram(thing->part);
#	if (wiring == NULL)
#		return 1;   // the wiring generator must have already printed an error message
#
#
#	if (outfile == NULL)
#	{
#		fprintf(stderr, "ERROR: No outfile specified.  Please use -o <file>.\n");
#		fprintf(stderr, "TODO: make this automatic, based on the infile name.\n");
#		return 1;
#	}
#
#
#	FILE *out = fopen(outfile, "w");
#	int rc = wiring_write(wiring, out);
#	fclose(out);
#	return rc;


