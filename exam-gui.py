#%%
import vedo
import numpy as np
import json
from itertools import cycle
#%%
angle = 0
idx = 50
dataRecord = {'0':{'date':'20 Jan 21', 'mesh':'data/afinese_antes.ply'},
              '1':{'date':'20 Jan 21', 'mesh':'data/afinese_depois.ply'},
              '2':{'date':'20 Jan 21', 'mesh':'data/afinese_antes.ply'},
              '3':{'date':'20 Jan 21', 'mesh':'data/afinese_depois.ply'}}

beforeIdx = list(dataRecord.keys())
afterIdx = list(dataRecord.keys())[::-1]
plt = vedo.Plotter(bg='k', sharecam=False, size='fullscreen')

#%%
def rotate(l, n):
    return l[-n:] + l[:-n]

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
    slice2D = [actor.x(x).y(y).z(z).c(color).rotateZ(90, locally=True) for actor in slice2D]
    return slice2D

def getLength(mslice, scale:float=11.5):
    size = len(mslice.entities)
    if size <= 2:
        return mslice.length/scale
    
    lengthTemp = list()
    for i in range(size):
        idxs = list(range(size))
        idxs.remove(i)
        msliceTemp = mslice.copy()
        msliceTemp.remove_entities(idxs)
        lengthTemp.append(msliceTemp.length/scale) 
    if size == 3: return np.sort(lengthTemp)[-1]
    elif size >= 4: return np.sort(lengthTemp)[-2:].sum()

#%%
for key in dataRecord.keys():
    dataRecord[key]['data'] = {}
    dataRecord[key]['data']['mesh'] = vedo.Mesh(dataRecord[key]['mesh']).c('w').wireframe().alpha(1)
    dataRecord[key]['data']['mslice'] = getSlices(dataRecord[key]['data']['mesh'])
    
beforeIdx = rotate(beforeIdx, -1)
afterIdx = rotate(afterIdx, -1)
vmesh1 = dataRecord[beforeIdx[0]]['data']['mesh'].clone() # Antes
vmesh2 = dataRecord[afterIdx[0]]['data']['mesh'].clone() # Depois
plt.show((vmesh1, vmesh2), resetcam=True, interactive=False, mode=9, zoom=.8, )
#plt.show((vmesh1, vmesh2), resetcam=True, interactive=False, zoom=.8)

#%%  
textDateBefore = vedo.Text2D(dataRecord[beforeIdx[0]]['date'], font='Comae', pos=(0.375,0.9), justify='center')
textDateAfter = vedo.Text2D(dataRecord[afterIdx[0]]['date'], font='Comae', pos=(0.125,0.9), justify='center')
mslices1 = dataRecord[beforeIdx[0]]['data']['mslice']
mslices2 = dataRecord[afterIdx[0]]['data']['mslice']
contour1 = getContour(mslices=mslices1, dx=-500, color='red', idx=idx)
contour2 = getContour(mslices=mslices2, dx=-1500, color='grey', idx=idx)
slice2D1 = getSlice2D(mslices=mslices1, x=1000, color='red', idx=idx)
slice2D2 = getSlice2D(mslices=mslices2, x=1000, color='grey', idx=idx)
vmesh1.x(-500)
vmesh2.x(-1500)

plt.add([textDateBefore, textDateAfter]+contour1+contour2+slice2D1+slice2D2)

#%%
textBefore, textAfter, textRatio = None, None, None
def setLengthText():
    global textBefore, textAfter, textRatio
    txt1 = getLength(dataRecord[beforeIdx[0]]['data']['mslice'][idx])
    txt2 = getLength(dataRecord[afterIdx[0]]['data']['mslice'][idx])
    ratio = (txt2/txt1 - 1)*100 if txt1 != 0 else 0.0

    textBefore = vedo.Text2D(f'{txt1:.0f} cm', font='Comae', pos=(0.65,0.2), justify='center')
    textAfter = vedo.Text2D(f'{txt2:.0f} cm', font='Comae', pos=(0.75,0.2), justify='center')
    textRatio = vedo.Text2D(f'{ratio:.0f} %', font='Comae', pos=(0.85,0.2), justify='center').c('lime' if ratio <= 0 else 'red')

setLengthText()
caption1 = vedo.Circle().clone2D(pos=[0.675, 0.17], coordsys=3, c='red', alpha=.65, scale=0.01)
caption2 = vedo.Circle().clone2D(pos=[0.78, 0.17], coordsys=3, c='grey', alpha=.65, scale=0.01)
plt.add((textBefore, textAfter, textRatio, caption1, caption2,
        vedo.Text2D('Antes', font='Comae', pos=(0.65,0.15), justify='center'), 
        vedo.Text2D('Depois', font='Comae', pos=(0.75,0.15), justify='center'), 
        vedo.Text2D('Razão', font='Comae', pos=(0.85,0.15), justify='center')))

