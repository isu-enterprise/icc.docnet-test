

def configuration(config, **settings):
    config.load_zcml("configure.zcml")
    config.load_zcml("webapp.zcml")
