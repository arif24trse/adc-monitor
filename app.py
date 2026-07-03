from flask import Flask, render_template, request, jsonify, Response, redirect
import mysql.connector
import csv
import io
import random

app = Flask(__name__)

# ==========================
# Koneksi MySQL
# ==========================
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="adc_monitor"
)

# ==========================
# Dashboard
# ==========================
@app.route('/')
def index():

    cursor = db.cursor()

    cursor.execute("""
        SELECT *
        FROM sensor_data
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    latest = 0

    if len(data) > 0:
        latest = data[0][1]

    total = len(data)

    cursor.close()

    return render_template(
        "index.html",
        data=data,
        latest=latest,
        total=total
    )


# ==========================
# API Arduino / ESP32
# ==========================
@app.route('/api/adc', methods=['POST'])
def receive_adc():

    data = request.get_json()

    adc = data["adc"]

    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO sensor_data(adc_value) VALUES(%s)",
        (adc,)
    )

    db.commit()

    cursor.close()

    return jsonify({
        "status": "success"
    })


# ==========================
# TEST DATA RANDOM
# ==========================
@app.route('/test')
def test():

    adc = random.randint(0, 1023)

    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO sensor_data(adc_value) VALUES(%s)",
        (adc,)
    )

    db.commit()

    cursor.close()

    return f"Data ADC {adc} berhasil dimasukkan"


# ==========================
# DATA GRAFIK
# ==========================
@app.route('/chart-data')
def chart_data():

    cursor = db.cursor()

    cursor.execute("""
        SELECT id, adc_value
        FROM sensor_data
        ORDER BY id ASC
        LIMIT 20
    """)

    rows = cursor.fetchall()

    cursor.close()

    labels = []
    values = []

    for row in rows:
        labels.append(row[0])
        values.append(float(row[1]))

    return jsonify({
        "labels": labels,
        "values": values
    })


# ==========================
# DOWNLOAD CSV
# ==========================
@app.route('/download')
def download():

    cursor = db.cursor()

    cursor.execute("""
        SELECT *
        FROM sensor_data
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "ID",
        "ADC",
        "Waktu"
    ])

    for row in rows:
        writer.writerow(row)

    cursor.close()

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=adc_data.csv"
        }
    )


# ==========================
# HAPUS DATA
# ==========================
@app.route('/delete')
def delete():

    cursor = db.cursor()

    cursor.execute("DELETE FROM sensor_data")

    db.commit()

    cursor.close()

    return redirect('/')


# ==========================
# Jalankan Flask
# ==========================
if __name__ == '__main__':
    app.run(debug=True)