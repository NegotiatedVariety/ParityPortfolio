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
        cutout: '75%',
        plugins: {
            legend: {
                display: false
            }
        }
    }
});

// Only create Target Portfolio chart if Preset data was received
if (chartValues2 != null)
{
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
            cutout: '75%',
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}

createTable = (elementId, chartValues) => {
    let tableDiv = document.getElementById(elementId);

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
        assetPercentage.innerText = ((chartValues[i] / chartTotal) * 100) + '%';

        tableDiv.appendChild(assetList);

        assetList.appendChild(assetLabel);
        assetList.appendChild(assetValue);
        assetList.appendChild(assetPercentage);
    }
}

if (showTables == "true")
{
    createTable('currentPortfolioTable', chartValues1);
    // Only create Target Portfolio table if Preset data was received
    if (chartValues2 != null)
    {
        createTable('targetPortfolioTable', chartValues2);
    }
}