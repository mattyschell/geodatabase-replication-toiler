import sys
import os

if __name__ == "__main__":

    sqlfilein        = sys.argv[1]
    sqlfileout       = sys.argv[2]
    commitfrequency  = int(sys.argv[3])

    linekount = 0
    outlines = []

    if os.path.exists(sqlfileout):
        os.remove(sqlfileout)

    with open(sqlfilein) as sqlfileinhandle:

        for line in sqlfileinhandle:
            linekount += 1
            
            if ((linekount % commitfrequency) == 0
            and  line.endswith('),\n')):

                outlines.append(line.replace('),\n',');\n'))
                outlines.append('commit;\n')
                outlines.append('begin;\n')
                outlines.append('insert into subaddress values\n')
                
            else:

                outlines.append(line)

    with open(sqlfileout,'w') as sqlfileouthandle:

        for outline in outlines:

            if outline == outlines[-1]:

                sqlfileouthandle.write(outline.replace('),\n',');\n'))
                sqlfileouthandle.write('commit;\n')
                sqlfileouthandle.write('alter table subaddress drop constraint sub_address_id_uqc;\n')

            else:
                
                sqlfileouthandle.write(outline)
    exit(0)

