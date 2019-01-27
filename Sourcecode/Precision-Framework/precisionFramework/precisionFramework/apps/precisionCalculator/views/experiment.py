from _csv import field_size_limit

from ..models import DjCeleryTaskresult, CeleryTask
from ..forms import ExperimentForm
from django.shortcuts import render, redirect
from ..models import Experiment, BCBClones, BCBFunctions, Block, CandidatePair, ExperimentJudge, ExperimentDetail
from django.views import generic
from django.utils import timezone
from ..tasks import *
from django.http import Http404, JsonResponse
import codecs
from ..services.utils import *
from django.core.exceptions import MultipleObjectsReturned


def exp_new(request):
    if request.method == 'POST':
        form = ExperimentForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            experiment = form.save(commit=False)
            experiment.user = request.user.profile
            experiment.upload_date = timezone.now()
            experiment.save()
            submitted_task = task_process_input_clonepairs.delay(request.user.username, experiment.clonepairs.path,
                                                                 experiment.id)
            celeryTask = CeleryTask()
            celeryTask.owner = request.user.profile
            celeryTask.task_id = submitted_task.task_id
            celeryTask.content_type = "EXPERIMENT_ID"
            celeryTask.content = str(experiment.id)
            celeryTask.date_issued = timezone.now()
            celeryTask.save()

            """
            print("submitted task id: {i}".format(i=submitted_task.task_id))
            try:
                result = DjCeleryTaskresult.objects.get(task_id=submitted_task.task_id)
                print("task state: {state}".format(state=result.status))
            except DjCeleryTaskresult.DoesNotExist:
                print("DOES NOT EXIST : {t}".format(t=submitted_task.task_id))
                pass
            """

            return redirect('precisionCalculator:exp_detail', pk=experiment.pk)
    else:
        form = ExperimentForm(request=request)
    return render(request, 'precisionCalculator/exp_new.html', {'form': form})


def getUploadStatus(request, experiment_id):
    try:
        celeryTask = CeleryTask.objects.get(content_type="EXPERIMENT_ID", content="{c}".format(c=experiment_id),
                                            owner=request.user.profile)
        try:
            result = DjCeleryTaskresult.objects.get(task_id=celeryTask.task_id)
            data = {"message": "{m}".format(m=result.status)}
            response = JsonResponse(data=data)
            response.status_code = 200
            return response
        except DjCeleryTaskresult.DoesNotExist:
            data = {"message": "PENDING"}
            response = JsonResponse(data=data)
            response.status_code = 200
            return response

    except CeleryTask.DoesNotExist:
        data = {"message": "Invalid query. No such task exists in the system."}
        response = JsonResponse(data=data)
        response.status_code = 401
        return response


def lockExperiment(request, experiment_id):
    experiment = None
    candidates_not_in_bcb_or_pf = set()
    candidates_found_in_bcb = set()
    candidates_found_in_pf = set()
    try:
        experiment = Experiment.objects.get(pk=experiment_id)
        if experiment.is_locked:
            data = {"message": "This experiment is locked already."}
            response = JsonResponse(data=data)
            response.status_code = 401
            return response

        getCandidatesForExperiment(experiment, candidates_not_in_bcb_or_pf, candidates_found_in_bcb,
                                   candidates_found_in_pf)
        print("size: candidates_not_in_bcb_or_pf {s}".format(s=len(candidates_not_in_bcb_or_pf)))
        print("size: candidates_found_in_bcb {s}".format(s=len(candidates_found_in_bcb)))
        print("size: candidates_found_in_pf {s}".format(s=len(candidates_found_in_pf)))
        judges = ExperimentJudge.objects.filter(experiment=experiment)
        for judge in judges:
            for candidatepair in candidates_not_in_bcb_or_pf:
                exp_detail = ExperimentDetail()
                exp_detail.experiment = experiment
                exp_detail.user = judge.user
                exp_detail.candidate_pair = candidatepair
                exp_detail.vote = False
                exp_detail.save()

        for candidatepair in candidates_found_in_bcb:
            exp_detail = ExperimentDetail()
            exp_detail.experiment = experiment
            exp_detail.candidate_pair = candidatepair
            exp_detail.source_type = ExperimentDetail.BCB_SOURCE_TYPE
            exp_detail.vote = True
            exp_detail.clone_type = candidatepair.clone_type
            exp_detail.visited = True
            exp_detail.save()

        for candidatepair in candidates_found_in_pf:
            exp_detail = ExperimentDetail()
            exp_detail.experiment = experiment
            exp_detail.candidate_pair = candidatepair
            exp_detail.source_type = ExperimentDetail.PRECISION_FRAMEWORK_SOURCE_TYPE
            exp_detail.vote = True if CandidatePair.STATUS_TRUE == candidatepair.confirmed_status else False
            exp_detail.clone_type = candidatepair.clone_type
            exp_detail.resolution_method = candidatepair.resolution_type
            exp_detail.visited = True
            exp_detail.save()

        data = {"message": "success"}
        response = JsonResponse(data=data)
        response.status_code = 200
        experiment.is_locked = True
        experiment.save()
        return response
    except Experiment.DoesNotExist:
        data = {"message": "Invalid Experiment id."}
        response = JsonResponse(data=data)
        response.status_code = 401
        return response


def loadType2s(request):
    print("starting type2 load")
    task_load_type2.delay()
    data = {"message": "job started."}
    response = JsonResponse(data=data)
    response.status_code = 200
    return response

