from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Ticket, TicketReply
from .forms import TicketForm, TicketReplyForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

# صفحه اصلی تیکت‌ها
@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(user=request.user)  # نمایش تیکت‌های کاربر وارد شده
    return render(request, 'support_app/ticket_list.html', {'tickets': tickets})

# ایجاد تیکت جدید
@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('../../tickets')  # بعد از ارسال تیکت به لیست تیکت‌ها می‌رویم
    else:
        form = TicketForm()
    return render(request, 'support_app/create_ticket.html', {'form': form})

# مشاهده تیکت
@login_required
def view_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # اگر کاربر خودش یا پشتیبانی این تیکت باشد، امکان مشاهده و ارسال پاسخ دارد
    if ticket.user != request.user and ticket.support_staff != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        reply_form = TicketReplyForm(request.POST)
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.ticket = ticket
            reply.user = request.user
            reply.save()
            return redirect('../../tickets', ticket_id=ticket.id)  # به صفحه تیکت برگردیم
    else:
        reply_form = TicketReplyForm()

    return render(request, 'support_app/view_ticket.html', {'ticket': ticket, 'reply_form': reply_form})

