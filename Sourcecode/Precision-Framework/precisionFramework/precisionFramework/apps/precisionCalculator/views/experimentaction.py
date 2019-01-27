from ..forms import ExperimentActionForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse
from django.utils import timezone
from ..models import ExperimentDetail, CandidateUserScore, Experiment, ExperimentJudge, CandidatePair
from django.conf import settings
from celery import shared_task
from ..tasks import testPrint


def exp_action_new(request, experiment_id):
    try:
        experimentJudge = ExperimentJudge.objects.get(experiment__id=experiment_id, user__id=request.user.profile.id)
    except ExperimentJudge.DoesNotExist:
        data = {"message": "You are not authorized to participate in this experiment."}
        response = JsonResponse(data=data)
        response.status_code = 401
        return response
    else:
        if experimentJudge.status == ExperimentJudge.STATUS_NOT_STARTED:
            experimentJudge.status = ExperimentJudge.STATUS_STARTED
            experimentJudge.save()

        experiment = experimentJudge.experiment
        if request.method == 'POST':
            try:
                candidate_id = int(request.POST.get('candidate_id', -1))
                try:
                    candidate = CandidatePair.objects.get(pk=candidate_id)
                except CandidatePair.DoesNotExist:
                    data = {"message": "Invalid candidate pair id."}
                    response = JsonResponse(data=data)
                    response.status_code = 401
                    return response

            except TypeError:
                data = {"message": "Invalid candidate pair id."}
                response = JsonResponse(data=data)
                response.status_code = 401
                return response

            try:
                time_spent = int(request.POST.get('time_spent', -1))
            except TypeError:
                data = {"message": "Invalid time spent information"}
                response = JsonResponse(data=data)
                response.status_code = 401
                return response
            form = ExperimentActionForm(experiment, request.POST, request=request)
            if form.is_valid():
                try:

                    exp_detail = ExperimentDetail.objects.get(experiment=experiment,
                                                              candidate_pair=candidate,
                                                              user=request.user.profile,
                                                              visited=False,
                                                              source_type=ExperimentDetail.USER_SOURCE_TYPE
                                                              )
                    exp_detail.vote = form.cleaned_data['vote']
                    exp_detail.SOURCE_TYPE = ExperimentDetail.USER_SOURCE_TYPE

                    # save candidate's user score.
                    candidate_user_score = CandidateUserScore()
                    candidate_user_score.user = request.user.profile
                    candidate_user_score.candidate = candidate
                    candidate_user_score.vote = exp_detail.vote
                    candidate_user_score.experiment = experiment
                    candidate_user_score.time_spent = time_spent  # => [137]
                    candidate_user_score.explaination = form.cleaned_data['explanation']
                    candidate_user_score.save()
                    exp_detail.visited = True
                    exp_detail.save()

                    next_exp_details = ExperimentDetail.objects.filter(user=request.user.profile,
                                                                       experiment=experiment,
                                                                       visited=False,
                                                                       source_type=ExperimentDetail.USER_SOURCE_TYPE).order_by(
                        '?')

                    if next_exp_details:
                        block1 = next_exp_details[0].candidate_pair.candidate_one
                        block2 = next_exp_details[0].candidate_pair.candidate_two

                        data = {"block_one": block1.getSourceCode().strip(),
                                "block_two": block2.getSourceCode().strip(),
                                "exp_id": experiment_id,
                                "candidate_id": next_exp_details[0].candidate_pair.id,
                                "has_next": next_exp_details.count() > 1,
                                "left": next_exp_details.count()
                                }
                        response = JsonResponse(data=data)
                        response.status_code = 200
                        return response
                    else:
                        data = getReportForExperimentForUser(request.user.profile, experiment)
                        response = JsonResponse(data=data)
                        response.status_code = 200
                        return response

                except ExperimentDetail.DoesNotExist:
                    data = {
                        "message": "Invalid request. Couldn't find the requested candidate pair",
                        "redirect_url": "send some url"}  # TODO:send redirect url
                    response = JsonResponse(data=data)
                    response.status_code = 401
                    return response
            else:
                print(form.errors)
                data = {
                    "message": "Some error in form validation",
                    "redirect_url": "send some url"}  # TODO:send redirect url
                response = JsonResponse(data=data)
                response.status_code = 401
                return response


