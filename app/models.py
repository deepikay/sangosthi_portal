"""
Definition of models.
"""
from .validators import validate_audiofile_extension, validate_phonenumbers_list
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.core.validators import int_list_validator

from django.utils import timezone

from django.db import models
from django.contrib.auth.models import ( AbstractBaseUser ,BaseUserManager)
# from author.decorators import with_author
import datetime
from django.contrib.auth import get_user_model as user_model
from django.contrib.auth.models import PermissionsMixin

from python_webapp_django import settings

showRecordingsPath = 'static/Uploads/show_recordings/'
showFeedbackPath = 'static/Uploads/show_feedback/'
combinedRecordingsPath = 'static/Uploads/show_recordings/combined_recordings/'
statsPath = 'static/Uploads/show_stats/'

# from smart_selects.db_fields import ChainedForeignKey


def audioFilesPath(instance, filename):
	return 'Static/Uploads/Audio_Files/' + instance.audioFor + '/' + filename

class UserManager(BaseUserManager):
    def create_user(self,email,location,password=None,is_active=True,is_staff=False,is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueWrror("Users mus habe a password")
        if not location:
            raise ValueWrror("Users mus habe a password")

        user_obj=self.model(
        email=self.normalize_email(email)
        )
        user_obj.location=location

        user_obj.set_password(password)
        user_obj.save(using=self._db)
        user_obj.staff=is_staff
        user_obj.admin=is_admin
        user_obj.active=is_active

        return user_obj
    def create_staffuser(self,location,email,password=None):
        user=self.create_user(email,location,password=password,is_staff=True)
        return user
    def create_superuser(self,location,email,password=None):
        user=self.create_user(email,location,password=password,is_staff=True,is_admin=True)
        return user

year_dropdown = []
for y in range(1980, (datetime.datetime.now().year + 10)):
	year_dropdown.append((y, y))

import datetime

from django.utils.deconstruct import deconstructible

@deconstructible
class CustomUser(AbstractBaseUser,PermissionsMixin):
    mail_sent=models.BooleanField(default=False)
    MA=models.BooleanField(default=False)
    SA=models.BooleanField(default=False)
    UA=models.BooleanField(default=False)
    is_Valid=models.BooleanField(default=False)
    full_name=models.CharField(max_length=255,blank=True,null=True)
    email=models.EmailField(max_length=255,unique=True)
    location=models.CharField(max_length=255)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['location'] #python manage.py createsuperuser
    objects=UserManager()
    def __str__(self):
        return self.email + seld.objects.MA
    def get_full_name(self):
        return self.full_name
    def get_short_name(self):
        return self.full_name


from django.forms import ModelForm
def get_exam():
    return CustomUser.objects.get(email="abc@m.com")
class Asha(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=100, blank=False, null=False)
    phoneNumber = models.BigIntegerField(null=False, unique=True, blank=False)
    ashaID = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)
    dateOfBirth = models.DateField(blank=True, null=True)
    YearOfJoining = models.IntegerField(choices=year_dropdown, blank=True, null=True)
    PhoneType = models.CharField( max_length=100, blank=True)
    photo = models.ImageField( upload_to='static/app/', height_field=None, width_field=None, max_length=100, blank=True, null=True)
    def __unicode__(self):
		return self.name + ' | ' + str(self.location)
# Create your models here.
class Cohort(models.Model):
	author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,)
	cohortID = models.CharField(max_length=100, unique=True, blank=False, null=False)
	broadcaster = models.ForeignKey('Asha', on_delete=models.CASCADE, blank=False, null=False, unique=False, related_name='broadcastedBy')
	listeners = models.ManyToManyField('Asha', blank=True, related_name='listenedBy')
	status =models.BooleanField(default=False)
	def __unicode__(self):
		q=[]
		for i in self.listeners.all():
			q.append(str(i))
		return str(self.broadcaster) +" "+str(self.status)+" "+str(q)























