"""Offizielle Kompatibilitäts-Badges (Google Find Hub / Apple Find My) in WEISS nachbauen.
Quelle: Screenshot der offiziellen Badges (source-screenshot.png, selbst bereitstellen; Poppins-TTFs in fonts/). Logos bleiben original:
- Google-Logo: exakt vermessene Vektor-Geometrie + Originalfarben (Abweichung zum Screenshot MAE 1.4/255)
- Apple-Find-My-Icon: Originalpixel aus dem Screenshot, hochskaliert, scharfe Kreiskante
Text + Rand: weiß (vorher schwarz). Hintergrund transparent."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import sys
FD='fonts/'
SRC=np.asarray(Image.open('source-screenshot.png').convert('RGB'))
S=int(sys.argv[1]) if len(sys.argv)>1 else 4
WHITE=(255,255,255)
COL={'TL':(85,135,240),'TR':(58,116,227),'BL':(55,113,56),'BR':(90,165,89),'R':(215,78,62),'Y':(240,190,56)}

def border(W,H,inset=1.5,rad=12.5,sw=1.25):
    ss=4; im=Image.new('L',(W*S*ss,H*S*ss),0); d=ImageDraw.Draw(im)
    k=S*ss; d.rounded_rectangle([inset*k-sw*k/2,inset*k-sw*k/2,(W-inset)*k+sw*k/2,(H-inset)*k+sw*k/2],radius=(rad+sw/2)*k,outline=255,width=max(1,round(sw*k)))
    a=im.resize((W*S,H*S),Image.LANCZOS)
    out=Image.new('RGBA',(W*S,H*S),WHITE+(0,)); out.putalpha(a); return out

def glogo(W,H,cx,cy,rh,rr,ro,ss=4):
    ys=(np.arange(H*S*ss)+0.5)/(S*ss); xs=(np.arange(W*S*ss)+0.5)/(S*ss)
    X,Y=np.meshgrid(xs,ys); dx=X-cx; dy=Y-cy; r=np.hypot(dx,dy)
    rgb=np.zeros(X.shape+(3,),np.float32); a=np.zeros(X.shape,np.float32)
    ring=(r>=rh)&(r<=rr); top=dy<0; left=dx<0; outer=(r>rr)&(r<=ro)
    for key,m in [('TL',ring&top&left),('TR',ring&top&~left),('BL',ring&~top&left),('BR',ring&~top&~left),('R',outer&top&~left),('Y',outer&~top&left)]:
        rgb[m]=COL[key]; a[m]=1
    pre=np.dstack([rgb*a[...,None],a]).reshape(H*S,ss,W*S,ss,4).mean((1,3))
    al=pre[...,3]; c=np.zeros_like(pre[...,:3]); nz=al>0; c[nz]=pre[...,:3][nz]/al[nz][:,None]
    return Image.fromarray(np.dstack([c,al*255]).clip(0,255).astype('uint8'),'RGBA')

def text_layer(W,H,txt,fontf,box,axes=None,fit='width',color=WHITE):
    """render txt so that its ink bbox matches box=(x0,y0,x1,y1) (source px, inclusive)"""
    x0,y0,x1,y1=box; tw=(x1-x0+1)*S; th=(y1-y0+1)*S
    def mk(size,track=0.0):
        f=ImageFont.truetype(fontf,max(1,int(round(size))))
        if axes: f.set_variation_by_axes(axes)
        # draw per char with tracking
        pad=int(size)
        im=Image.new('L',(int(size*len(txt)*1.2+track*len(txt))+2*pad,int(size*2)+2*pad),0); d=ImageDraw.Draw(im)
        x=pad
        for ch in txt:
            d.text((x,pad),ch,font=f,fill=255); x+=f.getlength(ch)+track
        bb=im.getbbox(); return im.crop(bb)
    if fit=='width':
        lo,hi=5.,400.
        for _ in range(30):
            m=(lo+hi)/2
            if mk(m).width<tw: lo=m
            else: hi=m
        g=mk(lo)
    else:  # height fit + tracking to width
        lo,hi=5.,400.
        for _ in range(30):
            m=(lo+hi)/2
            if mk(m).height<th: lo=m
            else: hi=m
        size=lo; tl,thh=0.,size
        for _ in range(30):
            m=(tl+thh)/2
            if mk(size,m).width<tw: tl=m
            else: thh=m
        g=mk(size,tl)
    g=g.resize((tw,th),Image.LANCZOS)
    lay=Image.new('RGBA',(W*S,H*S),color+(0,)); a=Image.new('L',(W*S,H*S),0); a.paste(g,(x0*S,y0*S)); lay.putalpha(a)
    return lay

def apple_icon(W,H,ox,oy,cx,cy,r):
    # original pixels, crop circle region, upscale, crisp circular alpha
    x0=int(np.floor(cx-r-2)); y0=int(np.floor(cy-r-2)); x1=int(np.ceil(cx+r+2)); y1=int(np.ceil(cy+r+2))
    crop=Image.fromarray(SRC[y0:y1,x0:x1]).resize(((x1-x0)*S,(y1-y0)*S),Image.LANCZOS)
    # replace edge pixels (mixed with screenshot bg) with nearest interior color: erode-fill
    arr=np.asarray(crop).astype(np.float32)
    hh,ww=arr.shape[:2]; yy,xx=np.mgrid[0:hh,0:ww]
    px=(xx+0.5)/S+x0; py=(yy+0.5)/S+y0; rr=np.hypot(px-cx,py-cy)
    # pull pixels in the outer 1.6 px band radially inward to avoid dark fringe
    band=rr>r-2.4
    k=(r-2.4)/np.maximum(rr,1e-6)
    src=np.asarray(Image.fromarray(arr.clip(0,255).astype('uint8')).filter(ImageFilter.GaussianBlur(S*0.6))).astype(np.float32)
    sx=((cx+(px-cx)*k-x0)*S-0.5).clip(0,ww-1).astype(int); sy=((cy+(py-cy)*k-y0)*S-0.5).clip(0,hh-1).astype(int)
    arr[band]=src[sy[band],sx[band]]
    ss=4; Y2,X2=np.mgrid[0:hh*ss,0:ww*ss]
    rr2=np.hypot((X2+0.5)/(S*ss)+x0-cx,(Y2+0.5)/(S*ss)+y0-cy)
    al=(rr2<=r).reshape(hh,ss,ww,ss).mean((1,3))
    ic=Image.fromarray(np.dstack([arr,al*255]).clip(0,255).astype('uint8'),'RGBA')
    lay=Image.new('RGBA',(W*S,H*S),(0,0,0,0)); lay.alpha_composite(ic,((x0-ox)*S,(y0-oy)*S)); return lay

def google():
    ox,oy,W,H=152,230,380,99
    im=border(W,H)
    im.alpha_composite(glogo(W,H,201.25-ox,279.72-oy,11.316,26.8,37.75))
    pb=FD+'Poppins-Bold.ttf'
    im.alpha_composite(text_layer(W,H,'Works with',pb,(239-ox,257-oy,354-ox,272-oy)))
    im.alpha_composite(text_layer(W,H,'Google’s Find Hub',pb,(237-ox,284-oy,512-ox,315-oy)))
    return im

def apple():
    ox,oy,W,H=553,230,381,99
    im=border(W,H)
    im.alpha_composite(apple_icon(W,H,ox,oy,604.0,279.5,32.75))
    sf='/System/Library/Fonts/SFNS.ttf'
    im.alpha_composite(text_layer(W,H,'Works with',sf,(648-ox,251-oy,760-ox,266-oy),axes=[100,28,400,400],fit='height'))
    im.alpha_composite(text_layer(W,H,'Apple Find My',sf,(650-ox,277-oy,912-ox,314-oy),axes=[100,28,400,400]))
    return im

if __name__=='__main__':
    g=google(); a=apple()
    g.save(f'badge-google-findhub-white-{S}x.png'); a.save(f'badge-apple-findmy-white-{S}x.png')
    print(g.size,a.size)
