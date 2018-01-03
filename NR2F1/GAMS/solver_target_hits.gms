$include ./output_data/search_test.gms

Set remainingNodes(node);
remainingNodes(node) = allNodes(node) - targetValueN(node);
alias(node,node1);


Option Optcr=0;

Binary Variables
	x(edge)	edge in use?
	y(node)	node in use?
	sigma(path)	relevant path?;


Equations
*	onePath(node)		one path per target
	inUse1(edge,path)	sigma UB by x
	inUse2(edge)		x UB number of active paths
	nodeOn1(edge,node,node)	is the node relevant?
	nodeOn2(edge,node,node)	is the node relevant2?
	nodeCount(node)		is the node in any edges
	maxNodes		maximum number of nodes constraint
	targetEnd(node)         end with target
	interEnd(node)          no intermediates can come from reg;

*one path per target
*onePath(targetValueN(node)).. 0 =l= sum(pnode(node,path),sigma(path));

*if edge not relevant, sigma must be 0
inUse1(pedge(edge,path)) .. sigma(path) =l= x(edge);
inUse2(edge)..	x(edge) =l= sum(pedge(edge,path),sigma(path));

*edge can’t be relevant without node
nodeOn1(enode(edge,node,node1)).. x(edge) =l= y(node);
nodeOn2(enode(edge,node,node1)).. x(edge) =l= y(node1);

* node cannot be relevant if no edges 
nodeCount(node) .. y(node) =l= sum( (edge,node1)$(enode(edge,node,node1) or enode(edge,node1,node)), x(edge)); 


*node end
targetEnd(targetValueN(node)).. y(node) =l= sum(enode(regulatoryValueE(edge),node1,node),x(edge));

*intermediate node inputs 
interEnd(remainingNodes(node)).. 0 =e= sum(enode(regulatoryValueE(edge),node1,node),x(edge));

*total number of nodes
Variable relNodes	"count relevent nodes"; 
maxNodes .. relNodes =e= sum(targetValueN(node),y(node));

Model minNodeModel /all/;
solve minNodeModel using mip max relNodes; 


file results /"./gams_intermediates/results.txt"/;
results.pc=5;
put results;
*loop(path$(sigma.l(path)>0), put path.tl /);
loop(targetValueN(node)$(y.l(node)>0),put node.tl /);


