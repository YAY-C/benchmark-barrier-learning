#!/usr/bin/env python3

import sys
import argparse as ap
import chemprop

# to make chemprop work with --proparg_combinat/--proparg_stereo,
# patch ${CONDA_PREFIX}/lib/python3.8/site-packages/chemprop/rdkit.py
# with cgr_proparg_patch.txt


def argparse():
    parser = ap.ArgumentParser()
    g1 = parser.add_mutually_exclusive_group(required=True)
    g1.add_argument('--true', action='store_true', help='use true atom mapping')
    g1.add_argument('--random', action='store_true', help='use random atom mapping')
    g1.add_argument('--rxnmapper', action='store_true', help='use atom mapping from rxnmapper')
    g2 = parser.add_mutually_exclusive_group(required=True)
    g2.add_argument('-c', '--cyclo', action='store_true', help='use Cyclo-23-TS dataset')
    g2.add_argument('-g', '--gdb_full', action='store_true', help='use GDB7-22-TS dataset')
    g2.add_argument('-p', '--proparg', action='store_true', help='use Proparg-21-TS dataset with SMILES from xyz')
    g2.add_argument('--gdb_mod', action='store_true', help='use curated GDB7-22-TS dataset')
    g2.add_argument('--proparg_combinat', action='store_true', help='use Proparg-21-TS dataset with fragment-based SMILES')
    g2.add_argument('--proparg_stereo', action='store_true', help='use Proparg-21-TS dataset with stereochemistry-enriched fragment-based SMILES')
    args = parser.parse_args()
    return parser, args


if __name__ == "__main__":

    parser, args = argparse()
    if args.cyclo:
        data_path = '../../data/cyclo/full_dataset.csv'
        target_columns = 'G_act'
    elif args.gdb_full:
        data_path = '../../data/gdb7-22-ts/ccsdtf12_dz.csv'
        target_columns = 'dE0'
    elif args.gdb_mod:
        data_path = '../../data/gdb7-22-ts/ccsdtf12_dz_mod.csv'
        target_columns = 'dE0'
    elif args.proparg:
        data_path = '../../data/proparg/data.csv'
        target_columns = "Eafw"
    elif args.proparg_combinat:
        data_path = '../../data/proparg/data_fixarom_smiles.csv'
        target_columns = "Eafw"
    elif args.proparg_stereo:
        data_path = '../../data/proparg/data_fixarom_smiles_stereo.csv'
        target_columns = "Eafw"

    if args.random:
        smiles_columns = 'rxn_smiles_random'
    elif args.rxnmapper:
        smiles_columns = 'rxn_smiles_rxnmapper'
    elif args.true:
        if args.proparg or args.proparg_combinat or args.proparg_stereo:
            smiles_columns = 'rxn_smiles_mapped'
        else:
            smiles_columns = 'rxn_smiles'

    arguments = [
        "--data_path", data_path,
        "--dataset_type",  "regression",
        "--target_columns", target_columns,
        "--smiles_columns", smiles_columns,
        "--metric", "mae",
        "--dropout", "0.05",
        "--epochs", "300",
        "--reaction",
        "--num_folds",  "10",
        "--batch_size", "50",
        "--save_dir", "./"]

    args = chemprop.args.TrainArgs().parse_args(arguments)
    mean_score, std_score = chemprop.train.cross_validate(args=args, train_func=chemprop.train.run_training)
    print("Mean score", mean_score, "std_score", std_score)
