#!/usr/bin/env python3.6
# Copyright 2017 M. Isuru Tharanga Chrishantha Perera
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# ----------------------------------------------------------------------------
# Create charts from the benchmark results
# ----------------------------------------------------------------------------
import glob

import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import numpy as np
import pandas as pd
import seaborn as sns

# This script should be run inside the results directory.

sns.set_style("darkgrid")
# Selected from https://matplotlib.org/users/colormaps.html#qualitative
sns.set_palette(sns.color_palette("tab20", n_colors=11))


def print_dataframe(df):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df)


def save_plot(df, title, filename, x="Threads", hue="Benchmark", col="Param: poolSize", col_wrap=2, print_data=False,
              formatter=tkr.FuncFormatter(lambda y, p: "{:,}".format(y))):
    unit = df['Unit'].unique()[0]
    print("Creating chart: " + title + ", filename: " + filename + ".")
    if print_data:
        print_dataframe(df)
    fig, ax = plt.subplots()
    g = sns.factorplot(x=x, y="Score", hue=hue, col=col, data=df, kind='bar',
                       size=5, aspect=1, col_wrap=col_wrap, legend=False)
    for ax in g.axes.flatten():
        ax.yaxis.set_major_formatter(formatter)
    g.set_axis_labels(y_var="Score (" + unit + ")")
    plt.subplots_adjust(top=0.9, left=0.1)
    g.fig.suptitle(title)
    plt.legend(loc='best', title=hue, frameon=True)
    plt.savefig(filename)
    plt.clf()
    plt.close(fig)


# Plot bar charts with error bars
# Some links helped:
# https://stackoverflow.com/a/42033734/1955702
# https://stackoverflow.com/a/30428808/1955702
# https://matplotlib.org/devdocs/gallery/api/barchart.html#sphx-glr-gallery-api-barchart-py
def barplot_with_errorbars(x, y, yerr, x_values, hue_values, label, **kwargs):
    # x_values and benchmarks must be sorted
    data = kwargs.pop("data")
    x_values_length = len(x_values)
    n = np.arange(x_values_length)
    offsets = (np.arange(len(hue_values)) - np.arange(len(hue_values)).mean()) / (len(hue_values) + 1.)
    width = np.diff(offsets).mean()
    # Make sure x axis data is sorted
    data = data.sort_values(x)
    data_length = len(data)
    if data_length < x_values_length:
        print('WARN: Not enough data points for %s. Expected %d, Found %d' % (label, x_values_length, data_length))
    for i, benchmark in enumerate(hue_values):
        if label == benchmark:
            plt.bar(n[:data_length] + offsets[i], data[y], width=width, label=label, yerr=data[yerr], capsize=2)
    plt.xticks(n, x_values)


def save_plot_with_error_bars(df, title, filename, x="Threads", hue="Benchmark", col="Param: poolSize", col_wrap=2,
                              print_data=False,
                              formatter=tkr.FuncFormatter(lambda y, p: "{:,}".format(y))):
    unit = df['Unit'].unique()[0]
    print("Creating chart: " + title + ", filename: " + filename + ".")
    if print_data:
        print_dataframe(df)
    fig, ax = plt.subplots()

    x_values = sorted(df[x].unique())
    hue_values = sorted(df[hue].unique())

    g = sns.FacetGrid(df, hue=hue, col=col, size=5, aspect=1, col_wrap=col_wrap)
    g = g.map_dataframe(barplot_with_errorbars, x, "Score", "Score Error (99.9%)", x_values, hue_values)
    for ax in g.axes.flatten():
        ax.yaxis.set_major_formatter(formatter)
    g.set_axis_labels(y_var="Score (" + unit + ")")
    plt.subplots_adjust(top=0.9, left=0.1)
    g.fig.suptitle(title)
    plt.legend(loc='best', title=hue, frameon=True)
    plt.savefig(filename)
    plt.clf()
    plt.close(fig)


def save_plots(df, title, filename_prefix, x="Threads", hue="Benchmark", col="Param: poolSize", col_wrap=2,
               print_data=False):
    # Save two plots with and without error bars
    # Plotting errorbars with dataframe data in factorplot is not directly supported.
    # First plot is important and must be used to verify the accuracy of the plot with error bars.
    save_plot(df, title, filename_prefix + '.png', x=x, hue=hue, col=col, col_wrap=col_wrap, print_data=print_data)
    save_plot_with_error_bars(df, title, filename_prefix + '-with-error-bars.png', x=x, hue=hue, col=col,
                              col_wrap=col_wrap, print_data=print_data)


