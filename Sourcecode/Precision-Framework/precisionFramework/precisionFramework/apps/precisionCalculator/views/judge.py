from django.contrib.auth.models import User

from ..models import Experiment, ExperimentJudge
from ..forms import JudgeForm
from django.shortcuts import render, redirect, get_object_or_404
from ..models import Judge
from django.views import generic
from django.forms import formset_factory
from django.http import Http404, JsonResponse


def judge_new(request, experiment_id):
    try:
        experiment = Experiment.objects.get(pk=experiment_id)
    except Experiment.DoesNotExist:
        data = {"message": "You are not authorized to participate in this experiment."}
        response = JsonResponse(data=data)
        response.status_code = 401
        return response
    if request.method == "POST":
        if experiment.is_locked:
            data = {"message": "This experiment is locked. You can not add more judges to this experiment"}
            response = JsonResponse(data=data)
            response.status_code = 401
            return response

        judge_form = JudgeForm(experiment, request.POST, request=request)
        if judge_form.is_valid():
            try:
                username = judge_form.cleaned_data['username']
                user = User.objects.get(username=username)

                experimentJudge = ExperimentJudge.objects.filter(experiment__id=experiment_id,
                                                                 user__id=user.profile.id)
                if experimentJudge:
                    # print("experimentJudge", experimentJudge)
                    data = {"message": "This judge has already been invited to participate in this experiment."}
                    response = JsonResponse(data=data)
                    response.status_code = 401  # may be we need to change the code in future.
                    return response
                else:
                    experiment_judge = ExperimentJudge()
                    experiment_judge.user = user.profile
                    experiment_judge.experiment = experiment
                    # TODO: send email to this judge about the experiment and link to the experiment.
                    experiment_judge.save()

                    data = {"message": "successfully invited the judge."}
                    response = JsonResponse(data=data)
                    response.status_code = 200
                    return response
            except User.DoesNotExist:
                data = {
                    "message": "This user does not exist in our system. Please ask the user to create an account first."}
                response = JsonResponse(data=data)
                response.status_code = 401  # may be we need to change the code in future.
                return response
    else:
        experiment = get_object_or_404(Experiment, pk=experiment_id)
        form = JudgeForm(experiment=experiment, request=request)
        return render(request, "precisionCalculator/judge_new.html", {'form': form})


def getJudgesForExperiemnt(request, experiment_id):
    try:
        experiment = Experiment.objects.get(pk=experiment_id)
    except Experiment.DoesNotExist:
        data = {"message": "You are not authorized to participate in this experiment."}
        response = JsonResponse(data=data)
        response.status_code = 401
        return response
    experimentJudges = ExperimentJudge.objects.filter(experiment__id=experiment_id)
    if experimentJudges:
        judges = []
        for exp_judge in experimentJudges:
            judges.append(exp_judge.user.user.username)
        data = {"message": "found {size} judges for this experiment".format(size=len(judges)),
                "usernames": judges}
        response = JsonResponse(data=data)
        response.status_code = 200
        return response
    else:
        data = {"message": "no invited judges found for this experiment"}
        response = JsonResponse(data=data)
        response.status_code = 401
        return response