def exp_action_replay(request, experiment_id):
    try:
        experimentJudge = ExperimentJudge.objects.get(experiment__id=experiment_id, user__id=request.user.profile.id)
    except ExperimentJudge.DoesNotExist:
        data = {"message": "You are not authorized to participate in this experiment."}
        response = JsonResponse(data=data)
        response.status_code = 401
        return response
    else:
        experiment = experimentJudge.experiment
        if request.method == 'POST':
            try:
                candidate_id = int(request.POST.get('candidate_id', -1))
                try:
                    candidate = CandidatePair.objects.get(pk=candidate_id)
                except CandidatePair.DoesNotExist:
                    data = {"message": "Invalid candidate pair id."}
                    response = JsonResponse(data=data)
                    response.status_code = 401
                    return response

            except TypeError:
                data = {"message": "Invalid candidate pair id."}
                response = JsonResponse(data=data)
                response.status_code = 401
                return response

            try:
                time_spent = int(request.POST.get('time_spent', -1))
            except TypeError:
                data = {"message": "Invalid time spent information"}
                response = JsonResponse(data=data)
                response.status_code = 401
                return response
            try:
                next_exp_details = ExperimentDetail.objects.filter(candidate_pair__id__gt =candidate_id,
                                                                experiment=experiment,
                                                                   visited=True,

                                                                   source_type=ExperimentDetail.PRECISION_FRAMEWORK_SOURCE_TYPE).order_by('candidate_pair')

                if next_exp_details:
                    block1 = next_exp_details[0].candidate_pair.candidate_one
                    block2 = next_exp_details[0].candidate_pair.candidate_two

                    data = {"block_one": block1.getSourceCode().strip(),
                            "block_two": block2.getSourceCode().strip(),
                            "exp_id": experiment_id,
                            "candidate_id": next_exp_details[0].candidate_pair.id,
                            "has_next": next_exp_details.count() > 1,
                            "left": next_exp_details.count(),
                            "clone_type": next_exp_details[0].clone_type,
                            "resolution_method": next_exp_details[0].resolution_method,
                            }
                    response = JsonResponse(data=data)
                    response.status_code = 200
                    return response
                else:
                    data = getReportForExperimentForUser(request.user.profile, experiment)
                    response = JsonResponse(data=data)
                    response.status_code = 200
                    return response

            except ExperimentDetail.DoesNotExist:
                data = {
                    "message": "Invalid request. Couldn't find the requested candidate pair",
                    "redirect_url": "send some url"}  # TODO:send redirect url
                response = JsonResponse(data=data)
                response.status_code = 401
                return response


def exp_action_start(request, experiment_id):
    experiment = get_object_or_404(Experiment, pk=experiment_id)
    form = ExperimentActionForm(experiment=experiment, request=request)
    return render(request, "precisionCalculator/exp_action_new.html", {'form': form})

def exp_action_review(request, experiment_id):
    experiment = get_object_or_404(Experiment, pk=experiment_id)
    form = ExperimentActionForm(experiment=experiment, request=request)
    return render(request, "precisionCalculator/exp_action_review.html", {'form': form})