class Show(models.Model):
	showID = models.CharField(max_length=100, unique=True, editable=False, blank=False, null=False)
	category = models.ForeignKey('ContentCategory', on_delete=models.CASCADE, blank=False, unique=False, null=True)

	content = models.ForeignKey('Content',on_delete=models.CASCADE, blank=False, unique=False, null=True, verbose_name='topic')

	recording = models.FileField(upload_to=combinedRecordingsPath, max_length=200, blank=True, null=True, validators=[validate_audiofile_extension])
	cohort = models.ForeignKey('Cohort', on_delete=models.CASCADE, blank=False, null=True, unique=False)
        STAT=models.BooleanField(default=False,editable=True)
	cho = ((0,0),
		(1, 1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10)
	)

	NoOfQuestions=models.IntegerField(null=False, blank=False,choices=cho)

	show_stats = models.FileField(upload_to=statsPath, max_length=200, blank=True, null=True)
	QA1 = models.ForeignKey('AudioFile',related_name='QA1_audio', blank=True,null=True,default="") #, limit_choices_to={'audioFor': 'Q&A'}

 	QA2 = models.ForeignKey('AudioFile',related_name='QA2_audio',  default="",null=True,blank=True) #, limit_choices_to={'audioFor': 'Q&A'}
	QA3 = models.ForeignKey('AudioFile',related_name='QA3_audio', blank=True,null=True,default="") #, limit_choices_to={'audioFor': 'Q&A'}

 	QA4 = models.ForeignKey('AudioFile',related_name='QA4_audio',  default="",null=True,blank=True) #, limit_choices_to={'audioFor': 'Q&A'}
	QA5 = models.ForeignKey('AudioFile',related_name='QA5_audio', blank=True,null=True,default="") #, limit_choices_to={'audioFor': 'Q&A'}

 	QA6 = models.ForeignKey('AudioFile',related_name='QA6_audio',  default="",null=True,blank=True) #, limit_choices_to={'audioFor': 'Q&A'}
	QA7 = models.ForeignKey('AudioFile',related_name='QA7_audio', blank=True,null=True,default="") #, limit_choices_to={'audioFor': 'Q&A'}

 	QA8 = models.ForeignKey('AudioFile',related_name='QA8_audio',  default="",null=True,blank=True) #, limit_choices_to={'audioFor': 'Q&A'}
	QA9 = models.ForeignKey('AudioFile',related_name='QA9_audio', blank=True,null=True,default="") #, limit_choices_to={'audioFor': 'Q&A'}

 	QA10 = models.ForeignKey('AudioFile',related_name='QA10_audio',  default="",null=True,blank=True) #, limit_choices_to={'audioFor': 'Q&A'}

        #question2 = models.ForeignKey('AudioFile',related_name='question2_audio', null=True, default="", blank=True, limit_choices_to={'audioFor': 'Q&A'})

        #answer2 = models.ForeignKey('AudioFile',related_name='answer2_audio', null=True, default="",blank=True, limit_choices_to={'audioFor': 'Q&A'})

        #question3 = models.ForeignKey('AudioFile',related_name='question3_audio', default=0, blank=True, limit_choices_to={'audioFor': 'Q&A'})

        #answer3 = models.ForeignKey('AudioFile',related_name='answer3_audio', default=0,blank=True, limit_choices_to={'audioFor': 'Q&A'})

	# preFeedback = ChainedForeignKey('Show',
	# 	chained_model_field='cohort',
	# 	limit_choices_to={'status': 1},
	# 	auto_choose=False,
	# 	show_all=False,
	# 	on_delete=models.CASCADE,
	# 	blank=True,
	# 	unique=False,
	# 	null=True,
	# 	help_text='The latest audio feedback of the show selected in this dropdown will be played, when the current show starts.')
	#
	timeOfAiring = models.DateTimeField( auto_now_add=True)
	status = models.IntegerField(blank=False, default=0, choices=((0,'Due'),(1,'Done')))

	def pre_feedback_player(self):
		if self.preFeedback:
			preFeedback = ShowFeedback.objects.filter(show=self.preFeedback.id).order_by('created_at')
			if len(preFeedback) == 0:
				return 'The show selected for getting pre-feedback does not have any feedback attached to it.'
			else:
				preFeedback = preFeedback[len(preFeedback)-1]
				file_url = settings.MEDIA_URL + str(preFeedback.feedbackFile)
				# file_url = self.recording
				player_string = '<p>' + str(preFeedback.name) + '</p>' + '<audio src="%s" controls preload="auto" autobuffer>Your browser does not support the audio element.</audio>' % (file_url)
				return player_string
		else:
			return 'No show selected for getting pre-feedback.'
	pre_feedback_player.allow_tags = True
	pre_feedback_player.short_description = 'Feedback to be played at the beginning of show'

	def file_link(self):
		f='/media/stat/'+self.showID+'/zipped.zip'
		if self.show_stats:
			return "<a href='%s'>download</a>" % (self.show_stats.url)
		else:
			return "NO ATTACHMENT"
	file_link.allow_tags = True
	file_link.short_description='Statistics File '
	def give_feedback_link(self):
		link = urlresolvers.reverse("admin:WebPortal_showfeedback_add") + "?show=" + str(self.id) #model name has to be lowercase
		return u'<a href="%s">%s</a>' % (link,'Give feedback for this show')

	give_feedback_link.allow_tags = True
	give_feedback_link.short_description = "Submit feedback"


	def get_feedback_players(self):
		feedbackPlayers = ''
		feedbacks = ShowFeedback.objects.filter(show=self.id)
		print str(feedbacks)
		for feedback in feedbacks:
			file_url = settings.MEDIA_URL + str(feedback.feedbackFile)
			player_string = '<audio src="%s" controls preload="auto" autobuffer>Your browser does not support the audio element.</audio>' % (file_url)
			feedbackPlayers = feedbackPlayers + '<p>' + str(feedback.name) + '</p>' + player_string + '<br><br>'
		return feedbackPlayers

	get_feedback_players.short_description = "Feedback"
	get_feedback_players.allow_tags = True

	def get_cohort_link(self):
		link = urlresolvers.reverse("admin:WebPortal_cohort_change", args=[self.cohort.id] ) #model name has to be lowercase
		return u'<a href="%s">%s</a>' % (link,'click to view Cohort members')
	get_cohort_link.short_description = 'Cohort'
	get_cohort_link.allow_tags = True

	def getBroadcaster(self):
		return self.cohort.broadcaster.name
	getBroadcaster.short_description = 'Broadcaster'

	class Meta:
		unique_together = ('cohort', 'timeOfAiring',)

	def recording_player(self):
		"""audio player tag for admin"""
		if self.recording:
			file_url = settings.MEDIA_URL + str(self.recording)
			# file_url = self.recording
			player_string = '<audio src="%s" controls preload="auto" autobuffer>Your browser does not support the audio element.</audio>' % (file_url)
			return player_string
		else:
			return 'No recording uploaded'
	recording_player.allow_tags = True
	recording_player.short_description = ('Show recording player')

	def get_recording_file_name(self):
		if self.recording:
			return self.recording.name
		else:
			return 'No recording uploaded'
	get_recording_file_name.short_description = 'Show recording audio file'

	def save(self, *args, **kwargs):
		super(Show, self).save(*args, **kwargs)
		self.showID = 'show_' + str(self.id)
		super(Show, self).save(*args, **kwargs)
	def __unicode__(self):
		return str(self.cohort) + ' | ' + str(timezone.localtime(self.timeOfAiring).strftime("%c"))



