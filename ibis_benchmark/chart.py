import os

import matplotlib.pyplot as plt
import pandas as pd

results_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'results'
)


def gen_chart(table_name):
    df = pd.read_json(
        os.path.join(results_path, 'benchmark-{}.json'.format(table_name))
    ).T
    print(df.head())

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel("Execution time (s)")
    ax.set_ylabel("Operation")

    df.T.plot(
        kind='barh',
        ax=ax,
        title='Ibis with OmniSciDB CPU and OmnisciDB GPU vs Pandas',
        grid=True,
    )

    fig.savefig(
        os.path.join(results_path, 'chart-{}.png'.format(table_name)),
        bbox_inches='tight',
    )


if __name__ == '__main__':
    gen_chart('nyc-taxi')
