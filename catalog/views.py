from django.shortcuts import render
from django.views import generic
from .models import Book, BookInstance, Genre, Author

def index(request):
    num_books=Book.objects.all().count()
    num_bookInstance=BookInstance.objects.all().count()
    num_bookInstance_available=BookInstance.objects.filter(status__exact='a').count()
    num_author=Author.objects.all().count()
    return render(request, 'index.html', context={'num_books':num_books, 'num_bookInstance':num_bookInstance, 'num_bookInstance_available':num_bookInstance_available, 'num_author':num_author})

class BookListView(generic.ListView):
    book=Book
    context_object_name='book_list'
    # template_name='catalog/templates/book_list.html'
    paginate_by=5
    # queryset=Book.objects.filter(title__icontains='war'[:5])
    def get_queryset(self):
        return Book.objects.all()[:5]
    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context
    
class BookDetailView(generic.DetailView):
    book=Book