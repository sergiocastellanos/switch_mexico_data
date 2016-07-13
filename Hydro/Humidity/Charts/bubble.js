var DEFAULT_DATASET_SIZE = 7;
var winter1 = {x: 0, y: 0.683513071838, r: 5.68351307184, };
var winter2 = {x: 0, y: 0.34647942715, r: 5.34647942715, };
var winter3 = {x: 0, y: 0.0376785950422, r: 5.03767859504, };
var winter4 = {x: 0, y: 0.656914181747, r: 5.65691418175, };
var winter5 = {x: 0, y: 0.0, r: 5.0, };
var winter6 = {x: 0, y: 0.912709456895, r: 5.91270945689, };
var winter7 = {x: 0, y: 1.0, r: 6.0, };
var winter8 = {x: 0, y: 0.069736591561, r: 5.06973659156, };
var winter9 = {x: 0, y: 0.989930630348, r: 5.98993063035, };
var winter10 = {x: 0, y: 0.442990280026, r: 5.44299028003, };
var spring1 = {x: 0.0, y: 0.53392099157, r: 5.53392099157, };
var spring2 = {x: 0.352601156069, y: 0.0, r: 5.0, };
var spring3 = {x: 0.0115606936416, y: 1.0, r: 6.0, };
var spring4 = {x: 0.335260115607, y: 0.233691566366, r: 5.23369156637, };
var spring5 = {x: 0.173410404624, y: 0.0311881527728, r: 5.03118815277, };
var spring6 = {x: 0.0578034682081, y: 0.42124797438, r: 5.42124797438, };
var spring7 = {x: 0.028901734104, y: 0.64984050833, r: 5.64984050833, };
var spring8 = {x: 0.734104046243, y: 0.220120093446, r: 5.22012009345, };
var spring9 = {x: 1.0, y: 0.657101759181, r: 5.65710175918, };
var spring10 = {x: 0.0, y: 0.573199117052, r: 5.57319911705, };
var summer1 = {x: 0.111111111111, y: 0.478876131088, r: 5.47887613109, };
var summer2 = {x: 0.177777777778, y: 0.0880759160239, r: 5.08807591602, };
var summer3 = {x: 0.388888888889, y: 0.68131407681, r: 5.68131407681, };
var summer4 = {x: 0.0, y: 0.257890941369, r: 5.25789094137, };
var summer5 = {x: 0.933333333333, y: 1.0, r: 6.0, };
var summer6 = {x: 0.322222222222, y: 0.614897464955, r: 5.61489746495, };
var summer7 = {x: 0.466666666667, y: 0.40825584626, r: 5.40825584626, };
var summer8 = {x: 0.6, y: 0.433685863941, r: 5.43368586394, };
var summer9 = {x: 0.5, y: 0.49356676047, r: 5.49356676047, };
var summer10 = {x: 1.0, y: 0.0, r: 5.0, };
var autumn1 = {x: 0.0, y: 0.390789000295, r: 5.39078900029, };
var autumn2 = {x: 0.583333333333, y: 0.0598222977986, r: 5.0598222978, };
var autumn3 = {x: 0.0, y: 0.607933309844, r: 5.60793330984, };
var autumn4 = {x: 0.0, y: 0.0504345945672, r: 5.05043459457, };
var autumn5 = {x: 0.0, y: 1.0, r: 6.0, };
var autumn6 = {x: 0.25, y: 0.897032215566, r: 5.89703221557, };
var autumn7 = {x: 0.0, y: 0.219841952194, r: 5.21984195219, };
var autumn8 = {x: 1.0, y: 0.48851721952, r: 5.48851721952, };
var autumn9 = {x: 0.0833333333333, y: 0.310489388547, r: 5.31048938855, };
var autumn10 = {x: 0.333333333333, y: 0.0, r: 5.0, };



var addedCount = 0;

var randomScalingFactor = function() {
    return (Math.random() > 0.5 ? 1.0 : -1.0) * Math.round(Math.random() * 100);
};
var randomColorFactor = function() {
    return Math.round(Math.random() * 255);
};
var randomColor = function() {
    return 'rgba(' + randomColorFactor() + ',' + randomColorFactor() + ',' + randomColorFactor() + ',.7)';
};


var uno = randomColor();
var dos = randomColor();
var tres = randomColor();
var cuatro = randomColor();
var cinco = randomColor();
var seis = randomColor();
var siete = randomColor();
var ocho = randomColor();
var nueve = randomColor();
var diez = randomColor();

var autumn = {
    animation: {
        duration: 10000
    },
    datasets: [{
        label: "2006",
        backgroundColor: uno,
        data: [autumn1]
    },
    {
        label: "2007",
        backgroundColor: dos,
        data: [autumn2]
    },
    {
        label: "2008",
        backgroundColor: tres,
        data: [autumn3]
    },
    {
        label: "2009",
        backgroundColor: cuatro,
        data: [autumn4]
    },
    {
        label: "2010",
        backgroundColor: cinco,
        data: [autumn5]
    },
    {
        label: "2011",
        backgroundColor: seis,
        data: [autumn6]
    },
    {
        label: "2012",
        backgroundColor: siete,
        data: [autumn7]
    },
    {
        label: "2013",
        backgroundColor: ocho,
        data: [autumn8]
    },
    {
        label: "2014",
        backgroundColor: nueve,
        data: [autumn9]
    },
    {
        label: "2015",
        backgroundColor: diez,
        data: [autumn10,
          {x: .6, y:1.000022 , r: .0001, },
          {x: -.00000000000000001, y:-.000022 , r: .0001, }
        ]
    }]
};

