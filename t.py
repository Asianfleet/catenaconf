from catenaconf import Catenaconf

cf = Catenaconf.load("config.xml")

print(Catenaconf.to_container(cf))