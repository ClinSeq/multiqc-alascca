# multiqc-alascca

Plugin to MultiQC with ALASCCA-specific information. It currently checks the following: 

* Coverage in the ALASCCA-target regions
* Genetic identity of the tumor and normal

## Install

~~~bash
pip install git+https://github.com/dakl/multiqc-alascca
~~~

## Test

~~~bash

git clone https://github.com/dakl/multiqc-alascca
cd multiqc-alascca
multiqc tests/data -n ~/tmp/mqc-test

~~~

