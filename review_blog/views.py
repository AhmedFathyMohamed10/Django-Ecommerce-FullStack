from .models import Blog, Review, Comment
from .forms import BlogForm
from django.contrib.auth.decorators import login_required
from product.models import Product


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# decorators.py
from .decorators import unauthenticated_user, allowed_users, admin_only


def blogs(request):
    # get all blogs from database
    blogs = Blog.objects.all().order_by('-created_at')
    # get the number of blogs
    blog_count = blogs.count()
    # paginate blogs
    page = request.GET.get('page', 1) # get the page number
    paginator = Paginator(blogs, 3) # show 3 blogs per page
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)


    context = {
        'blogs': blogs,
        'blog_count': blog_count,
    }
    return render(request, 'reviews/blog.html', context)


def blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    context = {
        'blog': blog,
    }
    return render(request, 'reviews/blog_details.html', context)


@login_required(login_url='login')
def comment_on_blog(request, pk):
    
    try:
        blog = get_object_or_404(Blog, pk=pk)
        user_profile = request.user.profile
        
    except:
        blog = get_object_or_404(Blog, pk=pk)
        user_profile = None
    if request.method == 'POST':
        comment = request.POST.get('comment')
        # create comment
        Comment.objects.create(user=request.user, comment=comment, blog=blog, user_profile=user_profile)
        messages.success(request, 'Comment added successfully!')
        return redirect('blog-details', pk=blog.pk)

    else:
        messages.error(request, 'Error adding comment!')
        return redirect('blog-details', pk=blog.pk)


def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request, 'Blog created successfully!')
            return redirect('blogs')
    else:
        form = BlogForm()
    context = {
        'form': form,
    }
    return render(request, 'reviews/add_blog.html', context)



# create view for getting all reviews for a particular product
def reviews(request, pk):
    # 1- get the product and user who posted the review
    try:
        product = get_object_or_404(Product, pk=pk)
    except:
        messages.error(request, 'Product not found!')
        return redirect('home')

    print(f'product: {product}')
    # 2- get all reviews for the product
    reviews = Review.objects.filter(product=product)

    context = {
        'product': product,
        'reviews': reviews,
    }

    return render(request, 'reviews/reviews.html', context)


def add_review(request, pk):
    # 1- get the product
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        review = request.POST.get('review')
        # create review
        Review.objects.create(name=name, review=review, product=product)
        messages.success(request, 'Review added successfully!')
        return redirect('product-details', pk=product.pk)

    else:
        messages.error(request, 'Error adding review!')
        return redirect('product-reviews', pk=product.pk)


def delete_review(request, pk):
    # 1- get the review
    review = get_object_or_404(Review, pk=pk)
    # 2- get the product
    product = review.product
    # 3- delete the review
    review.delete()
    messages.success(request, 'Review deleted successfully!')
    return redirect('product-details', pk=product.pk)

