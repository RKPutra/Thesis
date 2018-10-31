from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from tes.models import Fknn
import csv
import io
import os

nama = ''
password = ''

def index(request):
    return render(request, 'index/index.html')

def login(request):
	return render(request, 'login.html')

def cekLogin(request):
	admin_name = "admin"
	admin_pass = "admin"
	if request.method == "POST":
		if 'nama' in request.POST:
			nama = request.POST['nama']
		if 'password' in request.POST:
			password = request.POST['password']
		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		with open(os.path.join(BASE_DIR, 'tes\\static\\data\\dokter.csv'), "rt") as csvfile:
		    lines = csv.reader(csvfile)
		    dataset = list(lines)
		    statusAdmin = False
		    statusDokter = False
		    if nama == admin_name and password == admin_pass:
		    	statusAdmin =True
		    	row = [nama]
		    	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		    	with open(os.path.join(BASE_DIR, 'tes\\static\\data\\session.csv'), "w") as csvfile:
				    writer = csv.writer(csvfile)
				    writer.writerow(row)	
		    	csvfile.close()
		    	return redirect('tambahDokter')
		    else:
			    for i in range(len(dataset)):
			    	if dataset[i][0] == nama and dataset[i][2] == password:
			    		statusDokter = True
			    		row = [nama]
			    		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
			    		with open(os.path.join(BASE_DIR, 'tes\\static\\data\\session.csv'), "w") as csvfile:
						    writer = csv.writer(csvfile)
						    writer.writerow(row)
			    		csvfile.close()
			    		return redirect('diagnosis')
		    if statusDokter == False and statusDokter == False:
		    	return render(request, 'alert_login.html')

def logout(request):
	row = ["_"]
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	with open(os.path.join(BASE_DIR, 'tes\\static\\data\\session.csv'), "w") as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(row)

	csvfile.close()
	return redirect('login')

def tambahDokter(request):
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	with open(os.path.join(BASE_DIR, 'tes\\static\\data\\session.csv'), "rt") as csvfile:
		lines = csv.reader(csvfile)
		dataset = list(lines)
		for i in range(len(dataset)):
			if dataset[i][0] != "_":
				if dataset[i][0] == "admin":
					return render(request, 'index/tambah_dokter.html')
				else:
					return render(request, 'alert_dokter.html')
			else:
				return render(request, 'alert_masuk.html')

def prosesTambahDokter(request):
	if request.method == "POST":
		if 'nama' in request.POST:
			nama = request.POST['nama']
		if 'password' in request.POST:
			password = request.POST['password']
		if 'email' in request.POST:
			email = request.POST['email']
		row = [nama, email, password]
		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		with open(os.path.join(BASE_DIR, 'tes\\static\\data\\dokter.csv'), "a") as csvfile:
		    writer = csv.writer(csvfile)
		    writer.writerow(row)

		csvfile.close()
		
	return render(request, 'alert_tambah.html')

def training(request):
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	with open(os.path.join(BASE_DIR, 'tes\\static\\data\\session.csv'), "rt") as csvfile:
		lines = csv.reader(csvfile)
		dataset = list(lines)
		for i in range(len(dataset)):
			if dataset[i][0] != "_":
				if dataset[i][0] == "admin":
					return render(request, 'index/training_data.html')
				else:
					return render(request, 'alert_dokter.html')
			else:
				return render(request, 'alert_masuk.html')

def gantiParameter(request):
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	with open(os.path.join(BASE_DIR, 'tes\\static\\data\\session.csv'), "rt") as csvfile:
		lines = csv.reader(csvfile)
		dataset = list(lines)
		for i in range(len(dataset)):
			if dataset[i][0] != "_":
				if dataset[i][0] == "admin":
					return render(request, 'index/ganti_parameter.html')
				else:
					return render(request, 'alert_dokter.html')
			else:
				return render(request, 'alert_masuk.html')

