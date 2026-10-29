<div align="center">

# 🧬 Sequence Analysis ✨

*A tiny, cute Python script that reads DNA, counts GC and translates it into proteins* 🍊

![Python](https://img.shields.io/badge/Python-3.6+-ff69b4?style=for-the-badge&logo=python&logoColor=white)
![Biopython](https://img.shields.io/badge/Biopython-not%20needed-a78bfa?style=for-the-badge)
![Dependencies](https://img.shields.io/badge/dependencies-zero-34d399?style=for-the-badge)

</div>

---

## 🌷 What does it do?

For every sequence in `sequences.fasta`, the script calculates:

| | |
|---|---|
| 🏷️ | **id** of the sequence |
| 📏 | **length** (number of nucleotides) |
| 💗 | **GC content** (%) |
| 🍬 | **amino acid sequence**, translated in two ways |

Everything is printed on screen 🖥️ and saved to `results.csv` 📄.
Only the **Python standard library** is used. No Biopython! 🙅‍♀️🐍

---

## 🗂️ Project structure

```
sequence-analysis/
├── 🐍 analyze_sequences.py   # main script
├── 🧫 sequences.fasta        # input: 5 short DNA sequences
├── 📊 results.csv            # output: made by the script
└── 📖 README.md
```

---

## 🚀 How to run

```bash
python3 analyze_sequences.py
```

> 💡 The script finds `sequences.fasta` next to itself and writes `results.csv` in the same folder, so you can run it from anywhere.

**Requirements:** Python 3.6+ and nothing else 🎀

---

## 🧫 Input

`sequences.fasta` has 5 sequences (24 to 48 nucleotides):

```
>seq1
ATGCGTACGTTAGCCGATCGATGC
>seq2
GATTACAGGCCTAGCTAGGATCCGTAACGT
>seq3
TTGACCGATGCTAGCTAGGCTAACGTTAGCCGATGC
>seq4
ACGTACGTGGCCTTAAGGCCATCGATCGTTACGATCGTAGCA
>seq5
GGCCTAATCGATGCTAGCTTAACCGGATCCGTTACGATCGTAGCCTAG
```

---

## 📊 Output

### 🎀 `results.csv`

Columns: `id, length, gc_percent, aa_sequence, orf_protein`

| 🏷️ id | 📏 length | 💗 gc_percent | 🍬 aa_sequence | 🌟 orf_protein |
|------|--------|------------|------------------|-------------|
| seq1 | 24 | 54.17 | `MRTLADRC` | `MRTLADRC` |
| seq2 | 30 | 50.0 | `DYRPS*DP*R` | |
| seq3 | 36 | 52.78 | `LTDAS*ANVSRC` | `MLARLTLAD` |
| seq4 | 42 | 52.38 | `TYVALRPSIVTIVA` | |
| seq5 | 48 | 52.08 | `GLIDASLTGSVTIVA*` | `MLA` |

- 🍬 `aa_sequence`: plain translation from the first nucleotide
- 🌟 `orf_protein`: translation from the first start codon until the first stop codon (**empty** if there is no start codon)

### 🖥️ Screen output

```
ID: seq1
Length: 24
GC%: 54.17
Amino acid sequence (frame 1): MRTLADRC
Amino acid sequence (from start codon): MRTLADRC
----------------------------------------
ID: seq2
Length: 30
GC%: 50.0
Amino acid sequence (frame 1): DYRPS*DP*R
Amino acid sequence (from start codon): No start codon (AUG) found
----------------------------------------
...
Results saved to results.csv
```

---

## 🔬 Methods and assumptions

<details>
<summary>🧵 <b>1. Coding strand</b></summary>

<br>

All input sequences are assumed to be the **coding (sense) strand**, i.e. the DNA strand whose sequence is identical to the mRNA (with T instead of U). So they are translated directly, **without** taking the reverse complement.

</details>

<details>
<summary>💗 <b>2. GC content</b></summary>

<br>

`GC% = (G + C) / length × 100`, rounded to 2 decimal places.

</details>

<details>
<summary>🍬 <b>3. Main translation (<code>aa_sequence</code>)</b></summary>

<br>

- DNA is converted to RNA (`T` → `U`), then translated codon by codon using the standard genetic code
- Translation starts from the **first nucleotide** (reading frame 1), whether or not a start codon exists
- Stop codons are shown as `*` and translation **continues** past them
- If the length is not divisible by 3, the incomplete last codon is ignored
- A codon with an unknown character is shown as `X`

</details>

<details>
<summary>🌟 <b>4. Translation from the start codon (<code>orf_protein</code>)</b></summary>

<br>

- The script finds the **first start codon** (`AUG`, which is `ATG` in DNA)
- Translation starts there and **stops at the first stop codon** (the stop codon is not included)
- If there is no start codon, the CSV cell is left **empty** and the screen says "No start codon (AUG) found"

| 🏷️ id | 📍 Start position (1-based) | 🌟 Protein |
|------|--------------------------|----------------------------|
| seq1 | 1 | `MRTLADRC` |
| seq2 | not found | - |
| seq3 | 8 | `MLARLTLAD` |
| seq4 | not found | - |
| seq5 | 10 | `MLA` |

</details>

<details>
<summary>📄 <b>5. CSV columns</b></summary>

<br>

The exercise text lists the columns as `AA Sequence id,length,gc_percent`. I used the order `id, length, gc_percent, aa_sequence` and added one extra column, `orf_protein`, for the start-codon-based translation.

</details>

<details>
<summary>⚠️ <b>6. Limitations</b></summary>

<br>

Only the forward (coding) strand is analyzed. Other reading frames, the reverse complement and multiple ORFs per sequence are not considered. Only the first AUG is used.

</details>

---

<div align="center">

Made with 💖 and 🍊 by **[Maryam Rostamkhani](https://github.com/Maryam-Rostamkhani)**

</div>
