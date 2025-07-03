def write_lkh_par_file(tsp_file="problem_7.tsp",
                        par_file="params_7.par", tour_file='output_7.tour'):
    with open(par_file, 'w') as f:
        f.write(f"PROBLEM_FILE = {tsp_file}\n")
        f.write(f"OUTPUT_TOUR_FILE = {tour_file}\n")
        f.write("RUNS = 1\n")

# 使い方
write_lkh_par_file()
