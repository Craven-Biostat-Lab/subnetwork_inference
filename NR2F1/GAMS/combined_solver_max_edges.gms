$include ./output_data/search_test.gms
$include ./gams_intermediates/intermediates.gms
$include ./gams_intermediates/rnaintermediates.gms
$include ./gams_intermediates/truetargets.gms

Set remainingNodes(node);
remainingNodes(node) = allNodes(node) - targetValueN(node);
alias(node,node1);

Option Optcr=0;

Binary Variables
	x(edge)	edge in use?
	y(node)	node in use?
	sigma(path)	relevant path?;


Equations
	onePath(node)		one path per target
	inUse1(edge,path)	sigma UB by x
	inUse2(edge)		x UB number of active paths
	nodeOn1(edge,node,node)	is the node relevant?
	nodeOn2(edge,node,node)	is the node relevant2?
	nodeCount(node)		is the node in any edges
	maxNodes		maximum number of nodes constraint
	targetEnd(node)         end with target
	interEnd(node)          no intermediates can come from reg;

*one path per target
onePath(trueTargets(node)).. 1 =l= sum(pnode(node,path),sigma(path));

*if edge not relevant, sigma must be 0
inUse1(pedge(edge,path)) .. sigma(path) =l= x(edge);
inUse2(edge)..	x(edge) =l= sum(pedge(edge,path),sigma(path));

*edge can’t be relevant without node
nodeOn1(enode(edge,node,node1)).. x(edge) =l= y(node);
nodeOn2(enode(edge,node,node1)).. x(edge) =l= y(node1);

* node cannot be relevant if no edges 
nodeCount(node) .. y(node) =l= sum( (edge,node1)$(enode(edge,node,node1) or enode(edge,node1,node)), x(edge)); 


*node end
targetEnd(trueTargets(node)).. y(node) =l= sum(enode(regulatoryValueE(edge),node1,node),x(edge));

*intermediate node inputs 
interEnd(remainingNodes(node)).. 0 =e= sum(enode(regulatoryValueE(edge),node1,node),x(edge));

*manual constraint adjustment
$include ./gams_intermediates/rna_score.gms

*total number of nodes
Variable relNodes	"count relevent nodes"; 
maxNodes .. relNodes =e= sum(node,y(node));

Model minNodeModel /all/;
option MIP = cplex;
minNodeModel.optfile =1;

solve minNodeModel using mip min relNodes; 

* fix nodes

*Set chosen(node);
*chosen(node)=no;
*chosen(node)$(y.l(node)>0)=yes;

*y.fx(node)$(not chosen(node))=0;
*y.fx(node)$(chosen(node))=1;


*total weight of nodes
*Variable relRnaNodes    “count active edges”;
*Equation countRNA   “count active nodes”;
*countRNA .. relRnaNodes =e= sum(interRnaNodes,rw(interRnaNodes)*y(interRnaNodes));

*Model maxRNANodeScoreModel /all/;
*option MIP = cplex;
*maxRNANodeScoreModel.optfile=1;
*solve maxRNANodeScoreModel using mip max relRnaNodes;

* fix nodes

Set chosen(node);
chosen(node)=no;
chosen(node)$(y.l(node)>0)=yes;

y.fx(node)$(not chosen(node))=0;
y.fx(node)$(chosen(node))=1;


*total weight of nodes


Variable relGadgetNodes	“count active edges”;
Equation countGadget	“count active nodes”;
countGadget .. relGadgetNodes =e= sum(interNodes,w(interNodes)*y(interNodes));

Model maxGADGETNodeScoreModel /all/;
option MIP = cplex;
maxGADGETNodeScoreModel.optfile =1;
solve maxGADGETNodeScoreModel using mip max relGadgetNodes;

* fix nodes

Set chosen(node);
chosen(node)=no;
chosen(node)$(y.l(node)>0)=yes;

y.fx(node)$(not chosen(node))=0;
y.fx(node)$(chosen(node))=1;

Variable tlEdges	"count asctive edges";
Equation counttlEdges	"count edges";
counttlEdges .. tlEdges =e= sum(edge,x(edge));

Model maxEdge /all/;
option MIP = cplex;
maxEdge.optfile=1;
solve maxEdge using mip max tlEdges;


file results /"./final_output/final_results.txt"/;
results.pc=5;
put results;
loop(path$(sigma.l(path)>0), put path.tl /);



