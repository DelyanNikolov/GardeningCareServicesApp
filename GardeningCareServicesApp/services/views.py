from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from GardeningCareServicesApp.accounts.models import ServiceProviderProfile, HomeOwnerProfile
from GardeningCareServicesApp.common.forms import ReviewForm
from GardeningCareServicesApp.services.forms import ServiceAddForm, ServiceEditForm, ServiceCategoryForm
from GardeningCareServicesApp.services.models import Service, Review

from django.db import IntegrityError, models
from django.contrib import messages


# Create your views here.

class ServicesListPage(ListView):
    model = Service
    template_name = 'services/service_list.html'
    context_object_name = 'services'
    paginate_by = 6

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = super().get_queryset()
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(category__name__icontains=query) |
                Q(description__icontains=query) |
                Q(provider__business_name__icontains=query)
            )
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add filled and empty star data for each service
        services = context['services']
        for service in services:
            reviews = service.service_reviews.all()
            if reviews.exists():
                average_rating = reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0
            else:
                average_rating = 0

            service.filled_stars = range(int(average_rating))
            service.empty_stars = range(5 - int(average_rating))

        context['query'] = self.request.GET.get('q', '')
        return context


class ServiceAddPage(LoginRequiredMixin, CreateView):
    model = Service
    template_name = 'services/service_create.html'
    form_class = ServiceAddForm
    success_url = reverse_lazy('services-list')

    def form_valid(self, form):
        service = form.save(commit=False)
        provider_profile = ServiceProviderProfile.objects.get(user=self.request.user)
        service.provider = provider_profile

        return super().form_valid(form)


class ServiceDetailsPage(DetailView):
    model = Service
    template_name = 'services/service_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = ReviewForm()
        # Calculate full stars and empty stars for each review
        reviews = self.object.service_reviews.all()
        context['reviews_with_stars'] = [
            {
                'review': review,
                'filled_stars': range(review.rating),
                'empty_stars': range(5 - review.rating)
            }
            for review in reviews
        ]
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ReviewForm(request.POST)

        if not request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to leave a review.")

        # Check if the user is a homeowner
        try:
            homeowner_profile = HomeOwnerProfile.objects.get(user=request.user)
        except HomeOwnerProfile.DoesNotExist:
            messages.error(request, "Only homeowners can leave reviews.")
            return redirect(reverse('service-details', args=[self.object.id]))

        # Check if the user has already reviewed this service
        if Review.objects.filter(service=self.object, user=homeowner_profile).exists():
            messages.error(request, "You have already reviewed this service.")
            return redirect(reverse('service-details', args=[self.object.id]))

        if form.is_valid():
            review = form.save(commit=False)
            review.service = self.object
            review.user = homeowner_profile
            try:
                review.save()
                messages.success(request, "Your review has been submitted.")
                return redirect(reverse('service-details', args=[self.object.id]))
            except IntegrityError:
                messages.error(request, "You have already reviewed this service.")
                return redirect(reverse('service-details', args=[self.object.id]))
        else:
            # If the form is invalid, re-render the page with form errors
            context = self.get_context_data()
            context['review_form'] = form
            return self.render_to_response(context)  # Ensure this path returns a response


class ServiceEditPage(LoginRequiredMixin, UpdateView):
    permission = 'services.change_service'
    model = Service
    form_class = ServiceEditForm
    template_name = 'services/service_edit.html'

    def get_object(self, queryset=None):
        service = get_object_or_404(Service, pk=self.kwargs['pk'])

        # Only owner of the service or user with permission are authorised to edit
        if service.provider.user != self.request.user and not self.request.user.has_perm(self.permission):
            raise PermissionDenied("You are not authorized to edit this service.")
        return service

    def get_success_url(self):
        service = get_object_or_404(Service, pk=self.kwargs['pk'])
        return reverse_lazy('provider-profile', kwargs={'pk': service.provider.pk})


class ServiceDeletePage(LoginRequiredMixin, DeleteView):
    permission = 'services.delete_service'
    model = Service
    template_name = 'services/service_delete.html'
    success_url = reverse_lazy('services-list')

    def get_object(self, queryset=None):
        service = super().get_object(queryset)

        # Only owner of the service or user with permission are authorised to edit
        if service.provider.user != self.request.user and not self.request.user.has_perm(self.permission):
            raise PermissionDenied("You are not authorized to delete this service.")
        return service


@login_required
def moderation_dashboard(request):
    if not request.user.has_perm('services.view_review'):
        raise PermissionDenied("You are not authorized to access this page.")

    pending_reviews = Review.objects.filter(is_approved=False)
    category_form = ServiceCategoryForm()

    if request.method == "POST":
        category_form = ServiceCategoryForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            return redirect('moderation-dashboard')

    return render(
        request,
        'services/moderation_dashboard.html',
        {'pending_reviews': pending_reviews, 'category_form': category_form}
    )



@login_required
def approve_review(request, pk):
    if not request.user.has_perm('services.change_review'):
        raise PermissionDenied("You are not authorized to access this page.")

    review = get_object_or_404(Review, pk=pk)
    review.is_approved = True
    review.save()
    return redirect('moderation-dashboard')


@login_required()
def delete_review(request, pk):
    if not request.user.has_perm('services.delete_review'):
        raise PermissionDenied("You are not authorized to access this page.")

    review = get_object_or_404(Review, pk=pk)
    review.delete()
    return redirect('moderation-dashboard')
