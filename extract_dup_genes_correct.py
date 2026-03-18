import os
import re
import glob

# Input: phyparts duplication node files
INPUT_PATTERN = "/home/tomi/data/phyparts/phyparts_dup.dupl.*"
OUTDIR = "/home/tomi/data/phyparts/GeneExtraction/duplication_gene_lists"

os.makedirs(OUTDIR, exist_ok=True)

def extract_genes_from_newick(newick):
    # Match TAXON@GENEID format
    genes = re.findall(r'([A-Z]+2?@[A-Za-z0-9_]+)', newick)
    # Clean protein suffixes (.p1, .p2 etc)
    cleaned = set()
    for g in genes:
        gene = re.sub(r'\.p\d+$', '', g)
        cleaned.add(gene)
    return cleaned

for filepath in sorted(glob.glob(INPUT_PATTERN)):
    basename = os.path.basename(filepath)
    if basename.endswith(".tre") or basename.endswith(".key") or basename.endswith(".genes"):
        continue

    all_genes = set()

    with open(filepath) as f:
        dup_file_paths = [line.strip() for line in f if line.strip()]

    for dup_path in dup_file_paths:
        if not os.path.exists(dup_path):
            continue
        with open(dup_path) as df:
            content = df.read()
        genes = extract_genes_from_newick(content)
        all_genes.update(genes)

    outfile = os.path.join(OUTDIR, basename + ".genes")
    with open(outfile, "w") as out:
        for gene in sorted(all_genes):
            out.write(gene + "\n")

    print(f"[OK] {basename} -> {len(all_genes)} unique genes")

print("Done!")
