# Duplication Analysis — Aizoaceae Phylogenomics

This repository contains the gene duplication analysis pipeline for the AIM 1 Aizoaceae (ice plants) phylogenomics project, covering 39 taxa. The analysis identifies which gene families underwent duplication events at specific nodes of the species tree, and annotates those duplicated genes using PANTHER 19.0 functional classifications.

---

## Biological Context

Aizoaceae (ice plants) represent the fastest radiating plant family on Earth. A key question driving this project is whether gene duplication played a role in facilitating rapid radiation — specifically, whether genes involved in key biological traits such as CAM/C4 photosynthesis, stress response, and secondary metabolism are preferentially duplicated in the rapidly radiating Ruschioideae* clade. This analysis directly addresses that question by mapping gene duplications onto species tree nodes and annotating the duplicated genes functionally.

---

## Pipeline Overview

### 1. Duplicate Subtree Extraction
Duplicate subtrees were extracted from 15,818 final homolog gene trees using the `extract_clades.py` script from the Yang and Smith (2014) phylogenomic pipeline, with a minimum of 4 ingroup taxa required per subtree and taxon classifications defined in AIZO.txt.

    python2 extract_clades.py treefiles/ .treefile ExtractedDups/ 4 AIZO.txt dup

This produced 13,822 duplicate subtree files (.dup) in ExtractedDups/.

### 2. PhyParts Duplication Mapping
PhyParts (duplication mode) was run to map the extracted duplicate subtrees onto the rooted ASTRAL median species tree, identifying at which node of the species tree each duplication event occurred.

    java -jar phyparts-0.0.1-SNAPSHOT-jar-with-dependencies.jar \
      -a 2 \
      -d ExtractedDups/ \
      -m Median.tre.rr \
      -o phyparts_dup \
      -v

Output files phyparts_dup.dupl.N contain file paths to all .dup files mapping to node N.

### 3. Gene ID Extraction Per Node
Gene IDs were extracted from each .dup file listed per node using a custom Python script, which opens each duplicate subtree file, parses the newick tree, and extracts all TAXON@GeneID identifiers.

    python3 extract_dup_genes_correct.py

Output: duplication_gene_lists/phyparts_dup.dupl.N.genes — one file per node containing all unique gene IDs that duplicated at that node.

### 4. PANTHER Functional Annotation
PANTHER 19.0 HMM searches were run by the PI on peptide sequences for 34 of 39 taxa (SAS2, SAS3, SAS4, SAS5, SAS6 not included), producing .pep.fa.out annotation files. These were used to annotate the duplicated gene IDs per node by matching gene IDs to PANTHER family IDs and linking those to gene names and GO terms via PANTHER19.0_HMM_classifications.

    python3 annotate_dup_genes.py

### 5. Summary Table Generation
A summary table of the top 10 most frequently duplicated gene functions per node was generated for rapid interpretation.

    python3 make_summary_table.py

---

## Key Results

- **11 nodes** with detectable gene duplications across the species tree
- **Node 5** (SAS7/ZAPE2/SEHU2/SEPO2/SEVE2 clade) had the highest number of duplicated genes — **602 unique genes**
- **Node 9** (Core Ruschioideae* + SAS13/MECR2) — **486 unique genes**
- **Node 11** (Core Ruschioideae*) — **386 unique genes**
- **1,636 total annotated entries** across all nodes
- Key duplicated gene families identified across Ruschioideae* nodes:
  - **Phosphoenolpyruvate carboxylase** — CAM/C4 photosynthesis enzyme
  - **Glycosyltransferases** — secondary metabolism
  - **ABC transporters** — stress tolerance and transport
  - **Receptor-like serine/threonine kinases** — stress signaling
  - **O-methyltransferases** — secondary metabolite biosynthesis
  - **Heat shock proteins** — stress response
  - **UDP-glycosyltransferases** — secondary metabolism
  - **V-type proton ATPase** — vacuolar acidification, CAM related

These results suggest that gene duplication in the rapidly radiating Ruschioideae* was enriched for genes involved in CAM/C4 photosynthesis, stress response, and secondary metabolism — directly connecting gene family expansion to the key biological traits of this group.

---

## Repository Structure

    GeneExtraction/
    |
    |-- extract_dup_genes_correct.py     # Extracts gene IDs from .dup files per node
    |-- annotate_dup_genes.py            # Maps gene IDs to PANTHER annotations
    |-- make_summary_table.py            # Generates top 10 gene summary per node
    |-- README.md
    |
    |-- duplication_gene_lists/          # Gene IDs per node (phyparts_dup.dupl.N.genes)
    |
    |-- AnnotationResults/
        |-- all_nodes_annotations.tsv        # Master annotation table (all nodes)
        |-- summary_top_genes_per_node.tsv   # Top 10 genes per node summary
        |-- phyparts_dup.dupl.N_annotations.tsv  # Per-node annotation tables

---

## Node Key

| Node | Clade | Duplicated Genes |
|------|-------|-----------------|
| 5 | SAS7/ZAPE2/SEHU2/SEPO2/SEVE2 | 602 |
| 6 | ZAPE2/SEHU2/SEPO2/SEVE2 | 15 |
| 7 | SEHU2/SEPO2/SEVE2 | 192 |
| 8 | SEPO2/SEVE2 | 51 |
| 9 | Core Ruschioideae* + SAS13/MECR2 | 486 |
| 10 | SAS13/MECR2 | 152 |
| 11 | Core Ruschioideae* | 386 |
| 12 | Ruschioideae* subgroup | 78 |
| 15 | DEEC/SAS10/SAS8 clade | 14 |
| 26 | SAS28/SAS23/SAS5 clade | 21 |
| 36 | SAS18/SAS2 clade | 4 |

---

## Tools and Versions

| Tool | Version | Purpose |
|------|---------|---------|
| PhyParts | 0.0.1-SNAPSHOT | Duplication mapping onto species tree |
| PANTHER | 19.0 | Functional annotation |
| Python | 3.x | Gene extraction and annotation scripts |
| Yang & Smith scripts | — | Duplicate subtree extraction |

---

## Citations

> Yang, Y. & Smith, S.A. (2014). Orthology inference in nonmodel organisms using transcriptomes and low-coverage genomes. Molecular Biology and Evolution, 31(11):3081-3092.

> Mi, H. et al. (2021). PANTHER version 16: a revised family classification, tree-based classification tool, enhancer regions and extensive API. Nucleic Acids Research, 49(D1):D394-D403.

---

## Notes

* — Ruschioideae clade assignment pending confirmation with PI.
PANTHER annotations unavailable for SAS2, SAS3, SAS4, SAS5, SAS6 — peptide files not provided.
12 entries annotated as FAMILY NOT NAMED — legitimate PANTHER hits for uncharacterized gene families.

---

## Author

**Tomi Jacobs** — PhD Candidate, Computational Biology / Phylogenomics
