# -*- coding:UTF-8 -*-
__copyright__ = "Tongji University"

import numpy as np
import pandas as pd
import sys


def format_check(result_file_path, result_file_sample):
    """
    :param result_file_path: path to result file
    :param result_file_sample: path to sample result file
    :return: true or false represent if the result pass the format check
    """
    try:
        sample = pd.read_csv(result_file_sample, comment=';', header=None, names=['id', 'x', 'y', 'z'])
        result = pd.read_csv(result_file_path, comment=';', header=None, names=['id', 'x', 'y', 'z'])
        assert sample.shape == result.shape, 'Result dimension mismatch!'
        difference = np.sum(sample['id'] != result['id'])
        assert difference == 0, 'Directory value mismatch!'
        assert not (result.isnull().any().any()), 'Somewhere is null!'
    except Exception as e:
        print('Exception: ', e)
        return False
    return True


def main(argv):
    if len(argv) != 3:
        print('Usage: python3 result_format.py [path to your result] [path to sample result]')
        return
    if format_check(argv[1], argv[2]):
        print('Format check succeed!')
    else:
        print('Format check failed')


if __name__ == '__main__':
    main(sys.argv)




