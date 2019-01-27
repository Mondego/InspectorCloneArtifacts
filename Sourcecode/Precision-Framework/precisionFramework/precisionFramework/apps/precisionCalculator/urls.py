from django.conf.urls import url
from . import views

app_name = 'precisionCalculator'

urlpatterns = [
    url(r'^tool/new$', views.tool_new, name='tool_new'),
    url(r'^exp/new$', views.exp_new, name='exp_new'),
    url(r'^judge/(?P<experiment_id>[0-9]+)/new$', views.judge_new, name='judge_new'),
    url(r'^judge/(?P<experiment_id>[0-9]+)/getInvitedJudgesList$', views.getJudgesForExperiemnt, name='judge_list'),
    url(r'^exp/(?P<experiment_id>[0-9]+)/getUploadStatus$', views.getUploadStatus, name='upload_status'),
    url(r'^exp/(?P<experiment_id>[0-9]+)/lockExperiment$', views.lockExperiment, name='lockexperiment'),
    url(r'^tool/(?P<pk>[0-9]+)/success$', views.ToolDetailView.as_view(), name='tool_detail'),
    url(r'^exp/(?P<pk>[0-9]+)/success$', views.ExpDetailView.as_view(), name='exp_detail'),
    url(r'^exp/(?P<experiment_id>[0-9]+)/evaluate$', views.exp_action_new, name='exp_evaluate'),
    url(r'^exp/(?P<experiment_id>[0-9]+)/experimentaction$', views.exp_action_start, name='exp_start'),
    url(r'^exp/(?P<experiment_id>[0-9]+)/initExp$', views.get_first_candidate_for_exp, name='initExp'),
    url(r'^exp/(?P<experiment_id>[0-9]+)/completedExp$', views.exp_action_finished, name='completedExp'),
    url(r'^exp/(?P<experiment_id>[0-9]+)/genReport$', views.generateDetailedReport, name='genReport'),
    url(r'^exp/(?P<experiment_id>[0-9]+)/nextpair$', views.exp_next_pair, name='next_pair'),
    url(r'^exp/(?P<experiment_id>[0-9]+)/setup$', views.setup_experiment, name='exp_setup'),
    url(r'^exp/pending$', views.get_pending_experiments, name='exp_pending'),
    url(r'^exp/unlocked$', views.get_unlocked_experiments, name='exp_unlocked'),
    url(r'^exp/completed$', views.get_completed_experiments, name='get_completed_exps'),
    url(r'^exp/loadType2$', views.loadType2s, name='loadType2'),
    url(r'^downloads/(?P<filename>[\w\-]+)/$',views.download_files, name='download_file'),
    url(r'^exp/(?P<experiment_id>[0-9]+)/initReplay$', views.get_first_candidate_for_replay, name='initReplay'),
    url(r'^exp/(?P<experiment_id>[0-9]+)/review$', views.exp_action_replay, name='exp_review'),
    url(r'^exp/(?P<experiment_id>[0-9]+)/experimentreplay$', views.exp_action_review, name='exp_replay'),
    url(r'^exp/(?P<experiment_id>[0-9]+)/isexperimentcomplete', views.isExperimentComplete, name='isExpComplete'),
]