#%%
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
    global idx, contour1, contour2, slice2D1, slice2D2, angle, textBefore, textAfter, textRatio
    idx = int(widget.GetRepresentation().GetValue())
    
    plt.remove(contour1+contour2+slice2D1+slice2D2+[textBefore,textAfter,textRatio])

    setLengthText()
    
    contour1 = getContour(mslices=mslices1, dx=-500, color='red', idx=idx)
    contour2 = getContour(mslices=mslices2, dx=-1500, color='grey', idx=idx)
    slice2D1 = getSlice2D(mslices=mslices1, x=1000, color='red', idx=idx)
    slice2D2 = getSlice2D(mslices=mslices2, x=1000, color='grey', idx=idx)
    
    for actor1,actor2 in zip(contour1, contour2):
        actor1.rotateY(angle, locally=True)
        actor2.rotateY(angle, locally=True)
        
    plt.add(contour1+contour2+slice2D1+slice2D2+[textBefore,textAfter,textRatio])

def keyfunc(evt):
    if evt.keyPressed=='q':
        plt.close()  

def updateMeshBefore():
    global vmesh1, mslices1, contour1, slice2D1, textDateBefore
    textDateBefore = vedo.Text2D(dataRecord[beforeIdx[0]]['date'], font='Comae', pos=(0.375,0.9), justify='center')
    vmesh1 = dataRecord[beforeIdx[0]]['data']['mesh'].clone()
    mslices1 = dataRecord[beforeIdx[0]]['data']['mslice']
    contour1 = getContour(mslices=mslices1, dx=-500, color='red', idx=idx)
    slice2D1 = getSlice2D(mslices=mslices1, x=1000, color='red', idx=idx)
    vmesh1.x(-500)
    
def btnPrevBefore():
    global beforeIdx, vmesh1, mslice1, contour1, slice2D1, slice2D2, textDateBefore, textBefore, textAfter, textRatio
    beforeIdx = rotate(beforeIdx, 1)
    plt.remove([vmesh1, textDateBefore]+contour1+slice2D1+slice2D2+[textBefore,textAfter,textRatio])
    updateMeshBefore()
    rotateMeshesBefore(dtheta=angle)
    setLengthText()
    plt.add([vmesh1, textDateBefore]+contour1+slice2D1+slice2D2+[textBefore,textAfter,textRatio])
    
def btnNextBefore():
    global beforeIdx, vmesh1, mslice1, contour1, slice2D1, slice2D2, textDateBefore, textBefore, textAfter, textRatio
    beforeIdx = rotate(beforeIdx, -1)
    plt.remove([vmesh1, textDateBefore]+contour1+slice2D1+slice2D2+[textBefore, textAfter, textRatio])
    updateMeshBefore()
    rotateMeshesBefore(dtheta=angle)
    setLengthText()
    plt.add([vmesh1, textDateBefore]+contour1+slice2D1+slice2D2+[textBefore, textAfter, textRatio])

def updateMeshAfter():
    global vmesh2, mslices2, contour2, slice2D2, textDateAfter
    textDateAfter = vedo.Text2D(dataRecord[afterIdx[0]]['date'], font='Comae', pos=(0.125,0.9), justify='center')
    vmesh2 = dataRecord[afterIdx[0]]['data']['mesh'].clone()
    mslices2 = dataRecord[afterIdx[0]]['data']['mslice']
    contour2 = getContour(mslices=mslices2, dx=-1500, color='grey', idx=idx)
    slice2D2 = getSlice2D(mslices=mslices2, x=1000, color='grey', idx=idx)
    vmesh2.x(-1500)
    
def btnPrevAfter():
    global afterIdx, vmesh2, mslice2, contour2, slice2D1, slice2D2, textDateAfter, textBefore, textAfter, textRatio
    afterIdx = rotate(afterIdx, 1)
    plt.remove([vmesh2, textDateAfter]+contour2+slice2D2+slice2D1+[textBefore, textAfter, textRatio])
    updateMeshAfter()
    rotateMeshesAfter(dtheta=angle)
    plt.add([vmesh2, textDateAfter]+contour2+slice2D1+slice2D2+[textBefore, textAfter, textRatio])
    
def btnNextAfter():
    global afterIdx, vmesh2, mslice2, contour2, slice2D1, slice2D2, textDateAfter, textBefore, textAfter, textRatio
    afterIdx = rotate(afterIdx, -1)
    plt.remove([vmesh2, textDateAfter]+contour2+slice2D2+slice2D1+[textBefore, textAfter, textRatio])
    updateMeshAfter()
    rotateMeshesAfter(dtheta=angle)
    setLengthText()
    plt.add([vmesh2, textDateAfter]+contour2+slice2D1+slice2D2+[textBefore, textAfter, textRatio])

plt.addButton(btnPrevAfter, pos=(0.05, 0.90), states=["<"], c=["w"], bc=['none'], font="courier", size=22)
plt.addButton(btnNextAfter, pos=(0.20, 0.90), states=[">"], c=["w"], bc=['none'], font="courier", size=22)
plt.addButton(btnPrevBefore, pos=(0.30, 0.90), states=["<"], c=["w"], bc=['none'], font="courier", size=22)
plt.addButton(btnNextBefore, pos=(0.45, 0.90), states=[">"], c=["w"], bc=['none'], font="courier", size=22)

plt.addSlider2D(slider, 0, 100, value=50, pos=([0.25,0.15], [0.25,0.85]))
plt.addCallback('KeyPress', keyfunc)
plt.addCallback("timer", addAngle)
plt.timerCallback("create", dt=1)

vedo.interactive()