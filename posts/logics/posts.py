from posts.models import Posts


def get_posts_with_category(pk):
    return Posts.objects.filter(categories=pk)


def get_all_posts():
    return Posts.objects.all()
