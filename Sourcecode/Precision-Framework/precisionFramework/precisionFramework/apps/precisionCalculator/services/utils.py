from django.core.exceptions import MultipleObjectsReturned
import codecs
from ..models import CandidatePair, Block, BCBFunctions, BCBClones, ExperimentDetail
from django.utils import timezone
from django.conf import settings
from .httpservice import *
import os
from .predictor import Predictor
import math

def generate_filename_for_sampled_clonepairs(filename, username):
    d = timezone.now()
    time_stamp = string_i_want = ('%02d_%02d_%02d_%d' % (d.hour, d.minute, d.second, d.microsecond))[:-4]
    directory_path = "{media_root}/users/{username}/generated/clonepairs/{year}_{month}_{day}/{time_stamp}".format(
        media_root=settings.MEDIA_ROOT,
        username=username,
        year=d.year,
        month=d.month,
        day=d.day,
        time_stamp=time_stamp
    )
    file_path = "{directory}/{filename}".format(
        directory=directory_path,
        filename=filename
    )
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    return file_path


"""selected,1146149.java,64,121,selected,902388.java,1155,1218"""


def getFunctions(line):
    try:
        parts = line.split(",")
        function1 = BCBFunctions()
        function1.type = os.path.basename(os.path.normpath(parts[0]))
        function1.name = parts[1]
        function1.startline = int(parts[2])
        function1.endline = int(parts[3])
        function2 = BCBFunctions()
        function2.type = os.path.basename(os.path.normpath(parts[4]))
        function2.name = parts[5]
        function2.startline = int(parts[6])
        function2.endline = int(parts[7])
        return (function1, function2)
    except ValueError as e:
        raise ValueError("Invalid line detected: {line}".format(line=line))

def getCandidatePair(block_one, block_two):
    try:
        print("getCandidatePair block_one",getLengthActionDict(block_one.action_tokens), block_one.metric_hash)
        print("getCandidatePair block_two", getLengthActionDict(block_two.action_tokens), block_two.metric_hash)
    except:
        pass

    try:
        if block_one.tokens < block_two.tokens:
            candidate_one = block_one
            candidate_two = block_two
        elif block_two.tokens < block_one.tokens:
            candidate_one = block_two
            candidate_two = block_one
        else:
            if block_one.bcb_function_id < block_two.bcb_function_id:
                candidate_one = block_one
                candidate_two = block_two
            else:
                candidate_one = block_two
                candidate_two = block_one
        candidatepair = CandidatePair.objects.get(candidate_one=candidate_one,
                                                  candidate_two=candidate_two)

    except CandidatePair.DoesNotExist:
        candidatepair = CandidatePair()
        candidatepair.candidate_one = candidate_one
        candidatepair.candidate_two = candidate_two
        candidatepair.save()
    candidatepair.candidate_one = candidate_one  # imp these blocks have metrics and action tokens
    candidatepair.candidate_two = candidate_two  # imp these blocks have metrics and action tokens
    try:
        print("getCandidatePair candidate_one", getLengthActionDict(candidate_one.action_tokens))
        print("getCandidatePair candidate_two", getLengthActionDict(candidate_two.action_tokens))
    except:
        pass
    return candidatepair


def createBlockIfNeeded(func):
    block=None
    try:
        block = Block.objects.get(bcb_function_id=func.id)

    except Block.DoesNotExist:
        block = Block()
        block.bcb_function_id = func.id
        block.folder_name = func.type
        block.file_name = func.name
        block.start_line = func.startline
        block.end_line = func.endline
        block.tokens = func.tokens
        block.normalized_size = func.normalized_size
        block.hash = block.getSourceCodeHash()
        block.save()

    populateBlockActionTokensAndMetrics(block)
    return block