class Content(models.Model):
	contentID = models.CharField(max_length=100, unique=True, editable=False, blank=False, null=False)
	name = models.CharField(max_length=100, blank=False, null=False, verbose_name='Topic')
	localized = models.CharField(max_length=100, blank=False, null=True, verbose_name='Localised Name')
	category = models.ForeignKey('ContentCategory', on_delete=models.CASCADE, blank=False, null=False, unique=False)
	files = models.ManyToManyField('AudioFile', blank=False, limit_choices_to={'audioFor': 'content'} )

	def get_content_players(self):
		contentPlayers = ''
		for file in self.files.all():
			file_url = settings.MEDIA_URL + str(file.file)
			player_string = '<audio src="%s" controls preload="auto" autobuffer>Your browser does not support the audio element.</audio>' % (file_url)
			contentPlayers += '<p>' + str(file.name) + '</p>' + player_string + '<br><br>'
		return contentPlayers

	get_content_players.allow_tags = True
	get_content_players.short_description = "Audio files in this content"

	class Meta:
		verbose_name_plural = "Content"
	def save(self, *args, **kwargs):
		super(Content, self).save(*args, **kwargs)
		self.contentID = 'content_' + str(self.id)
		super(Content, self).save(*args, **kwargs)
	def __unicode__(self):
		return self.name