def save_lmplot(df, x, title, filename, print_data=False):
    unit = df['Unit'].unique()[0]
    print("Creating chart: " + title + ", filename: " + filename + ".")
    if print_data:
        print_dataframe(df)
    fig, ax = plt.subplots()
    markers_length = len(df["Benchmark"].unique())
    g = sns.lmplot(data=df, x=x, y="Score", hue="Benchmark", size=6, legend=False, x_jitter=0.2, y_jitter=0.5,
                   markers=['o', 'v', '^', '<', '>', '+', 's', 'p', '*', 'x', 'D'][:markers_length])
    for ax in g.axes.flatten():
        ax.yaxis.set_major_formatter(
            tkr.FuncFormatter(lambda y_value, p: "{:,}".format(y_value)))
    plt.subplots_adjust(top=0.9, left=0.18)
    g.set_axis_labels(y_var="Score (" + unit + ")")
    plt.legend(loc='upper left', frameon=True)
    g.fig.suptitle(title)
    plt.savefig(filename)
    plt.clf()
    plt.cla()
    plt.close(fig)


def replace_benchmark_names(df):
    df = df.replace(r'^com\.github\.chrishantha\.microbenchmark\.objectpool\.(.*)Benchmark.useObject$', r'\1',
                    regex=True)
    df = df.replace([r'^com\.github\.chrishantha\.microbenchmark\.objectpool\.(.*)Benchmark.useObject:useObject(.*)$'],
                    [r'\1\2'], regex=True)
    # Profiler Details
    df = df.replace([r'^com\.github\.chrishantha\.microbenchmark\.objectpool\.(.*)Benchmark.useObject:(.*)$'],
                    [r'\1\2'], regex=True)
    df = df.replace('com.github.chrishantha.microbenchmark.objectpool.TestObjectBenchmark.expensiveObjectCreate',
                    'OnDemandExpensiveObject', regex=False)
    df = df.replace(
        r'^com\.github\.chrishantha\.microbenchmark\.objectpool\.TestObjectBenchmark\.expensiveObjectCreate' +
        r':expensiveObjectCreate(.*)$', r'OnDemandExpensiveObject\1', regex=True)
    # Profiler Details
    df = df.replace(
        r'^com\.github\.chrishantha\.microbenchmark\.objectpool\.TestObjectBenchmark\.expensiveObjectCreate' +
        r':(.*)$', r'OnDemandExpensiveObject\1', regex=True)
    return df


def save_percentile_plot(df, title_percentile, percentile):
    df_sample_percentile = df.loc[df['Benchmark'].str.endswith(percentile)]
    save_plot(df_sample_percentile, "Sample Time " + title_percentile + "th Percentile Comparison",
              "sample-time-" + title_percentile + "th-percentile.png", formatter=tkr.FormatStrFormatter('%.2f'))


