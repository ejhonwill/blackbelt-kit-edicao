import subprocess,sys,os
D=sys.argv[1]; O=D+"/cortes"
C=[("REAL_MJ_01","MJ_rockwithyou",19.6,0.45),("REAL_MJ_02","MJ_cork1988",61,0.4),("REAL_MJ_03","MJ_offthewall",38,0.5),("REAL_MJ_04","MJ_cork1988",91,0.5),("REAL_MJ_05","MJ_rockwithyou",196,0.5),
("REAL_ALI_01","ALI_training",99.5,0.3),("REAL_ALI_02","ALI_training",75.5,0.45),("REAL_ALI_03","ALI_training",81.3,0.5),
("REAL_PHELPS_01","PHELPS_ritual",0.4,0.4),("REAL_PHELPS_02","PHELPS_ritual",18.2,0.5),("REAL_PHELPS_03","PHELPS_journey",98.5,0.5),("REAL_PHELPS_04","PHELPS_rule",61,0.4),
("REAL_CARREY_01","CARREY_oprah",124,0.5),("REAL_CARREY_02","CARREY_oprah",133,0.5)]
for nm,src,t,xc in (C if len(sys.argv)<3 else [c for c in C if c[0] in sys.argv[2:]]):
    vf=f"crop=trunc(ih*9/16/2)*2:ih:max(0\\,min(iw-ih*9/16\\,iw*{xc}-ih*9/32)):0,scale=1080:1920:flags=lanczos,setsar=1,fps=25"
    subprocess.run(["ffmpeg","-v","error","-ss",str(t),"-t","5","-i",f"{D}/{src}.mp4","-vf",vf,"-an","-c:v","libx264","-crf","16","-pix_fmt","yuv420p",f"{O}/{nm}.mp4","-y"],check=True)
    print(nm,"ok")
