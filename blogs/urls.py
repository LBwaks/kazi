from django.urls import path
from .views import BlogListView,DeleteBlogView,BlogDetailView,UpdateBlogView,TagView,AddBlogView
# ,LikeView
urlpatterns = [
    path('', BlogListView.as_view(), name='blogs'),
    path('<slug>',BlogDetailView.as_view(),name='blog_detail'),
    path('add_blog/',AddBlogView.as_view(),name='add_blog'),
    path('edit/<slug>',UpdateBlogView.as_view(),name='edit_blog'),
    path('delete/<slug>',DeleteBlogView.as_view(),name='delete_blog'),
    # path('like/<slug>',LikeView,name="like_blog"),
    path('tags/<slug>/',TagView,name='blog_tags')
]