def getCandidatesForExperiment(experiment, candidates_not_in_bcb_or_pf, candidates_found_in_bcb,
                               candidates_found_in_pf):
    predictor = Predictor()
    line_counter = 0
    added_to_usr = 0
    added_to_bcb = 0
    added_to_pf = 0
    auto_t1_count = 0
    auto_t2_count = 0
    t2_count = 0
    auto_t3_count = 0
    with codecs.open(experiment.sampled_clonepairs, mode="r", encoding="utf-8") as clone_pairs:
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

                b1 = createBlockIfNeeded(f1)

                f2 = None
                try:
                    f2 = BCBFunctions.objects.get(name=function2.name,
                                                  type=function2.type,
                                                  startline=function2.startline,
                                                  endline=function2.endline,
                                                  )

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
                            #check Type1 clones
                            if candidate_pair.candidate_one.hash == candidate_pair.candidate_two.hash:
                                auto_t1_count+=1
                                candidates_found_in_pf.add(candidate_pair)
                                candidate_pair.resolution_type = ExperimentDetail.AUTO_T1
                                candidate_pair.clone_type = 1
                                candidate_pair.confirmed_status = CandidatePair.STATUS_TRUE
                                added_to_pf += 1
                                continue
                            #check Type2 clones
                            t2_detected = check_t2(candidate_pair)
                            if not t2_detected:
                                t3_detected = check_t3(candidate_pair,predictor)
                                if not t3_detected:
                                    if candidate_pair.confirmed_status == CandidatePair.STATUS_UNDECIDED:
                                        candidates_not_in_bcb_or_pf.add(candidate_pair)
                                        added_to_usr += 1
                                    else:
                                        candidates_found_in_pf.add(candidate_pair)
                                        added_to_pf += 1
                                        t2_count+=1
                                        candidate_pair.resolution_type = ExperimentDetail.ADDED_T2
                                        candidate_pair.clone_type = 2
                                    continue
                                else:
                                    candidates_found_in_pf.add(candidate_pair)
                                    candidate_pair.confirmed_status = CandidatePair.STATUS_TRUE
                                    added_to_pf += 1
                                    auto_t3_count += 1
                                    candidate_pair.resolution_type = ExperimentDetail.AUTO_T3_1
                                    candidate_pair.clone_type = 3
                                    continue
                            else:
                                candidates_found_in_pf.add(candidate_pair)
                                candidate_pair.confirmed_status = CandidatePair.STATUS_TRUE
                                added_to_pf += 1
                                auto_t2_count += 1
                                candidate_pair.resolution_type = ExperimentDetail.AUTO_T2
                                candidate_pair.clone_type = 2
                                continue

                    # clone pair found in BCB
                    if cp.similarity_token > 1 or cp.similarity_line > 1:
                        candidate_pair = getCandidatePair(b1, b2)
                        candidate_pair.source_type = CandidatePair.BCB_SOURCE_TYPE
                        candidate_pair.save()
                        candidate_pair.clone_type=cp.syntactic_type
                        candidates_found_in_bcb.add(candidate_pair)
                        added_to_bcb += 1

                    else:
                        candidate_pair = getCandidatePair(b1, b2)
                        # check Type2 clones
                        t2_detected = check_t2(candidate_pair)
                        if not t2_detected:
                            t3_detected = check_t3(candidate_pair, predictor)
                            if not t3_detected:
                                if candidate_pair.confirmed_status == CandidatePair.STATUS_UNDECIDED:
                                    candidates_not_in_bcb_or_pf.add(candidate_pair)
                                    added_to_usr += 1
                                else:
                                    candidates_found_in_pf.add(candidate_pair)
                                    added_to_pf += 1
                                    t2_count += 1
                                    candidate_pair.resolution_type = ExperimentDetail.ADDED_T2
                                    candidate_pair.clone_type = 2
                                continue
                            else:
                                candidates_found_in_pf.add(candidate_pair)
                                candidate_pair.confirmed_status = CandidatePair.STATUS_TRUE
                                added_to_pf += 1
                                auto_t3_count += 1
                                candidate_pair.resolution_type = ExperimentDetail.AUTO_T3_1
                                candidate_pair.clone_type = 3
                                continue
                        else:
                            candidates_found_in_pf.add(candidate_pair)
                            candidate_pair.confirmed_status = CandidatePair.STATUS_TRUE
                            added_to_pf += 1
                            auto_t2_count += 1
                            candidate_pair.resolution_type = ExperimentDetail.AUTO_T2
                            candidate_pair.clone_type = 2
                            continue
                except BCBFunctions.DoesNotExist:
                    print("f2 DoesNotExist  {f}".format(f=function2))
            except BCBFunctions.DoesNotExist:
                print("f1 DoesNotExist {f}".format(f=function1))
    print("processed {c} candidate pairs".format(c=line_counter))
    print("added to user {c} candidate pairs".format(c=added_to_usr))
    print("added to bcb {c} candidate pairs".format(c=added_to_bcb))
    print("added to pf {c} candidate pairs".format(c=added_to_pf))
    print("Auto T1 count {c} ".format(c=auto_t1_count))
    print("Auto T2 count {c} ".format(c=auto_t2_count))
    print("T2 count {c} ".format(c=t2_count))
    print("Auto T3 count {c} ".format(c=auto_t3_count))
    predictor.clear_session()

