from django.shortcuts import render, HttpResponse,redirect
from blog.models import post, BlogComment
from django.contrib import messages
from blog.templatetags import extras
# Create your views here.
def blogHome(request):
    allposts =post.objects.all()
    context = {'allposts': allposts}
    return render(request, 'blog/blogHome.html', context)
    
def blogPost(request, slug):
    Post = post.objects.filter(slug=slug).first()
    Post.views = Post.views + 1
    Post.save()
    comments = BlogComment.objects.filter(Post=Post, parent=None)
    replies = BlogComment.objects.filter(Post=Post).exclude(parent=None)
    repDict = {}
    for reply in replies:
        if reply.parent.sno not in repDict.keys():
            repDict[reply.parent.sno] = [reply]
        else:
            
            repDict[reply.parent.sno].append(reply)
    print(comments, replies)
    context= {'Post': Post, 'comments': comments, 'user': request.user, 'repDict':repDict}
    
    return render(request, 'blog/blogPost.html', context)
    
def PostComment(request):
    if request.method == 'POST':
        comment = request.POST.get("comment")
        user = request.user
        PostSno = request.POST.get("PostSno")
        Post = post.objects.get(sno=PostSno)
        parentSno = request.POST.get("parentSno")
        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, Post=Post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully!")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, Post=Post, parent=parent)

            comment.save()
            messages.success(request, "Your Reply has been posted successfully!")
    return redirect (f"/blog/{Post.slug}")