#! /usr/bin/env python

# SPDX-FileCopyrightText: 2020 - 2022 Intel Corporation
#
# SPDX-License-Identifier: Apache-2.0

import dpctl
import numpy as np

import numba_dpex as dpex


@dpex.kernel
def data_parallel_sum(a, b, c):
    """
    A two-dimensional vector addition example using the ``kernel`` decorator.
    """
    i = dpex.get_global_id(0)
    j = dpex.get_global_id(1)
    c[i, j] = a[i, j] + b[i, j]


def driver(a, b, c, global_size):
    print("before A: ", a)
    print("before B: ", b)
    data_parallel_sum[global_size, dpex.DEFAULT_LOCAL_SIZE](a, b, c)
    print("after  C : ", c)


def main():
    # Array dimensions
    X = 8
    Y = 8
    global_size = X, Y

    a = np.arange(X * Y, dtype=np.float32).reshape(X, Y)
    b = np.array(np.random.random(X * Y), dtype=np.float32).reshape(X, Y)
    c = np.ones_like(a).reshape(X, Y)

    # Use the environment variable SYCL_DEVICE_FILTER to change the default device.
    # See https://github.com/intel/llvm/blob/sycl/sycl/doc/EnvironmentVariables.md#sycl_device_filter.
    device = dpctl.select_default_device()
    print("Using device ...")
    device.print_device_info()

    with dpctl.device_context(device):
        driver(a, b, c, global_size)

    print(c)

    print("Done...")


if __name__ == "__main__":
    main()
