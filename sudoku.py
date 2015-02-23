#!/usr/bin/env python
import os,sys,constraint

def solve(data):
  # a text file that contains 9x9 digits seperated with whitespace.
  # empty squares are denoted by zeroes.
  #3x3 square template
  square = [0,1,2,9,10,11,18,19,20]

  sudoku = constraint.Problem()

  #add free variables
  sudoku.addVariables(filter(lambda x: data[x]==0, range(81)),range(1,10))
  #limit the domain for given values
  [sudoku.addVariable(i,[e]) for i,e in enumerate(data) if e]

  #row constraint
  [sudoku.addConstraint(constraint.AllDifferentConstraint(),[9*row+p for p in range(9)]) for row in range(9)]
  #column constraint
  [sudoku.addConstraint(constraint.AllDifferentConstraint(),[row+9*p for p in range(9)]) for row in range(9)]
  #3x3 square constraint
  [sudoku.addConstraint(constraint.AllDifferentConstraint(),map(lambda x:x+o,square)) for o in map(lambda x:x*3,square)]

  #pure witchcraft
  solution = sudoku.getSolution()
  return solution


if __name__ == '__main__': 
    data = map(int,open(sys.argv[1]).read().split())
    solution = solve(data)
    #check if solution exists
    if not solution: 
      print "No solution found!"
    else:
      #output formatting
      out = ""
      vals = solution.values()
      for e in xrange(81):
        if (e+1)%9:
          out += "%d "%vals[e]
        else: out += "%d\n"%vals[e]

      print out
