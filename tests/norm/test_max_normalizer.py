#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: BSD-3 (https://tldrlegal.com/license/bsd-3-clause-license-(revised))
# Copyright (c) 2016-2021, Cabral, Juan; Luczywo, Nadia
# All rights reserved.

# =============================================================================
# DOCS
# =============================================================================

"""test for skcriteria.norm.max_normalizer

"""


# =============================================================================
# IMPORTS
# =============================================================================

import numpy as np

import skcriteria
from skcriteria.norm import max_normalizer


# =============================================================================
# TEST CLASSES
# =============================================================================


def test_MaxNormalizer_simple_matrix():

    dm = skcriteria.mkdm(
        matrix=[[1, 2, 3], [4, 5, 6]],
        objectives=[min, max, min],
        weights=[1, 2, 3],
    )

    expected = skcriteria.mkdm(
        matrix=[[1 / 4, 2 / 5, 3 / 6], [4 / 4, 5 / 5, 6 / 6]],
        objectives=[min, max, min],
        weights=[1, 2, 3],
        dtypes=[float, float, float],
    )

    normalizer = max_normalizer.MaxNormalizer(normalize_for="matrix")

    result = normalizer.normalize(dm)

    assert result.equals(expected)


def test_MaxNormalizer_matrix(decision_matrix):

    dm = decision_matrix(
        seed=42,
        min_alternatives=10,
        max_alternatives=10,
        min_criteria=20,
        max_criteria=20,
        min_objectives_proportion=0.5,
    )

    expected = skcriteria.mkdm(
        matrix=dm.matrix / np.max(dm.matrix, axis=0, keepdims=True),
        objectives=dm.objectives,
        weights=dm.weights,
        anames=dm.anames,
        cnames=dm.cnames,
        dtypes=dm.dtypes,
    )

    normalizer = max_normalizer.MaxNormalizer(normalize_for="matrix")
    result = normalizer.normalize(dm)

    assert result.equals(expected)


def test_MaxNormalizer_simple_weights():

    dm = skcriteria.mkdm(
        matrix=[[1, 2, 3], [4, 5, 6]],
        objectives=[min, max, min],
        weights=[1, 2, 3],
    )

    expected = skcriteria.mkdm(
        matrix=[[1, 2, 3], [4, 5, 6]],
        objectives=[min, max, min],
        weights=[1 / 3, 2 / 3, 3 / 3],
        dtypes=[int, int, int],
    )

    normalizer = max_normalizer.MaxNormalizer(normalize_for="weights")

    result = normalizer.normalize(dm)

    assert result.equals(expected)


def test_MaxNormalizer_weights(decision_matrix):

    dm = decision_matrix(
        seed=42,
        min_alternatives=10,
        max_alternatives=10,
        min_criteria=20,
        max_criteria=20,
        min_objectives_proportion=0.5,
    )

    expected = skcriteria.mkdm(
        matrix=dm.matrix,
        objectives=dm.objectives,
        weights=dm.weights / np.max(dm.weights),
        anames=dm.anames,
        cnames=dm.cnames,
        dtypes=dm.dtypes,
    )

    normalizer = max_normalizer.MaxNormalizer(normalize_for="weights")
    result = normalizer.normalize(dm)

    assert result.equals(expected)


def test_MaxNormalizer_simple_both():

    dm = skcriteria.mkdm(
        matrix=[[1, 2, 3], [4, 5, 6]],
        objectives=[min, max, min],
        weights=[1, 2, 3],
    )

    expected = skcriteria.mkdm(
        matrix=[[1 / 4, 2 / 5, 3 / 6], [4 / 4, 5 / 5, 6 / 6]],
        objectives=[min, max, min],
        weights=[1 / 3, 2 / 3, 3 / 3],
        dtypes=[float, float, float],
    )

    normalizer = max_normalizer.MaxNormalizer(normalize_for="both")

    result = normalizer.normalize(dm)

    assert result.equals(expected)


def test_MaxNormalizer_both(decision_matrix):

    dm = decision_matrix(
        seed=42,
        min_alternatives=10,
        max_alternatives=10,
        min_criteria=20,
        max_criteria=20,
        min_objectives_proportion=0.5,
    )

    expected = skcriteria.mkdm(
        matrix=dm.matrix / np.max(dm.matrix, axis=0, keepdims=True),
        objectives=dm.objectives,
        weights=dm.weights / np.max(dm.weights),
        anames=dm.anames,
        cnames=dm.cnames,
        dtypes=dm.dtypes,
    )

    normalizer = max_normalizer.MaxNormalizer(normalize_for="both")
    result = normalizer.normalize(dm)

    assert result.equals(expected)


# =============================================================================
# TEST FUNCTIONS
# =============================================================================


def test_max_norm_mtx(decision_matrix):

    dm = decision_matrix(
        min_alternatives=10,
        max_alternatives=10,
        min_criteria=20,
        max_criteria=20,
        min_objectives_proportion=1.0,
    )

    nweights = max_normalizer.max_norm(dm.weights, axis=0)
    expected = dm.weights / np.max(dm.weights)

    assert np.all(nweights == expected)


def test_max_norm_weights(decision_matrix):

    dm = decision_matrix(
        min_alternatives=10,
        max_alternatives=10,
        min_criteria=20,
        max_criteria=20,
        min_objectives_proportion=1.0,
    )

    nmtx = max_normalizer.max_norm(dm.matrix, axis=0)
    expected = dm.matrix / np.max(dm.matrix, axis=0, keepdims=True)

    assert np.all(nmtx == expected)
