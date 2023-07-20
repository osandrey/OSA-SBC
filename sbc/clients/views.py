import os
import smtplib
import ssl
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views import View

from .forms import CreateCitizen, EditCitizen, SendEmailForm
from .models import Citizen
from dotenv import dotenv_values


CONFIG = dotenv_values('.env')
MetaLogin = CONFIG.get("MetaLogin")
MetaPassword = CONFIG.get("MetaPassword")




def root(request):
    return render(request, "clients/index.html", {})

def create_client_profile(request):


    if request.method == 'POST':
        form = CreateCitizen(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clients:got_success')
        else:
            return render(request, 'clients/create_citizen.html', context={"form": form})

    form = CreateCitizen()
    return render(request, 'clients/create_citizen.html', context={"form": form})


def got_success(request):
    return render(request, 'clients/success_page.html', {})



# def edit_client_profile(request):


def view_forms_list(request, page=1):


    citizens_model = Citizen.objects.all()

    # per_page = 100
    # paginator = Paginator(list(citizens_model), per_page)
    # citizens_on_page = paginator.page(page)
    return render(request, 'clients/list.html', {"citizens": citizens_model})



class CitizenObjectMixin(object):
    model = Citizen
    def get_object(self):
        _id = self.kwargs.get('id')
        obj = None
        if _id is not None:
            obj = get_object_or_404(self.model, pk=_id)
        return obj

    def get_id(self):
        return self.kwargs.get("id")


class CitizenView(CitizenObjectMixin, View):
    template_name = "clients/citizen_page.html"   # DetailView
    def get(self, request, id=None, *args, **kwargs):
        citizen = self.get_object()
        # print(f'!!!!!!!!!!!!!{citizen}')
        # GET method
        if self.template_name == 'clients/edit_citizen.html':
            citizen = get_object_or_404(Citizen, pk=id)
            form = EditCitizen()
            return render(request, 'clients/edit_citizen.html', context={"form": form, "citizen": citizen})
        context = {'citizen': citizen}
        return render(request, self.template_name, context)


    def post(self, request, id):
        if request.method == 'POST':
            form = EditCitizen(request.POST)
            print("I am in the POST")
            if form.is_valid():
                # form.save()
                self.update_citizen_view(form.cleaned_data)
                # print(form.cleaned_data.get('firstname'))
                return redirect('clients:view_forms_list')
            else:
                return render(request, 'clients/edit_citizen.html', context={"form": form})

        # obj = CitizenObjectMixin()
        # citizen_obj = obj.get_object()
        print("I am in the GET")
        citizen = get_object_or_404(Citizen, pk=id)
        form = EditCitizen()
        return render(request, 'clients/edit_citizen.html', context={"form": form, "citizen": citizen})



    def update_citizen_view(self, data: dict):
        citizen = self.get_object()
        # _id = self.get_id()
        # Citizen.objects.update_or_create(pk=_id, defaults={'firstname': data.get("firstname"),
        #                                                    "lastname": data.get("lastname"),
        #                                                    "email": data.get("email"),
        #                                                    "telephone_num": data.get("telephone_num"),
        #                                                    "age": data.get("age"),
        #                                                    "note": data.get("note"),
        #                                                    "stage": data.get("stage"),
        #                                                     })

        citizen.firstname = data.get('firstname')
        citizen.lastname = data.get('lastname')
        citizen.email = data.get('email')
        citizen.telephone_num = data.get('telephone_num')
        citizen.age = data.get('age')
        citizen.note = data.get('note')
        citizen.stage = data.get('stage')

        citizen.save()
        print('Update was successful')

    # def remove_citizen_view(self):
    #     citizen = self.get_object()
    #     citizen.delete()
    #     print('Deleting citizen form was successful')



class CitizenDeleteView(CitizenObjectMixin, View):
    template_name = 'clients/delete_citizen.html' # DetailView
    def get(self, request, id=None, *args, **kwargs):
        # GET method
        context = {}
        obj = self.get_object()
        if obj is not None:
            context['object'] = obj
        return render(request, self.template_name, context)

    def post(self, request, id=None,  *args, **kwargs):
        # POST method
        context = {}
        obj = self.get_object()
        if obj is not None:
            obj.delete()
            context['object'] = None
            print(context)
            return redirect('/clients/')
        return render(request, self.template_name, context)




def search_client_view(request):
    query = request.GET.get("q")
    print(query)
    citizens_model = Citizen.objects.filter(
        Q(firstname__icontains=query) |
        Q(lastname__icontains=query) |
        Q(email__icontains=query) |
        Q(telephone_num__icontains=query)

    )
    return render(request, 'clients/list.html', {"citizens": citizens_model})



def about_citizen(request, firstname):
    print('I Am in about_citizen Func!!!!!!!!!!!!')
    citizen = Citizen.objects.get(firstname=firstname)
    print(citizen)
    return render(request, "clients/citizen_page.html", {"citizen": citizen})




class CitizenSendEmail(CitizenObjectMixin, View):
    template_name = 'clients/send_email.html' # DetailView
    def get(self, request, id=None, *args, **kwargs):
        # GET method
        print('I am get method')
        context = {}
        obj = self.get_object()
        form = SendEmailForm()
        if obj is not None:
            context['object'] = obj

        return render(request, self.template_name, context={"form": form,"object": obj})

    def post(self, request, id=None,  *args, **kwargs):
        # POST method
        print('I am post method')
        context = {}
        obj = self.get_object()
        if obj is not None:
            self.send_email(request, obj)
            context['object'] = None
            return redirect('/clients/')
        return render(request, self.template_name, context)

    def handle_uploaded_file(self, file: InMemoryUploadedFile):
        # Generate a unique file name
        file_name = file.name
        upload_folder_path = "uploads/"
        if not os.path.exists(upload_folder_path):
            os.mkdir(upload_folder_path)

        file_path = upload_folder_path + file_name

        # Read the file contents
        file_contents = file.read()

        # Save the file to disk
        with open(file_path, 'wb') as destination:
            destination.write(file_contents)


        return file_path


    def send_email(self, request, obj):
        if request.method == 'POST':
            print('I am in send email POST method!')
            form = SendEmailForm(request.POST, request.FILES)
            if form.is_valid():
                # File upload handling logic

                attachment_file: InMemoryUploadedFile = form.cleaned_data['attachment']
                file_path = self.handle_uploaded_file(attachment_file)
                # Process the file as needed
                print('I am in sending email form is OK!')
                print(form.cleaned_data)

                run_send_email(obj, form.cleaned_data, file_path)
                return render(request, 'clients/success_page.html')
        else:
            form = SendEmailForm()
        return render(request, 'clients/send_email.html', {'form': form})



def run_send_email(obj: Citizen, data: dict, file_path: str):

    user_name = obj.firstname + " " + obj.lastname
    print(user_name)
    Host = 'smtp.meta.ua'
    Port = 465
    Sender = MetaLogin
    Sender_password = MetaPassword


    # Enter your address
    receiver_email = obj.email
    subject = f"Subject: Greetings, dear {user_name}, {data['theme']}"
    message = data['text']

    # mail = EmailMessage(subject=subject, body=message, from_email=Sender, to=[receiver_email],
    #                     cc=[data.get('coppy_to')])


    attachment_name = os.path.basename(file_path)

    with open(file_path, 'rb') as attachment:
        mail = EmailMessage(subject=subject, body=message, from_email=Sender, to=[receiver_email],
                            cc=[data.get('coppy_to')])
        mail.attach(attachment_name, attachment.read(), data.get('attachment').content_type)
        mail.send()

    # mail.attach(data.get('attachment').name, data.get('attachment').read(), data.get('attachment').content_type)
    # mail.send()

      # Enter receiver address
    # password = input("Type your password and press enter: ")
    # email_message = f"Subject: Hi {message.get('payload')[0]}\n {message.get('text')}"
    # context = ssl.create_default_context()
    # with smtplib.SMTP_SSL(Host, Port, timeout=30) as server:
    #     try:
    #         # context.check_hostname = False
    #         # server.starttls(context=context)
    #
    #         server.login(Sender, Sender_password)
    #
    #         message = MIMEMultipart()
    #         message['From'] = Sender
    #         message['To'] = receiver_email
    #         message['Subject'] = f"Subject: Greetings, dear {user_name},\n{data['theme']}"
    #         message.attach(MIMEText(data['text'], 'plain', 'utf-8'))
    #
    #         with open(file_path, 'rb') as attachment:
    #             file = MIMEImage(attachment.read(), _subtype='None')
    #             file.add_header('Content-Disposition', 'attachment', filename=data.get("attachment").name)
    #             message.attach(file)
    #
    #         server.send_message(message)
    #         print('Email was successfully sent!')
    #     except Exception as err:
    #         print(f'Error occurred: {err}')




#

# def edit_form(request, id):
#
#     if request.method == 'POST':
#         form = EditCitizen(request.POST)
#
#         if form.is_valid():
#             form.save()
#             return redirect('clients:view_forms_list')
#         else:
#             return render(request, 'clients/edit_citizen.html', context={"form": form})
#
#     # obj = CitizenObjectMixin()
#     # citizen_obj = obj.get_object()
#
#     citizen = get_object_or_404(Citizen, pk=id)
#     form = EditCitizen()
#     return render(request, 'clients/edit_citizen.html', context={"form": form, "citizen": citizen})