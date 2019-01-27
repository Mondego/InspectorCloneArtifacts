This package contains documentation about InspectorClone, which is a web-based tool to facilitate the precision studies of clone detection tools. In addition to this, this package provides the materials related to the evaluation of this tool: the input data used in the evaluation (sampled clone pairs from 16 rounds of experiments), the pairs automatically resolved by InspectorClone, and the pairs marked as false positive by judges in their manual validations. Since InspectorClone is available on the web, you don't need its source code to execute it; however, we have made its source code available  so that the adaptation of source code for other uses is simplified. In the following sections, the materials contained in this package are explained.
# 1. InspectorClone Tool
InspectorClone, available at http://www.inspectorclone.org/, is designed as a web-based tool to faciliate the precision studies of clone detection tools. By automatically resolving a portion of clone pairs uploaded to it, InspectorClone helps in conducting precision evaluation of clone detectors. In order to automatically resolve the clone pairs, InspectorClone leverages information retrieval, software metrics and machine learning techniques. The precision evaluation of a clone detector using InspectorClone is carried out by following the steps listed below:
1. A  user who aims to evaluate the precision of a clone detector creates an account at  InspectorClone web site and registers his tool at the web site.
1. The user  downloads  the  Java source code dataset from the InspectorClone's website and runs  his tool on the dataset. At the end of this step, he/she has the clone pairs by his/her tool available.
1. The user uploads the identified clone pairs to InspectorClone website under his registered tool, and creates a precsion experiment for his tool.
1. The user invites as many judges as he wishes to his expriment (judges need to have accounts on InspectorClone).
1. InspectorClone filters out the methods that are less than 50 tokens, and then  selects  a  random  and statistically significant sample of the tool's clone pairs. Then, it automatically resolve as many pairs as it can from the sampled pairs.
1. The remaining  clone pairs  of  the  sample (not resolved by InspectorClone) are shown to the invited judges.
1. Each judge evaluates all the remaining pairs individually (tagging them as either true positive or false positive).
1. InspectorClone aggregates all judges' votes by taking the majority vote, and creates a precision report.

We have evaluated InspectorClone by desiging 16 precision experiments where five judges individually went through the resolved pairs in each of the experiments. The experiments were designed by running seven clone detection tools on the BigCloneBench source code dataset [1] (available at InspectorClone web site for download after logging in). One of the tools comes in two modes, and for each tool we designed two rounds of experiments; hence, a total of 16 experiments were conducted. The evaluation results show that InspectorClone is capable of reducing the number of clone pairs needed to be manually validated by an average of 39%. InspectorClone's source code is available in the `source_code` folder of this package.
Details on using InspectorClone for conducting precision experiments is explained in the `INSTALL` file.

# 2. Evaluation Artifacts
The evaluation of InspectorClone has been done by conducting 16 rounds of precision experiments using it. Seven clone detection tools were run on BigCloneBench source code dataset to get their reported clone pairs. The tools include: CCAligner [2], Oreo [3], SourcererCC [4], NiCad [5], CloneWorks [6], SimCad [7], iClones [8]. CloneWorks comes in two different modes (Conservative and Aggressive), and it was executed in both modes. Two rounds of precision experiments were designed for each set of reported clone pairs (consequently, a total of 16 experiments), and five judges independently reviewed the clone pairs that were resolved by InspectorClone to measure the precision of automatic resolution approach of InspectorClone. The folder named `evaluation` contains the artifacts pertaining to these sets of experiments. This folder contains the following folders:
* The folder named `sampled_pairs` contains the pairs InspectorClone sampled from each of the clone detectors' reported clone pairs in each round of precision experiments. That is 400 pairs per experiment, per clone detector. Each line of each file denotes a pair reported by the corresponding clone detector and consists of the following columns:
  * method1_dir: the directory (in BigCloneBench dataset) at which the source file of the first method in this clone pair is located. 
  * method1_file: the name of the source code file in which the first method in this clone pair is located. This file is inside `method1_dir` directory.
  * method1_startline: the line number  (in `method1_file`) from which the first method in the clone pair starts. 
  * method1_endline: the line number (in `method1_file`) at which the first method in the clone pair ends.
  * method2_dir: the directory (in BigCloneBench dataset) at which the source file of the second method in this clone pair is located.
  * method2_file: the name of the source code file in which the second method in this clone pair is located. This file is inside `method2_dir` directory.
  * method2_startline: the line number  (in `method2_file`) from which the second method in the clone pair starts. 
  * method2_endline: the line number (in `method2_file`) at which the second method in the clone pair ends.
