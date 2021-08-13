#!/usr/bin/env python3

from schutzenbergergraph import InverseMonoidPresentation, SchutzenbergerGraph


class Stephen:
    def __init__(self, presn: InverseMonoidPresentation):
        self.presn = presn
        self.orbit = [SchutzenbergerGraph(presn, "")]
        self.finished = False

    def run(self) -> None:
        if self.finished:
            return
        for sg1 in self.orbit:
            w = sg1.rep
            for x in range(len(self.presn.A)):
                xw = [x] + w
                sg_xw = SchutzenbergerGraph(self.presn, self.presn.string(xw))
                for sg2 in self.orbit:
                    if (
                        self.presn.string(xw) in sg2
                        and self.presn.string(sg2.rep) in sg_xw
                    ):
                        break
                else:
                    self.orbit.append(sg_xw)
        self.finished = True

    def size(self) -> int:
        self.run()
        result = 0
        for sg in self.orbit:
            result += sg.number_of_nodes()
        return result

    def number_of_r_classes(self) -> int:
        self.run()
        return len(self.orbit)
