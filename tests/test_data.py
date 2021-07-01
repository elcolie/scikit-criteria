#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: BSD-3 (https://tldrlegal.com/license/bsd-3-clause-license-(revised))
# Copyright (c) 2016-2021, Cabral, Juan; Luczywo, Nadia
# All rights reserved.

# =============================================================================
# DOCS
# =============================================================================

"""test for skcriteria.data

"""


# =============================================================================
# IMPORTS
# =============================================================================

import numpy as np

import pandas as pd

import pytest

from skcriteria import data


# =============================================================================
# HELPER
# =============================================================================


def construct_objectives_values(arr):
    return [data.Objective.construct_from_alias(obj).value for obj in arr]


def construct_objectives(arr):
    return [data.Objective.construct_from_alias(obj) for obj in arr]


# =============================================================================
# ENUM
# =============================================================================


def test_objective_construct():
    for alias in data.Objective._MAX_ALIASES.value:
        objective = data.Objective.construct_from_alias(alias)
        assert objective is data.Objective.MAX
    for alias in data.Objective._MIN_ALIASES.value:
        objective = data.Objective.construct_from_alias(alias)
        assert objective is data.Objective.MIN
    with pytest.raises(ValueError):
        data.Objective.construct_from_alias("no anda")


def test_objective_str():
    assert str(data.Objective.MAX) == data.Objective.MAX.name
    assert str(data.Objective.MIN) == data.Objective.MIN.name


def test_objective_to_string():
    assert data.Objective.MAX.to_string() == data.Objective._MAX_STR.value
    assert data.Objective.MIN.to_string() == data.Objective._MIN_STR.value


# =============================================================================
# MUST WORK
# =============================================================================


def test_simple_creation(data_values):

    mtx, objectives, weights, anames, cnames = data_values(seed=42)

    dm = data.mkdm(
        matrix=mtx,
        objectives=objectives,
        weights=weights,
        anames=anames,
        cnames=cnames,
    )

    np.testing.assert_array_equal(dm.matrix, mtx)
    np.testing.assert_array_equal(
        dm.objectives_values, construct_objectives_values(objectives)
    )
    np.testing.assert_array_equal(
        dm.objectives, construct_objectives(objectives)
    )
    np.testing.assert_array_equal(dm.weights, weights)
    np.testing.assert_array_equal(dm.anames, anames)
    np.testing.assert_array_equal(dm.cnames, cnames)
    np.testing.assert_array_equal(dm.dtypes, [np.float64] * len(cnames))


def test_no_provide_weights(data_values):
    mtx, objectives, _, anames, cnames = data_values(seed=42)

    dm = data.mkdm(
        matrix=mtx,
        objectives=objectives,
        anames=anames,
        cnames=cnames,
    )

    weights = np.ones(len(dm.objectives))

    np.testing.assert_array_equal(dm.matrix, mtx)
    np.testing.assert_array_equal(
        dm.objectives_values, construct_objectives_values(objectives)
    )
    np.testing.assert_array_equal(
        dm.objectives, construct_objectives(objectives)
    )
    np.testing.assert_array_equal(dm.weights, weights)
    np.testing.assert_array_equal(dm.anames, anames)
    np.testing.assert_array_equal(dm.cnames, cnames)


def test_no_provide_anames(data_values):

    mtx, objectives, weights, _, cnames = data_values(seed=42)

    dm = data.mkdm(
        matrix=mtx,
        objectives=objectives,
        weights=weights,
        cnames=cnames,
    )

    anames = [f"A{idx}" for idx in range(mtx.shape[0])]

    np.testing.assert_array_equal(dm.matrix, mtx)
    np.testing.assert_array_equal(
        dm.objectives_values, construct_objectives_values(objectives)
    )
    np.testing.assert_array_equal(
        dm.objectives, construct_objectives(objectives)
    )
    np.testing.assert_array_equal(dm.weights, weights)
    np.testing.assert_array_equal(dm.anames, anames)
    np.testing.assert_array_equal(dm.cnames, cnames)


