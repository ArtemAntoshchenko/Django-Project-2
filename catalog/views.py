from django.shortcuts import render, redirect
from django.views import generic
from .models import Book, BookInstance, Genre, Author
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    num_books=Book.objects.all().count()
    num_bookInstance=BookInstance.objects.all().count()
    num_bookInstance_available=BookInstance.objects.filter(status__exact='a').count()
    num_author=Author.objects.all().count()
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits
    return render(request, 'index.html', context={'num_books':num_books, 'num_bookInstance':num_bookInstance, 'num_bookInstance_available':num_bookInstance_available, 'num_author':num_author, 'num_visits':num_visits})

class BookListView(generic.ListView):
    book=Book
    context_object_name='book_list'
    # template_name='catalog/templates/book_list.html'
    paginate_by=5
    # queryset=Book.objects.filter(title__icontains='war'[:5])
    # def lastViewedBooks(self, request, *args, **kwargs):
    #     self.object=self.get_object()
    #     pk=self.object.pk
    #     recently_viewed=request.session.get('recently_viewed',[])
    #     if pk in recently_viewed:
    #         recently_viewed.remove(pk)
    #     recently_viewed.insert(0,pk)
    #     request.session['recently_viewed']=recently_viewed
    #     recently_viewed_books = Book.objects.filter(
    #         pk__in=recently_viewed
    #     )
    #     request.session.modified=True
    #     context = super().get_context_data(**kwargs)
    #     context['recently_viewed_books']=recently_viewed_books
    #     return context
    def get_queryset(self):
        return Book.objects.all()[:5]
    # def get_context_data(self, **kwargs):
    #     context = super(BookListView, self).get_context_data(**kwargs)
    #     context['recently_viewed'] = 'recently_viewed'
    #     return context
    
class BookDetailView(generic.DetailView):
    book=Book
    def get_queryset(self):
        return Book.objects.all()
    
# def BookDetailView(request, pk):
#     try:
#         book = Book.objects.get(pk=pk)
#     except Book.DoesNotExist:
#         raise 'Book does not exist'

#     return render(request, 'catalog/book_detail.html', context={'book': book})

class AuthorListView(generic.ListView):
    author=Author
    context_object_name='author_list'
    paginate_by=5
    def get_queryset(self):
        return Author.objects.all()[:5]
    
class AuthorDetailView(generic.DetailView):
    author=Author
    def get_queryset(self):
        return Author.objects.all()
    

# def contact_view(request):
#     if request.method=='GET':
#         from_email = request.get('email')
#         protocol='http'
#         domain='127.0.0.1:8000'
#         html_message=render_to_string('Django-Project-2/templates/registration/password_reset_email.html',{'from_email':from_email, 'protocol':protocol, 'domain':domain})
#         send_mail(from_email=settings.DEFAULT_FROM_EMAIL, html_message=html_message, fail_silently=False)
    