def prosesGantiParameter(request):
	if request.method == "POST":
		if 'k' in request.POST:
			k = request.POST['k']
		if 'm' in request.POST:
			m = request.POST['m']
		row = [k, m]
		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		with open(os.path.join(BASE_DIR, 'tes\\static\\data\\parameter.csv'), "w") as csvfile:
		    writer = csv.writer(csvfile)
		    writer.writerow(row)

		csvfile.close()
		
	return render(request, 'alert_ganti.html')

def diagnosis(request):
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	with open(os.path.join(BASE_DIR, 'tes\\static\\data\\session.csv'), "rt") as csvfile:
		lines = csv.reader(csvfile)
		dataset = list(lines)
		for i in range(len(dataset)):
			if dataset[i][0] != "_":
				if dataset[i][0] != "admin":
					return render(request, 'index/diagnosis.html')
				else:
					return render(request, 'alert_admin.html')
			else:
				return render(request, 'alert_masuk.html')

def single(request):
    return render(request, 'index/single.html')

def hasilTraining(request):
	if request.method == "POST":
		label = []
		if 'dengue' in request.POST:
			dengue = request.POST['dengue']
			label.append(dengue)
		if 'typoid' in request.POST:
			typoid = request.POST['typoid']
			label.append(typoid)
		if 'gea' in request.POST:
			gea = request.POST['gea']
			label.append(gea)
		if 'diare' in request.POST:
			diare = request.POST['diare']
			label.append(diare)
		if 'bronkitis' in request.POST:
			bronkitis = request.POST['bronkitis']
			label.append(bronkitis)
		if 'farangitis' in request.POST:
			farangitis = request.POST['farangitis']
			label.append(farangitis)
		if 'pnemonia' in request.POST:
			pnemonia = request.POST['pnemonia']
			label.append(pnemonia)
		if 'campak' in request.POST:
			campak = request.POST['campak']
			label.append(campak)

		if 'split' in request.POST:
			split = request.POST['split']
		if 'k' in request.POST:
			k = request.POST['k']
		if 'm' in request.POST:
			m = request.POST['m']

		f = Fknn
			
		args, tr, te = f.main(label, split, k, m)
		
		return render(request, 'hasil_training.html', args)
	else:
		return render(request, 'alert_training.html')

def hasilDiagnosis(request):
	if request.method == "POST":
		label = []
		if 'dengue' in request.POST:
			dengue = request.POST['dengue']
			label.append(dengue)
		if 'typoid' in request.POST:
			typoid = request.POST['typoid']
			label.append(typoid)
		if 'gea' in request.POST:
			gea = request.POST['gea']
			label.append(gea)
		if 'diare' in request.POST:
			diare = request.POST['diare']
			label.append(diare)
		if 'bronkitis' in request.POST:
			bronkitis = request.POST['bronkitis']
			label.append(bronkitis)
		if 'farangitis' in request.POST:
			farangitis = request.POST['farangitis']
			label.append(farangitis)
		if 'pnemonia' in request.POST:
			pnemonia = request.POST['pnemonia']
			label.append(pnemonia)
		if 'campak' in request.POST:
			campak = request.POST['campak']
			label.append(campak)

		if 'nadi' in request.POST:
			nadi = request.POST['nadi']
		if 'suhu' in request.POST:
			suhu = request.POST['suhu']
		if 'nafas' in request.POST:
			nafas = request.POST['nafas']
		if 'nyeri' in request.POST:
			nyeri = request.POST['nyeri']
		if 'berat' in request.POST:
			berat = request.POST['berat']
		if 'tinggi' in request.POST:
			tinggi = request.POST['tinggi']
			
		if 'a' in request.POST:
			num = request.POST['a']
			
		s = ""
		
		te = []
		for i in range(int(num)):
			x = 'anamnesis' + str((i+1))
			if x in request.POST:
				if i != int(num)-1:
					s += request.POST[x] + "_"
				else:
					s += request.POST[x]
		te.append([(nadi+'_'+suhu+'_'+nafas+'_'+nyeri+'_'+berat+'_'+tinggi+'_'+s)])

		f = Fknn
		args = f.main2(te, label)
		
		return render(request, 'hasil_diagnosis.html', args)
	else:
		return render(request, 'alert_diagnosis.html')

