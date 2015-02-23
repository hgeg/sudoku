#!/usr/bin/env python
from flask import Flask, request, render_template
from flup.server.fcgi import WSGIServer
from sudoku import solve
import json

app = Flask(__name__,static_url_path="/sudoku/static",static_folder="./static")

@app.route("/sudoku/",methods=['GET','POST'])
def sudoku():
  if request.method=='POST':
    board = [[0 for e in xrange(9)] for e in xrange(9)]
    for k,v in request.form.items():
        board[int(k[1])-1][int(k[2])-1] = int(v) if v else 0
    lined = reduce(lambda e,f: e+f, board)
    off = lambda i: i+(i/3)*6
    line = lambda i: lined[off(i)*3:off(i)*3+3]+lined[off(i)*3+9:off(i)*3+12]+lined[off(i)*3+18:off(i)*3+21]
    listed = reduce(lambda e,f: e+f, [line(i) for i in xrange(9)])
    try:
        lined = solve(listed).values()
    except:
        lined = list('NO'+' '*7+'POSSIBLE '+'SOLUTIONS'+54*' ')
    values = reduce(lambda e,f: e+f, [line(i) for i in xrange(9)])
    keys = ['c%d%d'%(e,f) for e in xrange(1,10) for f in xrange(1,10)]
    solution = json.dumps(dict(zip(keys,values)))
    given = json.dumps(request.form)
    return render_template('sudoku.html',solution=solution,given=given)
  else:
    return render_template('sudoku.html')
  

def main():
  #app.run('0.0.0.0',9753,debug=True)
  WSGIServer(app).run()

if __name__ == '__main__': main()
