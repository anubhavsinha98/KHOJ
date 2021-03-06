from django.shortcuts import render
from core import encode_faces
from django.views.decorators.csrf import csrf_protect
from core import encode_faces
from .models import *
from khoj_api import settings
import os

def get_upload_lost_person_image_form(request):
	return render(request, 'upload_lost_person_image_form.html')


def upload_lost_person_image_form(request):
	data = {
		'name' : request.POST['name'],
		'gender' : request.POST['gender'],
		'addhar_card_number' : request.POST['aadhar_num']
	}

	missing_person = MissingPerson(**data)
	missing_person.save()

	person = MissingPerson.objects.filter(addhar_card_number=request.POST['aadhar_num'])[0]
	images =request.FILES.getlist('images')
	
	try:
		os.mkdir("media/images/"+data["addhar_card_number"])
	except FileExistsError:
		pass

	# print(images)
	files=[]
	file_num=0
	for image in images:
		extension=str(image).split(".")[-1]
		file_not_created=True
		while file_not_created:
			try:
				file_name = str(file_num)+"."+extension
				file_loc = "media/images/"+data["addhar_card_number"]+"/"+file_name
				with open(file_loc, 'wb+') as destination:
					destination.write(image.read())
				file_not_created=False
				files.append(file_name)
				file_num+=1
			except FileExistsError:
				file_num+=1

	args= {'dataset' : "media/images/"+data["addhar_card_number"]}
	encoded_faces=encode_faces.update_pickle(args)


	for pickles in encoded_faces:
		file_num=0
		for pickle in encoded_faces[pickles]:
			if pickle:
				image_data = {
					'addhar_card_number': person,
					'image': files[file_num],
					'pickel': pickle
				}
				new_person = MissingPersonImages(**image_data)
				new_person.save()
				# print(new_person.pickel)
			file_num+=1


	return render(request, 'base.html')
