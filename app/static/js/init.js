for(var i = 1; i <= parseInt($('section').attr('aria-label')); i++){
	var uh = $('#playBtn-'+i)
	$(uh).click(function(){
		var str = $(this).attr('aria-label');
		$('#ap').attr('src', str);
		$('#ap').attr('aria-valuenow', true);
	});
}

$('#playPause').click(function() {
    if($('#ap').attr('aria-valuenow') == "true"){
        $('#ap').attr('aria-valuenow', false);
        document.getElementById("ap").pause();
    }else{
        $('#ap').attr('aria-valuenow', true);
        document.getElementById("ap").play();
    }
});

$('#closeStop').click(function(){
	$('#ap').attr('aria-valuenow', false);
	$('#ap').attr('src', '');
});

$('#ap').on('timeupdate', function() {
        var demo = ((this.currentTime / this.duration) * 100)

        var remainingTime = this.duration - this.currentTime;
        var floorDuration = Math.floor(this.duration)
        var minutes = Math.floor(this.currentTime / 60);
        var seconds = Math.floor(this.currentTime % 60);

        if(seconds < 10){
            seconds = '0' + seconds;
        }
        if(minutes < 10){
            minutes = '0' + minutes;
        }

        var dur = minutes + ":" + seconds;

        $('#progressBarr').attr("aria-valuenow", demo);
        $('#progressBarr').attr("style", "width: " + demo + "%;");
        $('#showTime').html(dur);
    });

$('#rangeInput').change(function() {
        $('#ap').prop("volume", this.value);
    });