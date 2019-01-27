from ..forms import ToolForm
from django.shortcuts import render, redirect
from ..models import Tool
from django.views import generic

def tool_new(request):
    if request.method == "POST":
        form = ToolForm(request.POST)
        if form.is_valid():
            tool = form.save(commit=False)
            tool.user = request.user.profile
            tool.save()
            return redirect('precisionCalculator:tool_detail', pk=tool.pk)
    else:
        form = ToolForm()
    return render(request, 'precisionCalculator/tool_new.html', {'form': form})

class ToolDetailView(generic.DetailView):
    model = Tool
    template_name = 'precisionCalculator/tool_detail.html'
