function Update() {
	$('#table').hide();
	var port = $('#port').val();

	$('#h1port').hide();
	$('#res').hide()

	if (port == parseInt(port, 10)) {

		$('#display_port').html(port);

		req = $.ajax({
			url : '/port/update',
			type : 'POST',
			data : { port : port }
		});
 
		req.done(function(data){
			var c = 'bg-'.concat(data.color);
			$('#display_result').html(data.result);
			$('#display_result').addClass(c);
			$('#res').show()
			$('#h1port').show();
		});
	}
}

function scan() {
	$('#res').hide();
    $('#h1port').hide();
    $('#table').show();

	req = $.ajax({
		url : '/port/scan',
		type : 'POST',
	});
	req.done(function(data){
		for (x=0;x<9;x++) {
			id = x.toString();
			var c = 'table-'.concat(data.color[x]);
			$('#p'.concat(id)).html(data.ports[x]);
			$('#r'.concat(id)).html(data.result[x]);
			$('#s'.concat(id)).html(data.services[x]);
			$('#row'.concat(id)).addClass(c);
		}

	});

}

$( document ).ready(function() {
   	$('#res').hide();
   	$('#h1port').hide();
   	$('#table').hide();
   	$('#checkbtn').prop('disabled', true);
	$("#port").on('keyup', function(){

		$('#realtimep').html($('#port').val());
		if (realtimep != '') {
			$('#checkbtn').prop('disabled', false);
		}

		else {
			$('#checkbtn').prop('disabled', true);
		}

	});

});

function login(){
	req = $.ajax({
		url : '/login',
		type : 'POST',
	});
	req.done(function(data){
		$().alert('closed');
	});
}