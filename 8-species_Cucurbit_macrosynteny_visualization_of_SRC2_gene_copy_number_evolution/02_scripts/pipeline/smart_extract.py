#!/usr/bin/env python3
"""
Extract pep/cds sequences from genomic files using GFF3 coordinates.
"""
import os, sys
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

def extract_sequences(gff3, genome_fasta, feature_type="CDS", out_fasta=None):
    """Extract feature sequences from genome assembly."""
    genome = SeqIO.to_dict(SeqIO.parse(genome_fasta, "fasta"))
    records = []
    
    with open(gff3) as f:
        for line in f:
            if line.startswith('#'): continue
            parts = line.strip().split('\t')
            if len(parts) < 9: continue
            if parts[2] != feature_type: continue
            
            chrom, start, end, strand = parts[0], int(parts[3]), int(parts[4]), parts[6]
            attr = parts[8]
            
            if chrom not in genome: continue
            seq = genome[chrom].seq[start-1:end]
            if strand == '-':
                seq = seq.reverse_complement()
            
            # Extract ID
            m = __import__('re').search(r'ID=([^;]+)', attr)
            gene_id = m.group(1) if m else f"{chrom}_{start}_{end}"
            
            records.append(SeqRecord(seq, id=gene_id, description=""))
    
    if out_fasta:
        SeqIO.write(records, out_fasta, "fasta")
        print(f"Wrote {len(records)} sequences to {out_fasta}")
    return records

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: smart_extract.py GFF3 GENOME_FASTA OUT_FASTA")
        sys.exit(1)
    extract_sequences(sys.argv[1], sys.argv[2], out_fasta=sys.argv[3])
