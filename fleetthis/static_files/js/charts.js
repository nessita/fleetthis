function mod(a, b) {
    return ((a % b) + b) % b;
}


function get_current_month() {
    var date = new Date();
    var month = date.getMonth() + 1;  // January is 0
    return month;
}

function slide_date_data(data) {
    var month = get_current_month();

    /* update month index to show last 12 months in order,
     * according to current month */
    for (var i = 0; i < data.length; i++){
        data[i][0] = mod(data[i][0] - month, 12) + 1;
    }
    return data;
}


function consumption_chart(container_id, title, data, penalties) {
    var current_month = get_current_month();
    var data = slide_date_data(data);
    var penalties = slide_date_data(penalties);

    var m1 = [], m2 = [];
    for(var i = 0; i < data.length; i++){
        m1.push([data[i][0], data[i][1]]);
        m2.push([penalties[i][0], (data[i][1] + penalties[i][1]]).toFixed(2));
    }

    var container = document.getElementById(container_id);
    var graph = Flotr.draw(container, [{
            data: data,
            label: "Used"
        }, {
            data: penalties,
            label: "Penalty"
        }, {
            data: m1,
            bars: {
                show: false
            },
            markers: {
                show: true,
                labelFormatter: function(obj){
                                    return data[obj.index][1];
                                }
            }
        }, {
            data: m2,
            bars: {
                show: false
            },
            markers: {
                show: true,
                labelFormatter: function(obj){
                                    return data[obj.index][1] + penalties[obj.index][1];
                                }
            }
        }], {
            legend: {
                backgroundColor: "#D2E8FF",
                backgroundOpacity: 0.25,
                position: 'sw'
            },
            title: title,
            colors: ['#357703', '#D50606'],
            yaxis: {
              min: 0,
              tickDecimals: 0
            },
            xaxis: {
                min: current_month - 1,
                noTicks: 12,
                tickFormatter: function(x) {
                    var x = parseInt(x);
                    var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
                    return months[((x - 1) + (current_month - 1)) % 12];
                }
            },
            bars: {
                show: true,
                stacked: true,
                horizontal: false,
                barWidth: 0.6,
                lineWidth: 1,
                shadowSize: 0
            },
            grid: {
                verticalLines: false,
                horizontalLines: true
            }
        }
    );
    return graph;
}
