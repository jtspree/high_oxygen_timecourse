"""
INFO

Script for analyzing vO2 fluorescence data
Generates graphs and statistical data

Created by Joshua Temple
Assistance from Ben Lucker and Oliver Tessmer

Created 2018-03-16
@jtspree
"""

# LIBRARY

import numpy as np
import pandas as pd
import os, sys
import matplotlib.pyplot as plt
import glob 
import csv
import pickle
import datetime


# FUNCTIONS

def savePlot(WholeTrace, DestinationFolder, basename):
    fig = plt.figure(1, figsize=(10, 6))
    ax = fig.add_subplot(1, 1, 1)
    y = WholeTrace['NormFluor']
    ax.plot(y)
    ax.set_ylim(0, 4)
    ax.set_ylabel("Fluorescence")
    ax.set_xlabel("")
    # plt.show()
    fig.savefig(DestinationFolder + basename + "_plot.png")
    plt.clf()


def calculator(WholeTrace, rep):
    calc_dict = {}

    # Values
    calc_dict["F0"] = WholeTrace.iloc[98][2]
    calc_dict["Fm"] = WholeTrace['NormFluor'].iloc[99:198].quantile(q=0.98)
    calc_dict["Fs"] = WholeTrace['NormFluor'].iloc[687:697].mean(axis=0)
    calc_dict["Fm_prime"] = WholeTrace['NormFluor'].iloc[700:780].quantile(q=0.98)
    calc_dict["F0_prime"] = WholeTrace['NormFluor'].iloc[1187:1197].mean(axis=0)
    calc_dict["Fm_prime2"] = WholeTrace['NormFluor'].iloc[1305:1380].quantile(q=0.98)
    calc_dict["Fm_prime4"] = WholeTrace['NormFluor'].iloc[2500:2580].quantile(q=0.98)
    calc_dict["Fm_prime6"] = WholeTrace['NormFluor'].iloc[3700:3780].quantile(q=0.98)

    F0 = calc_dict["F0"]
    Fm = calc_dict["Fm"]
    Fs = calc_dict["Fs"]
    Fm_prime = calc_dict["Fm_prime"]
    F0_prime = calc_dict["F0_prime"]
    Fm_prime2 = calc_dict["Fm_prime2"]
    Fm_prime4 = calc_dict["Fm_prime4"]
    Fm_prime6 = calc_dict["Fm_prime6"]

    # Calculations
    calc_dict["Fv"] = Fm - F0
    calc_dict["FvFm"] = calc_dict["Fv"] / Fm
    calc_dict["NPQ"] = (Fm - Fm_prime) / Fm_prime
    calc_dict["qE"] = Fm_prime2 - Fm_prime
    calc_dict["qL"] = ((Fm_prime - Fs) / (Fm_prime - F0_prime)) * (F0_prime / Fs)
    calc_dict["qT"] = Fm_prime6 - Fm_prime4
    calc_dict["qP"] = (Fm_prime - Fs) / (Fm_prime - F0_prime)

    measurements = pd.DataFrame(calc_dict, index=["rep" + str(rep)])
    return measurements

def parse_phi2_fluor(folder):
    Phi2_Filename = None
    Fluor_Filename = None
    for filename in os.listdir(folder):
        if filename.endswith(Phi2_Filename_Suffix):
            Phi2_Filename = filename
        elif filename.endswith(Fluor_Filename_Suffix):
            Fluor_Filename = filename
    if (Phi2_Filename is None):
        print("No phi2 file for " + folder)
        return None
    if (Fluor_Filename is None):
        print("No fluorescence file for " + folder)
        return None
    Phi2_data =  pd.read_table(folder + Phi2_Filename)
    Phi2_data.columns = ["Time", "Fluorescence", "Reference", "Delta"]
    Phi2_data = Phi2_data[[0, 1]]

    Fluor_data = pd.read_table(folder + Fluor_Filename)
    Fluor_data.columns = ["Time", "Fluorescence", "Reference", "Delta"]
    Fluor_data = Fluor_data[[0, 1]]
    FvFm_Trace = pd.DataFrame(Fluor_data[:599])
    DarkRec_Trace = pd.DataFrame(Fluor_data[600:])

    T1 =(FvFm_Trace, Phi2_data, DarkRec_Trace)

    WholeTrace = pd.concat(T1)
    WholeTrace.reset_index(WholeTrace, inplace=True, drop=True)

    BaseLineCor = (WholeTrace['Fluorescence'] - 0.127)
    Norm_Val = BaseLineCor[90:98].mean(axis=0)
    NormFluor = BaseLineCor / Norm_Val
    WholeTrace['NormFluor'] = NormFluor
    return WholeTrace