def isExperimentComplete(request, experiment_id):
    try:
        experiment = Experiment.objects.get(pk=experiment_id)
        if experiment.is_locked:
            experimentJudges = ExperimentJudge.objects.filter(experiment=experiment)
            if experimentJudges:
                num_judges = experimentJudges.count()
                min_majority_count = num_judges//2 # int part
                for judge in experimentJudges:
                    if judge.status != ExperimentJudge.STATUS_COMPLETED:
                        data = {"message": "Not all judges have completed this experiment. We can not generate the detailed report "}
                        response = JsonResponse(data=data)
                        response.status_code = 401
                        return response
                data = {
                    "message": "success"}
                response = JsonResponse(data=data)
                response.status_code = 200
                return response
            else:
                data = {"message": "No Judges assigned to the experiment"}
                response = JsonResponse(data=data)
                response.status_code = 401
                return response
        else:
            data = {"message": "Experiment not locked yet."}
            response = JsonResponse(data=data)
            response.status_code = 401
            return response
    except Experiment.DoesNotExist:
        data = {"message": "Invalid Experiment id."}
        response = JsonResponse(data=data)
        response.status_code = 401
        return response

def generateDetailedReport(request, experiment_id):
    try:
        experiment = Experiment.objects.get(pk=experiment_id)
        if experiment.is_locked:
            experimentJudges = ExperimentJudge.objects.filter(experiment=experiment)
            if experimentJudges:
                num_judges = experimentJudges.count()
                min_majority_count = num_judges//2 # int part
                for judge in experimentJudges:
                    if judge.status != ExperimentJudge.STATUS_COMPLETED:
                        data = {"message": "Not all judges have completed this experiment. We can not generate the detailed report "}
                        response = JsonResponse(data=data)
                        response.status_code = 401
                        return response

                # get the judges again.
                experimentJudges = ExperimentJudge.objects.filter(experiment=experiment)
                report = {"judge_evaluation":{"TP":0,
                                              "FP":0}}
                judges_evaluations = []
                judge_count=0

                # get evaluations for each judge
                for judge in experimentJudges:
                    judge_experiment_details =  ExperimentDetail.objects.filter(user=judge.user,
                                                    experiment=experiment,
                                                    visited=True,
                                                    source_type=ExperimentDetail.USER_SOURCE_TYPE)
                    judges_evaluations.append(judge_experiment_details)
                    judge_count+=1

                # gather per candidate details
                candidates = {}
                for judge_experiment_details in judges_evaluations:
                    for row in judge_experiment_details:
                        candidate_id = row.candidate_pair.id
                        if row.vote==1:
                            if candidate_id in candidates:
                                vote_details=candidates[candidate_id]
                                vote_details["TP_count"] = vote_details["TP_count"] + 1
                                vote_details["TP_voters"].append(row.user.user.username)
                            else:
                                vote_details = {}
                                vote_details["TP_count"] = 1
                                vote_details["FP_count"] = 0
                                vote_details["TP_voters"]=[row.user.user.username]
                                vote_details["FP_voters"] = []
                                candidates[candidate_id]= vote_details
                        else:
                            if candidate_id in candidates:
                                vote_details=candidates[candidate_id]
                                vote_details["FP_count"] = vote_details["FP_count"] + 1
                                vote_details["FP_voters"].append(row.user.user.username)
                            else:
                                vote_details = {}
                                vote_details["TP_count"] = 0
                                vote_details["FP_count"] = 1
                                vote_details["TP_voters"] = []
                                vote_details["FP_voters"] = [row.user.user.username]
                                candidates[candidate_id] = vote_details

                # get precision
                judges_tp_count=0
                judges_fp_count = 0
                judges_undecided_count = 0
                for candidate_id, vote_details in candidates.items():
                    if vote_details["TP_count"]>min_majority_count:
                        judges_tp_count+=1
                    else:
                        judges_fp_count+=1 # what to do about these.

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

                total_tps = judges_tp_count + bcb_exp_details_tps.count() + pf_exp_details_tps.count()
                total_fps = judges_fp_count + bcb_exp_details_fps.count() + pf_exp_details_fps.count()
                precision = total_tps * 100 / (total_fps + total_tps)

                data = {
                    "message": "finished",
                    "total_tps": total_tps,
                    "total_fps": total_fps,
                    "tps_usr": judges_tp_count,
                    "fps_usr": judges_fp_count,
                    "tps_bcb": bcb_exp_details_tps.count(),
                    "fps_bcb": bcb_exp_details_fps.count(),
                    "tps_pf": pf_exp_details_tps.count(),
                    "fps_pf": pf_exp_details_fps.count(),
                    "precision": precision,
                    "num_judges": num_judges,
                    "redirect_url": "send some url"}

                #response = JsonResponse(data=data)
                #response.status_code = 200
                #return response
                return render(request, "precisionCalculator/complete_experiment_report.html",
                          {'data': data, 'experiment': experiment})

            else:
                data = {"message": "This experiment has not been evaluated by any judges"}
                response = JsonResponse(data=data)
                response.status_code = 401
                return response
        else:
            data = {"message": "This experiment's detailed report can not be generated."}
            response = JsonResponse(data=data)
            response.status_code = 401
            return response
    except Experiment.DoesNotExist:
        data = {"message": "Invalid Experiment id."}
        response = JsonResponse(data=data)
        response.status_code = 401
        return response

class ExpDetailView(generic.DetailView):
    model = Experiment
    template_name = 'precisionCalculator/exp_detail.html'
