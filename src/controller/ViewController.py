from src.model.DataTest import DataTest
import json

class ViewController:
    def __init__(self):
        self.DataTest = DataTest()
    

    def front_analyze(self):
        raw = self.DataTest.get()
        
        ret = []
        for row in raw:
            ret.append({
                'original_image': row['base_path']+'/original.png',
                'keypoint_image': row['base_path']+'/keypoint.png', 

            })
        return ret
