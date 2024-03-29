import os

import matplotlib.pyplot as plt
import pandas as pd

results_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'docs',
    'static',
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

    try:
        df.T.plot(
            kind='barh',
            ax=ax,
            title='Ibis with OmniSciDB CPU and OmnisciDB GPU vs Pandas',
            grid=True,
        )
    except TypeError as e:
        print(e)
        return

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    fig.savefig(
        os.path.join(results_path, 'chart-{}.png'.format(table_name)),
        bbox_inches='tight',
    )


if __name__ == '__main__':
    gen_chart('nyc-taxi')
