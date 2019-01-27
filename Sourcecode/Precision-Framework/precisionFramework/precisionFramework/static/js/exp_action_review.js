var ExperimentAction = function () {
    that = this;
    that.candidate_id = false;
    that.has_next = true;
    //$("#clone_type").hide();

    this.registerListeners = function () {
        $("#next").click(function () {
            that.next_index++;
            $.ajax({
                type: "POST",
                url: SITE_DEFAULTS.baseurl + '/pf/exp/' + experiment_id + '/review',
                data: $("#experimentactionfrm").serialize(),
                dataType: 'json',
                success: function (data) {
                    console.log("success");
                    //console.log(data);
                    if (data.message === "finished") {
                        $("#next").hide();
                        url = SITE_DEFAULTS.baseurl + '/pf/exp/' + experiment_id + '/completedExp';
                        window.location.replace(url);
                    } else {
                        $("#candidate_id").val(data.candidate_id);
                        that.has_next = data.has_next
                        console.log(that.has_next);
                        console.log($("#candidate_id").val());
                        console.log(data.clone_type);
                        console.log(data.resolution_method);
                        var codeLeftElement = $("#codeLeft")
                        var codeRightElement = $("#codeRight")
                        var b1 = data.block_one;
                        var b2 = data.block_two;
                        //console.log(b1);
                        codeLeftElement.html(Prism.highlight(b1, Prism.languages.java));
                        codeRightElement.html(Prism.highlight(b2, Prism.languages.java));
                        that.resetInputs();
                        Prism.highlightAll();
                        $("#current_status").text("( candidate_id: " +data.candidate_id+", "+ data.resolution_method+ ": "+ data.left + " more to evaluate)");

                    }

                },
                error: function (request, status, error) {
                    console.log(request.responseText);
                },
                beforeSend: function () {
                    if ($('input:radio[name=vote]:checked').length > 0) {
                        if ($("#voteerror").length) {
                            $("#voteerror").remove();
                        }
                        return true;
                    } else {

                        var element = $("#vote");
                        $("<span id='voteerror' class='alert alert-danger'> please cast a vote </span>").appendTo(element);
                        return false;
                    }
                }
            });
        })
        $('input:radio[name="vote"]').change(function () {
            if ($(this).val() === "1") {
                console.log("True positive selected")

                $("#clone_type").show();

            } else {
                // false positive selected.
                $("#clone_type").hide();
            }
            if ($("#voteerror").length) {
                $("#voteerror").remove();
            }
        });
        $('#id_clone_type input[type=checkbox]').click(function () {
            $("#id_vote_0").prop('checked', true);
        });

        $(document).keypress(function (e) {
            var keyID = (e.charCode) ? e.charCode : ((e.which) ? e.which : e.keyCode);
            console.log(keyID)
            if ($("#id_explanation").is(":focus")) {
                return true;
            }
            if (keyID == 121) {
                if ($("#voteerror").length) {
                    $("#voteerror").remove();
                }
                // true positive : Y is pressed
                $("#id_vote_0").prop('checked', true);
                $("#id_vote_1").prop('checked', false);
                //$("#next").trigger('click');
            } else if (keyID == 110) {
                if ($("#voteerror").length) {
                    $("#voteerror").remove();
                }
                $("#id_vote_1").prop('checked', true);
                $("#id_vote_0").prop('checked', false);
                //$("#next").trigger('click');
            } else if (keyID >= 50 && keyID <= 52) {
                if ($("#voteerror").length) {
                    $("#voteerror").remove();
                }
                $("#clone_type").show();
                $("#id_vote_0").prop('checked', true);
                $("#id_vote_1").prop('checked', false);

                for (var i = 0; i < 3; i++) {
                    $("#id_clone_type_" + i).prop('checked', false);
                }
                var i = keyID - 50;
                $("#id_clone_type_" + i).prop('checked', true);
                //$("#next").trigger('click');
            } else if (keyID == 13) {
                if ($("#voteerror").length) {
                    $("#voteerror").remove();
                }
                // enter is pressed
                $("#next").trigger('click');
            }
            console.log("pressed :" + keyID)
        });
    }
    this.initExp = function () {
        $.ajax({
            type: "POST",
            url: SITE_DEFAULTS.baseurl + '/pf/exp/' + experiment_id + '/initReplay',
            data: {
                'csrfmiddlewaretoken': csrftoken,
            },
            dataType: 'json',
            success: function (data) {
                console.log("success");
                if (data.message === "finished") {
                    $("#next").hide();
                    url = SITE_DEFAULTS.baseurl + '/pf/exp/' + experiment_id + '/completedExp';
                    window.location.replace(url);
                } else {
                    $("#candidate_id").val(data.candidate_id);
                    that.has_next = data.has_next
                    console.log(that.has_next);
                    console.log($("#candidate_id").val());
                    console.log(data.clone_type);
                    console.log(data.resolution_method);
                    var codeLeftElement = $("#codeLeft")
                    var codeRightElement = $("#codeRight")
                    var b1 = data.block_one;
                    var b2 = data.block_two;
                    //console.log(b1);
                    codeLeftElement.html(Prism.highlight(b1, Prism.languages.java));
                    codeRightElement.html(Prism.highlight(b2, Prism.languages.java));
                    Prism.highlightAll();
                    $("#current_status").text("( candidate_id: " +data.candidate_id+", "+ data.resolution_method+ ": "+ data.left + " more to evaluate)");
                }
            },
            error: function (request, status, error) {
                console.log(request.responseText);
            }
        });
    }
    this.resetInputs = function () {
        $("#id_vote_0").prop('checked', false);
        $("#id_vote_1").prop('checked', false);
        $("#id_explanation").val("")
        for (var i = 0; i < 3; i++) {
            $("#id_clone_type_" + i).prop('checked', false);
        }

    }
}

action = new ExperimentAction();
Prism.plugins.NormalizeWhitespace.setDefaults({
    //'remove-trailing': true,
    //'remove-indent': true,
    'left-trim': true,
    'right-trim': true,
    /*'break-lines': 80,
    'indent': 2,
    'remove-initial-line-feed': false,
    'tabs-to-spaces': 4,
    'spaces-to-tabs': 4*/
});

action.registerListeners();
action.initExp();

