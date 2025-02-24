import gnss_lib_py as glp

def main():
    derived_data = glp.AndroidDerived2021("data/Pixel4XL_derived.csv", remove_timing_outliers=False)
    state_wls = glp.solve_wls(derived_data)
    fig = glp.plot_map(state_wls)
    fig.show()

if __name__ == "__main__":
    main()