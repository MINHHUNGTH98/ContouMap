import numpy as np
from scipy.spatial.qhull import Delaunay
from tkinter import *
import PIL
from PIL import ImageTk, Image
import pandas as pd

# tạo nền canvas và chèn ảnh map
tk = Tk()
tk.title("Bản đồ đồng mức cho chỉ số tín hiệu thu WIFI ")
image = Image.open("D:\Python\CheckCode\map1.jpg")
w = image.size[0]
h = image.size[1]
cas = Canvas(tk, width = w , height = h )
photo = ImageTk.PhotoImage(image)
item5 = cas.create_image(0, 0, anchor=NW, image=photo)

# doc file data_point_0.csv
contour_df0 = pd.read_csv('./data_point_0.csv')
lat_t0 = contour_df0['lat'].values
lon_t0 = contour_df0['lon'].values
lat0 = lat_t0/1000000
lon0 = lon_t0/1000000
z0 = contour_df0['rssi'].values

# doc file data_point_1.csv
contour_df1 = pd.read_csv('./data_point_1.csv')
lat_t1 = contour_df1['lat'].values
lon_t1 = contour_df1['lon'].values
lat1 = lat_t1/1000000
lon1 = lon_t1/1000000
z1 = contour_df1['rssi'].values

# chuyen he tọa do cua ban do sang canvas:

   # Ham tinh khoang cach giua 2 diem biet toa do:
def distanceBetween2Points(la1, lo1, la2, lo2):
	dLat = (la2 - la1) * (np.pi / 180)
	dLon = (lo2 - lo1) * (np.pi / 180)
	la1ToRad = (la1) * (np.pi / 180)
	la2ToRad = (la2) * (np.pi / 180)
	a = np.sin(dLat / 2) * np.sin(dLat / 2) + np.cos(la1ToRad) * np.cos(la2ToRad) * np.sin(dLon / 2) * np.sin(dLon / 2)
	c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
	R = 6371000                                     #  R la bk trai dat
	d = R * c
	return d
   # Chuyen tu bản do sang canvas dau vao kinh do, vi do; dau ra toa do x,y trn nen canvas
def chuyenHe(la2, lo2):
	# vi do, kinh do diem tranmister 
	la1 = 21.005719
	lo1 = 105.842480
	
	d1 = distanceBetween2Points(la2, lo2, la2, lo1)
	d2 = distanceBetween2Points(la2, lo2, la1, lo2)
	d1_pixel = (d1*160)/30
	d2_pixel = (d2*160)/30

	if( la2 <= la1 and lo2 >= lo1):
		x = w/2 + d1_pixel
		y = h/2 + d2_pixel
	if( la2 <= la1 and lo2 <= lo1):
		x = w/2 - d1_pixel
		y = h/2 + d2_pixel
	if( la2 >= la1 and lo2 >= lo1):
		x = w/2 + d1_pixel
		y = h/2 - d2_pixel
	if( la2 >= la1 and lo2 <= lo1):
		x = w/2 - d1_pixel
		y = h/2 - d2_pixel
	return x,y

# Ham ve cac duong contour
def drawContour(tg,value,color):
	if(tg[0][2] == value):   # tg[0][2] là gia tri z cua dinh dau tien tam giac
		M = tg[0][0:2]
	else:
		rate = (value - tg[1][2]) * 1.0 / (tg[0][2] - value)
		if(rate>=0):
			M = [tg[1][0] * 1.0 / (rate + 1) + tg[0][0] * rate / (rate + 1),tg[1][1] * 1 / (rate + 1) + tg[0][1] * rate / (rate + 1)]
		else:
			M = None

	if(tg[1][2] == value):
		N = tg[1][0:2]
	else:
		rate = (value - tg[2][2]) * 1.0 / (tg[1][2] - value)
		if(rate>=0):
			N = [tg[2][0] * 1.0 / (rate + 1) + tg[1][0] * rate / (rate + 1),tg[2][1] * 1 / (rate + 1) + tg[1][1] * rate / (rate + 1)]
		else:
			N = None

	if(tg[2][2] == value):
		P = tg[2][0:2]
	else:
		rate = (value - tg[0][2]) * 1.0 / (tg[2][2] - value)
		if(rate>=0):
			P = [tg[0][0] * 1.0 / (rate + 1) + tg[2][0] * rate / (rate + 1),tg[0][1] * 1 / (rate + 1) + tg[2][1] * rate / (rate + 1)]
		else:
			P = None

	if( M!=None and N!=None):
		cas.create_line(M[0],M[1], N[0], N[1], fill = color, width = 1.5)
	if( M!=None and P!=None):
		cas.create_line(M[0],M[1], P[0], P[1], fill = color, width = 1.5)
	if( P!=None and N!=None):
		cas.create_line(P[0],P[1], N[0], N[1], fill = color, width = 1.5)

