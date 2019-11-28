import os

from ibis_benchmark.nyc_taxi import config
from ibis_benchmark.utils import register_log

# start a new benchmark log
register_log(config.log_path, new_log=True)

os.system('python run.py --omniscidb --cpu --cursor')
os.system('python run.py --omniscidb --cpu --ipc')
# os.system('python run.py --omniscidb --gpu --ipc')
# os.system('python run.py --pandas')
