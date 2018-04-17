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
import plot_flr_meas_timepoint
import ECS_DIRK_oxidation
import vO2_ECS_DIRK_oxidation

# CODE

# root folders for file input and output
root_folder = "C:/Users/templejo/Desktop/high_oxygen_timecourse/specdata_raw_edited/"
root_output = "C:/Users/templejo/Desktop/high_oxygen_timecourse/output/"
root_master_folder = root_output + '/' + 'master/'
root_master_plots_folder = root_master_folder + '/' + 'plots/'

all_measurements_types = {
    # type name: [parsing function, calculator function, xlim, ylim, ignore_index]
    'flr'                   : [parse_math.parse_phi2_flr, parse_math.flr_calculator, None, (0, 4), True],
    'ECS_DIRK'              : [parse_math.parse_ECS_data, parse_math.ECS_rates_calculator, None, (-0.001, 0.001), False],
    'ECS_DCMU_P700'         : [parse_math.parse_ECS_DCMU_P700_data, parse_math.ECS_DCMU_P700_rates_calc, (12.4, 13.4), (-0.0002, 0.0012), False],
    'ECS_DIRK_oxidation'    : [ECS_DIRK_oxidation.parse_ECS_DIRK_oxidation_data, ECS_DIRK_oxidation.ECS_DIRK_oxidation_rates_calc,
                               (2.4, 4), (None, 0.0002), False],
    'vO2_ECS_DIRK_oxidation': [vO2_ECS_DIRK_oxidation.parse_vO2_ECS_DIRK_oxidation_data, vO2_ECS_DIRK_oxidation.vO2_ECS_DIRK_oxidation_rates_calc,
                               (None, None), (None, None), False]
    }

# select samples, timepoints, reps for script to analyze
all_samples = ["CC-1009", "CC-2343"]
all_timepoints = [1, 3]
all_reps = [1, 2, 3, 4]

master_dict = {}

for sample in all_samples:
    master_dict[sample] = {}
    for timepoint in all_timepoints:
        master_dict[sample][timepoint] = {}
        all_reps_computed_values = {}
        all_reps_raw_data = {}
        for measurements_type in all_measurements_types.keys():
            all_reps_computed_values[measurements_type] = []
            all_reps_raw_data[measurements_type] = None

        for rep in all_reps:

            rel_path, basename, folder = parse_math.get_path(root_folder, sample, timepoint, rep)
            if rel_path is None:
                continue

            destination_folder = root_output + rel_path
            if not os.path.isdir(destination_folder):
                os.makedirs(destination_folder)

            for measurements_type in all_measurements_types.keys():

                # raw trace dataframe from parse functions
                trace_df = all_measurements_types[measurements_type][0](folder)

                if trace_df is None:
                    continue

                if all_reps_raw_data[measurements_type] is None:
                    all_reps_raw_data[measurements_type] = pd.DataFrame(index=trace_df['Time'])

                print(measurements_type, sample, timepoint, rep)
                all_reps_raw_data[measurements_type][rep] = trace_df['y_correct'].values

                # compute fm, phi2, etc. for this sample, timepoint, rep
                calc_function = all_measurements_types[measurements_type][1]
                calc_values_df = calc_function(trace_df, sample, timepoint, rep, destination_folder)

                # save an image file with the fluorescence plot for this sample/time/rep
                if measurements_type == 'flr':
                    plots.save_flr_plot(trace_df, destination_folder, basename)
                if measurements_type == 'ECS_DIRK':
                    mean = calc_values_df['ECS_DIRK_rates_mean'].values[0]
                    plots.save_ECS_DIRK_plot(destination_folder, basename, trace_df, mean)
                if measurements_type == 'ECS_DCMU_P700':
                    ECS_DCMU_P700_mean = calc_values_df['ECS_DCMU_P700_rates_mean'].values[0]
                    plots.save_ECS_DCMU_P700_plot(destination_folder, basename, trace_df, ECS_DCMU_P700_mean)
                if measurements_type == 'ECS_DIRK_oxidation':
                    ECS_DIRK_oxidation_mean = calc_values_df['ECS_DIRK_oxidation_rate_mean'].values[0]
                    ECS_DIRK_oxidation.save_ECS_DIRK_oxidation_plot(
                        destination_folder, basename, trace_df, ECS_DIRK_oxidation_mean)
                if measurements_type == 'vO2_ECS_DIRK_oxidation':
                    vO2_ECS_DIRK_oxidation_mean = calc_values_df['vO2_ECS_DIRK_oxidation_rate_mean'].values[0]
                    vO2_ECS_DIRK_oxidation.save_vO2_ECS_DIRK_oxidation_plot(
                        destination_folder, basename, trace_df, vO2_ECS_DIRK_oxidation_mean)

                # append the computed values to the dictionary that will contain all the reps for this sample/timepoint
                all_reps_computed_values[measurements_type].append(calc_values_df)

                # save the computed values and the raw fluorescence to csv files (for just one sample/
                calc_values_df.to_csv(destination_folder + basename + "_" + measurements_type + "_measurements.csv")
                trace_df.to_csv(destination_folder + basename + "_" + measurements_type + '_trace.csv', sep=',')

        # switch to avg std and combined reps

        averages_destination = os.path.dirname(os.path.abspath(destination_folder)) + "/averages"
        if not os.path.isdir(averages_destination):
            os.makedirs(averages_destination)

        averages_output_path_prefix = averages_destination + "/" + sample + "_" + "hr" + str(timepoint) + "_"

        for measurements_type in all_measurements_types.keys():
            all_measurements_df = pd.concat(all_reps_computed_values[measurements_type])
            all_measurements_df.loc['average'] = all_measurements_df.mean()
            all_measurements_df.loc['std dev'] = all_measurements_df.std()
            all_measurements_df.to_csv(averages_output_path_prefix + measurements_type + "_averages.csv")

            master_dict[sample][timepoint][measurements_type] = all_measurements_df

            reps_list = list(all_reps_raw_data[measurements_type].columns)

            all_reps_raw_data[measurements_type]['average'] = all_reps_raw_data[measurements_type].mean(axis=1)
            all_reps_raw_data[measurements_type]['std dev'] = all_reps_raw_data[measurements_type].std(axis=1)
            all_reps_raw_data[measurements_type].to_csv(averages_output_path_prefix + measurements_type + "_trace.csv")

            plots.save_allreps_plots(averages_output_path_prefix + measurements_type,
                                     all_reps_raw_data[measurements_type], reps_list,
                                     xlim=all_measurements_types[measurements_type][2],
                                     ylim=all_measurements_types[measurements_type][3],
                                     ignore_index=all_measurements_types[measurements_type][4])

# generate master dataframe containing all measurements
master_df = parse_math.build_master_df(master_dict, all_samples, all_timepoints, all_measurements_types)

if not os.path.isdir(root_master_plots_folder):
    os.makedirs(root_master_plots_folder)

master_df.to_csv(root_master_folder + '/' + 'master_calc_values.csv')

plots.save_calc_values_plots(master_df, root_master_plots_folder)

plot_flr_meas_timepoint.save_flr_measurement_plot(master_df, root_master_folder,
                                                  figure_rows=all_timepoints, figure_columns=all_samples)