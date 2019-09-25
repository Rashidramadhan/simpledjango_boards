from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .forms import NewTopicForm
from .models import Board, Topic, Post

# Create your views here.
def home(request):
    boards = Board.objects.all()
    context = {
        'boards': boards
    }

    return render(request, 'home.html', context)

def board_topics(request, pk):
    try:
        board = get_object_or_404(Board, pk=pk)
        context = {
            'board': board
        }
    except Board.DoesNotExist:
        raise Http404

    return render(request, 'topics.html', context)



def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('board_topics', pk=board.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})