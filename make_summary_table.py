import os
from collections import Counter

RESULTS_DIR = "/home/tomi/data/phyparts/GeneExtraction/AnnotationResults"
OUTFILE = "/home/tomi/data/phyparts/GeneExtraction/AnnotationResults/summary_top_genes_per_node.tsv"

node_descriptions = {
    "phyparts_dup.dupl.5":  "SAS7/ZAPE2/SEHU2/SEPO2/SEVE2 clade",
    "phyparts_dup.dupl.6":  "ZAPE2/SEHU2/SEPO2/SEVE2 clade",
    "phyparts_dup.dupl.7":  "SEHU2/SEPO2/SEVE2 clade",
    "phyparts_dup.dupl.8":  "SEPO2/SEVE2 clade",
    "phyparts_dup.dupl.9":  "Core Ruschioideae + SAS13/MECR2",
    "phyparts_dup.dupl.10": "SAS13/MECR2",
    "phyparts_dup.dupl.11": "Core Ruschioideae",
    "phyparts_dup.dupl.12": "Ruschioideae subgroup",
    "phyparts_dup.dupl.15": "DEEC/SAS10/SAS8 clade",
    "phyparts_dup.dupl.26": "SAS28/SAS23/SAS5 clade",
    "phyparts_dup.dupl.36": "SAS18/SAS2 clade",
}

with open(OUTFILE, "w") as out:
    out.write("node\tnode_description\ttotal_entries\ttotal_annotated\trank\tgene_name\tcount\n")

    for annot_file in sorted(os.listdir(RESULTS_DIR)):
        # Skip master file and non per-node files
        if annot_file == "all_nodes_annotations.tsv":
            continue
        if not annot_file.endswith("_annotations.tsv"):
            continue

        node = annot_file.replace("_annotations.tsv", "")
        
        # Skip if not a recognized node
        if node not in node_descriptions:
            continue
            
        filepath = os.path.join(RESULTS_DIR, annot_file)
        description = node_descriptions[node]

        gene_names = []
        total_entries = 0

        with open(filepath) as f:
            next(f)  # skip header
            for line in f:
                parts = line.strip().split("\t")
                if len(parts) >= 5:
                    gene_name = parts[4]
                    if gene_name and gene_name != "Unknown":
                        gene_names.append(gene_name)
                total_entries += 1

        counts = Counter(gene_names)
        top10 = counts.most_common(10)

        for rank, (gene_name, count) in enumerate(top10, 1):
            out.write(f"{node}\t{description}\t{total_entries}\t{len(gene_names)}\t{rank}\t{gene_name}\t{count}\n")

        print(f"[OK] {node} ({description}): {total_entries} entries, top gene: {top10[0] if top10 else 'N/A'}")

print(f"\nSummary table written to: {OUTFILE}")
