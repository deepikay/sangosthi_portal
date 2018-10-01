"""
Definition of forms.
"""

from django import forms
from models import *
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.forms import modelformset_factory

QAModelFormset = modelformset_factory(
    AudioFile,
    fields=('name', ),
    extra=1,
    widgets={'name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Book Name here'
        })
    }
)
class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(widget=forms.PasswordInput)

class ShowForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = ( 'category', 'content','recording','cohort','STAT','show_stats','NoOfQuestions','QA1','QA2','QA3','QA4','QA5','QA6','QA7','QA8','QA9','QA10')
        #AddShow.html
        #change question number
    def __init__(self, *args, **kwargs):
        super(ShowForm,self).__init__(*args, **kwargs)
        self.fields['content'].queryset = Content.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                print("O~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print(category_id)
                qeryset = Content.objects.filter(category_id=category_id).order_by('name')
                for q in qeryset:
                    print(q)
                self.fields['content'].queryset=qeryset
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['Content'].queryset = self.instance.category.content_set.order_by('name')


class TextMessageForm(forms.ModelForm):
    class Meta:
        model = TextMessage
        fields = ( 'textMessage', 'recipientAshas','additionalPhoneNumbers',)

class ShowFeedbackForm(forms.ModelForm):
    class Meta:
        model = ShowFeedback
        fields = ( 'name','show','feedbackFile','textualFeedback',)


class SendAudioTrailerForm(forms.ModelForm):
    class Meta:
        model = SendAudioTrailer
        fields = ('show','choices','recipientAshas','additionalPhoneNumbers','timeAndDate','trailer','status',)




q=CustomUser.objects.all()
a=Asha.objects.all()
class CohortForm(forms.ModelForm):
    class Meta:
        model = Cohort
        fields = ( 'cohortID','broadcaster', 'listeners','author')
    listeners=forms.ModelMultipleChoiceField(queryset=Asha.objects.all(),widget=forms.CheckboxSelectMultiple)

class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ( 'name', 'localized','category','files',)


class ShowRecordingForm(forms.ModelForm):
    class Meta:
        model = ShowRecording
        fields = ( 'show', 'recordingFile',)




class SignUpForm(forms.ModelForm ):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ( 'full_name','email','location','password' )

        def save(self,commit=True):
            instance=super(SignUpForm,self).save(commit=False)
            if(commit):
                instance.save()
            return instance




class ContentCategoryForm(forms.ModelForm):
    class Meta:
        model = ContentCategory
        fields = ( 'name',)
class AudioFileForm(forms.ModelForm):
    class Meta:
        model=AudioFile
        fields=('audioFor','name','file','localized',)
        def save(self, commit=True):
            instance = super(AudioFileForm, self).save(commit=False)
            f = self['file'].value() # actual file object
            # process the file in a way you need
            if commit:
                instance.save()
            return instance
    #broadcaster = forms.ModelChoiceField(label=_("UP"),queryset=a, empty_label=None,
    #)
    #listeners=forms.ModelMultipleChoiceField(queryset=a)
class ExpertForm(forms.ModelForm):
    class Meta:
        model=ExpertProfile
        fields=( 'ExpertID','FullName','phoneNumber','dateOfBirth','location','area')
    dateOfBirth = forms.DateField(label=_("DOB"),
    widget=forms.DateInput({
        'placeholder': 'Enter DOB',
        'id':'datepicker'
        })       )


class NameForm(forms.ModelForm):
    class Meta:
        model = Asha
        fields = ('name', 'phoneNumber', 'ashaID' ,'location' ,'dateOfBirth' ,'area','YearOfJoining','author','PhoneType','photo')#,'received')

    name = forms.CharField(max_length=254,
    widget=forms.TextInput({
        'class': 'form-control',
        'placeholder': 'Name Of Asha'}))

    phoneNumber = forms.IntegerField(label=_("PhoneNumber"),
    widget=forms.NumberInput({
        'class': 'form-control',
        'placeholder': 'Enter a 10 digit Phone Number'})        )
    ashaID = forms.CharField(label=("AshaID"),
    widget=forms.TextInput({
        'class': 'form-control',
        'placeholder': 'Enter Asha ID'})        )
    location = forms.CharField(label=("location"),
    widget=forms.TextInput({
        'class': 'form-control',
        })        )
    dateOfBirth = forms.DateField(label=_("DOB"),
    widget=forms.DateInput({
        'class': 'form-control pull-right',
        'placeholder': 'Enter DOB',
        'id':'datepicker'
        })       )

    area = forms.CharField(label=("area"),
    widget=forms.TextInput({
        'class': 'form-control ',
        'placeholder': 'Enter the Area',
        })       )
    YearOfJoining = forms.CharField(widget=forms.Select(attrs={'class':'form-control select2','multiple':"multiple" ,'data-placeholder':"Select Year Of Joining",
                'style':"width: 100%;"})   )
    PhoneType =    forms.CharField(widget=forms.Select(attrs={'class':'form-control select2','multiple':"multiple" ,'data-placeholder':"Select Phone Type",
                'style':"width: 100%;"})   )
    LastUpdatedBy = forms.DateField(label=_("UP"),
    widget=forms.DateInput({'class': 'form-control pull-right','id':'datepicker'
        })       )
    #
    # photo = forms.ImageField(label=_("UP"),
    # widget=forms.FileInput({
    #     'class': 'form-control',
    #     'id':'exampleInputFile'
    #
    #     })       )
    author = forms.ModelChoiceField(label=_("UP"),queryset=q, empty_label=None,
    )

                # <input type="file" id="exampleInputFile">



    #ashaID = models.CharField(max_length=100, blank=True, null=True)
    #location = models.CharField(max_length=100, blank=True, null=True)
    #dateOfBirth = models.DateField(blank=True, null=True)
    #yearOfJoining = models.IntegerField(choices=year_dropdown, blank=True, null=True)
    #phoneType = models.CharField(choices=phoneChoices, max_length=100, blank=True)
    #photo

class AshaAdd(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))
