import gnss_lib_py as glp

# Load measurements and ground truth into a NavData object
derived_data = glp.AndroidDerived2023("data/device_gnss.csv")
gt_data = glp.AndroidGroundTruth2023("data/ground_truth.csv")

# Convert NavData object to pandas dataframe
derived_data_df = derived_data.pandas_df()
gt_data_df = gt_data.pandas_df()

# Save to csv
derived_data_df.to_csv("data/device_gnss_derived.csv")
gt_data_df.to_csv("data/ground_truth_derived.csv")