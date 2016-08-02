var MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
var MM = [17,16,12,32,81,197,174,191,201,103,38,22];
var SEIS = [78.4, 47.3, 32.2, 49.2, 229.7, 447, 356.7, 285.1, 339.4, 323.5, 94.4, 71.3];
var SIETE = [104, 31.6, 33.4, 58.5, 148, 256.6, 279.3, 459.1, 368.3, 503.2, 41.4, 19.2];
var OCHO = [69.9, 50.6, 33.3, 90.8, 203.2, 431.3, 390, 315.8, 486, 224.2, 25.8, 34];
var NUEVE = [47, 18.5, 29, 27, 168.1, 369, 214.5, 333.7, 300, 245.9, 142, 58.4];
var DIEZ = [45.1, 17.8, 14.8, 70.4, 186.4, 507.5, 395.1, 756.7, 559.5, 58.4, 89.9, 28.7];
var ONCE = [46, 37.1, 84.3, 74.2, 149.5, 300.6, 458.5, 433.7, 422.3, 273.7, 58.8, 42.9];
var DOCE = [53.3, 38.6, 58.2, 57.8, 181.1, 264, 211.8, 418.1, 321.3, 194.4, 29, 57.7];
var TRECE = [59, 16.9, 15.7, 29.6, 214.6, 339.3, 248.4, 309.9, 394.9, 299.5, 193.2, 157.8];
var CATORCE = [67, 20, 38, 94, 262, 348, 150, 226, 462, 292, 80, 19];
var QUINCE = [83, 31, 53, 81, 127, 207, 135, 197, 341, 247, 150, 91];


var randomScalingFactor = function() {
    return Math.round(Math.random() * 100);
    //return 0;
};
var randomColorFactor = function() {
    return Math.round(Math.random() * 255);
};
var randomColor = function(opacity) {
    return 'rgba(' + randomColorFactor() + ',' + randomColorFactor() + ',' + randomColorFactor() + ',' + (opacity || '.3') + ')';
};

var config = {
    type: 'line',
    data: {
        labels: MONTHS,
        datasets: [{
            label: "Datos Historicos",
            data: MM,
            fill: false,
            borderDash: [5, 5],
        }, {
            hidden: true,
            label: '2006',
            data: SEIS,
        }, {
            label: "My Second dataset",
            data: SIETE,
        }, {
            label: "My Second dataset",
            data: OCHO,
        }, {
            label: "My Second dataset",
            data: NUEVE,
        }, {
            label: "My Second dataset",
            data: DIEZ,
        }, {
            label: "My Second dataset",
            data: ONCE,
        }, {
            label: "My Second dataset",
            data: DOCE,
        }, {
            label: "My Second dataset",
            data: TRECE,
        }, {
            label: "My Second dataset",
            data: CATORCE,
        }, {
            label: "My Second dataset",
            data: QUINCE,
        }]
    },
    options: {
        responsive: true,
        title:{
            display:true,
            text:'Chart.js Line Chart'
        },
        tooltips: {
            mode: 'label',
            callbacks: {
            }
        },
        hover: {
            mode: 'dataset'
        },
        scales: {
            xAxes: [{
                display: true,
                scaleLabel: {
                    show: true,
                    labelString: 'Month'
                }
            }],
            yAxes: [{
                display: true,
                scaleLabel: {
                    show: true,
                    labelString: 'Value'
                },
                ticks: {
                    suggestedMin: -10,
                    suggestedMax: 250,
                }
            }]
        }
    }
};

$.each(config.data.datasets, function(i, dataset) {
    dataset.borderColor = randomColor(0.4);
    dataset.backgroundColor = randomColor(0.5);
    dataset.pointBorderColor = randomColor(0.7);
    dataset.pointBackgroundColor = randomColor(0.5);
    dataset.pointBorderWidth = 1;
});

window.onload = function() {
    var ctx = document.getElementById("canvas").getContext("2d");
    window.myLine = new Chart(ctx, config);
};
