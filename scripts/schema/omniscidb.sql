DROP TABLE IF EXISTS nyc_taxi;

CREATE TABLE nyc_taxi (
  VendorID int,
  tpep_pickup_datetime	TIMESTAMP,
  tpep_dropoff_datetime	TIMESTAMP,
  passenger_count int,
  trip_distance	int,
  RatecodeID int,
  store_and_fwd_flag text,
  PULocationID int,
  DOLocationID int,
  payment_type int,
  fare_amount int,
  extra	int,
  mta_tax int,
  tip_amount int,
  tolls_amount int,
  improvement_surcharge int,
  total_amount int
);

