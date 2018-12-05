#####################################################
#
# surface fem-dem coupling test
#
#####################################################

# import interfaces
import sys
import os
#
import liboofem
import libyade
from demfemcoupling import OofemInterface,YadeInterface,OofemYadeMeshSurfaceMap,FemDemSurfaceCoupler,TimeStep


def vtkExport(i,fem,dem):
	"""Do VTK export"""
	fem.vtkExport(i)
	dem.vtkExport(i)


# initialize both domains
femName = 'surf7_oofem'
demName = 'surf7_yade'
fem = OofemInterface(femName,liboofem)
dem = YadeInterface(demName,libyade)

# create coupler object
femSurf = fem.toUnstructuredGrid().getSurface()
demSurf = dem.addSurface(femSurf)
femDemMeshMap = OofemYadeMeshSurfaceMap(fem,dem,femSurf,demSurf)
coupler = FemDemSurfaceCoupler(fem,dem,femDemMeshMap,vtkExport)

# run the simulation dt for 0.005
nSteps,dt,output = 500,0.0005,5
coupler.solve(nSteps,dt,output)