* The folder named `pairs_resolved` contains the portion of sampled clone pairs from each experiment that was automatically resolved by InspectorClone. The format of each line in the files of this folder is similar to the files in the `sampled_pairs` folder.
* The folder named `false_positives` contains a file that has the false positives reported by each judge while manually evaluating the portion of clone pairs that were automatically resolved by InspectorClone. The format of the file in this folder is same as the ones in `sampled_pairs` folder, with an addition of one column, `judge_ids`, which shows the ids of judges who voted for each pair to be false positive.
# 3. Source Code
The source code for InspectorClone is located at the `Sourcecode` directory of this package.

# Summary
In summary, this package contains the following artifacts:
1.	Documents about the usage of [InspectorClone](http://www.inspectorclone.org/);
2.	The files related to the precision experiments conducted to evaluate InspectorClone;
3.	The source code of InspectorClone.

# References
[1] J.  Svajlenko  and  C.  K.  Roy,“Evaluating  clone  detection  tools  with bigclonebench,”in Proceedings of the 2015  IEEE  International  Conference  on  Software Maintenance and Evolution (ICSME), pp. 131–140, Sept 2015.

[2] P. Wang, J. Svajlenko, Y. Wu, Y. Xu, and C. K. Roy,“Ccaligner: A token based large-gap clone detector,”in Proceedings of the 40th International Conference on Software Engineering, ICSE '18 (New York, NY, USA), pp. 1066–1077, ACM, 2018.

[3] V. Saini, F. Farmahinifarahani, Y. Lu, P. Baldi, and C. V. Lopes,“Oreo: Detection of clones in the twilight zone," in Proceedings of the 2018 26th ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software Engineering. ESEC/FSE'18 (New York, NY, USA), pp. 354–365, ACM, 2018.

[4] H. Sajnani, V. Saini, J. Svajlenko, C. K. Roy, and C. V. Lopes, “Sourcerercc: Scaling code clone detection to big-code", in Proceedings of the 2016 IEEE/ACM 38th International  Conference  on  Software  Engineering  (ICSE),  pp.  1157–1168, May 2016.

[5] C.  K.  Roy  and  J.  R.  Cordy,  “Nicad:  Accurate  detection  of  near-miss intentional clones using flexible pretty-printing and code normalization," in Proceedings of the 2008 16th IEEE International Conference on Program Comprehension, pp. 172–181, June 2008.

[6] J. Svajlenko and C. K. Roy, “Fast and flexible large-scale clone detection with cloneworks,”in Proceedings of the 2017 IEEE/ACM 39th International Conference on Software Engineering Companion (ICSE-C) , pp. 27–30, May 2017.

[7] M. S. Uddin, C. K. Roy, and K. A. Schneider, “Simcad: An extensible and  faster  clone  detection  tool  for  large  scale  software  systems,”in Proceedings of the IEEE 21st International Conference on Program Comprehension (ICPC), pp. 236–238, IEEE, 2013.

[8] N.  Göde  and  R.  Koschke,  “Incremental  clone  detection,” in Proceedings of the 13th European  Conference  on  Software  Maintenance  and  Reengineering (CSMR), pp. 219–228, IEEE, 2009.

