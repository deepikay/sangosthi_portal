import os
from django.core.exceptions import ValidationError

def validate_audiofile_extension(value):
	ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
	valid_extensions = ['.wav']
	if not ext.lower() in valid_extensions:
		raise ValidationError(u'Unsupported file extension. Please upload .wav file.')

def validate_phonenumbers_list(value):
	phoneNumbers = value.split(",")
	for phoneNumber in phoneNumbers:
		if len(phoneNumber)!=10:
			raise ValidationError(u'One of the phone numbers mentioned is not 10 digits long: ' + phoneNumber + ' Please do not use any spaces in this field.')

def validate_trailer_presence(value):
	if not value.trailer:
		raise ValidationError(u'The selected show does not have a trailer file')