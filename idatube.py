from flask import Flask,render_template,flash,url_for,redirect,request
from pydub import AudioSegment
import pafy,os
import youtube_dl


   
def audio(video):
	audio = video.getbestaudio()
	path="static/audio/"+video.title+".m4a"
	audio.download(filepath=path,quiet=True, callback=mycb)
	
def convertirAMp3(path):
	if(path[-3:]=="m4a"):
		
		try:
			wav_audio = AudioSegment.from_file(path, format="m4a")
		except:
			wav_audio = AudioSegment.from_file(path)	
		wav_audio.export(path[:-3]+"mp3", format="mp3")
		os.remove(path)
		return("Convertido")
	else:
		return("No se puede convertir")




def mycb(total, recvd, ratio, rate, eta):
    porcentaje=int((recvd/total)* 100)
    os.system ("cls")
    print("\t Descargando\n ",porcentaje,"%")


app = Flask(__name__)
app.secret_key='mysecretkey'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/descargar', methods=['POST'])
def descargar():
	if request.method=='POST':
		enlace=request.form['enlace']
		formato=request.form['formato']
		v = pafy.new(enlace)
		if formato=="mp4":
			s = v.getbest()
			filename = s.download(filepath=("/static/video/"+v.title+".mp4"),quiet=True, callback=mycb)
		if formato=="m4a":
			audio(v)
		flash("Descarga exitosa de"+ v.title)
	return redirect(url_for('index'))

@app.route('/listarCanciones')
def listarCanciones():
	audios= os.listdir('static/audio')
	return render_template('listarCanciones.html',audios=audios)

@app.route('/listarVideos')
def listarVideos():
	contenido= os.listdir('static/video')
	videos = []
	for fichero in contenido:
	    if os.path.isfile(os.path.join( 'static/video',fichero)) and fichero.endswith('.mp4'):
	        videos.append(fichero)
	return render_template('listarVideos.html',videos=videos)

@app.route('/convertirAudio/<string:cancion>')
def convertirAudio(cancion):
	path="static/audio/"+ cancion
	flash(cancion+" "+convertirAMp3(path))
	return redirect(url_for('listarCanciones'))






if __name__ == '__main__':
    app.run(debug=True,port=2000)
