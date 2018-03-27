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

import pandas as pd
import os
import plots
import parse_math

# CODE


rootFolder = "C:/Users/templejo/Desktop/PBRexp060_PyScript/specdata_raw/"

for sample in ["CC-1009", "CC-2343"]:
    for timepoint in [0, 1, 3, 6, 12, 24, 48]:
        all_reps_measurements = []
        all_reps_ECS_DIRK = []
        all_reps_fluor = None
        for rep in [1, 2, 3, 4]:

            rel_path, basename, folder = parse_math.get_path(rootFolder, sample, timepoint, rep)
            if rel_path is None:
                continue

            DestinationFolder = "C:/Users/templejo/Desktop/PBRexp060_PyScript/output/" + rel_path
            if not os.path.isdir(DestinationFolder):
                os.makedirs(DestinationFolder)

            WholeTrace = parse_math.parse_phi2_fluor(folder)
            if WholeTrace is None:
                continue
            if all_reps_fluor is None:
                all_reps_fluor = WholeTrace.copy()
                all_reps_fluor[rep] = all_reps_fluor['NormFluor']
                all_reps_fluor.drop(['NormFluor', 'Fluorescence', 'Time'], axis=1, inplace=True)
            else:
                all_reps_fluor[rep] = WholeTrace['NormFluor']

            # save an image file with the fluorescence plot for this sample/time/rep
            plots.save_flr_plot(WholeTrace, DestinationFolder, basename)

            # compute fm, phi2, etc. for this sample/time/rep
            measurements = parse_math.calculator(WholeTrace, rep)

            # append the computed values to the dictionary that will contain all the reps for this sample/time
            all_reps_measurements.append(measurements)

            # save the computed values and the raw fluorescence to csv files (for just one sample/
            measurements.to_csv(DestinationFolder + basename + "_" + "flr_measurements.csv")
            WholeTrace.to_csv(DestinationFolder + basename + "_" + 'flr_trace.csv', sep=',')

            # parse ECS data into dataframe
            ECS_DIRK_data = parse_math.parse_ECS_data(folder, DestinationFolder, basename)

            # calculate ECS DIRK rates
            df, values, mean, std_dev = parse_math.ECS_rates_calculator(ECS_DIRK_data, DestinationFolder, basename)

            # save ECS DIRK plot
            plots.save_ECS_DIRK_plot(DestinationFolder, basename, ECS_DIRK_data, mean)

            all_reps_ECS_DIRK.append(values)

        averagesDestination = os.path.dirname(os.path.abspath(DestinationFolder)) + "/averages"
        if not os.path.isdir(averagesDestination):
            os.makedirs(averagesDestination)

        all_measurements = pd.concat(all_reps_measurements)
        all_measurements.loc['average'] = all_measurements.mean()
        all_measurements.loc['std dev'] = all_measurements.std()
        all_measurements.to_csv(averagesDestination + "/" + sample + "_" + "hr" + str(timepoint) + "_" + "flr_averages.csv")

        reps_list = list(all_reps_fluor.columns)
        all_reps_fluor['average'] = all_reps_fluor.mean(axis=1)
        all_reps_fluor['std dev'] = all_reps_fluor.std(axis=1)

        all_ECS_DIRK = pd.concat(all_reps_ECS_DIRK)
        all_ECS_DIRK.loc['average'] = all_ECS_DIRK.mean()
        all_ECS_DIRK.loc['std dev'] = all_ECS_DIRK.std()
        all_ECS_DIRK.to_csv(averagesDestination + "/" + sample + "_" + "hr" + str(timepoint) + "_" + "ECS_DIRK_averages.csv")

        all_reps_fluor.to_csv(averagesDestination + "/" + sample + "_" + "hr" + str(timepoint) + "_" + "flr_trace.csv")

        # plot of avg and std dev for timepoint
        plots.plot_avg_stddev(averagesDestination, all_reps_fluor, sample, timepoint)

        # plot of all replicates for timepoint
        plots.plot_allreps(averagesDestination, all_reps_fluor, sample, timepoint, reps_list)