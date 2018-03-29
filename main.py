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


root_folder = "C:/Users/templejo/Desktop/PBRexp060_PyScript/specdata_raw/"

all_measurements_types = {
    # type name: [parsing function, calculator function, xlim, ylim]
    'flr'            : [parse_math.parse_phi2_fluor, parse_math.flr_calculator, None, (0, 4)],
    'ECS_DIRK'       : [parse_math.parse_ECS_data, parse_math.ECS_rates_calculator, None, (-0.001, 0.001)],
    'ECS_DCMU_P700'  : [parse_math.parse_ECS_DCMU_P700_data, parse_math.ECS_DCMU_P700_rates_calc, None, (-0.0008, 0.0012)]
}

all_samples = ["CC-1009", "CC-2343"]

all_timepoints = [0, 1, 3, 6, 12, 24, 48]

all_reps = [1, 2, 3, 4]


for sample in all_samples:
    for timepoint in all_timepoints:
        all_reps_computed_values = {}
        all_reps_raw_data = {}
        for measurements_type in all_measurements_types.keys():
            all_reps_computed_values[measurements_type] = []
            all_reps_raw_data[measurements_type] = pd.DataFrame()

        for rep in all_reps:

            rel_path, basename, folder = parse_math.get_path(root_folder, sample, timepoint, rep)
            if rel_path is None:
                continue

            DestinationFolder = "C:/Users/templejo/Desktop/PBRexp060_PyScript/output/" + rel_path
            if not os.path.isdir(DestinationFolder):
                os.makedirs(DestinationFolder)

            for measurements_type in all_measurements_types.keys():

                # trace_df = parse_math.parse_phi2_fluor(folder)
                trace_df = all_measurements_types[measurements_type][0](folder)

                if trace_df is None:
                    continue

                all_reps_raw_data[measurements_type][rep] = trace_df['y_correct']

                # compute fm, phi2, etc. for this sample/time/rep
                calc_function = all_measurements_types[measurements_type][1]
                calc_values_df = calc_function(trace_df, sample, timepoint, rep, DestinationFolder)

                # save an image file with the fluorescence plot for this sample/time/rep
                if measurements_type == 'flr':
                    plots.save_flr_plot(trace_df, DestinationFolder, basename)
                if measurements_type == 'ECS_DIRK':
                    mean = calc_values_df['rates_mean'].values[0]
                    plots.save_ECS_DIRK_plot(DestinationFolder, basename, trace_df, mean)
                if measurements_type == 'ECS_DCMU_P700':
                    ECS_DCMU_P700_mean = calc_values_df['rates_mean'].values[0]
                    plots.save_ECS_DCMU_P700_plot(DestinationFolder, basename, trace_df, ECS_DCMU_P700_mean)


                # append the computed values to the dictionary that will contain all the reps for this sample/time
                all_reps_computed_values[measurements_type].append(calc_values_df)

                # save the computed values and the raw fluorescence to csv files (for just one sample/
                calc_values_df.to_csv(DestinationFolder + basename + "_" + measurements_type + "_measurements.csv")
                trace_df.to_csv(DestinationFolder + basename + "_" + measurements_type + '_trace.csv', sep=',')

        # Switch to avg std and combined reps

        averagesDestination = os.path.dirname(os.path.abspath(DestinationFolder)) + "/averages"
        if not os.path.isdir(averagesDestination):
            os.makedirs(averagesDestination)

        averages_output_path_prefix = averagesDestination + "/" + sample + "_" + "hr" + str(timepoint) + "_"

        for measurements_type in all_measurements_types.keys():
            all_measurements_df = pd.concat(all_reps_computed_values[measurements_type])
            all_measurements_df.loc['average'] = all_measurements_df.mean()
            all_measurements_df.loc['std dev'] = all_measurements_df.std()
            all_measurements_df.to_csv(averages_output_path_prefix + measurements_type + "_averages.csv")

            reps_list = list(all_reps_raw_data[measurements_type].columns)

            all_reps_raw_data[measurements_type]['average'] = all_reps_raw_data[measurements_type].mean(axis=1)
            all_reps_raw_data[measurements_type]['std dev'] = all_reps_raw_data[measurements_type].std(axis=1)
            all_reps_raw_data[measurements_type].to_csv(averages_output_path_prefix + measurements_type + "_trace.csv")

            plots.save_allreps_plots(averages_output_path_prefix + measurements_type, all_reps_raw_data[measurements_type],
                                     reps_list, xlim=all_measurements_types[measurements_type][2],
                                     ylim=all_measurements_types[measurements_type][3])