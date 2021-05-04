import csv
import random
import time
from datetime import datetime
from pathlib import Path

import geopandas
import requests.exceptions
from matplotlib import pyplot as plt
from requests import request
from tqdm import tqdm

import switzerland_db


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
    url = 'https://{}.impfung-covid.ch/'
    for canton in tqdm(cantons, desc='http request'):
        canton_url = url.format(canton)
        try:
            if request('GET', canton_url).__str__() == '<Response [200]>':
                cantons[canton]['uses_site'] = True
        except requests.exceptions.ConnectionError:
            cantons[canton]['uses_site'] = False
        wait_time = random.randint(3, 8)
        time.sleep(wait_time)

    # plot the reaults
    fig, ax = plt.subplots(figsize=(16, 9))

    for canton in tqdm(cantons, desc='plot cantons'):
        if cantons[canton]['uses_site']:
            color = 'green'
        else:
            color = 'red'
        cantons[canton]['df'].plot(ax=ax, color=color, edgecolor='white')

    # format figure
    ax.set_title('Usage of https://<canton>.impfung-covid.ch/', fontsize=32, fontweight='bold')
    fig.patch.set_visible(False)
    ax.axis('off')
    fig.show()

    # export figure
    fig.savefig(file_path / 'switzerland_impfung_covid_usage.pdf')
    fig.savefig(file_path / 'switzerland_impfung_covid_usage.svg')
    fig.savefig(file_path / 'switzerland_impfung_covid_usage.png', dpi=150)

    # logging the data
    log = [str(cantons[key]['uses_site']) for key in cantons]
    log = [datetime.now().strftime('%d %b %Y %H:%M'), *log]

    with open(csv_path, 'a+', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(log)


if __name__ == '__main__':
    main()
