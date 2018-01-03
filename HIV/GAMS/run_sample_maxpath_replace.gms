* Replace-friendly run file - Nov 2014
* Maximizes node score given additional node limit
* then maximizes paths among those nodes
*
* Text to replace: 
* Filenames: {ALL_SETS}, {SCORE_FILE}, {OUTPUT_FILE}, {MODEL}
* Floats (parameters): {CX_ODDS}, {MIN_NODE_OPT_TOL}, {MAX_PATH_OPT_TOL}
 
** Testing out the IP
* SHORTER VERSION: require 95% of hits and most interfaces
* Use a minimum number of nodes; prioritize by DK score
* Try to include all interfaces and hits
* For each min-node solution, maximize paths.
* So called "easy" because no directions are inferred.
*
* Complexes must be overrepresented 
* No special treatment of reactions 

$phantom null

* don't show input in listing file
$offlisting
* suppress listing and cross-reference of symbols
$offsymxref offsymlist
* equations and vars per block
option
	limrow = 0,
	limcol= 0;

* info for calculating odds ratios
Scalar cxOdds   "odds ratio required for complexes"     / {CX_ODDS} /;

* most sets
$Include {ALL_SETS}


* node, edge, path, and subgraph sets
* that are specific to the hit selection
* includes sets for hits and interfaces
$Include {SAMPLE_SETS}

* Constrain number of additional nodes added
Scalar addlimit / {LIMIT} /;

Scalar bgTotNodes "total GENES in human" / 20000 /;
display bgTotNodes;

* Upper limit of genes in inferred subnetwork
Scalar nodecard /0/;
nodecard = sum(node$(hit(node) or intNode(node)), 1) + addLimit;
display nodecard;

* read DK scores and hits to hide
$Include {SCORE_FILE}

Set activate(edge)	"activating edges",
	inhibit(edge)	"inhibitory edges",
	signed(edge)	"signed edges";
activate(edge)=no;
inhibit(edge)=no;
signed(edge)=activate(edge) or inhibit(edge);

$Include {MODEL}

Free variable hitCount	"number of active hits";
Equation activeHits	"count active hits";
activeHits .. sum(hit, y(hit)) =e= hitCount;

* require most hits
* Now, fix the hit count
Scalar maxActHit "active hits" / 0 /;
maxActHit = card(hit);

Equation setHitCount "set number of active hits";
setHitCount .. hitCount =g= 0.95 * maxActHit;

Free variable intCount "active interfaces";
Equation activeInts	"count active interface edges";
activeInts .. intCount =e= sum(intEdge(edge), x(edge));

* set int count within 5%
Scalar maxActInt	"required active interface edges" / 0 /;
maxActInt = card(intEdge);

Equation constrainIntCount "make sure we use close to the max number of interfaces and hits";
constrainIntCount .. intCount =g= 0.95*maxActInt;

Equation limitAddNodes "limit number of new genes added";
limitAddNodes .. addlimit =g= sum(node$novelGene(node), y(node));

* Finally, maximize the scores of those additional nodes
* Don't include reactions, complexes, or species in the calculation.

Free variable totScore	"sum of scores of novel gene nodes";
Equation countScore	"sum up scores of gene nodes";
countScore .. totScore =e= sum(node$novelGene(node), y(node)*score(node));

Model maxScore /all/;
Option MIP = Cplex;
maxScore.optcr = {MIN_NODE_OPT_TOL};
maxScore.reslim = 1000000;
maxScore.optfile = 1;
* one solution
solve maxScore max totScore using mip;

** FIX CHOSEN NODE SET chosen(node)
*
Set chosen(node);
chosen(node)=no;
chosen(node)$(y.l(node)>0)=yes;

* fix nodes

y.fx(node)$(not chosen(node))=0;
y.fx(node)$(chosen(node))=1;

Variable pathCt	"count total paths";
Equation countPaths	"do path counting";
countPaths .. pathCt =e= sum(path, sigma(path));

Model maxPath /all/;
Option MIP = Cplex;
maxPath.optcr = {MIN_NODE_OPT_TOL};
maxPath.reslim = 100000;
maxPath.optfile = 1;
* one sol
solve maxPath max pathCt using mip;

execute_unload '{OUTPUT_FILE}.gdx' x,y,sigma;

