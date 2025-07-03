import csv

def read_input(filename):
    with open(filename) as f:
        cities = []
        for line in f.readlines()[1:]:  # Ignore the first line.
            xy = line.split(',')
            cities.append((float(xy[0]), float(xy[1])))
        return cities


def write_tsplib_file(cities, filename='problem.tsp'):
    with open(filename, 'w') as f:
        f.write("NAME: problem\n")
        f.write("TYPE: TSP\n")
        f.write(f"DIMENSION: {len(cities)}\n")
        f.write("EDGE_WEIGHT_TYPE: EUC_2D\n")
        f.write("NODE_COORD_SECTION\n")
        for i, (x, y) in enumerate(cities, 1):
            f.write(f"{i} {x} {y}\n")
        f.write("EOF\n")

if __name__ == '__main__':
    csv_file = 'input_7.csv'  
    cities = read_input(csv_file)
    write_tsplib_file(cities, 'problem_7.tsp')
    print(f"TSPLIB形式のproblem.tspを作成しました。都市数: {len(cities)}")
