var Home = function(){
    that = this;
    that.judgesInvited=0;
    $("#lockExpDiv").hide();
    $("#startExpDiv").hide();
    this.registerListeners = function(){
    }
    this.getPendingExperiments = function(){
        that = this;
        $.ajax({
                type: "GET",
                url: SITE_DEFAULTS.baseurl+'/pf/exp/pending',
                data: {
                  'csrfmiddlewaretoken':csrftoken
                },
                dataType: 'json',
                success: function (data) {
                    console.log(data["message"]);
                    if (data.message==="success"){
                        experiment_ids =  data["experiment_ids"];
                        experiment_details =  data["experiment_details"];
                        if(experiment_ids.length >0){
                            for (var i=0;i<experiment_ids.length;i++) {
                                //that.addPendingExps(experiment_ids[i]);
                                that.addPendingExps(experiment_ids[i], experiment_details[i]);
                                //console.log(experiment_ids[i]);
                            }
                        }
                    }
                },
                error: function (request, status, error) {
                    //console.log(request.responseText);
                    //$("#msgLabel").text(request.responseJSON.message)


                }
            });
    }
    this.addPendingExps = function(text, detail){
        //var li = $("<li>").html(text);
        //$("#invitedJudgesList ul").append(li)

        var url = SITE_DEFAULTS.baseurl+"/pf/exp/"+text+"/experimentaction";

        var row_header = '<div class="row align-items-start">';
        var text_col = '<div class="col-lg-3"><p>'+detail+'</p></div>'

        var link = '<div class="col-lg-offset-6"><a class="btn btn-primary btn-sm" href="'+url+'">Evaluate &raquo;</a></div>';


        var row_footer = '</div><hr>';

        var html_element = row_header + text_col + link + row_footer ;

        $("#pendingExperiments").append(html_element );
        //$("#invitedJudgesList ul").html('<li>' + text+ '</li>');
    }
    this.getUnlockedExperiments = function(){
        that = this;
        $.ajax({
                type: "GET",
                url: SITE_DEFAULTS.baseurl+'/pf/exp/unlocked',
                data: {
                  'csrfmiddlewaretoken':csrftoken
                },
                dataType: 'json',
                success: function (data) {
                    console.log(data["message"]);
                    if (data.message==="success"){
                        experiment_ids =  data["experiment_ids"];
                        experiment_details =  data["experiment_details"];
                        if(experiment_ids.length >0){
                            for (var i=0;i<experiment_ids.length;i++) {
                                //that.addUnlockedExps(experiment_ids[i]);
                                that.addUnlockedExps(experiment_ids[i], experiment_details[i]);
                                //console.log(experiment_ids[i]);
                            }
                        }
                    }
                },
                error: function (request, status, error) {
                    //console.log(request.responseText);
                    //$("#msgLabel").text(request.responseJSON.message)


                }
            });
    }
    this.addUnlockedExps = function(text, detail){
        //var li = $("<li>").html(text);
        //$("#invitedJudgesList ul").append(li)

        var row_header = '<div class="row align-items-start">';
        var text_col = '<div class="col-lg-6"><p>'+detail+'</p></div>'

        var url = SITE_DEFAULTS.baseurl+"/pf/judge/"+text+"/new";
        var link = '<div class="col-lg-offset-6"><a class="btn btn-primary btn-sm" href="'+url+'">Complete Setup &raquo;</a></div>';

        var row_footer = '</div><hr>';

        var html_element = row_header + text_col + link + row_footer ;

        $("#unlockedExperiments ").append(html_element );
        //$("#invitedJudgesList ul").html('<li>' + text+ '</li>');
    }
    this.getCompletedExperiments = function(){
        that = this;
        $.ajax({
                type: "GET",
                url: SITE_DEFAULTS.baseurl+'/pf/exp/completed',
                data: {
                  'csrfmiddlewaretoken':csrftoken
                },
                dataType: 'json',
                success: function (data) {
                    console.log(data["message"]);
                    if (data.message==="success"){
                        experiment_ids =  data["experiment_ids"];
                        experiment_details =  data["experiment_details"];
                        if(experiment_ids.length >0){
                            for (var i=0;i<experiment_ids.length;i++) {
                                that.addCompletedExps(experiment_ids[i], experiment_details[i]);
                                //console.log(experiment_ids[i]);
                            }
                        }
                    }
                },
                error: function (request, status, error) {
                    //console.log(request.responseText);
                    //$("#msgLabel").text(request.responseJSON.message)


                }
            });
    }
    this.addCompletedExps = function(text, detail) {

        var row_header = '<div class="row align-items-start">';
        var text_col = '<div class="col-lg-3"><p>'+detail+'</p></div>'
        var url = SITE_DEFAULTS.baseurl+  "/pf/exp/" + text + "/completedExp";
        var link = '<div class="col-lg-offset-6"><a class="btn btn-primary btn-sm" href="'+url+'">View Report &raquo;</a></div>';
        var row_footer = '</div><hr>';
        var html_element = row_header + text_col + link + row_footer ;
        $("#completedExperiments").append(html_element);
        //$("#invitedJudgesList ul").html('<li>' + text+ '</li>');
    }
}

home = new Home();
home.registerListeners();
home.getPendingExperiments();
home.getUnlockedExperiments();
home.getCompletedExperiments();
