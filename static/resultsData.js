let ctx1 = document.getElementById('myCurrentChart').getContext('2d');
let myCurrentChart = new Chart(ctx1, {
    type: 'doughnut',
    data: {
        labels: chartLabels,
        datasets: [{
            label: 'Assets ($)',
            data: chartValues1,
            backgroundColor: chartColors,
            hoverOffset: 4
        }]
    },
    options: {
        plugins: {
            legend: {
                display: false
            }
        }
    }
});

let ctx2 = document.getElementById('myTargetChart').getContext('2d');
let myTargetChart = new Chart(ctx2, {
    type: 'doughnut',
    data: {
        labels: chartLabels,
        datasets: [{
            label: 'Assets ($)',
            data: chartValues2,
            backgroundColor: chartColors,
            hoverOffset: 4
        }]
    },
    options: {
        plugins: {
            legend: {
                display: false
            }
        }
    }
});