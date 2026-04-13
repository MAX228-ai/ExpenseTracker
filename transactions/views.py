import logging
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, FormView
)
from .models import Transaction
from .forms import TransactionForm, RegisterForm

logger = logging.getLogger('transactions')


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('transaction_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        logger.info(f'Jauns lietotājs reģistrēts: {user.username}')
        messages.success(self.request, f'Laipni lūdzam, {user.username}!')
        return super().form_valid(form)


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transactions/transaction_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset()
        context['total_balance'] = sum(t.amount for t in qs)
        context['transaction_count'] = qs.count()
        return context


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transaction_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        logger.info(
            f'Lietotājs {self.request.user.username} pievienoja transakciju: '
            f'{form.instance.amount} EUR [{form.instance.category}]'
        )
        messages.success(self.request, 'Transakcija veiksmīgi pievienota.')
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.error(
            f'Transakcijas izveides kļūda lietotājam {self.request.user.username}: {form.errors}'
        )
        messages.error(self.request, 'Lūdzu, izlabojiet kļūdas veidlapā.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Pievienot transakciju'
        context['btn_label'] = 'Pievienot'
        return context


class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transaction_list')

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def form_valid(self, form):
        logger.info(
            f'Lietotājs {self.request.user.username} atjaunināja transakciju id={self.object.pk}'
        )
        messages.success(self.request, 'Transakcija veiksmīgi atjaunināta.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Lūdzu, izlabojiet kļūdas veidlapā.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Rediģēt transakciju'
        context['btn_label'] = 'Saglabāt izmaiņas'
        return context


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = 'transactions/transaction_confirm_delete.html'
    success_url = reverse_lazy('transaction_list')

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def form_valid(self, form):
        logger.info(
            f'Lietotājs {self.request.user.username} dzēsa transakciju id={self.object.pk}'
        )
        messages.success(self.request, 'Transakcija dzēsta.')
        return super().form_valid(form)