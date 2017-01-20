from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comments
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def post_list(request):
	print(request.method)
	posts = Post.objects.filter(published_date__lte = timezone.now()).order_by('published_date')
	return render(request, 'mblog/post_list.html', {'post':posts})

def post_detail(request, post_id):
	post = get_object_or_404(Post, pk = post_id)
	return render(request, 'mblog/post_detail.html', {'post': post})

@login_required
def post_new(request):
	print(request.path)
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			new_post = form.save(commit = False)
			new_post.author = request.user
			# post.published_date = timezone.now()
			new_post.save()
			return redirect('mblog:post_detail', post_id = new_post.id)
	else:
		form = PostForm()
		return render(request, 'mblog/post_edit.html', {'form': form})

@login_required
def post_edit(request, post_id):
	existing_post = get_object_or_404(Post, pk = post_id)
	if request.method == 'POST':
		print(request.POST)
		form = PostForm(request.POST, instance = existing_post)
		if form.is_valid():
			updated_post = form.save(commit = False)
			updated_post.author = request.user
			# updated_post.published_date = timezone.now()
			updated_post.save()
			return redirect('mblog:post_detail', post_id = updated_post.id)
	else:
		form = PostForm(instance = existing_post)
		return render(request, 'mblog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
	draft_posts = Post.objects.filter(published_date__isnull = True).order_by('created_date')
	return render(request, 'mblog/post_draft_list.html', {'draft_posts': draft_posts})

@login_required
def post_publish(request, post_id):
	post = get_object_or_404(Post, pk = post_id)
	post.published_date = timezone.now()
	post.save()
	return redirect('mblog:post_detail', post_id = post_id)

@login_required
def post_delete(request, post_id):
	post = get_object_or_404(Post, pk = post_id)
	post.delete()
	return redirect('mblog:post_list')

def add_comment_to_post(request, post_id):
	post = get_object_or_404(Post, pk = post_id)
	if request.Method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit = False)
			comment.post = post
			comment.save()
			return redirect('mblog:post_detail', post_id = post_id)
	else:
		form = CommentForm()
		return render(request, 'mblog/add_comment_to_post.html', {'form': form})






