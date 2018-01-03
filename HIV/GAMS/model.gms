****
* GAMS IP for updated HIV project: fall 2014.

* Easy version: don't care about direction? or sign.
* Complexes must be overrepresented.
* Special way of incorporating complex proteins into paths.
*
* Reactions are not special in this representation.
****

**** Aliases*******
alias(node,node1);
alias(edge,edge1);

Binary variables
	y(node)	"Node relevance"
	v(node)	"Node phenotype label"
	x(edge)	"Edge relevance"
	d(edge)	"Edge direction"
	act(edge)	"Activating"
	inh(edge)	"Inhibitory"
	sigma(path)	"Path relevance";

************** Equations *************

** Node phenotypes - none for now.
v.fx(node)=0;

** Local equations

* Nodes: must be in active edge
* Edges: in active path OR, for subgraph edges, having one node in an active path

Set snode(node)	"nodes in subgraph";
snode(node)=no;
loop(subnode(subgraph,node), snode(node)=yes;);

Set sedge(edge)	"edges in subgraph";
sedge(edge)=no;
loop(subedge(subgraph,edge), sedge(edge)=yes;);

* Special edges don't require paths and are for interpretation only
* Fill in with run file.
Set specialEdge(edge) "special fixed edges";
specialEdge(edge)=no;

Equations
	nodeOn1(edge,node,node)	"edge active only if first node active"
	nodeOn2(edge,node,node)	"edge active only if second node active"
	edgeOn(node)	"nodes active only if edge active";
nodeOn1(enode(edge,node,node1)) ..	x(edge) =l= y(node);
nodeOn2(enode(edge,node,node1)) ..	x(edge) =l= y(node1);
edgeOn(node) .. y(node) =l= sum( (edge, node1)$(enode(edge,node,node1) or enode(edge,node1,node)), x(edge));

Equations	
	pathEdge1(edge,path)	"path is only as active as each edge"
	pathEdge2(edge)	"edge must have at least one active path OR be in a subgraph";
pathEdge1(pedge(edge,path)) .. sigma(path) =l= x(edge);

* non-subgraph edges must have at least one active path
* or - they could be in a special set of edges that we include for interpretation
* reasons.
pathEdge2(edge)$(not sedge(edge) and not specialEdge(edge)) .. x(edge) =l= sum(pedge(edge,path), sigma(path));

* subgraph edges are only active if at least one of their nodes has an active path
Equation subEdgeActive(edge,node,node1)	"subgraph edges active if one node in active path";
subEdgeActive(enode(edge,node,node1))$sedge(edge) .. x(edge) =l= sum(pedge(edge,path), sigma(path)) + sum(pnode(node,path), sigma(path)) + sum(pnode(node1,path), sigma(path));

** Global equations

* Complexes must be overrepresented relative to background network
* By including 1-y(node) for the complex, we toggle to de-activating the complex if insufficient nodes are present.
Equation meetOdds(node) "active complexes must have at least a min ratio of active nodes (RHS >= 1)";
meetOdds(node)$(complexFeatureN(node)) .. sum(cxprot(node, node1), y(node1))/ complexSize(node) + (1-y(node)) =g= cxOdds * nodecard / bgTotNodes;