def get_first_candidate_for_exp(request, experiment_id):
    try:
        experiment = Experiment.objects.get(pk=experiment_id)

    except Experiment.DoesNotExist:
        data = {
            "message": "Experiment doesn't exist",
            "redirect_url": "send some url"}  # TODO:send redirect url
        response = JsonResponse(data=data)
        response.status_code = 401
        return response
    if experiment.is_locked:
        next_exp_details = ExperimentDetail.objects.filter(user=request.user.profile,
                                                           experiment=experiment,
                                                           visited=False,
                                                           source_type=ExperimentDetail.USER_SOURCE_TYPE).order_by('?')
        if next_exp_details:
            for exp_detail in next_exp_details:
                candidate_id = exp_detail.candidate_pair.id

                block1 = next_exp_details[0].candidate_pair.candidate_one
                block2 = next_exp_details[0].candidate_pair.candidate_two

                data = {"message": "success",
                        "block_one": block1.getSourceCode().strip(),
                        "block_two": block2.getSourceCode().strip(),
                        "exp_id": experiment_id,
                        "candidate_id": next_exp_details[0].candidate_pair.id,
                        "has_next": next_exp_details.count() > 1,
                        "left": next_exp_details.count()
                        }
                response = JsonResponse(data=data)
                response.status_code = 200
                return response
        else:
            data = getReportForExperimentForUser(request.user.profile, experiment)
            response = JsonResponse(data=data)
            response.status_code = 200
            return response

    else:
        data = {
            "message": "The experiment is not yet locked. Please make sure to have this experiment locked before starting to evaluate the candidate pairs.",
            "redirect_url": "send some url"}  # TODO:send redirect url
        response = JsonResponse(data=data)
        response.status_code = 401
        return response

def get_first_candidate_for_replay(request, experiment_id):
    try:
        experiment = Experiment.objects.get(pk=experiment_id)

    except Experiment.DoesNotExist:
        data = {
            "message": "Experiment doesn't exist",
            "redirect_url": "send some url"}  # TODO:send redirect url
        response = JsonResponse(data=data)
        response.status_code = 401
        return response
    if experiment.is_locked:
        next_exp_details = ExperimentDetail.objects.filter(experiment=experiment,
                                                           visited=True,
                                                           source_type=ExperimentDetail.PRECISION_FRAMEWORK_SOURCE_TYPE).order_by('candidate_pair')
        if next_exp_details:
            for exp_detail in next_exp_details:
                candidate_id = exp_detail.candidate_pair.id

                block1 = next_exp_details[0].candidate_pair.candidate_one
                block2 = next_exp_details[0].candidate_pair.candidate_two

                data = {"message": "success",
                        "block_one": block1.getSourceCode().strip(),
                        "block_two": block2.getSourceCode().strip(),
                        "exp_id": experiment_id,
                        "candidate_id": next_exp_details[0].candidate_pair.id,
                        "has_next": next_exp_details.count() > 1,
                        "left": next_exp_details.count(),
                        "clone_type": next_exp_details[0].clone_type,
                        "resolution_method": next_exp_details[0].resolution_method,
                        }
                response = JsonResponse(data=data)
                response.status_code = 200
                return response
        else:
            data = getReportForExperimentForUser(request.user.profile, experiment)
            response = JsonResponse(data=data)
            response.status_code = 200
            return response

    else:
        data = {
            "message": "The experiment is not yet locked. Please make sure to have this experiment locked before starting to evaluate the candidate pairs.",
            "redirect_url": "send some url"}  # TODO:send redirect url
        response = JsonResponse(data=data)
        response.status_code = 401
        return response


def exp_next_pair(request, experiment_id):
    try:
        experimentJudge = ExperimentJudge.objects.filter(experiment__id=experiment_id, user__id=request.user.profile.id)
    except ExperimentJudge.DoesNotExist:
        data = {"message": "You are not authorized to participate in this experiment."}
        response = JsonResponse(data=data)
        response.status_code = 401
        return response

    experiment = experimentJudge.experiment

    next_index = int(request.POST.get('next_index', 0))
    folder = "default"
    file_name = "92183.java"
    lines = [(51, 61), (63, 73), (79, 89), (97, 99), (105, 123)]

    user = request.user.profile
    ExperimentDetail.objects.filter(user=user,
                                    )

    data = {"block_one": getSourceCode(folder, file_name, lines[next_index][0], lines[next_index][1]),
            "block_two": getSourceCode(folder, file_name, lines[0][0], lines[0][1])
            }
    return JsonResponse(data=data)


