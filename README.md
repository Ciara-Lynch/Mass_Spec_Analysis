# Mass_Spec_Analysis
Code for analysis of mass spectrometry data from Perseus, in order to generate 3 visualization graphs:
one barchart of the number of proteins in each pathway identified,
one piechart of the % of identified protiens that were contained within said pathway,
one scatter plot of the significantly dysregulated proteins, with a mean flouresence intensity difference between the sample and the baseline of >0.5 and an FDR of <0.05.
Takes two input files, a tab-delimited .txt file of up-regulated proteins, and the same for down-regulated proteins. Each file should contain four columns; 
a column each for the protein name, the gene name, the pathway involved, and the difference in mean intensity.
The first three columns can be found using the ID mapping tool on Uniprot, while the fourth comes from a students t-test carried out using Perseus software.
Usage: <directory path>python Pathway_graphs.py input_file_1.txt input_file_2.txt
