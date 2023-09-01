import os
import sys
import shutil
import argparse
file_dir = os.path.abspath(os.path.dirname(__file__))
packagedir = os.path.dirname(file_dir)
sys.path.append(packagedir)
from md_setup.gmx import GMX_param

parser = argparse.ArgumentParser()
parser.add_argument('structure_filepath', metavar='structure_filepath', type=str, help="path to .pdb file a protein complex w/o water ")
parser.add_argument('-o', '--output', metavar='output', type=str, default=os.getcwd(), help="path to directory where to save the files.")
args = parser.parse_args()

host_dir = args.output
os.makedirs(host_dir, exist_ok=True)

# specify your input pdb
pdb = args.structure_filepath

# ff_dir = f'{packagedir}/forcefields/amber99sb-ildn.ff' # Produces this error: openmm.OpenMMException: PeriodicTorsionForce: periodicity must be positive
ff_dir = f'{packagedir}/forcefields/charmm36-feb2021.ff'
mdp_file = f'{packagedir}/forcefields/ions.mdp'

# label for ligand identity
pdb_code = os.path.basename(pdb)[:-4]

# make a work dir
work_dir = os.path.abspath(os.path.join(host_dir, 'input_' + pdb_code))
os.makedirs(work_dir, exist_ok=True)

# make a copy of pdb and ff
pdb_copy = os.path.join(work_dir, os.path.basename(pdb))
mdp_copy = os.path.join(work_dir, os.path.basename(mdp_file))
ff_copy = os.path.join(work_dir, os.path.basename(ff_dir))
shutil.copy2(pdb, pdb_copy)
shutil.copy2(mdp_file, mdp_copy)
shutil.copytree(ff_dir, ff_copy)

# run the parameterization
os.chdir(work_dir)
charmmP = GMX_param(pdb_copy, box_padding=1.0)
os.chdir(host_dir)
