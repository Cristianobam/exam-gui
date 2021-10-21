import vedo
import numpy as np

from util import *

angle = 0
idx = 50
dataRecord = {'0':{'date':'17 Jan 21', 'mesh':'data/afinese_1.ply'},
              '1':{'date':'18 Jul 21', 'mesh':'data/afinese_2.ply'},
              '2':{'date':'19 Ago 21', 'mesh':'data/afinese_3.ply'},
              '3':{'date':'20 Set 21', 'mesh':'data/afinese_4.ply'}}
                         
beforeIdx = list(dataRecord.keys())
afterIdx = list(dataRecord.keys())
plt = vedo.Plotter(bg='#E4E9E9', sharecam=False, size='fullscreen')  

def getSlices(vmesh, num:int=100):
    mesh = vedo.vedo2trimesh(vmesh)
    bounds = mesh.bounds
    dx, dy, dz = bounds[1]-bounds[0]
    heights = np.linspace(0, dy, num)
    mslices = mesh.section_multiplane([0,bounds[0][1],0],[0,1,0],heights=heights)
    return mslices

def getContour(mslices, dx=0, dy=0, dz=0, color='red', idx:int=50):
    contour = vedo.trimesh2vedo(mslices[idx].to_3D()).actors
    contour = [actor.c(color).lw(5).shift(dx,dy,dz) for actor in contour]
    return contour

def getSlice2D(mslices, x=0, y=0, z=0, color='green', idx:int=50):
    slice2D = vedo.trimesh2vedo(mslices[idx]).actors
    slice2D = [actor.x(x).y(y).z(z).c(color).rotateZ(82, locally=True).scale(s=(3,3,3)) for actor in slice2D]
    return slice2D

def getLength(mslice, scale:float=11.0):
    size = len(mslice.entities)
    print(size)
    if size <= 1:
        return mslice.length/scale
    if size == 2:
        return (mslice.length/scale)/2        
    
    lengthTemp = list()
    for i in range(size):
        idxs = list(range(size))
        idxs.remove(i)
        msliceTemp = mslice.copy()
        msliceTemp.remove_entities(idxs)
        lengthTemp.append(msliceTemp.length/scale) 
    if size == 3: return np.sort(lengthTemp)[-1]
    elif size >= 4: return np.sort(lengthTemp)[-2:].sum()

for key in dataRecord.keys():
    dataRecord[key]['data'] = {}    
    dataRecord[key]['data']['mesh'] = vedo.Mesh(dataRecord[key]['mesh']).c('#EFF0F1').alpha(1)  
    dataRecord[key]['data']['mslice'] = getSlices(dataRecord[key]['data']['mesh'])
    
beforeIdx = rotate(beforeIdx, -1)
afterIdx = rotate(afterIdx, 0)
vmesh1 = dataRecord[beforeIdx[0]]['data']['mesh'].clone() # Antes
vmesh2 = dataRecord[afterIdx[0]]['data']['mesh'].clone() # Depois
plt.show((vmesh1, vmesh2), resetcam=True, interactive=False, zoom=.75, title='AfinTech Scanners 3D', mode=9)

textDateBefore = vedo.Text2D(dataRecord[beforeIdx[0]]['date'], font='Comae', pos=(0.375,0.9), justify='center')
textDateAfter = vedo.Text2D(dataRecord[afterIdx[0]]['date'], font='Comae', pos=(0.125,0.9), justify='center')
mslices1 = dataRecord[beforeIdx[0]]['data']['mslice']
mslices2 = dataRecord[afterIdx[0]]['data']['mslice']
contour1 = getContour(mslices=mslices1, dx=-560, color='grey', idx=idx)
contour2 = getContour(mslices=mslices2, dx=-1700, color='red', idx=idx)
slice2D1 = getSlice2D(mslices=mslices1, x=1000, color='grey', idx=idx)
slice2D2 = getSlice2D(mslices=mslices2, x=1000, color='red', idx=idx)
vmesh1.x(-560)
vmesh2.x(-1700)

plt.add([textDateBefore, textDateAfter]+contour1+contour2+slice2D1+slice2D2)
textBefore, textAfter, textRatio, textTypeRatio = None, None, None, None

def setLengthText():
    global textBefore, textAfter, textRatio, ratio, textTypeRatio
    txt1 = getLength(dataRecord[afterIdx[0]]['data']['mslice'][idx])    
    txt2 = getLength(dataRecord[beforeIdx[0]]['data']['mslice'][idx])    
    ratio = (txt2/txt1 - 1)*100 if txt1 != 0 else 0.0

    textBefore = vedo.Text2D(f'{txt1:.0f} cm', font='Comae', pos=(0.65,0.2), justify='center')
    textAfter = vedo.Text2D(f'{txt2:.0f} cm', font='Comae', pos=(0.75,0.2), justify='center')
    textRatio = vedo.Text2D(f'{ratio:.1f} %', font='Comae', pos=(0.85,0.2), justify='center').c('lime' if ratio <= 0 else 'red')
    textTypeRatio = vedo.Text2D('Perda' if ratio <= 0 else 'Ganho', font='Comae', pos=(0.85,0.15), justify='center')

