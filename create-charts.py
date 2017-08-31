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
import pandas as pd
import seaborn as sns

sns.set_style("darkgrid")
# Selected from https://matplotlib.org/users/colormaps.html#qualitative
sns.set_palette(sns.color_palette("tab20", n_colors=11))


def save_plot(df, title, filename, print_data=False, formatter=tkr.FuncFormatter(lambda y, p: "{:,}".format(y))):
    unit = df['Unit'].unique()[0]
    print("Creating chart: " + title + ", filename: " + filename + ".")
    if print_data:
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(df)
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
    plt.legend(loc='upper right', frameon=True)
    plt.savefig(filename)
    plt.clf()
    plt.close(fig)


def replace_benchmark_name(df):
    return df.replace(
        [r'^com\.github\.chrishantha\.microbenchmark\.objectpool\.(.*)Benchmark.useObject:useObject(.*)$'], [r'\1\2'],
        regex=True)


def save_percentile_plot(df, title_percentile, percentile):
    df_sample_percentile = df.loc[df['Benchmark'].str.endswith(':useObject·' + percentile)]
    df_sample_percentile = replace_benchmark_name(df_sample_percentile)
    save_plot(df_sample_percentile, title_percentile + "th Percentile Latency Comparison",
              "latency" + title_percentile + ".png", formatter=tkr.FormatStrFormatter('%.2f'))


def main():
    all_results = glob.glob("*.csv")
    print("Creating charts using data in following files:")
    for file in all_results:
        print(file)

    print("\nCreating charts...\n")
    df = pd.concat(map(pd.read_csv, all_results), ignore_index=True)

    df_thrpt = df.loc[df['Mode'] == "thrpt"]
    df_thrpt = df_thrpt.replace(r'^com\.github\.chrishantha\.microbenchmark\.objectpool\.(.*)Benchmark.useObject$',
                                r'\1',
                                regex=True)
    df_thrpt = df_thrpt.replace(
        'com.github.chrishantha.microbenchmark.objectpool.TestObjectBenchmark.expensiveObjectCreate',
        'OnDemandExpensiveObject', regex=False)

    mask = df_thrpt['Benchmark'].isin(['OnDemandExpensiveObject'])
    save_plot(df_thrpt[~mask], "Throughput Comparison", "thrpt-all.png")

    save_plot(df_thrpt[df_thrpt['Benchmark'].isin(
        ['OnDemandExpensiveObject', 'CommonsPool2GenericObjectPool', 'StormpotBlazePool'])],
              "On Demand Object Creation vs Object Pooling Throughput Comparison", "thrpt-ondemand-vs-pooling.png")

    df_sample = df.loc[df['Mode'] == "sample"]

    save_percentile_plot(df_sample, '50', 'p0.50')
    save_percentile_plot(df_sample, '90', 'p0.90')
    save_percentile_plot(df_sample, '95', 'p0.95')
    save_percentile_plot(df_sample, '99', 'p0.99')
    save_percentile_plot(df_sample, '99.9', 'p0.999')
    save_percentile_plot(df_sample, '99.99', 'p0.9999')
    save_percentile_plot(df_sample, '100', 'p1.00')

    df_sample_percentiles = df_sample.loc[df_sample['Benchmark'].str.contains(':useObject·p')]
    df_sample_percentiles = replace_benchmark_name(df_sample_percentiles)
    df_sample_percentiles['Pool'] = df_sample_percentiles['Benchmark'].str.extract('(?P<Pool>\w+Pool)', expand=True)

    unique_pools = df_sample_percentiles['Pool'].unique()

    for pool in unique_pools:
        save_plot(df_sample_percentiles.loc[df_sample_percentiles['Pool'] == pool], "Latency Percentiles for " + pool,
                  pool + "-latency.png")

    print("Done")


if __name__ == '__main__':
    main()
