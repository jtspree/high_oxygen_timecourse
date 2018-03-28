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
        all_reps_flr_measurements = []
        all_reps_ECS_DIRK_values = []
        all_reps_fluor = None
        all_reps_ECS_DIRK = None
        all_reps_ECS_DCMU_P700 = None
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
            flr_calc_values_df = parse_math.flr_calculator(WholeTrace, rep)

            # append the computed values to the dictionary that will contain all the reps for this sample/time
            all_reps_flr_measurements.append(flr_calc_values_df)

            # save the computed values and the raw fluorescence to csv files (for just one sample/
            flr_calc_values_df.to_csv(DestinationFolder + basename + "_" + "flr_measurements.csv")
            WholeTrace.to_csv(DestinationFolder + basename + "_" + 'flr_trace.csv', sep=',')

            # parse ECS data into dataframe
            ECS_DIRK_data = parse_math.parse_ECS_data(folder, DestinationFolder, basename)

            # calculate ECS DIRK rates
            df, ECS_DIRK_calc_values_df, mean, std_dev = parse_math.ECS_rates_calculator(ECS_DIRK_data, DestinationFolder, basename, rep)
            all_reps_ECS_DIRK_values.append(ECS_DIRK_calc_values_df)

            # save ECS DIRK plot
            plots.save_ECS_DIRK_plot(DestinationFolder, basename, ECS_DIRK_data, mean)

            if all_reps_ECS_DIRK is None:
                all_reps_ECS_DIRK = ECS_DIRK_data.copy()
                all_reps_ECS_DIRK[rep] = all_reps_ECS_DIRK['y_correct']
                all_reps_ECS_DIRK.index = all_reps_ECS_DIRK['x_correct']
                all_reps_ECS_DIRK.drop(['Delta', 'y_initial', 'amplitude', 'y_correct', 'Time', 'x_correct'], axis=1, inplace=True)
            else:
                all_reps_ECS_DIRK[rep] = ECS_DIRK_data['y_correct'].values

            # parse ECS DCMU P700 data into dataframe
            ECS_DCMU_P700_df = parse_math.parse_ECS_DCMU_P700_data(folder, DestinationFolder, basename)

            # calculate ECS DCMU P700 measurements
            ECS_DCMU_P700_calc_values_df, ESC_DCMU_P700_slope, ECS_DCMU_P700_mean, ECS_DCMU_P700_std_dev = parse_math.ECS_DCMU_P700_rates_calc(ECS_DCMU_P700_df, DestinationFolder, basename, rep)

            # save ECS DCMU P700 plot
            plots.save_ECS_DCMU_P700_plot(DestinationFolder, basename, ECS_DCMU_P700_df, ECS_DCMU_P700_mean)

            if all_reps_ECS_DCMU_P700 is None:
                all_reps_ECS_DCMU_P700 = ECS_DCMU_P700_df.copy()
                all_reps_ECS_DCMU_P700[rep] = all_reps_ECS_DCMU_P700['y_correct']
                all_reps_ECS_DCMU_P700.index = all_reps_ECS_DCMU_P700['x_correct']
                all_reps_ECS_DCMU_P700.drop(['Delta', 'y_initial', 'amplitude', 'y_correct', 'Time', 'x_correct', 'y_final'], axis=1, inplace=True)
            else:
                all_reps_ECS_DCMU_P700[rep] = ECS_DCMU_P700_df['y_correct'].values

        averagesDestination = os.path.dirname(os.path.abspath(DestinationFolder)) + "/averages"
        if not os.path.isdir(averagesDestination):
            os.makedirs(averagesDestination)

        all_flr_measurements_df = pd.concat(all_reps_flr_measurements)
        all_flr_measurements_df.loc['average'] = all_flr_measurements_df.mean()
        all_flr_measurements_df.loc['std dev'] = all_flr_measurements_df.std()
        all_flr_measurements_df.to_csv(averagesDestination + "/" + sample + "_" + "hr" + str(timepoint) + "_" + "flr_averages.csv")

        all_ECS_DIRK_measurements_df = pd.concat(all_reps_ECS_DIRK_values)
        all_ECS_DIRK_measurements_df.loc['average'] = all_ECS_DIRK_measurements_df.mean()
        all_ECS_DIRK_measurements_df.loc['std dev'] = all_ECS_DIRK_measurements_df.std()
        all_ECS_DIRK_measurements_df.to_csv(averagesDestination + "/" + sample + "_" + "hr" + str(timepoint) + "_" + "ECS_DIRK_averages.csv")

        reps_list = list(all_reps_fluor.columns)

        all_reps_fluor['average'] = all_reps_fluor.mean(axis=1)
        all_reps_fluor['std dev'] = all_reps_fluor.std(axis=1)
        all_reps_fluor.to_csv(averagesDestination + "/" + sample + "_" + "hr" + str(timepoint) + "_" + "flr_trace.csv")

        all_reps_ECS_DIRK['average'] = all_reps_ECS_DIRK.mean(axis=1)
        all_reps_ECS_DIRK['std dev'] = all_reps_ECS_DIRK.std(axis=1)
        all_reps_ECS_DIRK.to_csv(averagesDestination + "/" + sample + "_" + "hr" + str(timepoint) + "_" + "ECS_DIRK_trace.csv")

        all_reps_ECS_DCMU_P700['average'] = all_reps_ECS_DCMU_P700.mean(axis=1)
        all_reps_ECS_DCMU_P700['std dev'] = all_reps_ECS_DCMU_P700.std(axis=1)
        all_reps_ECS_DCMU_P700.to_csv(averagesDestination + "/" + sample + "_" + "hr" + str(timepoint) + "_" + "ECS_DCMU_P700_trace.csv")

        # plot of flr avg and std dev for timepoint
        output_path = averagesDestination + "/" + sample + "_" + "hr" + str(timepoint) + "_" + "flr_avg_plot.png"
        plots.plot_allreps_avg(output_path, all_reps_fluor, ylim=(0, 4))

        # plot of all flr replicates for timepoint
        output_path = averagesDestination + "/" + sample + "_" + "hr" + str(timepoint) + "_" + "flr_all_plot.png"
        plots.plot_allreps_separate(output_path, all_reps_fluor, reps_list, xlim=None, ylim=(0, 4))

        # plot of ECS DIRK avg and std dev for timepoint
        output_path = averagesDestination + "/" + sample + "_" + "hr" + str(timepoint) + "_" + "ECS_DIRK_avg_plot.png"
        plots.plot_allreps_avg(output_path, all_reps_ECS_DIRK, ylim=(-0.0008, 0.001))

        # plot of all ECS DIRK replicates for timepoint
        output_path = averagesDestination + "/" + sample + "_" + "hr" + str(timepoint) + "_" + "ECS_DIRK_all_plot.png"
        plots.plot_allreps_separate(output_path, all_reps_ECS_DIRK, reps_list, xlim=None, ylim=(-0.0008, 0.001))

        # plot ECS DCMU P700 avg and std dev for timepoint
        output_path = averagesDestination + "/" + sample + "_" + "hr" + str(timepoint) + "_" + "ECS_DCMU_P700_avg_plot.png"
        plots.plot_allreps_avg(output_path, all_reps_ECS_DCMU_P700, xlim=(-0.1, 1), ylim=(-0.0002, 0.001))

        # plot all ECS DCMU P700 reps for timepoint
        output_path = averagesDestination + "/" + sample + "_" + "hr" + str(timepoint) + "_" + "ECS_DCMU_P700_all_plot.png"
        plots.plot_allreps_separate(output_path, all_reps_ECS_DCMU_P700, reps_list, xlim=(-0.1, 1), ylim=(-0.0002, 0.001))