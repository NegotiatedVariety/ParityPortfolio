let ctx2 = document.getElementById('myChart2').getContext('2d');
let myChart2 = new Chart(ctx2, {
    type: 'doughnut',
    data: {
        labels: chartLabels2,
        datasets: [{
            label: 'Assets ($)',
            data: chartValues2,
            backgroundColor: chartColors2,
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
    let tableDiv = document.getElementById('targetPortfolioTable');

    for (let i = 0; i < chartLabels2.length; i++) {
        let assetList = document.createElement('ul');
        assetList.className = 'targetPortfolioList';
        assetList.style.borderLeft = '10px solid' + chartColors2[i];

        let assetLabel= document.createElement('li');
        assetLabel.innerText = chartLabels2[i];

        
        let assetValue = document.createElement('li');
        assetValue.innerText = '$' + chartValues2[i].toFixed(2);

        tableDiv.appendChild(assetList);

        assetList.appendChild(assetLabel);     
        assetList.appendChild(assetValue);
    }
}

createTable();