# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from . import models
import os
from django.utils import timezone
from pydub import AudioSegment
from django.conf import settings
from django.core.files import File
import datetime
import sys
sys.path.append('/home/sangoshthi/sangoshthi_new/sangoshthi_server/')

import portal_request_handler as esl

import mongo_file as mongo
# Register your models here.

class AshaAdmin(admin.ModelAdmin):
	list_display = ('name', 'phoneNumber', 'area')
	search_fields = ['name', 'phoneNumber', 'area']
	list_filter = ['area']
	expert_readonly_fields = ['photo','name','phoneNumber','phoneType','area','dateOfBirth','yearOfJoining']

	def get_readonly_fields(self, request, obj=None):
		if request.user.groups.filter(name='Expert').exists():
			return self.expert_readonly_fields
		else:
			return super(AshaAdmin, self).get_readonly_fields(request, obj=obj)

	class Media:
		js = ("instantsearch.js",)

class CohortAdmin(admin.ModelAdmin):
	list_display = ('get_broadcaster_name','get_broadcaster_phoneNumber','get_broadcaster_area')
	search_fields = ['get_broadcaster_name','get_broadcaster_phoneNumber','get_broadcaster_area']
	list_filter = ('broadcaster',)
	readonly_fields = ['author','updated_by']
	expert_readonly_fields = ['cohortID','get_broadcaster_link','get_listeners_links']

	def get_readonly_fields(self, request, obj=None):
		if request.user.groups.filter(name='Expert').exists():
			return self.expert_readonly_fields
		else:
			return super(CohortAdmin, self).get_readonly_fields(request, obj=obj)

	class Media:
		js = ("instantsearch.js",)

class ShowAdmin(admin.ModelAdmin):
	list_display = ('getBroadcaster', 'timeOfAiring', 'category', 'status', 'question1', 'answer1','question2', 'answer2', 'question3', 'answer3')
	list_filter = ('cohort', 'timeOfAiring', 'category', 'status')	
	search_fields = ['cohort', 'category', 'status']

	readonly_fields = ['pre_feedback_player', 'recording_player', 'get_feedback_players', 'author','updated_by']
	expert_readonly_fields = ('category','content','get_cohort_link','timeOfAiring','status', 'show_stats', 'recording_player', 'get_feedback_players', 'give_feedback_link')

	def get_queryset(self, request):
		qs = super(ShowAdmin, self).get_queryset(request)
		if request.user.groups.filter(name='Expert').exists():
			return qs.filter(status=1)
		return qs

	def get_readonly_fields(self, request, obj=None):
		if request.user.groups.filter(name='Expert').exists():
			return self.expert_readonly_fields
		else:
			return super(ShowAdmin, self).get_readonly_fields(request, obj=obj)

	class Media:
		js = ("instantsearch.js",)

class ShowRecordingAdmin(admin.ModelAdmin):
	list_display = ['show','recording_file_player']
	list_filter = ['show',]
	search_fields = ['show','recordingFile']

	actions = ['custom_delete_selected', 'combine_recordings']
	readonly_fields = ['recording_file_player','author','updated_by']

	def combine_recordings(self, request, queryset):
		show = list(set([ str(i.show.id) for i in queryset ]))
		if len(show) == 0:
			self.message_user(request, ("No shows selected"))
		elif len(show) > 1:
			self.message_user(request, ("The selected recordings should all belong to one show"))
		else:
			recordingPaths = [ str(i.recordingFile.path) for i in queryset ]
			flag = 1
			for recording in recordingPaths:
				if flag == 1:
					combinedRecording = AudioSegment.from_wav(recording)
					flag = 0
				else:
					combinedRecording += AudioSegment.from_wav(recording)
			try:
				outputFile = settings.BASE_DIR + str('/uploads/show_recordings/show' + show[0] + "_combined_recording.wav")
				print outputFile
				returnValue = combinedRecording.export(outputFile, format="wav")
				show = queryset[0].show
				with open(outputFile, 'rb') as recording:
					show.recording.save(str(show.id) + "_combined_recording.wav", File(recording), save=True)
				self.message_user(request, ("Selected recordings combined and attached to show."))	
			except Exception as e:
				print show
				self.message_user(request, ("Error in combining files " + str(e)))


	def custom_delete_selected(self, request, queryset):
		#custom delete code
		n = queryset.count()
		for i in queryset:
			if i.recordingFile:
				if os.path.exists(i.recordingFile.path):
					os.remove(i.recordingFile.path)
			i.delete()
		self.message_user(request, ("Successfully deleted %d recording files.") % n)
	custom_delete_selected.short_description = "Delete selected recordings"

	def get_actions(self, request):
		actions = super(ShowRecordingAdmin, self).get_actions(request)
		if not request.user.groups.filter(name='Expert').exists():
			del actions['delete_selected']
		return actions

	class Media:
		js = ("instantsearch.js",)

