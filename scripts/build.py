#!/usr/bin/env python3
"""Build local, unsigned macOS 27/arm64 installers from the published sources."""
from pathlib import Path
import hashlib, os, platform, plistlib, re, shutil, subprocess
ROOT=Path(__file__).resolve().parents[1]
BUILD=Path(os.environ.get('BROTHER_BUILD_DIR',str(ROOT/'build'))).resolve(); DIST=ROOT/'dist'
def run(*args):
 subprocess.run([str(x) for x in args],cwd=ROOT,check=True)
def copy(src,dst):
 dst=Path(dst);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
def strip(path):
 subprocess.run(['xattr','-cr',str(path)],check=True)
def sign(path):
 # Finder/iCloud may add bundle FinderInfo just after creation. Remove only
 # that non-code attribute and retry; never weaken executable signature checks.
 import time
 for attempt in range(5):
  subprocess.run(['xattr','-d','com.apple.FinderInfo',str(path)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  result=subprocess.run(['codesign','--force','--sign','-',str(path)],capture_output=True,text=True)
  subprocess.run(['xattr','-d','com.apple.FinderInfo',str(path)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  if result.returncode==0:return
  if 'resource fork, Finder information' not in result.stderr:break
  time.sleep(0.2)
 raise RuntimeError(result.stderr)
def verify(path):
 import time
 for attempt in range(5):
  subprocess.run(['xattr','-d','com.apple.FinderInfo',str(path)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  result=subprocess.run(['codesign','--verify','--deep','--strict',str(path)],capture_output=True,text=True)
  if result.returncode==0:return
  if 'Finder' not in result.stderr and 'resource fork' not in result.stderr:break
  time.sleep(0.2)
 raise RuntimeError(result.stderr)
def bundle_binary(path,libdir):
 """Use only relative bundle paths; strip CMake's absolute build RPATHs."""
 path=Path(path)
 if path.suffix=='.dylib':run('install_name_tool','-id','@loader_path/'+path.name,path)
 deps=subprocess.check_output(['otool','-L',str(path)],text=True).splitlines()[1:]
 for line in deps:
  dep=line.strip().split(' (')[0];base=Path(dep).name
  if (dep.startswith('/opt/homebrew/') or dep.startswith('@rpath/')) and (libdir/base).exists():
   prefix='@loader_path/' if path.suffix=='.dylib' else '@loader_path/../lib/'
   run('install_name_tool','-change',dep,prefix+base,path)
 load=subprocess.check_output(['otool','-l',str(path)],text=True)
 for rp in re.findall(r'cmd LC_RPATH\s+cmdsize \d+\s+path (.*?) \(offset',load):run('install_name_tool','-delete_rpath',rp,path)
 sign(path)
def pkg(root,identifier,version,out,app=False):
 args=['pkgbuild','--root',root,'--identifier',identifier,'--version',version,'--install-location','/','--ownership','recommended','--filter',r'(^|/)\._','--filter',r'(^|/)\.DS_Store$']
 if app:
  cp=BUILD/'components.plist';run('pkgbuild','--analyze','--root',root,cp)
  ds=plistlib.loads(cp.read_bytes())
  for d in ds:d.update(BundleIsRelocatable=False,BundleHasStrictIdentifier=True,BundleOverwriteAction='upgrade')
  cp.write_bytes(plistlib.dumps(ds));args+=['--component-plist',cp]
 strip(root)
 run('env','COPYFILE_DISABLE=1',*args,out)
def product(title,components,out):
 """One visible choice installs all components. No scripts or queue mutations."""
 from xml.sax.saxutils import escape
 refs=''.join(f'<pkg-ref id="{ident}" version="{version}">{name}</pkg-ref>' for ident,version,name in components)
 choices=''.join(f'<pkg-ref id="{ident}"/>' for ident,_,_ in components)
 d=BUILD/(out.stem+'.xml')
 d.write_text(f'''<?xml version="1.0"?><installer-gui-script minSpecVersion="2"><title>{escape(title)}</title><options customize="never" require-scripts="false" hostArchitectures="arm64"/><domains enable_localSystem="true" enable_currentUserHome="false" enable_anywhere="false"/><volume-check><allowed-os-versions><os-version min="27.0"/></allowed-os-versions></volume-check><choices-outline><line choice="all"/></choices-outline><choice id="all" title="{escape(title)}">{choices}</choice>{refs}</installer-gui-script>''')
 run('productbuild','--distribution',d,'--package-path',BUILD/'packages',out)
if platform.system()!='Darwin' or platform.machine()!='arm64':raise SystemExit('Requires Apple Silicon macOS 27, Xcode Command Line Tools and Homebrew build dependencies.')
if int(platform.mac_ver()[0].split('.')[0])<27:raise SystemExit('Requires macOS 27 or later for this build recipe.')
BUILD.mkdir(exist_ok=True);DIST.mkdir(exist_ok=True)
for name in ['packages','Icon.iconset']: (BUILD/name).mkdir(exist_ok=True)
flags=f'-Wno-int-conversion -Wno-incompatible-pointer-types -Wno-implicit-function-declaration -ffile-prefix-map="{ROOT}=."'
# DCP printing
run('cmake','-S',ROOT/'vendor/brlaser','-B',BUILD/'brlaser','-DCMAKE_BUILD_TYPE=Release','-DCMAKE_OSX_ARCHITECTURES=arm64','-DCMAKE_OSX_DEPLOYMENT_TARGET=27.0',f'-DCMAKE_CXX_FLAGS=-ffile-prefix-map="{ROOT}=."')
run('cmake','--build',BUILD/'brlaser','-j','4');run('ctest','--test-dir',BUILD/'brlaser','--output-on-failure')
pr=BUILD/'printer-root';flt=pr/'Library/Printers/brlaser/Filter/rastertobrlaser'
copy(BUILD/'brlaser/rastertobrlaser',flt);sign(flt)
ppd=(BUILD/'brlaser/ppd/br7055.ppd').read_text();ppd=re.sub(r'^\*NickName:.*$', '*NickName: "Brother DCP-7055, brlaser 6.2.8 Apple Silicon"',ppd,flags=re.M);ppd='\n'.join(l for l in ppd.splitlines() if not l.startswith('*APICADriver:'))+'\n'
p=pr/'Library/Printers/PPDs/Contents/Resources/Brother-DCP-7055-brlaser-arm64.ppd';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(ppd)
copy(ROOT/'vendor/brlaser/COPYING',pr/'Library/Printers/brlaser/Documentation/COPYING.txt')
# QL printing
qr=BUILD/'ql-root';qf=qr/'Library/Printers/QL720/Filter/rastertoql720';qf.parent.mkdir(parents=True,exist_ok=True)
run('clang','-O2',f'-ffile-prefix-map={ROOT}=.','-I',ROOT/'src/ql',ROOT/'src/ql/ql-cups.c','-lcups','-o',qf);sign(qf)
run('ppdc','-d',BUILD/'ql-ppd',ROOT/'src/ql/ppd/QL-700.drv',ROOT/'src/ql/ppd/QL-720NW.drv')
for model,name in [('QL-700','ql700arm.ppd'),('QL-720NW','ql720arm.ppd')]:
 p=qr/f'Library/Printers/PPDs/Contents/Resources/Brother-{model}-Apple-Silicon.ppd';copy(BUILD/'ql-ppd'/name,p);run('cupstestppd','-I','filters',p)
copy(ROOT/'vendor/ptouch/COPYING',qr/'Library/Printers/QL720/Documentation/COPYING.txt')
# Scanner backend and self-contained app
run('cmake','-S',ROOT/'vendor/brscan','-B',BUILD/'scanner','-DCMAKE_BUILD_TYPE=Release','-DCMAKE_OSX_ARCHITECTURES=arm64','-DCMAKE_OSX_DEPLOYMENT_TARGET=27.0',f'-DCMAKE_C_FLAGS={flags}')
run('cmake','--build',BUILD/'scanner','-j','4')
app=BUILD/'scanner-root/Applications/DCP-7055 Scan.app';contents=app/'Contents';res=contents/'Resources';lib=res/'lib'
for d in [contents/'MacOS',res/'bin',lib]:d.mkdir(parents=True,exist_ok=True)
run('swiftc','-O','-module-cache-path',BUILD/'swift-cache',ROOT/'src/scanner/ScanApp.swift','-o',contents/'MacOS/DCP7055Scan')
run('clang',f'-ffile-prefix-map={ROOT}=.','-I',ROOT/'vendor/brscan/include',ROOT/'src/scanner/dcp-scan.c','-L',BUILD/'scanner','-lsane-brother',f'-Wl,-rpath,{BUILD}/scanner','-o',res/'bin/dcp-scan')
for name in ['libsane-brother.1.dylib','libbrscandec.1.dylib','libbrcolm.1.dylib']:copy(BUILD/'scanner'/name,lib/name)
for prefix,name in [('libusb','libusb-1.0.0.dylib'),('libusb-compat','libusb-0.1.4.dylib'),('jpeg-turbo','libjpeg.8.dylib')]:copy(Path('/opt/homebrew/opt',prefix,'lib',name),lib/name)
for alias,target in [('libbrscandec.dylib','libbrscandec.1.dylib'),('libbrcolm.dylib','libbrcolm.1.dylib')]:
 p=lib/alias
 if not p.exists():p.symlink_to(target)
copy(ROOT/'vendor/brscan/data/Brsane2.ini',res/'Data/Brsane2.ini')
shutil.copytree(ROOT/'vendor/brscan/libbrcolm/GrayCmData',res/'Data/GrayCmData',dirs_exist_ok=True)
shutil.copytree(ROOT/'licenses',res/'Licenses',dirs_exist_ok=True)
for name in ['Copying','copying.brother','copying.lib']:copy(ROOT/'vendor/brscan'/name,res/'Licenses'/name)
copy(ROOT/'LICENSE',res/'Licenses/Integration-GPL-2.txt');copy(ROOT/'UPSTREAM.md',res/'Licenses/UPSTREAM.md')
run('swiftc','-module-cache-path',BUILD/'swift-cache',ROOT/'src/scanner/MakeIcon.swift','-o',BUILD/'MakeIcon');run(BUILD/'MakeIcon',BUILD);run('iconutil','-c','icns',BUILD/'Icon.iconset','-o',res/'AppIcon.icns')
(contents/'Info.plist').write_bytes(plistlib.dumps({'CFBundleIdentifier':'org.local.dcp7055.scan','CFBundleName':'DCP-7055 Scan','CFBundleExecutable':'DCP7055Scan','CFBundlePackageType':'APPL','CFBundleShortVersionString':'0.3.0','CFBundleVersion':'4','CFBundleIconFile':'AppIcon.icns','LSMinimumSystemVersion':'27.0','NSHighResolutionCapable':True}))
strip(app)
for f in lib.glob('*.dylib'):
 if not f.is_symlink():bundle_binary(f,lib)
bundle_binary(res/'bin/dcp-scan',lib);sign(app);verify(app)
# Source-level decoder regression tests (no scanner access).
run('clang',ROOT/'tests/test_integration.c','-o',BUILD/'decoder-tests')
run(BUILD/'decoder-tests',lib/'libbrscandec.1.dylib',lib/'libbrcolm.1.dylib',ROOT/'vendor/brscan/libbrcolm/GrayCmData/YL4FB/brlutcm.dat')
run('clang','-I',ROOT/'vendor/brscan/libsane-brother',ROOT/'src/scanner/test-scanner-metadata.c',ROOT/'vendor/brscan/libsane-brother/brother_brscan4.c','-o',BUILD/'metadata-tests');run(BUILD/'metadata-tests')
run('clang','-I',ROOT/'vendor/brscan/include','-I',ROOT/'vendor/brscan/libsane-brother','-I','/opt/homebrew/opt/libusb-compat/include','-I','/opt/homebrew/include',ROOT/'tests/test_color_jpeg.c','-L',BUILD/'scanner','-lsane-brother',f'-Wl,-rpath,{BUILD}/scanner','-L','/opt/homebrew/lib','-ljpeg','-o',BUILD/'jpeg-tests');run(BUILD/'jpeg-tests')
# Validate PPD syntax, then package with root-owned files and non-relocatable app.
run('cupstestppd','-I','filters',pr/'Library/Printers/PPDs/Contents/Resources/Brother-DCP-7055-brlaser-arm64.ppd')
pkg(pr,'org.local.brlaser.dcp7055.arm64','6.2.8.2',BUILD/'packages/Printer.pkg')
pkg(BUILD/'scanner-root','org.local.dcp7055.scan','0.3.0',BUILD/'packages/Scanner.pkg',True)
pkg(qr,'org.local.brother.ql720.arm64','0.3.0',BUILD/'packages/QL.pkg')
product('Brother DCP-7055 – Drucken und Scannen',[('org.local.brlaser.dcp7055.arm64','6.2.8.2','Printer.pkg'),('org.local.dcp7055.scan','0.3.0','Scanner.pkg')],DIST/'Brother-DCP-7055-macOS27-arm64.pkg')
product('Brother QL-700 und QL-720NW',[('org.local.brother.ql720.arm64','0.3.0','QL.pkg')],DIST/'Brother-QL-700-720NW-macOS27-arm64.pkg')
(DIST/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in sorted(DIST.glob('*.pkg'))))
print('Built installers in',DIST)
