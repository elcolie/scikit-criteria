#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: BSD-3 (https://tldrlegal.com/license/bsd-3-clause-license-(revised))
# Copyright (c) 2016-2021, Cabral, Juan; Luczywo, Nadia
# All rights reserved.

# =============================================================================
# DOCS
# =============================================================================

"""test for skcriteria.pipelines

"""


# =============================================================================
# IMPORTS
# =============================================================================

import pytest

from skcriteria import pipeline
from skcriteria.madm.similarity import TOPSIS
from skcriteria.preprocessing.invert_objectives import MinimizeToMaximize
from skcriteria.preprocessing.scalers import StandarScaler
from skcriteria.preprocessing.weighters import Critic

# =============================================================================
# TESTS
# =============================================================================


def test_pipeline_mkpipe(decision_matrix):
    dm = decision_matrix(seed=42)

    steps = [
        MinimizeToMaximize(),
        StandarScaler(target="matrix"),
        Critic(correlation="spearman"),
        Critic(),
        TOPSIS(),
    ]

    expected = dm
    for step in steps[:-1]:
        expected = step.transform(expected)
    expected = steps[-1].evaluate(expected)

    pipe = pipeline.mkpipe(*steps)
    result = pipe.evaluate(dm)

    assert result.equals(expected)
    assert len(pipe) == len(steps)
    assert steps == [s for _, s in pipe.steps]
    for s in pipe.named_steps.values():
        assert s in steps


def test_pipeline_slicing():

    steps = [
        MinimizeToMaximize(),
        StandarScaler(target="matrix"),
        Critic(correlation="spearman"),
        Critic(),
        TOPSIS(),
    ]

    pipe = pipeline.mkpipe(*steps)

    for idx, step in enumerate(steps):
        assert pipe[idx] == step

    for name, step in pipe.named_steps.items():
        assert pipe[name] == step

    assert [s for _, s in pipe[2:].steps] == steps[2:]

    with pytest.raises(ValueError):
        pipe[::2]

    with pytest.raises(KeyError):
        pipe[None]


def test_pipeline_not_transformer_fail():
    steps = [TOPSIS(), TOPSIS()]
    with pytest.raises(TypeError):
        pipeline.mkpipe(*steps)


def test_pipeline_not_dmaker_fail():
    steps = [Critic()]
    with pytest.raises(TypeError):
        pipeline.mkpipe(*steps)


def test_pipeline_name_not_str():
    with pytest.raises(TypeError):
        pipeline.SKCPipeline(steps=[(..., Critic()), ("final", TOPSIS())])
    with pytest.raises(TypeError):
        pipeline.SKCPipeline(steps=[("first", Critic()), (..., TOPSIS())])
