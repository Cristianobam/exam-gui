import vedo
import numpy as np

from util import *
from area import *
from ger import *

angle = 0
idx = 50
dataRecord = {'0':{'date':'17 Jan 21', 'mesh':'data/afinese_1.ply', 'gender':'male', 'height':169, 'weight':81, 'age':45},
              '1':{'date':'18 Jul 21', 'mesh':'data/afinese_2.ply', 'gender':'male', 'height':169, 'weight':81, 'age':45},
              '2':{'date':'19 Ago 21', 'mesh':'data/afinese_3.ply', 'gender':'male', 'height':169, 'weight':81, 'age':45},
              '3':{'date':'20 Set 21', 'mesh':'data/afinese_4.ply', 'gender':'male', 'height':169, 'weight':81, 'age':45}}
                         
beforeIdx = list(dataRecord.keys())
afterIdx = list(dataRecord.keys())
plt = vedo.Plotter(bg='#E4E9E9', sharecam=False, size='fullscreen')  

for key in dataRecord.keys():
    dataRecord[key]['data'] = {}    
    dataRecord[key]['data']['mesh'] = vedo.Mesh(dataRecord[key]['mesh']).c('#EFF0F1').alpha(1)  
    
beforeIdx = rotate(beforeIdx, -1)
afterIdx = rotate(afterIdx, 0)
vmesh1 = dataRecord[beforeIdx[0]]['data']['mesh'].clone() # Antes
vmesh2 = dataRecord[afterIdx[0]]['data']['mesh'].clone() # Depois

plane = vedo.Plane(pos=(500,-500,0), normal=(1,0,0), sx=500,sy=2000).alpha(0.0)
point = [100000, 0, 0]
sa = vmesh1.clone().cutWithPlane(origin=(0, 0, 0), normal=(1, 0, 0)).projectOnPlane(plane, point=point).c('m').alpha(0)
sb = vmesh2.clone().cutWithPlane(origin=(0, 0, 0), normal=(1, 0, 0)).projectOnPlane(plane, point=point).c('m').alpha(0)
sagital_before = sb.silhouette('2d').c('red').rotateY(-90).x(+560)
sagital_after = sa.silhouette('2d').c('grey').rotateY(-90).x(+560)

plt.show((vmesh1, vmesh2, sagital_before, sagital_after), resetcam=True, interactive=False, zoom=.8, title='AfinTech Scanners 3D', mode=9)

textDateBefore = vedo.Text2D(dataRecord[beforeIdx[0]]['date'], font='Comae', pos=(0.375,0.9), justify='center')
textDateAfter = vedo.Text2D(dataRecord[afterIdx[0]]['date'], font='Comae', pos=(0.125,0.9), justify='center')
vmesh1.x(-560)
vmesh2.x(-1700)

plt.add([textDateBefore, textDateAfter])
textBefore, textAfter, textRatio = None, None, None

def setLengthText():
    global textBefore, textAfter, textRatio

setLengthText()
plt.add((textBefore, textAfter, textRatio, 
        vedo.Text2D('Peso Total', font='Comae', pos=(0.65,0.95), justify='center'), 
        vedo.Text2D('Massa Gorda', font='Comae', pos=(0.75,0.95), justify='center'), 
        vedo.Text2D('Massa Magra', font='Comae', pos=(0.85,0.95), justify='center'),
        vedo.Text2D('Perdeu 2,3kg', font='Comae', pos=(0.65,0.92), justify='center'), 
        vedo.Text2D('Perdeu 6,3%', font='Comae', pos=(0.75,0.92), justify='center'), 
        vedo.Text2D('Ganhou 6,1%', font='Comae', pos=(0.85,0.92), justify='center'),
        vedo.Text2D('-1,6%', font='Comae', pos=(0.65,0.895), justify='center'), 
        vedo.Text2D('-16,8%', font='Comae', pos=(0.75,0.895), justify='center'), 
        vedo.Text2D('10,3%', font='Comae', pos=(0.85,0.895), justify='center')))


p1 = vedo.Picture(runPlotExample(300)).x(750).y(-500)
plt.add(p1)


p2 = vedo.Picture(plotTableGET(dpi=280, **dataRecord[beforeIdx[0]])).x(750).y(-1600)
plt.add(p2)

def rotateMeshesBefore(dtheta):
    vmesh1.rotateY(dtheta, locally=True)

def rotateMeshesAfter(dtheta):
    vmesh2.rotateY(dtheta, locally=True)
    
def addAngle(event):
    global angle
    angle = angle + .5 if angle <= 359 else 0
    rotateMeshesBefore(dtheta=.5)
    rotateMeshesAfter(dtheta=.5)
    plt.render()
       
def keyfunc(evt):
    if evt.keyPressed=='q':
        plt.close()  

def updateMeshBefore():
    global vmesh1, textDateBefore, textBefore, textAfter, textRatio, sagital_before, sagital_after
    plt.remove([vmesh1, textDateBefore, textBefore, textAfter, textRatio, sagital_before, sagital_after])
    textDateBefore = vedo.Text2D(dataRecord[beforeIdx[0]]['date'], font='Comae', pos=(0.375,0.9), justify='center')
    vmesh1 = dataRecord[beforeIdx[0]]['data']['mesh'].clone()
    
    plane = vedo.Plane(pos=(500,-500,0), normal=(1,0,0), sx=500,sy=2000).alpha(0.0)
    point = [100000, 0, 0]
    sb = vmesh1.clone().cutWithPlane(origin=(0, 0, 0), normal=(1, 0, 0)).projectOnPlane(plane, point=point).c('m').alpha(0)
    sagital_before = sb.silhouette('2d').c('red').rotateY(-90).x(+560)
    
    vmesh1.x(-560)
    rotateMeshesBefore(dtheta=angle)
    setLengthText()
    plt.add([vmesh1, textDateBefore, textBefore, textAfter, textRatio, sagital_before, sagital_after])
    
def btnPrevBefore():
    global beforeIdx
    beforeIdx = rotate(beforeIdx, 1)
    updateMeshBefore()
    
def btnNextBefore():
    global beforeIdx
    beforeIdx = rotate(beforeIdx, -1)
    updateMeshBefore()
    
def updateMeshAfter():
    global vmesh2, textDateAfter, textBefore, textAfter, textRatio, sagital_before, sagital_after
    plt.remove([vmesh2, textDateAfter, textBefore, textAfter, textRatio, sagital_before, sagital_after])
    textDateAfter = vedo.Text2D(dataRecord[afterIdx[0]]['date'], font='Comae', pos=(0.125,0.9), justify='center')
    vmesh2 = dataRecord[afterIdx[0]]['data']['mesh'].clone()
    
    plane = vedo.Plane(pos=(500,-500,0), normal=(1,0,0), sx=500,sy=2000).alpha(0.0)
    point = [100000, 0, 0]
    sa = vmesh2.clone().cutWithPlane(origin=(0, 0, 0), normal=(1, 0, 0)).projectOnPlane(plane, point=point).c('m').alpha(0)
    sagital_after = sa.silhouette('2d').c('grey').rotateY(-90).x(+560)    
    
    vmesh2.x(-1700)
    rotateMeshesAfter(dtheta=angle)
    plt.add([vmesh2, textDateAfter, textBefore, textAfter, textRatio, sagital_before, sagital_after])
    
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

plt.addCallback('KeyPress', keyfunc)
#plt.addCallback("timer", addAngle)
plt.timerCallback("create", dt=1)

vedo.interactive()