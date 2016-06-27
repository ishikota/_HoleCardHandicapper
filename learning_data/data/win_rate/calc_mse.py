import sys
import csv

def read_data(file_path):
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        data = []
        for row in reader:
            data.append(float(row[2]))
        return data

def calc_max_diff(a, b):
    return reduce(lambda best, d: max(best, abs(d[0]-d[1])), zip(a,b), 0)

def calc_mse(a, b):
    return reduce(lambda acc, d: acc + abs(d[0]-d[1])**2, zip(a,b), 0)

def main():
    file_a_path = sys.argv[1]
    file_b_path = sys.argv[2]
    a = read_data(file_a_path)
    b = read_data(file_b_path)
    print "MSE      = %f" % (calc_mse(a, b) / len(a))
    print "MAX DIFF = %f" % calc_max_diff(a, b)

if __name__ == '__main__':
    main()
