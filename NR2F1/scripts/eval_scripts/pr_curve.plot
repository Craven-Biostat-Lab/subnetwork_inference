set term pdfcairo enhanced font "Gill Sans,7" lw 2 rounded size 4,6
 unset log 
 unset label 
 set autoscale
 set xtic auto 
 set ytic auto 
set size ratio .8
set pointsize .05
 set key top right

set style line 1 lt 2 lc rgb "#006633" lw 2 pt 1	 
set style line 2 lt 2 lc rgb "#CC9900" lw 2 pt 5
set style line 3 lt 2 lc rgb "#003399" lw 2 pt 2
set style line 4 lt rgb "#CC0099" lw 2 pt 4
set style line 5 lt rgb "#66CCCC" lw 2 pt 3
set style line 6 lt rgb "#993300" lw 2 pt 6
set style line 7 lt rgb "#FF6600" lw 2 pt 7

set xlabel font ", 10"
set ylabel font ", 10"
set key font ", 8"

set xr [0.0:1.0] 
set yr [0.0:1.0]  
set size ratio -1
# pr curves
set xlabel "Recall"
set ylabel "Precision

set output "breast_cancer_pr.pdf"

#set origin 0.0, 0.0
set multiplot layout 3,2 rowsfirst scale 1,1 title "Subnetwork inference results: predicting hits and interfaces"

# hits: 2413 
# total: 14534
# 815/13829: .166
set arrow 1 from 0,0.166 to 1,0.166 nohead lt 2



set title "Breast Cancer Subnetwork Inference"
plot "evals/results.opr" title "Baseline" with points ls 1, \
"evals/results.pr" title "" with lines ls 1, \





