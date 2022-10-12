# Creates the `*.gd` files that go in ./goal_src/<game>/dgos
# Takes input from the `dgo.txt` file that is generated by the decompiler
# Run with all inputs enabled to get all the info!

# example - python .\scripts\gsrc\skeleton_creation\generated-dgo-files.py --game jak2 --dgotxt .\decompiler_out\jak2\dgo.txt

import argparse

parser = argparse.ArgumentParser("generate-dgo-files")
parser.add_argument("--game", help="The name of the game", type=str)
parser.add_argument("--dgotxt", help="Path to the dgo.txt file", type=str)
args = parser.parse_args()

# Read in the dgo.txt file
with open(args.dgotxt, "r") as f:
  lines = f.readlines()[2:] # skip the first two lines, assumed to be a comment header and an empty line
  # OpenGOAL still doesn't have a data serialization/deserialization format
  # so read line by line, assuming each DGO is seperated by an empty line
  current_dgo_name = None
  current_dgo_lines = []
  for line in lines:
    if line.strip() == "":
      # Write out contents to the .gd file
      if current_dgo_name is not None:
        path = "./goal_src/{}/dgos/{}".format(args.game, current_dgo_name)
        print("writing to {}".format(path))
        with open(path, "w") as wf:
          wf.writelines(current_dgo_lines)
      current_dgo_name = None
      current_dgo_lines = []
      continue
    if ".CGO" in line or ".DGO" in line:
      print("found one! - {}".format(line.strip()))
      # figure out the name
      current_dgo_name = line.replace("(", "").replace("\"", "").strip().lower().replace(".dgo", ".gd").replace(".cgo", ".gd")
      print(current_dgo_name)
    if current_dgo_name is not None:
      current_dgo_lines.append(line)
