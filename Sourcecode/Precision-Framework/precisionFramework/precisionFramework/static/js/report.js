var Report = function(){
    that = this;
    this.registerListeners = function(){
    }

    this.isExperiemntComplete = function(){
        that = this;
        $.ajax({
                type: "GET",
                url: SITE_DEFAULTS.baseurl+'/pf/exp/'+experiment_id+'/isexperimentcomplete',
                data: {
                  'csrfmiddlewaretoken':csrftoken
                },
                dataType: 'json',
                success: function (data) {
                    console.log(data["message"]);
                    if (data.message==="success"){
                        that.addReportButton(experiment_id);
                    }
                },
                error: function (request, status, error) {
                    //console.log(request.responseText);
                    //$("#msgLabel").text(request.responseJSON.message)


                }
            });
    }

    this.addReportButton = function(text) {

        var row_header = '<div class="row align-items-start">';
        var text_col = '<div class="col-lg-3"><p></p></div>'
        var url = SITE_DEFAULTS.baseurl+  "/pf/exp/" + text + "/genReport";
        var link = '<div class="col-lg-offset-6"><a class="btn btn-primary btn-lg" href="'+url+'">View Aggregated Report &raquo;</a></div>';
        var row_footer = '</div><hr>';
        var html_element = row_header + text_col + link + row_footer ;
        $("#detailed_report_div").append(html_element);
        //$("#invitedJudgesList ul").html('<li>' + text+ '</li>');
    }
}

report = new Report();
report.registerListeners();
report.isExperiemntComplete();
