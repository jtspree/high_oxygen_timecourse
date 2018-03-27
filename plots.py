"""
INFO

Plot functions
"""

# LIBRARY

import matplotlib.pyplot as plt

# FUNCTIONS

def save_ECS_DIRK_plot(DestinationFolder, ECS_DIRK_data, mean):
    fig = plt.figure(1, figsize=(8, 6))
    ax = fig.add_subplot(1, 1, 1)
    x = ECS_DIRK_data['x_correct']
    y1 = ECS_DIRK_data['y_correct']
    y2 = ECS_DIRK_data['y_initial']
    y3 = mean * x + ECS_DIRK_data['y_initial'][0]
    y4 = ECS_DIRK_data['amplitude']
    ax.set_ylim(-0.0008, 0.0008)
    plt.plot(x, y1, label='ECS')
    plt.plot(x, y2, label='y_initial')
    plt.plot(x, y3, label='slope')
    plt.plot(x, y4, label='amplitude')
    plt.legend()
    plt.savefig(DestinationFolder + "/"+ "ECS_figure.png")
    # plt.show()
    plt.clf()