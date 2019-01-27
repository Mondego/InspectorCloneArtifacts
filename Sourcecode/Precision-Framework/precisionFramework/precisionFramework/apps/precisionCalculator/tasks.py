# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .services import *
from .services.utils import *
from .models.experiment import Experiment
from .models.bcbfunction import BCBFunctions
import codecs


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def testPrint(msg):
    print("received: {m}".format(m=msg))


@shared_task
def task_process_input_clonepairs(username, input_filepath, experiment_id):
    print("received a task to process input clonepairs file for username: {u} and file: {f}".format(u=username,
                                                                                                    f=input_filepath))
    service = ClonePairService(min_size=0,
                               max_size=1024 * 1000 * 1000,
                               )
    print("calling service.create_clonepair_files", input_filepath, "**************")

    service.create_clonepair_files(input_filepath, username)
    try:
        experiment = Experiment.objects.get(pk=experiment_id)
        experiment.sampled_clonepairs = service.clonepairs_50_plus_tokens_filepath
        experiment.save()
    except Experiment.DoesNotExist:
        print("WARNING: experiment with this id not found.")

    print("done with the task, the sample file is ready.")


@shared_task
def task_load_type2():
    MIN_TOKENS = 50
    line_counter = 0
    added_to_pf = 0
    type2_clonepairs = "/Users/vaibhavsaini/Documents/sample_clone_pairs/type2_clones_intersected.txt"
    with codecs.open(type2_clonepairs, mode="r", encoding="utf-8") as clone_pairs:
        for line in clone_pairs:
            line_counter += 1
            line = line.strip()
            function1, function2 = getFunctions(line)
            f1 = None
            b1 = None
            b2 = None
            try:
                f1 = BCBFunctions.objects.get(name=function1.name,
                                              type=function1.type,
                                              startline=function1.startline,
                                              endline=function1.endline,
                                              )
                if f1.tokens < MIN_TOKENS:
                    continue
                f2 = None
                try:
                    f2 = BCBFunctions.objects.get(name=function2.name,
                                                  type=function2.type,
                                                  startline=function2.startline,
                                                  endline=function2.endline,
                                                  )
                    if f2.tokens < MIN_TOKENS:
                        continue
                    b1 = createBlockIfNeeded(f1)
                    b2 = createBlockIfNeeded(f2)
                    cp = None
                    try:
                        cp = BCBClones.objects.get(function_id_one=f1.id,
                                                   function_id_two=f2.id,
                                                   )
                    except MultipleObjectsReturned:
                        cp = BCBClones.objects.filter(function_id_one=f1.id,
                                                      function_id_two=f2.id,
                                                      ).first()
                    except BCBClones.DoesNotExist:
                        try:
                            cp = BCBClones.objects.get(function_id_one=f2.id,
                                                       function_id_two=f1.id)
                        except MultipleObjectsReturned:
                            cp = BCBClones.objects.filter(function_id_one=f2.id,
                                                          function_id_two=f1.id).first()
                        except BCBClones.DoesNotExist:
                            # this is not a clone pair as per BCB
                            candidate_pair = getCandidatePair(b1, b2)
                            if candidate_pair.candidate_one.hash == candidate_pair.candidate_two.hash:
                                # no need to add this, this is type1.
                                continue
                            if candidate_pair.confirmed_status == CandidatePair.STATUS_UNDECIDED:
                                candidate_pair.confirmed_status = CandidatePair.STATUS_TRUE
                                candidate_pair.source_type = CandidatePair.PRECISION_FRAMEWORK_SOURCE_TYPE
                                candidate_pair.type_two_count = 1
                                candidate_pair.save()
                                print("added: {c}".format(c=candidate_pair))
                            else:
                                # no need to add this pair, this pair is already present in pf
                                continue
                            continue

                    # clone pair found in BCB
                    if cp.similarity_token >= 0.7 or cp.similarity_line >= 0.7:
                        candidate_pair = getCandidatePair(b1, b2)
                        candidate_pair.source_type = CandidatePair.BCB_SOURCE_TYPE
                        candidate_pair.confirmed_status = CandidatePair.STATUS_TRUE
                        candidate_pair.save()
                    else:
                        candidate_pair = getCandidatePair(b1, b2)
                        if candidate_pair.confirmed_status == CandidatePair.STATUS_UNDECIDED:
                            candidate_pair.confirmed_status = CandidatePair.STATUS_TRUE
                            candidate_pair.source_type = CandidatePair.PRECISION_FRAMEWORK_SOURCE_TYPE
                            candidate_pair.type_two_count = 1
                            candidate_pair.save()
                            print("added: {c}".format(c=candidate_pair))
                        else:
                            # do nothing, already in pf
                            continue
                except BCBFunctions.DoesNotExist:
                    print("f2 DoesNotExist  {f}".format(f=function2))
            except BCBFunctions.DoesNotExist:
                print("f1 DoesNotExist {f}".format(f=function1))
    print("processed {c} candidate pairs".format(c=line_counter))
    print("added to pf {c} candidate pairs".format(c=added_to_pf))
