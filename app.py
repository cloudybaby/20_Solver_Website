from flask import Flask, render_template, request

app = Flask(__name__)

# Fungsi solver 20 yang sebelumnya sudah kita buat
def twenty_solver(numbers):
    import itertools
    import operator

    operators = [
        ('+', operator.add), 
        ('-', operator.sub), 
        ('*', operator.mul), 
        ('/', operator.truediv)
    ]
    
    solutions = []
    
    for num_order in itertools.permutations(numbers):
        for op_combination in itertools.product(operators, repeat=3):
            exprs = [
                f"({num_order[0]} {op_combination[0][0]} {num_order[1]}) {op_combination[1][0]} {num_order[2]} {op_combination[2][0]} {num_order[3]}",
                f"{num_order[0]} {op_combination[0][0]} ({num_order[1]} {op_combination[1][0]} {num_order[2]}) {op_combination[2][0]} {num_order[3]}",
                f"{num_order[0]} {op_combination[0][0]} {num_order[1]} {op_combination[1][0]} ({num_order[2]} {op_combination[2][0]} {num_order[3]})",
                f"({num_order[0]} {op_combination[0][0]} {num_order[1]} {op_combination[1][0]} {num_order[2]}) {op_combination[2][0]} {num_order[3]}",
                f"{num_order[0]} {op_combination[0][0]} ({num_order[1]} {op_combination[1][0]} {num_order[2]} {op_combination[2][0]} {num_order[3]})"
            ]
            
            for expr in exprs:
                try:
                    if eval(expr) == 20:
                        solutions.append(expr)
                except ZeroDivisionError:
                    continue

    if solutions:
        return solutions
    else:
        return "Tidak ada solusi, silakan coba dengan angka yang lain."

# Route untuk halaman utama
@app.route('/')
def index():
    return render_template('index.html')

# Route untuk menangani form input dan output solver
@app.route('/solve', methods=['POST'])
def solve():
    try:
        numbers = [int(request.form['num1']), int(request.form['num2']), int(request.form['num3']), int(request.form['num4'])]
        solutions = twenty_solver(numbers)
        
        if isinstance(solutions, list):
            return render_template('index.html', solutions=solutions)
        else:
            return render_template('index.html', error=solutions)
    except ValueError:
        return render_template('index.html', error="Input tidak valid. Masukkan angka antara 1-10.")

if __name__ == "__main__":
    app.run(debug=True)
