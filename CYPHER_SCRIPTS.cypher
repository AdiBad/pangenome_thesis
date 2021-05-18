CREATE DATABASE

Create all CDS (283621 nodes, 3.8 seconds)
LOAD CSV with headers FROM "file:///panaroo_base.csv" as row
WITH toString(row.clustering_id) AS cluster_id,toString(row.gff_file) AS gff_file,toString(row.annotation_id) AS annotation_id,toString(row.description) AS description,toString(row.gene_name) AS gene_name
create (c:CDS{cluster_id:cluster_id,annotation_id:annotation_id,name:gene_name,description:description,file_name:gff_file})

Create all CLUSTER (12298 nodes, 362 milliseconds)
LOAD CSV with headers FROM "file:///Nodes_base.csv" as row
WITH toString(row.id) AS cluster_id,toString(row.label) AS label,toString(row.lengths) AS lengths,toString(row.description) AS description,toString(row.name) AS name,toString(row.seqIDs) AS seqIDs,toString(row.dna) AS dna,toString(row.annotation) AS annotation
create (c:CLUSTER{cluster_id:cluster_id,label:label,annotation:annotation,description:description,lengths:lengths,seqIDs:seqIDs,dna:dna,name:name})
Create Index on Cluster ID to make edge creation more efficient (1 index, 8 milliseconds)
create index on :CLUSTER(cluster_id)

Create edges between neighboring clusters (14286 relationships, 475 ms)
LOAD CSV with headers FROM "file:///Edges_base.csv" as row
WITH toString(row.source) AS source,toString(row.target) AS target,toInteger(row.size) AS size,toString(row.members) AS members
MATCH (c1:CLUSTER {cluster_id:source}), (c2:CLUSTER {cluster_id:target})
CREATE ((c1)-[r:NEIGHBOUR{number_of_members:size, members:members}]->(c2))

Create index on CLuster ID of CDS (1 index, 4 ms)
create index on :CDS(cluster_id)

Create edges between orthologous CDS and respective cluster (282604 relationships, 2732 ms)
match (p:CLUSTER) with *,p.seqIDs as id
with *,[x in split(id,'~') | x] as cl_id
unwind cl_id as i
match (c:CDS {cluster_id:i})
create ((c)-[:ORTHOLOG{orthologous_cluster_id:i}]->(p))

[1.6 GB at this stage] Now make index on specific attributes to increase speed of match and set (because some of these are NULL)
create index on :CLUSTER(name) (3 ms)
create index on :CDS(annotation_id) (3 ms)

Add CLUSTER specific annotation (121375 properties, 1549 ms)
LOAD CSV with headers FROM "file:///cds_annot.csv" as row
WITH toString(row.Gene_name) AS name,toString(row.UNIPROT_ID) AS UniProt_ID where name is not null 
MATCH(d:CLUSTER{name:name})
SET d.UNIPROT_ID=UniProt_ID

Add CDS specific information (957495 properties, 4181 ms)
LOAD CSV with headers FROM "file:///cds_annot.csv" as row
WITH toString(row.ID) AS ID,toString(row.Gene_name) AS name,toString(row.strand) AS strand,toString(row.COG_ID) AS COG_ID,toInteger(row.CDS_start) AS CDS_start,toInteger(row.CDS_end) AS CDS_stop where ID is not null
MATCH (d:CDS{annotation_id:ID})
SET d.COG_ID = COG_ID,d.strand=strand, d.CDS_start=CDS_start, d.CDS_stop=CDS_stop
