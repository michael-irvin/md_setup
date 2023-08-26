import string
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('structure_filepath', metavar='structure_filepath', type=str, help="path to .pdb file a protein complex w/o water ")
args = parser.parse_args()

filepath = args.structure_filepath
outpath = f"{os.path.splitext(filepath)[0]}_chain{os.path.splitext(filepath)[1]}"

f = open(filepath, 'r')
out = open(outpath, 'w')

chain_ids = list(string.ascii_uppercase + "0123456789"+ string.ascii_lowercase)

current_chain = chain_ids.pop(0)
for line in f:
    if line.startswith('END'):
        out.write(line)
    else:
        line = list(line)
        line[21] = current_chain
        line = ''.join(line)
        if line.startswith('TER'):
            current_chain = chain_ids.pop(0)
        out.write(line)

f.close()
out.close()