class ContentAdmin(admin.ModelAdmin):
	list_display = ('name', 'category', 'localized')
	search_fields = ['name', 'category']
	list_filter = ['category']
	readonly_fields = ['get_content_players','author','updated_by'];
	expert_readonly_fields = ['name', 'category', 'localized', 'get_content_players']
	def get_readonly_fields(self, request, obj=None):
		if request.user.groups.filter(name='Expert').exists():
			return self.expert_readonly_fields
		else:
			return super(ContentAdmin, self).get_readonly_fields(request, obj=obj)
	class Media:
		js = ("instantsearch.js",)






class AudioFileAdmin(admin.ModelAdmin):
	list_display = ('name', 'audio_file_player', 'get_file_name', 'audioFor')
	search_fields = ['name', 'get_file_name', 'audioFor']
	actions = ['custom_delete_selected']
	readonly_fields = ['author','updated_by']

	def custom_delete_selected(self, request, queryset):
		#custom delete code
		n = queryset.count()
		for i in queryset:
			if i.file:
				if os.path.exists(i.file.path):
					os.remove(i.file.path)
			i.delete()
		self.message_user(request, ("Successfully deleted %d audio files.") % n)
	custom_delete_selected.short_description = "Delete selected items"

	def get_actions(self, request):
		actions = super(AudioFileAdmin, self).get_actions(request)
		if not request.user.groups.filter(name='Expert').exists():
			del actions['delete_selected']
		return actions

	class Media:
		js = ("instantsearch.js",)

class ContentCategoryAdmin(admin.ModelAdmin):
	list_display = ('id','name')
	search_fields = ['id','name']
	
	readonly_fields = ['author','updated_by']


	class Media:
		js = ("instantsearch.js",)


class ShowFeedbackAdmin(admin.ModelAdmin):
	list_display = ('name', 'get_show_link', 'audio_file_player')
	search_fields = ['name', 'get_show_link']
	# actions = ['custom_delete_selected']
	readonly_fields = ['author','updated_by']
	list_filter = ['name','show']

	# def custom_delete_selected(self, request, queryset):
	# 	#custom delete code
	# 	n = queryset.count()
	# 	for i in queryset:
	# 		if i.file:
	# 			if os.path.exists(i.file.path):
	# 				os.remove(i.file.path)
	# 		i.delete()
	# 	self.message_user(request, ("Successfully deleted %d audio files.") % n)
	# custom_delete_selected.short_description = "Delete selected items"

	class Media:
		js = ("instantsearch.js",)

