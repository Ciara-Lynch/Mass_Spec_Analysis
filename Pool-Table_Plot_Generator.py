#!usr/bin/env python3
# by Ciara Lynch, 20/09/2020, last edit 01/07/2022
# Python can't read in files with gaps in the names, ensure to use a file name with no spaces, use _ instead
# this code takes two command line arguments;
# 2 INPUT.txt (as a tab delimited text file), one for up-regulated proteins and one for down-regulated proteins
# NOTE: need to edit this to take only one input file
# Changes made were involving unannotated pathway proteins
# Added a GUI for plot generation
import sys
import PySimpleGUI as sg
from matplotlib import pyplot as plt


def gui():
    sg.theme('DarkTeal12')  # Add a touch of color
    # All the stuff inside the window.
    layout = [[sg.Text("Your input file should be tab delimited in .txt format and have the following headers:")],
              [sg.Text("Protein ID | Protein Name | Pathway | LFQ Difference in Intensity")],
              [sg.In(size=(100, 1), enable_events=True, key="-FIN-"), sg.FileBrowse()],
              [sg.Text("Do you want labels? (y/n)"), sg.In(size=(20, 1), enable_events=True, key="-ANO-")],
              [sg.Text("Please give a cut-off point for labels:"), sg.In(size=(20, 1), enable_events=True, key="-CUT-")],
              [sg.Button("Generate Pool-Table Plot", disabled=True)],
              [sg.Button('Ok'), sg.Button('Cancel')]]

    # Create the Window
    window = sg.Window('Pool-Table Plot Generator', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event in [sg.WIN_CLOSED, 'Cancel']:  # if user closes window or clicks cancel
            break
        if event == "-FIN-":
            window["Generate Pool-Table Plot"].Update(disabled=False)
        if event == "Generate Pool-Table Plot":
            fin = values["-FIN-"]      # this should show the name of the file for input plus filepath
            if values["-FIN-"][-4::1] != ".txt":
                sg.popup("File should be in .txt format")
            if values["-ANO-"] == "y":
                annotation = "yes"
                try:
                    float(values["-CUT-"])
                    cutoff = float(values["-CUT-"])
                    if values["-FIN-"][-4::1] == ".txt":
                        return annotation, cutoff, fin
                except:
                    sg.popup("Cut-off value should be a number")
            else:
                annotation = "no"
                cutoff = "none"
                if values["-FIN-"][-4::1] == ".txt":
                    return annotation, cutoff, fin


def plot_generator(pathways, annot, cutoff):
    # pathways = a dictionary of each pathway as keys, and a list of lists of proteins and differences as value.
    # annot = whether the user wanted annotations or not
    # cutoff = a float of a cut off point for the labels
    # now for a scatter of the statistically significant proteins (each marker individually labelled) and their fold difference (x-value) in each pathway (y value)
    # first need a dictionary with all only statistically significant protein and combined up and down regs.
    fig, ax = plt.subplots(figsize=[15, 10])
    alldiff = []
    orderedpathways = {}
    for i in sorted(pathways.keys(), key=str.lower):
        orderedpathways[i] = pathways[i]
    print(orderedpathways)
    # the three lines above make an alphabetical dictionary

    for key, value in orderedpathways.items():
        listofdiff = []  # will be a specific list for each pathway of coordinates to plot
        for value in sorted(pathways[key]):  # alphabetically sorts the values (ie proteins) for later mapping as well in case of annotation
            listofdiff += [float(value[1])]
        alldiff += [listofdiff]
        print(listofdiff)
    for xe, ye in zip(alldiff, (
    orderedpathways.keys())):  # this is a list of lists of differences as x-values, and list of pathway(keys) as y-values
        plt.scatter(xe, [ye] * len(xe), s=7)  # this line of code pairs off the keys with the matching list of x-values

    # now to add annotation for only the markers with more than 2 fold difference in expression
    if annot == "yes":
        for key, value in pathways.items():
            for protein in pathways[key]:
                if float(protein[1]) >= cutoff:  # can change these cut offs depending on how squished the graph is
                    ax.annotate(protein[0], (float(protein[1]), key), xytext=(-26, 4), textcoords="offset points")
                if float(protein[1]) <= -cutoff:  # i.e. want labels on only some points, if legible
                    ax.annotate(protein[0], (float(protein[1]), key), xytext=(-26, 4), textcoords="offset points")

    ax.set(xlabel="Mean Difference in LFQ Intensity")
    ax.axvline(0.5, color='gray', linewidth=1)      # draws a vertical cut off line to indicate threshold, optional
    ax.axvline(-0.5, color='gray', linewidth=1)
    plt.subplots_adjust(top=0.927, bottom=0.177, left=0.346, right=0.961, hspace=0.2, wspace=0.2)
    return plt.show()


def main():
    gui_output = gui()  # list of annotation (yes/no) and file input name
    annotation = gui_output[0]
    cutoff = gui_output[1]

    with open(gui_output[2]) as fin:
        fin.readline()  # skips header line
        lines = fin.readlines()
    n_up = 0
    n_down = 0
    n_nopath = 0
    pathways = {}  # to make a dictionary of each pathway (key), then a list of the proteins and the fold difference

    for line in lines:
        line = line.strip().split("\t")
        if float(line[-1]) > 0:
            n_up += 1
        if float(line[-1]) < 0:
            n_down += 1
        if line[-2] == "":
            n_nopath += 1


        # first need to make a variable called "path" for each protein"
        if line[2].startswith("PATHWAY"):
            path = line[2][9:line[2].find(";")]
            if "." in path:
                path = path[:path.find(".")]  # accounts for in a full stop is used instead of ;
        elif line[2].startswith('"PATHWAY'):
            path = line[2][9:line[2].find(";")]
            if "." in path:
                path = path[:path.find(".")]  # accounts for in a full stop is used instead of ;
        elif line[2] == "":
            path = "Unannotated"
        else:
            path = line[2]
        # assigns a single pathway known as "path" for each protein, some empty if no pathway known, or if manually entered.


        if path in pathways:
            pathways[path] += [[line[0], line[-1]]]
        else:
            pathways[path] = [[line[0], line[-1]]]

    # now have a dictionary (pathways) of each pathway as key, and a list of lists containing values of protein name and diff
    print(pathways)
    print("Total upreg proteins = {}".format(n_up))
    print("Total downreg proteins = {}".format(n_down))
    print("No of proteins with no pathway = {}".format(n_nopath))

    #set up the final graph of difference in intensity
    plot_generator(pathways, annotation, cutoff)


if __name__ == '__main__':
    main()
