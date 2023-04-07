from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreationForm, ContactForm
from django.core.mail import send_mail
from django.shortcuts import redirect, render


class SignUp(CreateView):
    form_class = CreationForm
    # После успешной регистрации перенаправляем пользователя на главную.
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


send_mail(
    'Тема письма',
    'Текст письма.',
    'from@example.com',  # Это поле "От кого"
    ['to@example.com'],  # Это поле "Кому" (можно указать список адресов)
    fail_silently=False
    # Сообщать об ошибках («молчать ли об ошибках?»)
)


def only_user_view(request):
    if not request.user.is_authenticated:
        # Если пользователь не авторизован - отправляем его на страницу логина.
        return redirect('/auth/login/')
    # Если пользователь авторизован — здесь выполняется полезный код функции.


def user_contact(request):
    # Проверяем, получен POST-запрос или какой-то другой:
    if request.method == 'POST':
        # Создаём объект формы класса ContactForm
        # и передаём в него полученные данные
        form = ContactForm(request.POST)

        # Если все данные формы валидны - работаем с "очищенными данными" формы
        if form.is_valid():
            # Берём валидированные данные формы из словаря form.cleaned_data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['body']
            # При необходимости обрабатываем данные
            # ...
            # сохраняем объект в базу
            form.save()

            # Функция redirect перенаправляет пользователя
            # на другую страницу сайта, чтобы защититься
            # от повторного заполнения формы
            return redirect('/thank-you/')

        # Если условие if form.is_valid() ложно и данные не прошли валидацию -
        # передадим полученный объект в шаблон,
        # чтобы показать пользователю информацию об ошибке

        # Заодно заполним все поля формы данными, прошедшими валидацию, 
        # чтобы не заставлять пользователя вносить их повторно
        return render(request, 'contact.html', {'form': form})

    # Если пришёл не POST-запрос - создаём и передаём в шаблон пустую форму
    # пусть пользователь напишет что-нибудь
    form = ContactForm()
    return render(request, 'contact.html', {'form': form})