def getCandidatesForExperiment_no_auto_resolution(experiment, candidates_not_in_bcb_or_pf, candidates_found_in_bcb,
                               candidates_found_in_pf):
    predictor = Predictor()
    line_counter = 0
    added_to_usr = 0
    added_to_bcb = 0
    added_to_pf = 0
    auto_t1_count = 0
    auto_t2_count = 0
    t2_count = 0
    auto_t3_count = 0
    with codecs.open(experiment.sampled_clonepairs, mode="r", encoding="utf-8") as clone_pairs:
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

                b1 = createBlockIfNeeded(f1)

                f2 = None
                try:
                    f2 = BCBFunctions.objects.get(name=function2.name,
                                                  type=function2.type,
                                                  startline=function2.startline,
                                                  endline=function2.endline,
                                                  )

                    b2 = createBlockIfNeeded(f2)


                    candidate_pair = getCandidatePair(b1, b2)
                    candidates_not_in_bcb_or_pf.add(candidate_pair)
                    added_to_usr += 1
                except BCBFunctions.DoesNotExist:
                    print("f2 DoesNotExist  {f}".format(f=function2))
            except BCBFunctions.DoesNotExist:
                print("f1 DoesNotExist {f}".format(f=function1))
    print("processed {c} candidate pairs".format(c=line_counter))
    print("added to user {c} candidate pairs".format(c=added_to_usr))
    print("added to bcb {c} candidate pairs".format(c=added_to_bcb))
    print("added to pf {c} candidate pairs".format(c=added_to_pf))
    print("Auto T1 count {c} ".format(c=auto_t1_count))
    print("Auto T2 count {c} ".format(c=auto_t2_count))
    print("T2 count {c} ".format(c=t2_count))
    print("Auto T3 count {c} ".format(c=auto_t3_count))
    predictor.clear_session()

def check_t3(candidate_pair, predictor):
    try:
        if isSatisfySimilarity(candidate_pair):
            print("SIMILARITY MATCHES ")
            features = []
            features.append("1") # method_id_1
            features.append("2") # method_id_2
            features.append("0")  # clone label
            metrics_1 = candidate_pair.candidate_one.raw_metrics
            metrics_2 = candidate_pair.candidate_two.raw_metrics
            if metrics_1 and metrics_2:
                if "," in metrics_1 and "," in metrics_2:
                    list_metrics_1 = metrics_1.split(",")
                    list_metrics_2 = metrics_2.split(",")
                    if len(list_metrics_1)==len(list_metrics_2):
                        for i in range(0,len(list_metrics_1)):
                            features.append(str(list_metrics_1[i]))

                        for j in range(0, len(list_metrics_2)):
                            features.append(str(list_metrics_2[j]))

                        feature_vector = "~~".join(features)
                        prediction  = predictor.process(feature_vector)
                        print(prediction, feature_vector)
                        return prediction
        return False
    except:
        return False

