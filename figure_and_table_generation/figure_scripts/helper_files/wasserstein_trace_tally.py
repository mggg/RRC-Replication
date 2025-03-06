"""
Last Updated: 16-01-2025
Author: Peter Rock <peter@mggg.org>

Thsi file contains functions that are used to compute the Wasserstein trace between
two ensembles of maps.
"""

from collections import Counter, defaultdict
from scipy.stats import wasserstein_distance
from tqdm import tqdm
import numpy as np


def wasserstein_trace(counts1, counts2, weights1, weights2, resolution):
    """
    Computes the ongoing Wasserstein trace between two ensembles of maps. That is,
    given two arrays of length n, and a resolution r, this function computes the
    Wasserstein distance between the two arrays every r steps.

    Parameters
    ----------
    counts1 : array-like
        The first array of counts.
    counts2 : array-like
        The second array of counts.
    weights1 : array-like
        The weights of the first array of counts.
    weights2 : array-like
        The weights of the second array of counts.
    resolution : int
        The resolution of the trace.

    Returns
    -------
    (array-like, array-like):
        The xticks for use in plotting and the trace of the Wasserstein distances.
    """
    xticks = []
    trace = []
    hist1 = Counter()
    hist2 = Counter()
    for step, (c1, c2, w1, w2) in enumerate(
        tqdm(zip(counts1, counts2, weights1, weights2), total=len(counts1)),
    ):
        hist1[c1] += w1
        hist2[c2] += w2
        if step > 0 and step % resolution == 0:
            distance = wasserstein_distance(
                list(hist1.keys()),
                list(hist2.keys()),
                list(hist1.values()),
                list(hist2.values()),
            )
            xticks.append(step)
            trace.append(distance)
    return xticks, trace


def wasserstein_trace_ground_truth(
    counts, ref_counts, weights, ref_weights, resolution
):
    """
    Computes the Wasserstein trace between a reference ensemble and an ongoing ensemble.
    That is, given a reference array of counts and weights which generates some distribution,
    and some ongoing array of counts and weights, the Wasserstein trace contains the Wasserstein
    between the ongoing distribution and the totality of the reference distribution at each step
    equal to the resolution.

    Parameters
    ----------
    counts : array-like
        The array of counts for the ongoing ensemble.
    ref_counts : array-like
        The array of counts for the reference ensemble.
    weights : array-like
        The weights for the ongoing ensemble.
    ref_weights : array-like
        The weights for the reference ensemble.
    resolution : int
        The resolution of the trace.

    Returns
    -------
    (array-like, array-like):
        The xticks for use in plotting and the trace of the Wasserstein distances.
    """
    xticks = []
    trace = []
    hist = Counter()
    for step, (c, w) in enumerate(tqdm(zip(counts, weights), total=len(counts))):
        # We assume 1-indexed districts.
        hist[c] += w
        if step > 0 and step % resolution == 0:
            distance = wasserstein_distance(
                list(hist.keys()), ref_counts, list(hist.values()), ref_weights
            )
            xticks.append(step)
            trace.append(distance)
    return xticks, trace


def wasserstein_trace_v_full(
    shares_df, full_df, weights, weights_full, resolution=10_000
):
    """
    Computes the Wasserstein trace between a full ensemble and an ongoing ensemble.
    That is, given a full dataframe of counts and weights which generates some distribution,
    and some ongoing array of counts and weights, the Wasserstein trace contains the Wasserstein
    between the ongoing distribution and the totality of the full distribution at each step
    equal to the resolution.

    Parameters
    ----------
    shares_df : pandas.DataFrame
        The dataframe of shares for the ongoing ensemble.
    full_df : pandas.DataFrame
        The dataframe of shares for the full ensemble.
    weights : pandas.Series
        The weights for the ongoing ensemble.
    weights_full : pandas.Series
        The weights for the full ensemble.
    resolution : int
        The resolution of the trace.

    Returns
    -------
    (array-like, array-like):
        The xticks for use in plotting and the trace of the Wasserstein distances.
    """
    assert all(shares_df.columns == full_df.columns)

    shares1 = shares_df.sort_index(axis=1).to_numpy()
    shares2 = full_df.sort_index(axis=1).to_numpy()

    n_districts = len(shares1[0])

    assert len(shares1[0]) == len(shares2[0])
    state1 = np.zeros(n_districts)
    state2 = np.zeros(n_districts)
    xticks = []
    trace = []
    hist1 = [Counter() for _ in range(n_districts)]
    hist2 = [Counter() for _ in range(n_districts)]

    for s2, w2 in zip(shares2, weights_full):
        for dist, v in enumerate(s2):
            state2[dist] = v
        for k, v in enumerate(sorted(state2)):
            hist2[k][v] += w2

    for step, (s1, w1) in enumerate(
        tqdm(zip(shares1, weights), total=shares1.shape[0])
    ):
        # We assume 1-indexed districts.
        for dist, v in enumerate(s1):
            state1[dist] = v
        for k, v in enumerate(sorted(state1)):
            hist1[k][v] += w1
        if step > 0 and step % resolution == 0:
            distance = 0
            for dist1, dist2 in zip(hist1, hist2):
                distance += wasserstein_distance(
                    list(dist1.keys()),
                    list(dist2.keys()),
                    list(dist1.values()),
                    list(dist2.values()),
                )
            xticks.append(step)
            trace.append(distance)
    return xticks, trace


