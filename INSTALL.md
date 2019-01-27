# 1. Prerequisites
You need a desktop computer connected to internet, and a web browser in order to work with InspectorClone. We have tested InspectorClone on Chrome on iOS (Version 71.0.3578.98) and Firefox on Windows (Version 64.0.2).
# 2. Generate the Input for InspectorClone
InspectorClone is a web-based tool that assists in the precision evaluation of clone detection tools. Hence, its input is a clone pairs file generated by a clone detection tool. InspectorClone works for Java language and is based on BigCloneBench dataset [1]; therefore, the clone detection tool that is going to get evaluated needs to be run on this dataset so that its clone pairs on this dataset are detected. This dataset is available on the InspectorClone website for download (explained in **Section 3**).  In order to facilitate the use of InspectorClone, we have made the clone pairs predicted by a clone detection tool (iClones) on BigCloneBench dataset available with this package. The file is available for download after logging in to InspectorClone website. You can use this file as the input to InspectorClone, or if you have a clone pairs file from any clone detector, you can use the file that you own. 
# 3. Accessing InspectorClone
InspectorClone can be accessed at http://www.inspectorclone.org/. Accessing the tool's features requires having an account with InspectorClone. You can create an account on the website (by pressing the `Register` button on top-right part of the InspectorClone's home page). However, in order to make the process of running InspectorClone easier for you, we have created an account for you on the website. The credintials for this account are as follows: 
User name: `icse`
Password: `icse2019`
You can sign in to the website by pressing the `Sign in` button at the top-right part of InspectorClone's home page (next to the `Register` button).
After logging in to the website, you will see a button at the top-right of the page named `Download Dataset`. By pressing this button, you can download the BigCloneBench dataset which you need to run your tool on (to produce the clone pairs that serve as the input to InspectorClone). If you are going to use the clone pairs file provided by us, you do not need to download the dataset. Instead, you can download the clone pairs using the button named `Download Demo Clonepairs.zip` at the top-right part of this page. 
# 4. Setting up InspectorClone for Precision Studies
In order to evaluate the precision of your clone detection tool, you need to first register your tool on InspectorClone website, and then create an experiment for your tool using your tool's reported clone pairs. These steps are expalined throughout this section. It should be noted that in order to further ease the process of running InspectorClone for you, we have created an experiment with a registered tool on InspectorClone. You can directly start conducting a precision experiment using this experiment. If you intend to proceed with this experiment, you can skip the sections **4.1** and **4.2**, and proceed to **Section 5** to start the precision experiment with the available experiment, which is named `demo_experiment`. If you intend to create your own experiment, please follow the guidelines throughout the rest of this section.
## 4.1 Registering a Tool on InspectorClone
After logging in to InspectorClone website, you will see a button named `Start Here`. This button guides through the process of registering your tool. By pressing this button, you will be redirected to a webpage in which you provide three pieces of information about your tool: `Name`, `Version`, and a short `Description`. After submitting this information, your tool will be registered on InspectorClone's database, and you will be redirected to a page at which you can setup an experiment with your registered tool. The process of setting up an experiment is describd in **Section 4.2**.
## 4.2 Setting up an Experiment on InspectorClone
After Registering your tool on InspectorClone, you are redirected to a webpage with a button named `Setup Experiment`. By pressing this button, you will be redirected to a page at which you provide the information about your experiment. You can also get to this page by pressing the `Setup Experiment using an Existing Tool` button on the home page of InspectorClone (while logged in). The information that should be provided on this page include: a `Name` for your experiment (which you later will use to return to your experiment), the `Tool` this experiment aims to evaluate (should be selected from a drop down list of your registered tools), and a `File upload` button to upload the tool's clone pairs. This file needs to be a zip file containing the text file that has the clone pairs. Each line of this text file should correspond to a method pair (reported as a clone pair) with the following format: `method 1 directory, method 1 file, method 1 start line, method 1 end line, method 2 directory, method 2 file, method 2 start line, method 2 end line`. `directory` is the directory each method is located at (default, sample, or selected in BigCloneBench dataset), `file` is the name for the source file containing the method, `start line` is the line number at which the method starts, and `end line` is the line number at which the method ends. This file should not have a header.
After submitting the information, you may wait for a few seconds for the upload to complete. As soon as the upload is complete, you will be redirected to a webpage showing `Experiment Details`. InspectorClone preprocesses your clone pairs file in this page (filtering methods less than 50 tokens). You may need to remain on this page for a few minutes for the preparation to get done. Once the preparation step is complete, a button with `Invite Judges` caption appears on the current page. By pressing this button, you can invite judges to your experiment. Please note that judges need to have accounts on InspectorClone because you can invite them using their user names. On the `Invite Judges` page, you can type each judge's username to invite them. You can invite yourself as a judge to the experiment too.
After inviting judges, you need lock your experiment in order to let InspectorClone start the sampling process and resolving the pairs that it is capable of. Pressing `Lock Experiment` button will lock the experiment for you (which may take a few minutes). Once the experiment is locked, the invited judges will see the experiment in their home page (after they log in to InspectorClone) under the `Pending Experiment` section. If you are among the judges, you can also start your experiment by pressing `Begin Precision Experiment` in the current page.
It is worth mentioning that if you leave setting up your experiment at any point (before completing its setup), the experiment will appear under the `Incompleted Experiment Setups` section at your home page, and you can continue the setup from that section.
# 5 Conducting Precision Experiments using InspectorClone
The experiments that has been set up in InspectorClone appear under the `Pending Experiments` section of home page of judges (after they log in). Judges can click the `Evaluate` button appearing in front of each experiment's name to start their precision experiment. If you have set up your own experiment, you can find its name in this section, or if you are logged in with the credintials that we made available for you (username `icse`) and you want to proceed with the experiment we have pre-set up for you, you will find this experiment in this section with the name `demo_experiment`.
After selecting an experiment to evaluate, you will be redirected to a webpage that shows the two methods of each pair in a side-by-side manner, with highlights pertaining to Java language syntax to ease the judging process. In this page, you can mark a pair as `true positive` (if you believe it demonstrates a clone pair), or as `false positive` (if you think this pair does not indicate a clone pair). In case of selecting `true positive`, you can optionally select the type of clone pair. You can also (optionally) add a comment that you may have about this pair. By clicking `Submit` button, on this page, you can submit your vote to the database, and proceed to the next pair. Once you complete your exepriment, a report about your experiment (e.g., the precision of your tool, the number of false positives, etc.,) will be shown . The completed experiments appear under the section `Completed Experiments` at the home page of judges, and their reports can be viewed from that section too. Also, when all judges complete their experiments, an overall report about the precision of the tool (which has aggregated the votes of all participating judges) will be shown to the judges. This report can be accessed by pressing `View Aggregated Report` button on the View Report page. For quick observation, we have made examples of these reports available for you: if you are logged in with `icse` username, you will see `Demo_2` under the `Completed Experiments` section of your home page. By clicking `View Report`, you will see the precision report of this experiment based on user `icse`'s votes. In the View Report page, by clicking `View Aggregated Report` button, you will see the aggregated precision report of this experiment which is based on the votes of all judges who have participated in this experiment (including user `icse`).
# References
[1] J.  Svajlenko  and  C.  K.  Roy,“Evaluating  clone  detection  tools  with bigclonebench,”in Proceedings of the 2015  IEEE  International  Conference  on  Software Maintenance and Evolution (ICSME), pp. 131–140, Sept 2015.