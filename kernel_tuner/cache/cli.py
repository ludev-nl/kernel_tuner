
"""
The CLI tool to manipulate kernel tuner cache files. Works with the cache file manipulation library (cache.py), conversion functionality
(convert.py) and other helper functions (defined in cli_fct.py).

Basic usage:
$ cli {convert, t4, delete-line, get-line, merge}

We can:
	  - `convert`: using the functionality from convert.py one can convert to a specified version.
              Within conversion (all required yet nonpositional arguments):
                - `-i/--infile`: the input file to read from.
                - `-T/--target-version`: The version to convert to. 
                - `-o/--output`: The converted output file.

       - `t4`: using the functionality from convert.py one can convert to T4 format.
       		  Within t4 conversion:
       		  	- `-i/--infile`: the input file to read from.
       		  	- `-o/--output`: the t4-converted output file.

       - `delete-line`: using the cache library one can delete from a certain cachefile. 
              We have arguments:
              - <infile>: the input file to delete the entry.
              - (Required) `--key`: The key to try and delete.
              - (Optional): the new output file.

       - `get-line`: using the cache library one can get a certain cacheline entry from the input cachefile. Prints in JSON.
              We have arugments:
              - <infile>: the input file to get the cacheline entry from.
              - (Required) `--key`: The key to check if present in the cachefile. 

	  - `merge`: merge several (>=2) cache files that are of the same jsonschema and have equivalent metadata. Arguments are (all required):
                - <files>: The list of (space separated) input files to read in order to merge the cachefiles.
                - `-o, --output`: The output file to write the merged result to.

      -

Example usages:
$ cli convert --infile 1.json -v 1.1.0 -o 2.json
$ cli delete-line 1.json --key <key> 
$ cli get-line 1.json --key <key>
$ cli merge 1.json 2.json 3.json 4.json -o merged.json
$ cli t4 -i unconverted.json -o converted.json


[*] For now, we run it as a module:
When you are in the main /kernel_tuner directory, start a poetry shell (by running `poetry shell`), and run
`python3.X -m kernel_tuner.cache.cli <options>`
"""

# import required files from within kernel tuner
from .cache import Cache
from .cli_fct import cli_convert, cli_delete, cli_get, cli_merge, cli_t4

import argparse
import sys

def parse_args(args):
	# Setup parsing

	parser = argparse.ArgumentParser(
		prog="cache_cli",
		description="A CLI tool to manipulate kernel tuner cache files.",
		epilog="More help/issues? Visit https://github.com/kernel_tuner/kernel_tuner")

	sp = parser.add_subparsers(required=True, help="Possible subcommands: 'convert', 'delete-line', 'get-line' and 'inspect'.")

	convert = sp.add_parser("convert", help="Convert a cache file from one version to another.")
	convert.add_argument("-i", "--infile", required=True, help="The input cache file to read from.")
	convert.add_argument("-o", "--output", help="The (optional) output JSON file to write to.")
	convert.add_argument("-T", "--target", help="The destination target version. By default the newest version")
	convert.set_defaults(func=cli_convert)

	t4 = sp.add_parser("t4", help="Convert a cache file to the T4 auto-tuning format.")
	t4.add_argument("-i", "--infile", required=True, help="The input cache file to read from.")
	t4.add_argument("-o", "--output", required=True, help="The output JSON file to write to.")
	t4.set_defaults(func=cli_t4)

	delete = sp.add_parser("delete-line", help="Delete a certain cacheline entry from the specified cachefile.")
	delete.add_argument("infile", nargs=1, help="The input file to delete from.")
	delete.add_argument("--key", required=True, help="The (potential) key of the (potential) cacheline entry to delete.")
	delete.add_argument("-o", "--output", help="The (optional) output file to write the updated cachefile to.")
	delete.set_defaults(func=cli_delete)

	get = sp.add_parser("get-line", help="Get a certain cacheline entry from the specified cachefile.")
	get.add_argument("infile", nargs=1, help="The input file to check.")
	get.add_argument("--key", required=True, help="The (potential) key of the (potential) cacheline entry to get.")
	get.set_defaults(func=cli_get)


	merge = sp.add_parser("merge", help="Merge two or more cachefiles.")
	merge.add_argument("files", nargs="+", help="The cachefiles to merge (minimum two). They must be of the same version, and contain equivalent metadata.")
	merge.add_argument("-o", "--output", required=True, help="The output file to write the merged cachefiles to.")
	merge.set_defaults(func=cli_merge)


	# Parse input and call the appropiate function.
	return parser.parse_args(args)


def main():
	"""
	The main function performing the argument parsing and following the user-specified actions
	(one of {convert, delete-line, get-line, merge}); based on this the appropiate function is called.
	"""
	parser = parse_args(sys.argv[1:])

	parser.func(parser)

if __name__ == "__main__":
	main()