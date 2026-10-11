from flask import Flask,request

app=Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>BMI Calculator</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; min-height: 100vh; display: flex; align-items: center; justify-content: center;
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    background-size: 200% 200%; animation: bg 12s ease infinite;
  }}
  @keyframes bg {{ 0% {{ background-position: 0% 50%; }} 50% {{ background-position: 100% 50%; }} 100% {{ background-position: 0% 50%; }} }}
  .card {{ background: #fff; width: 380px; max-width: 92vw; padding: 28px; border-radius: 20px;
    box-shadow: 0 20px 60px rgba(0,0,0,.3); animation: pop .5s ease; }}
  @keyframes pop {{ from {{ transform: scale(.9); opacity: 0; }} to {{ transform: scale(1); opacity: 1; }} }}
  h2 {{ margin: 0 0 4px; text-align: center; font-size: 28px;
    background: linear-gradient(90deg, #667eea, #f5576c); -webkit-background-clip: text; background-clip: text; color: transparent; }}
  .sub {{ text-align: center; color: #888; margin: 0 0 22px; font-size: 14px; }}
  label {{ display: flex; justify-content: space-between; font-weight: 600; color: #444; font-size: 14px; margin-bottom: 6px; }}
  label span {{ color: #667eea; }}
  input[type=number] {{ width: 100%; padding: 12px 14px; border: 2px solid #e3e6f0; border-radius: 12px; font-size: 16px; outline: none; transition: .2s; }}
  input[type=number]:focus {{ border-color: #667eea; box-shadow: 0 0 0 4px rgba(102,126,234,.15); }}
  input[type=range] {{ width: 100%; margin: 10px 0 18px; accent-color: #667eea; cursor: pointer; }}
  button {{ width: 100%; padding: 14px; border: none; border-radius: 12px; font-size: 16px; font-weight: 700; color: #fff; cursor: pointer;
    background: linear-gradient(90deg, #667eea, #764ba2); transition: .2s; margin-top: 4px; }}
  button:hover {{ transform: translateY(-2px); box-shadow: 0 8px 20px rgba(102,126,234,.4); }}
  button:active {{ transform: translateY(0); }}
  .result {{ margin-top: 22px; text-align: center; opacity: 0; transform: translateY(10px); transition: .4s; }}
  .result.show {{ opacity: 1; transform: none; }}
  .num {{ font-size: 52px; font-weight: 800; line-height: 1; transition: color .3s; }}
  .cat {{ display: inline-block; margin-top: 8px; padding: 6px 16px; border-radius: 999px; color: #fff; font-weight: 600; font-size: 14px; transition: background .3s; }}
  .scale {{ position: relative; height: 12px; border-radius: 6px; margin: 22px 0 6px;
    background: linear-gradient(90deg, #3b82f6 0 28.3%, #22c55e 28.3% 50%, #f59e0b 50% 66.7%, #ef4444 66.7% 100%); }}
  .marker {{ position: absolute; top: -6px; left: 0; width: 24px; height: 24px; border-radius: 50%; background: #fff; border: 4px solid #333;
    transform: translateX(-50%); transition: left .5s cubic-bezier(.34,1.56,.64,1), border-color .3s; }}
  .legend {{ display: flex; font-size: 11px; color: #777; }}
  .legend span:nth-child(1) {{ width: 28.3%; }}
  .legend span:nth-child(2) {{ width: 21.7%; }}
  .legend span:nth-child(3) {{ width: 16.7%; }}
  .legend span:nth-child(4) {{ width: 33.3%; }}
  .tip {{ font-size: 13px; color: #666; margin-top: 14px; min-height: 18px; }}
  .server {{ margin-top: 14px; font-size: 13px; color: #764ba2; text-align: center; }}
</style>
</head>
<body>
<div class="card">
  <h2>BMI Calculator</h2>
  <p class="sub">Body Mass Index &bull; live results as you type</p>

  <form method="post" action="/bmi">
    <label>Weight <span id="wv">70 kg</span></label>
    <input type="number" id="w" name="weight" step="0.1" min="20" max="250" value="70" oninput="sync('w')">
    <input type="range" id="wr" min="20" max="250" step="0.5" value="70" oninput="sync('wr')">

    <label>Height <span id="hv">1.75 m</span></label>
    <input type="number" id="h" name="height" step="0.01" min="1" max="2.5" value="1.75" oninput="sync('h')">
    <input type="range" id="hr" min="1" max="2.5" step="0.01" value="1.75" oninput="sync('hr')">

    <button type="submit">Calculate</button>
  </form>

  <div class="result" id="result">
    <div class="num" id="num">--</div>
    <div class="cat" id="cat">--</div>
    <div class="scale"><div class="marker" id="marker"></div></div>
    <div class="legend"><span>Under</span><span>Normal</span><span>Over</span><span>Obese</span></div>
    <div class="tip" id="tip"></div>
  </div>
  <div class="server">{result}</div>
</div>

<script>
var cats = [
  {{ max: 18.5, name: 'Underweight', color: '#3b82f6', tip: 'A nutrient-rich diet can help you reach a healthy weight.' }},
  {{ max: 25,   name: 'Normal',      color: '#22c55e', tip: 'Great! Keep up the balanced lifestyle.' }},
  {{ max: 30,   name: 'Overweight',  color: '#f59e0b', tip: 'Regular activity and mindful eating can help.' }},
  {{ max: 1e9,  name: 'Obese',       color: '#ef4444', tip: 'Consider consulting a healthcare professional.' }}
];

function sync(src) {{
  var w = document.getElementById('w'), wr = document.getElementById('wr');
  var h = document.getElementById('h'), hr = document.getElementById('hr');
  if (src === 'wr') w.value = wr.value;
  if (src === 'w')  wr.value = w.value;
  if (src === 'hr') h.value = hr.value;
  if (src === 'h')  hr.value = h.value;
  document.getElementById('wv').innerText = (parseFloat(w.value) || 0) + ' kg';
  document.getElementById('hv').innerText = (parseFloat(h.value) || 0) + ' m';
  calcBMI();
}}

function calcBMI() {{
  var w = parseFloat(document.getElementById('w').value);
  var h = parseFloat(document.getElementById('h').value);
  var box = document.getElementById('result');
  var num = document.getElementById('num'), cat = document.getElementById('cat');
  var marker = document.getElementById('marker'), tip = document.getElementById('tip');

  box.classList.add('show');

  if (!w || !h || h <= 0) {{
    num.innerText = '--'; num.style.color = '#999';
    cat.innerText = 'Enter valid values'; cat.style.background = '#999';
    tip.innerText = '';
    marker.style.left = '0%'; marker.style.borderColor = '#999';
    return;
  }}

  var bmi = w / (h * h);
  var c = cats.find(function (x) {{ return bmi < x.max; }});

  num.innerText = bmi.toFixed(1);
  num.style.color = c.color;
  cat.innerText = c.name;
  cat.style.background = c.color;
  tip.innerText = c.tip;

  var pct = Math.min(Math.max((bmi - 10) / 30 * 100, 0), 100);
  marker.style.left = pct + '%';
  marker.style.borderColor = c.color;
}}

calcBMI();
</script>
</body>
</html>
"""

@app.route("/",methods=["GET","POST"])
def bmi():
    result=""
    if request.method=="POST":
        w=float(request.form["weight"])
        h=float(request.form["height"])
        bmi=round(w/(h*h),2)
        if bmi<18.5:
            cat="underweight"
        elif bmi<25:
            cat="normal"
        elif bmi<30:
            cat="overweight"
        else:
            cat="obese"
        result= f"BMI: {bmi} ({cat})"
    return HTML.format(result=result)

if __name__ == "__main__":
    app.run(debug=True)