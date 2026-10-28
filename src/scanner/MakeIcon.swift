import AppKit
func roundRect(_ r:NSRect,_ radius:CGFloat,_ color:NSColor){color.setFill();NSBezierPath(roundedRect:r,xRadius:radius,yRadius:radius).fill()}
func shape(_ pts:[NSPoint],_ color:NSColor){let p=NSBezierPath();p.move(to:pts[0]);for pt in pts.dropFirst(){p.line(to:pt)};p.close();color.setFill();p.fill()}
func render(_ size:Int,_ path:String){
 let rep=NSBitmapImageRep(bitmapDataPlanes:nil,pixelsWide:size,pixelsHigh:size,bitsPerSample:8,samplesPerPixel:4,hasAlpha:true,isPlanar:false,colorSpaceName:.deviceRGB,bytesPerRow:0,bitsPerPixel:0)!
 NSGraphicsContext.saveGraphicsState();NSGraphicsContext.current=NSGraphicsContext(bitmapImageRep:rep)
 NSGraphicsContext.current!.cgContext.scaleBy(x:CGFloat(size)/1024,y:CGFloat(size)/1024)
 let bg=NSBezierPath(roundedRect:NSRect(x:58,y:58,width:908,height:908),xRadius:205,yRadius:205)
 NSGradient(starting:NSColor(calibratedRed:0.10,green:0.49,blue:0.82,alpha:1),ending:NSColor(calibratedRed:0.035,green:0.16,blue:0.37,alpha:1))!.draw(in:bg,angle:-85)
 // Open lid, raised behind the flatbed.
 NSGraphicsContext.saveGraphicsState();let sh=NSShadow();sh.shadowColor=NSColor.black.withAlphaComponent(0.25);sh.shadowOffset=NSSize(width:0,height:-15);sh.shadowBlurRadius=20;sh.set()
 shape([NSPoint(x:215,y:575),NSPoint(x:260,y:825),NSPoint(x:790,y:825),NSPoint(x:830,y:575)],NSColor(calibratedWhite:0.78,alpha:1))
 NSGraphicsContext.restoreGraphicsState()
 shape([NSPoint(x:245,y:594),NSPoint(x:283,y:793),NSPoint(x:766,y:793),NSPoint(x:798,y:594)],NSColor(calibratedWhite:0.94,alpha:1))
 // Subtle hinge and scanner base.
 roundRect(NSRect(x:236,y:544,width:554,height:46),15,NSColor(calibratedWhite:0.24,alpha:1))
 NSGraphicsContext.saveGraphicsState();sh.shadowOffset=NSSize(width:0,height:-20);sh.shadowBlurRadius=24;sh.set()
 roundRect(NSRect(x:170,y:300,width:684,height:300),62,NSColor(calibratedWhite:0.77,alpha:1));NSGraphicsContext.restoreGraphicsState()
 roundRect(NSRect(x:170,y:356,width:684,height:244),52,NSColor(calibratedWhite:0.93,alpha:1))
 roundRect(NSRect(x:212,y:406,width:596,height:151),23,NSColor(calibratedRed:0.10,green:0.20,blue:0.27,alpha:1))
 // Document on the glass; cyan bar makes scanning recognizable.
 shape([NSPoint(x:310,y:419),NSPoint(x:348,y:536),NSPoint(x:682,y:536),NSPoint(x:718,y:419)],.white)
 roundRect(NSRect(x:307,y:463,width:413,height:9),4,NSColor(calibratedRed:0.12,green:0.82,blue:0.98,alpha:1))
 // Front panel and green ready button.
 roundRect(NSRect(x:216,y:326,width:490,height:18),9,NSColor(calibratedWhite:0.38,alpha:1))
 roundRect(NSRect(x:755,y:330,width:35,height:35),17.5,NSColor(calibratedRed:0.17,green:0.79,blue:0.43,alpha:1))
 // Small color swatches distinguish the scan application from a printer queue.
 for (i,c) in [NSColor.systemCyan,NSColor.magenta,NSColor.systemYellow].enumerated(){roundRect(NSRect(x:372+CGFloat(i)*93,y:212,width:70,height:22),11,c)}
 NSGraphicsContext.restoreGraphicsState()
 try! rep.representation(using:.png,properties:[:])!.write(to:URL(fileURLWithPath:path))
}
let outputRoot=CommandLine.arguments.count>1 ? CommandLine.arguments[1] : "build"
for s in [16,32,128,256,512]{render(s,"\(outputRoot)/Icon.iconset/icon_\(s)x\(s).png");render(s*2,"\(outputRoot)/Icon.iconset/icon_\(s)x\(s)@2x.png")}
render(512,"\(outputRoot)/AppIcon.png")
