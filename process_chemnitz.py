import gnss_lib_py as glp
from gnss_lib_py.parsers.smartloc import SmartLocRaw, calculate_gt_ecef, calculate_gt_vel, remove_nlos

# Load the TU Chemnitz SmartLoc dataset
def process_raw_data():
    # Load smartLoc data into NavData object
    smartloc_data = SmartLocRaw("data/smartloc.csv")
    SV_KEYS = ['x_sv_m', 'y_sv_m', 'z_sv_m', \
           'vx_sv_mps','vy_sv_mps','vz_sv_mps', \
           'b_sv_m', 'b_dot_sv_mps']
    smartloc_data.remove(rows=SV_KEYS,inplace=True)
    # Load ephermeris data
    sp3_path = "data/COD0MGXFIN_20211180000_01D_05M_ORB.SP3"
    clk_path = "data/COD0MGXFIN_20211180000_01D_30S_CLK.CLK"
    # Add ECEF for satellite positions
    derived_smartloc_data = glp.add_sv_states(smartloc_data, source="precise", file_paths=[sp3_path, clk_path],
        verbose = False)
    # Save to csv
    derived_smartloc_data.to_csv("data/smartloc_derived.csv")
    return derived_smartloc_data

# Plot the pseudorange over time of each individual satellite
def plot_pseudorange(data):
    fig = glp.plot_metric(data, "gps_millis","raw_pr_m", groupby="sv_id")
    fig.show()

# Plot the ground truth smartloc on a map
def plot_gt(data):
    fig = glp.plot_map(data)
    fig.show()

def check_ECEF(data):
    # Use wildcard index to show ECEF position row does not exist
    try:
        glp.find_wildcard_indexes(data, "x_*_m")
    except KeyError as no_row_exp:
        print(no_row_exp)

    # Compute ECEF ground truth position and show that row exists
    smartloc_ecef_gt = calculate_gt_ecef(data)
    print(glp.find_wildcard_indexes(smartloc_ecef_gt, "x_*_m"))
    'Missing x_*_m row.'
    {'x_*_m': ['x_rx_gt_m']}
    # Use wildcard index to show that ECEF velocity rows do not exist
    try:
        glp.find_wildcard_indexes(data, "vx_*_mps")
    except KeyError as no_row_exp:
        print(no_row_exp)

    # Use wildcard index to show that body frame velocity exists
    print(glp.find_wildcard_indexes(data, "v_*_mps"))

    # Compute ECEF ground truth velocity and verify row exists
    smartloc_vel_gt = calculate_gt_vel(data)
    print(glp.find_wildcard_indexes(smartloc_vel_gt, "vx_*_mps"))

    return smartloc_ecef_gt, smartloc_vel_gt

def main():
    smartloc_data = process_raw_data()
    print(smartloc_data)

if __name__ == "__main__":
    main()