from flask import Flask,request

app = Flask(__name__)





HTML = """
<h2>🎀 BMI Calculator 🎀</h2>
<form method="post">
  Weight (kg): <input type="number" step="0.1" name="weight" required><br><br>
  Height (m): <input type="number" step="0.01" name="height" required><br><br>
  <button type="submit">Calculate 💗</button>
</form>
<h3>{result}</h3>

<style>
body {{
    background-color: #fff0f5;
    color: #d63384;
    font-family: Arial;
    text-align: center;
    padding: 30px;
}}
input {{
    padding: 8px;
    border: 1px solid pink;
    border-radius: 8px;
}}
button {{
    background: hotpink;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 10px;
    cursor: pointer;
}}
</style>
"""





@app.route('/', methods=['GET', 'POST'])
def bmi():
    result=""
    if request.method == 'POST':
        w = float(request.form['weight'])
        h = float(request.form['height'])
        bmi = round(w/(h*h),2)
        if bmi < 18.5:
           cat=" You are underweight."
        elif bmi < 25:
            cat=" You have a normal weight."
        elif bmi < 30:
            cat=" You are overweight."
        else:
            cat=" You are obese."
        result = f"Your BMI is: {bmi} ({cat})"
    return HTML.format(result=result)


if __name__ == "__main__":
    app.run(debug=True)