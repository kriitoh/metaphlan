"""
Assemble and sort some COVID reads...
"""

import subprocess
from pathlib import Path

from latch import small_task, workflow
from latch.types import LatchFile
from enum import Enum

class seqType(Enum):
    fasta = "fasta"
    fastq = "fastq"
    bowtie2 = "bowtie2out"
    sam = "sam"

@small_task
def profile(input_file: LatchFile, nproc:int, sequence_type: seqType) -> LatchFile:

    # A reference to our output.
    out_metagenome = Path("profiled_metagenome.txt").resolve()

    _meta_cmd = [
        "metaphlan",
        input_file,
        "--input_type",
        str(sequence_type.value),
        "--nproc",
        str(nproc),
        "--output_file",
        str(out_metagenome)
    ]

    subprocess.run(_meta_cmd)

    return LatchFile(str(out_metagenome), "latch:///profiled_metagenome.txt")


@workflow
def metaphlan(input_file: LatchFile, sequence_type: seqType, nproc: int) -> LatchFile:
    """Compute microbial abundances from metagenomic data

    Metaphlan
    ----

    MetaPhlAn is a computational tool for profiling the composition of microbial communities (Bacteria, Archaea and Eukaryotes) from metagenomic shotgun sequencing data (i.e. not 16S) with species-level. 

    * Input File Types (fasta, fastq, sam, bowtie2out)
    * Output file (.txt): This file contains the final computed organism abundances.

    Organism abundances are listed one clade per line, tab-separated from the clade's percent abundance

    __metadata__:
        display_name: Metaphlan
        author:
            name: Krystal Ching
            email: klc595@nyu.edu
            github: https://github.com/kriitoh
        repository: https://github.com/kriitoh/metaphlan
        license:
            id: MIT

    Args:

        input_file:
          {fastq,fasta,bowtie2out,sam} set whether the input is the FASTA file of metagenomic reads or the SAM file of the mapping of the reads against the MetaPhlAn db

          __metadata__:
            display_name: Input File

        
        nproc:
          number of cores to be used in analysis
          __metadata__:
            display_name: Number of Processors

        sequence_type:
          Type of sequence file to be profiled (fasta, fastq, bowtie2 output, or SAM file).
          __metadata__:
            display_name: Sequence Type

    """
    
    return profile(input_file=input_file, sequence_type=sequence_type, nproc=nproc)
    
