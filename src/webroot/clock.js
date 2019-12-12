
function update_form(data) {
	$('#brightness').val(data.brightness)
	if(data.am_pm) {
		$('#am_pm').prop('checked',true)
	} else {
		$('#24_hour').prop('checked',true)
	}
	$('#displays').empty()
	$('#displays').append('<label>Time Mode</label>')
	for(var x=0;x<data.displays.length;++x) {
		$('#displays').append('<br>')
		$('#displays').append("<input type='radio' id='disp_"+x+"' name='display' value='"+x+"' onchange='send_change({display_num:"+x+"})'>")
		$('#displays').append("<label for=disp_"+x+">&nbsp;"+data.displays[x]+"</label>")
	}
	$('#disp_'+data.display_num).prop('checked',true)
}

function send_change(changes) {
	var qp = "?"
	var keys = Object.keys(changes)
	for(var x=0;x<keys.length;++x) {
		qp = qp+keys[x]+'='+changes[keys[x]]
		if(x!=keys.length-1) {
			qp = qp + '&'
		}
	}
	
	$.get('/clock'+qp, update_form)
}

$(function() {
	
	$.get('/clock', update_form)
	
})