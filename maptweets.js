var markerList = [];
var map;
var time;

function initialize() {
    time = new Date().getTime()/1000;
    var lat=78;
    var longi=37.5;
    var myFirebaseRef = new Firebase("https://prepel.firebaseio.com/"); //events");
    var myLatlng = new google.maps.LatLng(lat,longi);
    var mapOptions = {
        zoom: 4,
        center: myLatlng
    };
    map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
    myFirebaseRef.on('child_added', function(snapshot) {

        lat = snapshot.child("Lat").val();
        longi = snapshot.child("Long").val();
        keywords = snapshot.child("Text").val();
        timee = snapshot.child("Timestamp").val();
/*
        var temppos = new google.maps.LatLng(lat,longi);
        var image = 'event.png';
        var tempmarker = new google.maps.Marker( {
            position: temppos,
            map: map,
            title: "event",
            icon: image,
            zIndex: timee
            });

        var tempinfo = new google.maps.InfoWindow({
            content: keywords
        });
        google.maps.event.addListener(tempmarker, 'click', function() {
            tempinfo.open(map,tempmarker)
        });

        markerList.push(tempmarker);
*/
       eventToTweetArray(snapshot,map);
    });
}

var interval = setInterval(function () { updater(map) }, 500);

function eventToTweetArray(tweet, map) {
            lat = tweet.child("Lat").val();
            longi = tweet.child("Long").val();
            tweet_html = tweet.child("ID").val();
            tweet_html = '<blockquote class="twitter-tweet" lang="en"><p>text</p>(@usr) <a href="https://twitter.com/ust/status/' + tweet_html + '></a></blockquote><script async src="\/\/platform.twitter.com/widgets.js" charset="utf-8"><\/script>';
            time = tweet.child("Timestamp").val();
            var temppos = new google.maps.LatLng(lat,longi);
            var image = 'light.png';
            var tempmarker = new google.maps.Marker( {
                position: temppos,
                map: map,
                title: "tweet",
                icon: image,
                zIndex: timee
                });
            var wrapper = document.createElement("div");
            wrapper.innerHTML = tweet_html;
            wrapper.className = "map-popup";
            wrapper.style.height="20em";
            wrapper.style.width="45em";
	    var infowindow = new google.maps.InfoWindow({
    		  content: wrapper, 
            });	

            google.maps.event.addListener(infowindow, 'domready', function () {
                    ! function (d, s, id) {
                        var js, fjs = d.getElementsByTagName(s)[0];
                 //       if (d.getElementById(id)) {
		//		d.getElementById(id).parentNode.removeChild(d.getElementById(id));
		//	}
                        js = d.createElement(s);
                        js.id = id;
                        js.src = "//platform.twitter.com/widgets.js";
                       	js.parentNode.insertBefore(js, fjs);
                    }(document, "script", "twitter-wjs");
            });
            google.maps.event.addListener(tempmarker, 'click', function() {
		infowindow.open(map, tempmarker);
            });
            markerList.push(tempmarker);
}

function updater(map) {
    var arrayLength = markerList.length;
    for(var i = 0; i < arrayLength; i++) {
        if(time < markerList[i].zIndex || time > markerList[i].zIndex + 7200) {
            if(markerList[i].getMap() !== null){
                markerList[i].setMap(null);
            }
        } else{
            if(!markerList[i].getMap()){
                markerList[i].setMap(map);
            }
        }
    }
}

function showvalue(newValue) {
    time = newValue;
}

google.maps.event.addDomListener(window, 'load', initialize); // Run initalize on window load
