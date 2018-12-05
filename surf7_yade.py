######################################################################
#
# Python script (input file for YADE). Creates some DEM particles to
# "bombard" OOFEM mesh
#
######################################################################
from libyade import yade
from yade import geom,utils
from yade import polyhedra_utils
from yade import ymport,timing
from yade import pack,export
from yade import *
from math import *
#usePolyhedra = True
#Initial is False
# basic material

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

O.bodies.append(ymport.textPolyhedra('surf7-polyhedra.dat',material=matP))

load=O.bodies[-1].id
O.forces.setPermF(O.bodies[-1].id,(0,0,-3-1*sin(2*pi*O.time)))

O.engines =[
	ForceResetter(),
	InsertionSortCollider([Bo1_Polyhedra_Aabb(),Bo1_Facet_Aabb()]),
	InteractionLoop(
		[Ig2_Wall_Polyhedra_PolyhedraGeom(),Ig2_Polyhedra_Polyhedra_PolyhedraGeom(),Ig2_Facet_Polyhedra_PolyhedraGeom()],
		[Ip2_PolyhedraMat_PolyhedraMat_PolyhedraPhys()],
		[Law2_PolyhedraGeom_PolyhedraPhys_Volumetric()],
	),
	NewtonIntegrator(damping=0.3,gravity=(0,0,-9.81),label='newton')
]


#O.periodic = True

def vtkExport(i):
	name = '/tmp/surf7_yade'
	from yade import export
	export.VTKExporter(name,i).exportFacets()
	export.VTKExporter(name,i).exportPolyhedra()