def get_path(sample, timepoint, rep):
    rel_path = sample + "/" + "hr" + str(timepoint) + "/" + "rep" + str(rep) + "/"
    folder = rootFolder + rel_path
    if not os.path.isdir(folder):
        print(folder + " does not exist")
        return None, None, None
    basename = sample + "_" + "hr" + str(timepoint) + "_" + "rep" + str(rep)
    return rel_path, basename, folder


Phi2_Filename_Suffix = "vo2_flr_0001.dat"
Fluor_Filename_Suffix = "flr_0001.dat"
rootFolder = "C:/Users/templejo/Desktop/PBRexp060_PyScript/specdata_raw_edited/"


for sample in ["CC-1009", "CC-2343"]:
    for timepoint in [0, 1, 3, 6, 12, 24, 48]:
        all_reps_measurements = []
        all_reps_fluor = None
        for rep in [1, 2, 3, 4]:

            rel_path, basename, folder = get_path(sample, timepoint, rep)
            if rel_path is None:
                continue

            DestinationFolder = "C:/Users/templejo/Desktop/PBRexp060_PyScript/output/" + rel_path
            if not os.path.isdir(DestinationFolder):
                os.makedirs(DestinationFolder)

            WholeTrace = parse_phi2_fluor(folder)
            if WholeTrace is None:
                continue
            if all_reps_fluor is None:
                all_reps_fluor = WholeTrace.copy()
                all_reps_fluor[rep] = all_reps_fluor['NormFluor']
                all_reps_fluor.drop(['NormFluor', 'Fluorescence', 'Time'], axis=1, inplace=True)
            else:
                all_reps_fluor[rep] = WholeTrace['NormFluor']

            # save an image file with the fluorescence plot for this sample/time/rep
            savePlot(WholeTrace, DestinationFolder, basename)

            # compute fm, phi2, etc. for this sample/time/rep
            measurements = calculator(WholeTrace, rep)

            # append the computed values to the dictionary that will contain all the reps for this sample/time
            all_reps_measurements.append(measurements)

            # save the computed values and the raw fluorescence to csv files (for just one sample/
            measurements.to_csv(DestinationFolder + basename + "_" + "measurements.csv")
            WholeTrace.to_csv(DestinationFolder + basename + "_" + 'trace.csv', sep=',')

        averagesDestination = os.path.dirname(os.path.abspath(DestinationFolder)) + "/averages"
        if not os.path.isdir(averagesDestination):
            os.makedirs(averagesDestination)

        all_measurements = pd.concat(all_reps_measurements)
        all_measurements.loc['average'] = all_measurements.mean()
        all_measurements.loc['std dev'] = all_measurements.std()
        all_measurements.to_csv(averagesDestination + "/" + sample + "_" + "hr" + str(timepoint) + "_" + "averages.csv")

        reps_list = list(all_reps_fluor.columns)
        all_reps_fluor['average'] = all_reps_fluor.mean(axis=1)
        all_reps_fluor['std dev'] = all_reps_fluor.std(axis=1)

        all_reps_fluor.to_csv(averagesDestination + "/" + sample + "_" + "hr" + str(timepoint) + "_" + "trace.csv")


        # Plot of avg and std dev for timepoint
        fig = plt.figure(1, figsize=(10, 6))
        ax = fig.add_subplot(1, 1, 1)
        ax.errorbar(all_reps_fluor.index, all_reps_fluor['average'], all_reps_fluor['std dev'], ecolor='red')
        ax.set_ylim(0, 4)
        ax.set_ylabel("Fluorescence")
        # plt.show()
        fig.savefig(averagesDestination + "/" + sample + "_" + "hr" + str(timepoint) + "_" + "avg_plot.png")
        plt.clf()

        # Plot of all replicates for timepoint
        fig = plt.figure(1, figsize=(10, 6))
        ax = fig.add_subplot(1, 1, 1)
        for rep in reps_list:
            ax.plot(all_reps_fluor[rep], label='rep_' + str(rep))
        ax.set_ylim(0, 4)
        ax.legend()
        ax.set_ylabel("Fluorescence")
        # plt.show()
        fig.savefig(averagesDestination + "/" + sample + "_" + "hr" + str(timepoint) + "_" + "all_plot.png")
        plt.clf()