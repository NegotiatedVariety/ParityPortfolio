let ctx = document.getElementById('myChart').getContext('2d');
let myChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: chartLabels,
        datasets: [{
            label: 'Assets ($)',
            data: chartValues,
            backgroundColor: chartColors,
            hoverOffset: 4
        }]
    },
    options: {
        plugins: {
            title: {
                text: chartTitle,
                display: true
            }
        }
    }
});

