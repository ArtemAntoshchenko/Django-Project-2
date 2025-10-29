from django.shortcuts import render, redirect
from django.views import generic
from .models import Book, BookInstance, Genre, Author
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import RenewBookForm
import datetime


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
@permission_required('catalog.can_edit', raise_exception=True)
def index(request):
    num_books=Book.objects.all().count()
    num_bookInstance=BookInstance.objects.all().count()
    num_bookInstance_available=BookInstance.objects.filter(status__exact='a').count()
    num_author=Author.objects.all().count()
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits
    return render(request, 'index.html', context={'num_books':num_books, 'num_bookInstance':num_bookInstance, 'num_bookInstance_available':num_bookInstance_available, 'num_author':num_author, 'num_visits':num_visits})

class BookListView(PermissionRequiredMixin,generic.ListView):
    book=Book
    context_object_name='book_list'
    # template_name='catalog/templates/book_list.html'
    paginate_by=5
    permission_required = ('catalog.can_mark_returned', 'catalog.change_book')
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
    
class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )


class AllBorrowedBookListView(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    template_name = 'catalog/all_borrowed_books.html'
    paginate_by = 5

    def get_queryset(self):
        return (
            BookInstance.objects.filter(status__exact='o')
            .order_by('due_back')
        )
    
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    if request.method == 'POST':
        form=RenewBookForm(request.POST)
        if form.is_valid():
            book_instance.due_back=form.cleaned_data['renewal_date']
            book_instance.save()
            return HttpResponseRedirect(reverse('borrowed-books'))
    else:
        prossed_renewal_date=datetime.date.today()+datetime.timedelta(weeks=3)
        form=RenewBookForm(initial={'renewal_date':prossed_renewal_date})
        return render(request, 'catalog/book_renew_librarian.html', {'form':form, 'book_instance':book_instance})
