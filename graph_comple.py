import math
from kivy_garden.graph import Graph,MeshLinePlot,SmoothLinePlot,MeshStemPlot
graph=Graph(xmin = -6,xmax=6,ymax=36,padding=20,x_ticks_minor=2,x_grid_label=True,y_grid_label=True,x_ticks_major=1,y_ticks_major=4,y_ticks_minor=5,y_grid=True,x_grid=True)
#,precision='%.1f')
plot=MeshLinePlot(color=[0,1,0,1])
plot_x=MeshLinePlot(color=[1,1,1,1])
graph.add_plot(plot_x)
graph.add_plot(plot)
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
#from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
def rlround(x,n=2):
	if abs(int(x))>0:return round(x)
	i,y=0,x
	while int(y)==0:
		i+=1
		y*=10
	return round(x,i-2+n)
class graphclass(App):
	def build(self):
		upbox =BoxLayout(size_hint_y=None,height=60)
		box = BoxLayout(orientation='vertical')
		global txt
		txt = TextInput(text='x**2',multiline=False,size_hint_y=None,height=60,halign='center')
		txt.bind(on_text_validate=self.setplot)
		global txt_1
		txt_1=TextInput(text='-5',multiline=False,size_hint=(None,None),width=80,height=60,halign='center')
		txt_1.bind(on_text_validate=self.setplot)
		global txt_2
		txt_2=TextInput(text='5',multiline=False,size_hint=(None,None),height=60,width=80,halign='center')
		txt_2.bind(on_text_validate=self.setplot)
		upbox.add_widget(txt)
		upbox.add_widget(txt_1)
		upbox.add_widget(txt_2)
		box.add_widget(upbox)
		box.add_widget(graph)
		return box
	def setplot(self,*args):
		k=len(graph.plots)
		if k>2:
			for i in range(k-2):
				graph.remove_plot(graph.plots[-1])
			#graph._clear_buffer()
		if int(txt_1.text)>=int(txt_2.text):
			txt_1.text,txt_2.text=txt_2.text,txt_1.text
		x=[i*0.001 for i in range(int(txt_1.text)*1000,int(txt_2.text)*1000+1)]
		try:
			z=zip(x,map(lambda x:eval(txt.text),x))
			z=[(i,j) for i,j in z if j!=None]
		except:
			txt.text +=' **ERROR*func'
			return
		if len(z):
			try:
				y_min=min(x[1] for x in z)
			except TypeError:
				self.errorpop('Δόθηκε αρνητικό υπόριζο.Δεν ορίζεται δύναμη με αρνητική βάση και κλασματικό εκθέτη (δηλ. ρίζα με αρνητικό υπόριζο)')
				return
		else:
			txt.text ='Χωρίς Π.Ο'
			return
		x_min=min(x[0] for x in z)
		y_max=max(x[1] for x in z)
		x_max=max(x[0] for x in z)
		d=next((i,j) for i,j in z if j==y_min)
		f=next((i,j) for i,j in z if j==y_max)
		#txt.text+=' ({:.3f},{:.3f}) ({:.3f},{:.3f})'.format(*d,*f)
		d=rlround((y_max-y_min)/7)
		graph.ymin=rlround((2*y_min-d)/2)
		graph.ymax=graph.ymin +8*d
		graph.y_ticks_major=d
		m=d
		#txt.text=' y_min={:.0f},y_max={:.3f},ymin={}, ymay={},m={}'.format(y_min,y_max,graph.ymin,graph.ymax,m)
		graph.xmin=x_min
		graph.xmax=x_max
		r=filter(lambda x: abs(x[1])<.5e-2,z)
		list_yplots=[]
		ylist=[graph.ymin+.01*i*m for i in range(5) if graph.ymin+.01*i*m<0]
		xpnt=0
		while True:
			try:
				r1=next(r)
				if abs(r1[0]-xpnt)>0.02:
					list_yplots.append(MeshStemPlot(color=[1,.5,.5,.8]))
					graph.add_plot(list_yplots[-1])
					list_yplots[-1].points=list((r1[0],y) for y in ylist)
				#	txt.text+=' {:.4f} ,'.format(r1[1])
				xpnt=r1[0]
			except StopIteration:
				break
		plot_x.points=[(0.01*x,0) for x in range(100*int(txt_1.text),101*int(txt_2.text))]
		plot.points=z
		#txt.text+=str(graph.plots[1])
	def errorpop(self,txt):
		layout= BoxLayout(orientation='vertical',padding=10,pos_hint={'y':.1})
		lbl=Label(text=txt,pos_hint={'y':.29})
		lbl.bind(width=lambda *x:lbl.setter('text_size')(lbl,(lbl.width,None)),texture_size=lambda *x: lbl.setter('height')(lbl,lbl.texture_size[1]))
		layout.add_widget(lbl)
		popup =Popup(title='Λάθος στο όρισμα της συνάρτησης ',content=layout,size_hint=(.8,.3))
		popup.open()
graphclass().run()
