import csv
import random
import time
from datetime import datetime
from pathlib import Path

import geopandas
from matplotlib import pyplot as plt
from tqdm import tqdm

import python_tools as pt
import switzerland_db

# if True neither checks the websites nor logs the data
debug_mode = False


def main():
    # dictionary containing the cantons of switzerland
    cantons = switzerland_db.CANTONS_OF_SWITZERLAND

    # path of this file
    file_path = Path(__file__).parent

    # csv file for logging the data over time
    csv_path = file_path / 'usage_over_time.csv'

    # geo data files
    filename = 'swissBOUNDARIES3D_1_3_TLM_KANTONSGEBIET.'
    geo_data_files = {key: file_path / (filename + key) for key in ['shx', 'shp', 'dbf', 'cpg', 'prj']}

    # Check if required exist
    for file in geo_data_files:
        if not geo_data_files[file].exists():
            raise Exception('The file ' + geo_data_files[file].__str__() + ' doesn\'t exist!\n'
                            + '-> You can download it from:\n'
                              '-> https://www.swisstopo.admin.ch/de/geodata/landscape/boundaries3d.html#download')

    switzerland_df = geopandas.read_file(geo_data_files['shp'])

    for canton in tqdm(cantons, desc='extract cantons'):
        cantons[canton]['df'] = switzerland_df[switzerland_df['NAME'] == cantons[canton]['name']]

    # test homepage
    if not debug_mode:
        for canton in tqdm(cantons, desc='http request'):
            cantons[canton]['uses_site'] = pt.is_page_up(f'https://{canton}.impfung-covid.ch/')
            wait_time = random.randint(3, 8)
            time.sleep(wait_time)

    # plot the results
    fig, ax = plt.subplots(figsize=(16, 9))

    for canton in tqdm(cantons, desc='plot cantons'):
        if cantons[canton]['uses_site']:
            color = 'green'
        else:
            color = 'red'
        cantons[canton]['df'].plot(ax=ax, color=color, edgecolor='white')

    # format figure
    bbox = dict(boxstyle='round', facecolor='white', alpha=0.6)
    ax.set_title('Usage of https://<canton>.impfung-covid.ch/', fontsize=32,
                 fontweight='bold', bbox=bbox)
    fig.patch.set_visible(False)
    ax.axis('off')

    # Add reference
    ax.text(0.9, 0, 'geographical data by:\n©swisstopo', transform=ax.transAxes,
            fontsize=14, verticalalignment='bottom', horizontalalignment='center', bbox=bbox)

    fig.show()

    # export figure
    fig.savefig(file_path / 'switzerland_impfung_covid_usage.pdf')
    fig.savefig(file_path / 'switzerland_impfung_covid_usage.svg')
    fig.savefig(file_path / 'switzerland_impfung_covid_usage.png', dpi=150)

    # logging the data
    if not debug_mode:
        log = [str(cantons[key]['uses_site']) for key in cantons]
        log = [datetime.now().strftime('%d %b %Y %H:%M'), *log]

        with open(csv_path, 'a+', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(log)


if __name__ == '__main__':
    main()
