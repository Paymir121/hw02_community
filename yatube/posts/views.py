from django.shortcuts import render, get_object_or_404
from .models import Post, Group, User
from django.core.paginator import Paginator
from .forms import PostForm

POST_COUNT_IN_THE_SAMPLE: int = 10

def index(request):
    posts = Post.objects.select_related('group')
    paginator = Paginator(posts, POST_COUNT_IN_THE_SAMPLE) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)

def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, POST_COUNT_IN_THE_SAMPLE) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)

def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_count = Post.objects.filter(author=author).count
    posts_list = Post.objects.all()
    template = 'posts/profile.html'
    page_number = request.GET.get('page')
    paginator = Paginator(posts_list, POST_COUNT_IN_THE_SAMPLE)
    page_obj = paginator.get_page(page_number)
    context = {'author': author,
               'post_count':  post_count,
               'page_obj': page_obj,
               }
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    author_post = Post.objects.filter(author=post.author).count()
    template = 'posts/post_detail.html'
    context = {'post': post,
                'author_post' : author_post,
    }
    return render(request, template , context) 


def post_create(request):
    template = 'posts/post_create.html'
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.save()
            return render(request,request.user)
        else:
            return render(request, template , {'form' : form})
    else:
        form = PostForm()
        return render(request, template , {'form' : form})
