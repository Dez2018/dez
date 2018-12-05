# dez
keep learning the world
This dem-fem-coupler example is based on the code of Jan Stranský which aimed to solve the problem of surface coupler.
I first ran the 'yade-preproc.py' to generate the geom of polyhedra with the file 'surf7-polyhedra.dat', and then I ran the 'surf7.sh' shell to run the project.
The project aimed to :
first step: to generate the sample of ballast just in YADE. 
second step: make DEM-FEM coupling and load on the last polyhedra which is the loading plate with sin function.
But I have met some problem of it.
The warning was shown as:
InsertionSortCollider.cpp:240 action: verletDist is set to 0 because no spheres were found. It will result in suboptimal performances, consider setting a positive verletDist in your script.
terminate called after throwing an instance of 'std::runtime_error'
  what():  Undefined or ambiguous IPhys dispatch for types FrictMat and PolyhedraMat.
Aborted (core dumped)
So what's the problem?
