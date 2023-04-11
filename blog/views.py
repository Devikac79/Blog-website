from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.db.models import Q

# Create your views here.
from .models import Post
from .forms import PostForm


def post_create(request):
    # if not request.user.is_authenticated():
    #     raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user=request.user
        # print( form.cleaned_data.get("title"))
        instance.save()
        messages.success(request, "Successfully created")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request, "Not successfully created")
    # form=PostForm
    # if request.method=="POST":
    #     print (request.POST.get("title"))
    #     # title= (request.POST.get("content"))
    #     # Post.objects.create(title=title)

    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_detail(request, id=None):
    instance = get_object_or_404(Post, id=id)#slug=slug
    # share_string=quote_plus(instance.content)
    context = {
        "title": instance.title,
        "instance": instance,
        # "share_string":share_string,
    }
    return render(request, "post_detail.html", context)
    # return HttpResponse("detail")


def post_list(request):
    queryset_list = Post.objects.all().order_by("-timestamp")
    
    query=request.GET.get("q")
    if query:
        queryset_list=queryset_list.filter(Q(title__icontains=query) |Q(content__icontains=query)|Q(user__first_name__icontains=query)).distinct()
        # queryset_list=queryset_list.filter(title__icontains=query)
    paginator = Paginator(queryset_list, 2)
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {
        "object_list": queryset,
        "title": "list"
    }
    return render(request, "post_list.html", context)

    # if request.user.is_authenticated:

    #     context={
    #         "title":"my user list"
    #     }
    #     return render(request,"index2.html",context)
    # else:
    #     context={
    #         "title":"list"
    #     }
    #     return render(request,"index.html",context)

    # return HttpResponse("list home")


def post_update(request, id=None):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None,
                    request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Item saved")

        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form": form
    }
    return render(request, "post_form.html", context)


def post_delete(request, id=None):
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "Item deleted")

    return redirect("list")
