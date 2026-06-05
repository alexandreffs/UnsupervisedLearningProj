"""Add plt.savefig and .to_csv calls to report-relevant cells."""
import json, os

with open('project.ipynb', encoding='utf-8') as f:
    nb = json.load(f)

def append_to_cell(idx, code):
    src = ''.join(nb['cells'][idx]['source'])
    if code.strip().split('\n')[1] not in src:   # skip if already patched
        nb['cells'][idx]['source'] = src + '\n' + code
        return True
    return False

MKDIR_FIG = "os.makedirs('figures', exist_ok=True)\n"
MKDIR_TBL = "os.makedirs('tables', exist_ok=True)\n"

patches = [
    # (cell_idx, code_to_append, description)

    # ── Figures ───────────────────────────────────────────────────────────────
    # Cell 48: dendrogram
    (48,
     MKDIR_FIG + "plt.savefig('figures/fig_dendrogram.png', bbox_inches='tight', dpi=150)\n",
     "figures/fig_dendrogram.png"),

    # Cell 51: metrics comparison bar chart (silhouette/CH/DB across models)
    (51,
     MKDIR_FIG + "plt.savefig('figures/fig_metrics_comparison.png', bbox_inches='tight', dpi=150)\n",
     "figures/fig_metrics_comparison.png"),

    # Cell 60: cluster profile bar chart
    (60,
     MKDIR_FIG + "plt.savefig('figures/fig_cluster_profiles.png', bbox_inches='tight', dpi=150)\n",
     "figures/fig_cluster_profiles.png"),

    # Cell 62: E4 scree plot + loadings heatmap
    (62,
     MKDIR_FIG + "plt.savefig('figures/fig_e4_scree_loadings.png', bbox_inches='tight', dpi=150)\n",
     "figures/fig_e4_scree_loadings.png"),

    # Cell 63: E4 PCA-2 scatter
    (63,
     MKDIR_FIG + "plt.savefig('figures/fig_e4_pca2_scatter.png', bbox_inches='tight', dpi=150)\n",
     "figures/fig_e4_pca2_scatter.png"),

    # Cell 66: E1 anomaly score distribution + z-score fingerprint
    (66,
     MKDIR_FIG + "plt.savefig('figures/fig_e1_anomaly.png', bbox_inches='tight', dpi=150)\n",
     "figures/fig_e1_anomaly.png"),

    # ── Tables ────────────────────────────────────────────────────────────────
    # Cell 51: all model results
    (51,
     MKDIR_TBL + "results_all.to_csv('tables/results_all_models.csv', index=False)\n",
     "tables/results_all_models.csv"),

    # Cell 53: K-Means stability
    (53,
     MKDIR_TBL + "stability_df.to_csv('tables/stability_kmeans.csv', index=False)\n",
     "tables/stability_kmeans.csv"),

    # Cell 56: scaler sensitivity
    (56,
     MKDIR_TBL + "sens_df.to_csv('tables/sensitivity_scaler.csv', index=False)\n",
     "tables/sensitivity_scaler.csv"),

    # Cell 63: E4 PCA comparison
    (63,
     MKDIR_TBL + "e4_df.to_csv('tables/e4_pca_comparison.csv', index=False)\n",
     "tables/e4_pca_comparison.csv"),

    # Cell 65: E1 top-20 anomalies
    (65,
     MKDIR_TBL + "anom_df.to_csv('tables/e1_top20_anomalies.csv', index=False)\n",
     "tables/e1_top20_anomalies.csv"),
]

done = 0
for idx, code, desc in patches:
    if idx >= len(nb['cells']):
        print(f"  SKIP cell {idx} (out of range)")
        continue
    if append_to_cell(idx, code):
        print(f"  + cell {idx} → {desc}")
        done += 1
    else:
        print(f"  ~ cell {idx} already patched ({desc})")

with open('project.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"\nDone — {done} cells patched.")