def hasil(request):
	if request.method == "POST":
		if request.POST['hidden'] == "file":
			if 'data_training' in request.FILES:
				file = request.FILES['data_training']
				csv_file = request.FILES['data_training']
				reader = io.StringIO(csv_file.read().decode('utf-8'))
			label = []
			if 'dengue' in request.POST:
			    dengue = request.POST['dengue']
			    label.append(dengue)
			if 'typoid' in request.POST:
			    typoid = request.POST['typoid']
			    label.append(typoid)
			if 'gea' in request.POST:
				gea = request.POST['gea']
				label.append(gea)
			if 'diare' in request.POST:
			    diare = request.POST['diare']
			    label.append(diare)
			if 'bronkitis' in request.POST:
			    bronkitis = request.POST['bronkitis']
			    label.append(bronkitis)
			if 'farangitis' in request.POST:
			    farangitis = request.POST['farangitis']
			    label.append(farangitis)
			if 'pnemonia' in request.POST:
			    pnemonia = request.POST['pnemonia']
			    label.append(pnemonia)
			if 'campak' in request.POST:
			    campak = request.POST['campak']
			    label.append(campak)

			if 'split' in request.POST:
				split = request.POST['split']
			if 'k' in request.POST:
				k = request.POST['k']
			if 'm' in request.POST:
				m = request.POST['m']

			f = Fknn
			
			args, tr, te = f.main(list(reader), label, split, k, m)
		else:
			if 'data_training' in request.FILES:
				csv_file = request.FILES['data_training']
				reader = io.StringIO(csv_file.read().decode('utf-8'))
			label = []
			if 'dengue' in request.POST:
			    dengue = request.POST['dengue']
			    label.append(dengue)
			if 'typoid' in request.POST:
			    typoid = request.POST['typoid']
			    label.append(typoid)
			if 'gea' in request.POST:
				gea = request.POST['gea']
				label.append(gea)
			if 'diare' in request.POST:
			    diare = request.POST['diare']
			    label.append(diare)
			if 'bronkitis' in request.POST:
			    bronkitis = request.POST['bronkitis']
			    label.append(bronkitis)
			if 'farangitis' in request.POST:
			    farangitis = request.POST['farangitis']
			    label.append(farangitis)
			if 'pnemonia' in request.POST:
			    pnemonia = request.POST['pnemonia']
			    label.append(pnemonia)
			if 'campak' in request.POST:
			    campak = request.POST['campak']
			    label.append(campak)

			if 'split' in request.POST:
				split = request.POST['split']
			if 'k' in request.POST:
				k = request.POST['k']
				k2 = request.POST['k']
			if 'm' in request.POST:
				m = request.POST['m']

			if 'nadi' in request.POST:
				nadi = request.POST['nadi']
			if 'suhu' in request.POST:
				suhu = request.POST['suhu']
			if 'nafas' in request.POST:
				nafas = request.POST['nafas']
			if 'nyeri' in request.POST:
				nyeri = request.POST['nyeri']
			if 'berat' in request.POST:
				berat = request.POST['berat']
			if 'tinggi' in request.POST:
				tinggi = request.POST['tinggi']
			
			if 'a' in request.POST:
				num = request.POST['a']
			
			s = ""
			
			te = []
			for i in range(int(num)):
				x = 'anamnesis' + str((i+1))
				if x in request.POST:
					if i != int(num)-1:
						s += request.POST[x] + "_"
					else:
						s += request.POST[x]
			te.append([(nadi+'_'+suhu+'_'+nafas+'_'+nyeri+'_'+berat+'_'+tinggi+'_'+s)])
			if 'data_training' in request.FILES:
				csv_file2 = request.FILES['data_training']
				reader2 = io.StringIO(csv_file2.read().decode('utf-8'))
			f = Fknn
			f2 = Fknn
			args, tr, tes = f2.main(list(reader), label, 80, k2, m)
			for i in range(len(tes)):
				tr.append(tes[i])

			hasil = f.main2(tr, te, label, k, m)
			args.update(hasil)
			
		return render(request, 'hasil.html', args)
	else:
		return render(request, 'alert.html')