var summer = {
    animation: {
        duration: 10000
    },
    datasets: [{
        label: "2006",
        backgroundColor: uno,
        data: [summer1]
    },
    {
        label: "2007",
        backgroundColor: dos,
        data: [summer2]
    },
    {
        label: "2008",
        backgroundColor: tres,
        data: [summer3]
    },
    {
        label: "2009",
        backgroundColor: cuatro,
        data: [summer4]
    },
    {
        label: "2010",
        backgroundColor: cinco,
        data: [summer5]
    },
    {
        label: "2011",
        backgroundColor: seis,
        data: [summer6]
    },
    {
        label: "2012",
        backgroundColor: siete,
        data: [summer7]
    },
    {
        label: "2013",
        backgroundColor: ocho,
        data: [summer8]
    },
    {
        label: "2014",
        backgroundColor: nueve,
        data: [summer9]
    },
    {
        label: "2015",
        backgroundColor: diez,
        data: [summer10,
          {x: .6, y:1.000022 , r: .0001, },
          {x: -.00000000000000001, y:-.000022 , r: .0001, }
        ]
    }]


};



var spring = {
    animation: {
        duration: 10000
    },
    datasets: [{
        label: "2006",
        backgroundColor: uno,
        data: [spring1]
    },
    {
        label: "2007",
        backgroundColor: dos,
        data: [spring2]
    },
    {
        label: "2008",
        backgroundColor: tres,
        data: [spring3]
    },
    {
        label: "2009",
        backgroundColor: cuatro,
        data: [spring4]
    },
    {
        label: "2010",
        backgroundColor: cinco,
        data: [spring5]
    },
    {
        label: "2011",
        backgroundColor: seis,
        data: [spring6]
    },
    {
        label: "2012",
        backgroundColor: siete,
        data: [spring7]
    },
    {
        label: "2013",
        backgroundColor: ocho,
        data: [spring8]
    },
    {
        label: "2014",
        backgroundColor: nueve,
        data: [spring9]
    },
    {
        label: "2015",
        backgroundColor: diez,
        data: [spring10,
          {x: .6, y:1.000022 , r: .0001, },
          {x: -.00000000000000001, y:-.000022 , r: .0001, }
        ]
    }]
};


var winter = {
    animation: {
        duration: 10000
    },
    datasets: [{
        label: "2006",
        backgroundColor: uno,
        data: [winter1]
    },
    {
        label: "2007",
        backgroundColor: dos,
        data: [winter2]
    },
    {
        label: "2008",
        backgroundColor: tres,
        data: [winter3]
    },
    {
        label: "2009",
        backgroundColor: cuatro,
        data: [winter4]
    },
    {
        label: "2010",
        backgroundColor: cinco,
        data: [winter5]
    },
    {
        label: "2011",
        backgroundColor: seis,
        data: [winter6]
    },
    {
        label: "2012",
        backgroundColor: siete,
        data: [winter7]
    },
    {
        label: "2013",
        backgroundColor: ocho,
        data: [winter8]
    },
    {
        label: "2014",
        backgroundColor: nueve,
        data: [winter9]
    },
    {
        label: "2015",
        backgroundColor: diez,
        data: [winter10,
          {x: .6, y:1.000022 , r: .0001, },
          {x: -.00000000000000001, y:-.000022 , r: .0001, }
        ]
    }]
};

window.onload = function() {
    var ctx1 = document.getElementById("autumn").getContext("2d");
    window.myChart = new Chart(ctx1, {
        type: 'bubble',
        data: autumn,
        options: {
            responsive: true,
            title:{
                display:true,
                text:'Production - Precip Accumulation'
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Precip Accumulation'
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Production'
                    }
                }]
            }
        }
    });
    var ctx2 = document.getElementById("summer").getContext("2d");
    window.myChart = new Chart(ctx2, {
        type: 'bubble',
        data: summer,
        options: {
            responsive: true,
            title:{
                display:true,
                text:'Production - Precip Accumulation'
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Precip Accumulation'
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Production'
                    }
                }]
            }
        }
    });
    var ctx3 = document.getElementById("spring").getContext("2d");
    window.myChart = new Chart(ctx3, {
        type: 'bubble',
        data: spring,
        options: {
            responsive: true,
            title:{
                display:true,
                text:'Production - Precip Accumulation'
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Precip Accumulation'
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Production'
                    }
                }]
            }
        }
    });
    var ctx4 = document.getElementById("winter").getContext("2d");
    window.myChart = new Chart(ctx4, {
        type: 'bubble',
        data: winter,
        options: {
            responsive: true,
            title:{
                display:true,
                text:'Production - Precip Accumulation'
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Precip Accumulation'
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Production'
                    }
                }]
            }
        }
    });

};
