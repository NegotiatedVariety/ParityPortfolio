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
        cutout: '75%',
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
        assetList.style.border = '1px solid lightgray';
        assetList.style.borderLeft = '10px solid' + chartColors[i];


        let assetLabel= document.createElement('li');
        assetLabel.innerText = chartLabels[i];

        
        let assetValue = document.createElement('li');
        assetValue.innerText = '$' + chartValues[i].toFixed(2);

        let assetPercentage = document.createElement('li');
        assetPercentage.innerText = ((chartValues[i] / chartTotal) * 100).toFixed(1) + '%' + ' / ' + ((targetValues[i] / chartTotal) * 100).toFixed(1) + '%';

        tableDiv.appendChild(assetList);

        assetList.appendChild(assetLabel);     
        assetList.appendChild(assetValue);
        assetList.appendChild(assetPercentage);
    }
}

getAccountDetails = () => {
    let totalValue = document.getElementById('currentValue');
    totalValue.innerText = '$' + chartTotal;
    
}

createTable();
getAccountDetails();