def getSourceCode(folder_name, file_name, start_line, end_line):
    dataset_root = getattr(settings, "DATASET_ROOT", None)
    testPrint.delay("*******testing*********, " + str(timezone.now()))
    if dataset_root:
        file_path = "{root}/{folder}/{filename}".format(root=dataset_root,
                                                        folder=folder_name,
                                                        filename=file_name)
        count = min(1, start_line)
        code_lines = ""
        with open(file_path, encoding="utf-8", mode="r") as f:
            for line in f:
                if count > end_line:
                    return code_lines
                if count >= start_line:
                    code_lines = code_lines + line
                count += 1
        if end_line > count:
            raise SystemError("Error with block")
        return code_lines
    else:
        raise SystemError("DATASET_ROOT not set.")


def getReportForExperimentForUser(profile, experiment):
    usr_exp_details_tps = ExperimentDetail.objects.filter(user=profile,
                                                          experiment=experiment,
                                                          visited=True,
                                                          vote=True,
                                                          source_type=ExperimentDetail.USER_SOURCE_TYPE)

    usr_exp_details_fps = ExperimentDetail.objects.filter(user=profile,
                                                          experiment=experiment,
                                                          visited=True,
                                                          vote=False,
                                                          source_type=ExperimentDetail.USER_SOURCE_TYPE)

    bcb_exp_details_tps = ExperimentDetail.objects.filter(experiment=experiment,
                                                          visited=True,
                                                          vote=True,
                                                          source_type=ExperimentDetail.BCB_SOURCE_TYPE)
    bcb_exp_details_fps = ExperimentDetail.objects.filter(experiment=experiment,
                                                          visited=True,
                                                          vote=False,
                                                          source_type=ExperimentDetail.BCB_SOURCE_TYPE)

    pf_exp_details_tps = ExperimentDetail.objects.filter(experiment=experiment,
                                                         visited=True,
                                                         vote=True,
                                                         source_type=ExperimentDetail.PRECISION_FRAMEWORK_SOURCE_TYPE)

    pf_exp_details_fps = ExperimentDetail.objects.filter(experiment=experiment,
                                                         visited=True,
                                                         vote=False,
                                                         source_type=ExperimentDetail.PRECISION_FRAMEWORK_SOURCE_TYPE)

    total_tps = len(usr_exp_details_tps) + len(bcb_exp_details_tps) + len(pf_exp_details_tps)
    total_fps = len(usr_exp_details_fps) + len(bcb_exp_details_fps) + len(pf_exp_details_fps)
    precision = total_tps * 100 / (total_fps + total_tps)
    data = {
        "message": "finished",
        "total_tps": total_tps,
        "total_fps": total_fps,
        "tps_usr": len(usr_exp_details_tps),
        "fps_usr": len(usr_exp_details_fps),
        "tps_bcb": len(bcb_exp_details_tps),
        "fps_bcb": len(bcb_exp_details_fps),
        "tps_pf": len(pf_exp_details_tps),
        "fps_pf": len(pf_exp_details_fps),
        "precision": precision,
        "redirect_url": "send some url"}  # TODO:send redirect url

    return data


def exp_action_finished(request, experiment_id):
    experimentJudge = get_object_or_404(ExperimentJudge, experiment__id=experiment_id, user__id=request.user.profile.id)
    experiment = get_object_or_404(Experiment, pk=experiment_id)
    usr_exp_details = ExperimentDetail.objects.filter(user=request.user.profile,
                                                      experiment=experiment,
                                                      visited=False,
                                                      source_type=ExperimentDetail.USER_SOURCE_TYPE)
    if usr_exp_details:
        form = ExperimentActionForm(experiment=experiment, request=request)
        return render(request, "precisionCalculator/exp_action.html", {'form': form})
    else:
        data = getReportForExperimentForUser(request.user.profile, experiment)
        experimentJudge.status = ExperimentJudge.STATUS_COMPLETED
        experimentJudge.save()
        # TODO: set completed in Exeriment Judge for this user.
        # TODO: check if all judges have completed this experiment, then set exeriment to be completed and prepare an overall report.
        # TODO: delete rows for this experiment from the experiment details table
        return render(request, "precisionCalculator/exp_action_finished.html", {'data': data, 'experiment': experiment})
