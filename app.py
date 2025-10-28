from flask import Flask, request, jsonify, render_template_string
import math

app = Flask(__name__)

# evaluator aman berbasis ast untuk operasi dasar
import ast, operator as op

OPS = {
    ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv,
    ast.USub: op.neg, ast.Pow: op.pow, ast.Mod: op.mod
}

def eval_expr(expr: str) -> float:
    node = ast.parse(expr, mode='eval').body
    def _eval(n):
        if isinstance(n, ast.Num): return n.n
        if isinstance(n, ast.UnaryOp) and type(n.op) in OPS: return OPS[type(n.op)](_eval(n.operand))
        if isinstance(n, ast.BinOp) and type(n.op) in OPS: return OPS[type(n.op)](_eval(n.left), _eval(n.right))
        if isinstance(n, ast.Expression): return _eval(n.body)
        raise ValueError("Ekspresi tidak didukung")
    return float(_eval(node))

HTML = """
<!doctype html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Calculator</title>
<style>
body{font-family:sans-serif;background:#e8efe8;margin:0;padding:0;display:flex;justify-content:center}
.phone{width:360px;border:3px solid #1d2b1f;border-radius:24px;margin:24px;background:#6daf79}
.screen{color:#fff;padding:16px 20px 8px 20px}
.expr{opacity:.9}
.result{font-size:42px;font-weight:700}
.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;padding:16px}
.btn{background:#8cc096;border:none;border-radius:10px;padding:16px;font-size:18px}
.btn.op{background:#7ab589}
.btn.eq{background:#ffffff;color:#1d2b1f;font-weight:700}
.btn.del{background:#243128;color:#fff}
</style>
</head>
<body>
<div class="phone">
  <div class="screen">
    <div class="expr" id="expr"></div>
    <div class="result" id="res">0</div>
  </div>
  <div class="grid" id="keys"></div>
</div>
<script>
const keys = [
  ['/', '(', ')', '%'],
  ['*','7','8','9'],
  ['-','4','5','6'],
  ['+','1','2','3'],
  ['Del','0','=','C']
];
const grid = document.getElementById('keys');
const exprEl = document.getElementById('expr');
const resEl  = document.getElementById('res');
let expr = '';

function render(){
  exprEl.textContent = expr || '0';
  if(expr && !/[=]$/.test(expr)){
    fetch('/eval?e=' + encodeURIComponent(expr))
      .then(r=>r.json()).then(j=>{ resEl.textContent = j.ok ? j.value : 'Err'; });
  } else if(!expr){ resEl.textContent = '0'; }
}

keys.flat().forEach(k=>{
  const b=document.createElement('button');
  b.className='btn'+((k=='=' )?' eq':(k=='Del'?' del':' op'));
  if(/[0-9]/.test(k)) b.className='btn';
  b.textContent=k;
  b.onclick=()=>{
    if(k==='C'){ expr=''; }
    else if(k==='Del'){ expr = expr.slice(0,-1); }
    else if(k==='='){
      fetch('/eval?e=' + encodeURIComponent(expr)).then(r=>r.json()).then(j=>{
        resEl.textContent = j.ok ? j.value : 'Err';
      });
    } else { expr+=k; }
    render();
  };
  grid.appendChild(b);
});
render();
</script>
</body>
</html>
"""

@app.get("/")
def index():
    return render_template_string(HTML)

@app.get("/eval")
def eval_api():
    e = request.args.get("e","")
    try:
        val = round(eval_expr(e), 5)
        return jsonify(ok=True, value=val)
    except Exception:
        return jsonify(ok=False, error="invalid"), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
