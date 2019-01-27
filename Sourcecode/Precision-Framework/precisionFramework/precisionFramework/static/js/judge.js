var Judge = function () {
    that = this;
    that.judgesInvited = 0;
    $("#lockExpDiv").hide();
    $("#startExpDiv").hide();
    $("#spinner").hide();
    this.registerListeners = function () {
        $("#inviteBtn").click(function () {
            that.judgesInvited++;
            console.log(that.judgesInvited);
            $.ajax({
                type: "POST",
                url: SITE_DEFAULTS.baseurl + '/pf/judge/' + experiment_id + '/new',
                data: {
                    'username': $("#id_username").val(),
                    'csrfmiddlewaretoken': csrftoken
                },
                dataType: 'json',
                success: function (data) {
                    console.log(data["message"]);
                    $("#reponseMsg").text(data["message"])
                    $("#reponseMsg").show();
                    $("#id_username").val('')
                    $("#invitedJudgesList ul").html("");
                    that.populateInvitedJudges();
                },
                error: function (request, status, error) {
                    //console.log(request.responseText);
                    $("#reponseMsg").text(request.responseJSON.message)
                    $("#reponseMsg").show();
                }
            });
        })

        $("#lockExp").click(function () {

            $.ajax({
                type: "POST",
                url: SITE_DEFAULTS.baseurl + '/pf/exp/' + experiment_id + '/lockExperiment',
                data: {
                    'csrfmiddlewaretoken': csrftoken
                },
                dataType: 'json',
                success: function (data) {
                    $("#spinner").hide();
                    console.log(data["message"]);
                    if (data["message"] === "success") {
                        $("#lockExpDiv").hide();
                        $("#startExpDiv").show();
                    }
                },
                error: function (request, status, error) {
                    console.log(request.responseText);
                },
                beforeSend: function () {
                    $("#lockExp").hide();
                    $("#spinner").show();
                }
            });
        })


    }
    this.populateInvitedJudges = function () {
        that = this;
        $.ajax({
            type: "GET",
            url: SITE_DEFAULTS.baseurl + '/pf/judge/' + experiment_id + '/getInvitedJudgesList',
            data: {
                'csrfmiddlewaretoken': csrftoken
            },
            dataType: 'json',
            success: function (data) {
                console.log(data["message"]);
                usernames = data["usernames"];
                $("#msgLabel").text('');
                if (usernames.length > 0) {
                    if (is_locked === "True") {
                        $("#lockExpDiv").hide();
                        $("#startExpDiv").show();
                    } else {
                        $("#lockExpDiv").show();
                    }
                }
                for (var i = 0; i < usernames.length; i++) {
                    that.addLi(usernames[i]);
                }
            },
            error: function (request, status, error) {
                //console.log(request.responseText);
                //$("#msgLabel").text(request.responseJSON.message)


            }
        });
    }
    this.addLi = function (text) {
        //var li = $("<li>").html(text);
        //$("#invitedJudgesList ul").append(li)

        $("#invitedJudgesList ul").append("<li class='list-group-item'>" + text + "</li> <br>");
        //$("#invitedJudgesList ul").html('<li>' + text+ '</li>');
    }
    $(document).on("keypress", "form", function (e) {
        var keyID = (e.charCode) ? e.charCode : ((e.which) ? e.which : e.keyCode);
        return keyID != 13;
    });
    $("#id_username").focus(function () {
        $("#reponseMsg").hide();
    })
}

judge = new Judge();
judge.registerListeners();
judge.populateInvitedJudges()