class SendAudioTrailerAdmin(admin.ModelAdmin):
	list_display = ('show', 'choices', 'timeAndDate', 'get_recipient_ashas', 'additionalPhoneNumbers', 'trailer_player', 'status')
	search_fields = ['show', 'choices', 'get_recipient_ashas', 'additionalPhoneNumbers']
	readonly_fields = ['author','updated_by']
	class Media:
		js = ("instantsearch.js",)

	actions = ['send_audio_trailer']

	def send_audio_trailer(self, request, queryset):
		n = queryset.count()
		
		for scheduledTrailer in queryset:
			if (scheduledTrailer.trailer):
				ashas = [ str(asha.phoneNumber) for asha in scheduledTrailer.recipientAshas.all() ]
				additionalPhoneNumbers = map(str,scheduledTrailer.additionalPhoneNumbers.split(","))
				if scheduledTrailer.choices == 'listeners only' and scheduledTrailer.show:
					listeners = [ str(listener.phoneNumber) for listener in scheduledTrailer.show.cohort.listeners.all() ]
					broadcaster = []
				elif scheduledTrailer.choices == 'broadcaster only' and scheduledTrailer.show:
					listeners = []
					broadcaster = [ str(scheduledTrailer.show.cohort.broadcaster.phoneNumber) ]
				elif scheduledTrailer.choices == 'broadcaster and listeners' and scheduledTrailer.show:
					broadcaster = [ str(scheduledTrailer.show.cohort.broadcaster.phoneNumber) ]
					listeners = [ str(listener.phoneNumber) for listener in scheduledTrailer.show.cohort.listeners.all() ]
				else:
					listeners = []
					broadcaster = []
				allPhonenumbers = [ashas,additionalPhoneNumbers,broadcaster,listeners]
				allPhonenumbers = list(set().union(*allPhonenumbers))
				date_str = timezone.localtime(scheduledTrailer.timeAndDate).strftime("%Y-%m-%d")
				time_str = timezone.localtime(scheduledTrailer.timeAndDate).strftime("%H:%M:%S")
				if scheduledTrailer.show:
					show_id = scheduledTrailer.show.showID
				else:
					show_id = None
				for phno in allPhonenumbers:
					if phno:
						print date_str
						print time_str
						print phno
						print show_id
						print scheduledTrailer.trailer.file.path
						value = esl.schedule_trailer(date_str, time_str, phno, show_id, scheduledTrailer.trailer.file.path)
				scheduledTrailer.status = 1
				super(queryset.model, scheduledTrailer).save()
				# scheduledTrailer.save()
		self.message_user(request, ("Successfully sent %d trailers.") % n)
	send_audio_trailer.short_description = "Schedule selected trailers"

	def get_actions(self, request):
		actions = super(SendAudioTrailerAdmin, self).get_actions(request)
		# print actions['delete_selected']
		if not request.user.groups.filter(name='Expert').exists():
			actions['delete_selected'][0].short_description = "Delete selected trailers"
		return actions

class TextMessageAdmin(admin.ModelAdmin):
	list_display = ('textMessage', 'additionalPhoneNumbers', 'get_recipient_ashas')
	search_fields = ['textMessage', 'additionalPhoneNumbers']
	readonly_fields = ['author','updated_by']
	actions = ['update_text_message_in_mongo']

	def update_text_message_in_mongo(self, request, queryset):
		n = queryset.count()
		currTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		for x in queryset:
			if (x.textMessage):
				ashas = [ str(asha.phoneNumber) for asha in x.recipientAshas.all() ]
				additionalPhoneNumbers = map(str,x.additionalPhoneNumbers.split(","))
				allPhonenumbers = [ashas,additionalPhoneNumbers]
				allPhonenumbers = list(set().union(*allPhonenumbers))
				allPhonenumbers = [ p for p in allPhonenumbers if p != "" ]
				mongo.insert_user_notifications(str(x.id), x.textMessage, allPhonenumbers, currTime)
		self.message_user(request, ("Successfully updated %d messages in MongoDB.") % n)
	update_text_message_in_mongo.short_description = "Update selected messages in MongoDB"

	class Media:
		js = ("instantsearch.js",)


admin.site.register(models.Asha, AshaAdmin)
admin.site.register(models.Cohort, CohortAdmin)
admin.site.register(models.Show, ShowAdmin)
admin.site.register(models.ShowRecording, ShowRecordingAdmin)
admin.site.register(models.Content, ContentAdmin)
admin.site.register(models.AudioFile, AudioFileAdmin)
admin.site.register(models.ContentCategory, ContentCategoryAdmin)
admin.site.register(models.ShowFeedback, ShowFeedbackAdmin)
admin.site.register(models.TextMessage, TextMessageAdmin)
admin.site.register(models.SendAudioTrailer, SendAudioTrailerAdmin)
