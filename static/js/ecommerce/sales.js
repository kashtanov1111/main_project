$(document).ready(function(){

    function renderChart(id, data, labels){
        const ctx = document.getElementById(id);
        const myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Sales',
                    data: data,
                    backgroundColor: 'rgba(75, 13, 132, 0.3)',
                    borderColor: 'rgba(75, 13, 132, 1)',
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
            }
        });
    }
    
    
    function getSalesData(id, type){
        var url = '/analytics/sales/data/'
        var method = 'get'
        var data = {'type': type}
        $.ajax({
            url: url,
            method: method,
            data: data,
            success: function(responseData){
                renderChart(id, responseData.data, responseData.labels)
            },
            error: function(error){
                console.log('An error occured')
            }
        })
    }

    var chartsToRender = $('.cfe-render-chart')

    $.each(chartsToRender, function(index, html){
        var $this = $(this)
        if ( $this.attr('id'), $this.attr('data-type') ){
            getSalesData($this.attr('id'), $this.attr('data-type'))
        }

    })

})