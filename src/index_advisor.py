import sys
from join_query import *
from simple_query import *

if __name__ == '__main__':

    file_name = str(sys.argv[1])
    f_in = open(file_name, 'r')
    f_out = open(file_name + "_result.sql", 'w')

    str = f_in.readline()
    i = 0
    while str != "":
        i += 1
        f_out.write('Query #{}:\n{}\n'.format(i, str))

        str = str.lower()
        try:
            if str.find(" join ") != -1:
                query = JoinQuery(sql_query=str)

                indexes = query.get_indexes()
                j = 0
                while j < len(indexes):
                    f_out.write("\nRecommendation #{}:\n".format(j // 2 + 1))

                    f_out.write(indexes[j].sql() + "\n")
                    f_out.write(indexes[j + 1].sql() + "\n")

                    j += 2

            else:
                query = SimpleQuery(sql_query=str)
                index = query.get_index()
                f_out.write(index.sql() + "\n")

        except Exception:
            f_out.write("Parse error\n\n")

        f_out.write("-----------------------\n\n")
        str = f_in.readline()