def main():
    all_results = glob.glob("results-*-threads.csv")
    print("Creating charts using data in following files:")
    for file in all_results:
        print(file)

    print("\nCreating charts...\n")
    df = pd.concat(map(pd.read_csv, all_results), ignore_index=True)
    df = replace_benchmark_names(df)

    df.to_csv('all_results.csv')

    thrpt_unit = 'ops/ms'
    sample_unit = 'ms/op'
    alloc_rate_unit = 'MB/sec'

    df_thrpt = df.loc[(df['Mode'] == "thrpt") & (df['Unit'] == thrpt_unit)]

    thrpt_mask = df_thrpt['Benchmark'].isin(['OnDemandExpensiveObject'])
    save_plots(df_thrpt[~thrpt_mask], "Throughput vs Threads Comparison", "thrpt-vs-threads")
    save_plots(df_thrpt[~thrpt_mask], "Throughput vs Pool Sizes Comparison", "thrpt-vs-pool-sizes", col="Threads",
               x="Param: poolSize")

    save_lmplot(df_thrpt, "Threads", "Throughput vs Threads", "lmplot-thrpt-vs-threads.png")
    save_lmplot(df_thrpt[~pd.isnull(df_thrpt['Param: poolSize'])], "Param: poolSize", "Throughput vs Pool Sizes",
                "lmplot-thrpt-vs-pool-sizes.png")

    for benchmark in df_thrpt[~thrpt_mask]['Benchmark'].unique():
        df_benchmark_thrpt = df_thrpt[df_thrpt['Benchmark'] == benchmark]
        save_plots(df_benchmark_thrpt, "Throughput vs Threads", benchmark + "-thrpt", col="Benchmark",
                   hue="Param: poolSize", col_wrap=1)

    df_sample = df.loc[(df['Mode'] == "sample") & (df['Unit'] == sample_unit)]
    # Score Error (99.9%) is NaN for percentiles
    df_sample_without_percentiles = df_sample[~pd.isnull(df_sample['Score Error (99.9%)'])]
    df_sample_pools_without_percentiles = df_sample_without_percentiles[
        ~pd.isnull(df_sample_without_percentiles['Param: poolSize'])]

    sample_mask = df_sample_without_percentiles['Benchmark'].isin(['OnDemandExpensiveObject'])
    save_plots(df_sample_without_percentiles[~sample_mask], "Sample Time vs Threads Comparison",
               "sample-time-vs-threads")
    save_plots(df_sample_pools_without_percentiles, "Sample Time vs Pool Sizes Comparison",
               "sample-time-vs-pool-sizes", col="Threads", x="Param: poolSize")

    save_lmplot(df_sample_without_percentiles, "Threads", "Sample Time vs Threads", "lmplot-sample-vs-threads.png")
    save_lmplot(df_sample_pools_without_percentiles, "Param: poolSize", "Sample Time vs Pool Sizes",
                "lmplot-sample-vs-pool-sizes.png")

    for benchmark in df_sample_pools_without_percentiles['Benchmark'].unique():
        df_benchmark_sample = df_sample_pools_without_percentiles[
            df_sample_pools_without_percentiles['Benchmark'] == benchmark]
        save_plots(df_benchmark_sample, "Sample Time vs Threads", benchmark + "-sample-time", col="Benchmark",
                   hue="Param: poolSize", col_wrap=1)

    save_percentile_plot(df_sample, '50', 'p0.50')
    save_percentile_plot(df_sample, '90', 'p0.90')
    save_percentile_plot(df_sample, '95', 'p0.95')
    save_percentile_plot(df_sample, '99', 'p0.99')
    save_percentile_plot(df_sample, '99.9', 'p0.999')
    save_percentile_plot(df_sample, '99.99', 'p0.9999')
    save_percentile_plot(df_sample, '100', 'p1.00')

    df_sample_percentiles = df_sample.copy()
    df_sample_percentiles = df_sample_percentiles.loc[pd.isnull(df_sample_percentiles['Score Error (99.9%)'])]
    df_sample_percentiles['Pool'] = df_sample_percentiles['Benchmark'].str.extract('(?P<Pool>\w+Pool)', expand=True)

    df_sample_pool_percentiles = df_sample_percentiles.loc[~pd.isnull(df_sample_percentiles['Pool'])]
    unique_pools = df_sample_pool_percentiles['Pool'].unique()
    for pool in unique_pools:
        save_plot(df_sample_percentiles.loc[df_sample_percentiles['Pool'] == pool],
                  "Sample Time Percentiles for " + pool,
                  pool + "-sample-time-percentiles.png")

    # Save gc.alloc.rate plots
    df_alloc = df.loc[(df['Unit'] == alloc_rate_unit) & (df['Benchmark'].str.endswith('gc.alloc.rate'))]
    df_alloc = df_alloc.replace([r'^(.*)·gc.alloc.rate$'], [r'\1'], regex=True)
    df_thrpt_alloc = df_alloc[df_alloc['Mode'] == "thrpt"]
    df_thrpt_alloc_mask = df_thrpt_alloc['Benchmark'].isin(['OnDemandExpensiveObject'])
    save_plots(df_thrpt_alloc[~df_thrpt_alloc_mask], "GC Allocation Rate vs Threads Comparison",
               "gc-alloc-rate-vs-threads")
    save_plots(df_thrpt_alloc[~df_thrpt_alloc_mask], "GC Allocation Rate vs Pool Sizes Comparison",
               "gc-alloc-rate-vs-pool-sizes", col="Threads", x="Param: poolSize")

    save_lmplot(df_thrpt_alloc, "Threads", "Throughput vs Threads", "lmplot-gc-alloc-rate-vs-threads.png")
    save_lmplot(df_thrpt_alloc[~pd.isnull(df_thrpt_alloc['Param: poolSize'])], "Param: poolSize",
                "Throughput vs Pool Sizes", "lmplot-gc-alloc-rate-vs-pool-sizes.png")

    print("Done")


if __name__ == '__main__':
    main()
