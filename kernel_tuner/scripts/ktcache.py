"""The CLI tool to manipulate kernel tuner cache files.

Works with the cache file manipulation library (cache.py),
conversion functionality (convert.py) and other helper functions (defined in cli_functionality.py).

Basic usage:
$ ktcache {convert, t4, delete-line, get-line, merge}

We can:
   - `convert`: using the functionality from convert.py one can convert to a specified version.
      Within conversion (all required yet nonpositional arguments):
         - `-i/--infile`: the input file to read from.
         - `-T/--target`: The version to convert to. 
         - `--out/--output`: The converted output file.
         - `--force-version-absence`: allow unversioned cachefiles to be converted.


   - `t4`: using the functionality from convert.py one can convert to T4 format.
      Within t4 conversion:
         - `-i/--infile`: the input file to read from.
         - `-o/--output`: the t4-converted output file.

   - `delete-line`: using the cache library one can delete from a certain cachefile; only works with the latest 
      schema_version. 
      We have arguments:
         - <infile>: the input file to delete the entry.
         - `--key`: The key to try and delete.
         - ``: the new output file.

   - `get-line`: using the cache library one can get a certain cacheline entry from the input cachefile. 
      Prints in JSON.
      We have arugments:
         - <infile>: the input file to get the cacheline entry from.
         - (Required) `--key`: The key to check if present in the cachefile. 

   - `merge`: merge several (>=2) cache files that are of the same jsonschema and have equivalent metadata, to the 
      latest schema_version.
      Arguments are (all required):
         - <files>: The list of (space separated) input files to read in order to merge the cachefiles.
         - `-o, --output`: The output file to write the merged result to.


"""

# import required files from within kernel tuner
import argparse
import sys

from kernel_tuner.cache.cli_tools import convert, convert_t4, delete_line, get_line, merge


def cli_convert(ap_res: argparse.Namespace):
    """The main function for handling conversion to a `schema_version` in the cli."""
    convert(ap_res.infile, write_file=ap_res.output, target=ap_res.target, \
            allow_version_absence=ap_res.allow_version_absence)


def cli_delete_line(ap_res: argparse.Namespace):
    """The main function for handling deletion of a cacheline using `delete-line` in the cli."""
    delete_line(ap_res.infile[0], ap_res.key, outfile=ap_res.output)


def cli_getline(ap_res: argparse.Namespace):
    """The main function for getting a line using `get-line` in the cli."""
    get_line(ap_res.infile[0], ap_res.key)
    

def cli_merge(ap_res: argparse.Namespace):
    """The main function for merging several cachefiles using `merge` in the cli."""
    merge(ap_res.files, ap_res.output)


def cli_t4(ap_res: argparse.Namespace):
    """The main function for handling conversion to t4 format in the cli."""
    convert_t4(ap_res.infile, write_file=ap_res.output)


def parse_args(args):
    """The main parsing function.

    Uses argparse to parse, then calls the appropiate function, one of:
    cli_{convert, delete-line, get-line, merge}.
    """
	# Setup parsing

    parser = argparse.ArgumentParser(
		prog="ktcache",
		description="A CLI tool to manipulate kernel tuner cache files.",
		epilog="Example usages:\n\n" \
        "ktcache convert --in a.json -T 1.1.0 --out b.json\n" \
        "ktcache convert --in a.json -T 1.1.0 --out b.json --allow-version-absence\n" \
        "ktcache delete-line 1.json --key 1,2,3,4 --out 2.json\n" \
        "ktcache get-line file.json --key 1,2,3,4\n" \
        "ktcache t4 --in x.json --out y.json\n" \
        "ktcache merge 1.json 2.json 3.json --out 4.json\n\n",
        formatter_class=argparse.RawDescriptionHelpFormatter)

    sp = parser.add_subparsers(required=True,
                               help="Possible subcommands: 'convert', 'delete-line', 'get-line' and 'inspect'.")
    

    convert = sp.add_parser("convert", help="Convert a cache file from one version to another.")
    convert.add_argument("--in", "--infile", 
                    required=True, 
                    help="The input cache file to read from.", 
                    dest="infile")
    convert.add_argument("--out", "--output", 
                    help="The (optional) output JSON file to write to.", 
                    dest="output")
    convert.add_argument("-T", "--target", 
                    help="The destination target version. By default the newest version")
    convert.add_argument("--allow-version-absence", dest="allow_version_absence", action="store_true",
                    help="Allow unversioned cachefiles to be converted.")
    convert.set_defaults(func=cli_convert)

    t4 = sp.add_parser("t4", help="Convert a cache file to the T4 auto-tuning format.")
    t4.add_argument("--in", "--infile", 
                    required=True, 
                    help="The input cache file to read from.", 
                    dest="infile")
    t4.add_argument("--out", "--output", 
                    required=True, 
                    help="The output JSON file to write to.", 
                    dest="output")
    t4.set_defaults(func=cli_t4)
    
    delete = sp.add_parser("delete-line", help="Delete a certain cacheline entry from the specified cachefile.")
    delete.add_argument("infile", 
                    nargs=1, 
                    help="The input file to delete from.")
    delete.add_argument("--key", 
                    required=True,
                    help="The (potential) key of the (potential) cacheline entry to delete.")
    delete.add_argument("-o", "--out", "--output", 
                    help="The (optional) output file to write the updated cachefile to.", 
                    dest="output")
    delete.set_defaults(func=cli_delete_line)
    
    get = sp.add_parser("get-line", help="Get a certain cacheline entry from the specified cachefile.")
    get.add_argument("infile", 
                    nargs=1, 
                    help="The input file to check.")
    get.add_argument("--key", 
                    required=True, 
                    help="The (potential) key of the (potential) cacheline entry to get.")
    get.set_defaults(func=cli_getline)
    
    merge = sp.add_parser("merge", help="Merge two or more cachefiles.")
    merge.add_argument("files", 
                    nargs="+",
					help="The cachefiles to merge (minimum two). They must be of the same version, and " \
                         "contain equivalent metadata.")
    merge.add_argument("-o", "--out", "--output", 
                    required=True,
					help="The output file to write the merged cachefiles to.", 
                    dest="output")
    merge.set_defaults(func=cli_merge)
    

    # Parse input and call the appropiate function.
    return parser.parse_args(args)


def main():
    """The function called when running the cli. This function calls the main parsing function.
    
    This is one of {convert, delete-line, get-line, merge, t4},
    based on this the appropiate function cli_{convert, delete-line, get-line, merge, t4} is called.
    """
    parser = parse_args(sys.argv[1:])

    parser.func(parser)

if __name__ == "__main__":
	main()
