var Experiment = function () {
    this.test = "TEST";
    that = this;
    that.uploadReady = false;
    $("#invite").hide();
    $("#message").show();
    this.registerListeners = function () {
        // nothing to register here.
    }
    this.checkUploadFileStatus = function () {
        that.uploadReady = false;
        console.log("inside checkUploadFileStatus, test: " + that.test);
        $.ajax({
            type: "GET",
            url: SITE_DEFAULTS.baseurl+'/pf/exp/' + experiment_id + '/getUploadStatus',
            data: {
                'csrfmiddlewaretoken': csrftoken
            },
            dataType: 'json',
            success: function (data) {
                console.log(data["message"]);
                if (data["message"] === "PENDING") {
                    // do nothing.
                } else {
                    that.uploadReady = true;
                    $("#message").hide();
                    $("#invite").show();
                }

            },
            error: function (request, status, error) {
                console.log(request.responseText);
                that.uploadReady = false;
            }
        });
    }
}
console.log("HERE")
exp = new Experiment();
exp.registerListeners();
time = 5000;
console.log("POLLING")

function checkFlag() {
    console.log("POLLING time: " + time + ", exp.uploadReady: " + exp.uploadReady);
    if(!exp.uploadReady) {
        exp.checkUploadFileStatus();
        window.setTimeout(checkFlag, time); /* this checks the flag every time milliseconds*/
        time +=2000;
    } else {
        console.log("upload complete");
    }
}
checkFlag();