class ContentCategory(models.Model):
	name = models.CharField(max_length=100, blank=False, null=False)
	class Meta:
		verbose_name_plural = "Content categories"
	def __unicode__(self):
		return self.name


class AudioFile(models.Model):
	audioFileChoices = (
		('content', 'content'),
		('trailer', 'trailer'),
		('Q&A', 'Q&A')
	)

	audioFor = models.CharField(choices=audioFileChoices, max_length=100, blank=False, null=True)
	name = models.CharField(max_length=100, blank=False, null=False, unique=True)
	file = models.FileField(upload_to=audioFilesPath, max_length=200, blank=False, null=True, validators=[validate_audiofile_extension])
	localized = models.CharField(max_length=100, blank=False, null=True, verbose_name='Localised Name')
	def __unicode__(self):
		return self.name + ' - ' + self.file.name


class ExpertProfile(models.Model):
    ExpertID = models.CharField(max_length=100, unique=True, blank=False, null=False)
    FullName = models.CharField(max_length=100, unique=True, blank=False, null=False)
    phoneNumber = models.BigIntegerField(null=False, unique=True, blank=False)
    dateOfBirth = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)

class TextMessage(models.Model):
	textMessage = models.TextField(max_length=1000, blank=False, null=True)
	recipientAshas = models.ManyToManyField('Asha', blank=True)
	additionalPhoneNumbers = models.TextField(max_length=1000, blank=True, null=True, validators=[int_list_validator, validate_phonenumbers_list], help_text="Add comma separated phone numbers. Please do not use any spaces in this field.")

	def get_recipient_ashas(self):
		return " | ".join([recipientAsha.__unicode__() for recipientAsha in self.recipientAshas.all()])
	get_recipient_ashas.short_description = 'Recipient Ashas'


