
import gluclient.api as gluapi

server    = gluapi.GluServer("http://localhost:8001")
component = server.get_component ("TestComponent")
print component.get_all_services()

print "\n\nAll services...\n\n"

for sname, sdef in component.get_all_services().items():
    print "@@@@ sname = ", sdef

print "\n\nOne service...\n\n"

srv = component.get_service("blahblah")
print "@@@@ src: ", srv

print "\n\nOne service...\n\n"

srv = component.get_service("foobar")
print "@@@@ src: ", srv

print "\n\nPositional parameters...\n\n"

print srv.get_positional_param_names()

print "\n\n-------------------------------------------\n\n"

print "\n\nAll resource names...\n\n"

print server.get_all_resource_names()


print "\n\nAll resource names PLUS...\n\n"


print server.get_all_resource_names_plus()


print "\n\nOne resource...\n\n"

r = server.get_resource("MyJavaTestComponent")
print r

print "\n\n--------------------------------------------\n\n"

rt = component.get_resource_template()
#rt.set("api_key", "foo")
rt.params         = dict(api_key="bar")
rt.description    = "Some description"
rt.public         = False
rt.suggested_name = "somename"

r = rt.create_resource()
print r
print r.get_all_services()
s = r.get_service("blahblah")
print s
print s.access()



 
