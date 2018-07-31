// Define on click event.
$('#table').on("click-row.bs.table", (e, row, $element, field) => {
    // Get row number first.
    var index = $element.data('index');

    // Expand the target row if the row is not selected, otherwise collapse it.
    if (!row.state) {

        // Expand the detail row first in order to reveal the email-chart div.
        $('#table').bootstrapTable('expandRow', index);

    }
    else {
        $('#table').bootstrapTable('collapseRow', index);
    }

});

// Handle event when user check all rows on the current page.
$('#table').on("check-all.bs.table", (e, rows) => {
    $('#table').bootstrapTable('expandAllRows');
});

// Handle event when user uncheck all rows on the current page.
$('#table').on("uncheck-all.bs.table", (e, rows) => {
    $('#table').bootstrapTable('collapseAllRows');
});

// Handle event when user expand one row.
$('#table').on("expand-row.bs.table", (e, index, row, $detail) => {


//    alert(111);
	// Highlight the keywords in the target email body.
	var detailDiv = document.getElementById('email-detail' + index);
	var detailContents = detailDiv.innerHTML;

	// Split the detail contents into arrays by keywords.
	var keywords = row.keywords.split(',');
//	alert(keywords)



	for (keyword of keywords) {
	    if(keyword != ","){
	    var detailSplitArray = detailContents.split(keyword);

		detailContents = detailSplitArray.join('<span style="background:yellow;">' + keyword + '</span>');
	}
		}

	detailDiv.innerHTML = detailContents;

    // Draw the echart for the target email.
    var myChart = echarts.init(document.getElementById('email-chart' + index));

    var option = {
        title: {
            text: 'WATSON NLU Analysis Results',
            subtext: 'for the current email',
            x: 'center'
        },
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
            orient: 'vertical',
            left: 'left',
            data: ['Sadness', 'Joy', 'Fear', 'Disgust', 'Anger']
        },
        series: [
            {
                name: 'Emotion Results',
                type: 'pie',
                radius: '55%',
                center: ['50%', '60%'],
                data: [
                    { value: row.sadness, name: 'Sadness' },
                    { value: row.joy, name: 'Joy' },
                    { value: row.fear, name: 'Fear' },
                    { value: row.disgust, name: 'Disgust' },
                    { value: row.anger, name: 'Anger' }
                ],
                itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };

    myChart.setOption(option);
});
