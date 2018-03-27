"""
INFO
"""

# LIBRARY

import pandas as pd

# FUNCTION

def parse_ECS_data(FilePath, ECS_DIRK_filename, DestinationFolder):
    ECS_DIRK_data = pd.read_table(FilePath + ECS_DIRK_filename, header=None)
    ECS_DIRK_data.columns = ["Time", "Fluorescence", "Reference", "Delta"]
    ECS_DIRK_data = ECS_DIRK_data[[0, 3]]
    ECS_DIRK_data = pd.DataFrame(ECS_DIRK_data)
    ECS_DIRK_data['x_correct'] = ECS_DIRK_data['Time'] - ECS_DIRK_data['Time'][249]
    ECS_DIRK_data['y_correct'] = ECS_DIRK_data['Delta'] - ECS_DIRK_data['Delta'][249]
    ECS_DIRK_data['y_initial'] = ECS_DIRK_data['y_correct'].iloc[240:249].mean(axis=0)
    ECS_DIRK_data['amplitude'] = ECS_DIRK_data['y_correct'].iloc[470:495].mean(axis=0)

    ECS_DIRK_data.to_csv(DestinationFolder + "/" + "ECS_raw.csv")
    return ECS_DIRK_data


def ECS_rates_calculator(ECS_DIRK_data, DestinationFolder):
    df = pd.DataFrame(columns=['x_initial', 'x_final', 'y_initial', 'y_final'])
    for x in range(10, 20):
        rates_dict = {}
        rates_dict['x_initial'] = ECS_DIRK_data['x_correct'][249]
        rates_dict['x_final'] = ECS_DIRK_data['x_correct'][250 + x]
        rates_dict['y_initial'] = ECS_DIRK_data['y_correct'].iloc[240:249].mean(axis=0)
        rates_dict['y_final'] = ECS_DIRK_data['y_correct'].iloc[249 + x:251 + x].mean(axis=0)
        df = df.append(rates_dict, ignore_index=True)

    df['Rate'] = (df['y_final'] - df['y_initial']) / (df['x_final'] - df['x_initial'])
    df.to_csv(DestinationFolder + "/" + "slope_rates.csv")

    values = pd.DataFrame(columns=['rates_mean', 'rates_std_dev', 'end_trace_mean', 'end_trace_std_dev', 'y_initial', 'amplitude'])

    values_dict = {}
    values_dict['rates_mean'] = df['Rate'].mean()
    values_dict['rates_std_dev'] = df['Rate'].std()
    values_dict['end_trace_mean'] = ECS_DIRK_data['y_correct'].iloc[470:495].mean(axis=0)
    values_dict['end_trace_std_dev'] = ECS_DIRK_data['y_correct'].iloc[470:495].std(axis=0)
    values_dict['y_initial'] = ECS_DIRK_data['y_correct'].iloc[240:249].mean(axis=0)
    values_dict['amplitude'] = values_dict['y_initial'] - values_dict['end_trace_mean']
    values = values.append(values_dict, ignore_index=True)
    values.to_csv(DestinationFolder + "/" + "ECS_values.csv")

    mean = df['Rate'].mean()
    std_dev = df['Rate'].std()
    return df, values, mean, std_dev