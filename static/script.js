// ==========================
// JAM DIGITAL
// ==========================
function updateClock() {

    let now = new Date();

    let time = now.toLocaleTimeString('id-ID');

    document.getElementById("clock").innerHTML = time;

}

setInterval(updateClock, 1000);

updateClock();


// ==========================
// MEMBUAT GRAFIK
// ==========================
const ctx = document.getElementById('adcChart').getContext('2d');

const adcChart = new Chart(ctx, {

    type: 'line',

    data: {

        labels: [],

        datasets: [{

            label: 'Nilai ADC',

            data: [],

            borderWidth: 3,

            fill: true,

            tension: 0.4

        }]

    },

    options: {

        responsive: true,

        maintainAspectRatio: false,

        animation: false,

        scales: {

            y: {

                beginAtZero: true,

                suggestedMax: 1023

            }

        }

    }

});


// ==========================
// AMBIL DATA DARI FLASK
// ==========================
function loadChart() {

    fetch('/chart-data')

    .then(response => response.json())

    .then(data => {

        adcChart.data.labels = data.labels;

        adcChart.data.datasets[0].data = data.values;

        adcChart.update();

    });

}

loadChart();

setInterval(loadChart, 2000);


// ==========================
// AUTO REFRESH HALAMAN
// ==========================
setTimeout(function () {

    location.reload();

}, 2000);