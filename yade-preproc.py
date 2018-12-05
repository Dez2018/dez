from yade import pack,export
from yade import polyhedra_utils
from yade import geom,utils
from yade import qt
from yade import *

global stepnum

matP = PolyhedraMat()
matP.density = 2600 #kg/m^3 
matP.young = 2e7
matP.poisson = 0.21 # real 0.21
matP.frictionAngle = 0.6

matF = PolyhedraMat()
matF.density = 2600 #kg/m^3 
matF.young = 2e7
matF.poisson = 0.21 # real 0.21
matF.frictionAngle = 0.6

#matP = O.materials.append(PolyhedraMat(young=2e7,density=2600,poisson=0.21))
#matS = O.materials.append(FrictMat(young=2e7,poisson=0.21,density=2500))
#matF = O.materials.append(FrictMat(young=2e7,poisson=0.21,density=2500))

global stepnum
stepnum=1
##add walls
#left wall
O.bodies.append(utils.facet(((0.17,0.17,0.601),(0.17,0.40,0.601),(0.17,0.17,1.2)),dynamic=None,fixed=True,material=matF))
O.bodies.append(utils.facet(((0.17,0.40,0.601),(0.17,0.40,1.2),(0.17,0.17,1.2)),dynamic=None,fixed=True,material=matF))
#right wall
O.bodies.append(utils.facet(((0.40,0.17,0.601),(0.40,0.40,0.601),(0.40,0.17,1.2)),dynamic=None,fixed=True,material=matF))
O.bodies.append(utils.facet(((0.40,0.40,0.601),(0.40,0.40,1.2),(0.40,0.17,1.2)),dynamic=None,fixed=True,material=matF))
#front wall
O.bodies.append(utils.facet(((0.17,0.17,0.601),(0.40,0.17,0.601),(0.17,0.17,1.2)),dynamic=None,fixed=True,material=matF))
O.bodies.append(utils.facet(((0.40,0.17,0.601),(0.40,0.17,1.2),(0.17,0.17,1.2)),dynamic=None,fixed=True,material=matF))
#behind wall
O.bodies.append(utils.facet(((0.17,0.40,0.601),(0.40,0.40,0.601),(0.17,0.40,1.2)),dynamic=None,fixed=True,material=matF))
O.bodies.append(utils.facet(((0.40,0.40,0.601),(0.40,0.40,1.2),(0.17,0.40,1.2)),dynamic=None,fixed=True,material=matF))

#wall below
O.bodies.append(utils.facet(((0.0,0.0,0.6),(0.57,0.0,0.6),(0.57,0.57,0.6)),dynamic=None,fixed=True,material=matF))
O.bodies.append(utils.facet(((0.0,0.0,0.6),(0.0,0.57,0.6),(0.57,0.57,0.6)),dynamic=None,fixed=True,material=matF))

## add polyhedron
ballast=polyhedra_utils.fillBox((0.17,0.17,0.6),(0.40,0.40,0.8),matP,sizemin=[0.026,0.026,0.026],sizemax=[0.038,0.038,0.038],ratio=[1,1,1],seed=4,mask=1)

#O.bodies.append(wall((0,0,0),2))

O.engines =[
	ForceResetter(),
	InsertionSortCollider([Bo1_Polyhedra_Aabb(),Bo1_Wall_Aabb(),Bo1_Facet_Aabb()]),
	InteractionLoop(
		[Ig2_Wall_Polyhedra_PolyhedraGeom(),Ig2_Polyhedra_Polyhedra_PolyhedraGeom(),Ig2_Facet_Polyhedra_PolyhedraGeom(),Ig2_Sphere_Sphere_ScGeom()],
		[Ip2_PolyhedraMat_PolyhedraMat_PolyhedraPhys(),Ip2_FrictMat_PolyhedraMat_FrictPhys(),Ip2_FrictMat_FrictMat_FrictPhys()],
		[Law2_PolyhedraGeom_PolyhedraPhys_Volumetric()],
	),
	NewtonIntegrator(damping=0.3,gravity=(0,0,-9.81),label='newton'),
	PyRunner(command='Step()',iterPeriod=1,label='step')
]

def Step():
	from yade import polyhedra_utils,export
	global stepnum
	vim=min([b.state.vel[2] for b in O.bodies if isinstance(b.shape,Polyhedra)])
	if O.iter<500:return
	if vim < -0.05:return
	if stepnum == 1:
		pmax=max([b.state.pos[2] for b in O.bodies if isinstance(b.shape,Polyhedra)])+0.036
		lp=polyhedra_utils.polyhedra(matP,v=((0.175,0.175,pmax),(0.395,0.175,pmax),(0.395,0.395,pmax),(0.175,0.395,pmax),(0.175,0.175,pmax+0.02),(0.395,0.175,pmax+0.02),(0.395,0.395,pmax+0.02),(0.175,0.395,pmax+0.02)),fixed=False,color=(0.6,0.6,0.6))
		O.bodies.append(lp)
		lpnum=O.bodies[-1].id
		O.bodies[lpnum].state.blockedDOFs='xyXYZ'
		O.bodies[lpnum].state.vel=(0,0,-0.01)
		stepnum=stepnum+1
	elif stepnum == 2:
		lpnum=O.bodies[-1].id
		plateforce=O.forces.f(lpnum)[2]
		if plateforce < 1:return
		O.bodies[lpnum].state.vel=(0,0,0)
		export.textPolyhedra('/tmp/surf7-polyhedra.dat')
		O.pause()

#O.periodic = True
O.dt = 0.0005

qt.Controller()
V = qt.View()
V.screenSize = (550,450)
V.sceneRadius = 1
V.eyePosition = (0.7,0.5,0.1)
V.upVector = (0,0,1)
V.lookAt = (0.15,0.15,0.1)

#O.dt = PWaveTimeStep()
O.run()

#export.text(base+'-polyhedra.dat')

