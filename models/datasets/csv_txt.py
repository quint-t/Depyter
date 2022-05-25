# template-name: CSV/TXT
# template-type: Файл
# <code-block> Load dataset from CSV/TXT file

import pandas as pd

train_data = pd.read_csv(filepath_or_buffer, sep=pd.NoDefault.no_default, delimiter=None, header='infer',
                         names=pd.NoDefault.no_default, index_col=None, usecols=None, squeeze=None,
                         prefix=pd.NoDefault.no_default, mangle_dupe_cols=True, dtype=None, engine=None,
                         converters=None, true_values=None, false_values=None, skipinitialspace=False, skiprows=None,
                         skipfooter=0, nrows=None, na_values=None, keep_default_na=True, na_filter=True, verbose=False,
                         skip_blank_lines=True, parse_dates=None, infer_datetime_format=False, keep_date_col=False,
                         date_parser=None, dayfirst=False, cache_dates=True, iterator=False, chunksize=None,
                         compression='infer', thousands=None, decimal='.', lineterminator=None, quotechar='"',
                         quoting=0, doublequote=True, escapechar=None, comment=None, encoding=None,
                         encoding_errors='strict', dialect=None, error_bad_lines=None, warn_bad_lines=None,
                         on_bad_lines=None, delim_whitespace=False, low_memory=True, memory_map=False,
                         float_precision=None, storage_options=None)
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html


import numpy as np

test_data = np.genfromtxt(filepath, dtype=float, comments='#', delimiter=None, skip_header=0, skip_footer=0,
                          converters=None, missing_values=None, filling_values=None, usecols=None, names=None,
                          excludelist=None, deletechars=" !#$%&'()*+, -./:;<=>?@[\\]^{|}~",
                          replace_space='_', autostrip=False, case_sensitive=True, defaultfmt='f%i', unpack=None,
                          usemask=False, loose=True, invalid_raise=True, max_rows=None, encoding='bytes', like=None)
