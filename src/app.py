"""Flask web application for managing Ohtuvarasto warehouses."""
from flask import Flask, render_template, request, redirect, url_for, flash
from varasto import Varasto

app = Flask(__name__)
app.secret_key = 'dev-secret-key-change-in-production'

# In-memory storage for multiple warehouses
varastot = {}
next_id = 1


def validate_varasto_exists(varasto_id):
    """Validate that warehouse exists."""
    if varasto_id not in varastot:
        flash('Varastoa ei löydy', 'error')
        return False
    return True


def validate_amount(maara):
    """Validate amount is not negative."""
    if maara < 0:
        flash('Määrä ei voi olla negatiivinen', 'error')
        return False
    return True


@app.route('/')
def index():
    """Display home page with list of all warehouses."""
    return render_template('index.html', varastot=varastot)


@app.route('/varasto/uusi', methods=['POST'])
def create_varasto():
    """Create a new warehouse."""
    global next_id  # pylint: disable=global-statement

    try:
        nimi = request.form.get('nimi', '').strip()
        tilavuus = float(request.form.get('tilavuus', 0))
        alku_saldo = float(request.form.get('alku_saldo', 0))

        if not nimi:
            flash('Varaston nimi on pakollinen', 'error')
            return redirect(url_for('index'))

        if tilavuus < 0:
            flash('Tilavuus ei voi olla negatiivinen', 'error')
            return redirect(url_for('index'))

        if alku_saldo < 0:
            flash('Alkusaldo ei voi olla negatiivinen', 'error')
            return redirect(url_for('index'))

        varasto = Varasto(tilavuus, alku_saldo)
        varastot[next_id] = {'nimi': nimi, 'varasto': varasto}
        next_id += 1

        flash(f'Varasto "{nimi}" luotu onnistuneesti', 'success')
    except ValueError:
        flash('Virheelliset arvot. Tarkista tilavuus ja alkusaldo.', 'error')

    return redirect(url_for('index'))


@app.route('/varasto/<int:varasto_id>')
def show_varasto(varasto_id):
    """Display individual warehouse details."""
    if not validate_varasto_exists(varasto_id):
        return redirect(url_for('index'))

    varasto_data = varastot[varasto_id]
    return render_template('varasto.html',
                         varasto_id=varasto_id,
                         nimi=varasto_data['nimi'],
                         varasto=varasto_data['varasto'])


@app.route('/varasto/<int:varasto_id>/lisaa', methods=['POST'])
def lisaa_varastoon(varasto_id):
    """Add items to warehouse."""
    if not validate_varasto_exists(varasto_id):
        return redirect(url_for('index'))

    try:
        maara = float(request.form.get('maara', 0))

        if not validate_amount(maara):
            pass
        else:
            varastot[varasto_id]['varasto'].lisaa_varastoon(maara)
            flash(f'Lisättiin {maara} yksikköä varastoon', 'success')
    except ValueError:
        flash('Virheellinen määrä', 'error')

    return redirect(url_for('show_varasto', varasto_id=varasto_id))


@app.route('/varasto/<int:varasto_id>/ota', methods=['POST'])
def ota_varastosta(varasto_id):
    """Remove items from warehouse."""
    if not validate_varasto_exists(varasto_id):
        return redirect(url_for('index'))

    try:
        maara = float(request.form.get('maara', 0))

        if not validate_amount(maara):
            pass
        else:
            saatu = varastot[varasto_id]['varasto'].ota_varastosta(maara)
            flash(f'Otettiin {saatu} yksikköä varastosta', 'success')
    except ValueError:
        flash('Virheellinen määrä', 'error')

    return redirect(url_for('show_varasto', varasto_id=varasto_id))


@app.route('/varasto/<int:varasto_id>/muokkaa', methods=['POST'])
def muokkaa_varastoa(varasto_id):
    """Edit warehouse name."""
    if not validate_varasto_exists(varasto_id):
        return redirect(url_for('index'))

    uusi_nimi = request.form.get('nimi', '').strip()

    if not uusi_nimi:
        flash('Nimi ei voi olla tyhjä', 'error')
    else:
        varastot[varasto_id]['nimi'] = uusi_nimi
        flash('Varaston nimi päivitetty', 'success')

    return redirect(url_for('show_varasto', varasto_id=varasto_id))


@app.route('/varasto/<int:varasto_id>/poista', methods=['POST'])
def poista_varasto(varasto_id):
    """Delete warehouse."""
    if not validate_varasto_exists(varasto_id):
        return redirect(url_for('index'))

    nimi = varastot[varasto_id]['nimi']
    del varastot[varasto_id]
    flash(f'Varasto "{nimi}" poistettu', 'success')

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
