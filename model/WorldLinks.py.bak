#from log import *

class WorldLinkData(object):
    def __init__(self):
        self._links = {}

    def addLink(self, w1, w2):
        world1 = str(w1)
        world2 = str(w2)
        if world1 not in self._links:
            self._links[world1] = [world2]
        elif world2 not in self._links[world1]:
            self._links[world1].append(world2)
                    
        if world2 not in self._links:
            self._links[world2] = [world1]
        elif world1 not in self._links[world2]:
            self._links[world2].append(world1)
        print self

    def removeLink(self, w1, w2):
        world1 = str(w1)
        world2 = str(w2)
        if world1 in self._links:
            if world2 in self._links[world1]:
                self._links[world1].remove(world2)
                if len(self._links[world1]) == 0:
                    del self._links[world1]

        if world2 in self._links:
            if world1 in self._links[world2]:
                self._links[world2].remove(world1)
                if len(self._links[world2]) == 0:
                    del self._links[world2]
        print self

    def rename(self, old_name, new_name):
        if old_name in self._links and new_name not in self._links:
            self._links[new_name] = self._links[old_name]
            #Rename world in counter-party lists
            for partner in self._links[old_name]:
                back_links = self._links[partner]
                self._links[partner][back_links.index(old_name)] = new_name
            del self._links[old_name]
        print self

    def linkExists(self, w1, w2):
        world1 = str(w1)
        world2 = str(w2)
        if world1 in self._links:
            if world2 in self._links[world1]:
                return True
        return False

    def linksFrom(self, world):
        if world in self._links:
            return self._links[world]
        else:
            return []

    def hasLinks(self, world):
        if world in self._links:
            return True
        else:
            return False

    @property
    def linkList(self):
        #Returns each bi-directional relationship only once,
        #which partner comes first in the entry is arbitrary.
        link_list = []
        for world in self._links:
            for partner in self._links[world]:
                if (partner, world) not in link_list:
                    link_list.append((world, partner))
        return link_list

    def __repr__(self):
        report = ''
        for world, links  in self._links.iteritems():
             report = report + str(world) + '\t' + str(links) + '\n'
        return report

if __name__ == '__main__':
    tl = WorldLinkData()
    tl.addLink('Goyal', 'Merka')
    tl.addLink('Goyal', 'Humiss')
    print 'Before\n', tl
    tl.rename('Goyal', 'Kenjiro')
    print 'After\n', tl
    

    
