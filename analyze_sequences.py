#!/usr/bin/env python3
"""Read sequences.fasta, compute length, GC% and protein translation
for each sequence, print the results and save them to results.csv.

Two translations are produced (both saved in the CSV):
  1. aa_sequence : plain translation from the first nucleotide (frame 1).
  2. orf_protein : translation from the first start codon (AUG) until
                   the first stop codon (empty if no start codon exists).
"""

import csv
from pathlib import Path

BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR / "sequences.fasta"
OUTPUT_FILE = BASE_DIR / "results.csv"

genetic_code = {
    # Phenylalanine
    "UUU": "F", "UUC": "F",

    # Leucine
    "UUA": "L", "UUG": "L",
    "CUU": "L", "CUC": "L", "CUA": "L", "CUG": "L",

    # Isoleucine
    "AUU": "I", "AUC": "I", "AUA": "I",

    # Methionine (Start)
    "AUG": "M",

    # Valine
    "GUU": "V", "GUC": "V", "GUA": "V", "GUG": "V",

    # Serine
    "UCU": "S", "UCC": "S", "UCA": "S", "UCG": "S",
    "AGU": "S", "AGC": "S",

    # Proline
    "CCU": "P", "CCC": "P", "CCA": "P", "CCG": "P",

    # Threonine
    "ACU": "T", "ACC": "T", "ACA": "T", "ACG": "T",

    # Alanine
    "GCU": "A", "GCC": "A", "GCA": "A", "GCG": "A",

    # Tyrosine
    "UAU": "Y", "UAC": "Y",

    # Stop codons
    "UAA": "*", "UAG": "*", "UGA": "*",

    # Histidine
    "CAU": "H", "CAC": "H",

    # Glutamine
    "CAA": "Q", "CAG": "Q",

    # Asparagine
    "AAU": "N", "AAC": "N",

    # Lysine
    "AAA": "K", "AAG": "K",

    # Aspartic acid
    "GAU": "D", "GAC": "D",

    # Glutamic acid
    "GAA": "E", "GAG": "E",

    # Cysteine
    "UGU": "C", "UGC": "C",

    # Tryptophan
    "UGG": "W",

    # Arginine
    "CGU": "R", "CGC": "R", "CGA": "R", "CGG": "R",
    "AGA": "R", "AGG": "R",

    # Glycine
    "GGU": "G", "GGC": "G", "GGA": "G", "GGG": "G"
}


def read_fasta(path):
    """Return a dict {id: sequence} from a FASTA file."""
    sequences = {}
    seq_id = None
    parts = []
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if seq_id is not None:
                    sequences[seq_id] = "".join(parts).upper()
                seq_id = line[1:].split()[0]
                parts = []
            else:
                parts.append(line)
        if seq_id is not None:
            sequences[seq_id] = "".join(parts).upper()
    return sequences


def gc_percent(seq):
    """GC content as a percentage, rounded to 2 decimals."""
    if not seq:
        return 0.0
    return round((seq.count("G") + seq.count("C")) / len(seq) * 100, 2)


def dna_to_rna(seq):
    """Convert a DNA sequence to RNA (T -> U)."""
    return seq.replace("T", "U")


def translate(seq):
    """Translate DNA to protein from the first nucleotide (frame 1)."""
    mrna = dna_to_rna(seq)
    protein = []
    for i in range(0, len(mrna) - len(mrna) % 3, 3):
        codon = mrna[i:i + 3]
        protein.append(genetic_code.get(codon, "X"))
    return "".join(protein)


def translate_from_start(seq):
    """Translate from the first AUG until the first stop codon."""
    mrna = dna_to_rna(seq)
    start = mrna.find("AUG")
    if start == -1:
        return None

    protein = []
    for i in range(start, len(mrna) - 2, 3):
        codon = mrna[i:i + 3]
        amino_acid = genetic_code.get(codon, "X")
        if amino_acid == "*":
            break
        protein.append(amino_acid)
    return "".join(protein)


def main():
    sequences = read_fasta(INPUT_FILE)

    rows = []
    for seq_id, seq in sequences.items():
        orf = translate_from_start(seq)
        rows.append({
            "id": seq_id,
            "length": len(seq),
            "gc_percent": gc_percent(seq),
            "aa_sequence": translate(seq),
            "orf_protein": "" if orf is None else orf,
        })

    # Print results on screen
    for row in rows:
        print(f"ID: {row['id']}")
        print(f"Length: {row['length']}")
        print(f"GC%: {row['gc_percent']}")
        print(f"Amino acid sequence (frame 1): {row['aa_sequence']}")
        if row["orf_protein"] == "":
            print("Amino acid sequence (from start codon): "
                  "No start codon (AUG) found")
        else:
            print("Amino acid sequence (from start codon): "
                  f"{row['orf_protein']}")
        print("-" * 40)

    # Save to CSV
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["id", "length", "gc_percent",
                        "aa_sequence", "orf_protein"],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Results saved to {OUTPUT_FILE.name}")


if __name__ == "__main__":
    main()
