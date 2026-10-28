import AppKit
import UniformTypeIdentifiers
final class ScanApp: NSObject, NSApplicationDelegate {
 var window:NSWindow!;var status:NSTextField!;var button:NSButton!;var process:Process?;var resolution:NSPopUpButton!;var colorMode:NSPopUpButton!
 func applicationDidFinishLaunching(_ notification:Notification) {
  let menu=NSMenu();let root=NSMenuItem();menu.addItem(root);let sub=NSMenu();sub.addItem(withTitle:"Beenden",action:#selector(NSApplication.terminate(_:)),keyEquivalent:"q");root.submenu=sub;NSApp.mainMenu=menu
  window=NSWindow(contentRect:NSRect(x:0,y:0,width:600,height:350),styleMask:[.titled,.closable,.miniaturizable],backing:.buffered,defer:false);window.title="DCP-7055 Scan 0.2 - Testversion";window.center()
  let title=NSTextField(labelWithString:"Brother DCP-7055");title.font=NSFont.boldSystemFont(ofSize:25);title.frame=NSRect(x:28,y:290,width:540,height:34)
  let detail=NSTextField(wrappingLabelWithString:"USB · A4-Vorlage\nNutzbarer Bereich ca. 210 × 291 mm. Vorlage nach unten einlegen und Deckel schließen.");detail.frame=NSRect(x:28,y:220,width:545,height:60)
  let dpiLabel=NSTextField(labelWithString:"Auflösung");dpiLabel.frame=NSRect(x:28,y:182,width:130,height:22)
  resolution=NSPopUpButton(frame:NSRect(x:160,y:177,width:170,height:30));resolution.addItems(withTitles:["100 dpi","150 dpi","200 dpi","300 dpi","400 dpi","600 dpi"]);resolution.selectItem(withTitle:"300 dpi")
  let modeLabel=NSTextField(labelWithString:"Farbmodus");modeLabel.frame=NSRect(x:28,y:140,width:130,height:22)
  colorMode=NSPopUpButton(frame:NSRect(x:160,y:135,width:270,height:30));colorMode.addItems(withTitles:["Farbe (24 Bit)","Graustufen (8 Bit)"])
  button=NSButton(title:"Seite scannen …",target:self,action:#selector(scan));button.bezelStyle = .rounded;button.frame=NSRect(x:28,y:88,width:200,height:36)
  status=NSTextField(wrappingLabelWithString:"Bereit. Der Scanner muss per USB angeschlossen sein.");status.frame=NSRect(x:28,y:18,width:505,height:58)
  for v in [title,detail,dpiLabel,modeLabel,resolution!,colorMode!,button!,status!] {window.contentView!.addSubview(v)}
  window.makeKeyAndOrderFront(nil);NSApp.activate(ignoringOtherApps:true)
 }
 @objc func scan() {
  let panel=NSSavePanel();panel.allowedContentTypes=[.png];panel.nameFieldStringValue="Scan-"+ISO8601DateFormatter().string(from:Date()).replacingOccurrences(of:":",with:"-")+".png";panel.canCreateDirectories=true
  guard panel.runModal() == .OK,let output=panel.url,let resources=Bundle.main.resourceURL else{return}
  let dpi=Int(resolution.titleOfSelectedItem!.split(separator:" ")[0])!;let color=colorMode.indexOfSelectedItem==0
  let temp=FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString+".pnm")
  let log=FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString+".log")
  FileManager.default.createFile(atPath:log.path,contents:nil);guard let logHandle=try? FileHandle(forWritingTo:log) else{return}
  button.isEnabled=false;resolution.isEnabled=false;colorMode.isEnabled=false;status.stringValue="Scan läuft: \(dpi) dpi, \(color ? "Farbe" : "Graustufen"). Bitte warten …"
  let p=Process();process=p;p.executableURL=resources.appendingPathComponent("bin/dcp-scan");p.arguments=[temp.path,String(dpi),color ? "color" : "gray"]
  var env=ProcessInfo.processInfo.environment;env["BRSCAN_DATA_DIR"]=resources.appendingPathComponent("Data").path;p.environment=env;p.standardError=logHandle;p.standardOutput=FileHandle.nullDevice
  p.terminationHandler={ [weak self] proc in
   try? logHandle.close();let details=(try? String(contentsOf:log,encoding:.utf8)) ?? ""
   DispatchQueue.main.async {
    guard let self=self else{return};self.button.isEnabled=true;self.resolution.isEnabled=true;self.colorMode.isEnabled=true;self.process=nil
    defer {try? FileManager.default.removeItem(at:temp);try? FileManager.default.removeItem(at:log)}
    guard proc.terminationStatus==0 else {self.status.stringValue="Scan fehlgeschlagen. USB-Verbindung und Gerät prüfen.";let a=NSAlert();a.messageText="Scan fehlgeschlagen";a.informativeText=String(details.suffix(1500));a.runModal();return}
    do {try self.writePNG(temp,output,dpi)
     if details.contains("BRSCAN_INCOMPLETE_LINES=") {self.status.stringValue="Gespeichert. Achtung: Am unteren Rand wurden fehlende Zeilen weiß ergänzt. Testversion."}
     else {self.status.stringValue="Scan gespeichert: "+output.lastPathComponent}
     NSWorkspace.shared.open(output)
    } catch {self.status.stringValue="Speichern fehlgeschlagen: "+error.localizedDescription}
   }
  }
  do {try p.run()} catch {try? logHandle.close();button.isEnabled=true;resolution.isEnabled=true;colorMode.isEnabled=true;status.stringValue=error.localizedDescription}
 }
 func writePNG(_ input:URL,_ output:URL,_ dpi:Int)throws {
  let data=try Data(contentsOf:input);var pos=0;var lines:[String]=[]
  for _ in 0..<3 {guard let end=data[pos...].firstIndex(of:10),let line=String(data:data[pos..<end],encoding:.ascii) else{throw NSError(domain:"PGM",code:1)};lines.append(line);pos=end+1}
  let dims=lines[1].split(separator:" ").compactMap{Int($0)}
  let samples=lines[0]=="P6" ? 3 : 1
  guard (lines[0]=="P5" || lines[0]=="P6"),lines[2]=="255",dims.count==2,dims[0]>0,dims[1]>0,data.count-pos==dims[0]*dims[1]*samples,let rep=NSBitmapImageRep(bitmapDataPlanes:nil,pixelsWide:dims[0],pixelsHigh:dims[1],bitsPerSample:8,samplesPerPixel:samples,hasAlpha:false,isPlanar:false,colorSpaceName:samples==3 ? .deviceRGB : .deviceWhite,bytesPerRow:dims[0]*samples,bitsPerPixel:8*samples),let dst=rep.bitmapData else{throw NSError(domain:"PGM",code:2)}
  _ = data.withUnsafeBytes{raw in memcpy(dst,raw.baseAddress!.advanced(by:pos),dims[0]*dims[1]*samples)}
  rep.size=NSSize(width:Double(dims[0])*72/Double(dpi),height:Double(dims[1])*72/Double(dpi))
  guard let png=rep.representation(using:.png,properties:[:]) else{throw NSError(domain:"PNG",code:1)};try png.write(to:output,options:.atomic)
 }
 func applicationShouldTerminateAfterLastWindowClosed(_ sender:NSApplication)->Bool{return true}
 func applicationShouldTerminate(_ sender:NSApplication)->NSApplication.TerminateReply {
  if process != nil {let a=NSAlert();a.messageText="Ein Scan läuft noch.";a.informativeText="Bitte den Scan abwarten, bevor du die Anwendung beendest.";a.runModal();return .terminateCancel};return .terminateNow
 }
}
let app=NSApplication.shared;app.setActivationPolicy(.regular);let delegate=ScanApp();app.delegate=delegate;app.run()