setLengthText()
caption1 = vedo.Circle().clone2D(pos=[0.675, 0.17], coordsys=3, c='red', alpha=.65, scale=0.01)
caption2 = vedo.Circle().clone2D(pos=[0.78, 0.17], coordsys=3, c='grey', alpha=.65, scale=0.01)
plt.add((textBefore, textAfter, textRatio, caption1, caption2,
        vedo.Text2D('Antes', font='Comae', pos=(0.65,0.15), justify='center'), 
        vedo.Text2D('Depois', font='Comae', pos=(0.75,0.15), justify='center'), 
        textTypeRatio))

def rotateMeshesBefore(dtheta):
    for actor1 in contour1:
        actor1.rotateY(dtheta, locally=True)
    vmesh1.rotateY(dtheta, locally=True)

def rotateMeshesAfter(dtheta):
    for actor2 in contour2:
        actor2.rotateY(dtheta, locally=True)
    vmesh2.rotateY(dtheta, locally=True)
    
def addAngle(event):
    global angle
    angle = angle + .5 if angle <= 359 else 0
    rotateMeshesBefore(dtheta=.5)
    rotateMeshesAfter(dtheta=.5)
    plt.render()

def slider(widget, event):
    global idx, contour1, contour2, slice2D1, slice2D2, textBefore, textAfter, textRatio, textTypeRatio
    idx = int(widget.GetRepresentation().GetValue())    
    plt.remove(contour1+contour2+slice2D1+slice2D2+[textBefore,textAfter,textRatio,textTypeRatio])
    setLengthText()
    updateMeshBefore()    
    updateMeshAfter()        
    

def keyfunc(evt):
    if evt.keyPressed=='q':
        plt.close()  

def updateMeshBefore():
    global vmesh1, mslice1, contour1, slice2D1, slice2D2, textDateBefore, textBefore, textAfter, textRatio, textTypeRatio
    plt.remove([vmesh1, textDateBefore, textBefore, textAfter, textRatio, textTypeRatio]+contour1+slice2D1+slice2D2)
    textDateBefore = vedo.Text2D(dataRecord[beforeIdx[0]]['date'], font='Comae', pos=(0.375,0.9), justify='center')
    vmesh1 = dataRecord[beforeIdx[0]]['data']['mesh'].clone()
    mslices1 = dataRecord[beforeIdx[0]]['data']['mslice']
    contour1 = getContour(mslices=mslices1, dx=-560, color='grey', idx=idx)
    slice2D1 = getSlice2D(mslices=mslices1, x=1000, color='grey', idx=idx)
    vmesh1.x(-560)
    rotateMeshesBefore(dtheta=angle)
    setLengthText()
    plt.add([vmesh1, textDateBefore, textBefore, textAfter, textRatio, textTypeRatio]+contour1+slice2D1+slice2D2)
    
def btnPrevBefore():
    global beforeIdx
    beforeIdx = rotate(beforeIdx, 1)
    updateMeshBefore()
    
def btnNextBefore():
    global beforeIdx
    beforeIdx = rotate(beforeIdx, -1)
    updateMeshBefore()
    
def updateMeshAfter():
    global vmesh2, mslice2, contour2, slice2D1, slice2D2, textDateAfter, textBefore, textAfter, textRatio, textTypeRatio
    plt.remove([vmesh2, textDateAfter, textBefore, textAfter, textRatio, textTypeRatio]+contour2+slice2D2+slice2D1)
    textDateAfter = vedo.Text2D(dataRecord[afterIdx[0]]['date'], font='Comae', pos=(0.125,0.9), justify='center')
    vmesh2 = dataRecord[afterIdx[0]]['data']['mesh'].clone()
    mslices2 = dataRecord[afterIdx[0]]['data']['mslice']
    contour2 = getContour(mslices=mslices2, dx=-1700, color='red', idx=idx)
    slice2D2 = getSlice2D(mslices=mslices2, x=1000, color='red', idx=idx)
    vmesh2.x(-1700)
    rotateMeshesAfter(dtheta=angle)
    plt.add([vmesh2, textDateAfter, textBefore, textAfter, textRatio, textTypeRatio]+contour2+slice2D1+slice2D2)
    
def btnPrevAfter():
    global afterIdx
    afterIdx = rotate(afterIdx, 1)
    updateMeshAfter()
    
def btnNextAfter():
    global afterIdx
    afterIdx = rotate(afterIdx, -1)
    updateMeshAfter()

plt.addButton(btnPrevAfter, pos=(0.05, 0.90), states=["<"], c=["w"], bc=['none'], font="courier", size=22)
plt.addButton(btnNextAfter, pos=(0.20, 0.90), states=[">"], c=["w"], bc=['none'], font="courier", size=22)
plt.addButton(btnPrevBefore, pos=(0.30, 0.90), states=["<"], c=["w"], bc=['none'], font="courier", size=22)
plt.addButton(btnNextBefore, pos=(0.45, 0.90), states=[">"], c=["w"], bc=['none'], font="courier", size=22)

plt.addSlider2D(slider, 0, 100, value=50, pos=([0.25,-0.15], [0.25,1.15]), showValue=False)
plt.addCallback('KeyPress', keyfunc)
plt.addCallback("timer", addAngle)
plt.timerCallback("create", dt=1)

vedo.interactive()