import argparse

import numpy as np
from matplotlib import pyplot as plt

import config
from datasets.dataset import Dataset
from datasets.dataset_torch import TorchDatasetWrapper
from models.process_based.chill_hours import LocalChillHoursModel
from models.process_based.utah_chill import LocalUtahChillModel
from runs.args_util.args_dataset import configure_argparser_dataset, get_configured_dataset

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    configure_argparser_dataset(parser)
    args = parser.parse_args()

    args.seed = 31
    args.locations = 'japan_wo_okinawa'

    model_cls_1 = LocalChillHoursModel
    model_cls_2 = LocalUtahChillModel

    model_name_1 = model_cls_1.__name__ + '_japan_wo_okinawa_seed_31'
    model_name_2 = model_cls_2.__name__ + '_japan_wo_okinawa_seed_31'

    # model_1 = model_cls_1.load(model_name_1)
    # model_2 = model_cls_2.load(model_name_2)

    model_1 = model_cls_1.load(model_cls_1.__name__)  # TODO -- using model name
    model_2 = model_cls_2.load(model_cls_2.__name__)

    dataset, _ = get_configured_dataset(args)

    bloom_ixs_true = list()
    bloom_ixs_pred_m1 = list()
    bloom_ixs_pred_m2 = list()
    chill_ixs_pred_m1 = list()
    chill_ixs_pred_m2 = list()

    for x in dataset.get_test_data():

        bloom_ix_pred_m1, _, info_m1 = model_1.predict_ix(x)
        bloom_ix_pred_m2, _, info_m2 = model_2.predict_ix(x)

        chill_ix_pred_m1 = info_m1['ix_chill']
        chill_ix_pred_m2 = info_m2['ix_chill']

        bloom_ixs_true.append(x['bloom_ix'])

        bloom_ixs_pred_m1.append(bloom_ix_pred_m1)
        bloom_ixs_pred_m2.append(bloom_ix_pred_m2)

        chill_ixs_pred_m1.append(chill_ix_pred_m1)
        chill_ixs_pred_m2.append(chill_ix_pred_m2)

    fn = 'plot_pb_chill_requirement_scatter.png'

    fig, ax = plt.subplots()

    ax.plot(np.arange(0, 200), np.arange(0, 200), '--', color='grey')

    ax.scatter([Dataset.index_to_doy(ix) for ix in bloom_ixs_pred_m1],
               [Dataset.index_to_doy(ix) for ix in bloom_ixs_pred_m2],
               c='red',
               label=f'Bloom DOY',
               s=3,
               alpha=0.3,
               )

    ax.scatter([Dataset.index_to_doy(ix) for ix in chill_ixs_pred_m1],
               [Dataset.index_to_doy(ix) for ix in chill_ixs_pred_m2],
               c='blue',
               label=f'Chill DOY',
               s=3,
               alpha=0.3,
               )

    ax.set_xlabel('DOY (Chill Hours Model)')
    ax.set_ylabel('DOY (Utah Chill Model)')

    # ax.set_xlim(0, 200)
    # ax.set_ylim(0, 200)

    plt.legend()

    plt.savefig(fn)

    plt.cla()
    plt.close()
