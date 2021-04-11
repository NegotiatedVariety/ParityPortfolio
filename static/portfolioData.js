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
            legend: {
                display: false
            }
        }
    }
});

createTable = () => {
    let tableDiv = document.getElementById('currentPortfolioTable');

    for (let i = 0; i < chartLabels.length; i++) {
        let assetList = document.createElement('ul');
        assetList.className = 'currentPortfolioList';
        assetList.style.borderLeft = '10px solid' + chartColors[i];

        let assetLabel= document.createElement('li');
        assetLabel.innerText = chartLabels[i];

        
        let assetValue = document.createElement('li');
        assetValue.innerText = '$' + chartValues[i];

        tableDiv.appendChild(assetList);

        assetList.appendChild(assetLabel);     
        assetList.appendChild(assetValue);
    }
}

createTable();