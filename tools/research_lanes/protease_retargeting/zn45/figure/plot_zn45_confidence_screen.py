"""Offline Zn45 screening scatter figure; ReportLab only, no model execution.

Usage: python plot_zn45_confidence_screen.py PATH/zn45_activity_af3_join.csv
Outputs go beside this script unless --outdir is supplied.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

from reportlab.graphics import renderPDF, renderSVG
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.shapes import Drawing, Group, Line, Rect, String
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.lib.colors import HexColor, Color, white

INK=HexColor('#16232B')
MUTED=HexColor('#56636E')
GRID=HexColor('#DEE4E8')
BLUE=HexColor('#0072B2')
ORANGE=HexColor('#D55E00')
GRAY=HexColor('#9AA4AC')
W,H=980,610
PLOT_Y,PLOT_H=192,252
YMIN,YMAX=-0.2,3.5


def pearson(rows,field):
    x=[r[field] for r in rows];y=[r['fold_over_wt'] for r in rows]
    mx=sum(x)/len(x);my=sum(y)/len(y)
    return sum((a-mx)*(b-my) for a,b in zip(x,y))/math.sqrt(sum((a-mx)**2 for a in x)*sum((b-my)**2 for b in y))


def text(d,x,y,value,size=11,color=INK,font='Helvetica',anchor='start'):
    d.add(String(x,y,value,fontName=font,fontSize=size,fillColor=color,textAnchor=anchor))


def make_figure(rows,stats):
    d=Drawing(W,H)
    d.add(Rect(0,0,W,H,fillColor=white,strokeColor=None))
    text(d,64,574,'AF3 confidence filters retain the strongest Zn45 screening signals',18,font='Helvetica-Bold')
    text(d,64,553,'Retrospective, single-scaffold data: model confidence has limited ranking value within the retained set.',11.2,color=MUTED)
    text(d,64,530,f"Joint rule: complex_plddt > 94 and ipae_min < 1.5    |    {stats['retained']}/{stats['total']} mutants retained    |    {stats['signals_retained']}/{stats['signals']} signals >1.5-fold retained",11.3,font='Helvetica-Bold')
    legend=[('Circle',GRAY,64,f"Excluded by joint rule (n={stats['excluded']})"),('FilledCircle',BLUE,370,f"Retained, <=1.5-fold (n={stats['retained_other']})"),('FilledDiamond',ORANGE,688,f"Retained, >1.5-fold signal (n={stats['signals_retained']})")]
    for kind,color,x,label in legend:
        marker=makeMarker(kind,size=6,fillColor=white if kind=='Circle' else color,strokeColor=color,strokeWidth=0.8)
        marker.x=x+4;marker.y=506;d.add(marker)
        text(d,x+15,502,label,10.3,color=MUTED)
    groups=[ [r for r in rows if not r['retained']], [r for r in rows if r['retained'] and r['fold_over_wt']<=1.5], [r for r in rows if r['retained'] and r['fold_over_wt']>1.5] ]
    panels=[('A','complex_plddt',88,87,97,[88,90,92,94,96],94,'Complex pLDDT','complex_plddt (mean over five model samples)'),('B','ipae_min',568,0.5,4.5,[0.5,1.5,2.5,3.5,4.5],1.5,'Minimum protein-substrate PAE','ipae_min (mean over five model samples)')]
    for letter,field,left,xmin,xmax,xticks,threshold,title,xlabel in panels:
        width=348
        text(d,left-23,473,letter,15,font='Helvetica-Bold')
        text(d,left,473,title,13,font='Helvetica-Bold')
        text(d,left,455,f"Retained-set Pearson r = {stats['pearson_retained'][field]:.3f}",10.5,color=MUTED)
        plot=LinePlot();plot.x=left;plot.y=PLOT_Y;plot.width=width;plot.height=PLOT_H
        plot.data=[[(r[field],r['fold_over_wt']) for r in group] for group in groups]
        plot.joinedLines=0
        plot.lines.lineStyle=None
        plot.fillColor=None;plot.strokeColor=None
        plot.xValueAxis.valueMin=xmin;plot.xValueAxis.valueMax=xmax;plot.xValueAxis.valueSteps=xticks
        plot.yValueAxis.valueMin=YMIN;plot.yValueAxis.valueMax=YMAX;plot.yValueAxis.valueSteps=[0,0.5,1,1.5,2,2.5,3,3.5]
        for axis in (plot.xValueAxis,plot.yValueAxis):
            axis.strokeColor=MUTED;axis.strokeWidth=0.7;axis.labels.fontName='Helvetica';axis.labels.fontSize=10;axis.labels.fillColor=MUTED
            axis.tickStrokeColor=MUTED;axis.tickStrokeWidth=0.7
        plot.xValueAxis.labels.dy=-8
        plot.yValueAxis.labels.dx=-7
        plot.yValueAxis.visibleGrid=1;plot.yValueAxis.gridStrokeColor=GRID;plot.yValueAxis.gridStrokeWidth=0.4
        plot.yValueAxis.gridStart=0;plot.yValueAxis.gridEnd=width
        plot.gridFirst=1
        styles=[('Circle',GRAY,4.1),('FilledCircle',BLUE,4.1),('FilledDiamond',ORANGE,6.3)]
        for i,(kind,color,size) in enumerate(styles):
            plot.lines[i].strokeColor=color
            plot.lines[i].symbol=makeMarker(kind,size=size,fillColor=white if kind=='Circle' else color,strokeColor=color,strokeWidth=0.6)
        d.add(plot)
        # Threshold guides are drawn above the fine grid, below an explanatory label.
        xx=left+(threshold-xmin)/(xmax-xmin)*width
        d.add(Line(xx,PLOT_Y,xx,PLOT_Y+PLOT_H,strokeColor=MUTED,strokeWidth=0.8,strokeDashArray=[4,4]))
        yy=PLOT_Y+(1.5-YMIN)/(YMAX-YMIN)*PLOT_H
        d.add(Line(left,yy,left+width,yy,strokeColor=ORANGE,strokeWidth=0.75,strokeDashArray=[3,4]))
        text(d,left+width/2,PLOT_Y-36,xlabel,11,anchor='middle')
        text(d,xx+5,PLOT_Y+PLOT_H-13,f'{threshold:g}',9,color=MUTED)
    label=Group()
    label.add(String(0,0,'Blank-corrected reporter RFU slope relative to WT (fold)',fontName='Helvetica',fontSize=11.2,fillColor=INK,textAnchor='middle'))
    label.translate(24,PLOT_Y+PLOT_H/2);label.rotate(90);d.add(label)
    text(d,64,119,'Each point is one mutant measured in one screening well; AF3 scores are means over five model samples.',10.3,color=MUTED)
    text(d,64,101,'The dashed horizontal line marks >1.5-fold screening signals. Fold is a blank-corrected reporter RFU slope ratio,',10.3,color=MUTED)
    text(d,64,83,'not kcat or a validated hit. Colors use both score thresholds; a point may fail the threshold shown in the other panel.',10.3,color=MUTED)
    text(d,64,57,'Source: Chen et al., Computational design of metalloproteases, bioRxiv v3 (2026-09-21); Zenodo 22654831.',9.3,color=MUTED)
    text(d,64,41,'Retrospective reanalysis of 378 Zn45 single-substitution records; no prospective validation or cross-scaffold claim.',9.3,color=MUTED)
    return d


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv',type=Path)
    parser.add_argument('--outdir',type=Path,default=Path(__file__).resolve().parent)
    args=parser.parse_args();payload=args.csv.read_bytes()
    rows=[]
    for r in csv.DictReader(payload.decode().splitlines()):
        row={k:float(r[k]) for k in ('complex_plddt','ipae_min','fold_over_wt')}
        row['well']=r['well'];row['design_name']=r['design_name'];row['retained']=row['complex_plddt']>94 and row['ipae_min']<1.5
        assert all(math.isfinite(row[k]) for k in ('complex_plddt','ipae_min','fold_over_wt'))
        rows.append(row)
    retained=[r for r in rows if r['retained']];signals=[r for r in rows if r['fold_over_wt']>1.5]
    stats={'input_csv':args.csv.name,'input_sha256':hashlib.sha256(payload).hexdigest(),'total':len(rows),'retained':len(retained),'excluded':len(rows)-len(retained),'signals':len(signals),'signals_retained':sum(r['retained'] for r in signals),'retained_other':sum(r['fold_over_wt']<=1.5 for r in retained),'pearson_retained':{f:pearson(retained,f) for f in ('complex_plddt','ipae_min')},'axes':{'complex_plddt':[87,97],'ipae_min':[0.5,4.5],'fold_over_wt':[YMIN,YMAX]},'data_ranges':{f:[min(r[f] for r in rows),max(r[f] for r in rows)] for f in ('complex_plddt','ipae_min','fold_over_wt')},'endpoint':'blank-corrected reporter RFU slope divided by WT slope; not kcat','replication':'one screening well per mutant; five AF3 model samples summarized as means','scope':'retrospective one-scaffold source dataset'}
    assert stats['total']==378 and stats['retained']==211 and stats['signals']==stats['signals_retained']==19
    assert round(stats['pearson_retained']['complex_plddt'],3)==0.254 and round(stats['pearson_retained']['ipae_min'],3)==-0.038
    for field,bounds in stats['axes'].items():
        assert bounds[0]<stats['data_ranges'][field][0] and bounds[1]>stats['data_ranges'][field][1]
    args.outdir.mkdir(parents=True,exist_ok=True)
    drawing=make_figure(rows,stats)
    svg=args.outdir/'zn45_confidence_screen_scatter.svg';renderSVG.drawToFile(drawing,str(svg))
    pdf=args.outdir/'zn45_confidence_screen_scatter.pdf'
    renderPDF.drawToFile(drawing,str(pdf))
    stats['pdf_sha256']=hashlib.sha256(pdf.read_bytes()).hexdigest()
    stats['svg_sha256']=hashlib.sha256(svg.read_bytes()).hexdigest()
    (args.outdir/'figure_receipt.json').write_text(json.dumps(stats,indent=2)+'\n')
    print(json.dumps(stats,indent=2))


if __name__=='__main__':
    main()
