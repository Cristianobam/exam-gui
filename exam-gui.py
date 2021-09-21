#%%
import vedo
import numpy as np

#%%
angle = 0
idxInit = 50
plt = vedo.Plotter(bg='k', sharecam=False)

#%%
vmesh1 = vedo.Mesh('data/afinese_antes.ply').c('w').wireframe().alpha(1)
vmesh2 = vedo.Mesh('data/afinese_depois.ply').c('w').wireframe().alpha(1)
plt.show((vmesh1, vmesh2), resetcam=True, interactive=False, mode=9, zoom=.8)

def getSlices(vmesh, num:int=100):
    mesh = vedo.vedo2trimesh(vmesh)
    bounds = mesh.bounds
    dx, dy, dz = bounds[1]-bounds[0]
    heights = np.linspace(0, dy, num)
    mslices = mesh.section_multiplane([0,bounds[0][1],0],[0,1,0],heights=heights)
    return np.array([dx,dy,dz]), mslices

bounds1, mslices1 = getSlices(vmesh1)
bounds2, mslices2 = getSlices(vmesh2)

#%%
def getContour(mslices, dx=0, dy=0, dz=0, color='red', idx:int=50):
    contour = vedo.trimesh2vedo(mslices[idx].to_3D()).actors
    contour = [actor.c(color).lw(5).shift(dx,dy,dz) for actor in contour]
    return contour

def getSlice2D(mslices, x=0, y=0, z=0, color='green', idx:int=50):
    slice2D = vedo.trimesh2vedo(mslices[idx]).actors
    slice2D = [actor.x(x).y(y).z(z).c(color).rotateZ(90, locally=True) for actor in slice2D]
    return slice2D

contour1 = getContour(mslices=mslices1, dx=-1500, color='red', idx=idxInit)
contour2 = getContour(mslices=mslices2, dx=-500, color='red', idx=idxInit)
slice2D1 = getSlice2D(mslices=mslices1, x=1000, color='red', idx=idxInit)
slice2D2 = getSlice2D(mslices=mslices2, x=1000, color='white', idx=idxInit)
vmesh1.x(-1500)
vmesh2.x(-500)

plt.add(contour1+contour2+slice2D1+slice2D2)

#%%
txt1, txt2 = round(mslices1[idxInit].length, 2), round(mslices2[idxInit].length, 2)
ratio = txt2/txt1 - 1 if txt1 != 0 else 0.0

text1 = vedo.Text2D(f'{txt1} cm', font='Comae', pos=(0.65,0.2), justify='center')
text2 = vedo.Text2D(f'{txt2} cm', font='Comae', pos=(0.75,0.2), justify='center')
text3 = vedo.Text2D(f'{ratio:.4f} %', font='Comae', pos=(0.85,0.2), justify='center').c('lime' if ratio <= 0 else 'red')

caption1 = vedo.Circle().clone2D(pos=[0.675, 0.17], coordsys=3, c='red', alpha=.65, scale=0.01)
caption2 = vedo.Circle().clone2D(pos=[0.78, 0.17], coordsys=3, c='white', alpha=.65, scale=0.01)
plt.add((text1, text2, text3, caption1, caption2,
        vedo.Text2D('Antes', font='Comae', pos=(0.65,0.15), justify='center'), 
        vedo.Text2D('Depois', font='Comae', pos=(0.75,0.15), justify='center'), 
        vedo.Text2D('Razão', font='Comae', pos=(0.85,0.15), justify='center')))

#%%
def rotateMeshes(event):
    global angle
    angle = angle + .5 if angle <= 359 else 0
    for actor1,actor2 in zip(contour1, contour2):
        actor1.rotateY(.5, locally=True)
        actor2.rotateY(.5, locally=True)
    vmesh1.rotateY(.5, locally=True)
    vmesh2.rotateY(.5, locally=True)
    plt.render()

def slider(widget, event):
    global contour1, contour2, slice2D1, slice2D2, angle, text1, text2, text3
    idx = int(widget.GetRepresentation().GetValue())
    
    plt.remove(contour1+contour2+slice2D1+slice2D2+[text1,text2,text3])

    txt1, txt2 = round(mslices1[idx].length, 2), round(mslices2[idx].length, 2)
    ratio = txt2/txt1 - 1 if txt1 != 0 else 0.0

    text1 = vedo.Text2D(f'{txt1} cm', font='Comae', pos=(0.65,0.2), justify='center')
    text2 = vedo.Text2D(f'{txt2} cm', font='Comae', pos=(0.75,0.2), justify='center')
    text3 = vedo.Text2D(f'{ratio:.4f} %', font='Comae', pos=(0.85,0.2), justify='center').c('lime' if ratio <= 0 else 'red')
    
    contour1 = getContour(mslices=mslices1, dx=-1500, color='red', idx=idx)
    contour2 = getContour(mslices=mslices2, dx=-500, color='red', idx=idx)
    slice2D1 = getSlice2D(mslices=mslices1, x=1000, color='red', idx=idx)
    slice2D2 = getSlice2D(mslices=mslices2, x=1000, color='white', idx=idx)
    
    for actor1,actor2 in zip(contour1, contour2):
        actor1.rotateY(angle, locally=True)
        actor2.rotateY(angle, locally=True)
        
    plt.add(contour1+contour2+slice2D1+slice2D2+[text1,text2,text3])

plt.addSlider2D(slider, 0, 100, value=50, pos=([0.265,0.15], [0.265,0.85]))
plt.addCallback("timer", rotateMeshes)
plt.timerCallback("create", dt=1)

vedo.interactive()