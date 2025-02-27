"""
Last Updated: 16-01-2025
Author: Peter Rock <peter@mggg.org>

This file contains many helper functions that are used to generate the boxplots
in this paper.
"""

import numpy as np


def find_median(arr, wts):
    """
    Finds the median of a weighted array. That is, given an array of values, and
    an array of weights representing the number of times each value should be
    repeated, this function then finds the median value of the array of values
    with the appropriate repeat counts.

    For example, if the array of values is
    [1, 2, 3, 4]
    and the array of weights is
    [4, 3, 2, 1]

    then the median value is the median of the array
    [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]
    which is 2.


    Parameters
    ----------
    arr : array-like
        The array of values to find the median of.
    wts : array-like
        The array of weights to use when finding the median.

    Returns:
    --------
    (float, int, float):
        (the actual median of the weighted array,
         the index of the median value in passed array `arr`,
         the location of the median value in the array of repeated values)
    """
    cum_wts = [0] + list(np.cumsum(wts))
    total_sum = cum_wts[-1]
    median_location = (total_sum - 1) / 2

    for i in range(len(wts) - 1):
        if cum_wts[i] == median_location:
            return arr[i], i, median_location

        if cum_wts[i] < median_location < cum_wts[i + 1]:
            if median_location == cum_wts[i + 1] - 0.5:
                return (arr[i] + arr[i + 1]) / 2, i + 0.5, median_location
            else:
                return arr[i], i, median_location

    return arr[-1], len(arr) - 1, median_location


def get_weighted_stats(array, weights):
    """
    Finds the q1, median, and q3 of a weighted array. That is, given an array of
    values, and an array of weights representing the number of times each value should
    be repeated, this function then finds the q1, median, and q3 of the array of values
    with the appropriate repeat counts.

    For example, if the array of values is
    [1, 2, 3, 4]
    and the array of weights is
    [4, 3, 2, 1]

    then the repeated array that the statistics are computed from is
    [1, 1, 1, 1, 2, 2, 2, 3, 3, 4]


    Parameters
    ----------
    arr : array-like
        The array of values to find the median of.
    wts : array-like
        The array of weights to use when finding the median.

    Returns:
    --------
    (float, int, float):
        (the first quartile of the weighted array,
         the median of the weighted array,
         the third quartile of the weighted array)
    """
    arg_order = np.argsort(array)
    sorted_array = array[arg_order]
    sorted_weights = weights[arg_order]
    cumsum_weights = list(np.cumsum(sorted_weights))

    med, med_idx, med_loc = find_median(sorted_array, sorted_weights)

    int_med_idx = int(med_idx)
    q1_arr = sorted_array[:int_med_idx]
    q1_wts = sorted_weights[:int_med_idx]
    q1_remainder = int(med_loc + 0.5) - np.sum(q1_wts)

    if q1_remainder > 0:
        q1_arr = np.append(q1_arr, sorted_array[int_med_idx])
        q1_wts = np.append(q1_wts, q1_remainder)

    q3_pos_0_count = cumsum_weights[int_med_idx] - int(med_loc) - 1
    if q3_pos_0_count > 0:
        q3_arr = sorted_array[int_med_idx:]
        q3_wts = sorted_weights[int_med_idx:]
        q3_wts[0] = q3_pos_0_count

    else:
        q3_arr = sorted_array[int_med_idx + 1 :]
        q3_wts = sorted_weights[int_med_idx + 1 :]

    q1, _, _ = find_median(q1_arr, q1_wts)
    q3, _, _ = find_median(q3_arr, q3_wts)
    return q1, med, q3


def weighted_quantile(
    values, quantiles, sample_weight=None, values_sorted=False, old_style=False
):
    """
    Compute weighted quantiles of a given sample.

    Parameters
    ----------
    values : array-like
        The data.
    quantiles : array-like
        The quantiles to compute, must be between 0 and 1.
    sample_weight : array-like, optional
        Weights for each value in `values`.
        If None, all weights are equal.
    values_sorted : bool, optional
        If True, `values` and `sample_weight` are assumed to be sorted by `values`.
    old_style : bool, optional
        If True, matches numpy.percentile's behavior.
        If False, quantiles are defined as the smallest value v such that P(X <= v) >= quantile.

    Returns
    -------
    np.ndarray
        The computed quantiles.
    """
    values = np.array(values)
    quantiles = np.array(quantiles, dtype=float)
    if sample_weight is None:
        sample_weight = np.ones(len(values))
    sample_weight = np.array(sample_weight, dtype=float)

    assert np.all(quantiles >= 0) and np.all(
        quantiles <= 1
    ), "quantiles should be in [0, 1]"

    if not values_sorted:
        # Sort by values
        sorter = np.argsort(values)
        values = values[sorter]
        sample_weight = sample_weight[sorter]

    # Compute the cumulative sum of weights as a proportion of the total weight
    cumulative_weights = np.cumsum(sample_weight)
    cumulative_weights /= cumulative_weights[-1]

    # Interpolate to find the quantile values
    return np.interp(quantiles, cumulative_weights, values)
