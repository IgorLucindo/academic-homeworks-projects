from utils.solve_utils import *
import numpy as np


# variables
num_of_cargoes = 12
DD = [3, 4, 6, 6, 9, 9, 10, 10, 10, 13, 15, 15]
PO = "XYXYXYXXYYYY"
PD = "AACABAACBBBC"
sailing_time = {
    'X': {'A': 2, 'B': 3, 'C': 2},
    'Y': {'A': 1, 'B': 2, 'C': 1}
}
M = 15

# solve min ships
model = min_ship_solver(num_of_cargoes, DD, PO, PD, sailing_time, M)

# get opt model variables
x = np.zeros((num_of_cargoes, num_of_cargoes))
y = np.zeros((num_of_cargoes))
for var in model.getVars():
    if var.varName.startswith('x[') and ']' in var.varName:
        indices = var.varName[2:-1].split(',')
        i = int(indices[0]); j = int(indices[1])
        x[i][j] = var.x
    elif var.varName[0] == 'y':
        i = int(var.varName[2])
        y[i] = var.x
        
# print results
print('Min-ships - objective function value: %f' % model.objVal)
print("\nvariables:\nx: ", x)
print("\ny: ", y)