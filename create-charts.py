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


def print_data(df):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df)


def save_plot(df, title, filename, print_data=False, formatter=tkr.FuncFormatter(lambda y, p: "{:,}".format(y))):
    unit = df['Unit'].unique()[0]
    print("Creating chart: " + title + ", filename: " + filename + ".")
    if print_data:
        print_data(df)
    fig, ax = plt.subplots()
    g = sns.factorplot(x="Threads", y="Score",
                       hue="Benchmark", col="Param: poolSize",
                       data=df, kind='bar',
                       size=6, aspect=1, col_wrap=2, legend=False)
    for ax in g.axes.flatten():
        ax.yaxis.set_major_formatter(formatter)
    g.set_axis_labels(y_var="Score (" + unit + ")")
    plt.subplots_adjust(top=0.9, left=0.1)
    g.fig.suptitle(title)
    plt.legend(loc='upper left', frameon=True)
    plt.savefig(filename)
    plt.clf()
    plt.close(fig)


# Plot bar charts with error bars
# Some links helped:
# https://stackoverflow.com/a/42033734/1955702
# https://stackoverflow.com/a/30428808/1955702
# https://matplotlib.org/devdocs/gallery/api/barchart.html#sphx-glr-gallery-api-barchart-py
def barplot_with_errorbars(x, y, yerr, threads, benchmarks, label, **kwargs):
    data = kwargs.pop("data")
    x = np.arange(len(threads))
    offsets = (np.arange(len(benchmarks)) - np.arange(len(benchmarks)).mean()) / (len(benchmarks) + 1.)
    width = np.diff(offsets).mean()
    # Make sure data is sorted by Threads, which is in x axis.
    data = data.sort_values('Threads')
    for i, benchmark in enumerate(benchmarks):
        if label == benchmark:
            plt.bar(x + offsets[i], data['Score'], width=width, label=label, yerr=data['Score Error (99.9%)'],
                    capsize=3)
    plt.xticks(x, threads)


def save_plot_with_error_bars(df, title, filename, print_data=False,
                              formatter=tkr.FuncFormatter(lambda y, p: "{:,}".format(y))):
    unit = df['Unit'].unique()[0]
    print("Creating chart: " + title + ", filename: " + filename + ".")
    if print_data:
        print_data(df)
    fig, ax = plt.subplots()

    threads = sorted(df['Threads'].unique())
    benchmarks = sorted(df['Benchmark'].unique())

    g = sns.FacetGrid(df, hue="Benchmark", col="Param: poolSize",
                      size=6, aspect=1, col_wrap=2)
    g = g.map_dataframe(barplot_with_errorbars, "Threads", "Score", "Score Error (99.9%)", threads, benchmarks)
    for ax in g.axes.flatten():
        ax.yaxis.set_major_formatter(formatter)
    g.set_axis_labels(y_var="Score (" + unit + ")")
    plt.subplots_adjust(top=0.9, left=0.1)
    g.fig.suptitle(title)
    plt.legend(loc='upper left', frameon=True)
    plt.savefig(filename)
    plt.clf()
    plt.close(fig)


def save_plots(df, title, filename_prefix):
    # Save two plots with and without error bars
    # Plotting errorbars with dataframe data in factorplot is not directly supported.
    # First plot is important and must be used to verify the accuracy of the plot with error bars.
    save_plot(df, title, filename_prefix + '.png')
    save_plot_with_error_bars(df, title, filename_prefix + '-with-error-bars.png')


def save_lmplot(df, x, title, filename, print_data=False):
    unit = df['Unit'].unique()[0]
    print("Creating chart: " + title + ", filename: " + filename + ".")
    if print_data:
        print_data(df)
    fig, ax = plt.subplots()
    markers_length = len(df["Benchmark"].unique())
    g = sns.lmplot(data=df, x=x, y="Score", hue="Benchmark", size=8, legend=False, x_jitter=0.1, y_jitter=0.1,
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
    df = df.replace('com.github.chrishantha.microbenchmark.objectpool.TestObjectBenchmark.expensiveObjectCreate',
                    'OnDemandExpensiveObject', regex=False)
    df = df.replace(
        r'^com\.github\.chrishantha\.microbenchmark\.objectpool\.TestObjectBenchmark\.expensiveObjectCreate' +
        r':expensiveObjectCreate(.*)$', r'OnDemandExpensiveObject\1', regex=True)
    return df


def save_percentile_plot(df, title_percentile, percentile):
    df_sample_percentile = df.loc[df['Benchmark'].str.endswith(percentile)]
    save_plot(df_sample_percentile, title_percentile + "th Percentile Latency Comparison",
              "latency" + title_percentile + ".png", formatter=tkr.FormatStrFormatter('%.2f'))


def main():
    all_results = glob.glob("*.csv")
    print("Creating charts using data in following files:")
    for file in all_results:
        print(file)

    print("\nCreating charts...\n")
    df = pd.concat(map(pd.read_csv, all_results), ignore_index=True)
    df = replace_benchmark_names(df)

    df_thrpt = df.loc[df['Mode'] == "thrpt"]

    mask = df_thrpt['Benchmark'].isin(['OnDemandExpensiveObject'])
    save_plots(df_thrpt[~mask], "Throughput Comparison", "thrpt-all")

    save_lmplot(df_thrpt, "Threads", "Throuphput vs Threads", "lmplot_thrpt_vs_threads.png")
    save_lmplot(df_thrpt[~pd.isnull(df_thrpt['Param: poolSize'])], "Param: poolSize", "Throuphput vs Pool Sizes",
                "lmplot_thrpt_vs_pool_sizes.png")

    df_sample = df.loc[df['Mode'] == "sample"]
    # Score Error (99.9%) is NaN for percentiles
    df_sample_without_percentiles = df_sample[~pd.isnull(df_sample['Score Error (99.9%)'])]

    save_plots(df_sample_without_percentiles, "Sample Time Comparison", "sample-all")

    save_lmplot(df_sample_without_percentiles, "Threads", "Sample Time vs Threads", "lmplot_sample_vs_threads.png")
    save_lmplot(df_sample_without_percentiles[~pd.isnull(df_sample_without_percentiles['Param: poolSize'])],
                "Param: poolSize", "Sample Time vs Pool Sizes", "lmplot_sample_vs_pool_sizes.png")

    save_percentile_plot(df_sample, '50', 'p0.50')
    save_percentile_plot(df_sample, '90', 'p0.90')
    save_percentile_plot(df_sample, '95', 'p0.95')
    save_percentile_plot(df_sample, '99', 'p0.99')
    save_percentile_plot(df_sample, '99.9', 'p0.999')
    save_percentile_plot(df_sample, '99.99', 'p0.9999')
    save_percentile_plot(df_sample, '100', 'p1.00')

    df_sample_percentiles = df_sample.copy()
    df_sample_percentiles = df_sample_percentiles.loc[pd.isnull(df_sample['Score Error (99.9%)'])]
    df_sample_percentiles['Pool'] = df_sample_percentiles['Benchmark'].str.extract('(?P<Pool>\w+Pool)', expand=True)

    df_sample_pool_percentiles = df_sample_percentiles.loc[~pd.isnull(df_sample_percentiles['Pool'])]
    unique_pools = df_sample_pool_percentiles['Pool'].unique()
    for pool in unique_pools:
        save_plot(df_sample_percentiles.loc[df_sample_percentiles['Pool'] == pool], "Latency Percentiles for " + pool,
                  pool + "-latency.png")

    print("Done")


if __name__ == '__main__':
    main()