def test_no_provide_cnames(data_values):
    mtx, objectives, weights, anames, _ = data_values(seed=42)

    dm = data.mkdm(
        matrix=mtx,
        objectives=objectives,
        weights=weights,
        anames=anames,
    )

    cnames = [f"C{idx}" for idx in range(mtx.shape[1])]

    np.testing.assert_array_equal(dm.matrix, mtx)
    np.testing.assert_array_equal(
        dm.objectives_values, construct_objectives_values(objectives)
    )
    np.testing.assert_array_equal(
        dm.objectives, construct_objectives(objectives)
    )
    np.testing.assert_array_equal(dm.weights, weights)
    np.testing.assert_array_equal(dm.anames, anames)
    np.testing.assert_array_equal(dm.cnames, cnames)


def test_no_provide_cnames_and_anames(data_values):
    mtx, objectives, weights, _, _ = data_values(seed=42)

    dm = data.mkdm(
        matrix=mtx,
        objectives=objectives,
        weights=weights,
    )

    anames = [f"A{idx}" for idx in range(mtx.shape[0])]
    cnames = [f"C{idx}" for idx in range(mtx.shape[1])]

    np.testing.assert_array_equal(dm.matrix, mtx)
    np.testing.assert_array_equal(
        dm.objectives_values, construct_objectives_values(objectives)
    )
    np.testing.assert_array_equal(
        dm.objectives, construct_objectives(objectives)
    )
    np.testing.assert_array_equal(dm.weights, weights)
    np.testing.assert_array_equal(dm.anames, anames)
    np.testing.assert_array_equal(dm.cnames, cnames)


def test_copy(data_values):
    mtx, objectives, weights, anames, cnames = data_values(seed=42)

    dm = data.mkdm(
        matrix=mtx,
        objectives=objectives,
        weights=weights,
        anames=anames,
        cnames=cnames,
    )
    copy = dm.copy()

    assert dm is not copy
    assert dm == copy


def test_self_eq(data_values):
    mtx, objectives, weights, anames, cnames = data_values(seed=42)

    dm = data.mkdm(
        matrix=mtx,
        objectives=objectives,
        weights=weights,
        anames=anames,
        cnames=cnames,
    )
    same = dm

    assert dm is same
    assert dm == same


def test_self_ne(data_values):
    mtx, objectives, weights, anames, cnames = data_values(seed=42)

    dm = data.mkdm(
        matrix=mtx,
        objectives=objectives,
        weights=weights,
        anames=anames,
        cnames=cnames,
    )

    omtx, oobjectives, oweights, oanames, ocnames = data_values(seed=43)

    other = data.mkdm(
        matrix=omtx,
        objectives=oobjectives,
        weights=oweights,
        anames=oanames,
        cnames=ocnames,
    )
    assert dm != other