def isSatisfySimilarity(candidate_pair):
    try:
        similarity = 0
        len_C1 = getLengthActionDict(candidate_pair.candidate_one.action_tokens)
        len_C2 = getLengthActionDict(candidate_pair.candidate_two.action_tokens)
        threshold = math.ceil(0.7 * max(len_C1, len_C2))
        print("******************************----BEGIN----********************************************************************")
        if len_C1 >=len_C2:
            for key, value in candidate_pair.candidate_one.action_tokens.items():
                value = int(value)

                if key in candidate_pair.candidate_two.action_tokens:
                    sim =  min(value,int(candidate_pair.candidate_two.action_tokens[key]))
                    print(key, sim, value, int(candidate_pair.candidate_two.action_tokens[key]))
                    similarity = similarity + sim
                    #if similarity >=threshold:
                    #    return True
        else:
            for key, value in candidate_pair.candidate_two.action_tokens.items():
                value = int(value)
                if key in candidate_pair.candidate_one.action_tokens:
                    sim =  min(value,int(candidate_pair.candidate_one.action_tokens[key]))
                    similarity = similarity + sim
                    #if similarity >=threshold:
                    #    return True
        print("candidate_id: ",candidate_pair.id, "similarity: ", similarity, " threshold: ", threshold, " len_C1:", len_C1,
              " len_C2:", len_C2)
        print("b1:", candidate_pair.candidate_one.getSourceCode())
        print("b2:", candidate_pair.candidate_two.getSourceCode())
        print(
            "******************************----END----********************************************************************")
        return similarity>=threshold
    except:
        return False

def getLengthActionDict(inp_dict):
    sum =0
    for key, value in inp_dict.items():
        sum = sum + int(value)
    return sum

def check_t2(candidate_pair):
    t2_detected=False
    try:
        if (candidate_pair.candidate_one.metric_hash and candidate_pair.candidate_two.metric_hash
                and candidate_pair.candidate_one.metric_hash == candidate_pair.candidate_two.metric_hash):
            for key, value in candidate_pair.candidate_one.action_tokens.items():
                if (key in candidate_pair.candidate_two.action_tokens
                        and value == candidate_pair.candidate_two.action_tokens[key]):
                    t2_detected = True
                    continue
                else:
                    t2_detected = False
                    break
        return t2_detected
    except:
        print("possibly ATs are missing, ignore this pair and return false")
        return False


def populateBlockActionTokensAndMetrics(block):
    response = send_post_request("metrics",block.getSourceCode())
    if response.status_code==200:
        #print("received: ", response.text)
        response_text = response.text
        print(response_text)
        if "@#@" in response_text:
            parts = response_text.split("@#@")
            metadata = parts[0]
            block.raw_metrics = parts[1]

            if "," in metadata:
                metadata_parts = metadata.split(",")
                metric_hash = metadata_parts[7]
                # set metric_hash
                block.metric_hash = metric_hash
                #print(metric_hash)
                #set actiontokens
                action_tokens = parts[2]
                if "," in action_tokens:
                    action_tokens_parts = action_tokens.split(",")
                    block.action_tokens = {}
                    for at_part in action_tokens_parts:
                        if ":" in at_part:
                            token_freq_parts = at_part.split(":")
                            token = token_freq_parts[0]
                            freq = token_freq_parts[1]
                            block.action_tokens[token]=freq
                else:
                    if ":" in action_tokens:
                        block.action_tokens = {}
                        token_freq_parts = action_tokens.split(":")
                        token = token_freq_parts[0]
                        freq = token_freq_parts[1]
                        block.action_tokens[token] = freq

                            #print(token, freq)
        try:
            print("AT len: ",getLengthActionDict(block.action_tokens))
        except:
            print("STRANGE RESPONSE: ", response_text)
