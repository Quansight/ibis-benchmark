export $(cat .env | xargs) && cat setup_files/raw_data_urls.txt | xargs -n 1 -P 6 wget -c -P $IBIS_BENCHMARK_DOWNLOAD
