from ..forms import ExperimentForm
from ..models import Experiment, BCBFunctions, BCBClones, ExperimentJudge
from django.views import generic
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from zipfile import ZipFile, is_zipfile
from random import randrange, sample
from django.conf import settings
from django.http import Http404, JsonResponse
import codecs

SAMPLE_SIZE = 400


def setup_experiment(request, experiment_id):
    experiment = get_object_or_404(Experiment, pk=experiment_id)
    clonePairsPath = experiment.clonepairs

    if is_zipfile(clonePairsPath):
        with ZipFile(clonePairsPath, 'r') as czip:
            txt_files = 0
            txt_name = ''
            for fileObj in czip.infolist():
                if fileObj.filename.endswith(".txt"):
                    txt_files += 1
                    txt_name = fileObj.filename
            if txt_files > 1:
                raise Exception(
                    'More than one file in the zip. Please make sure you have only one .txt file in the zip.')

            sampled_lines = getSample(czip, txt_name, request)
            print("sampled_lines", sampled_lines)


def getSample(czip, filename, request):
    MIN_TOKENS = 50
    # https://www.checkmarket.com/blog/how-to-estimate-your-population-and-survey-sample-size/
    MIN_POPULATION_SIZE = 100000
    total_lines = 0
    outFilePath = generate_filename("50_tokens_and_more.txt", request.user)
    with codecs.open(outFilePath, mode="w+", encoding="utf-8") as outFile:
        with czip.open(filename) as clonefile:
            for line in clonefile:
                line = line.strip()
                function1, function2 = getFunctions(line)
                f1 = BCBFunctions.objects.filter(name=function1.name,
                                                 type=function1.type,
                                                 startline=function1.startlinem,
                                                 endline=function1.endline,
                                                 )
                if f1 and f1.tokens >= MIN_TOKENS:
                    f2 = BCBFunctions.objects.filter(name=function2.name,
                                                     type=function2.type,
                                                     startline=function2.startlinem,
                                                     endline=function2.endline,
                                                     )
                    if f1 and f2.tokens >= MIN_TOKENS:
                        outFile.write(line + "/n")
                        total_lines += 1

    # TODO: add sanity check- total_lines should be greater than SAMPLE_SIZE
    if total_lines >= MIN_POPULATION_SIZE:
        rand_nums = set(sample(range(0, total_lines), SAMPLE_SIZE))
        counter = 0
        sampled_lines = []
        with codecs.open(outFilePath) as clonefile:
            for line in clonefile:
                if counter in rand_nums:
                    sampled_lines.append(line.strip())
                counter += 1
        return sampled_lines
    else:
        pass
        # raise InputError(total_lines, "number of pairs where both member's size is at least 50 tokens is less than minimum accepted population size.")


"""selected,1146149.java,64,121,selected,902388.java,1155,1218"""


def getFunctions(line):
    try:
        parts = line.split(",")
        function1 = BCBFunctions()
        function1.type = parts[0]
        function1.name = parts[1]
        function1.startline = int(parts[2])
        function1.endline = int(parts[3])
        function2 = BCBFunctions()
        function2.type = parts[4]
        function2.name = parts[5]
        function2.startline = int(parts[6])
        function2.endline = int(parts[6])
        return (function1, function2)
    except ValueError as e:
        pass
        # raise InputError(line, "Clonepairs file is not formatted correctly")


def generate_filename(filename, user):
    d = timezone.now()
    time_stamp = string_i_want = ('%02d_%02d_%02d_%d' % (d.hour, d.minute, d.second, d.microsecond))[:-4]
    file_path = "{media_root}/users/{username}/generated/clonepairs/{year}_{month}_{day}/{time_stamp}/{filename}".format(
        media_root=settings.MEDIA_ROOT,
        username=user.username,
        year=d.year,
        month=d.month,
        day=d.day,
        time_stamp=time_stamp,
        filename=filename
    )
    return file_path


def get_pending_experiments(request):
    pending_experiment_ids = []
    pending_experiment_details = []
    experimentJudges = ExperimentJudge.objects.filter(user=request.user.profile,
                                                      experiment__is_locked=True).exclude(
        status=ExperimentJudge.STATUS_COMPLETED)
    if not experimentJudges:
        data = {"message": "No experiments to evaluate."}
        response = JsonResponse(data=data)
        response.status_code = 200
        return response
    for experimentJudge in experimentJudges:
        experiment = experimentJudge.experiment
        pending_experiment_ids.append(experiment.id)
        detail = "{n}".format(n=experiment.name)
        pending_experiment_details.append(detail)

    data = {"message": "success",
            "experiment_ids": pending_experiment_ids,
            "experiment_details": pending_experiment_details}
    response = JsonResponse(data=data)
    response.status_code = 200
    return response


def get_unlocked_experiments(request):
    unlocked_experiments = []
    experiment_details = []
    experiments = Experiment.objects.filter(user=request.user.profile, is_locked=False)
    if not experiments:
        data = {"message": "No unlocked experiments."}
        response = JsonResponse(data=data)
        response.status_code = 200
        return response
    for experiment in experiments:
        unlocked_experiments.append(experiment.id)
        detail = "{n}".format(n=experiment.name)
        experiment_details.append(detail)
    data = {"message": "success",
            "experiment_ids": unlocked_experiments,
            "experiment_details": experiment_details}
    response = JsonResponse(data=data)
    response.status_code = 200
    return response


def get_completed_experiments(request):
    completed_experiment_ids = []
    experiment_details = []
    experimentJudges = ExperimentJudge.objects.filter(user=request.user.profile,
                                                      experiment__is_locked=True,
                                                      status=ExperimentJudge.STATUS_COMPLETED)
    if not experimentJudges:
        data = {"message": "No completed experiments found."}
        response = JsonResponse(data=data)
        response.status_code = 200
        return response
    for experimentJudge in experimentJudges:
        experiment = experimentJudge.experiment
        completed_experiment_ids.append(experiment.id)
        detail = "{n}".format(n=experiment.name)
        experiment_details.append(detail)

    data = {"message": "success",
            "experiment_ids": completed_experiment_ids,
            "experiment_details": experiment_details}
    response = JsonResponse(data=data)
    response.status_code = 200
    return response
