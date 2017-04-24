// https://remysharp.com/2010/07/21/throttling-function-calls
function debounce(fn, delay) {
    var timer = null;
    return function () {
      var context = this, args = arguments;
      clearTimeout(timer);
      timer = setTimeout(function () {
        fn.apply(context, args);
      }, delay);
    };
}

// do things with settings buttons
$("div.btn-group").change(function() {
    // front sensor auto routines
    var autostop = $("input.auto-stop").is(":checked");

    // true if checked, false if not
    if (autostop == true) {
        $.ajax({
            type: "GET",
            url: "http://192.168.2.30:5000/sensorEnable",
            dataType: "json",
        });
    } else {
        $.ajax({
            type: "GET",
            url: "http://192.168.2.30:5000/sensorDisable",
            dataType: "json",
        });
    };
});

// how many degrees off center to do nothing
var centerThresh = 12;

// initialize which mode am i in? variable
var active = false;

// bind handlers to ui buttons. also tell handler what to do
$( "a.stop" ).bind( "tap", stopHandler );
$( "a.forward" ).bind( "tap", {operation: "forward"}, pulseHandler );
$( "a.backward" ).bind( "tap", {operation: "backward"}, pulseHandler );
$( "a.spinLeft" ).bind( "tap", {operation: "spinLeft"}, pulseHandler );
$( "a.spinRight" ).bind( "tap", {operation: "spinRight"}, pulseHandler );
$( "a.rightBack" ).bind( "tap", {operation: "rightBack"}, pulseHandler );
$( "a.leftBack" ).bind( "tap", {operation: "leftBack"}, pulseHandler );

// grab default dc value
var dutyCycle = $("input#duty-cycle").val();

// when the slider is slid, do things but not too fast
$("#div-slider").change(debounce(function() {
                            // get the slider value
                            dutyCycle = $("input#duty-cycle").val();

                            // only if we're going already, then update our speed
                            if (active !== false) {
                                $.ajax({
                                  type: "GET",
                                  url: "http://192.168.2.30:5000/"+active+"/"+dutyCycle,
                                  dataType: "json",
                                });
                            };

                }, 100));

function pulseHandler( event ){
    if (active !== false) {
      stopHandler();
    };

    active = event.data.operation;

    $.ajax({
      type: "GET",
      url: "http://192.168.2.30:5000/"+active+"/"+dutyCycle,
      dataType: "json",
    });
}

function stopHandler( event ){
    active = false;

    $.ajax({
      type: "GET",
      url: "http://192.168.2.30:5000/stop",
      // data: {'seconds':'2','dutyCycle':'30'},
      // success: success,
      dataType: "json",
    });
}