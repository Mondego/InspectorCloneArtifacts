from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
from django.utils.deconstruct import deconstructible
from zipfile import ZipFile, is_zipfile
from ..models import BCBFunctions

from random import randrange, sample
from django.utils import timezone
from django.conf import settings
from .utils import *
import codecs, os


@deconstructible
class ClonePairService(object):
    error_messages = {
        'extra_files': "Found more than one .txt files.",
        'low_valid_pairs': "Detected {count}. Needed atleast {pop_size}",
        'low_pairs': "Detected {count}. Needed atleast {pop_size}.",
    }

    def __init__(self, max_size=None, min_size=None):
        self.max_size = max_size
        self.min_size = min_size
        self.clonepairs_50_plus_tokens_filepath = ""

    def create_clonepair_files(self, filepath, username):
        #import getpass
        #print("getpass", getpass.getuser())
        self.setup_experiment_files(filepath.strip(), username)
        print("done with all steps")

    def setup_experiment_files(self, filepath, username):
        # experiment = get_object_or_404(Experiment, pk=experiment_id)
        # clonePairsPath = experiment.clonepairs
        #filepath="/home/saini/Documents/code/repo/statgin_pf/Precision-Framework/precisionFramework/precisionFramework/media/users/icse_v/uploads/clonepairs/2018_8_7/20_54_30_87/cwpais_th_7_mit1_bceformatted.zip"
        print("checking if there are more than 1 txt files in the zip: ", filepath, type(filepath))
        if is_zipfile(filepath):
            czip = ZipFile(filepath, 'r')
            try:
                print("Obtained a handle to read files inside Zip")
                txt_files = 0
                txt_name = ''
                for fileObj in czip.infolist():
                    print("found file: {n}".format(n=fileObj.filename))
                    if fileObj.filename.endswith(".txt"):
                        txt_files += 1
                        txt_name = fileObj.filename
                if txt_files > 1:
                    raise ValidationError(self.error_messages['extra_files'])
                print("Calling createFilteredCandiadtesFile method to create a sample")
                sampled_lines = self.createFilteredCandiadtesFile(czip, txt_name, username)
                print("sampled_lines", sampled_lines)
            finally:
                if czip:
                    czip.close()
        else:
            print("not a zip file")

    def createFilteredCandiadtesFile(self, czip, filename, username):
        MIN_TOKENS = 50
        # https://www.checkmarket.com/blog/how-to-estimate-your-population-and-survey-sample-size/
        MIN_POPULATION_SIZE = 100000
        SAMPLE_SIZE = 400
        total_valid_lines = 0
        all_lines = 0
        print("filename {f}".format(f=filename))
        clonefile = czip.open(filename, mode="r")
        try:
            for line in clonefile:
                all_lines += 1
        finally:
            if clonefile:
                clonefile.close()
        print("number of lines in the uploaded file: {c} ".format(c=all_lines))
        if all_lines < MIN_POPULATION_SIZE:
            params = {
                'count': all_lines,
                'pop_size': MIN_POPULATION_SIZE
            }
            raise ValueError(self.error_messages['low_pairs'].format(count=all_lines))

        prev_rand_nums = set()
        clonepairs_50_plus_tokens_filepath = generate_filename_for_sampled_clonepairs("50_tokens_and_more.txt",
                                                                                      username)
        self.clonepairs_50_plus_tokens_filepath = clonepairs_50_plus_tokens_filepath
        print("creating a file with clones greater than 50 tokens")
        iteration_count = 0
        valid_lines = set()
        added = set()
        pairs_dict= {}
        try:
            while True:
                lines_processed = -1
                if len(prev_rand_nums) >= all_lines:
                    raise ValueError(self.error_messages['low_valid_pairs'].format(count=total_valid_lines,
                                                                                   pop_size=MIN_POPULATION_SIZE))
                iteration_count += 1
                print("iteration_count is : {ic}".format(ic=iteration_count))
                rand_nums = set(sample(range(all_lines + 1), MIN_POPULATION_SIZE)).difference(prev_rand_nums)
                prev_rand_nums = prev_rand_nums.union(rand_nums)
                clonefile = czip.open(filename, mode="r")
                print("size of rand_nums: {s}, and size prev_rand_nums: {prev}".format(s= len(rand_nums),prev=len(prev_rand_nums)))
                try:
                    if lines_processed % 10000 == 0:
                        print("lines processed {c}, total_lines: {t}".format(c=lines_processed, t=all_lines))
                    for line in clonefile:
                        lines_processed += 1
                        if lines_processed in rand_nums:
                            line = line.decode("'utf-8'")
                            line = line.strip()
                            function1, function2 = getFunctions(line)
                            f1 = None
                            try:
                                f1 = BCBFunctions.objects.get(name=function1.name,
                                                              type=function1.type,
                                                              startline=function1.startline,
                                                              endline=function1.endline,
                                                              )

                                if f1.tokens >= MIN_TOKENS:
                                    f2 = None
                                    try:
                                        f2 = BCBFunctions.objects.get(name=function2.name,
                                                                      type=function2.type,
                                                                      startline=function2.startline,
                                                                      endline=function2.endline,
                                                                      )
                                        if f2.tokens >= MIN_TOKENS:

                                            combination1 = "{a},{b}".format(a=f1, b=f2)
                                            combination2 = "{b},{a}".format(a=f1, b=f2)
                                            if combination1 in added or combination2 in added:
                                                print("ignore this pair, it was added before")
                                            else:

                                                if self.pair_added_before(f1,f2, pairs_dict):
                                                    print("ignore this pair, it was added before from other source")
                                                    continue
                                                print("**** writing to file***", f1, f2)
                                                added.add(combination1)
                                                added.add(combination2)
                                                valid_lines.add(line)
                                                total_valid_lines = len(valid_lines)
                                                print("pairs sampled so far: {l}/{ss}".format(l=total_valid_lines,ss=SAMPLE_SIZE))
                                                if total_valid_lines == SAMPLE_SIZE:
                                                    print("done with sampling, writing samples to outfile")
                                                    with codecs.open(clonepairs_50_plus_tokens_filepath, mode="w+",
                                                                     encoding="utf-8") as outFile:
                                                        for pair in valid_lines:
                                                            outFile.write(pair + "\n")
                                                    return
                                                #print("{t}, {a}".format(t=total_valid_lines, a=lines_processed))
                                        else:
                                            pass
                                            #print("f2:", f2, lines_processed)
                                    except BCBFunctions.DoesNotExist:
                                        print("f2 DoesNotExist  {f}".format(f=function2))
                                else:
                                    pass
                                    #print("f1: ", f1, lines_processed)
                            except BCBFunctions.DoesNotExist:
                                print("f1 DoesNotExist {f}".format(f=function1))
                except Exception as e:
                    print("ERROR during sampleing")
                    print(e)
                finally:
                    if clonefile:
                        clonefile.close()
        except Exception as e:
            print("ERROR caught in While loop")
            print(e)
        finally:
            if clonefile:
                clonefile.close()

    def createFilteredCandiadtesFile_no_sampling(self, czip, filename, username):
        all_lines = 0
        print("filename {f}".format(f=filename))
        clonepairs_50_plus_tokens_filepath = generate_filename_for_sampled_clonepairs("50_tokens_and_more.txt",
                                                                                      username)
        self.clonepairs_50_plus_tokens_filepath = clonepairs_50_plus_tokens_filepath

        with codecs.open(clonepairs_50_plus_tokens_filepath, mode="w+",
                         encoding="utf-8") as outFile:
            clonefile = czip.open(filename, mode="r")
            try:
                for line in clonefile:
                    all_lines += 1
                    line = line.decode("'utf-8'")
                    line = line.strip()
                    outFile.write(line + "\n")
            finally:
                if clonefile:
                    clonefile.close()


        print("File created")



    def pair_added_before(self, f1,f2, pairs_dict):
        b1 = createBlockIfNeeded(f1)
        b2 = createBlockIfNeeded(f2)
        if b1.hash in pairs_dict:
            if b2.hash in pairs_dict[b1.hash]:
                return True
            else:
                set_of_clones_b1 = pairs_dict[b1.hash]
                set_of_clones_b1.add(b2.hash)

                if b2.hash in pairs_dict:
                    set_of_clones_b2 = pairs_dict[b2.hash]
                    set_of_clones_b2.add(b1.hash)
                else:
                    set_of_clones_b2 = set()
                    set_of_clones_b2.add(b1.hash)
                    pairs_dict[b2.hash] = set_of_clones_b2
                return False

        if b2.hash in pairs_dict:
            if b1 in pairs_dict[b2.hash]:
                return True
            else:
                set_of_clones_b2 = pairs_dict[b2.hash]
                set_of_clones_b2.add(b1.hash)

                if b1.hash in pairs_dict:
                    set_of_clones_b1 = pairs_dict[b1.hash]
                    set_of_clones_b1.add(b1.hash)
                else:
                    set_of_clones_b1 = set()
                    set_of_clones_b1.add(b2.hash)
                    pairs_dict[b1.hash] = set_of_clones_b1
                return False

        else:
            set_of_clones_1 = set()
            set_of_clones_1.add(b2.hash)
            pairs_dict[b1.hash] = set_of_clones_1

            set_of_clones_2 = set()
            set_of_clones_2.add(b1.hash)
            pairs_dict[b2.hash] = set_of_clones_2

            return False


    def __eq__(self, other):
        return isinstance(other, ClonePairService)
