table_GDP = open("table/国内生产总值.csv", "r")

for line in table_GDP.readlines():
    print(line)
