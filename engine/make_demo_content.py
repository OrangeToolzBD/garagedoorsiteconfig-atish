import json, os, re
ROOT=os.path.dirname(os.path.abspath(__file__))
sites={s["domain"]:s for s in json.load(open("config/sites.json",encoding="utf-8"))["sites"]}
demo=json.load(open(os.path.join(os.path.dirname(ROOT),"_demo5.json")))
def slug(t): return re.sub(r"[^a-z0-9]+","-",t.lower()).strip("-")

def home(city,st,brand):
    return {"title":f"Garage Door Repair in {city}, {st} | {brand}",
      "meta":f"Local garage door repair, spring and opener service, and new-door installation across {city}, {st}. Same-day service, licensed techs, upfront pricing.",
      "h1":f"Garage Door Repair & Installation in {city}, {st}",
      "sections":[
        {"h2":"what_we_do","body":f"{brand} handles garage door repair, spring and opener service, and full door replacement across {city} and the surrounding area. One local crew, upfront written pricing, and same-day service on most repairs.\n\n- Broken and worn torsion springs\n- Openers, remotes and safety sensors\n- Off-track doors, cables and rollers\n- New insulated door installation"},
        {"h2":"why_local_matters","body":f"Doors around {city} take a beating from the local climate and age, and the hardware fails in predictable ways. Because we work here every day, we can usually tell you what is wrong before we are in the driveway, and whether a repair or a replacement is the smarter spend."}],
      "faq":[
        {"q":f"Do you offer same-day garage door repair in {city}?","a":f"Yes. Most repair calls in {city} are handled the same or next day, and broken springs and doors stuck open are prioritized."},
        {"q":"How much does a repair cost?","a":"It depends on the part - a spring, cable, roller or opener are all different jobs. You get a written price on site before any work starts."},
        {"q":"Is replacing a spring a DIY job?","a":"No. Torsion springs are wound under high tension and can cause serious injury. It is the one job we always recommend leaving to a tech."}],
      "schema_facts":{"areaServed":f"{city}, {st} and surrounding communities"}}

def svc(city,st,brand,cslug,name,h1,blurb):
    return {"title":f"{name} in {city}, {st} | {brand}","meta":blurb,"h1":h1,
      "sections":[
        {"h2":"what_to_expect","body":blurb+f" A tech inspects the door, explains the fix, and gives you a written price before starting."},
        {"h2":"why_us","body":f"Licensed and insured, upfront pricing, and same-day service on most {name.lower()} calls across {city}."}],
      "faq":[{"q":f"How fast can you help in {city}?","a":"Most jobs are same or next day."},
             {"q":"Do you charge for a quote?","a":"You get a written price on site before any work begins."}],
      "schema_facts":{"areaServed":f"{city}, {st}"}}

def nb(city,st,area):
    return {"title":f"Garage Door Service in {area} - {city}, {st}","meta":f"Garage door repair and installation in {area}, {city}. Same-day service, local techs.",
      "h1":f"Garage Door Service in {area}","sections":[
        {"h2":"serving_the_neighborhood","body":f"We cover {area} and the rest of {city} for garage door repair, spring and opener service, and new-door installation. Same-day service on most repairs, with a written price before we start."}],
      "faq":[{"q":f"Do you serve {area}?","a":f"Yes - {area} is inside our regular {city} service area."}],
      "schema_facts":{"areaServed":f"{area}, {city}, {st}"}}

def top(city,st,gslug,h1,body):
    return {"title":f"{h1} | {city} Garage Door Guide","meta":body[:150],"h1":h1,
      "sections":[{"h2":"the_short_version","body":body}],
      "faq":[{"q":"Need help now?","a":f"Call for same-day garage door service in {city}, {st}."}],
      "schema_facts":{"areaServed":f"{city}, {st}"}}

for domain in demo:
    s=sites[domain]; city=s["city"]; st=s["st"]; brand=s["brand"]; cont=s["content"]; cs=slug(city)
    pre=re.sub(r"[^a-z0-9]","",city.lower())
    d=os.path.join(ROOT,"content",cont); os.makedirs(d,exist_ok=True)
    W=lambda fn,obj: json.dump(obj,open(os.path.join(d,fn),"w",encoding="utf-8"),indent=1)
    W(f"{pre}-home.json",home(city,st,brand))
    W(f"{pre}-svc-garage-door-repair-{cs}-{st.lower()}.json",svc(city,st,brand,cs,"Garage Door Repair",f"Garage Door Repair in {city}, {st}",f"Broken springs, off-track doors and failing openers repaired across {city}."))
    W(f"{pre}-svc-garage-door-installation-{cs}-{st.lower()}.json",svc(city,st,brand,cs,"Garage Door Installation",f"New Garage Door Installation in {city}, {st}",f"Insulated steel and composite doors sized and installed for {city} homes."))
    W(f"{pre}-svc-garage-door-service-{cs}-{st.lower()}.json",svc(city,st,brand,cs,"Garage Door Service",f"Garage Door Service & Tune-Ups in {city}, {st}",f"Spring tension, roller and track service that keeps an older {city} door running quiet."))
    for area,aslug in [("Downtown","downtown"),("North Side","north-side"),("West End","west-end")]:
        W(f"{pre}-nb-{aslug}.json",nb(city,st,area))
    W(f"{pre}-top-why-a-door-goes-off-track.json",top(city,st,"why","Why a Garage Door Goes Off Track",f"Doors jump the track when a roller fails, a cable snaps, or the door is forced while an opener is fighting it. In {city} the fix is usually a roller and cable reset plus realignment - not a whole new door."))
    W(f"{pre}-top-noises-that-mean-something.json",top(city,st,"noise","Garage Door Noises and What They Mean",f"Grinding usually means rollers or bearings; a bang can be a spring; rattling is loose hardware. On an older {city} door, catching it early keeps a small repair from becoming a big one."))
    print(f"  {domain}: content/{cont}/  ({len(os.listdir(d))} files)")
print("done")