# Ham ve tam giac
def drawTg(tg):
	cas.create_line(tg[0][0],tg[0][1],tg[1][0],tg[1][1])
	cas.create_line(tg[1][0],tg[1][1],tg[2][0],tg[2][1])
	cas.create_line(tg[2][0],tg[2][1],tg[0][0],tg[0][1])

# Ham ve cac diem:
def drawPoint(tg):
	cas.create_oval(tg[0][0]-2,tg[0][1]-2,tg[0][0]+2,tg[0][1]+2, fill="green")
	cas.create_oval(tg[1][0]-2,tg[1][1]-2,tg[1][0]+2,tg[1][1]+2, fill="green")
	cas.create_oval(tg[2][0]-2,tg[2][1]-2,tg[2][0]+2,tg[2][1]+2, fill="green")

cas.create_rectangle(w-163, h-6, w-3, h-3, outline="#fb0", fill="#fb0")   # tìm ty le 30m = 160 pixel

x0 = []
y0 = []
for i in range(len(lat0)):
	x0.append(chuyenHe(lat0[i],lon0[i])[0])
	y0.append(chuyenHe(lat0[i],lon0[i])[1])

data0 = np.array([x0,y0,z0]).transpose()
data00 = data0[:,:2]
tri0 = Delaunay(data00)
list_tg0 = data0[tri0.simplices]


x1 = []
y1 = []
for i in range(len(lat1)):
	x1.append(chuyenHe(lat1[i],lon1[i])[0])
	y1.append(chuyenHe(lat1[i],lon1[i])[1])

data1 = np.array([x1,y1,z1]).transpose()
data11= data1[:,:2]
tri1 = Delaunay(data11)
list_tg1 = data1[tri1.simplices]

# Ve contour:
for i in range (0,list_tg0.shape[0]):
	drawContour(list_tg0[i],-30,"#99cc00")
	drawContour(list_tg0[i],-40,"#33ffff")
	drawContour(list_tg0[i],-50,"#ffff66")
	drawContour(list_tg0[i],-60,"#663300")
	drawContour(list_tg0[i],-70,"#ff9933")
	drawContour(list_tg0[i],-80,"#3300bb")
	drawContour(list_tg0[i],-90,"#cc0099")
	
for i in range (0,list_tg1.shape[0]):
	drawContour(list_tg1[i],-30,"#99cc00")
	drawContour(list_tg1[i],-40,"#33ffff")
	drawContour(list_tg1[i],-50,"#ffff66")
	drawContour(list_tg1[i],-60,"#663300")
	drawContour(list_tg1[i],-70,"#ff9933")
	drawContour(list_tg1[i],-80,"#3300bb")
	drawContour(list_tg1[i],-90,"#cc0099")

cas.create_rectangle(w-220, 2, w, 130, outline="#000033", fill="white")

cas.create_line(w-210, 12, w-110, 12, fill = "#99cc00", width = 1.5)
cas.create_text(w-50, 12, font="VNI-Dom 8", text="RSSI = -30")

cas.create_line(w-210, 27, w-110, 27, fill = "#33ffff", width = 1.5)
cas.create_text(w-50, 27, font="VNI-Dom 8", text="RSSI = -40")

cas.create_line(w-210, 42, w-110, 42, fill = "#ffff66", width = 1.5)
cas.create_text(w-50, 42, font="VNI-Dom 8", text="RSSI = -50")

cas.create_line(w-210, 57, w-110, 57, fill = "#663300", width = 1.5)
cas.create_text(w-50, 57, font="VNI-Dom 8", text="RSSI = -60")

cas.create_line(w-210, 72, w-110, 72, fill = "#ff9933", width = 1.5)
cas.create_text(w-50, 72, font="VNI-Dom 8", text="RSSI = -70")

cas.create_line(w-210, 87, w-110, 87, fill = "#3300bb", width = 1.5)
cas.create_text(w-50, 87, font="VNI-Dom 8", text="RSSI = -80")

cas.create_line(w-210, 102, w-110, 102, fill = "#cc0099", width = 1.5)
cas.create_text(w-50, 102, font="VNI-Dom 8", text="RSSI = -90")

# cas.create_line(w-210, 117, w-110, 117, fill = "#db7", width = 1.5)
# cas.create_text(w-50, 117, font="VNI-Dom 8", text="RSSI = -75")


cas.pack(side = TOP, expand=True, fill=BOTH)
tk.mainloop()


# lat : vi do(y), lon : kinh do(x)
