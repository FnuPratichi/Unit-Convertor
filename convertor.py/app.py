from flask import Flask, render_template, request, jsonify
from decimal import Decimal, InvalidOperation

app = Flask(__name__)

def convert_units(from_unit, to_unit, user_amount):
    try:
        amount = Decimal(user_amount)
    except (InvalidOperation, ValueError):
        return 'Invalid amount'

    if from_unit == to_unit:
        return 'Invalid conversion: Units are the same.'

    conversion_factors = {
        ('m', 'km'): Decimal('0.001'),
        ('m', 'inch'): Decimal('39.37'),
        ('m', 'cm'): Decimal('100'),
        ('m', 'mile'): Decimal('0.000621371'),

        ('km', 'm'): Decimal('1000'),
        ('km', 'mile'): Decimal('0.621'),
        ('km', 'inch'): Decimal('39370.1'),
        ('km', 'cm'): Decimal('100000'),

        ('inch', 'm'): Decimal('0.0254'),
        ('inch', 'cm'): Decimal('2.54'),
        ('inch', 'km'): Decimal('0.0000254'),
        ('inch', 'mile'): Decimal('0.00001578'),

        ('cm', 'm'): Decimal('0.01'),
        ('cm', 'km'): Decimal('0.00001'),
        ('cm', 'inch'): Decimal('0.393701'),
        ('cm', 'mile'): Decimal('0.00000621'),

        ('mile', 'km'): Decimal('1.60934'),
        ('mile', 'm'): Decimal('1609.34'),
        ('mile', 'inch'): Decimal('63360'),
        ('mile', 'cm'): Decimal('160934'),
    }

    if (from_unit, to_unit) in conversion_factors:
        result = amount * conversion_factors[(from_unit, to_unit)]
        return str(result.quantize(Decimal('0.0000')))  # Format result to 4 decimal places

    return 'Invalid conversion'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    data = request.json
    from_unit = data.get('from_unit')
    to_unit = data.get('to_unit')
    user_amount = data.get('amount')
    result = convert_units(from_unit, to_unit, user_amount)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
