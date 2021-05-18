# pangenome_thesis

This repository contains all major codes and scripts that were used at various stages of my Master thesis project 


The use of scripts:

Generate Prokka annotation

BASH: /annotate_thi.sh(input: Unicycler FASTA assemblies, output: ffn,faa, gbk, gff, fna, gbff files)


To populate database:

BASH: macros

cat *.gff | cut -f4,5,7,9 > cds_annot.tsv

sed -i "/##FASTA/,/##/d" cds_annot.tsv

sed -i '/^##/d' cds_annot.tsv



PYTHON: refine_CDS_annot.ipynb (input: cds_annot.tsv, output: cds_annot.csv) 

Create CDS specific annotation from the information in cds_annot.tsv above

Run panaroo on GFF files

Download github code for panaroo: https://github.com/gtonkinhill/panaroo 

python setup.py install

panaroo -i *.gff -o results/ --clean-mode strict



On the output of panaroo files:

PYTHON: noddy_and_eddy (input: final_graph.gml, output: Nodes_base.csv, Edges_base.csv)

Use panaroo's output file (final_graph.gml) to generate a Node specific file and Edge specific file

PYTHON: strainNamez.ipynb (input: gene_presence_absence.csv, output: referStrain.txt)

Uses the presence absence matrix generated from panaroo to make a text file that represents prokka’s code for each strain, this file will not be used later, it is just for information



ON NEO4J:

Create all CDS nodes from panaroo_base.csv (processed file from gene_data.csv provided as a result of panaroo output)

BASH: awk -F ","  -OFS ‘,’ '{ print $4,$3 ,$1,,$8,,$7,,$5,,$6}' gene_data.csv > panaroo_base.csv

After creating Neo4j database, I am updating the CDS and CLUSTER with appropriate information  NEO4J (input: cds_annot.csv)

CDS => COG_ID, strand, CDS_start, CDS_stop

CLUSTER => UniProt_ID



To use the database with certain scripts:

PYTHON: PSC_distribution_PaLo28.ipynb (input: CSV file from Neo4j specific to persistent/cloud/shell genes, output: graphs for gene families)

Makes a graph that spans across the length of genome and plots the gene family type (shell/cloud/persistent) in separate graphs. The CSV file can be created using the code written in Appendix (Cypher code_ reference)



Determine CDS in bacteria that correspond to prophage regions determined by PHASTER:

PYTHON: automate_phaster_upload.py (input: FNA files of all genomes, list of all file names, output: zip file from PHASTER for each genome)

BASH: extract_summary.sh (input: zip file from PHASTER for each genome, output: summary.txt files for each genome)

PYTHON: viral_extract.ipynb (input: summary.txt file(s) from PHASTER, output: PHASTER_out_47ronin.csv)

This script can create a structured dataframe of the summary file that comes from PHASTER. Also contains code to run for multiple summary.txt files. The output can be matched across Neo4j to fetch the appropriate CDS information.


