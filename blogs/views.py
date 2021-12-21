from django.http.response import HttpResponseRedirect
# from .forms import CommentForm
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from .models import Blog,Tag
from .forms import BlogForm,EditBlogForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,CreateView,DeleteView
from django.shortcuts import render,get_object_or_404
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.urls.base import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator

class BlogListView(ListView):
    model = Blog
    paginate_by = 2
    template_name ='blogs/blogs.html'
    ordering='-created_date'
class BlogDetailView(DetailView):
    model =Blog
    template_name = 'blogs/blog-details.html'

    def get_related_blogs_by_tags(self):
        return Blog.objects.filter(tag_slug=self.tag_slug).exclude(slug=self.slug)
        
    # def get_context_data(self,*args,**kwargs):
    #     context =super(BlogDetailView,self).get_context_data(**kwargs)
       
    # #    for like unlike
    #     blogs_to_like = get_object_or_404(Blog,slug=self.kwargs['slug'])
    #     total_likes = blogs_to_like.total_likes()
    #     liked=False
    #     if blogs_to_like.likes.filter(id=self.request.user.id).exists():
    #         like=False

    #     #  for commenting 
    #     blog_to_comment =get_object_or_404(Blog,slug=self.kwargs['slug'])
    #     form= CommentForm()
    #     comments=Blog_Comment.objects.filter(blog=blog_to_comment).order_by('-created_date',)

    #     context['total_likes']=total_likes
    #     context['liked']=liked
    #     context['form']=form
    #     context['blog_to_comment']=blog_to_comment
    #     context['comments']=comments
    #     return context

    # @method_decorator(login_required)
    # def post(self,request,slug,**kwargs):
    #     blog = get_object_or_404(Blog,slug=slug)
    #     new_comment =None
    #     form=CommentForm(request.POST)

    #     if form.is_valid():
    #         new_comment = form.save(commit=False)
    #         new_comment.user=request.user
    #         new_comment.blog=blog
    #         new_comment.save()

    #     comments=Blog_Comment.objects.filter(blog =blog).order_by('-created_date')
    #     context={'blog':blog,'form':form,'comments':comments
    #     }
    #     return render (request,'blogs/blog_detail.html',context)

class AddBlogView(LoginRequiredMixin,CreateView):
    model = Blog
    template_name = 'blogs/add-blog.html'
    form_class = BlogForm

    def form_valid(self, form):
        blog = form.save(commit=False)
        form.instance.user = self.request.user
        self.object =form.save()
        blog.save()
        form.save_m2m()
        return super(AddBlogView,self).form_valid(form)

        
class UpdateBlogView(LoginRequiredMixin,UpdateView):
    model = Blog 
    form_class = EditBlogForm
    template_name= 'blogs/edit-blog.html'

class DeleteBlogView(LoginRequiredMixin,DeleteView):
     model = Blog 
     template_name ='blogs/delete-blog.html'
     success_url= reverse_lazy('blogs')


def TagView(request,slug):
    tag_blog=get_object_or_404(Tag,slug=slug)
    blogs=Blog.objects.filter(tag=tag_blog)
    page=request.GET.get('page',1)
    paginator = Paginator(blogs, 2)
    try:
        blogs=paginator.page(page)
    except PageNotAnInteger:
        blogs=paginator.page(1)
    except EmptyPage:
        blogs=paginator.page(paginator.num_pages)
   
    return render(request,'Tags/blog_tags.html',{'slug':slug,'tag_blog':tag_blog,'blogs':blogs})

# @login_required
# def LikeView(request,slug):
#     blog=get_object_or_404(Blog,slug=request.POST.get('blog_slug'))
#     liked=False
#     if blog.likes.filter(id=request.user.id).exists():
#         blog.likes.remove(request.user)
#         liked=False
#     else:
#         blog.likes.add(request.user)
#         liked=True
#     return HttpResponseRedirect(reverse('blog_detail',args=[str(slug)]))