def test_simple_repr():

    dm = data.mkdm(
        matrix=[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        objectives=[min, max, min],
        weights=[0.1, 0.2, 0.3],
    )

    expected = (
        "   C0[\u25bc 0.1] C1[\u25b2 0.2] C2[\u25bc 0.3]\n"
        "A0         1         2         3\n"
        "A1         4         5         6\n"
        "A2         7         8         9\n"
        "[3 Alternatives x 3 Criteria]"
    )

    result = repr(dm)
    assert result == expected


def test_simple_html():
    dm = data.mkdm(
        matrix=[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        objectives=[min, max, min],
        weights=[0.1, 0.2, 0.3],
    )

    expected = """
        <div class="decisionmatrix">
            <div>
                <style scoped="">
                    .dataframe tbody tr th:only-of-type {
                        vertical-align: middle;
                    }

                    .dataframe tbody tr th {
                        vertical-align: top;
                    }

                    .dataframe thead th {
                        text-align: right;
                    }
                </style>
                <table border="1" class="dataframe">
                    <thead>
                        <tr style="text-align: right;">
                            <th/>
                            <th>C0[▼ 0.1]</th>
                            <th>C1[▲ 0.2]</th>
                            <th>C2[▼ 0.3]</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <th>A0</th>
                            <td>1</td>
                            <td>2</td>
                            <td>3</td>
                        </tr>
                        <tr>
                            <th>A1</th>
                            <td>4</td>
                            <td>5</td>
                            <td>6</td>
                        </tr>
                        <tr>
                            <th>A2</th>
                            <td>7</td>
                            <td>8</td>
                            <td>9</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <em class="decisionmatrix-dim">3 Alternatives x 3 Criteria
            </em>
        </div>
    """

    result = dm._repr_html_()

    def remove_white_spaces(txt):
        return "".join(
            [line.strip() for line in txt.splitlines() if line.strip()]
        )

    assert remove_white_spaces(expected) == remove_white_spaces(result)


def test_to_dataframe(data_values):

    mtx, objectives, weights, anames, cnames = data_values(seed=42)

    dm = data.mkdm(
        matrix=mtx,
        objectives=objectives,
        weights=weights,
        anames=anames,
        cnames=cnames,
    )

    df = dm.to_dataframe()

    rows = np.vstack((construct_objectives(objectives), weights, mtx))
    expected = pd.DataFrame(
        rows, index=["objectives", "weights"] + anames, columns=cnames
    )

    pd.testing.assert_frame_equal(df, expected)


# =============================================================================
# MUST FAIL
# =============================================================================


def test_no_provide_mtx(data_values):
    _, objectives, weights, anames, cnames = data_values(seed=42)
    with pytest.raises(TypeError):
        data.mkdm(
            objectives=objectives,
            weights=weights,
            cnames=cnames,
            anames=anames,
        )


def test_no_provide_objective(data_values):
    mtx, _, weights, anames, cnames = data_values(seed=42)
    with pytest.raises(TypeError):
        data.mkdm(mtxt=mtx, weights=weights, cnames=cnames, anames=anames)


def test_invalid_objective(data_values):
    mtx, _, weights, anames, cnames = data_values(seed=42)
    objectives = [1, 2, 3, 4]
    with pytest.raises(ValueError):
        data.mkdm(
            matrix=mtx,
            objectives=objectives,
            weights=weights,
            anames=anames,
            cnames=cnames,
        )


def test_weight_no_float(data_values):
    mtx, objectives, _, anames, cnames = data_values(seed=42)
    weights = ["hola"]
    with pytest.raises(ValueError):
        data.mkdm(
            matrix=mtx,
            objectives=objectives,
            weights=weights,
            anames=anames,
            cnames=cnames,
        )


def test_missmatch_objective(data_values):
    mtx, objectives, weights, anames, cnames = data_values(seed=42)
    objectives = objectives[1:]
    with pytest.raises(ValueError):
        data.mkdm(
            matrix=mtx,
            objectives=objectives,
            weights=weights,
            anames=anames,
            cnames=cnames,
        )


def test_missmatch_weights(data_values):
    mtx, objectives, weights, anames, cnames = data_values(seed=42)
    weights = weights[1:]
    with pytest.raises(ValueError):
        data.mkdm(
            matrix=mtx,
            objectives=objectives,
            weights=weights,
            anames=anames,
            cnames=cnames,
        )


def test_missmatch_anames(data_values):
    mtx, objectives, weights, anames, cnames = data_values(seed=42)
    anames = anames[1:]
    with pytest.raises(ValueError):
        data.mkdm(
            matrix=mtx,
            objectives=objectives,
            weights=weights,
            anames=anames,
            cnames=cnames,
        )


def test_missmatch_cnames(data_values):
    mtx, objectives, weights, anames, cnames = data_values(seed=42)
    cnames = cnames[1:]
    with pytest.raises(ValueError):
        data.mkdm(
            matrix=mtx,
            objectives=objectives,
            weights=weights,
            anames=anames,
            cnames=cnames,
        )


def test_mtx_ndim1(data_values):
    mtx, objectives, weights, anames, cnames = data_values(seed=42)
    mtx = mtx.flatten()
    with pytest.raises(ValueError):
        data.mkdm(
            matrix=mtx,
            objectives=objectives,
            weights=weights,
            anames=anames,
            cnames=cnames,
        )


def test_mtx_ndim3(data_values):
    _, objectives, weights, anames, cnames = data_values(seed=42)
    mtx = [[[1, 2, 3], [4, 5, 6], [7, 8, 9]]]
    with pytest.raises(ValueError):
        data.mkdm(
            matrix=mtx,
            objectives=objectives,
            weights=weights,
            anames=anames,
            cnames=cnames,
        )