class SendAudioTrailer(models.Model):
	sendAudioTrailerChoices = (
		('listeners only', 'listeners only'),
		('broadcaster only', 'broadcaster only'),
		('broadcaster and listeners', 'broadcaster and listeners'),
		('none', 'none')
	)
	show = models.ForeignKey('Show', on_delete=models.CASCADE, blank=True, null=True, unique=False)
	choices = models.CharField(choices=sendAudioTrailerChoices, max_length=100, blank=False, default='none')
	recipientAshas = models.ManyToManyField('Asha', blank=True, help_text="You may add additional Ashas here.", verbose_name='Other Ashas')
	additionalPhoneNumbers = models.TextField(max_length=1000, blank=True, null=True, validators=[int_list_validator, validate_phonenumbers_list], help_text="Add comma separated additional phone numbers. Please do not use any spaces in this field.")
	timeAndDate = models.DateTimeField(auto_now=False, auto_now_add=False, blank=False)
	trailer = models.ForeignKey('AudioFile', blank=False, null=True, limit_choices_to={'audioFor': 'trailer'}, on_delete=models.CASCADE )
	status = models.IntegerField(blank=False, default=0, choices=((0,'Not scheduled after last save'),(1,'Scheduled')))

	def get_trailer_file_name(self):
		if self.trailer:
			return self.trailer.file.name
		else:
			return 'No trailer uploaded'
	get_trailer_file_name.short_description = 'Show trailer audio file'

	def trailer_player(self):
		"""audio player tag for admin"""
		if self.trailer:
			file_url = settings.MEDIA_URL + str(self.trailer.file)
			player_string = '<p>' + self.trailer.file.name + '</p>'
			player_string += '<audio src="%s" controls preload="none">Your browser does not support the audio element.</audio>' % (file_url)
			return player_string
		else:
			return 'No trailer uploaded'
	trailer_player.allow_tags = True
	trailer_player.short_description = ('Show trailer player')


	def get_recipient_ashas(self):
		return " | ".join([recipientAsha.__unicode__() for recipientAsha in self.recipientAshas.all()])
	get_recipient_ashas.short_description = 'Other Ashas'

	def save(self, *args, **kwargs):
		super(SendAudioTrailer, self).save(*args, **kwargs)
		self.status = 0
		super(SendAudioTrailer, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.show.__unicode__()







class ShowFeedback(models.Model):
	created_at = models.DateTimeField(auto_now_add=True, blank=False, null=True, editable=False)
	updated_at = models.DateTimeField(auto_now=True, blank=False, null=True, editable=False)
	name = models.CharField(max_length=100, blank=False, null=False, help_text="Name of the person giving feedback.")
	show = models.ForeignKey('Show', on_delete=models.CASCADE, blank=False, null=True, unique=False)
	#, limit_choices_to={'status': 1}, help_text="Select a show from the dropdown. Click on the pencil if you want to view the show.")
	feedbackFile = models.FileField(upload_to=showFeedbackPath, max_length=200, blank=False, null=True, validators=[validate_audiofile_extension])
	textualFeedback = models.TextField(max_length=1000, blank=True, null=True)

	def audio_file_player(self):
		"""audio player tag for admin"""
		if self.feedbackFile:
			file_url = settings.MEDIA_URL + str(self.feedbackFile)
			player_string = '<audio src="%s" controls preload="none">Your browser does not support the audio element.</audio>' % (file_url)
			return player_string
		else:
			return 'No feedback file attached'
	audio_file_player.allow_tags = True
	audio_file_player.short_description = ('Audio feedback player')
        def save(self, *args, **kwargs):
                super(AudioFile, self).save(*args, **kwargs)
                #self.status = 0
                #super(SendAudioTrailer, self).save(*args, **kwargs)

	def get_show_link(self):
		link = urlresolvers.reverse("admin:WebPortal_show_change",args=[self.show.id]) #model name has to be lowercase
		return u'<a href="%s">%s</a>' % (link,self.show.__unicode__())
	get_show_link.short_description = 'Show'
	get_show_link.allow_tags = True

	def get_file_name(self):
		if self.feedbackFile:
			return self.feedbackFile.name
		else:
			return 'No feedback file attached'


	def __unicode__(self):
		return self.name + self.show.__unicode__()

class ShowRecording(models.Model):
	show = models.ForeignKey('Show', on_delete=models.CASCADE, blank=False, null=True, unique=False, help_text="Select a show from the dropdown")
	recordingFile = models.FileField(upload_to=showRecordingsPath, max_length=200, blank=False, null=True, validators=[validate_audiofile_extension])

	def recording_file_player(self):
		if self.recordingFile:
			file_url = settings.MEDIA_URL + str(self.recordingFile)
			player_string = '<audio src="%s" controls preload="none">Your browser does not support the audio element.</audio>' % (file_url)
			return player_string
		else:
			return 'No file uploaded'
	recording_file_player.short_description = "Audio player"
	recording_file_player.allow_tags = True

	def __unicode__(self):
		return str(unicode(self.show)) + ' | ' + unicode(self.recordingFile.name)
