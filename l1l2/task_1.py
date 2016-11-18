from numpy import *
from dual_simplex_method import DualSimplexMethodSolver
from simplex_method import SimplexMethodSolver
from math import floor

class IntegerLinearProgrammingSolver(object):
  def __init__(self, A, b, c, d_low = None, d_high = None):
    self.A = A
    self.b = b
    self.c = c
    self.d_low = d_low
    self.d_high = d_high
    self.m, self.n = A.shape
    self.has_solution = False
    self.optimal_cost = -inf
    self.eps = 0.000001

  def is_integer(self, val):
    return abs(round(val) - val) < self.eps

  def is_integers(self, x):
    round_x = array([round(el) for el in x])
    return all(abs(round_x - x) < self.eps)

  def get_index_of_first_float(self, x):
    round_x = array([round(el) for el in x])
    return list(abs(round_x - x) < self.eps).index(False)

  def dfs(self, d_low, d_high, basic_indexes = None, nonbasic_indexes = None):
    try:
      res = DualSimplexMethodSolver(self.A, self.b, self.c, d_low, d_high, basic_indexes, nonbasic_indexes).solve()
      x = res.x
      raised = False
      cost = dot(self.c, x)
    except:
      raised = True
    if (raised or cost <= self.optimal_cost):
     return
    if (self.is_integers(x)):
      self.has_solution = True
      self.x = x
      self.optimal_cost = cost
    else:
      j0 = self.get_index_of_first_float(x)
      value = floor(x[j0])

      right = copy(d_high)
      right[j0] = value
      self.dfs(d_low, right, res.basic_indexes, res.nonbasic_indexes)

      left = copy(d_low)
      left[j0] = value + 1
      self.dfs(left, d_high, res.basic_indexes, res.nonbasic_indexes)

  def the_branch_and_bound_method(self):
    self.dfs(self.d_low, self.d_high)
    if self.has_solution:
      return self
    else:
      raise ValueError("This task has no solution.")

  def change_params(self, res):
    self.A = res.A
    self.B = res.B
    self.b = res.b
    self.c = res.c
    self.basic_indexes = res.basic_indexes
    self.nonbasic_indexes = res.nonbasic_indexes
    self.n = res.n
    self.m = res.m
    self.x = res.x

  def create_y(self):
    i0 = self.get_index_of_first_float(self.x)
    ji0 = self.basic_indexes.index(i0)
    return dot(eye(self.m)[:, ji0], self.B)

  def change_A(self, y):
    alpha = dot(y, self.A)
    alpha = array([round(el) if self.is_integer(el) else el for el in alpha])
    alpha = array([el - floor(el) for el in alpha])
    self.A = vstack([self.A, alpha])
    column = -eye(self.m + 1)[:, self.m]
    self.A = hstack([self.A, column.reshape(self.m + 1, 1)])

  def change_b(self, y):
    betta = dot(y, self.b)
    betta = betta - floor(betta)
    self.b = append(self.b, [betta])

  def change_c(self):
    self.c = append(self.c, [0])

  def change_restrictions(self, y):
    self.change_A(y)
    self.change_b(y)
    self.change_c()
    self.m += 1
    self.n += 1

  def the_gomori_method(self):
    while True:
      res = SimplexMethodSolver(self.A, self.b, self.c).solve()
      self.change_params(res)
      if(self.is_integers(self.x)):
        return self
      y = self.create_y()
      self.change_restrictions(y)

if __name__ == "__main__":
  A = array([
    array([1, -3, 2, 0, 1, -1, 4, -1, 0], dtype=float),
    array([1, -1, 6, 1, 0, -2, 2, 2, 0], dtype=float),
    array([2, 2, -1, 1, 0, -3, 2, -1, 1], dtype=float),
    array([4, 1, 0, 0, 1, -1, 0, -1, 1], dtype=float),
    array([1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=float),
  ])
  b = array([18, 18, 30, 15, 18], dtype=float64)
  c = array([7, 5, -2, 4, 3, 1, 2, 8, 3], dtype=float64)
  d_low = array([0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=float64)
  d_high = array([8, 8, 8, 8, 8, 8, 8, 8, 8], dtype=float64)
  x0 = IntegerLinearProgrammingSolver(A, b, c, d_low, d_high).the_gomori_method()
  print x0.x[:len(c)]
  print dot(x0.c, x0.x)
