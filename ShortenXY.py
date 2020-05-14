# -*- coding: utf-8 -*-
"""
Created on Thu May 14 10:21:00 2020

@author: Jacob.Brown
"""

import sys

class GeoFile(object):
    '''
    A class of the HEC-RAS geo file
    '''
    def __init__(self):
        self.path_to_file = None
        self.og_lines = []
        self.new_lines = []
        
    def read_in_file(self, path_to_file):
        self.path_to_file = path_to_file
        
        with open(path_to_file, 'r') as in_file:
            for line in in_file:
                self.og_lines.append(line)
                
    def shorten_xy(self, num_characters):
        '''
        Amends the xy coordinates of cross sections so that there are fewer
        than 16 characters for each xy pair. Rhis is done by keeping the first
        num_characters of the coordinate
        
        The line is then re-written with the shortened xy pairs with spacing 
        between them

        Parameters
        -------
        num_characters = int
            the maximum number of characters a coordinate can have

        Returns
        -------
        None.
        '''
        
        # a switch used to tell when to edit the xy
        editing_xy = False
        
        for line in self.og_lines:
            if line.split('=')[0] == 'XS GIS Cut Line':
                editing_xy = True
                self.new_lines.append(line)
                continue 
            
            if line.split('=')[0] == 'Node Last Edited Time':
                editing_xy = False
            
            if line.split('=')[0] == '#Sta/Elev':
                editing_xy = False
            
            # split up the line into its xy components
            # if a component is more than 16 characters long, remove the 
            # last character. Then re-write everything to a string 
            if editing_xy == True:
                print(line)
                line = line.strip('\n')
                og_points = [line[i:i+16] for i in range(0, len(line), 16)]
                amended_points = []
                for p in og_points:
                    p = p.strip()
                    if len(p) < 16:
                        amended_points.append(p)
                    else:
                        amended_points.append(p[:num_characters])
                new_line = ''
                for ap in amended_points:
                    new_line += ap.rjust(16, ' ')
                new_line += '\n'
                print(new_line)
                self.new_lines.append(new_line)
            else:
                self.new_lines.append(line)
                
    def write_new_lines(self, out_file):
        '''
        Writes the new lines to a geo file

        Parameters
        ----------
        out_file : string
            The path to where the new file should be written

        Returns
        -------
        None.

        '''
        
        with open(out_file, 'w') as out:
            for line in self.new_lines:
                out.write(line)

def main(in_file, out_file, num_chars):
    in_geo = GeoFile()
    in_geo.read_in_file(in_file)
    in_geo.shorten_xy(num_chars)
    in_geo.write_new_lines(out_file)

if __name__ == '__main__':
    original_file = 'C:/C_PROJECTS/Misc/RAS/SCFHAD4.g02'
    
    out_geofile = 'C:/C_PROJECTS/Misc/RAS/test.g02'

    NUM_CHARS = 15
    
    main(original_file, out_geofile, NUM_CHARS)