def wasserstein_trace_shares(shares1_df, shares2_df, weights1, weights2, resolution):
    """
    Computes the Wasserstein trace between a full ensemble and an ongoing ensemble.
    That is, given a full dataframe of counts and weights which generates some distribution,
    and some ongoing array of counts and weights, the Wasserstein trace contains the Wasserstein
    between the ongoing distribution and the totality of the full distribution at each step
    equal to the resolution.

    Parameters
    ----------
    shares_df : pandas.DataFrame
        The dataframe of shares for the ongoing ensemble.
    full_df : pandas.DataFrame
        The dataframe of shares for the full ensemble.
    weights : pandas.Series
        The weights for the ongoing ensemble.
    weights_full : pandas.Series
        The weights for the full ensemble.
    resolution : int
        The resolution of the trace.

    Returns
    -------
    (array-like, array-like):
        The xticks for use in plotting and the trace of the Wasserstein distances.
    """
    assert all(shares1_df.columns == shares2_df.columns)

    shares1 = shares1_df.sort_index(axis=1).to_numpy()
    shares2 = shares2_df.sort_index(axis=1).to_numpy()

    n_districts = len(shares1[0])

    assert shares1_df.shape == shares2_df.shape

    state1 = np.zeros(n_districts)
    state2 = np.zeros(n_districts)
    xticks = []
    trace = []
    hist1 = [Counter() for _ in range(n_districts)]
    hist2 = [Counter() for _ in range(n_districts)]

    for step, (s1, w1, s2, w2) in enumerate(
        tqdm(zip(shares1, weights1, shares2, weights2), total=shares1.shape[0])
    ):
        # We assume 1-indexed districts.
        for dist, v in enumerate(s1):
            state1[dist] = v
        for k, v in enumerate(sorted(state1)):
            hist1[k][v] += w1
        for dist, v in enumerate(s2):
            state2[dist] = v
        for k, v in enumerate(sorted(state2)):
            hist2[k][v] += w2
        if step > 0 and step % resolution == 0:
            distance = 0
            for dist1, dist2 in zip(hist1, hist2):
                distance += wasserstein_distance(
                    list(dist1.keys()),
                    list(dist2.keys()),
                    list(dist1.values()),
                    list(dist2.values()),
                )
            xticks.append(step)
            trace.append(distance)
    return xticks, trace


def wasserstein_trace_shares(shares1_df, shares2_df, weights1, weights2, resolution):
    """
    Computes the Wasserstein trace between a full ensemble and an ongoing ensemble.
    """
    # Ensure that the dataframes have the same columns
    assert all(shares1_df.columns == shares2_df.columns)

    # Convert dataframes to numpy arrays (columns sorted)
    shares1 = shares1_df.sort_index(axis=1).to_numpy()
    shares2 = shares2_df.sort_index(axis=1).to_numpy()

    n_districts = shares1.shape[1]
    assert shares1_df.shape == shares2_df.shape

    xticks = []
    trace = []
    # Initialize a counter per district for each ensemble
    hist1 = [Counter() for _ in range(n_districts)]
    hist2 = [Counter() for _ in range(n_districts)]

    for step, (s1, w1, s2, w2) in enumerate(
        tqdm(zip(shares1, weights1, shares2, weights2), total=shares1.shape[0])
    ):
        # Directly sort the current row using NumPy
        sorted_s1 = np.sort(s1)
        for k, v in enumerate(sorted_s1):
            hist1[k][v] += w1

        sorted_s2 = np.sort(s2)
        for k, v in enumerate(sorted_s2):
            hist2[k][v] += w2

        # Compute the Wasserstein trace at the specified resolution
        if step > 0 and step % resolution == 0:
            distance = sum(
                wasserstein_distance(
                    list(dist1.keys()),
                    list(dist2.keys()),
                    list(dist1.values()),
                    list(dist2.values()),
                )
                for dist1, dist2 in zip(hist1, hist2)
            )
            xticks.append(step)
            trace.append(distance)

    return xticks, trace
