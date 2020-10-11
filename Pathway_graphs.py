#!usr/bin/env python3
# by Ciara Lynch, 20/09/2020, last edit 11/10/2020
# Python can't read in files with gaps in the names, ensure to use a file name with no spaces, use _ instead
# this code takes two command line arguments;
# 2 INPUT.txt (as a tab delimited text file), one for up-regulated proteins and one for down-regulated proteins
# this code will give three output files as .pdf into the working directory;
# a bar chart, a pie chart, and a scatter plot.
import sys
from matplotlib import pyplot as plt


def main():
    with open(sys.argv[1]) as fin1, open(sys.argv[2]) as fin2:
        fin1.readline()  # skips header line
        fin2.readline()
        lines1 = fin1.readlines()
        lines2 = fin2.readlines()
        up_protpath = {}     # blank dictionary to be populated later
        down_protpath = {}
        n_up = 0
        n_down = 0
        for line in lines1:
            line = line.split("\t")
            if line[2] == "":
                fin1.readline()  #skips if no pathway identified
            else:
                n_up += 1
                up_protpath[n_up] = line
        for line in lines2:
            line = line.split("\t")
            if line[2] == "":
                fin2.readline()  #skips if no pathway identified
            else:
                n_down += 1
                down_protpath[n_down] = line
        nototalupproteins = len(lines1)
        nopathwayupproteins = len(up_protpath)
        nototaldownproteins = len(lines2)
        nopathwaydownproteins = len(down_protpath)
        print("Total upreg proteins = {}".format(nototalupproteins))
        print("Total downreg proteins = {}".format(nototaldownproteins))
        print("No of proteins in up pathways = {}".format(nopathwayupproteins))
        print("No of proteins in down pathways = {}".format(nopathwaydownproteins))

    up_difference = {}         # to make a dictionary of each pathway (key), then a list of the proteins and the fold difference they demonstrated
    down_difference = {}
    #occurancesofpath = {}   # blank dictionary to put all pathways and number of times it occurred, can actually just use len of difference keys
    for key, value in up_protpath.items():
        path = up_protpath[key][2][up_protpath[key][2].find(":"):up_protpath[key][2].find(";")]  # cuts the string to after PATHWAY:, and before extra info
        path = path[2:]  # takes off leading : character
        if "." in path:
            path = path[0:path.find(".")]   # plans for possibility that path contains fullstop in place of usual semi-colon.
        if path in up_difference:
            up_difference[path] += ['{}:{}'.format(up_protpath[key][0], up_protpath[key][3])]
        else:
            up_difference[path] = ['{}:{}'.format(up_protpath[key][0], up_protpath[key][3])]

    for key, value in down_protpath.items():
        path = down_protpath[key][2][down_protpath[key][2].find(":"):down_protpath[key][2].find(";")]  # cuts the string to after PATHWAY:, and before extra info
        path = path[2:]  # takes off leading : character
        if "." in path:
            path = path[0:path.find(".")]   # plans for possibility that path contains fullstop in place of usual semi-colon.
        if path in down_difference:
            down_difference[path] += ['{}:{}'.format(down_protpath[key][0], down_protpath[key][3])]
        else:
            down_difference[path] = ['{}:{}'.format(down_protpath[key][0], down_protpath[key][3])]

    # now to make a graph of how many times each pathway occurred
    fig, ax = plt.subplots(nrows= 2, figsize=[15, 10])
    up_paths = []  # list of all pathways as y values
    up_occurr = []  # list of number of ocurrances as x values/ or percentage proteins maybe?
    down_paths = []
    down_occurr = []
    for key, value in up_difference.items():
        up_paths += [key]           # key is the name of the pathway
        up_occurr += [len(value)]   # this is the number of proteins in the path
    for key, value in down_difference.items():
        down_paths += [key]
        down_occurr += [len(value)]
    # this will be the upregulated subplot
    ax[0].barh(up_paths, up_occurr, color="darkblue", align="center")
    ax[0].set(title="Up-regulated Pathways", xlabel="Number of Proteins", ylabel="Pathway")
    textline = "Unidentified protein pathways = {:.2f}%".format(((nototalupproteins-nopathwayupproteins)/nototalupproteins)*100)
    ax[0].text(12, 11.5, textline, family='serif', style='italic', ha='center', va="top")
    # this will be the downregulated subplot
    ax[1].barh(down_paths, down_occurr, color="orange", align="center")
    ax[1].set(title="Down-regulated Pathways", xlabel="Number of Proteins", ylabel="Pathway")
    textline = "Unidentified protein pathways = {:.2f}%".format(((nototaldownproteins-nopathwaydownproteins)/nototaldownproteins)*100)
    ax[1].text(5, 9.5, textline, family='serif', style='italic', ha='left', va="top")

    plt.subplots_adjust(hspace=0.5, left=0.25)
    plt.savefig("{}_Barchart.png".format(str(sys.argv[1])[:-4], format="png"))
    plt.show()

    # now for the pie chart of percentages
    fig, ax = plt.subplots(nrows=2, figsize=[15, 10])
    ## need a list of percentage total proteins in each path with regard to all proteins id'd
    up_percpro = []
    down_percpro = []
    for number in up_occurr:
        up_percpro += [(number/nopathwayupproteins)*100]
    for number in down_occurr:
        down_percpro += [(number/nopathwaydownproteins)*100]
    ax[0].set(title="% Up-regulated Proteins in Pathway")
    patches, texts = ax[0].pie(up_percpro, shadow=True, startangle=90, radius=1.2)
    labels = ['{0} - {1:1.2f} %'.format(i, j) for i, j in zip(up_paths, up_percpro)]
    sort_legend = True
    if sort_legend:
        patches, labels, dummy = zip(*sorted(zip(patches, labels, up_percpro),
                                             key=lambda paths: paths[2],
                                             reverse=True))
    ax[0].legend(patches, labels, loc=[1, 0], fontsize=8)

    ax[1].set(title="% Down-regulated Proteins in Pathway")
    patches, texts = ax[1].pie(down_percpro, shadow=True, startangle=90, radius=1.2)
    labels = ['{0} - {1:1.2f} %'.format(i, j) for i, j in zip(down_paths, down_percpro)]
    sort_legend = True
    if sort_legend:
        patches, labels, dummy = zip(*sorted(zip(patches, labels, down_percpro),
                                             key=lambda paths: paths[2],
                                             reverse=True))
    ax[1].legend(patches, labels, loc=[1, 0], fontsize=8,)

    plt.subplots_adjust(hspace=2, left=-0.15)
    fig.tight_layout()
    plt.savefig("{}_Piechart.png".format(str(sys.argv[1])[:-4], format="png"))
    plt.show()

    # now for a scatter of the statistically significant proteins (each marker individually labelled) and their fold difference (x-value) in each pathway (y value)
    # first need a dictionary with all only statistically significant protein and combined up and down regs.

    statproteins = {}       # will include all, upreg and downreg
    for key, value in up_difference.items():
        for protein in up_difference[key]:
            diff = protein[protein.find(":")+1:-1]
            if float(diff) >= 0.5:      # diff here is the difference between the mean intensities after a studetn's t-test,with FDR of <0.05
                if key in statproteins:
                    statproteins[key] += [[protein[:protein.find(":")], diff]]
                else:
                    statproteins[key] = [[protein[:protein.find(":")], diff]]   # gives lists of a list for value of each pathway
    for key, value in down_difference.items():
        for protein in down_difference[key]:
            diff = protein[protein.find(":")+1:-1]
            if float(diff) <= -0.5:     # can change to suit depending on volume of proteins also
                if key in statproteins:
                    statproteins[key] += [[protein[:protein.find(":")], diff]]
                else:
                    statproteins[key] = [[protein[:protein.find(":")], diff]]   # gives lists of a list for value of each pathway
    print(statproteins)


    #set up the final graph of difference in intensity
    fig, ax = plt.subplots(figsize=[15, 10])
    alldiff = []
    for key, value in statproteins.items():
       listofdiff = []
       for value in statproteins[key]:
           listofdiff += [float(value[1])]
       alldiff += [listofdiff]
       print(listofdiff)
    for xe, ye in zip(alldiff, statproteins.keys()):
        plt.scatter(xe, [ye]*len(xe))

    # now to add annotation for only the markers with more than 2 fold difference in expression
    for key, value in statproteins.items():
        for protein in statproteins[key]:
            if float(protein[1]) >= 2.75:        # can change these cut offs depending on how squshed the graph is
                ax.annotate(protein[0], (float(protein[1]), key), xytext=(-26, 4), textcoords="offset points")
            if float(protein[1]) <= -1.5:         # i.e. want labels on only some points, if legible
                ax.annotate(protein[0], (float(protein[1]), key), xytext=(-26, 4), textcoords="offset points")

    ax.set(title="Significantly Dysregulated Proteins", xlabel="Mean Difference in Intensity")
    ax.axvline(0.5, color='gray', linewidth=2)      # draws a vertical cut off line
    ax.axvline(-0.5, color='gray', linewidth=2)
    fig.tight_layout()
    plt.savefig("{}_SigScatter.png".format(str(sys.argv[1])[:-4], format="png"))
    plt.show()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        import os.path

        print("""You must provide 2 input files: one of the up-regulated proteins, and the other of the down-regulated.
Files in .txt format, with tab delimited columns of protein name, gene name, pathway, and fold difference.

            USAGE: {} input_file_upregulated_proteins.txt input_file_downregulated_proteins.txt""".format(os.path.basename(sys.argv[0])))
        quit()
    main()

