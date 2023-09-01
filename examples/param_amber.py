import os
import sys
import shutil
import argparse
file_dir = os.path.abspath(os.path.dirname(__file__))
packagedir = os.path.dirname(file_dir)
sys.path.append(packagedir)
from md_setup.param import AMBER_param

parser = argparse.ArgumentParser()
parser.add_argument('structure_filepath', metavar='structure_filepath', type=str, help="path to .pdb file a protein complex w/o water ")
parser.add_argument('-o', '--output', metavar='output', type=str, default=os.getcwd(), help="path to directory where to save the files.")
args = parser.parse_args()

host_dir = args.output
# specify your input pdbs
pdb = args.structure_filepath # 'VPAVGx30_20230829_3_3_3_6.0nm_chain.pdb'

# getting parameter for protein-ligand complexes
info_list = []

# label for ligand identity
pdb_code = os.path.basename(pdb)[:-4]

# make the work dir
work_dir = os.path.abspath(os.path.join(host_dir, 'input_' + pdb_code))
os.makedirs(work_dir, exist_ok=True)

# make a copy of pdb in the new dir
pdb_copy = os.path.join(work_dir, os.path.basename(pdb))
shutil.copy2(pdb, pdb_copy)

# run and get the parameters
os.chdir(work_dir)
amberP = AMBER_param(pdb_copy, forcefield='ff99SB-old', watermodel='opc')
amberP.param_comp()
os.chdir(host_dir)


