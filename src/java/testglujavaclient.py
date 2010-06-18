from org.mulesource.glu.clientapi import GluServer
server = GluServer("http://localhost:8001")

component = server.getComponent("TestComponent")
print component.getAllServices()

rt = component.getResourceTemplate()
rt.set("api_key", "bar")
rt.setDescription("Some description")
rt.setSuggestedName("somename")
r = rt.createResource()

print r.getAllServices()
s = r.getService("blahblah")
res = s.access()
print res.status
print res.data

r.delete()


