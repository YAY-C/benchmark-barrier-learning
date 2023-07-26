import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd

def get_maes(npy, txt=False, csv=False):
    if txt:
        maes = np.loadtxt(npy)
    elif csv:
        df = pd.read_csv(npy)
        return df['Mean mae'].to_numpy()[0], df['Standard deviation mae'].to_numpy()[0]
    else:
        maes = np.load(npy)
    return np.mean(maes), np.std(maes)

def round_with_std(mae, std):
    # works only is std < 1
    std_1digit = int(std // 10**np.floor(np.log10(std)))
    std_1digit_pos = f'{std:.10f}'.split('.')[1].index(str(std_1digit))
    if std_1digit > 2:
        std_round = f'{std:.{std_1digit_pos+1}f}'
    else:
        std_round = f'{std:.{std_1digit_pos+2}f}'
    n_after_point = len(std_round.split('.')[1])
    mae_round = f'{mae:.{n_after_point}f}'
    return mae_round + '$\pm$' + std_round

matplotlib.rcParams.update({"font.size":12})
colors = ["#FF0000", "#B51F1F", "#00A79F", "#007480", "#413D3A", "#CAC7C7"]


cyclo_dir = 'data/cyclo/'
gdb_dir = 'data/gdb7-22-ts/'
proparg_dir = 'data/proparg/'

cyclo_lang_dir = 'outs/cyclo_bert_pretrained/5_epochs_8_batches_10_smiles_rand/results.txt'
gdb_lang_dir = 'outs/gdb_bert_pretrained/5_epochs_8_batches_10_smiles_rand/results.txt'
proparg_lang_dir = 'outs/proparg_bert_pretrained/5_epochs_8_batches_0_smiles_rand/results.txt'
lang_dirs = [gdb_lang_dir, cyclo_lang_dir, proparg_lang_dir]

cyclo_cgr_dir = 'results/cyclo_true/test_scores.csv'
gdb_cgr_dir = 'results/gdb_true/test_scores.csv'
proparg_cgr_dir = 'results/proparg_true/test_scores.csv'
cgr_dirs = [gdb_cgr_dir, cyclo_cgr_dir, proparg_cgr_dir]

titles = ['(a) GDB7-22-TS', '(b) Cyclo-23-TS', '(c) Proparg-21-TS']
fig, axes = plt.subplots(nrows=1, ncols=3)

axes[0].set_ylim(0,22)
axes[1].set_ylim(0,8)
axes[2].set_ylim(0,2.4)
for i, db in enumerate([gdb_dir, cyclo_dir, proparg_dir]):

    if i == 0:
        add = 0.5
    elif i == 1:
        add = 0.25
    elif i == 2:
        add = 0.15

    lang_dir = lang_dirs[i]
    cgr_dir = cgr_dirs[i]
    mfp_mae, mfp_std = get_maes(db + 'mfp_10_fold.npy')
    drfp_mae, drfp_std = get_maes(db + 'drfp_10_fold.npy')
    slatm_mae, slatm_std = get_maes(db + 'slatm_10_fold.npy')
    b2r2_mae, b2r2_std = get_maes(db + 'b2r2_l_10_fold.npy')
  #  spahm_mae, spahm_std = get_maes(db + 'spahm_10_fold.npy')

    rxnfp_mae, rxnfp_std = get_maes(lang_dir, txt=True)
    cgr_mae, cgr_std = get_maes(cgr_dir, csv=True)

    axes[i].set_title(titles[i], fontsize='medium')
    axes[i].bar(0, mfp_mae, yerr=mfp_std, color=colors[0])
    axes[i].text(0 - 0.26, mfp_mae + add, round_with_std(mfp_mae, mfp_std), rotation=90, fontsize='x-small', fontweight='bold')
    axes[i].bar(1, drfp_mae, yerr=drfp_std, color=colors[1])
    axes[i].text(1 - 0.26, drfp_mae + add, round_with_std(drfp_mae, drfp_std), rotation=90, fontsize='x-small', fontweight='bold')

    axes[i].bar(2, rxnfp_mae, yerr=rxnfp_std, color=colors[4])
    axes[i].text(2 - 0.26, rxnfp_mae + add, round_with_std(rxnfp_mae, rxnfp_std), rotation=90, fontsize='x-small', fontweight='bold')

    axes[i].bar(3, slatm_mae, yerr=slatm_std, color=colors[2])
    axes[i].text(3 - 0.26, slatm_mae + add, round_with_std(slatm_mae, slatm_std), rotation=90, fontsize='x-small', fontweight='bold')

    axes[i].bar(4, b2r2_mae, yerr=b2r2_std, color=colors[3])
    axes[i].text(4 - 0.26, b2r2_mae + add, round_with_std(b2r2_mae, b2r2_std), rotation=90, fontsize='x-small', fontweight='bold')

    #axes[i].bar(5, spahm_mae, yerr=spahm_std, color=colors[4])

    axes[i].bar(5, cgr_mae, yerr=cgr_std, color=colors[5])
    axes[i].text(5 - 0.26, cgr_mae + add, round_with_std(cgr_mae, cgr_std), rotation=90, fontsize='x-small', fontweight='bold')

    axes[i].set_xticks(list(range(6)))
    axes[i].set_xticklabels(['MFP', 'DRFP', 'BERT+RXNFP', 'SLATM$_d$', '$B^2R^2_l$', 'CGR'], rotation=90)

axes[0].set_ylabel("MAE $\Delta E^\ddag$ [kcal/mol]")
axes[1].set_ylabel("MAE $\Delta G^\ddag$ [kcal/mol]")
axes[2].set_ylabel("MAE $\Delta E^\ddag$ [kcal/mol]")

plt.tight_layout()
plt.savefig('figures/compare_all_models.pdf')
#plt.show()
